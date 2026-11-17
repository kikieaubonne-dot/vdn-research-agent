"""Isolated learning evidence, never reliable-memory or code promotion."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import threading
import time

from agent import budget
from agent.lab_store import clean_json
from agent.obsidian import safe_path
from agent.ocean_web import settings
from agent.lab_runner import LocalLab
from agent.storage import atomic_write
from scripts.eponge_guard import terminate,drain

VERSION='learning-1'


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def digest(value):return hashlib.sha256(clean_json(value,1_000_000).encode()).hexdigest()


def save(root,relative,value):atomic_write(safe_path(root,relative),clean_json(value,1_000_000)+'\n')


def load(root,relative):
    p=safe_path(root,relative)
    if p.stat().st_size>1_000_000:raise ValueError('learning record oversized')
    return json.loads(p.read_text(encoding='utf-8'))


def staged(root,relative,extensions,max_bytes=8_000_000):
    if not isinstance(relative,str) or not relative.startswith('lab/inbox/'):raise ValueError('explicit staged laboratory input required')
    p=safe_path(root,relative)
    if p.suffix.lower() not in extensions or not p.is_file() or not 0<p.stat().st_size<=max_bytes:raise ValueError('input type/size refused')
    return p


def capacity(root,extra=0):
    total=0;count=0
    for folder in ('lab/learning','lab/inbox/learning'):
        for p in safe_path(root,folder).rglob('*'):
            safe_path(root,p.relative_to(root).as_posix())
            if p.is_file():total+=p.stat().st_size;count+=1
    if count>1000:raise ValueError('learning file count cap')
    LocalLab(root).check_storage(total+extra)


def run_tool(root,args,output,timeout=12,max_bytes=1_000_000,json_stdout=False):
    """Trusted callers construct argv; never accepts commands from source text.

    Own process group, bounded wall time/output, no proxy or download mechanism.
    """
    budget.check();p=safe_path(root,output)
    if p.exists():raise ValueError('retain previous tool log')
    p.parent.mkdir(parents=True,exist_ok=True)
    active=budget.CURRENT.get();seconds=min(timeout,max(.05,active.deadline-time.monotonic())) if active else timeout
    env=dict(os.environ);env.update(OMP_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1',BLENDER_USER_RESOURCES=str(p.parent/'blender-user'))
    opts={'start_new_session':True} if os.name!='nt' else {'creationflags':subprocess.CREATE_NEW_PROCESS_GROUP}
    start=time.monotonic();child=None;reader=None;failed=threading.Event()
    with p.open('xb') as log:
        try:
            child=subprocess.Popen(args,cwd=root,stdout=log if json_stdout else subprocess.PIPE,stderr=subprocess.STDOUT,stdin=subprocess.DEVNULL,env=env,shell=False,**opts)
            if not json_stdout:
                reader=threading.Thread(target=drain,args=(child.stdout,log,failed),daemon=True);reader.start()
            while child.poll() is None:
                if time.monotonic()-start>=seconds or p.stat().st_size>max_bytes or failed.is_set():raise TimeoutError('tool time/output cap')
                budget.check();time.sleep(.02)
            if p.stat().st_size>max_bytes:raise ValueError('tool output oversized')
            if child.returncode:raise RuntimeError('local tool failed; retained log '+output)
        finally:
            if child is not None:terminate(child)
            if reader is not None:reader.join(timeout=1);child.stdout.close()
        if failed.is_set() or reader is not None and reader.is_alive():raise RuntimeError('tool log reader did not complete')
        log.flush()
        if p.stat().st_size>max_bytes:raise ValueError('tool output oversized')
    return {'exit_code':child.returncode,'elapsed_s':time.monotonic()-start,'log':output,'sha256':sha(p)}


def receipt(root,folder,result):
    """Seal output files. Readers detect missing or edited evidence before reuse."""
    p=safe_path(root,folder);files={}
    for f in sorted(p.iterdir()):
        safe_path(root,f.relative_to(root).as_posix())
        if f.is_file() and f.name!='result.json':files[f.name]=sha(f)
    result={**result,'files':files,'verified':False,'reliable_memory_modified':False}
    save(root,folder+'/result.json',{'payload':result,'sha256':digest(result)})
    return result


def get(root,folder):
    value=load(root,folder+'/result.json');r=value['payload']
    if digest(r)!=value.get('sha256'):raise ValueError('learning result integrity failure')
    for name,h in r['files'].items():
        if '/' in name or sha(safe_path(root,folder+'/'+name))!=h:raise ValueError('learning evidence changed')
    spec=r.get('spec',{});obsolete=False
    for path_key,hash_key in (('input','input_sha256'),('captions','captions_sha256')):
        if spec.get(path_key):
            try:obsolete=obsolete or sha(safe_path(root,spec[path_key]))!=spec[hash_key]
            except FileNotFoundError:obsolete=True
    for path,h in spec.get('extra_inputs',{}).items():
        try:obsolete=obsolete or sha(safe_path(root,path))!=h
        except FileNotFoundError:obsolete=True
    return {**r,'inputs_obsolete':obsolete}
