#!/usr/bin/env python3
"""Evaluator-only mechanical AU-v2 packet/scoring tools; never model dispatch."""
import importlib.util
import argparse
import datetime
import json
import re
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('au_v2_scoring_bridge', HERE / 'bridge.py')
assert spec is not None and spec.loader is not None
bridge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bridge)


READ_CONTRACT = 'Exact inventory paths; Unicode offsets/lengths; read_result or read_denied.'


class FrozenContext:
    """Trusted operator-side access; only packet dispatch loads private case/key content."""
    def __init__(self):
        bridge.contract()
        self.anchor = bridge.ANCHOR
        self.hashes = bridge.load(bridge.PACKAGE / 'freeze-manifest.json')['files']

    def hash(self, name):
        bridge.strict.canonical(name)
        require(name in self.hashes, 'path outside frozen package inventory')
        return self.hashes[name]

    def raw(self, name):
        expected = self.hash(name)
        path = bridge.PACKAGE / name
        require(not any(p.is_symlink() for p in (path, *path.parents)), 'frozen package symlink')
        raw = path.read_bytes()
        require(bridge.digest(raw) == expected, 'frozen package changed during scoring')
        return raw

    def get(self, name):
        return parse_json(self.raw(name))

    def schema(self, name):
        return self.get('schemas/' + name + '.schema.json')


def require(condition, message):
    if not condition:
        raise bridge.IntegrationError(message)


def parse_json(raw):
    value = bridge.strict.load_json(raw)
    def finite(item):
        if type(item) is float:
            require(math.isfinite(item), 'nonfinite JSON number, including exponent overflow')
        elif isinstance(item, dict):
            for sub in item.values():
                finite(sub)
        elif isinstance(item, list):
            for sub in item:
                finite(sub)
    finite(value)
    return value


def aware_time(value):
    require(isinstance(value, str), 'timestamp required')
    when = datetime.datetime.fromisoformat(value.replace('Z', '+00:00'))
    require(when.tzinfo is not None, 'timezone-aware timestamp required')
    return when


