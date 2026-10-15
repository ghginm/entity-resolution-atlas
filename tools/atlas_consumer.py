#!/usr/bin/env python3
"""Build/verify a deterministic allowlisted Markdown consumer snapshot."""
import argparse
from collections import Counter
import gzip
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import tarfile
from urllib.parse import unquote, urlsplit

import atlas_docs

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = 'consumer-manifest.json'
README = b'''# Entity Resolution Atlas consumer

A project-agnostic, read-only knowledge base for Entity Resolution decisions,
alternatives, trade-offs and evaluation. Start at [START_HERE.md](START_HERE.md).
This package is self-contained for Markdown consumption; tools and scripts are
optional, not prerequisites. Navigation checks do not establish ER accuracy or
agent decision quality.

## Connect an external coding agent

Give Codex, Claude Code, Hermes or another coding agent filesystem access to this
consumer directory (mount or copy it into the agent's accessible workspace).
Replace the placeholder below with its absolute path and paste the instruction
into the target project's agent instructions or task prompt. Automatic discovery
of AGENTS.md is not required.

```text
## External Entity Resolution Knowledge

Atlas entry point: <absolute-path>/atlas-consumer-wave5/START_HERE.md

For Entity Resolution tasks, read that entry point and select the relevant task
route. Retrieve only applicable decision, baseline/alternative solution and
evaluation cards; follow related cards only when needed. Follow START_HERE.md's
retrieval stop rules and project decision-note contract. Cite Atlas card IDs and
paths. Do not scan the entire Atlas.

Use only this consumer directory as read-only reference knowledge, not Atlas
development, validation, benchmark or maintainer artifacts. Project-specific
context is authoritative for project facts; Atlas supplies general methodological
guidance, not project-specific evidence or permission to change production.
```
'''


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe_path(root, name):
    if not isinstance(name, str) or not name or '\\' in name or PurePosixPath(name).is_absolute() or '..' in PurePosixPath(name).parts:
        raise ValueError(f'unsafe package path: {name}')
    path = root / name
    if path.is_symlink() or any(p.is_symlink() for p in path.parents if p != root.parent):
        raise ValueError(f'symlink not allowed: {name}')
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f'escaped package path: {name}')
    return path


def permitted(name):
    parts = PurePosixPath(name).parts
    if not parts or parts[0] not in {'AGENTS.md', 'START_HERE.md', 'SCOPE.md', 'SCHEMA.md', 'README.md',
                                    MANIFEST, 'CATALOG.md', 'decisions', 'solutions', 'architectures',
                                    'evaluation', 'research', 'deep-dives', 'taxonomy', 'indexes', 'guides', 'references'}:
        raise ValueError(f'non-consumer path: {name}')
    if parts[0] == 'research' and not name.startswith('research/hypotheses/'):
        raise ValueError(f'non-consumer research: {name}')


