#!/usr/bin/env python3
"""AU-v2 offline compatibility layer. No provider, runner or evaluator dispatch."""
import argparse
import datetime
import hashlib
import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / 'validation/agent-utility-v2'
ANCHOR = '22d2527c35b39e1f22a0ac5815c833924815b63cbd1704a958989f124c798f49'
ARMS = ('baseline-atlas', 'expanded-atlas', 'no-atlas')
POLICY = 'shared-legacy-knowledge-eligibility-v2; preserve review-named L2 cards; no guides; neutral md.txt payloads'
DISCOVERY_DESCRIPTION = 'Discovery metadata; applicability is not evidence. Follow inventory paths.'


class IntegrationError(ValueError):
    pass


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def dependency(name, path, expected):
    if path.is_symlink() or digest(path.read_bytes()) != expected:
        raise IntegrationError('dependency hash mismatch: ' + path.name)
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


legacy = dependency('au_v1_reused', ROOT / 'validation/agent-utility/harness.py',
                    'f1a835f7d934616a40371c03df0923eccebd7a1f8871f5b41da14c585aaf9cd4')
strict = dependency('au_v2_strict', PACKAGE / 'verify.py',
                    '1254176a9aaf6007c7602b0128d9bb98681848c450d66614fe628badd91f6108')


def canonical(value):
    return legacy.canonical(value)


def load(path):
    return strict.load_json(Path(path).read_bytes())


def eligible(name):
    layer = legacy.layer_for(name)
    if ('review' in name.lower() and layer != 'L2'):
        return None
    if any(word in name.lower() for word in ('answer', 'coverage', 'tracker',
                                             'opportunit', 'scenario', 'implementation', 'change-log')):
        return None
    return layer


def assert_plain_tree(root):
    try:
        return strict.inventory(Path(root))
    except (strict.IntegrityError, OSError, ValueError) as exc:
        raise IntegrationError(str(exc)) from exc


def prepare_snapshot(source, out, arm):
    out = Path(out)
    if arm not in ARMS or (arm == 'no-atlas') != (source is None):
        raise IntegrationError('invalid arm/source combination')
    if any(p.is_symlink() for p in (out, *out.parents)):
        raise IntegrationError('output symlink forbidden')
    if out.exists():
        raise IntegrationError('new snapshot directory required')
    files, cards, payloads = {}, [], {}
    if source is not None:
        source = Path(source)
        if any(p.is_symlink() for p in (source, *source.parents)):
            raise IntegrationError('source symlink forbidden')
        if not source.is_dir():
            raise IntegrationError('source directory missing')
        for path in sorted(source.rglob('*.md')):
            name = path.relative_to(source).as_posix()
            layer = eligible(name)
            if layer is None:
                continue
            strict.canonical(name)
            if any(p.is_symlink() for p in (path, *path.parents)):
                raise IntegrationError('source symlink forbidden')
            raw = path.read_bytes()
            raw.decode('utf-8')
            exported = name + '.txt'
            payloads[exported] = raw
            files[exported] = {'layer': layer, 'bytes': len(raw), 'sha256': digest(raw), 'source_path': name}
            if layer == 'L2':
                card = legacy.card_metadata(raw.decode('utf-8'), name)
                card['path'] = exported
                cards.append(card)
        if len({c['id'] for c in cards}) != len(cards):
            raise IntegrationError('duplicate card IDs')
        payloads['index/L0.json'] = canonical({
            'description': DISCOVERY_DESCRIPTION,
            'cards': sorted(cards, key=lambda c: c['id']),
        })
        raw = payloads['index/L0.json']
        files['index/L0.json'] = {'layer': 'L0', 'bytes': len(raw), 'sha256': digest(raw), 'source_path': None}
    manifest = {'cohort': 'AU-v2', 'arm': arm, 'export_policy': POLICY,
                'files': files, 'card_ids': sorted(c['id'] for c in cards)}
    out.mkdir(parents=True)
    (out / 'files').mkdir()
    for name, raw in payloads.items():
        target = out / 'files' / name
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as stream:
            stream.write(raw)
    legacy.write_new(out / 'corpus-manifest.json', manifest)
    return verify_snapshot(out)


