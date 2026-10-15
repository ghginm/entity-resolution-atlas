"""Offline read accounting is not a model-usage or quality benchmark."""
import unittest


class RetrievalCostTests(unittest.TestCase):
    def test_fenced_headings_do_not_start_or_end_real_sections(self):
        import atlas_retrieval_cost as cost
        for fence in ('```md', '~~~md', '````md'):
            close = fence.rstrip('md')
            data = (f'{fence}\n## First\nFake first\n{close}\n'
                    f'## First\nBefore\n{fence}\n## Example\ninside\n{close}\nAfter\n## Next\n').encode()
            chunk, offset = cost.section(data, 'First')
            self.assertIn(b'After\n', chunk)
            self.assertIn(b'## Example', chunk)
            self.assertTrue(chunk.startswith(b'## First\nBefore'))
            self.assertEqual(offset, 5)

    def test_section_preserves_exact_original_bytes(self):
        import atlas_retrieval_cost as cost
        data = b'# Title\r\n\r\n## First\r\nOne.\r\n### Child\r\nTwo.\r\n## Next\r\nNo.\r\n'
        chunk, offset = cost.section(data, 'First')
        self.assertEqual(chunk, b'## First\r\nOne.\r\n### Child\r\nTwo.\r\n')
        self.assertEqual(offset, 3)
        with self.assertRaises(ValueError):
            cost.section(data, 'Absent')


if __name__ == '__main__':
    unittest.main()
