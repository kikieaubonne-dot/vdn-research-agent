"""Atomic UTF-8 writes; temporary files never replace a good file on failure."""
from __future__ import annotations

import os
import tempfile
from pathlib import Path


def atomic_write(path: Path, text: str, *, create_only: bool = False):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix='.' + path.name + '.', suffix='.tmp', dir=path.parent)
    tmp = Path(name)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8', newline='') as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        if create_only:
            # An atomic hard link fails if a note already occupies this name.
            os.link(tmp, path)
        else:
            os.replace(tmp, path)
    finally:
        tmp.unlink(missing_ok=True)


def atomic_bytes(path: Path, data: bytes, *, create_only: bool = False):
    """Exact binary copies for evidence artifacts, not image transformations."""
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    fd,name=tempfile.mkstemp(prefix='.'+path.name+'.',suffix='.tmp',dir=path.parent)
    tmp=Path(name)
    try:
        with os.fdopen(fd,'wb') as stream:
            stream.write(data);stream.flush();os.fsync(stream.fileno())
        if create_only:os.link(tmp,path)
        else:os.replace(tmp,path)
    finally:tmp.unlink(missing_ok=True)
