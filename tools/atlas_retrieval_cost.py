#!/usr/bin/env python3
"""Replay declared selective read paths, not inference or recommendation quality."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import tarfile


def section(data, heading):
    from atlas_docs import section_range
    lines = data.splitlines(keepends=True)
    start, end = section_range(data.decode('utf-8'), heading)
    return b''.join(lines[start:end]), start + 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--baseline', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        import tiktoken
        encoder = tiktoken.get_encoding('cl100k_base')
    except ImportError:
        encoder = None
    root = args.root
    routes = json.loads((root / 'guides/task-routes.json').read_text())
    manifest = json.loads((root / 'references/atlas-manifest.json').read_text())
    with tarfile.open(args.baseline) as archive:
        old = {member.name: archive.extractfile(member).read() for member in archive.getmembers() if member.isfile()}
    def read(name, baseline=False):
        return old[name] if baseline else (root / name).read_bytes()
    def record(name, data, offset=1, layer='L0'):
        return {'path': name, 'offset': offset, 'lines': len(data.splitlines()),
                'bytes': len(data), 'words': len(data.decode().split()),
                'tokens': len(encoder.encode(data.decode(), disallowed_special=())) if encoder else None,
                'sha256': hashlib.sha256(data).hexdigest(), 'layer': layer}
    def metrics(events):
        card_paths = set(manifest['cards'].values())
        return {'file_reads': len(events), 'documents': len({e['path'] for e in events}),
                'canonical_cards': len({e['path'] for e in events} & card_paths),
                'retrieved_bytes': sum(e['bytes'] for e in events),
                'retrieved_tokens': sum(e['tokens'] for e in events) if encoder else None,
                'full_corpus_loading_detected': len({e['path'] for e in events} & card_paths) == len(card_paths),
                'events': events}
    tasks = {}
    for name, route in routes.items():
        arms = {}
        for baseline in (True, False):
            events = [record('AGENTS.md', read('AGENTS.md', baseline))]
            if baseline:
                chunk, offset = section(read('guides/agent-task-patterns.md', True), route['heading'])
                events.append(record('guides/agent-task-patterns.md', chunk, offset))
            else:
                events.extend(record(p, read(p)) for p in ('START_HERE.md', f'indexes/tasks/{name}.md'))
            # Identical selected L1 and L2 IDs in both arms; no whole-domain straw man.
            for ident in route['ids']:
                card = manifest['cards'][ident]
                fm = read(card, baseline).decode().split('---', 2)[1]
                import yaml
                meta = yaml.safe_load(fm)
                domain = f'indexes/domains/{meta["domain"]}.md'
                chunk, offset = section(read(domain, baseline), ident + ' — ' + meta['title'])
                events.append(record(domain, chunk, offset, 'L1'))
            for ident in route['ids']:
                path = manifest['cards'][ident]
                events.append(record(path, read(path, baseline), layer='L2'))
            arms['v1.2-selective' if baseline else 'v1.2.1-selective'] = metrics(events)
        a, b = arms.values()
        tasks[name] = {'arms': arms, 'reading_token_reduction_pct':
                       round(100 * (a['retrieved_tokens'] - b['retrieved_tokens']) / a['retrieved_tokens'], 2) if encoder else None}
    catalog = ['AGENTS.md', 'README.md', 'CATALOG.md', 'guides/agent-task-patterns.md', 'guides/project-atlas-integration.md']
    catalog += [f'indexes/domains/{i:02d}.md' for i in range(1, 15)]
    audit = {p: {'before': record(p, read(p, True)), 'after': record(p, read(p))} for p in catalog}
    result = {'kind': 'offline-declared-read-replay', 'not_model_usage': True, 'quality_measured': False,
              'tokenizer': 'tiktoken cl100k_base' if encoder else 'none; bytes/words are proxies',
              'limitations': ['Declared read paths, not autonomous agent decisions or measured model input usage.',
                             'Tokens cover returned UTF-8 content only; exclude prompts, tool wrappers, replay, reasoning, output and billing.',
                             'Identical L2 seed sets isolate navigation cost; sufficiency still requires project-specific review.',
                             'Read requests are not latency or sequential hop measurements; no execution cost claim.'],
              'baseline_archive_sha256': hashlib.sha256(args.baseline.read_bytes()).hexdigest(),
              'tasks': tasks, 'navigation_audit': audit,
              'canonical_corpus': {'cards': len(manifest['cards']), 'bytes': sum((root / p).stat().st_size for p in manifest['cards'].values())}}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: {'before_tokens': v['arms']['v1.2-selective']['retrieved_tokens'], 'after_tokens': v['arms']['v1.2.1-selective']['retrieved_tokens'],
                          'reduction_pct': v['reading_token_reduction_pct']} for k, v in tasks.items()}, indent=2))


if __name__ == '__main__':
    main()
