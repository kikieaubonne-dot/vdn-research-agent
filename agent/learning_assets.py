"""Explicit trusted-copy 3D inspection; Blender auto-run disabled, no model tool."""
import json
from pathlib import Path
import shutil
import math
from urllib.parse import unquote,urlsplit

from agent import intelligence_models as im
from agent.lab_store import lab_lock
from agent.learning_store import capacity,digest,get,load,receipt,run_tool,save,sha,staged
from agent.learning_media import rights
from agent.obsidian import safe_path

SCRIPT=Path(__file__).resolve().parents[1]/'scripts/blender_inspect_learning.py'


def gltf_dependencies(path):
    if path.suffix.lower()!='.gltf':return []
    data=json.loads(path.read_text(encoding='utf-8'));out=[]
    for obj in data.get('buffers',[])+data.get('images',[]):
        uri=obj.get('uri')
        if uri is None:continue
        if not isinstance(uri,str) or len(uri)>2_000_000:raise ValueError('invalid glTF URI')
        if uri.startswith(('data:application/octet-stream;base64,','data:image/png;base64,','data:image/jpeg;base64,')):continue
        for _ in range(2):uri=unquote(uri)
        parsed=urlsplit(uri)
        if parsed.scheme or parsed.netloc or parsed.query or parsed.fragment or '\\' in uri or ':' in uri:raise ValueError('external glTF reference refused')
        p=safe_path(path.parent,uri)
        if p.suffix.lower() not in ('.bin','.png','.jpg','.jpeg','.webp') or not p.is_file() or p.stat().st_size>8_000_000:raise ValueError('unavailable bounded glTF sidecar')
        out.append({'file':p.relative_to(path.parent).as_posix(),'sha256':sha(p)})
    return out


def inspect(root,relative,license='UNKNOWN',attest=False,trusted_copy=False):
    rights(license,attest)
    if trusted_copy is not True:raise PermissionError('trusted staged copy required; this runner is not an OS security boundary for hostile blend files')
    root=Path(root).resolve();source=staged(root,relative,('.blend','.obj','.fbx','.gltf','.glb'));deps=gltf_dependencies(source)
    binary=shutil.which('blender')
    if not binary:raise RuntimeError('Blender unavailable')
    spec={'schema':'vdn.asset-spec/1','storage_format':'canonical-inspection-1','input':relative,'input_sha256':sha(source),'script_sha256':sha(SCRIPT),'blender_executable_sha256':sha(binary),'dependencies':deps,'extra_inputs':{(Path(relative).parent/d['file']).as_posix():d['sha256'] for d in deps},'license':license,'trusted_copy_operator_attested':True,'auto_run':False}
    key=digest(spec);folder='lab/learning/assets/'+key
    with lab_lock(root,'.learning-assets'):
        if safe_path(root,folder+'/result.json').exists():return {**read(root,key),'cache_hit':True}
        if safe_path(root,folder).exists():raise ValueError('interrupted asset attempt retained')
        def work():
            capacity(root,500000);safe_path(root,folder).mkdir(parents=True);save(root,folder+'/spec.json',spec)
            execution=run_tool(root,[binary,'--background','--factory-startup','--disable-autoexec','--threads','1','--python-exit-code','2','--python',str(SCRIPT),'--','--input',relative,'--output',folder+'/inspection.json'],folder+'/process.log',timeout=15)
            report=load(root,folder+'/inspection.json')
            if report.get('schema')!='vdn.asset-inspection/1' or report.get('input_saved') is not False or sha(source)!=spec['input_sha256'] or gltf_dependencies(source)!=deps:raise ValueError('asset/source inspection integrity failure')
            capacity(root)
            receipt(root,folder,{'schema':'vdn.asset-result/1','key':key,'state':'PARTIAL','spec':spec,'inspection_file':'inspection.json','execution':execution,'scope':'actual Blender metrics only; trusted copy, no real Roblox or security-sandbox guarantee','cache_hit':False})
            return read(root,key)
        try:return im.operation(root,work)
        except Exception as exc:
            from agent.reliability import BlackBox
            BlackBox(root).incident('asset_inspector','read_only',str(exc),'MEDIUM',type(exc).__name__,True);raise


def read(root,key):
    import re
    if not re.fullmatch('[a-f0-9]{64}',key):raise ValueError('invalid asset result identity')
    folder='lab/learning/assets/'+key;r=get(root,folder)
    if r.get('inspection_file')!='inspection.json':raise ValueError('unknown inspection payload')
    return {**r,'inspection':load(root,folder+'/inspection.json')}


def roundtrip(native,imported,mesh_prefix=None):
    a=native['inspection'];b=imported['inspection'];issues=[]
    def meshes(r):return [x for x in r['objects'] if not mesh_prefix or x['name'].startswith(mesh_prefix)]
    x,y=meshes(a),meshes(b)
    if sum(o['triangles'] for o in x)!=sum(o['triangles'] for o in y):issues.append('triangle_count_changed')
    if not b['armatures'] and a['armatures']:issues.append('rig_missing')
    if not b['actions'] and a['actions']:issues.append('animation_missing')
    return {'state':'PASS' if not issues else 'FAIL','issues':issues,'scope':'structural roundtrip only; animation poses, coordinates and Roblox still need separate checks','Roblox':'NOT_TESTED','human_approved':False}


def compare_poses(native,imported,actor,bone,tolerance):
    """Compare independently imported poses in the reported world coordinates.

    Caller supplies a predeclared tolerance, actor and landmark. No axis fitting
    or best-pose alignment can hide an actual export loss. Structural PASS alone
    never implies animation preservation.
    """
    if type(tolerance) not in (int,float) or not math.isfinite(tolerance) or tolerance<0:raise ValueError('finite predeclared tolerance required')
    a=native['inspection']['pose_samples'];b=imported['inspection']['pose_samples']
    differences=[];issues=[]
    for fraction in (0,.5,1):
        try:
            def point(samples):
                sample=next(s for s in samples if s['fraction']==fraction)
                rig=next(r for r in sample['rigs'] if r['name']==actor or r['name'].startswith(actor+'.'))
                value=next(p['head'] for p in rig['bones'] if p['name']==bone)
                if len(value)!=3 or not all(type(v) in (int,float) and math.isfinite(v) for v in value):raise ValueError('invalid pose coordinates')
                return value
            error=math.dist(point(a),point(b));differences.append({'fraction':fraction,'distance':error})
            if error>tolerance:issues.append('pose_changed_at_'+str(fraction))
        except (StopIteration,KeyError):issues.append('missing_pose_at_'+str(fraction))
    return {'state':'FAIL' if issues else 'PASS','issues':issues,'differences':differences,'tolerance':tolerance,'scope':'three sampled landmark positions only; not exhaustive animation, deformation, aesthetic or Roblox validation','human_approved':False,'Roblox':'NOT_TESTED'}
