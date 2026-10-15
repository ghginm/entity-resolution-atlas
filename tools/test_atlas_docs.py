"""Tests for documentation checking, never ER examples or fabricated results."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

import atlas_docs


class ParsingTests(unittest.TestCase):
    def test_frontmatter_mapping(self):
        data, body = atlas_docs.frontmatter('---\nid: "SOL-07-001"\ndomain: "07"\n---\n# Body\n')
        self.assertEqual(data['domain'], '07')
        self.assertEqual(body, '# Body\n')

    def test_missing_frontmatter(self):
        with self.assertRaises(ValueError):
            atlas_docs.frontmatter('# No metadata\n')

    def test_duplicate_key_rejected(self):
        with self.assertRaisesRegex(ValueError, 'duplicate YAML key'):
            atlas_docs.frontmatter('---\nid: first\nid: second\n---\nBody\n')

    def test_scalar_frontmatter_rejected(self):
        with self.assertRaises(ValueError):
            atlas_docs.frontmatter('---\nhello\n---\nBody\n')

    def test_heading_ids_handle_duplicates_and_fences(self):
        self.assertEqual(atlas_docs.heading_ids('# A title\n## A title\n```md\n# Not a heading\n```\n'), {'a-title', 'a-title-1'})

    def test_citations_exclude_numeric_navigation(self):
        self.assertEqual(atlas_docs.citation_ids('[08](domain.md) Claim.[1][2]'), {1, 2})


class RepositoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='atlas-docs-test-')
        self.root = Path(self.tmp.name)
        (self.root/'docs').mkdir()
        self.path = self.root/'docs/start.md'
        self.path.write_text('# Start\n')
        self.target = self.root/'docs/target.md'
        self.target.write_text('# Real heading\n')

    def tearDown(self):
        self.tmp.cleanup()

    def test_relative_link_and_anchor(self):
        self.assertEqual(atlas_docs.validate_links(self.path,'[x](target.md#real-heading)',self.root),[])

    def test_broken_path(self):
        errors = atlas_docs.validate_links(self.path,'[x](absent.md)',self.root)
        self.assertIn('broken path', errors[0])

    def test_broken_anchor(self):
        errors = atlas_docs.validate_links(self.path,'[x](target.md#not-present)',self.root)
        self.assertIn('broken anchor',errors[0])

    def test_external_and_code_examples_ignored(self):
        text='[x](https://example.invalid/thing)\n```md\n[x](absent.md)\n```\n'
        self.assertEqual(atlas_docs.validate_links(self.path,text,self.root),[])

    def test_escape_rejected(self):
        errors=atlas_docs.validate_links(self.path,'[x](../../outside.md)',self.root)
        self.assertIn('escapes repository',errors[0])

    def fixture(self):
        for directory in ('decisions','solutions','evaluation','references','dev_docs'):
            (self.root/directory).mkdir(exist_ok=True)
        source=self.root/'dev_docs/original.txt'
        source.write_bytes(b'Original\r\n')
        (self.root/'references/dev-docs-sha256.json').write_text(json.dumps({'dev_docs/original.txt':hashlib.sha256(source.read_bytes()).hexdigest()}))
        (self.root/'references/retrieval-status.json').write_text(json.dumps({'verified_full_text':[1],'verified_metadata_only':[],'verified_publisher_abstract':[],'unverified_unused':[2]}))
        (self.root/'references/source-ledger.json').write_text(json.dumps({'sources':[{'id':1,'url':'https://example.invalid/verified'},{'id':2,'url':'https://example.invalid/unverified'}]}))
        (self.root/'SCHEMA.md').write_text('`interpretable`\n')
        cards=[
            ('decisions/question.md','DEC-07-001','decision','07',{'complements':['SOL-07-001'],'evaluated_by':['EVAL-11-001']}),
            ('solutions/method.md','SOL-07-001','solution','07',{'addresses':['DEC-07-001'],'evaluated_by':['EVAL-11-001']}),
            ('evaluation/measure.md','EVAL-11-001','evaluation','11',{'tests':['SOL-07-001'],'complements':['DEC-07-001']}),
        ]
        for name,ident,typ,domain,relations in cards:
            data={'id':ident,'type':typ,'title':'QA fixture','domain':domain,'summary':' '.join(['discovery']*60),'tags':['interpretable'],'maturity':'established','evidence':'theoretically-motivated','relations':relations}
            fm='\n'.join(f'{k}: {json.dumps(v)}' for k,v in data.items())
            sections = ''.join(f'\n## {heading}\n\nStructural fixture content.\n' for heading in atlas_docs.SECTION_ALIASES[typ])
            (self.root/name).write_text('---\n'+fm+'\n---\n# QA fixture\n\n'+' '.join(['content']*410)+'\n'+sections)
        atlas_docs.generate_indexes(self.root)

    def test_valid_nonpilot_fixture(self):
        self.fixture()
        self.assertEqual(atlas_docs.lint(self.root,pilot=False)['errors'],[])

    def test_missing_evaluation_route_rejected_even_when_connected(self):
        self.fixture()
        path = self.root/'solutions/method.md'
        data, body = atlas_docs.frontmatter(path.read_text())
        data['relations']['requires'] = data['relations'].pop('evaluated_by')
        fm = '\n'.join(f'{k}: {json.dumps(v)}' for k, v in data.items())
        path.write_text('---\n'+fm+'\n---\n'+body)
        atlas_docs.generate_indexes(self.root)
        errors = atlas_docs.lint(self.root, pilot=False)['errors']
        self.assertEqual(errors, ['SOL-07-001: missing explicit evaluated_by route'])

    def test_numeric_navigation_does_not_need_sources(self):
        self.fixture()
        path=self.root/'solutions/method.md'
        path.write_text(path.read_text()+'\n[08](../docs/target.md)\n')
        self.assertEqual(atlas_docs.lint(self.root,pilot=False)['errors'],[])

    def test_changed_input_rejected(self):
        self.fixture()
        (self.root/'dev_docs/original.txt').write_bytes(b'Changed\n')
        self.assertTrue(any('immutable input' in error for error in atlas_docs.lint(self.root,pilot=False)['errors']))

    def test_invalid_relation_rejected(self):
        self.fixture()
        path=self.root/'solutions/method.md'
        path.write_text(path.read_text().replace('DEC-07-001','DEC-07-099'))
        self.assertTrue(any('unresolved relation' in error for error in atlas_docs.lint(self.root,pilot=False)['errors']))

    def test_unverified_citation_rejected(self):
        self.fixture()
        path=self.root/'solutions/method.md'
        path.write_text(path.read_text()+'\nUnsupported.[2]\n\n## Sources\n[2] URL\n')
        self.assertTrue(any('unverified/unknown source' in error for error in atlas_docs.lint(self.root,pilot=False)['errors']))

    def test_citation_block_mismatch_rejected(self):
        self.fixture()
        path=self.root/'solutions/method.md'
        path.write_text(path.read_text()+'\nClaim.[1]\n\n## Sources\n[2] URL\n')
        self.assertTrue(any('cited/source-block IDs differ' in error for error in atlas_docs.lint(self.root,pilot=False)['errors']))

    def test_duplicate_id_rejected(self):
        self.fixture()
        original=self.root/'solutions/method.md'
        (self.root/'solutions/copy.md').write_text(original.read_text())
        self.assertTrue(any('duplicate ID' in error for error in atlas_docs.lint(self.root,pilot=False)['errors']))

    def test_redundant_reciprocal_metadata_rejected(self):
        self.fixture()
        path=self.root/'solutions/method.md'
        data, body=atlas_docs.frontmatter(path.read_text())
        data['relations']['complements']=['DEC-07-001']
        fm='\n'.join(f'{k}: {json.dumps(v)}' for k,v in data.items())
        path.write_text('---\n'+fm+'\n---\n'+body)
        self.assertTrue(any('redundant reciprocal' in error for error in atlas_docs.lint(self.root,pilot=False)['errors']))

    def test_compact_catalog_and_domain_summaries(self):
        self.fixture()
        text = atlas_docs.catalog_text(self.root)
        self.assertIn('Concise applicability', text)
        self.assertIn('Tag entry points', text)
        self.assertNotIn('discovery ' * 40, text)
        outputs = atlas_docs.index_texts(self.root)
        self.assertIn('indexes/domains/07.md', outputs)
        self.assertIn('discovery ' * 40, outputs['indexes/domains/07.md'])
        self.assertIn('Alternatives and differences', outputs['indexes/domains/07.md'])
        self.assertEqual(outputs, atlas_docs.index_texts(self.root))

    def test_tag_routes_are_domain_bounded_in_l0(self):
        self.fixture()
        text = atlas_docs.catalog_text(self.root)
        tag_table = text.split('## Tag entry points', 1)[1]
        self.assertIn('indexes/domains/07.md#tag-interpretable', tag_table)
        self.assertNotIn('SOL-07-001', tag_table)
        self.assertIn('## Tag interpretable', atlas_docs.index_texts(self.root)['indexes/domains/07.md'])

    def test_applicability_first_sentence_override_and_cap(self):
        self.assertEqual(atlas_docs.compact_applicability({'summary': 'First sentence. Second sentence.'}), 'First sentence.')
        self.assertLessEqual(len(atlas_docs.compact_applicability({'summary': 'word ' * 80})), 180)
        self.assertEqual(atlas_docs.compact_applicability({'summary': 'Summary.', 'applicability': 'Use for sparse names.'}), 'Use for sparse names.')
        self.assertTrue(atlas_docs.metadata_errors({'applicability': 'x' * 181}))

    def test_keyword_hints_are_warning_only(self):
        self.fixture()
        result = atlas_docs.lint(self.root, pilot=False)
        self.assertEqual(result['errors'], [])
        self.assertTrue(any('keyword hint' in warning for warning in result['warnings']))

    def test_no_pilot_still_checks_catalog_freshness(self):
        self.fixture()
        (self.root/'CATALOG.md').write_text('Outdated catalog\n')
        self.assertTrue(any('CATALOG.md: stale' in e for e in atlas_docs.lint(self.root, pilot=False)['errors']))

    def test_no_pilot_still_requires_domain_indexes(self):
        self.fixture()
        (self.root/'indexes/domains/07.md').unlink()
        self.assertTrue(any('indexes/domains/07.md: missing' in e for e in atlas_docs.lint(self.root, pilot=False)['errors']))

    def test_tag_edit_stales_both_retrieval_levels(self):
        self.fixture()
        (self.root/'SCHEMA.md').write_text('`interpretable` `few-labels`\n')
        self.edit_card('solutions/method.md', tags=['few-labels'])
        errors = atlas_docs.lint(self.root, pilot=False)['errors']
        self.assertTrue(any('CATALOG.md: stale' in e for e in errors))
        self.assertTrue(any('indexes/domains/07.md: stale' in e for e in errors))

    def edit_card(self, name, **changes):
        path = self.root/name
        data, body = atlas_docs.frontmatter(path.read_text())
        data.update(changes)
        path.write_text('---\n' + '\n'.join(f'{k}: {json.dumps(v)}' for k, v in data.items()) + '\n---\n' + body)

    def test_missing_required_sections_rejected_even_without_pilot(self):
        self.fixture()
        path = self.root/'solutions/method.md'
        data, body = atlas_docs.frontmatter(path.read_text())
        import re
        path.write_text(path.read_text().replace(body, re.sub(r'^## .*\n', '', body, flags=re.M)))
        self.assertTrue(any('required section' in e for e in atlas_docs.lint(self.root, pilot=False)['errors']))

    def test_depth_checks_warn_instead_of_claiming_semantic_proof(self):
        self.fixture()
        self.edit_card('solutions/method.md', summary='Brief discovery summary.')
        path = self.root/'solutions/method.md'
        path.write_text(path.read_text().replace('content '*409 + 'content', 'content'))
        atlas_docs.generate_indexes(self.root)
        result = atlas_docs.lint(self.root, pilot=False)
        self.assertEqual(result['errors'], [])
        self.assertTrue(any('body' in w for w in result['warnings']))
        self.assertTrue(any('summary' in w for w in result['warnings']))

    def test_malformed_metadata_is_a_diagnostic_not_a_crash(self):
        self.fixture()
        path = self.root/'solutions/method.md'
        original = path.read_text()
        for changes in ({'id': []}, {'type': {}}, {'maturity': []}, {'evidence': {}},
                        {'title': None}, {'summary': []}, {'tags': [{}]},
                        {'relations': {'addresses': [{}]}}, {'applicability': 7}):
            with self.subTest(changes=changes):
                path.write_text(original)
                self.edit_card('solutions/method.md', **changes)
                self.assertTrue(atlas_docs.lint(self.root, pilot=False)['errors'])

    def test_orphan_card_is_reported(self):
        self.fixture()
        original = self.root/'solutions/method.md'
        orphan = self.root/'solutions/orphan.md'
        orphan.write_text(original.read_text().replace('SOL-07-001', 'SOL-07-099'))
        self.edit_card('solutions/orphan.md', relations={})
        self.assertTrue(any('orphan' in e for e in atlas_docs.lint(self.root, pilot=False)['errors']))

    def test_wrong_target_types_and_source_directions(self):
        self.fixture()
        original = (self.root/'solutions/method.md').read_text()
        for relations, expected in (
            ({'addresses': ['EVAL-11-001'], 'complements': ['DEC-07-001']}, 'wrong addresses target'),
            ({'tests': ['SOL-07-001'], 'complements': ['DEC-07-001']}, 'tests must originate'),
        ):
            with self.subTest(relations=relations):
                (self.root/'solutions/method.md').write_text(original)
                self.edit_card('solutions/method.md', relations=relations)
                self.assertTrue(any(expected in e for e in atlas_docs.lint(self.root, pilot=False)['errors']))

    def test_requires_cycle_reported(self):
        self.fixture()
        self.edit_card('solutions/method.md', relations={'requires': ['DEC-07-001'], 'evaluated_by': ['EVAL-11-001']})
        self.edit_card('decisions/question.md', relations={'requires': ['SOL-07-001'], 'evaluated_by': ['EVAL-11-001']})
        self.assertTrue(any('requires cycle' in e for e in atlas_docs.lint(self.root, pilot=False)['errors']))

    def test_original_manifest_card_required_as_subset(self):
        self.fixture()
        (self.root/'references/pilot-manifest.json').write_text(json.dumps({'SOL-07-099': 'solutions/missing.md'}))
        self.assertTrue(any('missing original card SOL-07-099' in e for e in atlas_docs.lint(self.root, pilot=False)['errors']))

    def test_expansion_manifest_counts_and_paths(self):
        self.fixture()
        objects = atlas_docs.cards(self.root)
        manifest = {'version': '1.1', 'counts': {'decision': 1, 'solution': 1, 'evaluation': 1, 'architecture': 0, 'hypothesis': 0},
                    'cards': {d['id']: p.relative_to(self.root).as_posix() for p, d, _ in objects}}
        path = self.root/'references/atlas-manifest.json'
        path.write_text(json.dumps(manifest))
        result = atlas_docs.lint(self.root)
        self.assertFalse(any('atlas manifest' in e for e in result['errors']))
        manifest['counts']['solution'] = 2
        path.write_text(json.dumps(manifest))
        self.assertTrue(any('atlas manifest counts mismatch' in e for e in atlas_docs.lint(self.root)['errors']))

    def test_malformed_yaml_has_path_diagnostic(self):
        self.fixture()
        (self.root/'solutions/method.md').write_text('---\nid: [unterminated\n---\nBody\n')
        result = atlas_docs.lint(self.root, pilot=False)
        self.assertTrue(any('solutions/method.md' in e for e in result['errors']))

    def test_generator_rejects_invalid_domain_before_writing(self):
        self.fixture()
        self.edit_card('solutions/method.md', domain='../../../outside')
        with self.assertRaisesRegex(ValueError, 'domain'):
            atlas_docs.generate_indexes(self.root)

    def test_each_card_type_requires_nonempty_template_sections(self):
        for typ, sections in atlas_docs.SECTION_ALIASES.items():
            with self.subTest(typ=typ):
                good = ''.join(f'## {name}\nContent.\n' for name in sections)
                self.assertEqual(atlas_docs.section_errors(self.root, typ, good), [])
                self.assertTrue(atlas_docs.section_errors(self.root, typ, '# Missing sections\n'))
                self.assertTrue(atlas_docs.section_errors(self.root, typ, ''.join(f'## {name}\n' for name in sections)))

    def test_all_pilot_combined_headings_remain_valid(self):
        original = atlas_docs.load_json(atlas_docs.ROOT, 'references/pilot-manifest.json')
        selected = [item for item in atlas_docs.cards(atlas_docs.ROOT) if item[1]['id'] in original]
        self.assertEqual(len(selected), len(original))
        for path, data, body in selected:
            with self.subTest(card=data['id']):
                self.assertEqual(atlas_docs.section_errors(atlas_docs.ROOT, data['type'], body), [])

    def test_alternatives_are_bidirectionally_discovered_not_duplicated(self):
        self.fixture()
        path = self.root/'solutions/other.md'
        path.write_text((self.root/'solutions/method.md').read_text().replace('SOL-07-001', 'SOL-07-002'))
        self.edit_card('solutions/method.md', relations={'alternative_to': ['SOL-07-002'], 'addresses': ['DEC-07-001']})
        text = atlas_docs.index_texts(self.root)['indexes/domains/07.md']
        first = text.split('## SOL-07-001 —', 1)[1].split('## SOL-07-002 —', 1)[0]
        second = text.split('## SOL-07-002 —', 1)[1].split('## Tag', 1)[0]
        self.assertIn('Declared alternatives: [SOL-07-002', first)
        self.assertIn('Declared alternatives: [SOL-07-001', second)

    def test_catalog_generation_and_lint_cli_in_scratch(self):
        self.fixture()
        import subprocess
        import sys
        tool = Path(atlas_docs.__file__)
        for action in ('catalog', 'lint'):
            command = [sys.executable, str(tool), action, '--root', str(self.root), '--no-pilot']
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)['errors'], [])

    def test_no_pilot_does_not_accept_metadata_names_as_tags(self):
        self.fixture()
        (self.root/'SCHEMA.md').write_text('Metadata `summary`.\n## Controlled applicability tags\n- `interpretable`.\n## Other conventions\n`title`.\n')
        self.edit_card('solutions/method.md', tags=['summary'])
        self.assertTrue(any('unknown or malformed tags' in e for e in atlas_docs.lint(self.root, pilot=False)['errors']))

    def test_generator_rejects_duplicate_ids(self):
        self.fixture()
        (self.root/'solutions/duplicate.md').write_text((self.root/'solutions/method.md').read_text())
        with self.assertRaisesRegex(ValueError, 'duplicate ID'):
            atlas_docs.generate_indexes(self.root)

    def test_duplicate_applicability_tags_are_rejected(self):
        self.fixture()
        self.edit_card('solutions/method.md', tags=['interpretable', 'interpretable'])
        errors = atlas_docs.lint(self.root, pilot=False)['errors']
        self.assertTrue(any('duplicate applicability tags' in error for error in errors))

    def test_identical_discovery_summaries_warn_not_fail(self):
        self.fixture()
        self.edit_card('solutions/method.md', summary='  '.join(['discovery'] * 60))
        atlas_docs.generate_indexes(self.root)
        result = atlas_docs.lint(self.root, pilot=False)
        self.assertEqual(result['errors'], [])
        duplicates = [w for w in result['warnings'] if 'identical discovery summaries' in w]
        self.assertEqual(len(duplicates), 1)
        self.assertIn('DEC-07-001', duplicates[0])
        self.assertIn('SOL-07-001', duplicates[0])

    def test_catalog_routes_tasks_only_when_guide_exists(self):
        self.fixture()
        route = '[task patterns](guides/agent-task-patterns.md)'
        self.assertNotIn(route, atlas_docs.catalog_text(self.root))
        guide = self.root/'guides/agent-task-patterns.md'
        guide.parent.mkdir()
        guide.write_text('# Agent task patterns\n')
        self.assertIn(route, atlas_docs.catalog_text(self.root))
        atlas_docs.generate_indexes(self.root)
        self.assertEqual(atlas_docs.lint(self.root, pilot=False)['errors'], [])

    def test_manifest_wrong_path_is_reported(self):
        self.fixture()
        objects = atlas_docs.cards(self.root)
        from collections import Counter
        counts = Counter(d['type'] for p, d, b in objects)
        by_id = {d['id']: (p, d) for p, d, b in objects}
        manifest = {'version': '1.1', 'counts': {t: counts[t] for t in atlas_docs.TYPES},
                    'cards': {i: p.relative_to(self.root).as_posix() for i, (p, d) in by_id.items()}}
        manifest['cards']['SOL-07-001'] = 'solutions/wrong.md'
        (self.root/'references/atlas-manifest.json').write_text(json.dumps(manifest))
        self.assertTrue(any('SOL-07-001: path differs from atlas manifest' in e for e in atlas_docs.manifest_checks(self.root, by_id, counts, True)))

    def test_malformed_reference_metadata_is_graceful(self):
        self.fixture()
        for name in ('dev-docs-sha256.json', 'atlas-manifest.json', 'pilot-manifest.json'):
            with self.subTest(name=name):
                path = self.root/'references'/name
                original = path.read_text() if path.exists() else None
                path.write_text('[]')
                try:
                    self.assertTrue(atlas_docs.lint(self.root)['errors'])
                finally:
                    if original is None:
                        path.unlink()
                    else:
                        path.write_text(original)

    def test_frozen_utility_corpora_are_not_live_navigation(self):
        self.fixture()
        snapshot = self.root/'validation/agent-utility/corpora/v1/files/references/snapshot.md'
        snapshot.parent.mkdir(parents=True)
        snapshot.write_text('[Archived route](not-packaged.md)\n')
        self.assertEqual(atlas_docs.lint(self.root, pilot=False)['errors'], [])
        live = self.root/'validation/agent-utility/protocol.md'
        live.write_text('[Bad live route](not-present.md)\n')
        self.assertTrue(any('protocol.md: broken path' in e for e in atlas_docs.lint(self.root, pilot=False)['errors']))


if __name__ == '__main__':
    unittest.main()