def validate_run(run_raw, registration_raw, journal_raw, snapshot_root, context):
    run = parse_json(run_raw)
    if not isinstance(run, dict) or run.get('status') != 'completed':
        raise bridge.IntegrationError('only completed runs may be evaluated')
    bridge.strict.validate(run, context.schema('run'), '$run')
    registration = parse_json(registration_raw)
    bridge.strict.validate(registration, context.schema('registration'), '$registration')
    for meta in registration['generation'].values():
        require(meta['enforcement'] != 'unsupported'
                or (meta['effective'] is None and bool(meta['limitation'].strip())),
                'unsupported setting needs null effective value and limitation')
    require(run['registration_sha256'] == bridge.digest(registration_raw), 'registration byte hash mismatch')
    require(run['runtime_identity_attested'] is True and run['failure_reason'] is None,
            'completed run requires attested identity and no failure')
    require(isinstance(run['response'], str) and bool(run['response'].strip())
            and run['response_sha256'] == bridge.digest(run['response'].encode()), 'response hash mismatch')
    for field, expected in [('freeze_manifest_sha256', context.anchor),
                            ('prompt_sha256', context.hash('prompt.txt')),
                            ('settings_sha256', context.hash('settings.json'))]:
        require(run[field] == registration[field] == expected, 'run/registration provenance mismatch: ' + field)
    sid = run['scenario_id']
    require(run['scenario_sha256'] == context.hash('inputs/' + sid + '.json'), 'scenario hash mismatch')
    tested, evaluator = registration['tested'], registration['evaluator']
    require(run['tested_identity'] == tested['identity'], 'tested identity mismatch')
    require(tested['identity'] != evaluator['identity']
            and (tested['model'], tested['version']) != (evaluator['model'], evaluator['version']),
            'tested/evaluator models must be distinct')
    require(len({a['id'] for a in registration['arms']}) == 3, 'duplicate registered arms')
    binding = next(a for a in registration['arms'] if a['id'] == run['arm'])
    manifest = bridge.verify_snapshot(snapshot_root, binding['corpus_manifest_sha256'])
    require(bridge.snapshot_binding(snapshot_root, run['arm']) == binding, 'registered snapshot binding mismatch')
    require(run['inventory_sha256'] == binding['inventory_sha256'], 'inventory hash mismatch')
    budgets = context.get('settings.json')['budgets']
    require(len(run['response']) <= budgets['final_characters'], 'final budget exceeded')
    require(run['read_attempts'] <= budgets['read_attempts'], 'read attempt budget exceeded')
    journal = parse_json(journal_raw)
    require(isinstance(journal, dict) and set(journal) == {
        'format', 'run_sha256', 'exit_code', 'exit_observed_at', 'runtime_identity_evidence_sha256',
        'events', 'stderr_sha256', 'stderr_hex'}, 'journal shape mismatch')
    require(journal['format'] == 'au-v2-execution-journal-v1'
            and journal['run_sha256'] == bridge.digest(run_raw), 'journal/run hash mismatch')
    require(journal['runtime_identity_evidence_sha256'] == tested['evidence_sha256'], 'runtime evidence binding mismatch')
    require(type(journal['exit_code']) is int and journal['exit_code'] == 0, 'successful exit evidence required')
    stderr = bytes.fromhex(journal['stderr_hex'])
    require(bridge.digest(stderr) == journal['stderr_sha256'], 'stderr hash mismatch')
    events = journal['events']
    require(isinstance(events, list) and bool(events), 'execution events required')
    broker = bridge.Broker(snapshot_root, binding['corpus_manifest_sha256'])
    session = bridge.Session(broker, tested['identity'], run['settings_sha256'])
    expected_reply = None
    excerpts = []
    read_log = []
    first_time = previous_time = None
    for i, event in enumerate(events):
        require(isinstance(event, dict) and set(event) == {'direction', 'raw_hex', 'sha256', 'observed_at'},
                'journal event shape mismatch')
        when = aware_time(event['observed_at'])
        require(previous_time is None or when >= previous_time, 'journal time moved backwards')
        previous_time = when
        if first_time is None:
            first_time = when
        raw = bytes.fromhex(event['raw_hex'])
        require(bridge.digest(raw) == event['sha256'], 'journal event byte hash mismatch')
        if i == 0:
            require(event['direction'] == 'sent_start', 'journal must start with actual sent start')
            require(raw.endswith(b'\n') and b'\n' not in raw[:-1], 'start must be one JSONL message')
            require(len(raw.decode('utf-8')) <= budgets['initial_characters'], 'initial context budget exceeded')
            start = parse_json(raw)
            expected_start = {'type': 'start', 'scenario': context.get('inputs/' + sid + '.json'),
                              'prompt': context.raw('prompt.txt').decode(), 'settings_sha256': run['settings_sha256'],
                              'inventory': bridge.inventory(manifest), 'read_file': READ_CONTRACT}
            require(bridge.strict.json_equal(start, expected_start), 'start payload mismatch or unblinded/extra context')
            continue
        if expected_reply is not None:
            require(event['direction'] == 'sent_broker' and raw == bridge.canonical(expected_reply),
                    'actual sent broker bytes mismatch or missing response')
            expected_reply = None
            continue
        require(event['direction'] == 'received', 'unexpected journal direction or generated-only bytes')
        parse_json(raw)
        expected_reply = session.handle(raw)
        if expected_reply is not None and expected_reply['type'] == 'read_result':
            last = broker.logs[-1]
            read_log.append({'request_id': last['request_id'], 'path': last['path'], 'offset': last['offset'],
                             'requested_length': last['requested_length'], 'returned_characters': last['returned_chars'],
                             'content_sha256': last['content_sha256'], 'inventory_sha256': last['inventory_sha256']})
            excerpts.append({k: expected_reply[k] for k in ('path', 'offset', 'text', 'returned_characters', 'content_sha256')})
    require(expected_reply is None, 'unanswered broker request')
    exit_time = aware_time(journal['exit_observed_at'])
    require(previous_time is not None and first_time is not None and exit_time >= previous_time
            and (exit_time - first_time).total_seconds() <= budgets['solver_wall_seconds'], 'terminal time budget mismatch')
    require(session.finish(journal['exit_code']) == run['response'], 'journal/final response mismatch')
    require(run['read_attempts'] == broker.attempts and run['read_log'] == read_log, 'read counters/log provenance mismatch')
    return run, registration, excerpts


