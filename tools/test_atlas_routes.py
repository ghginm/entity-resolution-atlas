"""Selective routes are navigation, never measured recommendation quality."""
import json
from pathlib import Path
import unittest
import tempfile

import atlas_docs

ROOT = Path(__file__).resolve().parents[1]


class RouteTests(unittest.TestCase):
    def test_route_anchors_use_shared_heading_slug_for_linked_titles(self):
        from atlas_routes import route_texts
        objects = atlas_docs.cards(ROOT)
        for _, meta, _ in objects:
            if meta['id'] == 'SOL-08-003':
                meta['title'] = 'Connected [components](https://example.org)'
        expected = next(iter(atlas_docs.heading_ids('## SOL-08-003 — Connected [components](https://example.org)')))
        route = route_texts(ROOT, objects)['indexes/tasks/graph.md']
        self.assertIn('08.md#' + expected + ')', route)

    def test_reference_style_links_fail_closed_in_shared_validator_and_routes(self):
        from atlas_routes import route_texts
        for target in ('nonexistent.md', '../../../escape.md', '../validation/private-fixture.md'):
            text = f'[Broken][bad]\n\n[bad]: {target}\n'
            errors = atlas_docs.validate_links(ROOT / 'START_HERE.md', text, ROOT)
            self.assertTrue(any('reference-style' in error for error in errors), target)
            with tempfile.TemporaryDirectory() as tmp:
                source = Path(tmp)
                (source / 'guides').mkdir()
                (source / 'guides/task-routes.json').write_bytes((ROOT / 'guides/task-routes.json').read_bytes())
                (source / 'guides/agent-task-patterns.md').write_text((ROOT / 'guides/agent-task-patterns.md').read_text() + '\n' + text)
                with self.assertRaisesRegex(ValueError, 'reference-style'):
                    route_texts(source, atlas_docs.cards(ROOT))
        self.assertEqual(atlas_docs.validate_links(ROOT / 'START_HERE.md', '```md\n[x][ref]\n[ref]: missing.md\n```\n', ROOT), [])

    def test_graph_route_generated_from_existing_pattern_and_canonical_ids(self):
        outputs = atlas_docs.index_texts(ROOT)
        self.assertIn('indexes/tasks/graph.md', outputs,
                      'Question routes must be generated with L0/L1, not handwritten copies')
        text = outputs['indexes/tasks/graph.md']
        for ident in ('DEC-08-001', 'SOL-08-003', 'SOL-08-004', 'EVAL-11-003'):
            self.assertIn(ident, text)
        self.assertIn('A true chain may have bridges', text)
        self.assertNotIn('SOL-08-005', text)
        self.assertLess(len(text.split()), 450)

    def test_domain_navigation_does_not_repeat_long_titles_in_tag_fanout(self):
        text = atlas_docs.index_texts(ROOT)['indexes/domains/08.md']
        tags = text.split('## Tag ', 1)[1]
        self.assertNotIn('Connected components of accepted identity links', tags)
        self.assertIn('[SOL-08-003]', tags)


if __name__ == '__main__':
    unittest.main()
