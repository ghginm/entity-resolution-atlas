"""Scoring infrastructure fixtures only; no frozen scenarios/keys or models read."""
import copy
import contextlib
import importlib.util
import json
import io
import os
import datetime
from pathlib import Path
import tempfile
import unittest

HERE = Path(__file__).resolve().parents[1]


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


class FixtureContext:
    def __init__(self, bridge):
        self.b = bridge
        self.anchor = 'f' * 64
        self.private_reads = 0
        self.files = {'settings.json': self.b.canonical(self.b.contract()),
                      'prompt.txt': b'SYNTHETIC TEST ONLY: produce a protocol fixture.',
                      'evaluator-only/prompt.txt': b'SYNTHETIC TEST ONLY: independent ordinal evaluation.'}

    def schema(self, name):
        return self.b.load(self.b.PACKAGE / 'schemas' / (name + '.schema.json'))

    def hash(self, name):
        return self.b.digest(self.files[name])

    def raw(self, name):
        if name.startswith(('inputs/', 'evaluator-only/')):
            self.private_reads += 1
        return self.files[name]

    def get(self, name):
        return self.b.strict.load_json(self.raw(name))


class ScoringTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue((HERE / 'scoring.py').is_file(), 'AU-v2 blinded scoring module missing')
        self.s = module('au_v2_scoring_test', HERE / 'scoring.py')
        self.b = self.s.bridge
        self.ctx = FixtureContext(self.b)
        self.temp = tempfile.TemporaryDirectory(dir=os.environ.get('TMPDIR', '/home/ghgin/.hermes/cache/scratch'), prefix='au-score-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_unexecuted_run_cannot_load_evaluator_only_material(self):
        with self.assertRaisesRegex(self.b.IntegrationError, 'completed'):
            self.s.build_packet(self.b.canonical({'status': 'unexecuted'}), b'{}', b'{}', self.root, self.ctx)
        self.assertEqual(self.ctx.private_reads, 0)

    def fixture(self, arm='expanded-atlas'):
        helper_module = module('au_v2_synthetic_helpers', HERE / 'tests/test_bridge.py')
        helper = helper_module.BridgeTests()
        helper.setUp()
        self.addCleanup(helper.doCleanups)
        registration, roots, _, _, _ = helper.registration_fixture()
        sid = 'AUv2-01'
        scenario = {'cohort': 'AU-v2', 'scenario_id': sid, 'fictional': True,
                    'title': 'SYNTHETIC TEST ONLY', 'background': 'Infrastructure fixture, not a benchmark case.',
                    'observations': [f'Synthetic observation {i}' for i in range(4)],
                    'constraints': ['Synthetic constraint one', 'Synthetic constraint two'],
                    'request': 'Return a synthetic protocol fixture.'}
        self.ctx.files['inputs/' + sid + '.json'] = self.b.canonical(scenario)
        dims = self.ctx.schema('score')['properties']['dimensions']['required']
        key = {'cohort': 'AU-v2', 'scenario_id': sid, 'access': 'evaluator-only',
               'credible_baseline': 'Synthetic fixture baseline',
               'findings': [{'finding_id': f'{sid}-F{i:02d}', 'dimensions': [dims[0]],
                             'criterion': 'Synthetic finding, not a real answer key'} for i in range(1, 7)],
               'acceptable_alternatives': ['Synthetic A', 'Synthetic B', 'Synthetic C'],
               'unanticipated_alternative_policy': 'Credit defensible alternatives outside this fixture key.',
               'critical_failures': [{'failure_id': sid + '-CF-01', 'endorsement_required': True,
                                      'trigger': 'Synthetic endorsed fixture condition',
                                      'not_triggered_by': 'Rejecting the fixture condition',
                                      'caps': {dims[0]: 1, dims[3]: 2}}]}
        rubric = {'cohort': 'AU-v2', 'rubric_version': '2.0.0', 'scale': [0, 1, 2, 3], 'aggregation': 'none',
                  'dimensions': [{'id': dim, 'anchors': {str(i): f'Synthetic anchor {i}' for i in range(4)}} for dim in dims],
                  'applicability': 'Synthetic retrieval applicability', 'credit_policy': 'Synthetic alternative credit',
                  'critical_failure_policy': 'Synthetic per-dimension caps only', 'score_evidence': 'Exact fixture quotes'}
        self.ctx.files['evaluator-only/keys/' + sid + '.json'] = self.b.canonical(key)
        self.ctx.files['evaluator-only/rubric.json'] = self.b.canonical(rubric)
        registration.update(freeze_manifest_sha256=self.ctx.anchor,
                            prompt_sha256=self.ctx.hash('prompt.txt'), settings_sha256=self.ctx.hash('settings.json'))
        registration_raw = self.b.canonical(registration)
        snapshot = roots[arm]
        manifest = self.b.verify_snapshot(snapshot)
        binding = next(item for item in registration['arms'] if item['id'] == arm)
        broker = self.b.Broker(snapshot, binding['corpus_manifest_sha256'])
        request = {'type': 'read_file', 'request_id': 'fixture-read', 'path': 'solutions/fixture.md.txt', 'offset': 0, 'length': 20}
        result = broker.read(request)
        response = 'Synthetic recommendation. Unacceptable fixture assertion.'
        start = {'type': 'start', 'scenario': scenario, 'prompt': self.ctx.raw('prompt.txt').decode(),
                 'settings_sha256': registration['settings_sha256'], 'inventory': self.b.inventory(manifest),
                 'read_file': 'Exact inventory paths; Unicode offsets/lengths; read_result or read_denied.'}
        ready = {'type': 'ready', 'identity': registration['tested']['identity'],
                 'settings_sha256': registration['settings_sha256'], 'fresh_context': True, 'broker_only': True}
        records = [('sent_start', start), ('received', ready), ('received', request),
                   ('sent_broker', result), ('received', {'type': 'final', 'text': response})]
        events = [{'direction': direction, 'raw_hex': self.b.canonical(value).hex(),
                   'sha256': self.b.digest(self.b.canonical(value)),
                   'observed_at': '2026-10-14T21:00:00+00:00'} for direction, value in records]
        read_log = [{'request_id': request['request_id'], 'path': request['path'], 'offset': 0,
                     'requested_length': 20, 'returned_characters': result['returned_characters'],
                     'content_sha256': result['content_sha256'], 'inventory_sha256': binding['inventory_sha256']}] if result['type'] == 'read_result' else []
        run = {'cohort': 'AU-v2', 'scenario_id': sid, 'run_id': 'synthetic-run-not-executed-by-model',
               'arm': arm, 'status': 'completed', 'registration_sha256': self.b.digest(registration_raw),
               'freeze_manifest_sha256': self.ctx.anchor, 'prompt_sha256': registration['prompt_sha256'],
               'settings_sha256': registration['settings_sha256'], 'scenario_sha256': self.ctx.hash('inputs/' + sid + '.json'),
               'inventory_sha256': binding['inventory_sha256'], 'tested_identity': registration['tested']['identity'],
               'runtime_identity_attested': True, 'response': response, 'response_sha256': self.b.digest(response.encode()),
               'read_log': read_log, 'read_attempts': 1, 'failure_reason': None}
        run_raw = self.b.canonical(run)
        journal = {'format': 'au-v2-execution-journal-v1', 'run_sha256': self.b.digest(run_raw), 'exit_code': 0,
                   'exit_observed_at': '2026-10-14T21:00:00+00:00',
                   'runtime_identity_evidence_sha256': registration['tested']['evidence_sha256'],
                   'events': events, 'stderr_sha256': self.b.digest(b'synthetic stderr, not model execution'),
                   'stderr_hex': b'synthetic stderr, not model execution'.hex()}
        return run_raw, registration_raw, self.b.canonical(journal), snapshot, self.ctx

    def test_completed_fixture_packet_is_blinded_and_receipt_stays_private(self):
        args = self.fixture()
        packet, receipt = self.s.build_packet(*args)
        visible = json.dumps(packet)
        self.assertNotIn('expanded-atlas', visible)
        self.assertNotIn('fixture-provider', visible)
        self.assertNotIn('synthetic-tested', visible)
        self.assertNotIn('observed_at', visible)
        self.assertEqual(packet['response'], 'Synthetic recommendation. Unacceptable fixture assertion.')
        self.assertEqual(packet['reads'][0]['text'], (args[3] / 'files/solutions/fixture.md.txt').read_text()[:20])
        self.assertEqual(receipt['run_sha256'], self.b.digest(args[0]))
        self.assertEqual(receipt['packet_sha256'], self.b.digest(self.b.canonical(packet)))
        self.assertEqual(receipt['arm'], 'expanded-atlas')

    def evaluation_fixture(self, arm='expanded-atlas'):
        args = self.fixture(arm)
        packet, receipt = self.s.build_packet(*args)
        packet_raw, receipt_raw = self.b.canonical(packet), self.b.canonical(receipt)
        draft = {'cohort': 'AU-v2', 'scenario_id': packet['scenario_id'],
                 'run_sha256': packet['run_sha256'], 'response_sha256': packet['response_sha256'],
                 'packet_sha256': receipt['packet_sha256'], 'freeze_manifest_sha256': self.ctx.anchor,
                 'settings_sha256': packet['settings_sha256'], 'evaluator_identity': receipt['evaluator_identity'],
                 'evaluator_role': 'independent_evaluator', 'independence_attested': True, 'blinding_attested': True,
                 'evaluated_at': '2026-10-14T21:01:00+00:00',
                 'dimensions': {dim['id']: {'raw': 3, 'effective': 3, 'rationale': 'Synthetic fixture evidence',
                                            'response_quotes': ['Synthetic recommendation.'], 'omitted_finding_ids': []}
                                for dim in packet['rubric']['dimensions']},
                 'critical_failures': [{'failure_id': packet['scenario_id'] + '-CF-01',
                                        'response_quote': 'Unacceptable fixture assertion.',
                                        'endorsement_explanation': 'Synthetic endorsed fixture condition, not semantic model scoring'}],
                 'alternative_credit': ['Credit a synthetic defensible alternative outside the fixture key'], 'limitations': []}
        return args, packet_raw, receipt_raw, draft

    def test_frozen_context_uses_anchored_schemas_without_inspecting_case_contents(self):
        self.assertTrue(hasattr(self.s, 'FrozenContext'), 'frozen scoring context missing')
        ctx = self.s.FrozenContext()
        self.assertEqual(ctx.anchor, self.b.ANCHOR)
        self.assertEqual(ctx.hash('prompt.txt'), self.b.digest((self.b.PACKAGE / 'prompt.txt').read_bytes()))
        self.assertIn('evidence_and_scope', ctx.schema('score')['properties']['dimensions']['required'])

    def test_effective_scores_use_only_affected_dimension_caps(self):
        self.assertTrue(hasattr(self.s, 'finalize_score'), 'score finalization missing')
        args, packet_raw, receipt_raw, draft = self.evaluation_fixture()
        original = copy.deepcopy(draft)
        final = self.s.finalize_score(*args, packet_raw, receipt_raw, self.b.canonical(draft))
        self.assertEqual(final['dimensions']['evidence_and_scope']['effective'], 1)
        self.assertEqual(final['dimensions']['evaluation_design']['effective'], 2)
        self.assertEqual(final['dimensions']['baseline_and_options']['effective'], 3)
        self.assertEqual(final['alternative_credit'], draft['alternative_credit'])
        self.assertEqual(draft, original)
        self.assertNotIn('aggregate', final)

    def test_packet_and_score_bundles_are_exclusive_and_preserve_raw_draft(self):
        self.assertTrue(hasattr(self.s, 'write_packet_bundle'), 'packet artifact writer missing')
        self.assertTrue(hasattr(self.s, 'write_score_bundle'), 'score artifact writer missing')
        args, packet_raw, receipt_raw, draft = self.evaluation_fixture()
        packet_out, score_out = self.root / 'packet', self.root / 'score'
        info = self.s.write_packet_bundle(packet_out, *args)
        self.assertEqual((packet_out / 'packet.json').read_bytes(), packet_raw)
        self.assertEqual(self.b.digest((packet_out / 'private-receipt.json').read_bytes()), info['receipt_sha256'])
        draft_raw = (json.dumps(draft, indent=2) + '\n').encode()
        score_info = self.s.write_score_bundle(score_out, *args, packet_raw, receipt_raw, draft_raw)
        self.assertEqual((score_out / 'evaluator-draft.json').read_bytes(), draft_raw)
        final = json.loads((score_out / 'score.json').read_bytes())
        self.assertEqual(final['dimensions']['evidence_and_scope']['effective'], 1)
        self.assertEqual(self.b.digest((score_out / 'score.json').read_bytes()), score_info['score_sha256'])
        with self.assertRaises(self.b.IntegrationError):
            self.s.write_packet_bundle(packet_out, *args)
        with self.assertRaises(self.b.IntegrationError):
            self.s.write_score_bundle(score_out, *args, packet_raw, receipt_raw, draft_raw)

    def test_evaluator_cli_packet_and_score_workflow_with_synthetic_context(self):
        self.assertTrue(hasattr(self.s, 'main'), 'evaluator operator CLI missing')
        args, _, _, draft = self.evaluation_fixture()
        inputs = {}
        for name, raw in zip(('run', 'registration', 'journal'), args[:3]):
            inputs[name] = self.root / (name + '.json')
            inputs[name].write_bytes(raw)
        evaluation = self.root / 'synthetic-evaluation.json'
        evaluation.write_bytes(self.b.canonical(draft))
        packet_dir, score_dir = self.root / 'cli-packet', self.root / 'cli-score'
        common = ['--role', 'evaluator-operator', '--run', str(inputs['run']), '--registration', str(inputs['registration']),
                  '--journal', str(inputs['journal']), '--snapshot', str(args[3])]
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = self.s.main(['packet', *common, '--out', str(packet_dir)], context=self.ctx)
        self.assertEqual(code, 0)
        self.assertNotIn('Synthetic recommendation', out.getvalue())
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = self.s.main(['score', *common, '--out', str(score_dir), '--packet', str(packet_dir / 'packet.json'),
                                '--receipt', str(packet_dir / 'private-receipt.json'), '--evaluation', str(evaluation)], context=self.ctx)
        self.assertEqual(code, 0)
        self.assertEqual(json.loads((score_dir / 'score.json').read_bytes())['dimensions']['evidence_and_scope']['effective'], 1)

    def replace_run(self, args, **changes):
        run = self.b.strict.load_json(args[0])
        run.update(changes)
        raw = self.b.canonical(run)
        journal = self.b.strict.load_json(args[2])
        journal['run_sha256'] = self.b.digest(raw)
        return (raw, args[1], self.b.canonical(journal), *args[3:])

    def change_event(self, args, index, transform):
        journal = self.b.strict.load_json(args[2])
        event = journal['events'][index]
        value = self.b.strict.load_json(bytes.fromhex(event['raw_hex']))
        transform(value)
        raw = self.b.canonical(value)
        event.update(raw_hex=raw.hex(), sha256=self.b.digest(raw))
        return (args[0], args[1], self.b.canonical(journal), *args[3:])

    def test_packet_rejects_forged_read_counter(self):
        args = self.replace_run(self.fixture(), read_attempts=2)
        with self.assertRaisesRegex(self.b.IntegrationError, 'counters'):
            self.s.build_packet(*args)

    def test_packet_rejects_response_hash_mismatch(self):
        args = self.replace_run(self.fixture(), response_sha256='a' * 64)
        with self.assertRaisesRegex(self.b.IntegrationError, 'response hash'):
            self.s.build_packet(*args)

    def test_packet_rejects_identity_attestation_false(self):
        args = self.replace_run(self.fixture(), runtime_identity_attested=False)
        with self.assertRaises(self.b.IntegrationError):
            self.s.build_packet(*args)

    def test_packet_rejects_unblinded_start_metadata(self):
        args = self.change_event(self.fixture(), 0, lambda start: start.update(arm='expanded-atlas'))
        with self.assertRaisesRegex(self.b.IntegrationError, 'start payload'):
            self.s.build_packet(*args)

    def test_packet_requires_sent_not_generated_broker_bytes(self):
        args = self.fixture()
        journal = self.b.strict.load_json(args[2])
        journal['events'][3]['direction'] = 'broker_generated'
        args = (args[0], args[1], self.b.canonical(journal), *args[3:])
        with self.assertRaisesRegex(self.b.IntegrationError, 'sent broker'):
            self.s.build_packet(*args)

    def test_packet_rejects_forged_broker_content_even_if_rehashed(self):
        args = self.change_event(self.fixture(), 3, lambda result: result.update(text='forged excerpt'))
        with self.assertRaisesRegex(self.b.IntegrationError, 'sent broker'):
            self.s.build_packet(*args)

    def test_packet_rejects_final_response_disagreement(self):
        args = self.change_event(self.fixture(), 4, lambda result: result.update(text='Different synthetic final'))
        with self.assertRaisesRegex(self.b.IntegrationError, 'final response'):
            self.s.build_packet(*args)

    def test_packet_rejects_output_after_final(self):
        args = self.fixture()
        journal = self.b.strict.load_json(args[2])
        journal['events'].append(copy.deepcopy(journal['events'][4]))
        args = (args[0], args[1], self.b.canonical(journal), *args[3:])
        with self.assertRaisesRegex(self.b.IntegrationError, 'after final'):
            self.s.build_packet(*args)

    def test_packet_rejects_nonzero_exit(self):
        args = self.fixture()
        journal = self.b.strict.load_json(args[2])
        journal['exit_code'] = 1
        with self.assertRaisesRegex(self.b.IntegrationError, 'successful exit'):
            self.s.build_packet(args[0], args[1], self.b.canonical(journal), *args[3:])

    def test_packet_rejects_terminal_wall_budget_violation(self):
        args = self.fixture()
        journal = self.b.strict.load_json(args[2])
        start = datetime.datetime.fromisoformat(journal['events'][0]['observed_at'])
        wall = self.ctx.get('settings.json')['budgets']['solver_wall_seconds']
        journal['exit_observed_at'] = (start + datetime.timedelta(seconds=wall + 1)).isoformat()
        with self.assertRaisesRegex(self.b.IntegrationError, 'time budget'):
            self.s.build_packet(args[0], args[1], self.b.canonical(journal), *args[3:])

    def test_packet_rejects_rehashed_timezone_naive_journal(self):
        args = self.fixture()
        journal = self.b.strict.load_json(args[2])
        journal['events'][0]['observed_at'] = '2026-10-14T21:00:00'
        with self.assertRaisesRegex(self.b.IntegrationError, 'timezone'):
            self.s.build_packet(args[0], args[1], self.b.canonical(journal), *args[3:])

    def test_score_rejects_changed_packet_bytes(self):
        args, packet_raw, receipt_raw, draft = self.evaluation_fixture()
        with self.assertRaisesRegex(self.b.IntegrationError, 'packet/private receipt'):
            self.s.finalize_score(*args, packet_raw + b' ', receipt_raw, self.b.canonical(draft))

    def test_score_rejects_wrong_evaluator_identity(self):
        args, packet_raw, receipt_raw, draft = self.evaluation_fixture()
        draft['evaluator_identity'] = 'synthetic-tested'
        with self.assertRaisesRegex(self.b.IntegrationError, 'identity mismatch'):
            self.s.finalize_score(*args, packet_raw, receipt_raw, self.b.canonical(draft))

    def test_score_rejects_unknown_omitted_finding(self):
        args, packet_raw, receipt_raw, draft = self.evaluation_fixture()
        draft['dimensions']['evidence_and_scope']['omitted_finding_ids'] = ['AUv2-01-F99']
        with self.assertRaisesRegex(self.b.IntegrationError, 'omitted finding'):
            self.s.finalize_score(*args, packet_raw, receipt_raw, self.b.canonical(draft))

    def test_score_rejects_finding_from_other_dimension(self):
        args, packet_raw, receipt_raw, draft = self.evaluation_fixture()
        draft['dimensions']['baseline_and_options']['omitted_finding_ids'] = ['AUv2-01-F01']
        with self.assertRaisesRegex(self.b.IntegrationError, 'omitted finding'):
            self.s.finalize_score(*args, packet_raw, receipt_raw, self.b.canonical(draft))

    def test_score_requires_exact_dimension_quote(self):
        args, packet_raw, receipt_raw, draft = self.evaluation_fixture()
        draft['dimensions']['evidence_and_scope']['response_quotes'] = ['Invented quotation']
        with self.assertRaisesRegex(self.b.IntegrationError, 'exact response substring'):
            self.s.finalize_score(*args, packet_raw, receipt_raw, self.b.canonical(draft))

    def test_score_requires_exact_critical_failure_quote(self):
        args, packet_raw, receipt_raw, draft = self.evaluation_fixture()
        draft['critical_failures'][0]['response_quote'] = 'Invented critical quotation'
        with self.assertRaisesRegex(self.b.IntegrationError, 'exact response substring'):
            self.s.finalize_score(*args, packet_raw, receipt_raw, self.b.canonical(draft))

    def test_score_rejects_duplicate_critical_failure(self):
        args, packet_raw, receipt_raw, draft = self.evaluation_fixture()
        draft['critical_failures'].append(copy.deepcopy(draft['critical_failures'][0]))
        with self.assertRaisesRegex(self.b.IntegrationError, 'duplicate critical'):
            self.s.finalize_score(*args, packet_raw, receipt_raw, self.b.canonical(draft))

    def test_score_requires_specific_dimension_evidence(self):
        args, packet_raw, receipt_raw, draft = self.evaluation_fixture()
        draft['dimensions']['evidence_and_scope']['response_quotes'] = []
        with self.assertRaisesRegex(self.b.IntegrationError, 'dimension needs'):
            self.s.finalize_score(*args, packet_raw, receipt_raw, self.b.canonical(draft))

    def test_no_atlas_retrieval_is_null_not_zero(self):
        args, packet_raw, receipt_raw, draft = self.evaluation_fixture('no-atlas')
        draft['dimensions']['retrieval_grounding'].update(raw=None, effective=None, rationale='not_applicable: empty inventory')
        final = self.s.finalize_score(*args, packet_raw, receipt_raw, self.b.canonical(draft))
        self.assertIsNone(final['dimensions']['retrieval_grounding']['effective'])
        draft['dimensions']['retrieval_grounding'].update(raw=0, effective=0)
        with self.assertRaisesRegex(self.b.IntegrationError, 'null/not_applicable'):
            self.s.finalize_score(*args, packet_raw, receipt_raw, self.b.canonical(draft))

    def test_applicable_retrieval_cannot_be_null(self):
        args, packet_raw, receipt_raw, draft = self.evaluation_fixture()
        draft['dimensions']['retrieval_grounding'].update(raw=None, effective=None)
        with self.assertRaisesRegex(self.b.IntegrationError, 'ordinal raw'):
            self.s.finalize_score(*args, packet_raw, receipt_raw, self.b.canonical(draft))

    def test_read_attempt_count_is_visible_without_unblinding(self):
        packet, _ = self.s.build_packet(*self.fixture())
        self.assertIn('read_attempts', packet, 'evaluator packet loses denied/repeated attempt accounting')
        self.assertEqual(packet['read_attempts'], 1)

    def test_packet_rejects_boolean_integer_alias_in_actual_start(self):
        args = self.change_event(self.fixture(), 0, lambda start: start['scenario'].update(fictional=1))
        with self.assertRaisesRegex(self.b.IntegrationError, 'start payload'):
            self.s.build_packet(*args)

    def test_packet_rejects_nonfinite_exponent_in_registration(self):
        args = self.fixture()
        registration = self.b.strict.load_json(args[1])
        registration['generation']['temperature'].update(effective=float('inf'), enforcement='wire')
        registration_raw = json.dumps(registration).replace('Infinity', '1e999').encode()
        run = self.b.strict.load_json(args[0])
        run['registration_sha256'] = self.b.digest(registration_raw)
        run_raw = self.b.canonical(run)
        journal = self.b.strict.load_json(args[2])
        journal['run_sha256'] = self.b.digest(run_raw)
        with self.assertRaisesRegex(self.b.IntegrationError, 'nonfinite'):
            self.s.build_packet(run_raw, registration_raw, self.b.canonical(journal), *args[3:])

    def test_packet_rejects_nonfinite_replayed_read_even_when_broker_denies_it(self):
        args = self.fixture()
        journal = self.b.strict.load_json(args[2])
        request = self.b.strict.load_json(bytes.fromhex(journal['events'][2]['raw_hex']))
        request['overflow'] = float('inf')
        raw = (json.dumps(request).replace('Infinity', '1e999') + '\n').encode()
        journal['events'][2].update(raw_hex=raw.hex(), sha256=self.b.digest(raw))
        registration = self.b.strict.load_json(args[1])
        binding = next(item for item in registration['arms'] if item['id'] == 'expanded-atlas')
        broker = self.b.Broker(args[3], binding['corpus_manifest_sha256'])
        reply = broker.read(self.b.strict.load_json(raw))
        self.assertEqual(reply['type'], 'read_denied')
        sent = self.b.canonical(reply)
        journal['events'][3].update(raw_hex=sent.hex(), sha256=self.b.digest(sent))
        run = self.b.strict.load_json(args[0])
        run['read_log'] = []
        run_raw = self.b.canonical(run)
        journal['run_sha256'] = self.b.digest(run_raw)
        with self.assertRaisesRegex(self.b.IntegrationError, 'nonfinite'):
            self.s.build_packet(run_raw, args[1], self.b.canonical(journal), *args[3:])

    def test_packet_rejects_unsupported_setting_with_effective_value(self):
        args = self.fixture()
        registration = self.b.strict.load_json(args[1])
        registration['generation']['temperature'].update(effective=0.5, limitation='')
        registration_raw = self.b.canonical(registration)
        run = self.b.strict.load_json(args[0])
        run['registration_sha256'] = self.b.digest(registration_raw)
        run_raw = self.b.canonical(run)
        journal = self.b.strict.load_json(args[2])
        journal['run_sha256'] = self.b.digest(run_raw)
        with self.assertRaisesRegex(self.b.IntegrationError, 'unsupported setting'):
            self.s.build_packet(run_raw, registration_raw, self.b.canonical(journal), *args[3:])


if __name__ == '__main__':
    unittest.main()