def verify_snapshot(out, expected=None):
    out = Path(out)
    actual = assert_plain_tree(out)
    raw = (out / 'corpus-manifest.json').read_bytes()
    if expected is not None and digest(raw) != expected:
        raise IntegrationError('snapshot anchor mismatch')
    manifest = strict.load_json(raw)
    if (set(manifest) != {'cohort', 'arm', 'export_policy', 'files', 'card_ids'}
            or manifest['cohort'] != 'AU-v2' or manifest['arm'] not in ARMS
            or manifest['export_policy'] != POLICY or not isinstance(manifest['files'], dict)):
        raise IntegrationError('snapshot manifest shape/policy mismatch')
    wanted = {'corpus-manifest.json'} | {'files/' + p for p in manifest['files']}
    if wanted != actual:
        raise IntegrationError('snapshot inventory mismatch')
    if manifest['arm'] == 'no-atlas' and (manifest['files'] or manifest['card_ids']):
        raise IntegrationError('no-atlas must be empty')
    cards = []
    for name, meta in manifest['files'].items():
        strict.canonical(name)
        if set(meta) != {'layer', 'bytes', 'sha256', 'source_path'}:
            raise IntegrationError('invalid snapshot metadata')
        if name == 'index/L0.json':
            if meta['layer'] != 'L0' or meta['source_path'] is not None:
                raise IntegrationError('invalid L0')
        elif (name != str(meta['source_path']) + '.txt' or eligible(meta['source_path']) != meta['layer']):
            raise IntegrationError('snapshot allowlist violation')
        data = (out / 'files' / name).read_bytes()
        if len(data) != meta['bytes'] or digest(data) != meta['sha256']:
            raise IntegrationError('snapshot content hash mismatch')
        data.decode('utf-8')
        if meta['layer'] == 'L2':
            card = legacy.card_metadata(data.decode('utf-8'), meta['source_path'])
            card['path'] = name
            cards.append(card)
    ids = sorted(c['id'] for c in cards)
    if len(set(ids)) != len(ids) or manifest['card_ids'] != ids:
        raise IntegrationError('snapshot card inventory mismatch')
    if manifest['arm'] != 'no-atlas':
        if 'index/L0.json' not in manifest['files']:
            raise IntegrationError('snapshot discovery index missing')
        expected_l0 = {'description': DISCOVERY_DESCRIPTION, 'cards': sorted(cards, key=lambda c: c['id'])}
        if load(out / 'files/index/L0.json') != expected_l0:
            raise IntegrationError('snapshot discovery index mismatch')
    return manifest


def contract():
    # Only metadata is returned; inputs/keys stay in the verifier, not agent context.
    strict.verify(PACKAGE, ANCHOR)
    return load(PACKAGE / 'settings.json')


def inventory(manifest):
    return [{'path': name, 'layer': meta['layer'], 'bytes': meta['bytes']}
            for name, meta in sorted(manifest['files'].items())]


def snapshot_binding(root, arm):
    manifest = verify_snapshot(root)
    if manifest['arm'] != arm:
        raise IntegrationError('arm binding mismatch')
    return {'id': arm, 'inventory_sha256': digest(canonical(inventory(manifest))),
            'corpus_manifest_sha256': digest((Path(root) / 'corpus-manifest.json').read_bytes()),
            'inventory_count': len(manifest['files']),
            'snapshot_identity': digest(canonical(manifest))}


