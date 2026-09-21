"""Project-owned SessionStart context; Python 3.11+, no ThisDamnThing dependency."""
import json
from pathlib import Path
import sys


def main():
    raw = sys.stdin.buffer.read(65537)
    if len(raw) > 65536:
        raise ValueError('Hook input exceeds 64 KiB')
    event = json.loads(raw)
    if not isinstance(event, dict) or event.get('hook_event_name') != 'SessionStart':
        raise ValueError('Expected SessionStart object')
    cwd = event.get('cwd')
    if not isinstance(cwd, str) or not Path(cwd).is_absolute():
        raise ValueError('Expected absolute session cwd')
    root = Path(__file__).resolve().parents[1]
    cwd = Path(cwd).resolve(strict=True)
    if not cwd.is_relative_to(root):
        return
    # A nested Git project or installed workspace is a different scope.
    for directory in (cwd, *cwd.parents):
        if directory == root:
            break
        if (directory / '.git').exists() or (directory / '.tdt/config.json').exists():
            return
    path = root / '.tdt/CONSTITUTION.md'
    if path.is_symlink() or not path.is_file():
        raise ValueError('Missing or unsafe .tdt/CONSTITUTION.md')
    with path.open('rb') as stream:
        content = stream.read(32769)
    if len(content) > 32768 or not content.strip():
        raise ValueError('Constitution must be nonempty and at most 32 KiB')
    print(json.dumps({'hookSpecificOutput': {
        'hookEventName': 'SessionStart',
        'additionalContext': 'Project constitution (.tdt/CONSTITUTION.md):\n' + content.decode('utf-8')}}))


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, RuntimeError) as exc:
        print(f'project constitution: {exc}', file=sys.stderr)
        sys.exit(1)
