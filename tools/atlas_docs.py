#!/usr/bin/env python3
"""Catalog and lint the Markdown Atlas; no entity-resolution functionality."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]
CARD_DIRS = ('decisions', 'solutions', 'architectures', 'research/hypotheses', 'evaluation')
TYPES = {'decision': 'DEC', 'solution': 'SOL', 'architecture': 'AR', 'hypothesis': 'HYP', 'evaluation': 'EVAL'}
RELATIONS = {'addresses', 'alternative_to', 'complements', 'requires', 'conflicts_with', 'used_by', 'tests', 'evaluated_by'}
PILOT_MAPPING_SHA256 = '9120657bdade911ecb346f9084e5fa7ec306a64a14744241678758c7b2f5ca9f'
MATURITIES = {'established', 'context-dependent', 'experimental', 'speculative'}
EVIDENCE = {'theoretically-motivated', 'supported-by-external-literature', 'empirically-validated-in-specific-context', 'unknown-or-insufficient'}
ID_RE = re.compile(r'\b(?:AR-\d{2}|(?:DEC|SOL|HYP|EVAL)-\d{2}-\d{3})\b')
LINK_RE = re.compile(r'\[[^\]\n]+\]\(([^)\n]+)\)')

# Template headings plus structural aliases for the existing combined headings.
# Aliases recognize layout only; they do not prove that the prose is adequate.
SECTION_ALIASES = {
    'decision': {
        'Decision question': r'decision question',
        'Problem context': r'(problem )?context',
        'Relevant assumptions': r'assumptions',
        'Available solution families': r'(available )?alternatives|solution families',
        'Criteria for choosing': r'criteria|selection|choice',
        'Trade-off comparison': r'trade.off',
        'Good baseline candidates': r'baseline',
        'Prerequisites': r'prerequisites',
        'Open questions': r'open questions',
        'Related evaluations': r'evaluation',
        'Links to Solution Cards': r'solution (links|families)',
    },
    'solution': {
        'Short summary': r'summary',
        'Problem addressed': r'problem addressed',
        'Core mechanism': r'core mechanism',
        'Theoretical explanation': r'theoretical explanation',
        'Important variants': r'variants',
        'Assumptions and prerequisites': r'assumptions|prerequisites',
        'Applicability conditions': r'applicability|variants and prerequisites',
        'Advantages': r'advantages',
        'Trade-offs and failure modes': r'trade.off.*failure',
        'Relationships with other methods': r'relationships',
        'How to evaluate': r'evaluat',
        'Research opportunities': r'research opportunities',
        'References and evidence limitations': r'evidence (limit|limitation)|references|^sources$',
    },
    'architecture': {
        'Design philosophy': r'philosophy',
        'Architecture dimensions and pipeline topology': r'(four )?dimensions',
        'Conceptual pipeline': r'pipeline',
        'Required and optional components': r'components|pipeline and modules',
        'Conceptual module contracts': r'contracts',
        'Compatible alternatives': r'alternatives',
        'Composition rationale': r'rationale|pipeline and modules',
        'Preconditions and labeling assumptions': r'assumptions',
        'Advantages and failure modes': r'failures|failure modes',
        'Computational and operational considerations': r'costs|trade.offs',
        'Important component interactions': r'interactions',
        'Evaluation strategy': r'evaluation',
        'Variations and alternative configurations': r'alternatives',
        'Research directions': r'research',
        'References and evidence limitations': r'references|evidence limit|^sources$',
    },
    'hypothesis': {
        'Research question': r'question',
        'Explicit hypothesis': r'hypothesis',
        'Theoretical mechanism': r'mechanism',
        'Assumptions': r'assumptions|mechanism and scope',
        'Expected potential benefit': r'mechanism',
        'Reasons the hypothesis could fail': r'falsification|guardrails|mechanism and scope',
        'Proposed experiment': r'experiment|proposed test',
        'Baseline and controlled variables': r'baseline',
        'Required data': r'required data|supervision',
        'Primary metrics and guardrails': r'metrics',
        'Potential confounders': r'confounders|controlled variables',
        'Falsification criteria': r'falsification|decision rule',
        'Follow-up after positive and negative outcomes': r'falsification|decision rule',
        'Related solutions and references': r'references|^sources$',
    },
    'evaluation': {
        'What is measured': r'measurement|output contract|scope and estimand',
        'Why it matters': r'contract|scope and estimand',
        'Definitions and formulas': r'definitions|metrics|diagnostics',
        'Data requirements': r'data|reference requirements',
        'Sampling assumptions': r'sampling|data design',
        'Interpretation': r'interpretation|diagnostics|discrimination',
        'Potential biases': r'failure analysis|diagnostics|data design',
        'Known limitations': r'failure analysis|limitations|data design',
        'Recommended comparisons': r'comparisons',
        'Statistical uncertainty': r'uncertainty',
        'Related solutions and references': r'references|^sources$',
    },
}


KEYWORD_HINTS = {
    'decision': {'baseline/comparator': r'baseline|compar', 'assumptions/prerequisites': r'assum|prerequis'},
    'solution': {'mechanism': r'mechanism|operat|comput|estim', 'failure/limitations': r'fail|limit|risk'},
    'architecture': {'composition/contracts': r'compos|contract|module', 'failure/limitations': r'fail|limit|risk'},
    'hypothesis': {'falsification': r'falsif|reject|disconfirm', 'baseline/control': r'baseline|control'},
    'evaluation': {'sampling': r'sampl|population|inclusion', 'uncertainty': r'uncertain|variance|bootstrap|interval'},
}


def section_errors(root, typ, body):
    template = root / f'templates/{typ}.md'
    required = (re.findall(r'^##\s+(.+)$', template.read_text(encoding='utf-8'), re.M)
                if template.exists() else list(SECTION_ALIASES[typ]))
    sections = re.split(r'^##\s+(.+)\s*$', prose_without_fences(body), flags=re.M)
    headings = [(sections[i].strip(), sections[i+1].strip()) for i in range(1, len(sections), 2)]
    errors = []
    for name in required:
        alias = SECTION_ALIASES[typ].get(name)
        matching = [content for heading, content in headings
                    if heading.casefold() == name.casefold() or (alias and re.search(alias, heading, re.I))]
        if not matching:
            errors.append(f'missing required section: {name}')
        elif not any(matching):
            errors.append(f'empty required section: {name}')
    return errors


def metadata_errors(data):
    required = {'id', 'type', 'title', 'domain', 'summary', 'tags', 'maturity', 'evidence', 'relations'}
    missing = required - data.keys()
    errors = [f'missing fields {sorted(missing)}'] if missing else []
    for field in sorted(required - {'tags', 'relations'}):
        if field in data and (not isinstance(data[field], str) or not data[field].strip()):
            errors.append(f'{field} must be a nonempty string')
    if isinstance(data.get('domain'), str) and not re.fullmatch(r'0[1-9]|1[0-4]', data['domain']):
        errors.append('domain must be quoted 01–14')
    typ = data.get('type')
    if isinstance(typ, str) and typ not in TYPES:
        errors.append(f'unknown type {typ}')
    if isinstance(data.get('id'), str) and isinstance(typ, str) and typ in TYPES:
        pattern = r'AR-\d{2}' if typ == 'architecture' else rf'{TYPES[typ]}-{re.escape(str(data.get("domain")))}-\d{{3}}'
        if not re.fullmatch(pattern, data['id']):
            errors.append('ID does not match type/domain')
        if typ == 'architecture' and data.get('domain') != '02':
            errors.append('invalid architecture ID/domain')
    for field, permitted in (('maturity', MATURITIES), ('evidence', EVIDENCE)):
        if isinstance(data.get(field), str) and data[field] not in permitted:
            errors.append(f'invalid {field}')
    if 'tags' in data and (not isinstance(data['tags'], list) or any(not isinstance(t, str) or not t for t in data['tags'])):
        errors.append('tags must be a list of nonempty strings')
    elif isinstance(data.get('tags'), list) and len(set(data['tags'])) != len(data['tags']):
        errors.append('duplicate applicability tags')
    if 'relations' in data:
        if not isinstance(data['relations'], dict):
            errors.append('relations must be mapping')
        else:
            for relation, targets in data['relations'].items():
                if not isinstance(relation, str) or not isinstance(targets, list) or any(not isinstance(t, str) for t in targets):
                    errors.append(f'invalid relation payload: {relation}')
    for field in ('applicability',):
        if field in data and (not isinstance(data[field], str) or not data[field].strip()):
            errors.append(f'{field} must be a nonempty string')
    if isinstance(data.get('applicability'), str) and (len(data['applicability']) > 180 or '\n' in data['applicability']):
        errors.append('applicability must be one line of at most 180 characters')
    return errors


class UniqueLoader(yaml.SafeLoader):
    """Reject repeated YAML keys rather than silently accepting the last one."""


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError(f'duplicate YAML key: {key}')
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def frontmatter(text):
    match = re.match(r'\A---\r?\n(.*?)\r?\n---\r?\n(.*)\Z', text, re.S)
    if not match:
        raise ValueError('missing YAML frontmatter')
    data = yaml.load(match.group(1), Loader=UniqueLoader)
    if not isinstance(data, dict):
        raise ValueError('frontmatter must be a mapping')
    return data, match.group(2)


def prose_line_mask(text):
    """Classify Markdown lines outside backtick/tilde fences, retaining positions."""
    fence = None
    mask = []
    for line in text.splitlines(keepends=True):
        match = re.match(r'^ {0,3}(`{3,}|~{3,})([^\r\n]*)[\r\n]*$', line)
        if fence is not None:
            mask.append(False)
            if match and match[1][0] == fence[0] and len(match[1]) >= len(fence) and not match[2].strip():
                fence = None
        elif match and (match[1][0] != '`' or '`' not in match[2]):
            mask.append(False)
            fence = match[1]
        else:
            mask.append(True)
    return mask


def prose_without_fences(text):
    return ''.join(line if prose else '\n' for line, prose in zip(text.splitlines(keepends=True), prose_line_mask(text)))


def section_range(text, heading):
    lines = text.splitlines(keepends=True)
    mask = prose_line_mask(text)
    start = next((i for i, line in enumerate(lines) if mask[i] and line.rstrip('\r\n') == '## ' + heading), None)
    if start is None:
        raise ValueError(f'missing section: {heading}')
    end = next((i for i in range(start + 1, len(lines)) if mask[i] and lines[i].startswith('## ')), len(lines))
    return start, end


def citation_ids(text):
    """Numeric inline navigation labels are links, not source citations."""
    return set(map(int, re.findall(r'\[(\d+)\](?!\s*\()', text)))


def heading_ids(text):
    slugs = set()
    counts = Counter()
    for title in re.findall(r'^#{1,6}\s+(.+?)\s*#*\s*$', prose_without_fences(text), re.M):
        title = re.sub(r'\[([^]]+)\]\([^)]+\)', r'\1', title)
        slug = re.sub(r'[^\w\- ]', '', title.lower(), flags=re.UNICODE).replace(' ', '-')
        suffix = counts[slug]
        counts[slug] += 1
        slugs.add(slug if suffix == 0 else f'{slug}-{suffix}')
    slugs.update(re.findall(r'<a\s+(?:id|name)=["\']([^"\']+)', text))
    return slugs


def reference_link_errors(text):
    if re.search(r'^ {0,3}\[[^\]\n]+\]:', prose_without_fences(text), re.M):
        return ['unsupported reference-style link definition; use explicit inline Markdown links']
    return []


def validate_links(path, text, root):
    errors = reference_link_errors(text)
    for dest in LINK_RE.findall(prose_without_fences(text)):
        dest = dest.strip().split(' "', 1)[0].strip('<>')
        parsed = urlsplit(dest)
        if parsed.scheme or parsed.netloc:
            continue
        target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path.resolve()
        if not target.is_relative_to(root.resolve()):
            errors.append(f'link escapes repository: {dest}')
        elif not target.exists():
            errors.append(f'broken path: {dest}')
        elif parsed.fragment and target.suffix == '.md':
            if unquote(parsed.fragment) not in heading_ids(target.read_text(encoding='utf-8')):
                errors.append(f'broken anchor: {dest}')
    return errors


def cards(root, errors=None):
    output = []
    for directory in CARD_DIRS:
        for path in sorted((root / directory).rglob('*.md')):
            try:
                data, body = frontmatter(path.read_text(encoding='utf-8'))
            except (ValueError, TypeError, yaml.YAMLError, OSError) as exc:
                message = f'{path.relative_to(root).as_posix()}: {exc}'
                if errors is None:
                    raise ValueError(message) from exc
                errors.append(message)
                continue
            output.append((path, data, body))
    return output


def domain_registry(root, objects):
    """Minimal non-pilot fixtures may infer domains without extra fixture files."""
    path = root / 'taxonomy/domain-registry.json'
    if not path.exists():
        return {d['domain']: {'title': f'Domain {d["domain"]}'} for _, d, _ in objects}
    domains = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(domains, dict) or any(
        not isinstance(key, str) or not re.fullmatch(r'0[1-9]|1[0-4]', key)
        or not isinstance(info, dict) or not isinstance(info.get('title'), str)
        or not isinstance(info.get('path'), str)
        for key, info in domains.items()
    ):
        raise ValueError('malformed domain registry')
    return domains


def compact_applicability(data):
    """Use the first summary sentence; an explicit applicability is optional."""
    value = data.get('applicability', data['summary'])
    if not isinstance(value, str) or not value.strip():
        raise ValueError('applicability must be a nonempty string')
    value = ' '.join(value.split())
    if 'applicability' not in data:
        value = re.split(r'(?<=[.!?])\s+', value, maxsplit=1)[0]
    if len(value) > 180:
        value = value[:177].rsplit(' ', 1)[0].rstrip('.,;:') + '…'
    return value


def table_cell(text):
    return ' '.join(text.split()).replace('|', '\\|')


def index_texts(root):
    """Return all deterministic L0/L1 outputs without writing the corpus."""
    objects = cards(root)
    for path, data, _ in objects:
        problems = metadata_errors(data)
        if problems:
            raise ValueError(f'{path.relative_to(root)}: {"; ".join(problems)}')
    objects.sort(key=lambda item: item[1]['id'])
    domains = domain_registry(root, objects)
    by_id = {d['id']: (p, d) for p, d, _ in objects}
    if len(by_id) != len(objects):
        raise ValueError('duplicate ID in cards; refusing to generate ambiguous indexes')
    if any(d['domain'] not in domains for _, d, _ in objects):
        raise ValueError('card domain absent from registry')
    alternatives = {ident: set() for ident in by_id}
    for ident, (_, data) in by_id.items():
        for target in data['relations'].get('alternative_to', []):
            if target not in by_id:
                raise ValueError(f'{ident}: unresolved alternative_to target {target}')
            alternatives[ident].add(target)
            alternatives[target].add(ident)
    counts = Counter(d['type'] for _, d, _ in objects)
    lines = ['# Knowledge catalog', '',
             'L0: find an ID or tag, then retrieve its domain L1 index and canonical card. Tags and summaries are discovery clues, not recommendations or compatibility guarantees.', '']
    if (root / 'guides/agent-task-patterns.md').is_file():
        lines += ['Starting from a project question? Use the relevant section of [task patterns](guides/agent-task-patterns.md), then return to selected cards; do not read every pattern or domain.', '']
    lines += [f'**{len(objects)} knowledge objects:** ' + ', '.join(f'{counts[t]} {t}' for t in TYPES) + '.', '',
             '## Objects', '',
             '| ID | Title | Type | Domain | Concise applicability | Canonical path |',
             '|---|---|---|---|---|---|']
    for path, data, _ in objects:
        canonical = path.relative_to(root).as_posix()
        lines.append(f'| [{data["id"]}]({canonical}) | {table_cell(data["title"])} | {data["type"]} | {data["domain"]} | {table_cell(compact_applicability(data))} | `{canonical}` |')
    lines += ['', '## Domain L1 indexes', '']
    for domain, info in sorted(domains.items()):
        lines.append(f'- [{domain} — {info["title"]}](indexes/domains/{domain}.md)')
    lines += ['', '## Tag entry points', '', '| Tag | Domain routes to matching objects |', '|---|---|']
    for tag in sorted({tag for _, data, _ in objects for tag in data['tags']}):
        matching_domains = sorted({d['domain'] for _, d, _ in objects if tag in d['tags']})
        matches = ', '.join(f'[{domain}](indexes/domains/{domain}.md#tag-{tag})' for domain in matching_domains)
        lines.append(f'| `{tag}` | {matches} |')
    lines += ['', 'Navigation derived from canonical card metadata; applicability still requires reading the selected cards.', '']
    outputs = {'CATALOG.md': '\n'.join(lines)}
    for domain, info in sorted(domains.items()):
        outpath = root / f'indexes/domains/{domain}.md'
        def relative(path):
            return Path(os.path.relpath(path, outpath.parent)).as_posix()
        def card_link(ident, fragment='', short=False):
            path, data = by_id[ident]
            label = ident if short else f'{ident} — {data["title"]}'
            return f'[{label}]({relative(path)}{fragment})'
        lines = [f'# {domain} — {info["title"]}', '', '[L0 catalog](../../CATALOG.md)', '']
        if 'path' in info:
            lines += [f'[Domain map]({relative(root / info["path"])})', '']
        selected = [(p, d, b) for p, d, b in objects if d['domain'] == domain]
        if not selected:
            lines += ['Taxonomy coverage only; no standalone cards in this domain. This is a coverage gap, not a recommendation.', '']
        for path, data, body in selected:
            lines += [f'## {data["id"]} — {data["title"]}', '',
                      f'{data["type"]} · domain {domain} · {card_link(data["id"])}', '',
                      ' '.join(data['summary'].split()), '',
                      'Tags: ' + ', '.join(f'`{tag}`' for tag in sorted(data['tags'])) + '.', '',
                      '**Alternatives and differences**', '']
            related = [card_link(other_id, short=True) for other_id in sorted(alternatives[data['id']] - {data['id']})]
            lines += ['Declared alternatives: ' + (', '.join(related) if related else 'none in metadata; do not infer substitutability from shared tags') + '.', '']
            headings = re.findall(r'^##\s+(.+)$', prose_without_fences(body), re.M)
            refs = [heading for heading in headings if re.search(r'alternativ|variant|trade.off|comparison|criteria|relationship|composition|interaction|baseline', heading, re.I)]
            if refs:
                lines += ['Read differences and conditions in: ' + ', '.join(
                    f'[{heading}]({relative(path)}#{next(iter(heading_ids("## " + heading)))})' for heading in refs) + '.', '']
            else:
                lines += ['Read the canonical card for differences and conditions; metadata alone is insufficient.', '']
            for relation, targets in sorted(data['relations'].items()):
                if relation != 'alternative_to' and targets:
                    lines += [f'{relation}: ' + ', '.join(card_link(target, short=True) for target in sorted(targets)) + '.', '']
        for tag in sorted({tag for _, d, _ in selected for tag in d['tags']}):
            lines += [f'## Tag {tag}', '', ', '.join(card_link(d['id'], short=True) for _, d, _ in selected if tag in d['tags']) + '.', '']
        lines += ['Generated from card summaries, tags, typed relations and section links. No compatibility or performance conclusion is generated.', '']
        outputs[f'indexes/domains/{domain}.md'] = '\n'.join(lines)
    from atlas_routes import route_texts
    outputs.update(route_texts(root, objects))
    return outputs


def catalog_text(root):
    return index_texts(root)['CATALOG.md']


def generate_indexes(root):
    outputs = index_texts(root)
    for name, text in outputs.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')
    return sorted(outputs)


def graph_checks(by_id):
    """Check topology only, never infer semantic compatibility from edges."""
    errors, warnings = [], []
    neighbors = {ident: set() for ident in by_id}
    requires = {ident: set() for ident in by_id}
    for ident, (_, data) in by_id.items():
        for relation, targets in data['relations'].items():
            if relation not in RELATIONS:
                continue
            for target in targets:
                if target in by_id and target != ident:
                    neighbors[ident].add(target)
                    neighbors[target].add(ident)
                    if relation == 'requires':
                        requires[ident].add(target)
    for ident, targets in sorted(neighbors.items()):
        if not targets:
            errors.append(f'{ident}: orphan card; no resolved typed connections')
    remaining, components = set(neighbors), []
    while remaining:
        pending, component = [min(remaining)], set()
        while pending:
            ident = pending.pop()
            if ident not in component:
                component.add(ident)
                pending.extend(sorted(neighbors[ident] - component))
        components.append(sorted(component))
        remaining -= component
    if len(components) > 1:
        warnings.append(f'typed relation graph has {len(components)} disconnected components; review retrieval reachability: {components}')
    # Kahn elimination: prerequisites left over imply a cycle or its dependants.
    remaining = set(requires)
    while remaining:
        ready = {ident for ident in remaining if not requires[ident] & remaining}
        if not ready:
            errors.append(f'requires cycle in prerequisite graph: {sorted(remaining)}')
            break
        remaining -= ready
    return errors, warnings, {'components': components, 'orphans': sorted(i for i, n in neighbors.items() if not n)}


def load_json(root, name):
    try:
        value = json.loads((root/name).read_text(encoding='utf-8'))
        if not isinstance(value, dict):
            raise ValueError('metadata JSON must be an object')
        return value
    except (OSError, ValueError) as exc:
        raise ValueError(f'{name}: {exc}') from exc


def manifest_checks(root, by_id, counts, pilot):
    errors = []
    baseline = root/'references/pilot-manifest.json'
    if baseline.exists():
        original = load_json(root, 'references/pilot-manifest.json')
        if not isinstance(original, dict) or any(not isinstance(i, str) or not isinstance(p, str) for i, p in original.items()):
            errors.append('malformed historical pilot manifest')
        else:
            digest = hashlib.sha256(json.dumps(original, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
            if pilot and digest != PILOT_MAPPING_SHA256:
                errors.append('historical pilot manifest mapping changed')
            for ident, expected_path in sorted(original.items()):
                if ident not in by_id:
                    errors.append(f'missing original card {ident}: {expected_path}')
                elif by_id[ident][0].relative_to(root).as_posix() != expected_path:
                    errors.append(f'{ident}: path differs from original pilot manifest')
    elif pilot:
        errors.append('historical pilot manifest missing')
    if not pilot:
        return errors
    path = root/'references/atlas-manifest.json'
    if not path.exists():
        errors.append('atlas manifest missing: references/atlas-manifest.json')
        return errors
    manifest = load_json(root, 'references/atlas-manifest.json')
    if not isinstance(manifest, dict) or not isinstance(manifest.get('version'), str) or not manifest['version'].strip():
        return errors + ['malformed atlas manifest version']
    expected_counts, mapping = manifest.get('counts'), manifest.get('cards')
    if not isinstance(expected_counts, dict) or set(expected_counts) != set(TYPES) or any(type(n) is not int or n < 0 for n in expected_counts.values()):
        errors.append('malformed atlas manifest counts; explicitly supply all five types')
    elif {typ: counts[typ] for typ in TYPES} != expected_counts:
        errors.append(f'atlas manifest counts mismatch: {dict(counts)} expected {expected_counts}')
    if not isinstance(mapping, dict) or any(not isinstance(i, str) or not isinstance(p, str) for i, p in mapping.items()):
        errors.append('malformed atlas manifest cards mapping')
    else:
        if set(mapping) != set(by_id):
            errors.append(f'atlas manifest IDs differ: missing {sorted(set(mapping)-set(by_id))}; unexpected {sorted(set(by_id)-set(mapping))}')
        for ident, expected_path in sorted(mapping.items()):
            if ident in by_id and by_id[ident][0].relative_to(root).as_posix() != expected_path:
                errors.append(f'{ident}: path differs from atlas manifest')
    if {i for i, (_, d) in by_id.items() if d['type'] == 'architecture'} != {f'AR-{n:02d}' for n in range(1, 7)}:
        errors.append('architecture inventory must preserve exactly AR-01 through AR-06')
    return errors


def lint(root, pilot=True):
    """Report malformed inputs as diagnostics, including minimal legacy fixtures."""
    try:
        return _lint(root, pilot)
    except (OSError, ValueError, TypeError, KeyError, yaml.YAMLError) as exc:
        return {'errors': [f'cannot lint repository: {exc}'], 'warnings': [], 'counts': {}}


def _lint(root, pilot=True):
    errors, warnings = [], []
    try:
        objects = cards(root, errors)
    except (ValueError, TypeError, yaml.YAMLError, OSError) as exc:
        return {'errors': [str(exc)], 'warnings': [], 'counts': {}}
    by_id = {}
    schema_text = (root / 'SCHEMA.md').read_text()
    tag_section = re.search(r'^## Controlled applicability tags\s*\n(.*?)(?=^## |\Z)', schema_text, re.M | re.S)
    allowed_tags = set(re.findall(r'`([a-z][a-z0-9-]+)`', tag_section.group(1) if tag_section else schema_text))
    bodies = {path: body for path, _, body in objects}
    stats = []
    summary_owners = {}
    for path, data, body in objects:
        rel = path.relative_to(root).as_posix()
        problems = metadata_errors(data)
        if problems:
            errors.extend(f'{rel}: {problem}' for problem in problems)
            continue
        ident = data['id']
        if ident in by_id:
            errors.append(f'{rel}: duplicate ID {ident}')
        by_id[ident] = (path, data)
        summary_key = ' '.join(data['summary'].casefold().split())
        summary_owners.setdefault(summary_key, []).append(ident)
        typ, domain = data['type'], data['domain']
        if typ != 'evaluation' and not data['relations'].get('evaluated_by'):
            errors.append(f'{ident}: missing explicit evaluated_by route')
        if any(t not in allowed_tags for t in data['tags']):
            errors.append(f'{rel}: unknown or malformed tags {data["tags"]}')
        words = len(data['summary'].split())
        if not 50 <= words <= 100:
            warnings.append(f'{rel}: discovery summary {words} words (target 50–100)')
        words = len(re.findall(r'\S+', body.split('\n## Sources', 1)[0]))
        if words < 400:
            warnings.append(f'{rel}: substantive body only {words} words (target 400–900); inspect depth')
        elif words > 900:
            warnings.append(f'{rel}: body {words} words; consider justified deep dive')
        if typ in TYPES:
            errors.extend(f'{rel}: {problem}' for problem in section_errors(root, typ, body))
            prose = re.sub(r'^#{1,6}[^\n]*$', '', prose_without_fences(body), flags=re.M)
            for concept, pattern in KEYWORD_HINTS[typ].items():
                if not re.search(pattern, prose, re.I):
                    warnings.append(f'{rel}: keyword hint missing for {concept}; inspect manually, not a semantic verdict')
        stats.append({'id':ident,'path':rel,'body_words':words})
    for owners in summary_owners.values():
        if len(owners) > 1:
            warnings.append('identical discovery summaries: ' + ', '.join(sorted(owners)) + '; inspect duplication, not a semantic verdict')
    for ident, (path, data) in by_id.items():
        if not isinstance(data.get('relations'), dict):
            continue
        count = 0
        for relation, targets in data['relations'].items():
            if relation not in RELATIONS or not isinstance(targets, list):
                errors.append(f'{ident}: invalid relation {relation}')
                continue
            count += len(set(targets))
            if len(set(targets)) != len(targets):
                errors.append(f'{ident}: duplicate targets in {relation}')
            if relation == 'tests' and data['type'] not in {'hypothesis', 'evaluation'}:
                errors.append(f'{ident}: tests must originate in hypothesis/evaluation')
            if relation == 'evaluated_by' and data['type'] == 'evaluation':
                errors.append(f'{ident}: evaluated_by must originate in decision/solution/architecture/hypothesis')
            for target in targets:
                if target not in by_id:
                    errors.append(f'{ident}: unresolved relation {relation} → {target}')
                    continue
                target_type = by_id[target][1]['type']
                expected = {'addresses':'decision','used_by':'architecture','evaluated_by':'evaluation'}.get(relation)
                if expected and target_type != expected:
                    errors.append(f'{ident}: wrong {relation} target type {target}')
                if relation == 'addresses' and data['type'] != 'solution':
                    errors.append(f'{ident}: addresses must originate in solution')
                if relation == 'used_by' and data['type'] == 'architecture':
                    errors.append(f'{ident}: used_by direction reversed')
                if relation == 'tests' and target_type not in {'solution','architecture'}:
                    errors.append(f'{ident}: tests target must be solution/architecture')
                if target == ident:
                    errors.append(f'{ident}: self relation')
        body = bodies[path]
        exception = re.search(r'^>?\s*Relation exception:\s*\S.+$', body, re.M | re.I)
        if count < 2 and not exception:
            errors.append(f'{ident}: fewer than two typed outbound relationships')
    for ident, (_, data) in by_id.items():
        if not isinstance(data.get('relations'), dict):
            continue
        for relation in ('complements', 'alternative_to', 'conflicts_with'):
            targets = data['relations'].get(relation, [])
            if not isinstance(targets, list):
                continue
            for target in targets:
                if target not in by_id or not isinstance(by_id[target][1].get('relations'), dict):
                    continue
                reverse = by_id[target][1]['relations'].get(relation, [])
                if isinstance(reverse, list) and ident in reverse and ident < target:
                    errors.append(f'{ident}: redundant reciprocal {relation} with {target}')
    graph_errors, graph_warnings, graph = graph_checks(by_id)
    errors.extend(graph_errors)
    warnings.extend(graph_warnings)
    status = load_json(root, 'references/retrieval-status.json')
    allowed_sources = set(status['verified_full_text'] + status['verified_metadata_only'] + status['verified_publisher_abstract'])
    ledger = load_json(root, 'references/source-ledger.json')
    known_sources = {s['id'] for s in ledger['sources']}
    for path in sorted(root.rglob('*.md')):
        rel = path.relative_to(root).as_posix()
        # Harness allowlisted snapshots retain historical links to files that
        # intentionally are not packaged. They are not the live Atlas graph.
        if '.git' in path.parts or rel.startswith('validation/agent-utility/corpora/'):
            continue
        text = path.read_text(encoding='utf-8')
        for error in validate_links(path, text, root):
            errors.append(f'{rel}: {error}')
        if rel.startswith('templates/'):
            continue
        for ident in set(ID_RE.findall(prose_without_fences(text))):
            if ident not in by_id:
                errors.append(f'{rel}: unresolved prose ID {ident}')
        parts = re.split(r'^## Sources\s*$', text, maxsplit=1, flags=re.M)
        prose_ids = citation_ids(parts[0])
        for source in prose_ids:
            if source not in known_sources or source not in allowed_sources:
                errors.append(f'{rel}: unverified/unknown source [{source}]')
        if prose_ids and len(parts) != 2:
            errors.append(f'{rel}: citations but no rendered Sources block')
        if len(parts) == 2:
            rendered_ids = set(map(int, re.findall(r'^\[(\d+)\]', parts[1], re.M)))
            if prose_ids != rendered_ids and rel != 'references/bibliography.md':
                errors.append(f'{rel}: cited/source-block IDs differ {sorted(prose_ids)} vs {sorted(rendered_ids)}')
    hashes = load_json(root, 'references/dev-docs-sha256.json')
    for name, expected_hash in hashes.items():
        path = root / name
        if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != expected_hash:
            errors.append(f'{name}: immutable input missing or changed')
    actual_inputs = {p.relative_to(root).as_posix() for p in (root/'dev_docs').iterdir() if p.is_file()}
    if actual_inputs != set(hashes):
        errors.append('immutable input inventory differs from original baseline')
    counts = Counter(data['type'] for _, data, _ in objects if isinstance(data.get('type'), str))
    errors.extend(manifest_checks(root, by_id, counts, pilot))
    if pilot:
        domains = domain_registry(root, objects)
        if set(domains) != {f'{i:02d}' for i in range(1,15)}:
            errors.append('domain registry does not represent exactly 01–14')
        for domain in domains.values():
            if 'path' not in domain:
                errors.append('domain registry missing; inferred domains are for non-pilot fixtures only')
            elif not (root/domain['path']).exists():
                errors.append(f'missing domain summary {domain["path"]}')
        templates = {p.stem for p in (root/'templates').glob('*.md')}
        if templates != set(TYPES):
            errors.append('five card templates missing or unexpected')
    try:
        expected_indexes = index_texts(root)
        for name, expected_text in expected_indexes.items():
            path = root / name
            if not path.exists():
                errors.append(f'{name}: missing generated index')
            elif path.read_text(encoding='utf-8') != expected_text:
                errors.append(f'{name}: stale; regenerate from frontmatter')
        extras = {p.relative_to(root).as_posix() for p in (root/'indexes/domains').glob('*.md')} - set(expected_indexes)
        for name in sorted(extras):
            errors.append(f'{name}: unexpected generated domain index')
    except (ValueError, KeyError, TypeError, OSError) as exc:
        errors.append(f'cannot check index freshness: {exc}')
    return {'errors':errors,'warnings':warnings,'counts':dict(counts),'immutable_inputs':len(hashes),'card_statistics':stats,'graph':graph}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['catalog','lint'])
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--no-pilot', action='store_true', help='Disable expanded inventory/shape gate only; schema and index freshness still apply')
    args = parser.parse_args()
    if args.action == 'catalog':
        try:
            for name in generate_indexes(args.root):
                print(f'Generated {args.root/name}')
        except (OSError, ValueError, TypeError, KeyError, yaml.YAMLError) as exc:
            print(json.dumps({'errors': [f'cannot generate indexes: {exc}']}))
            return 1
        return 0
    result = lint(args.root, pilot=not args.no_pilot)
    print(json.dumps(result,indent=2,ensure_ascii=False))
    return 1 if result['errors'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