def preparation_plan(roots):
    settings = contract()
    if set(roots) != set(ARMS):
        raise IntegrationError('exact three arms required')
    bindings = [snapshot_binding(roots[arm], arm) for arm in ARMS]
    cells = []
    for i, sid in enumerate(settings['scenario_order']):
        for arm in settings['arm_order_cycle'][i % len(settings['arm_order_cycle'])]:
            cells.append({'scenario_id': sid, 'arm': arm, 'status': 'unexecuted'})
    return {'kind': 'offline-preparation-plan', 'cohort': 'AU-v2',
            'freeze_manifest_sha256': ANCHOR,
            'settings_sha256': digest((PACKAGE / 'settings.json').read_bytes()),
            'prompt_sha256': digest((PACKAGE / 'prompt.txt').read_bytes()),
            'bridge_sha256': digest(Path(__file__).read_bytes()),
            'export_policy': POLICY, 'arms': bindings, 'cells': cells,
            'actual_runs': 0, 'actual_scores': 0, 'execution_eligibility': 'blocked',
            'blockers': ['No attested registration', 'No integrated trusted executor/transport or scorer'],
            'recovery_rule': 'first completed attempt from earliest full cohort; recovery requires new full cohort'}


class Broker(legacy.ReadBroker):
    """Bind old read/accounting implementation without changing its globals."""
    def __init__(self, root, expected):
        self.corpus = Path(root)
        self.manifest = verify_snapshot(root, expected)
        b = contract()['budgets']
        self.budgets = {'max_read_attempts': b['read_attempts'], 'max_reads': b['successful_reads'],
                        'max_read_chars': b['retrieved_characters'], 'max_chunk_chars': b['read_chunk_characters']}
        self.inventory_sha256 = digest(canonical(inventory(self.manifest)))
        self.logs = []
        self.attempts = self.chars = self.successes = 0
        self.ids = set()
        self.failed = False

    def read(self, request):
        if self.failed:
            raise IntegrationError('broker already failed')
        original = request
        malformed = (not isinstance(request, dict)
                     or set(request) != {'type', 'request_id', 'path', 'offset', 'length'}
                     or request.get('type') != 'read_file')
        if malformed:
            request = dict(request) if isinstance(request, dict) else {}
            request['request_id'] = ''  # Old validation counts and denies, never reads.
        name = request.get('path')
        reason = None
        if isinstance(name, str) and name in self.manifest['files']:
            file = self.corpus / 'files' / name
            if any(p.is_symlink() for p in (file, *file.parents)):
                reason = 'snapshot symlink detected during read'
        before = len(self.logs)
        try:
            if reason:
                self.attempts += 1
                raise IntegrationError(reason)
            result = legacy.ReadBroker.read(self, request)
        except (legacy.BenchmarkError, IntegrationError, OSError, UnicodeError) as exc:
            self.failed = True
            if len(self.logs) == before:
                self.logs.append({'request_id': str(request.get('request_id', '')),
                                  'path': str(name), 'offset': request.get('offset'),
                                  'requested_length': request.get('length'), 'returned_chars': 0,
                                  'content': '', 'content_sha256': digest(b''), 'error': str(exc)})
            raise IntegrationError(str(exc)) from exc
        finally:
            if self.logs:
                self.logs[-1]['inventory_sha256'] = self.inventory_sha256
                self.logs[-1]['request'] = original
                self.logs[-1]['counters'] = {'attempts': self.attempts, 'reads': self.successes, 'characters': self.chars}
        if malformed:
            return {'type': 'read_denied', 'request_id': str(original.get('request_id', '')) if isinstance(original, dict) else '',
                    'reason': 'invalid read request shape'}
        if result['error'] is not None:
            return {'type': 'read_denied', 'request_id': result['request_id'], 'reason': result['error']}
        return {'type': 'read_result', 'request_id': result['request_id'], 'path': result['path'],
                'offset': request['offset'], 'text': result['content'],
                'returned_characters': len(result['content']),
                'content_sha256': digest(result['content'].encode('utf-8'))}