def build_packet(run_raw, registration_raw, journal_raw, snapshot_root, context):
    try:
        run, registration, excerpts = validate_run(run_raw, registration_raw, journal_raw, snapshot_root, context)
        sid = run['scenario_id']
        scenario = context.get('inputs/' + sid + '.json')
        key_path = 'evaluator-only/keys/' + sid + '.json'
        key = context.get(key_path)
        rubric = context.get('evaluator-only/rubric.json')
        bridge.strict.validate(scenario, context.schema('scenario'), '$scenario')
        bridge.strict.validate(key, context.schema('key'), '$key')
        bridge.strict.validate(rubric, context.schema('rubric'), '$rubric')
        require(key['scenario_id'] == sid == scenario['scenario_id'], 'case/key cross-reference mismatch')
        packet = {'cohort': 'AU-v2', 'scenario_id': sid, 'scenario': scenario,
                  'prompt': context.raw('prompt.txt').decode(), 'response': run['response'], 'reads': excerpts,
                  'read_attempts': run['read_attempts'],
                  'read_statistics': {'successful_reads': len(run['read_log']),
                                      'returned_characters': sum(item['returned_characters'] for item in run['read_log'])},
                  'retrieval_applicable': run['arm'] != 'no-atlas', 'answer_key': key, 'rubric': rubric,
                  'evaluation_instructions': context.raw('evaluator-only/prompt.txt').decode(),
                  'run_sha256': bridge.digest(run_raw), 'response_sha256': run['response_sha256'],
                  'freeze_manifest_sha256': context.anchor, 'settings_sha256': run['settings_sha256']}
        receipt = {'format': 'au-v2-packet-receipt-v1', 'packet_sha256': bridge.digest(bridge.canonical(packet)),
                   'run_sha256': bridge.digest(run_raw), 'registration_sha256': bridge.digest(registration_raw),
                   'journal_sha256': bridge.digest(journal_raw), 'arm': run['arm'],
                   'tested_identity': registration['tested']['identity'],
                   'evaluator_identity': registration['evaluator']['identity'],
                   'scenario_sha256': run['scenario_sha256'], 'inventory_sha256': run['inventory_sha256'],
                   'key_sha256': context.hash(key_path), 'rubric_sha256': context.hash('evaluator-only/rubric.json'),
                   'evaluator_prompt_sha256': context.hash('evaluator-only/prompt.txt')}
        return packet, receipt
    except (bridge.IntegrationError, bridge.strict.IntegrityError, bridge.legacy.BenchmarkError,
            OSError, ValueError, KeyError, TypeError, StopIteration) as exc:
        raise bridge.IntegrationError(str(exc)) from exc


