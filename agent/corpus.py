"""Read untrusted Markdown under a fixed library, without following symlinks."""
from pathlib import Path

MAX_NOTE_BYTES = 2_000_000


def library_path(root, relative):
    root = Path(root).resolve()
    # Validate the supplied POSIX form before Path renders native Windows '\\'.
    if '\\' in str(relative):
        raise ValueError('path must be relative to the library')
    relative = Path(relative)
    if relative.is_absolute() or '..' in relative.parts:
        raise ValueError('path must be relative to the library')
    path = root / relative
    base = root / 'knowledge'
    if not path.resolve().is_relative_to(base.resolve()) or base.is_symlink():
        raise ValueError('path outside knowledge')
    current = path
    while current != root:
        if current.is_symlink():
            raise ValueError('symlinks are not allowed in knowledge paths')
        current = current.parent
    return path


def read_text(root, relative):
    path = library_path(root, relative)
    if path.stat().st_size > MAX_NOTE_BYTES:
        raise ValueError('note exceeds size limit')
    return path.read_text(encoding='utf-8')


def scan_notes(root, diagnostics=None):
    from agent.knowledge import parse_note
    root = Path(root).resolve()
    diagnostics = diagnostics if diagnostics is not None else []
    out, seen = [], set()
    for path in sorted((root / 'knowledge').rglob('*.md')):
        if path.name.startswith('_') or any(p.startswith('.') for p in path.relative_to(root / 'knowledge').parts):
            continue
        relative = path.relative_to(root).as_posix()
        try:
            meta, body = parse_note(read_text(root, relative))
            if not isinstance(meta.get('id'), str) or not meta['id'].strip():
                raise ValueError('missing stable note id')
            if meta['id'] in seen:
                out[:] = [n for n in out if n['id'] != meta['id']]
                raise ValueError('duplicate note id; conflicting identity excluded')
            tier = meta.get('source_tier', 4) or 4
            if type(tier) is not int or not 1 <= tier <= 4:
                raise ValueError('invalid source_tier')
            for field in ('sources', 'queries'):
                if field in meta and (not isinstance(meta[field], list) or not all(isinstance(v, str) for v in meta[field])):
                    raise ValueError(f'invalid {field}')
            from urllib.parse import urlparse
            for url in meta.get('sources', []):
                urlparse(url)  # malformed bracketed host is a per-note diagnostic
            seen.add(meta['id'])
            out.append({**meta, '_path': relative, '_body': body})
        except (OSError, UnicodeError, ValueError, TypeError) as e:
            diagnostics.append({'path': relative, 'error': str(e)})
    return out