class Session:
    """Offline protocol state machine, not a process runner or identity attestor."""
    def __init__(self, broker, identity, settings_sha256):
        if (not isinstance(identity, str) or not identity.strip()
                or not isinstance(settings_sha256, str) or not re.fullmatch(r'[0-9a-f]{64}', settings_sha256)):
            raise IntegrationError('registered identity and exact settings hash required')
        self.broker = broker
        self.identity = identity
        self.settings_sha256 = settings_sha256
        self.state = 'awaiting_ready'
        self.response = None
        self.events = []
        self.budgets = contract()['budgets']

    def record(self, direction, raw):
        self.events.append({'direction': direction, 'raw_hex': raw.hex(),
                            'sha256': digest(raw),
                            'observed_at': datetime.datetime.now(datetime.timezone.utc).isoformat()})

    def handle(self, raw):
        try:
            if not isinstance(raw, bytes):
                raise IntegrationError('JSONL input must be bytes')
            self.record('received', raw)
            if (not raw.endswith(b'\n') or b'\n' in raw[:-1]
                    or len(raw) - 1 > self.budgets['stdout_line_bytes']):
                raise IntegrationError('invalid/oversized JSONL line')
            message = strict.load_json(raw.decode('utf-8'))
            if not isinstance(message, dict):
                raise IntegrationError('protocol message must be object')
            kind = message.get('type')
            if self.state == 'awaiting_ready':
                if (set(message) != {'type', 'identity', 'settings_sha256', 'fresh_context', 'broker_only'}
                        or kind != 'ready' or message['identity'] != self.identity
                        or message['settings_sha256'] != self.settings_sha256
                        or message['fresh_context'] is not True or message['broker_only'] is not True):
                    raise IntegrationError('missing/mismatched registered ready')
                self.state = 'reading'
                return None
            if self.state != 'reading':
                raise IntegrationError('output after final or failed session')
            if kind == 'read_file':
                result = self.broker.read(message)
                self.record('broker_generated', canonical(result))
                return result
            if kind == 'final':
                text = message.get('text')
                if (set(message) != {'type', 'text'} or not isinstance(text, str) or not text.strip()
                        or len(text) > self.budgets['final_characters']):
                    raise IntegrationError('invalid/oversized final')
                self.response = text
                self.state = 'awaiting_exit'
                return None
            raise IntegrationError('unexpected protocol message')
        except (strict.IntegrityError, IntegrationError, ValueError, UnicodeError) as exc:
            self.state = 'failed'
            raise IntegrationError(str(exc)) from exc

    def finish(self, exit_code):
        if self.state != 'awaiting_exit' or type(exit_code) is not int or exit_code != 0:
            self.state = 'failed'
            raise IntegrationError('successful terminal exit required after final')
        self.state = 'completed'
        return self.response


