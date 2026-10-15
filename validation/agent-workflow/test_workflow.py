"""Offline fixtures only: these are not solver runs or evaluator scores."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

PACKAGE = Path(__file__).resolve().parent

class WorkflowTests(unittest.TestCase):
    def module(self):
        path = PACKAGE / 'workflow.py'
        self.assertTrue(path.exists(), 'missing offline workflow implementation')
        spec = importlib.util.spec_from_file_location('agent_workflow', path)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_frozen_plan_has_eight_tasks_four_arms_zero_runs(self):
        w = self.module()
        manifest = w.verify()
        plan = w.plan()
        self.assertEqual(len(manifest['scenarios']), 8)
        self.assertEqual(len(plan['cells']), 32)
        self.assertEqual(set(c['arm'] for c in plan['cells']), {'A', 'B', 'C', 'D'})
        self.assertEqual(plan['genuine_runs'], 0)
        self.assertEqual(plan['genuine_scores'], 0)
        self.assertEqual(plan['execution_eligibility'], 'unavailable')
        self.assertTrue(all(c['status'] == 'unexecuted' for c in plan['cells']))

    def test_prepare_inventory_cannot_expose_keys_or_protocol(self):
        w = self.module()
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'prepared'
            w.prepare(out)
            w.verify_prepared(out)
            for arm in w.ARMS:
                inv = w.solver_inventory(out, arm)
                for entry in inv:
                    self.assertEqual(set(entry), {'path', 'layer', 'bytes'})
                    self.assertFalse(any(s in entry['path'] for s in ('frozen/', 'evaluator/', 'checklists', 'rubric', 'protocol', 'workflow.py', 'validation/')))
                self.assertEqual(inv, w.load(out / 'solver' / arm / 'inventory.json'))
            self.assertEqual(w.solver_inventory(out, 'A'), [])
            dpaths = {x['path'] for x in w.solver_inventory(out, 'D')}
            self.assertIn('guides/project-intake.md.txt', dpaths)
            self.assertIn('indexes/tasks/graph.md.txt', dpaths)
            for arm in ('B', 'C'):
                self.assertFalse(any(x['path'].startswith('guides/') for x in w.solver_inventory(out, arm)))
            with self.assertRaises(w.WorkflowError):
                w.prepare(out)

    def test_broker_counts_repeated_unicode_and_denied_reads_without_billing(self):
        w = self.module()
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'prepared'
            w.prepare(out)
            broker = w.Broker(out, 'D')
            path = 'START_HERE.md.txt'
            text = (out / 'snapshots/D/files' / path).read_text()
            offset = next(i for i, c in enumerate(text) if ord(c) > 127)
            for rid in ('one', 'two'):
                result = broker.read({'type':'read_file','request_id':rid,'path':path,'offset':offset,'length':1})
                self.assertEqual(result['content'], text[offset:offset+1])
            broker.read({'type':'read_file','request_id':'deny','path':'../../frozen/evaluator/checklists.json','offset':0,'length':1})
            account = broker.accounting()
            self.assertEqual(account['read_attempts'], 3)
            self.assertEqual(account['successful_reads'], 2)
            self.assertEqual(account['documents'], 1)
            self.assertEqual(account['retrieved_characters'], 2)
            self.assertEqual(account['retrieved_bytes'], 2 * len(text[offset].encode()))
            self.assertIsNone(account['retrieved_text_tokens'])
            self.assertIsNone(account['provider_input_tokens'])
            self.assertIsNone(account['wall_seconds'])
            self.assertIsNone(account['cost_usd'])
            self.assertEqual(broker.logs[-1]['returned_bytes'], 0)
            self.assertTrue(all(x['evaluator_relevance'] is None for x in broker.logs))
            self.assertEqual(broker.logs[0]['offset_unit'], 'unicode-code-points')

    def test_tamper_on_all_frozen_inputs_and_manifest_is_rejected(self):
        import shutil
        w = self.module()
        frozen = w.verify()
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / 'package'
            shutil.copytree(PACKAGE / 'frozen', copy / 'frozen')
            shutil.copyfile(PACKAGE / 'freeze-manifest.json', copy / 'freeze-manifest.json')
            for name in frozen['files']:
                target = copy / 'frozen' / name
                original = target.read_bytes()
                target.write_bytes(original + b' ')
                with self.assertRaises(w.WorkflowError, msg=name):
                    w.verify(copy)
                target.write_bytes(original)
            (copy / 'freeze-manifest.json').write_bytes(b'{}')
            with self.assertRaisesRegex(w.WorkflowError, 'anchor'):
                w.verify(copy)

    def test_tampered_preparation_receipt_and_extra_inventory_fail_closed(self):
        w = self.module()
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'prepared'
            w.prepare(out)
            broker = w.Broker(out, 'D')
            path = out / 'snapshots/D/files/START_HERE.md.txt'
            raw = path.read_bytes()
            path.write_bytes(raw + b'x')
            # Rehashing an untrusted receipt cannot authorize content different from frozen sources.
            receipt_path = out / 'preparation-manifest.json'
            receipt = w.load(receipt_path)
            receipt['files']['snapshots/D/files/START_HERE.md.txt'] = w.digest(path.read_bytes())
            receipt_path.write_bytes(w.canonical(receipt))
            with self.assertRaises(w.WorkflowError):
                broker.read({'type':'read_file','request_id':'tamper','path':'START_HERE.md.txt','offset':0,'length':20})
            self.assertEqual(len(broker.logs), 1)
            self.assertEqual(broker.logs[0]['returned_bytes'], 0)
            self.assertTrue(broker.failed)
            self.assertEqual(broker.attempts, 1)

    def test_invalid_requests_and_fatal_budget_keep_every_attempt(self):
        w = self.module()
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'prepared'
            w.prepare(out)
            broker = w.Broker(out, 'D')
            req = {'type':'read_file','request_id':'original','path':'START_HERE.md.txt','offset':0,'length':4}
            broker.read(req)
            req['length'] = 777
            self.assertEqual(broker.logs[0]['request']['length'], 4, 'audit request must be a retained value, not caller alias')
            for request in [None, {}, {'type':'final'}, {'type':'read_file','request_id':'bool','path':'START_HERE.md.txt','offset':True,'length':1}]:
                result = broker.read(request)
                self.assertIsNotNone(result['error'])
                self.assertEqual(result['content'], '')
            with self.assertRaises(w.WorkflowError):
                broker.read({'type':'read_file','request_id':'huge','path':'START_HERE.md.txt','offset':0,'length':8001})
            with self.assertRaises(w.WorkflowError):
                broker.read({'type':'read_file','request_id':'post-failure','path':'START_HERE.md.txt','offset':0,'length':1})
            self.assertEqual(broker.attempts, 7)
            self.assertEqual(len(broker.logs), 7)
            self.assertEqual(broker.logs[-1]['returned_bytes'], 0)

    def test_report_has_empty_per_task_frontiers_and_gate_cannot_be_asserted_ready(self):
        w = self.module()
        report = w.report()
        self.assertEqual(report['genuine_runs'], 0)
        self.assertEqual(report['genuine_scores'], 0)
        self.assertEqual(len(report['tasks']), 8)
        for task in report['tasks']:
            self.assertEqual(task['quality_cost_frontier'], [])
            self.assertEqual(set(task['arms']), set(w.ARMS))
            for cell in task['arms'].values():
                self.assertIsNone(cell['quality_dimensions'])
                self.assertIsNone(cell['retrieved_bytes'])
                self.assertEqual(cell['quality_status'], 'unscored')
        self.assertIn('confounds', report['navigation_confound'])
        with self.assertRaisesRegex(w.WorkflowError, 'unavailable'):
            w.gate_real_run()

    def test_attempt_read_character_budgets_and_empty_arm_fail_closed(self):
        w = self.module()
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'prepared'
            w.prepare(out)
            # Exercise frozen numeric limits, not monkeypatched settings.
            a = w.Broker(out, 'A')
            for i in range(24):
                self.assertIsNotNone(a.read({'type':'read_file','request_id':str(i),'path':'index/L0.json','offset':0,'length':1})['error'])
            with self.assertRaisesRegex(w.WorkflowError, 'attempt'):
                a.read({'type':'read_file','request_id':'25','path':'index/L0.json','offset':0,'length':1})
            self.assertEqual(a.attempts, 25)
            self.assertEqual(a.accounting()['retrieved_bytes'], 0)
            b = w.Broker(out, 'D')
            for i in range(16):
                b.read({'type':'read_file','request_id':str(i),'path':'START_HERE.md.txt','offset':0,'length':1})
            with self.assertRaisesRegex(w.WorkflowError, 'successful-read'):
                b.read({'type':'read_file','request_id':'17','path':'START_HERE.md.txt','offset':0,'length':1})
            c = w.Broker(out, 'C')
            path = next(x['path'] for x in w.solver_inventory(out, 'C') if x['bytes'] > 10000)
            for i in range(6):
                c.read({'type':'read_file','request_id':str(i),'path':path,'offset':0,'length':8000})
            with self.assertRaisesRegex(w.WorkflowError, 'character budget'):
                c.read({'type':'read_file','request_id':'7','path':path,'offset':0,'length':1})
            self.assertEqual(c.accounting()['retrieved_characters'], 48000)
            self.assertEqual(c.logs[-1]['returned_bytes'], 0)

    def test_extra_file_and_symlink_preparation_rejected(self):
        w = self.module()
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'prepared'
            w.prepare(out)
            extra = out / 'solver/D/secret-key.json'
            extra.write_text('{}')
            with self.assertRaisesRegex(w.WorkflowError, 'inventory'):
                w.verify_prepared(out)
            extra.unlink()
            target = out / 'snapshots/D/files/START_HERE.md.txt'
            original = target.read_bytes()
            replacement = Path(tmp) / 'replacement'
            replacement.write_bytes(original)
            target.unlink()
            target.symlink_to(replacement)
            with self.assertRaisesRegex(w.WorkflowError, 'symlink'):
                w.verify_prepared(out)

    def test_optional_pinned_tokenizer_is_offline_and_counts_each_return(self):
        w = self.module()
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / 'not-the-asset'
            bad.write_bytes(b'wrong encoding')
            with self.assertRaisesRegex(w.WorkflowError, 'tokenizer asset'):
                w.OfflineTokenizer(bad)
        asset = Path('/home/ghgin/.hermes/cache/scratch/data-gym-cache/9b5ad71b2ce5302211f9c61530b329a4922fc6a4')
        if not asset.exists():
            self.skipTest('optional pinned offline tokenizer asset absent')
        tokenizer = w.OfflineTokenizer(asset)
        self.assertEqual(tokenizer.count('hello world'), 2)
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'prepared'
            w.prepare(out)
            broker = w.Broker(out, 'D', tokenizer_asset=asset)
            for rid in ('first', 'again'):
                broker.read({'type':'read_file','request_id':rid,'path':'START_HERE.md.txt','offset':0,'length':500})
            account = broker.accounting()
            self.assertEqual(account['retrieved_text_tokens'], sum(x['returned_text_tokens'] for x in broker.logs))
            self.assertGreater(account['retrieved_text_tokens'], 0)
            self.assertEqual(account['tokenizer']['version'], '0.12.0')
            self.assertIsNone(account['provider_input_tokens'])

    def test_prescribed_probe_cannot_be_counted_as_model_evidence(self):
        w = self.module()
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'prepared'
            w.prepare(out)
            probe = w.offline_probe(out)
            self.assertEqual(probe['genuine_runs'], 0)
            self.assertEqual(probe['genuine_scores'], 0)
            self.assertIn('not-agent', probe['kind'])
            self.assertEqual(set(probe['arms']), set(w.ARMS))
            self.assertGreater(probe['arms']['D']['accounting']['retrieved_bytes'], 0)
            self.assertEqual(probe['arms']['A']['accounting']['retrieved_bytes'], 0)
            self.assertEqual(probe['arms']['D']['accounting']['read_attempts'], len(probe['arms']['D']['reads']))
            self.assertTrue(all(x['evaluator_relevance'] is None for x in probe['arms']['D']['reads']))

    def test_cli_refuses_explicit_missing_preparation_and_output_overwrite(self):
        from unittest.mock import patch
        import contextlib
        import io
        w = self.module()
        with tempfile.TemporaryDirectory() as tmp:
            with patch('sys.argv', ['workflow.py', 'verify', '--prepared', str(Path(tmp) / 'missing')]):
                with contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit) as raised:
                        w.main()
                self.assertEqual(raised.exception.code, 1)
            output = Path(tmp) / 'report.json'
            for iteration in range(2):
                with patch('sys.argv', ['workflow.py', 'report', '--output', str(output)]):
                    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                        if iteration == 0:
                            w.main()
                        else:
                            with self.assertRaises(SystemExit):
                                w.main()
            self.assertEqual(w.load(output)['genuine_runs'], 0)

if __name__ == '__main__':
    unittest.main()