def finalize_score(run_raw, registration_raw, journal_raw, snapshot_root, context,
                   packet_raw, receipt_raw, draft_raw):
    """Validate an independent evaluator's draft and compute caps, never assign raw scores."""
    try:
        packet, receipt = build_packet(run_raw, registration_raw, journal_raw, snapshot_root, context)
        require(packet_raw == bridge.canonical(packet)
                and parse_json(receipt_raw) == receipt, 'packet/private receipt provenance mismatch')
        score = parse_json(draft_raw)
        bridge.strict.validate(score, context.schema('score'), '$score')
        for field, expected in [('scenario_id', packet['scenario_id']), ('run_sha256', packet['run_sha256']),
                                ('response_sha256', packet['response_sha256']), ('packet_sha256', receipt['packet_sha256']),
                                ('freeze_manifest_sha256', packet['freeze_manifest_sha256']),
                                ('settings_sha256', packet['settings_sha256']),
                                ('evaluator_identity', receipt['evaluator_identity'])]:
            require(score[field] == expected, 'score provenance/identity mismatch: ' + field)
        require(aware_time(score['evaluated_at']) >= aware_time(parse_json(journal_raw)['exit_observed_at']),
                'evaluation time precedes completed run')
        dimension_ids = set(context.schema('score')['properties']['dimensions']['required'])
        rubric_ids = [entry['id'] for entry in packet['rubric']['dimensions']]
        require(len(rubric_ids) == len(set(rubric_ids)) and set(rubric_ids) == dimension_ids, 'rubric dimension mismatch')
        sid = packet['scenario_id']
        findings = {item['finding_id']: item for item in packet['answer_key']['findings']}
        failures = {item['failure_id']: item for item in packet['answer_key']['critical_failures']}
        require(len(findings) == len(packet['answer_key']['findings'])
                and all(fid.startswith(sid + '-F') for fid in findings), 'duplicate/cross-case key finding')
        require(len(failures) == len(packet['answer_key']['critical_failures'])
                and all(fid.startswith(sid + '-CF-') for fid in failures)
                and all(item['caps'] for item in failures.values()), 'duplicate/cross-case/uncapped key failure')
        response = packet['response']
        seen = set()
        for item in score['critical_failures']:
            fid = item['failure_id']
            require(fid in failures and fid not in seen, 'unknown/duplicate critical failure')
            require(bool(item['response_quote'].strip()) and item['response_quote'] in response,
                    'critical-failure quote is not an exact response substring')
            require(bool(item['endorsement_explanation'].strip()), 'endorsed-harm explanation required')
            seen.add(fid)
        for dim, entry in score['dimensions'].items():
            require(bool(entry['rationale'].strip()), 'nonempty dimension rationale required')
            omitted = entry['omitted_finding_ids']
            require(len(omitted) == len(set(omitted))
                    and all(fid in findings and dim in findings[fid]['dimensions'] for fid in omitted),
                    'unknown/duplicate/inapplicable omitted finding')
            require(all(quote.strip() and quote in response for quote in entry['response_quotes']),
                    'dimension quote is not an exact response substring')
            if dim == 'retrieval_grounding' and not packet['retrieval_applicable']:
                require(entry['raw'] is None and entry['effective'] is None
                        and 'not_applicable' in entry['rationale'], 'empty-inventory retrieval must be null/not_applicable')
                continue
            require(type(entry['raw']) is int, 'all applicable dimensions require ordinal raw scores')
            require(bool(entry['response_quotes'] or omitted), 'dimension needs response evidence or scoped omission')
            caps = [failures[fid]['caps'][dim] for fid in seen if dim in failures[fid]['caps']]
            entry['effective'] = min([entry['raw'], *caps])
        for text in score['alternative_credit'] + score['limitations']:
            require(bool(text.strip()), 'empty alternative/limitation note')
        limitation = 'Mechanical provenance/quote/cap validation does not certify semantic endorsement, signature trust or model independence.'
        if limitation not in score['limitations']:
            score['limitations'].append(limitation)
        bridge.strict.validate(score, context.schema('score'), '$final_score')
        return score
    except (bridge.IntegrationError, bridge.strict.IntegrityError, OSError, ValueError, KeyError, TypeError) as exc:
        raise bridge.IntegrationError(str(exc)) from exc


