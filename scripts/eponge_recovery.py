"""Explicitly approved, tested executable images; restore into a NEW workspace.

Standard library only. Never overwrites the failed workspace, starts a service,
promotes code, changes permissions, clears budgets or trusts a model's score.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

try:
    from scripts import eponge_guard as guard, eponge_validate as validator
except ModuleNotFoundError:
    import eponge_guard as guard
    import eponge_validate as validator


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def tree(root):
    root=Path(root);files={};total=0
    for p in sorted(root.rglob('*')):
        name=p.relative_to(root).as_posix();guard.safe(root,name)
        if p.is_file():
            total+=p.stat().st_size;files[name]=sha(p)
            if len(files)>10000 or total>64_000_000:raise ValueError('recovery copy cap reached')
    return files


def seal(source,baseline,validation,destination,approve=False):
    if approve is not True:raise PermissionError('explicit approval of tested image required')
    source=Path(source).absolute();dest=Path(destination).absolute();validation=Path(validation);baseline=Path(baseline)
    guard.safe(dest,'probe')
    if dest.exists() or dest.is_relative_to(source) or source.is_relative_to(dest):raise ValueError('new separate image required')
    pin=guard.read(baseline.parent,baseline.name);result=guard.read(validation,'validation.json')
    inputs=validator.inventory(source)
    if pin.get('schema')!='vdn.validation-baseline/1' or pin.get('files')!=inputs:raise ValueError('source differs from independently pinned tests')
    if result.get('state')!='PASS' or result.get('suite')!='offline' or result.get('exit_code')!=0 or result.get('pinned_inputs_changed') is not False or result.get('manifest_sha256')!=sha(baseline) or result.get('log_sha256')!=sha(guard.safe(validation,'tests.log')):raise ValueError('matching successful full validation required')
    files={n:h for n,h in inputs.items() if n.startswith(('agent/','scripts/','config/')) or n in ('eponge.py','vdn_mcp.py','Eponge.cmd')}
    if not files or sum(guard.safe(source,n).stat().st_size for n in files)>10_000_000:raise ValueError('bounded executable image required')
    dest.mkdir(parents=True)
    for name in files:
        p=guard.safe(dest,'files/'+name);p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(guard.safe(source,name),p)
    if validator.inventory(source)!=inputs:raise ValueError('source changed during image preparation')
    record={'schema':'vdn.approved-executable/1','files':files,'approval':'EXPLICIT_OPERATOR_ONLY','validation_manifest_sha256':sha(baseline),'validation_result_sha256':sha(guard.safe(validation,'validation.json')),'data_contract':'vdn.mission-checkpoint/2','promotion':False,'scope':'checksummed image, not an OS authentication boundary or universal bug-free guarantee'}
    guard.write(dest,'image.json',record)
    return {'state':'SEALED_TESTED_IMAGE','image_sha256':sha(dest/'image.json'),'files':len(files),'promoted':False}


def check_image(image,expected_hash):
    image=Path(image)
    if sha(guard.safe(image,'image.json'))!=expected_hash:raise ValueError('approved image manifest fingerprint mismatch')
    record=guard.read(image,'image.json')
    if record.get('schema')!='vdn.approved-executable/1' or record.get('approval')!='EXPLICIT_OPERATOR_ONLY' or record.get('data_contract')!='vdn.mission-checkpoint/2':raise ValueError('unapproved or incompatible image')
    if not 1<=len(record['files'])<=1000 or tree(guard.safe(image,'files'))!=record['files']:raise ValueError('image files missing, changed or unexpected')
    return record


def recover(workspace,image,expected_hash,destination,apply=False):
    if apply is not True:raise PermissionError('explicit recovery to a NEW copy required')
    source=Path(workspace).absolute();dest=Path(destination).absolute();guard.safe(dest,'probe')
    if dest.exists() or dest.is_relative_to(source) or source.is_relative_to(dest):raise ValueError('new isolated recovery destination required')
    approved=check_image(image,expected_hash)
    cp=guard.read(source,'checkpoint.json');checkpoint_hash=sha(guard.safe(source,'checkpoint.json'));base={k:v for k,v in cp.items() if k!='payload_sha256'}
    if cp.get('schema')!='vdn.mission-checkpoint/2' or cp.get('payload_sha256')!=hashlib.sha256(json.dumps(base,sort_keys=True,ensure_ascii=False,allow_nan=False).encode()).hexdigest():raise ValueError('checkpoint damaged; preserve for manual review')
    locks=[]
    try:
        # A dead guard can leave a lease companion briefly alive. Both locks
        # must be free; never kill or steal a recorded PID to allow recovery.
        for name in ('guard.lock','worker.lock'):locks.append(guard.exclusive(guard.safe(source,name)))
        incoming={}
        for folder in ('runtime','vault','reports'):
            if guard.safe(source,folder).exists():incoming.update({folder+'/'+n:h for n,h in tree(guard.safe(source,folder)).items()})
        if not any(n.startswith('runtime/') for n in incoming):raise ValueError('runtime missing')
        cfg=guard.read(source,'mission.json',16000)
        # Verify existing protected files against the pre-crash checkpoint.
        for name,h in cp['baseline_protected'].items():
            if sha(guard.safe(source,'runtime/'+name))!=h:raise ValueError('reliable inputs changed; executable recovery cannot repair them')
        dest.mkdir(parents=True)
        for name,h in incoming.items():
            p=guard.safe(dest,name);p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(guard.safe(source,name),p)
            if sha(p)!=h:raise ValueError('runtime copy integrity failure')
        for name in approved['files']:
            p=guard.safe(dest,'code/'+name);p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(guard.safe(Path(image),'files/'+name),p)
        guard.write(dest,'code-manifest.json',{'schema':'vdn.frozen-code/1','files':approved['files']})
        guard.verify_code(dest)
        cfg['enabled']=False;guard.write(dest,'mission.json',cfg)
        shutil.copyfile(guard.safe(source,'checkpoint.json'),guard.safe(dest,'checkpoint.json'))
        if sha(guard.safe(dest,'checkpoint.json'))!=checkpoint_hash:raise ValueError('checkpoint changed during recovery')
        guard.write(dest,'control.json',{'state':'STOPPED'})
        if any(sha(guard.safe(source,n))!=h for n,h in incoming.items()):raise ValueError('failed workspace changed during recovery')
        receipt={'schema':'vdn.executable-recovery/1','state':'RECOVERED_DISABLED','approved_image_sha256':expected_hash,'copied_files':len(incoming),'runtime_files_unchanged':True,'checkpoint_preserved':True,'budget_reset':False,'old_workspace_retained':True,'automatic_promotion':False,'automatic_start':False,'requires':'explicit diagnostic and start on the new workspace'}
        guard.write(dest,'recovery.json',receipt);return receipt
    finally:
        for lock in reversed(locks):lock.close()


def main():
    p=argparse.ArgumentParser(description=__doc__);s=p.add_subparsers(dest='command',required=True)
    a=s.add_parser('seal');a.add_argument('--source',type=Path,required=True);a.add_argument('--manifest',type=Path,required=True);a.add_argument('--validation',type=Path,required=True);a.add_argument('--destination',type=Path,required=True);a.add_argument('--approve-image',action='store_true')
    a=s.add_parser('recover');a.add_argument('--workspace',type=Path,required=True);a.add_argument('--image',type=Path,required=True);a.add_argument('--image-sha256',required=True);a.add_argument('--destination',type=Path,required=True);a.add_argument('--apply',action='store_true');a=p.parse_args()
    try:
        r=seal(a.source,a.manifest,a.validation,a.destination,a.approve_image) if a.command=='seal' else recover(a.workspace,a.image,a.image_sha256,a.destination,a.apply)
        print(json.dumps(r));return 0
    except (OSError,ValueError,KeyError) as exc:
        print(json.dumps({'state':'BLOCKED','type':type(exc).__name__,'message':guard.redact(exc)}));return 2


if __name__=='__main__':raise SystemExit(main())
