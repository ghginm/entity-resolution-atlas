"""Synthetic process probes, NOT an AU-v2 executor or model results.

Only the hardcoded fixture below may be spawned. Reuse the pinned legacy line
reader and AU-v2 state/broker unchanged. No frozen case/key text is loaded here.
The optional evidence directory is operator-only and must use new output paths.
"""
import contextlib
import importlib.util
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location(
    'wave4_bridge', ROOT / 'validation/agent-utility-integration/bridge.py')
assert SPEC is not None and SPEC.loader is not None
bridge = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bridge)

# These bytes are a fixed test program, not generated model output or an adapter.
FIXTURE = r'''
import json, os, sys, time
mode = sys.argv[1]
def emit(value):
    sys.stdout.buffer.write((json.dumps(value, ensure_ascii=False) + '\n').encode())
    sys.stdout.buffer.flush()
def receive():
    raw = sys.stdin.buffer.readline()
    sys.stderr.buffer.write(raw.hex().encode() + b'\n')
    sys.stderr.buffer.flush()
    return json.loads(raw)
start = receive()
ready = dict(type='ready', identity='synthetic-only', settings_sha256='a'*64,
             fresh_context=True, broker_only=True)
request = dict(type='read_file', request_id='r0', path='taxonomy/overview.md.txt',
               offset=0, length=3)
if mode == 'partial':
    sys.stdout.buffer.write(b'{"type":'); sys.stdout.buffer.flush(); sys.exit(0)
if mode == 'stall':
    sys.stdout.buffer.write(b'{"type":'); sys.stdout.buffer.flush(); time.sleep(30)
if mode == 'line_overflow':
    sys.stdout.buffer.write(b'x'*65537 + b'\n'); sys.stdout.buffer.flush(); sys.exit(0)
if mode == 'before_ready':
    emit(request); sys.exit(0)
if mode == 'wrong_identity':
    ready['identity'] = 'different-synthetic-only'
emit(ready)
if mode == 'duplicate_json':
    sys.stdout.buffer.write(b'{"type":"final","type":"final","text":"fixture"}\n')
    sys.stdout.buffer.flush(); sys.exit(0)
if mode == 'over_chunk':
    request['length'] = 8001; emit(request); sys.exit(0)
if mode == 'exchange':
    for i in range(3):
        request['request_id'] = 'r'+str(i)
        if i == 2:
            request['path'] = '../outside'
        emit(request)
        reply = receive()
        if i < 2:
            assert reply['type'] == 'read_result' and reply['text'] == 'ΑБ🙂'
        else:
            assert reply['type'] == 'read_denied' and 'text' not in reply
    sys.stderr.buffer.write(b'\xffsynthetic-stderr\n'); sys.stderr.buffer.flush()
text = 'SYNTHETIC process fixture; not a model recommendation.'
if mode == 'final_overflow':
    text = 'x'*24001
emit(dict(type='final', text=text))
if mode == 'after_final':
    emit(request)
if mode == 'nonzero':
    sys.exit(7)
'''


class RuntimeBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(
            prefix='atlas-wave4-', dir=os.environ['TMPDIR'])
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        source = self.root / 'source'
        (source / 'taxonomy').mkdir(parents=True)
        (source / 'taxonomy/overview.md').write_text('ΑБ🙂 fixture only.\n', encoding='utf-8')
        snapshot = self.root / 'snapshot'
        bridge.prepare_snapshot(source, snapshot, 'expanded-atlas')
        self.broker = bridge.Broker(
            snapshot, bridge.digest((snapshot / 'corpus-manifest.json').read_bytes()))
        self.session = bridge.Session(self.broker, 'synthetic-only', 'a' * 64)
        self.events = []

    @contextlib.contextmanager
    def fixture(self, mode):
        # Test scaffolding only: no arbitrary argv, provider, cohort or dispatch API.
        env = {'PATH': os.defpath, 'HOME': str(self.root), 'TMPDIR': str(self.root),
               'LANG': 'C.UTF-8', 'PYTHONIOENCODING': 'utf-8'}
        process = subprocess.Popen(
            [sys.executable, '-I', '-B', '-c', FIXTURE, mode],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            cwd=self.root, env=env, start_new_session=True)
        assert process.stdin is not None and process.stdout is not None and process.stderr is not None
        reader = bridge.legacy.LineReader(process.stdout, 65536, time.monotonic() + 5)
        try:
            yield process, reader
        finally:
            # Always clean up the fixture's group, including after leader exit.
            # This does NOT contain descendants that create a new session.
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            process.wait(timeout=5)
            reader.close()
            for stream in (process.stdin, process.stdout, process.stderr):
                if stream is not None:
                    stream.close()

    def send(self, process, kind, value):
        raw = bridge.canonical(value)
        process.stdin.write(raw)
        process.stdin.flush()
        self.events.append({'direction': kind, 'raw_hex': raw.hex(),
                            'sha256': bridge.digest(raw), 'observed_at': bridge.legacy.utc_now()})

    def receive(self, reader):
        line = reader.line()
        self.assertIsNotNone(line)
        raw = line + b'\n'
        self.events.append({'direction': 'received', 'raw_hex': raw.hex(),
                            'sha256': bridge.digest(raw), 'observed_at': bridge.legacy.utc_now()})
        return self.session.handle(raw)

    def start(self, process):
        # Deliberately not a genuine frozen start/scenario or an eligible journal.
        self.send(process, 'sent_start', {'type': 'synthetic_start', 'fixture': True})

    def test_real_pipe_exchange_retains_sent_received_and_stderr(self):
        with self.fixture('exchange') as (process, reader):
            self.start(process)
            self.assertIsNone(self.receive(reader))
            for _ in range(3):
                reply = self.receive(reader)
                self.send(process, 'sent_broker', reply)
            self.assertIsNone(self.receive(reader))
            self.assertIsNone(reader.line())
            exit_code = process.wait(timeout=5)
            assert process.stderr is not None
            stderr = process.stderr.read()
            self.assertIn('SYNTHETIC', self.session.finish(exit_code))
            sent = [bytes.fromhex(e['raw_hex']) for e in self.events
                    if e['direction'].startswith('sent_')]
            # Child reports actual received stdin bytes, not merely generated replies.
            self.assertEqual(stderr, b''.join(x.hex().encode() + b'\n' for x in sent)
                             + b'\xffsynthetic-stderr\n')
            self.assertEqual((self.broker.attempts, self.broker.successes, self.broker.chars), (3, 2, 6))
            generated = [e['raw_hex'] for e in self.session.events if e['direction'] == 'broker_generated']
            transmitted = [e['raw_hex'] for e in self.events if e['direction'] == 'sent_broker']
            self.assertEqual(generated, transmitted)
            evidence = os.environ.get('ATLAS_WAVE4_EVIDENCE_DIR')
            if evidence:
                report = {'kind': 'synthetic-pipe-probe-not-run-record', 'actual_model_calls': 0,
                          'eligible_for_scoring': False, 'events': self.events,
                          'stderr_hex': stderr.hex(), 'stderr_sha256': bridge.digest(stderr),
                          'exit_code': exit_code, 'attempts': self.broker.attempts,
                          'successful_reads': self.broker.successes,
                          'returned_characters': self.broker.chars,
                          'fixture_sha256': bridge.digest(FIXTURE.encode()),
                          'limitations': ['Fixed fixture only; not an executor or identity attestation.',
                                          'Synthetic start is intentionally not a frozen AU-v2 start.']}
                with (Path(evidence) / 'synthetic-pipe.json').open('x') as output:
                    json.dump(report, output, indent=2)
                    output.write('\n')

    def test_read_before_ready_is_rejected(self):
        with self.fixture('before_ready') as (process, reader):
            self.start(process)
            with self.assertRaisesRegex(bridge.IntegrationError, 'ready'):
                self.receive(reader)
            self.assertEqual(self.broker.attempts, 0)

    def test_ready_identity_mismatch_is_rejected(self):
        with self.fixture('wrong_identity') as (process, reader):
            self.start(process)
            with self.assertRaisesRegex(bridge.IntegrationError, 'ready'):
                self.receive(reader)

    def test_partial_line_at_eof_is_rejected(self):
        with self.fixture('partial') as (process, reader):
            self.start(process)
            with self.assertRaisesRegex(bridge.legacy.BenchmarkError, 'unterminated'):
                reader.line()

    def test_partial_line_stall_hits_reader_deadline(self):
        with self.fixture('stall') as (process, reader):
            self.start(process)
            reader.deadline = time.monotonic() + 0.2
            with self.assertRaisesRegex(bridge.legacy.BenchmarkError, 'wall timeout'):
                reader.line()

    def test_stdout_line_byte_limit_rejects_real_process_output(self):
        with self.fixture('line_overflow') as (process, reader):
            self.start(process)
            with self.assertRaisesRegex(bridge.legacy.BenchmarkError, 'byte budget'):
                reader.line()

    def test_duplicate_json_keys_from_process_are_rejected(self):
        with self.fixture('duplicate_json') as (process, reader):
            self.start(process)
            self.receive(reader)
            with self.assertRaises(bridge.IntegrationError):
                self.receive(reader)
            self.assertEqual(self.session.state, 'failed')

    def test_chunk_excess_is_failed_not_silently_corrected(self):
        with self.fixture('over_chunk') as (process, reader):
            self.start(process)
            self.receive(reader)
            with self.assertRaisesRegex(bridge.IntegrationError, 'chunk'):
                self.receive(reader)
            self.assertEqual((self.broker.attempts, self.broker.successes), (1, 0))
            self.assertEqual(self.session.state, 'failed')

    def test_final_character_excess_is_rejected(self):
        with self.fixture('final_overflow') as (process, reader):
            self.start(process)
            self.receive(reader)
            with self.assertRaisesRegex(bridge.IntegrationError, 'final'):
                self.receive(reader)

    def test_output_after_final_is_rejected(self):
        with self.fixture('after_final') as (process, reader):
            self.start(process)
            self.receive(reader)
            self.receive(reader)
            with self.assertRaisesRegex(bridge.IntegrationError, 'after final'):
                self.receive(reader)

    def test_nonzero_process_exit_cannot_complete(self):
        with self.fixture('nonzero') as (process, reader):
            self.start(process)
            self.receive(reader)
            self.receive(reader)
            self.assertIsNone(reader.line())
            code = process.wait(timeout=5)
            self.assertEqual(code, 7)
            with self.assertRaisesRegex(bridge.IntegrationError, 'terminal exit'):
                self.session.finish(code)

    @unittest.expectedFailure
    def test_buffered_line_must_not_bypass_expired_deadline(self):
        # AU-v2 reuse requirement: RED diagnostic, not permission to edit legacy.
        # Expected failure is a BLOCKER, not a pass; keep the strict assertion.
        read_fd, write_fd = os.pipe()
        os.close(write_fd)
        with os.fdopen(read_fd, 'rb') as stream:
            reader = bridge.legacy.LineReader(stream, 65536, time.monotonic() - 1)
            self.addCleanup(reader.close)
            reader.buffer = b'{"type":"final","text":"late synthetic"}\n'
            with self.assertRaisesRegex(bridge.legacy.BenchmarkError, 'wall timeout'):
                reader.line()


if __name__ == '__main__':
    unittest.main()