def new_bundle(out):
    out = Path(out)
    require(not any(p.is_symlink() for p in (out, *out.parents)), 'bundle symlink forbidden')
    for forbidden in (bridge.ROOT / 'validation/agent-utility', bridge.PACKAGE):
        require(not out.resolve().is_relative_to(forbidden.resolve()), 'protected benchmark output forbidden')
    require(not out.exists(), 'new artifact directory required; never overwrite')
    out.mkdir(parents=True, mode=0o700)
    return out


def write_packet_bundle(out, run_raw, registration_raw, journal_raw, snapshot_root, context):
    packet, receipt = build_packet(run_raw, registration_raw, journal_raw, snapshot_root, context)
    out = new_bundle(out)
    bridge.legacy.write_new(out / 'packet.json', packet)
    bridge.legacy.write_new(out / 'private-receipt.json', receipt)
    for path in out.iterdir():
        path.chmod(0o600)
    return {'operation': 'packet_bundle', 'access': 'evaluator-only', 'packet_sha256': receipt['packet_sha256'],
            'receipt_sha256': bridge.digest((out / 'private-receipt.json').read_bytes()),
            'mechanical_only': True}


def write_score_bundle(out, run_raw, registration_raw, journal_raw, snapshot_root, context,
                       packet_raw, receipt_raw, draft_raw):
    score = finalize_score(run_raw, registration_raw, journal_raw, snapshot_root, context,
                           packet_raw, receipt_raw, draft_raw)
    out = new_bundle(out)
    with (out / 'evaluator-draft.json').open('xb') as stream:
        stream.write(draft_raw)
    bridge.legacy.write_new(out / 'score.json', score)
    manifest = {'operation': 'mechanical_score_validation',
                'run_sha256': bridge.digest(run_raw), 'registration_sha256': bridge.digest(registration_raw),
                'journal_sha256': bridge.digest(journal_raw), 'packet_sha256': bridge.digest(packet_raw),
                'private_receipt_sha256': bridge.digest(receipt_raw), 'draft_sha256': bridge.digest(draft_raw),
                'score_sha256': bridge.digest((out / 'score.json').read_bytes()),
                'scoring_code_sha256': bridge.digest(Path(__file__).read_bytes()),
                'semantic_correctness_and_independence_certified': False}
    bridge.legacy.write_new(out / 'validation.json', manifest)
    for path in out.iterdir():
        path.chmod(0o600)
    return {'operation': 'score_bundle', 'score_sha256': manifest['score_sha256'], 'mechanical_only': True}


def read_input(path):
    path = Path(path)
    require(not any(p.is_symlink() for p in (path, *path.parents)) and path.is_file(), 'regular nonsymlink input required')
    return path.read_bytes()


def main(argv=None, context=None):
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_subparsers(dest='action', required=True)
    for action in ('packet', 'score'):
        child = actions.add_parser(action)
        child.add_argument('--role', choices=['evaluator-operator'], required=True)
        for option in ('run', 'registration', 'journal', 'snapshot', 'out'):
            child.add_argument('--' + option, type=Path, required=True)
        if action == 'score':
            for option in ('packet', 'receipt', 'evaluation'):
                child.add_argument('--' + option, type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        run_raw = read_input(args.run)
        run = parse_json(run_raw)
        require(isinstance(run, dict) and run.get('status') == 'completed', 'only completed runs may be evaluated')
        context = FrozenContext() if context is None else context
        inputs = (run_raw, read_input(args.registration), read_input(args.journal), args.snapshot, context)
        if args.action == 'packet':
            result = write_packet_bundle(args.out, *inputs)
        else:
            result = write_score_bundle(args.out, *inputs, read_input(args.packet), read_input(args.receipt), read_input(args.evaluation))
        print(json.dumps(result, sort_keys=True))
        return 0
    except (bridge.IntegrationError, bridge.strict.IntegrityError, OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({'error': str(exc), 'mechanical_only': True}, sort_keys=True))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