def source_payload(root):
    policy_bytes = (root / 'tools/consumer-policy.json').read_bytes()
    policy = json.loads(policy_bytes)
    manifest = json.loads(safe_path(root, policy['include_canonical_manifest']).read_bytes())
    registry_name = policy['include_domain_registry']
    registry = json.loads(safe_path(root, registry_name).read_bytes())
    generated = atlas_docs.index_texts(root)
    names = set(policy['files']) | set(manifest['cards'].values()) | {registry_name}
    names.update(info['path'] for info in registry.values())
    if policy['include_generated_navigation']:
        names.update(generated)
    card_paths = set(manifest['cards'].values())
    files, transformations = {}, {}
    for name in sorted(names):
        permitted(name)
        path = safe_path(root, name)
        raw = path.read_bytes()
        if path.suffix == '.md' and atlas_docs.reference_link_errors(raw.decode()):
            raise ValueError(f'{name}: unsupported reference-style links; use inline links')
        if name in generated and raw != generated[name].encode():
            raise ValueError(f'stale navigation: {name}; run atlas_docs.py catalog')
        if path.suffix == '.md' and name not in card_paths:
            def replace(match):
                label, dest = match.groups()
                parsed = urlsplit(dest)
                if parsed.scheme or parsed.netloc or not parsed.path:
                    return match.group(0)
                target = (path.parent / unquote(parsed.path)).resolve()
                if not target.is_relative_to(root.resolve()):
                    raise ValueError(f'escaping link: {name}: {dest}')
                relative = target.relative_to(root).as_posix()
                if relative in names or any(n.startswith(relative + '/') for n in names):
                    return match.group(0)
                raise ValueError(f'undeclared unbundled link: {name}: {dest}; fix canonical source')
            # Preserve code fences literally; examples are not live navigation.
            text = raw.decode()
            chunks = re.split(r'(?ms)(^```.*?^```[^\n]*\n?|^~~~.*?^~~~[^\n]*\n?)', text)
            raw = ''.join(chunk if i % 2 else re.sub(r'\[([^]\n]+)\]\(([^)\n]+)\)', replace, chunk)
                          for i, chunk in enumerate(chunks)).encode()

        files[name] = raw
    files['README.md'] = README
    return files, {'format': 'atlas-consumer-v1', 'workflow_version': policy['version'],
                   'knowledge_version': manifest['version'], 'policy_sha256': digest(policy_bytes),
                   'cards': manifest['cards'], 'counts': manifest['counts'],
                   'source_hashes': {n: digest(safe_path(root, n).read_bytes()) for n in sorted(names)},
                   'transformations': transformations}


def verify(output, root=None):
    output = output.resolve()
    data = json.loads(safe_path(output, MANIFEST).read_bytes())
    if data.get('format') != 'atlas-consumer-v1':
        raise ValueError('unknown consumer manifest')
    expected = set(data['files']) | {MANIFEST}
    actual = {p.relative_to(output).as_posix() for p in output.rglob('*') if p.is_file() or p.is_symlink()}
    if actual != expected:
        raise ValueError(f'package inventory mismatch: extra={sorted(actual-expected)}, missing={sorted(expected-actual)}')
    for name, checksum in data['files'].items():
        permitted(name)
        path = safe_path(output, name)
        if digest(path.read_bytes()) != checksum:
            raise ValueError(f'content hash mismatch: {name}')
    source_manifest = json.loads((output / 'references/atlas-manifest.json').read_bytes())
    if data['cards'] != source_manifest['cards'] or data['counts'] != source_manifest['counts']:
        raise ValueError('canonical inventory mismatch')
    by_id, counts = {}, Counter()
    status = json.loads((output / 'references/retrieval-status.json').read_bytes())
    sources = {s['id']: s['url'] for s in json.loads((output / 'references/source-ledger.json').read_bytes())['sources']}
    verified = set(status['verified_full_text'] + status['verified_metadata_only'] + status['verified_publisher_abstract'])
    for ident, name in data['cards'].items():
        raw = safe_path(output, name).read_bytes()
        meta, body = atlas_docs.frontmatter(raw.decode())
        if meta['id'] != ident or ident in by_id or atlas_docs.metadata_errors(meta):
            raise ValueError(f'canonical metadata mismatch: {ident}')
        by_id[ident] = meta
        counts[meta['type']] += 1
        if digest(raw) != data['source_hashes'][name]:
            raise ValueError(f'canonical card changed: {ident}')
    if dict(counts) != data['counts']:
        raise ValueError('type counts mismatch')
    for ident, meta in by_id.items():
        for targets in meta['relations'].values():
            if any(target not in by_id for target in targets):
                raise ValueError(f'unresolved relation: {ident}')
    for name in sorted(data['files']):
        path = output / name
        if path.suffix != '.md':
            continue
        text = path.read_text()
        errors = atlas_docs.validate_links(path, text, output)
        if errors:
            raise ValueError(f'{name}: {errors}')
        parts = re.split(r'^## Sources\s*$', text, maxsplit=1, flags=re.M)
        citations = atlas_docs.citation_ids(parts[0])
        if not citations <= verified & sources.keys():
            raise ValueError(f'{name}: unknown/unverified source')
        if citations and len(parts) != 2:
            raise ValueError(f'{name}: missing Sources block')
        if len(parts) == 2:
            rendered = {int(n): url for n, url in re.findall(r'^\[(\d+)\]\s+(https?://\S+)', parts[1], re.M)}
            if any(sources.get(n) != url for n, url in rendered.items()) or (name != 'references/bibliography.md' and citations != rendered.keys()):
                raise ValueError(f'{name}: source rendering mismatch')
    # Reconcile generated navigation against the payload's canonical metadata.
    for name, text in atlas_docs.index_texts(output).items():
        # Frozen consumer-1 snapshots use the original catalog footer. Preserve
        # their verification without changing frozen bytes or current generation.
        if name == 'CATALOG.md' and data['workflow_version'] == '1.2.1-consumer-1':
            text = text.replace(
                'Navigation derived from canonical card metadata; applicability still requires reading the selected cards.',
                'Generated by `python tools/atlas_docs.py catalog`; edit card metadata, not derived indexes.')
        if (output / name).read_bytes() != text.encode():
            raise ValueError(f'stale packaged navigation: {name}')
    if root is not None:
        payload, meta = source_payload(root)
        if data != dict(meta, files={n: digest(raw) for n, raw in sorted(payload.items())}):
            raise ValueError('package does not match authoritative source/policy')
    return {'cards': len(by_id), 'files': len(expected), 'bytes': sum((output / n).stat().st_size for n in expected),
            'manifest_sha256': digest((output / MANIFEST).read_bytes()), 'source_verified': root is not None}


