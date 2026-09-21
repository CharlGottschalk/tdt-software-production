"""Explicit project setup, shipped as a stack template; Python 3.11+ stdlib."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shlex
import sys
import tempfile

OWNER = 'tdt.software-production.constitution.v1'
STATE = '.tdt/constitution-setup.json'
LOADER = '.tdt/constitution-loader.py'
DOCUMENT = '.tdt/CONSTITUTION.md'
CONFIGS = {'claude': '.claude/settings.json', 'codex': '.codex/hooks.json'}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path, limit=262144):
    for part in (path, *path.parents):
        if part.is_symlink():
            raise ValueError(f'Symlink refused: {path}')
        if part != path and part.exists() and not part.is_dir():
            raise ValueError(f'Non-directory ancestor: {path}')
    if not path.exists():
        return None
    if not path.is_file():
        raise ValueError(f'Expected regular file: {path}')
    with path.open('rb') as stream:
        value = stream.read(limit + 1)
    if len(value) > limit:
        raise ValueError(f'File exceeds limit: {path}')
    return value


def decode(raw):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('Duplicate JSON key')
            result[key] = value
        return result
    value = json.loads(raw, object_pairs_hook=unique)
    if not isinstance(value, dict):
        raise ValueError('Expected JSON object')
    return value


def encoded(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', type=Path, required=True)
    parser.add_argument('--project-id')
    parser.add_argument('--host', choices=(*CONFIGS, 'both'))
    parser.add_argument('--content', type=Path, help='Reviewed UTF-8 constitution draft; omit to reuse')
    parser.add_argument('--expected-sha256', help='Required exact prior document hash for an authorized content update')
    parser.add_argument('--apply', action='store_true', help='Apply already authorized setup; default is read-only preview')
    args = parser.parse_args()
    workspace = args.workspace.absolute()
    config = read(workspace / '.tdt/config.json')
    if config is None:
        raise ValueError('Not an installed workspace')
    decode(config)
    raw = read(workspace / '.tdt/state/projects.json')
    records = json.loads(raw) if raw is not None else []
    if not isinstance(records, list):
        raise ValueError('Invalid registry')
    seen = set()
    for record in records:
        if (not isinstance(record, dict) or not isinstance(record.get('path'), str)
                or not Path(record['path']).is_absolute()
                or record.get('id') != sha(record['path'].encode())
                or record['id'] in seen):
            raise ValueError('Invalid registry entry')
        seen.add(record['id'])
    if not args.project_id:
        print('Select/provide a project ID; no files changed:')
        for record in records:
            print(f"{record['id']}  {Path(record['path']).name}")
        return
    record = next((r for r in records if r['id'] == args.project_id), None)
    if record is None:
        raise ValueError('Unknown project ID; list registered IDs first')
    root = Path(record['path'])
    if not root.is_dir() or root.resolve(strict=True) != root:
        raise ValueError('Project path missing or moved')
    if root.is_relative_to(workspace) or workspace.is_relative_to(root):
        raise ValueError('Project overlaps workspace')
    for parent in (root, *root.parents):
        if (parent / '.tdt/config.json').exists():
            raise ValueError('Project is inside an installed workspace')
    project = read(root / '.tdt/project.json')
    if project is not None:
        project = decode(project)
        if project.get('format_version') != 1 or project.get('stack_id') != 'tdt-software-production':
            raise ValueError('Incompatible project.json; preserve and reconcile')
    if not args.host:
        raise ValueError('Select host: claude, codex or both; no files changed')
    if os.name != 'posix':
        raise ValueError('Native Windows setup unverified; do not generate POSIX commands (coordinate task 10)')
    old = {}
    changes = {}
    def snapshot(relative):
        if relative not in old:
            old[relative] = read(root / relative)
        return old[relative]
    prior = snapshot(STATE)
    state = decode(prior) if prior is not None else {'owner': OWNER, 'loader_sha256': None, 'hooks': {}}
    if (set(state) != {'owner', 'loader_sha256', 'hooks'} or state['owner'] != OWNER
            or not isinstance(state['hooks'], dict) or set(state['hooks']) - set(CONFIGS)):
        raise ValueError('Setup ownership collision')
    loader = read(Path(__file__).absolute().with_name('constitution-loader.py'))
    if loader is None:
        raise ValueError('Missing bundled loader')
    current_loader = snapshot(LOADER)
    if prior is None and current_loader is not None:
        raise ValueError('Unowned loader collision')
    if prior is not None and (current_loader is None or sha(current_loader) != state['loader_sha256']):
        raise ValueError('Owned loader edited or missing; preserve and reconcile')
    if prior is not None and current_loader != loader:
        raise ValueError('Loader version changed; explicit migration required')
    document = snapshot(DOCUMENT)
    if args.content:
        candidate = read(args.content.absolute(), 32768)
        if candidate is None or not candidate.strip():
            raise ValueError('Missing or empty constitution draft')
        candidate.decode('utf-8')
        if document is not None and candidate != document and args.expected_sha256 != sha(document):
            raise ValueError('Existing constitution: reuse or supply reviewed prior SHA256 for update')
        changes[DOCUMENT] = candidate
    elif document is None:
        raise ValueError('Missing constitution; provide grounded reviewed --content')
    elif not document.strip() or len(document) > 32768:
        raise ValueError('Constitution must be nonempty and at most 32 KiB')
    else:
        document.decode('utf-8')
    changes[LOADER] = loader
    hosts = list(CONFIGS) if args.host == 'both' else [args.host]
    # Validate all previously owned registrations even when adding only one host.
    for host in sorted(set(hosts) | set(state['hooks'])):
        relative = CONFIGS[host]
        raw_config = snapshot(relative)
        provider = decode(raw_config) if raw_config is not None else {}
        hooks = provider.setdefault('hooks', {})
        if not isinstance(hooks, dict):
            raise ValueError(f'Invalid hooks: {relative}')
        entries = hooks.setdefault('SessionStart', [])
        if not isinstance(entries, list) or any(not isinstance(e, dict) for e in entries):
            raise ValueError(f'Invalid SessionStart: {relative}')
        owned = state['hooks'].get(host)
        expected = {'hooks': [{'type': 'command', 'command': shlex.join([
            sys.executable, str(root / LOADER)]), 'timeout': 10}]}
        if owned is not None and owned != expected:
            raise ValueError(f'Owned command differs from current root/interpreter: {relative}; explicit migration required')
        if owned is not None and entries.count(owned) != 1:
            raise ValueError(f'Owned hook edited, missing or duplicated: {relative}')
        for entry in entries:
            if entry != owned and 'constitution-loader' in json.dumps(entry):
                raise ValueError(f'Constitution hook collision: {relative}')
        if host in hosts and owned is None:
            entry = expected
            entries.append(entry)
            state['hooks'][host] = entry
            changes[relative] = encoded(provider)
    state['loader_sha256'] = sha(loader)
    changes[STATE] = encoded(state)
    changes = {key: value for key, value in changes.items() if value != snapshot(key)}
    print(json.dumps({'project_id': args.project_id, 'changes': list(changes),
                      'mode': 'apply' if args.apply else 'preview',
                      'runtime': 'Hook delivery requires fresh trusted host verification; trust is unchanged'}))
    if not args.apply:
        return
    # Preflight every file before any writes. Retain originals for local rollback.
    for relative, before in old.items():
        if read(root / relative) != before:
            raise ValueError(f'Concurrent edit: {relative}')
    written = []
    try:
        for relative, data in changes.items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            if read(path) != old[relative]:
                raise ValueError(f'Concurrent edit: {relative}')
            fd, temporary = tempfile.mkstemp(prefix='.constitution-', dir=path.parent)
            try:
                with os.fdopen(fd, 'wb') as stream:
                    stream.write(data)
                if old[relative] is not None:
                    os.chmod(temporary, path.stat().st_mode & 0o777)
                if read(path) != old[relative]:
                    raise ValueError(f'Concurrent edit: {relative}')
                os.replace(temporary, path)
                written.append(relative)
            finally:
                if os.path.exists(temporary):
                    os.unlink(temporary)
    except Exception:
        for relative in reversed(written):
            path = root / relative
            if read(path) == changes[relative]:
                if old[relative] is None:
                    path.unlink()
                else:
                    path.write_bytes(old[relative])
        raise


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, RuntimeError) as exc:
        print(f'constitution setup: {exc}', file=sys.stderr)
        sys.exit(1)
