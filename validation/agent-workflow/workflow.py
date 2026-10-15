#!/usr/bin/env python3
"""AW offline preparation. No subprocess, provider, executor or score admission."""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
PACKAGE = Path(__file__).resolve().parent
ANCHOR = '132fef9b963a68c87faae045f1e2ef96201827f1f70a445616464fdb728011e8'
ARMS = ('A', 'B', 'C', 'D')


class WorkflowError(ValueError):
    pass


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()


def load(path):
    return json.loads(Path(path).read_bytes())


def plain(path):
    path = Path(path)
    if any(p.is_symlink() for p in (path, *path.parents)):
        raise WorkflowError('symlink forbidden: ' + str(path))
    return path


def tree(root):
    plain(root)
    return {p.relative_to(root).as_posix() for p in Path(root).rglob('*')
            if plain(p).is_file()}


def verify(package=PACKAGE):
    package = plain(package)
    if digest(plain(package / 'freeze-manifest.json').read_bytes()) != ANCHOR:
        raise WorkflowError('freeze manifest anchor mismatch')
    manifest = load(package / 'freeze-manifest.json')
    if tree(package / 'frozen') != set(manifest['files']):
        raise WorkflowError('frozen inventory mismatch')
    for name, checksum in manifest['files'].items():
        if digest((package / 'frozen' / name).read_bytes()) != checksum:
            raise WorkflowError('frozen content changed: ' + name)
    bindings = load(package / 'frozen/bindings.json')
    for name, checksum in bindings['dependencies'].items():
        if digest(plain(ROOT / name).read_bytes()) != checksum:
            raise WorkflowError('dependency changed: ' + name)
    for source in bindings['sources'].values():
        if digest(plain(ROOT / source['path'] / source['manifest']).read_bytes()) != source['sha256']:
            raise WorkflowError('source manifest changed: ' + source['path'])
    return manifest


def bridge():
    # Import only infrastructure; never call bridge.contract(), Session or old evaluators.
    verify()
    spec = importlib.util.spec_from_file_location('aw_reused_bridge', ROOT / 'validation/agent-utility-integration/bridge.py')
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def safe_name(name):
    if (not isinstance(name, str) or not name or '\\' in name
            or Path(name).is_absolute() or '..' in Path(name).parts
            or Path(name).as_posix() != name):
        raise WorkflowError('noncanonical inventory path')
    return name


def payloads():
    verify()
    b = bridge()
    bindings = load(PACKAGE / 'frozen/bindings.json')
    policy = load(PACKAGE / 'frozen/export-policy.json')
    result = {'A': ({}, {})}
    for arm in ('B', 'C'):
        source = ROOT / bindings['sources'][arm]['path']
        manifest = b.verify_snapshot(source, bindings['sources'][arm]['sha256'])
        data = {name: (source / 'files' / name).read_bytes() for name in manifest['files']}
        result[arm] = (data, manifest['files'])
    source = ROOT / bindings['sources']['D']['path']
    consumer = load(source / 'consumer-manifest.json')
    if set(consumer['files']) != set(policy['D_files']):
        raise WorkflowError('consumer policy inventory changed')
    if tree(source) != set(consumer['files']) | {'consumer-manifest.json'}:
        raise WorkflowError('consumer inventory changed')
    if not set(policy['required_D_files']) <= set(consumer['files']):
        raise WorkflowError('workflow guides/routes missing')
    data, meta, cards = {}, {}, []
    for name, checksum in sorted(consumer['files'].items()):
        safe_name(name)
        if any(name.startswith(p) for p in policy['forbidden_solver_prefixes']):
            raise WorkflowError('forbidden solver path')
        raw = plain(source / name).read_bytes()
        if digest(raw) != checksum:
            raise WorkflowError('consumer content changed: ' + name)
        raw.decode('utf-8')
        layer = b.eligible(name)
        if layer is None:
            layer = 'workflow'
        exported = name + '.txt'
        data[exported] = raw
        meta[exported] = {'layer': layer, 'bytes': len(raw), 'sha256': checksum, 'source_path': name}
        if name in consumer['cards'].values():
            card = b.legacy.card_metadata(raw.decode(), name)
            card['path'] = exported
            cards.append(card)
    if len(cards) != len(consumer['cards']) or sorted(c['id'] for c in cards) != sorted(consumer['cards']):
        raise WorkflowError('consumer canonical card mismatch')
    # Existing compact discovery format; canonical text stays byte-identical.
    raw = b.canonical({'description': b.DISCOVERY_DESCRIPTION, 'cards': sorted(cards, key=lambda c: c['id'])})
    data['index/L0.json'] = raw
    meta['index/L0.json'] = {'layer': 'L0', 'bytes': len(raw), 'sha256': digest(raw), 'source_path': None}
    result['D'] = (data, meta)
    return result