def validate_registration(value, roots, evidence_root, runtime_path, adapter_path):
    """Check artifact bindings. Never certify attestation truth or permit dispatch."""
    try:
        plan = preparation_plan(roots)
        strict.validate(value, load(PACKAGE / 'schemas/registration.schema.json'), '$registration')
        for key in ('freeze_manifest_sha256', 'prompt_sha256', 'settings_sha256'):
            if value[key] != plan[key]:
                raise IntegrationError('registration provenance mismatch: ' + key)
        if (len(value['arms']) != len(ARMS)
                or {a['id'] for a in value['arms']} != set(ARMS)
                or sorted(value['arms'], key=lambda a: a['id']) != sorted(plan['arms'], key=lambda a: a['id'])):
            raise IntegrationError('registration arm bindings mismatch')
        for key, path in (('runtime_sha256', runtime_path), ('adapter_sha256', adapter_path)):
            path = Path(path)
            if any(p.is_symlink() for p in (path, *path.parents)) or digest(path.read_bytes()) != value[key]:
                raise IntegrationError('registration executable hash mismatch: ' + key)
        tested, evaluator = value['tested'], value['evaluator']
        if (tested['identity'] == evaluator['identity']
                or (tested['model'], tested['version']) == (evaluator['model'], evaluator['version'])):
            raise IntegrationError('distinct actual models required, not provider/identity aliases')
        root = Path(evidence_root)
        assert_plain_tree(root)
        for role in ('tested', 'evaluator'):
            identity = value[role]
            raw = (root / (identity['evidence_sha256'] + '.json')).read_bytes()
            if digest(raw) != identity['evidence_sha256']:
                raise IntegrationError('model attestation hash mismatch')
            record = strict.load_json(raw)
            required = ('identity', 'provider', 'model', 'version', 'fresh_process',
                        'fresh_conversation', 'independence_attested')
            if (record.get('kind') != 'model-attestation' or record.get('role') != role
                    or any(k not in record or not strict.json_equal(record[k], identity[k]) for k in required)
                    or record.get('broker_only') is not True
                    or type(record.get('callable_tools')) is not int or record['callable_tools'] != 0
                    or not isinstance(record.get('signed_conflict_declaration'), str)
                    or not record['signed_conflict_declaration'].strip()):
                raise IntegrationError('incomplete/mismatched model evidence')
        for setting, meta in value['generation'].items():
            strict.canonical(meta['evidence'])
            record = load(root / meta['evidence'])
            if (record.get('kind') != 'generation-attestation' or record.get('setting') != setting
                    or record.get('cross_arm_equivalence') is not True
                    or any(k not in record or not strict.json_equal(record[k], meta[k])
                           for k in ('requested', 'effective', 'enforcement'))):
                raise IntegrationError('generation evidence mismatch')
            if meta['enforcement'] == 'unsupported' and (meta['effective'] is not None or not meta['limitation'].strip()):
                raise IntegrationError('unsupported setting needs null effective value and limitation')
        return {'structure_and_bindings_checked': True, 'execution_eligibility': 'blocked',
                'registration_sha256': digest(canonical(value)),
                'blockers': ['Attestation truth/signature trust needs independent operator verification',
                             'Trusted executor/transport and independent scoring integration absent']}
    except (strict.IntegrityError, OSError, ValueError, KeyError, TypeError) as exc:
        raise IntegrationError(str(exc)) from exc


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    prepare = sub.add_parser('prepare')
    prepare.add_argument('--source', type=Path)
    prepare.add_argument('--arm', choices=ARMS, required=True)
    prepare.add_argument('--out', type=Path, required=True)
    verify = sub.add_parser('verify')
    verify.add_argument('--snapshot', type=Path, required=True)
    verify.add_argument('--expected-sha256', required=True)
    for action in ('plan', 'check-registration'):
        child = sub.add_parser(action)
        for option in ('baseline', 'expanded', 'empty'):
            child.add_argument('--' + option, type=Path, required=True)
        if action == 'plan':
            child.add_argument('--out', type=Path, required=True)
        else:
            for option in ('registration', 'evidence', 'runtime', 'adapter'):
                child.add_argument('--' + option, type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        contract()
        if args.action == 'prepare':
            manifest = prepare_snapshot(args.source, args.out, args.arm)
            result = {'snapshot': str(args.out), 'files': len(manifest['files']), 'cards': len(manifest['card_ids']),
                      'manifest_sha256': digest((args.out / 'corpus-manifest.json').read_bytes())}
        elif args.action == 'verify':
            manifest = verify_snapshot(args.snapshot, args.expected_sha256)
            result = {'integrity': 'verified', 'files': len(manifest['files']), 'cards': len(manifest['card_ids'])}
        else:
            roots = dict(zip(ARMS, (args.baseline, args.expanded, args.empty)))
            if args.action == 'plan':
                value = preparation_plan(roots)
                legacy.write_new(args.out, value)
                result = {'plan': str(args.out), 'planned_cells': len(value['cells']),
                          'plan_sha256': digest(args.out.read_bytes()), 'execution_eligibility': 'blocked',
                          'actual_runs': 0, 'actual_scores': 0}
            else:
                result = validate_registration(load(args.registration), roots, args.evidence, args.runtime, args.adapter)
        print(json.dumps(result, sort_keys=True))
        return 0
    except (IntegrationError, strict.IntegrityError, legacy.BenchmarkError, OSError, ValueError, TypeError, KeyError) as exc:
        print(json.dumps({'error': str(exc), 'execution_eligibility': 'blocked'}, sort_keys=True))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
