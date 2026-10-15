"""Generate bounded views of existing task patterns; no search runtime or ontology."""
import json
import os
from pathlib import Path
import re
from urllib.parse import urlsplit


def route_texts(root, objects):
    from atlas_docs import heading_ids, reference_link_errors, section_range
    config = root / 'guides/task-routes.json'
    if not config.exists():
        return {}
    routes = json.loads(config.read_text(encoding='utf-8'))
    guide = root / 'guides/agent-task-patterns.md'
    text = guide.read_text(encoding='utf-8')
    if reference_link_errors(text):
        raise ValueError('unsupported reference-style links in task patterns; use inline links')
    by_id = {data['id']: (path, data) for path, data, _ in objects}
    outputs = {}
    hub = ['# Task routes', '', 'Choose one route. These are generated views of existing task patterns, not required reading lists.', '',
           '| Problem | Route |', '|---|---|']
    for name, route in routes.items():
        if not re.fullmatch(r'[a-z]+(?:-[a-z]+)*', name):
            raise ValueError(f'invalid route name: {name}')
        heading, ids = route['heading'], route['ids']
        if len(ids) != len(set(ids)) or any(ident not in by_id for ident in ids):
            raise ValueError(f'{name}: duplicate or unresolved canonical ID')
        start, end = section_range(text, heading)
        outpath = root / f'indexes/tasks/{name}.md'
        def relative(path):
            return Path(os.path.relpath(path, outpath.parent)).as_posix()
        def rewrite(link):
            label, dest = link.groups()
            parsed = urlsplit(dest)
            if parsed.scheme or parsed.netloc:
                return link.group(0)
            dest = relative((guide.parent / parsed.path).resolve()) + (f'#{parsed.fragment}' if parsed.fragment else '')
            return f'[{label}]({dest})'
        body = re.sub(r'\[([^]\n]+)\]\(([^)\n]+)\)', rewrite, ''.join(text.splitlines(keepends=True)[start + 1:end]).strip())
        lines = [f'# {heading}', '', body, '', '## Selective next reads', '',
                 'Open the decision first; select only needed solutions and evaluation. The seed set is not exhaustive. Read named L1 sections, not the whole domain; skip L1 when the decision already resolves the comparison.', '']
        for ident in ids:
            path, data = by_id[ident]
            # Use the same heading convention as the domain index.
            slug = next(iter(heading_ids(f'## {ident} — {data["title"]}')))
            lines.append(f'- [{ident} — {data["title"]}]({relative(path)}) · [L1 section](../domains/{data["domain"]}.md#{slug})')
        lines += ['', 'Stop when the decision, baseline, alternatives, prerequisites/failures, evaluation and important unknowns are covered. Expand only for an unresolved constraint; links are not a reading queue.', '',
                  'Generated from `guides/agent-task-patterns.md`, `guides/task-routes.json` and canonical metadata. Navigation is not evidence of ER accuracy.', '']
        outputs[outpath.relative_to(root).as_posix()] = '\n'.join(lines)
        hub.append(f'| {heading} | [{name}](tasks/{name}.md) |')
    hub += ['', 'For architecture-only questions, read the architecture review section of [task patterns](../guides/agent-task-patterns.md#architecture-review-and-modularity). Otherwise search only a relevant [catalog](../CATALOG.md) portion.', '']
    outputs['indexes/tasks.md'] = '\n'.join(hub)
    return outputs
