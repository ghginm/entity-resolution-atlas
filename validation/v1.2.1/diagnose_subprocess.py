#!/usr/bin/env python3
"""Diagnose legacy synthetic subprocess timing; never model/ER outcomes.

Run with the same QA interpreter as the protected test. No legacy bytes edited.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--repetitions', type=int, default=5)
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location('legacy_timing_diagnostic', ROOT / 'validation/agent-utility/harness.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    base = ROOT / 'validation/agent-utility'
    results = []
    with tempfile.TemporaryDirectory(prefix='atlas-timing-', dir=os.environ['TMPDIR']) as tmp:
        corpus = Path(tmp) / 'corpus'
        module.prepare(base / 'corpora/v1/files', corpus, 'v1.1')
        for deadline in (0.5, 2.0):
            for repetition in range(args.repetitions):
                settings = module.load(base / 'settings.json')
                settings['budgets']['timeout_seconds'] = deadline
                start = time.monotonic()
                result = module.run_scenario(corpus, 'AU-01', settings,
                                            [sys.executable, str(base / 'tests/fixture_adapter.py'), 'ok'])
                results.append({'deadline_seconds': deadline, 'repetition': repetition,
                                'elapsed_seconds': round(time.monotonic() - start, 6),
                                'status': result['status'], 'error': result['error'],
                                'read_attempts': result['read_attempts'], 'successful_reads': len(result['reads']),
                                'adapter_exit_code': result['adapter_exit_code']})
    report = {'kind': 'synthetic-legacy-subprocess-diagnostic-not-model-results',
              'python': sys.version, 'executable': sys.executable, 'trials': results,
              'harness_sha256': hashlib.sha256((base / 'harness.py').read_bytes()).hexdigest(),
              'test_sha256': hashlib.sha256((base / 'tests/test_harness.py').read_bytes()).hexdigest(),
              'fixture_sha256': hashlib.sha256((base / 'tests/fixture_adapter.py').read_bytes()).hexdigest(),
              'protected_files_modified': False,
              'limits': ['Elapsed includes freeze/corpus/setup overhead, not merely child startup.',
                         'Passing bounded trials cannot exclude scheduler-dependent flakiness.',
                         'Two seconds is a diagnostic comparator only; protected 0.5-second assertion remains unchanged.']}
    with args.output.open('x') as output:
        json.dump(report, output, indent=2)
        output.write('\n')
    print(json.dumps({'trials': len(results), 'failed': sum(r['status'] != 'completed' for r in results),
                      'max_elapsed_seconds': max(r['elapsed_seconds'] for r in results)}, indent=2))


if __name__ == '__main__':
    main()