def inventory(meta):
    return [{'path': name, 'layer': info['layer'], 'bytes': info['bytes']}
            for name, info in sorted(meta.items())]


def prepared_payloads():
    result = {}
    for arm, (data, meta) in payloads().items():
        result['solver/' + arm + '/inventory.json'] = canonical(inventory(meta))
        result['snapshots/' + arm + '/manifest.json'] = canonical({
            'kind': 'AW-snapshot-1', 'arm': arm, 'freeze_manifest_sha256': ANCHOR, 'files': meta})
        for name, raw in data.items():
            result['snapshots/' + arm + '/files/' + name] = raw
    manifest = verify()
    for sid in manifest['scenarios']:
        result['solver/scenarios/' + sid + '.json'] = (PACKAGE / 'frozen/scenarios' / (sid + '.json')).read_bytes()
    result['solver/prompt.txt'] = (PACKAGE / 'frozen/prompt.txt').read_bytes()
    return result


def write_new(path, raw):
    path = plain(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write(raw)


def prepare(out):
    verify()
    out = plain(Path(out).absolute())
    if out.exists():
        raise WorkflowError('new preparation directory required; no overwrite/resume writes')
    data = prepared_payloads()
    receipt = {'kind': 'AW-preparation-1', 'freeze_manifest_sha256': ANCHOR,
               'files': {name: digest(raw) for name, raw in sorted(data.items())}}
    out.mkdir(parents=True)
    for name, raw in sorted(data.items()):
        write_new(out / name, raw)
    write_new(out / 'preparation-manifest.json', canonical(receipt))
    return verify_prepared(out)


def verify_prepared(out):
    verify()
    out = plain(Path(out))
    expected = prepared_payloads()
    receipt = {'kind': 'AW-preparation-1', 'freeze_manifest_sha256': ANCHOR,
               'files': {name: digest(raw) for name, raw in sorted(expected.items())}}
    if load(out / 'preparation-manifest.json') != receipt:
        raise WorkflowError('preparation receipt mismatch')
    if tree(out) != set(expected) | {'preparation-manifest.json'}:
        raise WorkflowError('preparation inventory mismatch')
    for name, raw in expected.items():
        if (out / name).read_bytes() != raw:
            raise WorkflowError('prepared content changed: ' + name)
    return receipt


def solver_inventory(out, arm):
    verify_prepared(out)
    if arm not in ARMS:
        raise WorkflowError('unknown arm')
    return load(Path(out) / 'solver' / arm / 'inventory.json')


_legacy = bridge().legacy


class OfflineTokenizer:
    """Local-only cl100k_base; no registry lookup, download or cache mutation."""
    ASSET_SHA256 = '223921b76ee99bde995b7ff738513eef100fb51d18c93597a113bcffe865b2a7'

    def __init__(self, asset):
        import base64
        from importlib.metadata import version
        self.asset = Path(asset)
        self.verify()
        if version('tiktoken') != '0.12.0':
            raise WorkflowError('optional tokenizer requires tiktoken 0.12.0')
        import tiktoken
        ranks = {base64.b64decode(token): int(rank)
                 for token, rank in (line.split() for line in self.asset.read_bytes().splitlines())}
        # Exact regex/special-token configuration from installed tiktoken 0.12.0
        # tiktoken_ext.openai_public.cl100k_base; never call its remote loader.
        self.encoding = tiktoken.Encoding(
            name='cl100k_base',
            pat_str=r"'(?i:[sdmt]|ll|ve|re)|[^\r\n\p{L}\p{N}]?+\p{L}++|\p{N}{1,3}+| ?[^\s\p{L}\p{N}]++[\r\n]*+|\s++$|\s*[\r\n]|\s+(?!\S)|\s",
            mergeable_ranks=ranks,
            special_tokens={'<|endoftext|>': 100257, '<|fim_prefix|>': 100258,
                            '<|fim_middle|>': 100259, '<|fim_suffix|>': 100260,
                            '<|endofprompt|>': 100276})
        self.metadata = {'library': 'tiktoken', 'version': '0.12.0', 'encoding': 'cl100k_base',
                         'asset_sha256': self.ASSET_SHA256,
                         'counting': 'sum per returned excerpt; encode_ordinary; special spellings treated as text'}

    def verify(self):
        verify()
        if not plain(self.asset).is_file() or digest(self.asset.read_bytes()) != self.ASSET_SHA256:
            raise WorkflowError('tokenizer asset missing or hash mismatch')

    def count(self, text):
        self.verify()
        return len(self.encoding.encode_ordinary(text))


class Broker(_legacy.ReadBroker):
    """Explicit new-snapshot binding to the unchanged legacy read method.

    This is an offline object seam, NOT legacy Session/contract or a model runtime.
    Returned content hashes/byte lengths are local evidence, not billing evidence.
    """
    def __init__(self, prepared, arm, tokenizer_asset=None):
        verify_prepared(prepared)
        self.tokenizer = OfflineTokenizer(tokenizer_asset) if tokenizer_asset is not None else None
        if arm not in ARMS:
            raise WorkflowError('unknown arm')
        self.prepared = Path(prepared)
        self.corpus = self.prepared / 'snapshots' / arm
        self.manifest = load(self.corpus / 'manifest.json')
        budget = load(PACKAGE / 'frozen/protocol.json')['budgets']
        self.budgets = {'max_read_attempts': budget['read_attempts'],
                        'max_reads': budget['successful_reads'],
                        'max_read_chars': budget['retrieved_characters'],
                        'max_chunk_chars': budget['read_chunk_characters']}
        self.logs = []
        self.attempts = self.chars = self.successes = 0
        self.ids = set()
        self.failed = False

    def read(self, request):
        before = len(self.logs)
        attempted = False
        try:
            verify_prepared(self.prepared)
            if self.tokenizer:
                self.tokenizer.verify()
            if self.failed:
                raise WorkflowError('broker already failed')
            valid_shape = (isinstance(request, dict)
                           and set(request) == {'type', 'request_id', 'path', 'offset', 'length'}
                           and request.get('type') == 'read_file')
            normalized = request if valid_shape else dict(request) if isinstance(request, dict) else {}
            if not valid_shape:
                normalized['request_id'] = ''  # Legacy validation counts and denies, never reads.
            attempted = True
            result = super().read(normalized)
            return result
        except (_legacy.BenchmarkError, WorkflowError, ValueError, OSError) as exc:
            self.failed = True
            if not attempted:
                self.attempts += 1
            if len(self.logs) == before:
                req = request if isinstance(request, dict) else {}
                self.logs.append({'request_id': req.get('request_id'), 'path': req.get('path'),
                                  'offset': req.get('offset'), 'requested_length': req.get('length'),
                                  'content': '', 'content_sha256': digest(b''), 'returned_chars': 0,
                                  'error': str(exc), 'layer': 'denied'})
            raise WorkflowError(str(exc)) from exc
        finally:
            if len(self.logs) > before:
                entry = self.logs[-1]
                entry.update({'request': copy.deepcopy(request), 'offset_unit': 'unicode-code-points',
                              'returned_bytes': len(entry['content'].encode('utf-8')),
                              'returned_text_tokens': self.tokenizer.count(entry['content']) if self.tokenizer else None,
                              'text_tokens_status': 'measured-offline-cl100k_base' if self.tokenizer else 'unavailable-offline-tokenizer',
                              'evaluator_relevance': None, 'evaluator_relevance_reason': None,
                              'counters': {'read_attempts': self.attempts, 'reads': self.successes,
                                           'characters': self.chars},
                              'freeze_manifest_sha256': ANCHOR})

    def accounting(self):
        verify_prepared(self.prepared)
        return {'read_attempts': self.attempts, 'successful_reads': self.successes,
                'documents': len({x['path'] for x in self.logs if x['error'] is None}),
                'retrieved_characters': self.chars,
                'retrieved_bytes': sum(x['returned_bytes'] for x in self.logs),
                'retrieved_text_tokens': sum(x['returned_text_tokens'] for x in self.logs) if self.tokenizer else None,
                'tokenizer': self.tokenizer.metadata if self.tokenizer else None,
                'provider_input_tokens': None, 'provider_output_tokens': None,
                'wall_seconds': None, 'cost_usd': None,
                'relevant_reads': None, 'irrelevant_reads': None, 'uncertain_reads': None,
                'quality_status': 'unscored', 'failed': self.failed,
                'scope': 'returned text only; repeated excerpts counted; no provider evidence'}


def offline_probe(prepared, tokenizer_asset=None):
    """Prescribed small read replay, not any of the 32 planned solver cells."""
    verify_prepared(prepared)
    result = {'kind': 'prescribed-seam-probe-not-agent-run', 'genuine_runs': 0, 'genuine_scores': 0,
              'freeze_manifest_sha256': ANCHOR, 'arms': {},
              'limitation': 'Different prescribed paths exercise the seam only; no task quality, navigation savings or model comparison.'}
    for arm in ARMS:
        broker = Broker(prepared, arm, tokenizer_asset=tokenizer_asset)
        path = 'START_HERE.md.txt' if arm == 'D' else 'index/L0.json'
        for i in range(2):
            broker.read({'type': 'read_file', 'request_id': 'repeat-' + str(i),
                         'path': path, 'offset': 0, 'length': 500})
        broker.read({'type': 'read_file', 'request_id': 'denied',
                     'path': '../../frozen/evaluator/checklists.json', 'offset': 0, 'length': 1})
        result['arms'][arm] = {'accounting': broker.accounting(), 'reads': broker.logs,
                               'inventory_bytes_not_retrieved': len((Path(prepared) / 'solver' / arm / 'inventory.json').read_bytes())}
    return result


def plan():
    manifest = verify()
    protocol = load(PACKAGE / 'frozen/protocol.json')
    sources = payloads()  # Validate the full externally pinned source closure on this action.
    cells = [{'scenario_id': sid, 'arm': arm, 'status': 'unexecuted'}
             for i, sid in enumerate(manifest['scenarios'])
             for arm in protocol['order_cycle'][i % len(protocol['order_cycle'])]]
    return {'kind': 'offline-plan-not-results', 'freeze_manifest_sha256': ANCHOR,
            'cells': cells, 'genuine_runs': 0, 'genuine_scores': 0,
            'execution_eligibility': 'unavailable', 'blockers': protocol['execution_gate'],
            'budgets': protocol['budgets'],
            'arm_documents_available_not_retrieved': {a: len(sources[a][0]) for a in ARMS},
            'navigation_confound': protocol['ablation']}


def gate_real_run():
    p = plan()
    raise WorkflowError('real run unavailable: ' + '; '.join(p['blockers']))


def report(prepared=None):
    p = plan()
    if prepared is not None:
        verify_prepared(prepared)
    scenarios = verify()['scenarios']
    # No result-admission path exists: this report cannot turn fixture reads into runs.
    empty = {'status': 'unexecuted', 'quality_status': 'unscored', 'quality_dimensions': None,
             'read_attempts': None, 'successful_reads': None, 'documents': None,
             'retrieved_bytes': None, 'retrieved_characters': None, 'retrieved_text_tokens': None,
             'relevant_reads': None, 'irrelevant_reads': None, 'uncertain_reads': None,
             'provider_input_tokens': None, 'provider_output_tokens': None,
             'wall_seconds': None, 'cost_usd': None}
    tasks = [{'scenario_id': sid, 'arms': {a: dict(empty) for a in ARMS},
              'quality_cost_frontier': [], 'frontier_status': 'no eligible independently evaluated runs'}
             for sid in scenarios]
    return {'kind': 'offline-readiness-report-not-model-results', 'freeze_manifest_sha256': ANCHOR,
            'genuine_runs': 0, 'genuine_scores': 0, 'planned_cells': len(p['cells']),
            'execution_eligibility': 'unavailable', 'blockers': p['blockers'],
            'tasks': tasks, 'navigation_confound': p['navigation_confound'],
            'cost_limitations': ['No transport evidence, so provider tokens/wall/money are null.',
                                 'Returned UTF-8 bytes are measured by Broker, never inferred billing.',
                                 'Tokenizer is opt-in with a pinned offline asset; no genuine solver token measurements exist.',
                                 'Inventory/scenario/prompt bytes are available for auditing, not automatically retrieved corpus text.',
                                 'Tool wrappers, repeated model context, automatic instructions and output billing are unobserved.'],
            'quality_rule': load(PACKAGE / 'frozen/evaluator/rubric.json')['judgment_requirements'],
            'frontier_rule': load(PACKAGE / 'frozen/protocol.json')['frontier']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['prepare', 'verify', 'plan', 'report'])
    parser.add_argument('--prepared', type=Path, help='preparation directory; defaults to prepared/initial')
    parser.add_argument('--output', type=Path, help='new JSON file; never overwrite')
    args = parser.parse_args()
    try:
        verify()
        prepared = args.prepared if args.prepared is not None else PACKAGE / 'prepared/initial'
        if args.action != 'prepare' and args.prepared is not None and not prepared.exists():
            raise WorkflowError('explicit preparation directory missing')
        if args.action == 'prepare':
            value = prepare(prepared)
        elif args.action == 'verify':
            value = {'freeze_manifest_sha256': ANCHOR, 'frozen_files': len(verify()['files']),
                     'sources_verified': {a: len(d) for a, (d, _) in payloads().items()}}
            if prepared.exists():
                value['preparation_manifest_sha256'] = digest((prepared / 'preparation-manifest.json').read_bytes())
                value['prepared_files'] = len(verify_prepared(prepared)['files'])
        elif args.action == 'plan':
            if prepared.exists():
                verify_prepared(prepared)
            value = plan()
        else:
            value = report(prepared if prepared.exists() else None)
        if args.output:
            write_new(args.output, canonical(value))
        print(canonical(value).decode(), end='')
    except (ValueError, OSError, KeyError) as exc:
        parser.exit(1, str(exc) + '\n')


if __name__ == '__main__':
    main()
