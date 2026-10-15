"""Synthetic infrastructure checks only: no cases, keys, models or scores."""
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path
import tempfile
import unittest

HERE = Path(__file__).resolve().parents[1]


def load_bridge():
    spec = importlib.util.spec_from_file_location('au_v2_bridge_test', HERE / 'bridge.py')
    assert spec is not None and spec.loader is not None
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


class BridgeTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue((HERE / 'bridge.py').is_file(), 'AU-v2 integration bridge is missing')
        self.b = load_bridge()
        self.temp = tempfile.TemporaryDirectory(dir=os.environ.get('TMPDIR', '/home/ghgin/.hermes/cache/scratch'), prefix='au-bridge-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / 'source'
        self.source.mkdir()

    def fixture_card(self):
        text = ('---\nid: SOL-01-999\ntitle: Synthetic fixture\ntype: solution\n'
                'domain: "01"\nsummary: Synthetic discovery metadata only.\n---\n'
                '# Synthetic fixture\nΑБ🙂 evidence.\n')
        path = self.source / 'solutions' / 'fixture.md'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')
        return text

    def test_snapshot_export_uses_only_allowlisted_knowledge(self):
        text = self.fixture_card()
        for name in ['README.md', 'CATALOG.md', 'guides/answer.md', 'validation/secret.md', 'deep-dives/review-notes.md']:
            path = self.source / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('not corpus knowledge')
        out = self.root / 'snapshot'
        self.b.prepare_snapshot(self.source, out, 'expanded-atlas')
        snapshot = self.b.verify_snapshot(out)
        self.assertEqual(set(snapshot['files']), {'solutions/fixture.md.txt', 'index/L0.json'})
        self.assertEqual((out / 'files/solutions/fixture.md.txt').read_text(), text)
        l0 = json.loads((out / 'files/index/L0.json').read_text())
        self.assertEqual(l0['cards'][0]['path'], 'solutions/fixture.md.txt')
        self.assertNotIn('expanded-atlas', json.dumps(l0))

    def test_review_named_knowledge_card_is_not_a_review_artifact(self):
        self.fixture_card()
        (self.source / 'solutions/fixture.md').rename(self.source / 'solutions/probability-sampled-review.md')
        out = self.root / 'snapshot'
        manifest = self.b.prepare_snapshot(self.source, out, 'expanded-atlas')
        self.assertEqual(manifest['card_ids'], ['SOL-01-999'])

    def test_preparation_plan_preserves_frozen_three_arm_rotation(self):
        self.assertTrue(hasattr(self.b, 'preparation_plan'), 'preparation_plan missing')
        self.fixture_card()
        roots = {}
        for arm in self.b.ARMS:
            root = self.root / arm
            self.b.prepare_snapshot(None if arm == 'no-atlas' else self.source, root, arm)
            roots[arm] = root
        plan = self.b.preparation_plan(roots)
        self.assertEqual(len(plan['cells']), 24)
        self.assertEqual([c['arm'] for c in plan['cells'][:9]], [
            'baseline-atlas', 'expanded-atlas', 'no-atlas',
            'expanded-atlas', 'no-atlas', 'baseline-atlas',
            'no-atlas', 'baseline-atlas', 'expanded-atlas'])
        self.assertTrue(all(c['status'] == 'unexecuted' for c in plan['cells']))
        self.assertEqual(plan['actual_runs'], 0)
        self.assertEqual(plan['execution_eligibility'], 'blocked')

    def test_broker_returns_au_v2_unicode_slice_with_legacy_accounting(self):
        self.assertTrue(hasattr(self.b, 'Broker'), 'AU-v2 Broker missing')
        text = self.fixture_card()
        out = self.root / 'snapshot'
        self.b.prepare_snapshot(self.source, out, 'expanded-atlas')
        anchor = self.b.digest((out / 'corpus-manifest.json').read_bytes())
        broker = self.b.Broker(out, anchor)
        self.assertIsInstance(broker, self.b.legacy.ReadBroker)
        request = {'type': 'read_file', 'request_id': 'r1', 'path': 'solutions/fixture.md.txt',
                   'offset': text.index('Α'), 'length': 3}
        result = broker.read(request)
        self.assertEqual(result['text'], 'ΑБ🙂')
        self.assertEqual(result['returned_characters'], 3)
        self.assertEqual(result['content_sha256'], self.b.digest('ΑБ🙂'.encode()))
        self.assertEqual(broker.attempts, 1)
        self.assertEqual(broker.successes, 1)
        self.assertEqual(broker.logs[0]['inventory_sha256'], broker.inventory_sha256)
        self.assertEqual(set(result), {'type', 'request_id', 'path', 'offset', 'text',
                                       'returned_characters', 'content_sha256'})

    def broker(self, empty=False):
        if not empty:
            self.fixture_card()
        out = self.root / 'snapshot'
        self.b.prepare_snapshot(None if empty else self.source, out,
                                'no-atlas' if empty else 'expanded-atlas')
        return self.b.Broker(out, self.b.digest((out / 'corpus-manifest.json').read_bytes()))

    def request(self, **overrides):
        value = {'type': 'read_file', 'request_id': 'r1', 'path': 'solutions/fixture.md.txt',
                 'offset': 0, 'length': 1}
        value.update(overrides)
        return value

    def test_over_budget_read_fails_closed_and_retains_attempt(self):
        broker = self.broker()
        with self.assertRaises(self.b.IntegrationError):
            broker.read(self.request(length=broker.budgets['max_chunk_chars'] + 1))
        self.assertTrue(broker.failed)
        self.assertEqual(broker.attempts, 1)
        self.assertEqual(len(broker.logs), 1)
        self.assertEqual(broker.logs[0]['inventory_sha256'], broker.inventory_sha256)

    def test_malformed_request_is_denied_and_counted(self):
        broker = self.broker()
        result = broker.read(self.request(undeclared_field='no'))
        self.assertEqual(result['type'], 'read_denied')
        self.assertEqual(broker.attempts, 1)
        self.assertEqual(broker.successes, 0)
        self.assertNotIn('text', result)

    def test_symlink_parent_replacement_cannot_return_content(self):
        broker = self.broker()
        parent = broker.corpus / 'files/solutions'
        moved = broker.corpus / 'moved'
        parent.rename(moved)
        parent.symlink_to(moved, target_is_directory=True)
        with self.assertRaises(self.b.IntegrationError):
            broker.read(self.request())
        self.assertEqual(broker.attempts, 1)
        self.assertEqual(broker.successes, 0)

    def test_denied_no_atlas_attempts_exhaust_frozen_budget(self):
        broker = self.broker(empty=True)
        for i in range(broker.budgets['max_read_attempts']):
            self.assertEqual(broker.read(self.request(request_id=f'r{i}'))['type'], 'read_denied')
        with self.assertRaises(self.b.IntegrationError):
            broker.read(self.request(request_id='overflow'))
        self.assertEqual(broker.successes, 0)
        self.assertEqual(len(broker.logs), broker.attempts)

    def test_protocol_requires_ready_then_final_and_successful_exit(self):
        self.assertTrue(hasattr(self.b, 'Session'), 'AU-v2 protocol Session missing')
        broker = self.broker()
        session = self.b.Session(broker, 'synthetic-registered-identity', 'a' * 64)
        ready = {'type': 'ready', 'identity': 'synthetic-registered-identity',
                 'settings_sha256': 'a' * 64, 'fresh_context': True, 'broker_only': True}
        self.assertIsNone(session.handle(self.b.canonical(ready)))
        response = session.handle(self.b.canonical(self.request()))
        self.assertEqual(response['type'], 'read_result')
        session.handle(self.b.canonical({'type': 'final', 'text': 'Synthetic protocol fixture, not a model answer.'}))
        self.assertEqual(session.finish(0), 'Synthetic protocol fixture, not a model answer.')
        self.assertEqual(session.events[0]['raw_hex'], self.b.canonical(ready).hex())

    def registration_fixture(self):
        self.fixture_card()
        roots = {}
        for arm in self.b.ARMS:
            roots[arm] = self.root / arm
            self.b.prepare_snapshot(None if arm == 'no-atlas' else self.source, roots[arm], arm)
        plan = self.b.preparation_plan(roots)
        evidence = self.root / 'evidence'
        evidence.mkdir()
        identities = {}
        for role in ('tested', 'evaluator'):
            record = {'kind': 'model-attestation', 'role': role, 'identity': f'synthetic-{role}',
                      'provider': 'fixture-provider', 'model': f'fixture-{role}', 'version': 'fixture-version',
                      'fresh_process': True, 'fresh_conversation': True, 'independence_attested': True,
                      'broker_only': True, 'callable_tools': 0,
                      'signed_conflict_declaration': 'SYNTHETIC TEST ONLY, not an operator attestation'}
            raw = self.b.canonical(record)
            hash_ = self.b.digest(raw)
            (evidence / (hash_ + '.json')).write_bytes(raw)
            identities[role] = {key: record[key] for key in ('identity', 'provider', 'model', 'version',
                                                           'fresh_process', 'fresh_conversation', 'independence_attested')}
            identities[role].update(attested=True, evidence_sha256=hash_)
        generation = {}
        for setting in ('temperature', 'top_p', 'seed', 'provider_output_token_limit'):
            record = {'kind': 'generation-attestation', 'setting': setting, 'requested': None,
                      'effective': None, 'enforcement': 'unsupported', 'cross_arm_equivalence': True}
            name = setting + '.json'
            (evidence / name).write_bytes(self.b.canonical(record))
            generation[setting] = {'requested': None, 'effective': None, 'enforcement': 'unsupported',
                                   'evidence': name, 'limitation': 'Synthetic unsupported setting'}
        runtime = self.root / 'synthetic-runtime.txt'
        adapter = self.root / 'synthetic-adapter.txt'
        runtime.write_text('synthetic runtime bytes, not executing')
        adapter.write_text('synthetic adapter bytes, not executing')
        registration = {'cohort': 'AU-v2', 'registration_id': 'synthetic-only',
                        'freeze_manifest_sha256': plan['freeze_manifest_sha256'],
                        'prompt_sha256': plan['prompt_sha256'], 'settings_sha256': plan['settings_sha256'],
                        'runtime_sha256': self.b.digest(runtime.read_bytes()),
                        'adapter_sha256': self.b.digest(adapter.read_bytes()),
                        'tested': identities['tested'], 'evaluator': identities['evaluator'],
                        'distinct_models_attested': True, 'author_conflicts_resolved': True,
                        'settings_attested': True, 'arm_equivalence_attested': True, 'broker_only_attested': True,
                        'generation': generation, 'arms': plan['arms'], 'planned_cells': 24,
                        'registered_at': 'synthetic-fixture'}
        return registration, roots, evidence, runtime, adapter

    def test_registration_checks_bound_evidence_without_granting_execution(self):
        self.assertTrue(hasattr(self.b, 'validate_registration'), 'registration validation missing')
        args = self.registration_fixture()
        result = self.b.validate_registration(*args)
        self.assertTrue(result['structure_and_bindings_checked'])
        self.assertEqual(result['execution_eligibility'], 'blocked')
        args[0]['tested']['evidence_sha256'] = 'f' * 64
        with self.assertRaises(self.b.IntegrationError):
            self.b.validate_registration(*args)

    def test_cli_prepares_snapshot_with_no_dispatch_command(self):
        self.fixture_card()
        out = self.root / 'cli-snapshot'
        proc = subprocess.run([sys.executable, '-B', str(HERE / 'bridge.py'), 'prepare',
                               '--source', str(self.source), '--arm', 'expanded-atlas', '--out', str(out)],
                              capture_output=True, text=True, check=False)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertTrue(proc.stdout.strip(), 'offline CLI returned no artifact report')
        result = json.loads(proc.stdout)
        self.assertEqual(result['cards'], 1)
        self.assertTrue((out / 'corpus-manifest.json').is_file())
        proc = subprocess.run([sys.executable, '-B', str(HERE / 'bridge.py'), 'run'],
                              capture_output=True, text=True, check=False)
        self.assertNotEqual(proc.returncode, 0)

    def test_export_rejects_symlink_output_ancestor(self):
        self.fixture_card()
        real = self.root / 'real'
        real.mkdir()
        alias = self.root / 'alias'
        alias.symlink_to(real, target_is_directory=True)
        with self.assertRaises(self.b.IntegrationError):
            self.b.prepare_snapshot(self.source, alias / 'snapshot', 'expanded-atlas')
        self.assertFalse((real / 'snapshot').exists())

    def test_snapshot_rejects_rehashed_but_false_l0(self):
        broker = self.broker()
        path = broker.corpus / 'files/index/L0.json'
        false = self.b.canonical({'description': 'false', 'cards': []})
        path.write_bytes(false)
        mpath = broker.corpus / 'corpus-manifest.json'
        manifest = json.loads(mpath.read_text())
        manifest['files']['index/L0.json'].update(bytes=len(false), sha256=self.b.digest(false))
        mpath.write_bytes(self.b.canonical(manifest))
        with self.assertRaises(self.b.IntegrationError):
            self.b.verify_snapshot(broker.corpus)

    def test_registration_rejects_missing_null_evidence_field(self):
        args = self.registration_fixture()
        path = args[2] / 'temperature.json'
        record = json.loads(path.read_text())
        del record['effective']
        path.write_bytes(self.b.canonical(record))
        with self.assertRaises(self.b.IntegrationError):
            self.b.validate_registration(*args)

    def test_protocol_nonbyte_input_is_a_terminal_validation_failure(self):
        session = self.b.Session(self.broker(), 'fixture', 'a' * 64)
        with self.assertRaises(self.b.IntegrationError):
            session.handle('not bytes')
        self.assertEqual(session.state, 'failed')

    def ready(self, session):
        return self.b.canonical({'type': 'ready', 'identity': session.identity,
                                 'settings_sha256': session.settings_sha256,
                                 'fresh_context': True, 'broker_only': True})

    def test_protocol_requires_nonempty_registered_identity(self):
        with self.assertRaises(self.b.IntegrationError):
            self.b.Session(self.broker(), '', 'a' * 64)

    def test_protocol_denies_read_before_ready(self):
        session = self.b.Session(self.broker(), 'fixture', 'a' * 64)
        with self.assertRaises(self.b.IntegrationError):
            session.handle(self.b.canonical(self.request()))
        self.assertEqual(session.state, 'failed')

    def test_protocol_denies_identity_mismatch(self):
        session = self.b.Session(self.broker(), 'fixture', 'a' * 64)
        ready = json.loads(self.ready(session))
        ready['identity'] = 'other-model'
        with self.assertRaises(self.b.IntegrationError):
            session.handle(self.b.canonical(ready))

    def test_protocol_denies_settings_mismatch(self):
        session = self.b.Session(self.broker(), 'fixture', 'a' * 64)
        ready = json.loads(self.ready(session))
        ready['settings_sha256'] = 'b' * 64
        with self.assertRaises(self.b.IntegrationError):
            session.handle(self.b.canonical(ready))

    def test_protocol_rejects_duplicate_json_keys(self):
        session = self.b.Session(self.broker(), 'fixture', 'a' * 64)
        with self.assertRaises(self.b.IntegrationError):
            session.handle(b'{"type":"ready","type":"final"}\n')

    def test_protocol_rejects_output_after_final(self):
        session = self.b.Session(self.broker(), 'fixture', 'a' * 64)
        session.handle(self.ready(session))
        session.handle(self.b.canonical({'type': 'final', 'text': 'Synthetic fixture'}))
        with self.assertRaises(self.b.IntegrationError):
            session.handle(self.b.canonical(self.request()))
        with self.assertRaises(self.b.IntegrationError):
            session.finish(0)

    def test_protocol_rejects_nonzero_exit(self):
        session = self.b.Session(self.broker(), 'fixture', 'a' * 64)
        session.handle(self.ready(session))
        session.handle(self.b.canonical({'type': 'final', 'text': 'Synthetic fixture'}))
        with self.assertRaises(self.b.IntegrationError):
            session.finish(1)

    def test_protocol_rejects_oversized_final_without_truncation(self):
        session = self.b.Session(self.broker(), 'fixture', 'a' * 64)
        session.handle(self.ready(session))
        with self.assertRaises(self.b.IntegrationError):
            session.handle(self.b.canonical({'type': 'final', 'text': 'a' * (session.budgets['final_characters'] + 1)}))
        self.assertIsNone(session.response)

    def test_snapshot_rejects_payload_mutation(self):
        broker = self.broker()
        (broker.corpus / 'files/solutions/fixture.md.txt').write_text('changed')
        with self.assertRaises(self.b.IntegrationError):
            self.b.verify_snapshot(broker.corpus)

    def test_snapshot_rejects_added_file(self):
        broker = self.broker()
        (broker.corpus / 'files/extra.txt').write_text('extra')
        with self.assertRaises(self.b.IntegrationError):
            self.b.verify_snapshot(broker.corpus)

    def test_snapshot_rejects_overwrite(self):
        broker = self.broker()
        with self.assertRaises(self.b.IntegrationError):
            self.b.prepare_snapshot(self.source, broker.corpus, 'expanded-atlas')

    def test_broker_denies_path_aliases_and_counts_them(self):
        broker = self.broker()
        paths = ('../secret', '/etc/passwd', 'solutions/../solutions/fixture.md.txt',
                 './solutions/fixture.md.txt', 'validation/key.json')
        for i, path in enumerate(paths):
            result = broker.read(self.request(path=path, request_id=f'r{i}'))
            self.assertEqual(result['type'], 'read_denied')
            self.assertNotIn('text', result)
        self.assertEqual(broker.attempts, len(paths))
        self.assertEqual(broker.successes, 0)

    def test_broker_counts_repeated_content_then_fails_read_budget(self):
        broker = self.broker()
        for i in range(broker.budgets['max_reads']):
            self.assertEqual(broker.read(self.request(request_id=f'r{i}'))['type'], 'read_result')
        self.assertEqual(broker.chars, broker.budgets['max_reads'])
        with self.assertRaises(self.b.IntegrationError):
            broker.read(self.request(request_id='overflow'))

    def test_broker_fails_character_budget_before_returning_content(self):
        self.fixture_card()
        path = self.source / 'solutions/fixture.md'
        path.write_text(path.read_text() + ('α' * 70000))
        out = self.root / 'snapshot'
        self.b.prepare_snapshot(self.source, out, 'expanded-atlas')
        broker = self.b.Broker(out, self.b.digest((out / 'corpus-manifest.json').read_bytes()))
        chunk = broker.budgets['max_chunk_chars']
        for i in range(broker.budgets['max_read_chars'] // chunk):
            broker.read(self.request(request_id=f'r{i}', length=chunk))
        with self.assertRaises(self.b.IntegrationError):
            broker.read(self.request(request_id='overflow', length=chunk))
        self.assertEqual(broker.logs[-1]['content'], '')

    def test_broker_detects_mutation_during_read(self):
        broker = self.broker()
        (broker.corpus / 'files/solutions/fixture.md.txt').write_text('changed')
        with self.assertRaises(self.b.IntegrationError):
            broker.read(self.request())
        self.assertEqual(len(broker.logs), broker.attempts)

    def test_registration_rejects_duplicate_arms(self):
        args = self.registration_fixture()
        args[0]['arms'][1] = dict(args[0]['arms'][0])
        with self.assertRaises(self.b.IntegrationError):
            self.b.validate_registration(*args)

    def test_registration_rejects_aliases_of_same_model(self):
        args = self.registration_fixture()
        args[0]['evaluator'].update(model=args[0]['tested']['model'], version=args[0]['tested']['version'])
        with self.assertRaises(self.b.IntegrationError):
            self.b.validate_registration(*args)

    def test_registration_rejects_claimed_unsupported_effective_setting(self):
        args = self.registration_fixture()
        args[0]['generation']['temperature']['effective'] = 0.5
        path = args[2] / 'temperature.json'
        record = json.loads(path.read_text())
        record['effective'] = 0.5
        path.write_bytes(self.b.canonical(record))
        with self.assertRaises(self.b.IntegrationError):
            self.b.validate_registration(*args)


if __name__ == '__main__':
    unittest.main()