def build(root, output):
    root, output = root.resolve(), output.absolute()
    if root.is_relative_to(output.resolve()) or (output.resolve().is_relative_to(root) and not output.resolve().is_relative_to(root / 'dist')):
        raise ValueError('output must be dist/ or outside source repository')
    files, manifest = source_payload(root)
    manifest['files'] = {name: digest(raw) for name, raw in sorted(files.items())}
    files[MANIFEST] = (json.dumps(manifest, indent=2, sort_keys=True) + '\n').encode()
    if output.exists():
        verify(output, root)
        return manifest
    output.mkdir(parents=True)
    for name, raw in sorted(files.items()):
        target = safe_path(output, name)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
    verify(output, root)
    return manifest


def check_archive_destination(output, destination, root=ROOT):
    output, destination, root = output.resolve(), destination.absolute(), root.resolve()
    resolved = destination.resolve()
    if resolved.is_relative_to(output):
        raise ValueError('archive destination must be outside the consumer package')
    if resolved.is_relative_to(root) and not resolved.is_relative_to(root / 'dist'):
        raise ValueError('archive destination must not overwrite source repository files')
    if destination.is_symlink() or any(parent.is_symlink() for parent in destination.parents):
        raise ValueError('archive destination must not use symlinks')


def archive(output, destination, root=ROOT):
    check_archive_destination(output, destination, root)
    verify(output)
    with destination.open('wb') as raw, gzip.GzipFile(filename='', mode='wb', fileobj=raw, mtime=0) as gz, tarfile.open(fileobj=gz, mode='w') as tar:
        for path in sorted(p for p in output.rglob('*') if p.is_file()):
            content = path.read_bytes()
            info = tarfile.TarInfo('atlas-consumer/' + path.relative_to(output).as_posix())
            info.size, info.mode, info.mtime = len(content), 0o644, 0
            tar.addfile(info, io.BytesIO(content))
    verify(output)
    return digest(destination.read_bytes())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['build', 'verify'])
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--output', type=Path, default=ROOT / 'dist/atlas-consumer-wave5')
    parser.add_argument('--archive', type=Path)
    args = parser.parse_args()
    try:
        if args.archive:
            check_archive_destination(args.output, args.archive, args.root)
        if args.action == 'build':
            build(args.root, args.output)
        result = verify(args.output, args.root)
        if args.archive:
            checksum = archive(args.output, args.archive, args.root)
            result = verify(args.output, args.root)
            result['archive_sha256'] = checksum
        print(json.dumps(result, indent=2))
    except (ValueError, OSError, KeyError) as exc:
        parser.exit(1, f'{exc}\n')


if __name__ == '__main__':
    main()
