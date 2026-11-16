"""Run the suite in a disposable copy with network/autonomy enabled personally.

No setting in the source checkout is changed. Test roots use frozen fixtures.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def main():
    source=Path(__file__).resolve().parents[1]
    before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (source/'config').glob('*.json')}
    with tempfile.TemporaryDirectory(prefix='vdn-personal-') as d:
        root=Path(d)/'project';root.mkdir()
        def ignore(folder,names):return [n for n in names if n in ('.git','.env','.obsidian','__pycache__','.venv','lab','cache') or (Path(folder)/n).is_symlink()]
        for name in ('agent','bench','config','docs','knowledge','output','roblox','scripts','tests','.github'):
            if (source/name).exists():shutil.copytree(source/name,root/name,ignore=ignore)
        for path in source.iterdir():
            if path.is_file() and not path.is_symlink() and path.suffix in ('.py','.md'):shutil.copyfile(path,root/path.name)
        p=root/'config/v10.json';cfg=json.loads(p.read_text(encoding='utf-8'));cfg['network_enabled']=True;cfg['autonomous_enabled']=True;cfg['schedule']['enabled']=True;p.write_text(json.dumps(cfg),encoding='utf-8')
        personal=p.read_bytes()
        result=subprocess.run([sys.executable,'-m','tests.offline'],cwd=root,timeout=500)
        if p.read_bytes()!=personal:raise AssertionError('test suite changed personal configuration')
    after={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (source/'config').glob('*.json')}
    if before!=after:raise AssertionError('source configuration modified')
    print('PERSONAL_CONFIG: network/autonomy enabled in disposable copy; personal/source settings unchanged.')
    return result.returncode


if __name__=='__main__':raise SystemExit(main())
