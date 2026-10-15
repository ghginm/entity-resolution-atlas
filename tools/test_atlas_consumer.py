"""Consumer acceptance: real builds, not synthetic ER utility results."""
import json
from pathlib import Path
import tempfile
import unittest
import shutil

ROOT = Path(__file__).resolve().parents[1]


class ConsumerTests(unittest.TestCase):
    def test_frozen_consumer_one_remains_internally_verifiable(self):
        import atlas_consumer as consumer
        self.assertEqual(consumer.verify(ROOT / 'dist/atlas-consumer')['cards'], 57)

    def test_support_sources_are_consumer_ready_without_rewriting(self):
        import atlas_consumer as consumer
        files, manifest = consumer.source_payload(ROOT)
        self.assertEqual(manifest['transformations'], {})
        for name, raw in files.items():
            if name != 'README.md':
                self.assertEqual(raw, (ROOT / name).read_bytes(), name)
            if name.endswith('.md'):
                for forbidden in ('source repository only', 'MAINTAINERS.md',
                                  'validation/', 'tools/atlas_docs.py', 'dev_docs/'):
                    self.assertNotIn(forbidden, raw.decode(), name)

    def test_excluded_maintainer_link_cannot_be_hidden_by_policy(self):
        import atlas_consumer as consumer
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'source'
            files, _ = consumer.source_payload(ROOT)
            for name, raw in files.items():
                target = source / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(raw)
            policy = json.loads((ROOT / 'tools/consumer-policy.json').read_text())
            policy['unbundled_link_targets'] = ['MAINTAINERS.md']
            (source / 'tools').mkdir()
            (source / 'tools/consumer-policy.json').write_text(json.dumps(policy))
            scope = source / 'SCOPE.md'
            scope.write_text(scope.read_text() + '\n[Maintenance](MAINTAINERS.md)\n')
            with self.assertRaisesRegex(ValueError, 'fix canonical source'):
                consumer.source_payload(source)

    def test_archive_cannot_write_into_package_or_source_including_aliases(self):
        import atlas_consumer as consumer
        with tempfile.TemporaryDirectory() as tmp:
            output, source = Path(tmp) / 'package', Path(tmp) / 'source'
            source.mkdir()
            original = source / 'card.md'
            original.write_bytes(b'original source')
            consumer.build(ROOT, output)
            entry = (output / 'START_HERE.md').read_bytes()
            with self.assertRaises(ValueError):
                consumer.archive(output, output / 'START_HERE.md')
            self.assertEqual((output / 'START_HERE.md').read_bytes(), entry)
            with self.assertRaises(ValueError):
                consumer.archive(output, original, source)
            self.assertEqual(original.read_bytes(), b'original source')
            alias = Path(tmp) / 'alias'
            alias.symlink_to(source, target_is_directory=True)
            with self.assertRaises(ValueError):
                consumer.archive(output, alias / 'card.md', source)
            self.assertEqual(original.read_bytes(), b'original source')
            consumer.verify(output, ROOT)

    def test_real_build_is_complete_link_valid_and_byte_deterministic(self):
        import atlas_consumer as consumer
        with tempfile.TemporaryDirectory() as tmp:
            a, b = Path(tmp) / 'a', Path(tmp) / 'b'
            first, second = consumer.build(ROOT, a), consumer.build(ROOT, b)
            self.assertEqual(first, second)
            self.assertEqual(consumer.verify(a, ROOT)['cards'], 57)
            self.assertEqual((a / 'README.md').read_bytes(), (b / 'README.md').read_bytes())
            self.assertIn('START_HERE.md', (a / 'README.md').read_text())
            source = json.loads((ROOT / 'references/atlas-manifest.json').read_text())
            for ident, path in source['cards'].items():
                self.assertEqual((a / path).read_bytes(), (ROOT / path).read_bytes(), ident)
            self.assertFalse((a / 'validation').exists())
            self.assertFalse((a / 'MAINTAINERS.md').exists())
            self.assertFalse((a / 'dev_docs').exists())
            self.assertEqual(consumer.archive(a, Path(tmp) / 'a.tar.gz'),
                             consumer.archive(b, Path(tmp) / 'b.tar.gz'))

    def test_verification_rejects_extra_missing_changed_and_symlink_files(self):
        import atlas_consumer as consumer
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / 'consumer'
            consumer.build(ROOT, output)
            extra = output / 'validation/evaluator-key.json'
            extra.parent.mkdir()
            extra.write_text('{}')
            with self.assertRaisesRegex(ValueError, 'inventory mismatch'):
                consumer.verify(output, ROOT)
            extra.unlink()
            path = output / 'START_HERE.md'
            original = path.read_bytes()
            path.unlink()
            with self.assertRaisesRegex(ValueError, 'inventory mismatch'):
                consumer.verify(output, ROOT)
            path.write_bytes(original + b'changed')
            with self.assertRaisesRegex(ValueError, 'hash mismatch'):
                consumer.verify(output, ROOT)
            path.unlink()
            path.symlink_to(ROOT / 'START_HERE.md')
            with self.assertRaisesRegex(ValueError, 'symlink'):
                consumer.verify(output, ROOT)

    def test_changed_canonical_title_regenerates_navigation_without_manual_copy(self):
        import atlas_consumer as consumer
        import atlas_docs
        with tempfile.TemporaryDirectory() as tmp:
            source, output = Path(tmp) / 'source', Path(tmp) / 'package'
            files, _ = consumer.source_payload(ROOT)
            for name in files:
                if name == 'README.md':
                    continue
                target = source / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / name, target)
            (source / 'tools').mkdir()
            shutil.copyfile(ROOT / 'tools/consumer-policy.json', source / 'tools/consumer-policy.json')
            card = source / 'solutions/decision-resolution/connected-components.md'
            card.write_text(card.read_text().replace('title: Connected components of accepted identity links',
                                                    'title: Updated canonical title'))
            atlas_docs.generate_indexes(source)
            consumer.build(source, output)
            self.assertIn('Updated canonical title', (output / 'indexes/tasks/graph.md').read_text())
            self.assertEqual((output / card.relative_to(source)).read_bytes(), card.read_bytes())


if __name__ == '__main__':
    unittest.main()
