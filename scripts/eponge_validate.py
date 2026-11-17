"""Independent local test runner: fixed suites, pinned inputs, real exit codes.

Does not import the core, edit tests, approve a patch or promote a solution.
"""
import argparse
import hashlib
import json
from pathlib import Path
import os
import subprocess
import sys
import threading
import time

try:
    from scripts import eponge_guard as guard
except ModuleNotFoundError:
    import eponge_guard as guard


def inventory(source):
    files=[]
    for folder in ('agent','scripts','tests','bench','config'):
        for p in (source/folder).rglob('*') if (source/folder).exists() else []:
            if p.suffix.lower() in ('.py','.json','.cmd','.ps1') and '__pycache__' not in p.parts:files.append(p)
    files += [source/n for n in ('eponge.py','vdn_mcp.py','Eponge.cmd') if (source/n).exists()]
    if not files or len(files)>2000:raise ValueError('validation inventory cap')
    return {p.relative_to(source).as_posix():hashlib.sha256(guard.safe(source,p.relative_to(source).as_posix()).read_bytes()).hexdigest() for p in sorted(files)}


def run(source,baseline,output,suite,timeout=500):
    source=Path(source).resolve();output=Path(output).absolute();baseline=Path(baseline)
    if output.exists() or output.is_relative_to(source) or source.is_relative_to(output):raise ValueError('new external validation output required')
    if baseline.stat().st_size>2_000_000:raise ValueError('baseline oversized')
    m=json.loads(baseline.read_text(encoding='utf-8'))
    output.mkdir(parents=True);before=inventory(source)
    if m.get('schema')!='vdn.validation-baseline/1' or m.get('files')!=before:
        result={'state':'REJECTED','reason':'pinned inputs or criteria changed','promoted':False};guard.write(output,'validation.json',result);return result,2
    commands={'offline':[sys.executable,'-m','tests.offline'],'operations':[sys.executable,'-m','unittest','tests.test_operations','-v']}
    if suite not in commands:raise ValueError('suite not allowlisted')
    if type(timeout) is not int or not 1<=timeout<=500:raise ValueError('bounded validation timeout required')
    start=time.monotonic();env=dict(os.environ);env.update(PYTHONUTF8='1',PYTHONIOENCODING='utf-8');timed_out=False
    options={'start_new_session':True} if os.name!='nt' else {'creationflags':subprocess.CREATE_NEW_PROCESS_GROUP}
    with (output/'tests.log').open('wb') as log:
        p=subprocess.Popen(commands[suite],cwd=source,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env=env,shell=False,**options)
        failed=threading.Event();reader=threading.Thread(target=guard.drain,args=(p.stdout,log,failed),daemon=True);reader.start()
        while p.poll() is None:
            if time.monotonic()-start>=timeout or failed.is_set():timed_out=True;guard.terminate(p);break
            time.sleep(.1)
        reader.join(timeout=2)
    changed=inventory(source)!=before
    result={'schema':'vdn.validation-result/1','state':'FAIL' if changed or timed_out or p.returncode else 'PASS','exit_code':p.returncode,'timeout_or_log_failure':timed_out,'pinned_inputs_changed':changed,'suite':suite,'elapsed_s':time.monotonic()-start,'manifest_sha256':hashlib.sha256(baseline.read_bytes()).hexdigest(),'log_sha256':hashlib.sha256((output/'tests.log').read_bytes()).hexdigest(),'promoted':False,'scope':'real software checks, no game or semantic quality inferred'}
    guard.write(output,'validation.json',result);return result,0 if result['state']=='PASS' else 1


def main():
    p=argparse.ArgumentParser();s=p.add_subparsers(dest='command',required=True)
    q=s.add_parser('prepare');q.add_argument('--source',type=Path,required=True);q.add_argument('--manifest',type=Path,required=True);q.add_argument('--approve-baseline',action='store_true')
    q=s.add_parser('run');q.add_argument('--source',type=Path,required=True);q.add_argument('--manifest',type=Path,required=True);q.add_argument('--output',type=Path,required=True);q.add_argument('--suite',choices=['offline','operations'],default='offline');q.add_argument('--timeout',type=int,default=500);a=p.parse_args()
    try:
        if a.command=='prepare':
            if not a.approve_baseline or a.manifest.exists():raise PermissionError('new explicitly approved baseline required')
            guard.write(a.manifest.parent,a.manifest.name,{'schema':'vdn.validation-baseline/1','files':inventory(a.source.resolve()),'at':time.time(),'source':'explicit operator approval; never generated from model score'})
            print(json.dumps({'state':'PINNED','automatic_promotion':False}));return 0
        r,code=run(a.source,a.manifest,a.output,a.suite,a.timeout);print(json.dumps(r));return code
    except Exception as exc:print(json.dumps({'state':'BLOCKED','exception_type':type(exc).__name__,'promoted':False}));return 2


if __name__=='__main__':raise SystemExit(main())
