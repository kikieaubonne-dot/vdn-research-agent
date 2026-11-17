"""Explicit, quota-bound visual-bake trial over an existing trusted prototype."""
import argparse
import datetime as dt
import gzip
import json
import math
from pathlib import Path
import re
import shutil
from agent import intelligence_models as im
from agent.lab_store import lab_lock
from agent.learning_media import rights
from agent.learning_store import capacity,digest,get,load,receipt,run_tool,save,sha,staged
from agent.obsidian import safe_path
from agent.research_session import config

SCRIPT=Path(__file__).resolve().parents[1]/'scripts/blender_animation_trial.py'


def load_samples(root,path):
    with gzip.open(safe_path(root,path),'rb') as stream:raw=stream.read(1000001)
    if len(raw)>1000000:raise ValueError('expanded pose evidence oversized')
    value=json.loads(raw)
    if value.get('schema')!='vdn.animation-samples/1':raise ValueError('unknown pose evidence')
    return value


def compare(reference,candidate,position_tolerance=1e-5,duration_tolerance=1e-6):
    """25 samples, all joints and skinned surfaces. No best-fit alignment."""
    for v in (position_tolerance,duration_tolerance):
        if type(v) not in (int,float) or not math.isfinite(v) or v<0:raise ValueError('finite predeclared tolerances required')
    errors=[];joint=surface=skin=tail=0.
    def number(v):
        if type(v) not in (int,float) or not math.isfinite(v):raise ValueError('invalid metric')
        return v
    duration=abs(number(reference['duration_s'])-number(candidate['duration_s']))
    if duration>duration_tolerance:errors.append('duration_changed')
    a=reference['samples'];b=candidate['samples']
    if len(a)!=25 or len(b)!=25:errors.append('sample_count_changed')
    for i,(x,y) in enumerate(zip(a,b)):
        if x['fraction']!=i/24 or y['fraction']!=i/24:errors.append('sample_time_changed')
        for kind in ('bones','meshes'):
            if not x[kind] or set(x[kind])!=set(y[kind]):errors.append('missing_or_extra_'+kind);continue
            for name,row in x[kind].items():
                other=y[kind][name]
                for field in (('head',) if kind=='bones' else ('min','max','surface_centroid')):
                    v,w=row[field],other[field]
                    if len(v)!=3 or len(w)!=3:raise ValueError('3D vector required')
                    distance=math.dist([number(n) for n in v],[number(n) for n in w])
                    if kind=='bones':joint=max(joint,distance)
                    else:surface=max(surface,distance)
                if kind=='meshes' and row['triangles']!=other['triangles']:errors.append('topology_changed')
                if kind=='bones':
                    # glTF stores joints/inverse binds, not Blender display tails.
                    # Compare deformation transforms; preserve tail differences
                    # as a diagnostic, never align or alter the actual geometry.
                    tail=max(tail,math.dist([number(n) for n in row['tail']],[number(n) for n in other['tail']]))
                    v,w=row.get('skin_matrix',[]),other.get('skin_matrix',[])
                    if len(v)!=16 or len(w)!=16:errors.append('missing_skin_transform')
                    else:skin=max(skin,max(abs(number(n)-number(m)) for n,m in zip(v,w)))
    if joint>position_tolerance:errors.append('joint_trajectory_changed')
    if surface>position_tolerance:errors.append('deformation_changed')
    if skin>position_tolerance:errors.append('skin_transform_changed')
    return {'state':'FAIL' if errors else 'PASS','criteria_version':'interop-2','errors':sorted(set(errors)),'max_joint_position_error':joint,'max_surface_error':surface,'max_skin_matrix_element_error':skin,'max_display_tail_error':tail,'duration_error_s':duration,'samples_compared':min(len(a),len(b)),'position_tolerance':position_tolerance,'duration_tolerance':duration_tolerance,'scope':'25 sampled poses, joint heads, skin matrices and surface bounds/area centroids; glTF display tails are reconstructed and separately reported; no exhaustive continuous animation or Roblox validation','Roblox':'NOT_TESTED','human_approved':False}


def remaining(root):
    path=safe_path(root,'lab/ocean/intelligence/compute.json');record=load(root,'lab/ocean/intelligence/compute.json') if path.exists() else {}
    used=record.get('reserved_s',0) if record.get('date')==dt.datetime.now(dt.timezone.utc).date().isoformat() else 0
    return max(0,config(root)['research']['compute_budget_s']-used)


def trial(root,relative,actor,format='glb',apply=False,license='UNKNOWN',attest=False,trusted_copy=False,existing_export=None):
    rights(license,attest)
    if trusted_copy is not True:raise PermissionError('explicit trusted copy required; Blender is not an OS security sandbox')
    if format not in ('glb','fbx') or not re.fullmatch('[A-Za-z0-9_.-]{1,80}',actor):raise ValueError('invalid trial parameters')
    root=Path(root).resolve();source=staged(root,relative,('.blend',));binary=shutil.which('blender')
    if not binary:raise RuntimeError('Blender unavailable')
    exported=staged(root,existing_export,('.'+format,)) if existing_export else None
    spec={'schema':'vdn.animation-trial/1','input':relative,'input_sha256':sha(source),'actor':actor,'format':format,'license':license,'script_sha256':sha(SCRIPT),'binary_sha256':sha(binary),'criteria_version':'interop-2','position_tolerance':1e-5,'duration_tolerance':1e-6,'poses':25,'method':'reopen_and_compare_existing' if exported else 'visual_bake','minimum_remaining_s':5 if exported else 8,'existing_export':existing_export,'existing_export_sha256':sha(exported) if exported else None}
    key=digest(spec);folder='lab/learning/animation/'+key;output='lab/inbox/learning/animation-'+key
    plan={'state':'PLANNED','key':key,'spec':spec,'output':output,'remaining_compute_s':remaining(root),'network_calls':0,'writes':0}
    if not apply:return plan
    if remaining(root)<spec['minimum_remaining_s']:return {**plan,'state':'BLOCKED','reason':'insufficient existing compute budget for bounded bake and independent probe; no quota change or process started'}
    with lab_lock(root,'.animation-trial'):
        if safe_path(root,folder+'/result.json').exists():return {**get(root,folder),'cache_hit':True}
        if remaining(root)<spec['minimum_remaining_s']:return {**plan,'state':'BLOCKED','reason':'insufficient existing compute budget for bounded bake and independent probe; no quota change or process started'}
        if safe_path(root,folder).exists() or safe_path(root,output).exists():raise ValueError('previous attempt retained; inspect before a revised trial')
        def work():
            capacity(root,80000 if exported else 300000);safe_path(root,folder).mkdir(parents=True);safe_path(root,output).mkdir(parents=True);save(root,folder+'/spec.json',spec)
            args=[binary,'--background','--factory-startup','--disable-autoexec','--threads','1','--python-exit-code','2','--python',str(SCRIPT),'--','--actor',actor,'--format',format,'--output',output]
            bake=run_tool(root,args+['--phase','reference' if exported else 'bake','--input',relative],folder+'/bake.log',timeout=10)
            native=load_samples(root,output+'/native.json.gz');internal=None if exported else compare(native,load_samples(root,output+'/baked.json.gz'))
            if internal and internal['state']!='PASS':raise ValueError('visual bake changed native trajectory; retain candidate and do not export as accepted')
            probe=run_tool(root,args+['--phase','probe','--input',existing_export if exported else output+'/baked.'+format],folder+'/probe.log',timeout=8)
            imported=load_samples(root,output+'/imported.json.gz');comparison=compare(native,imported)
            if comparison['state']=='FAIL':
                from agent.reliability import BlackBox
                BlackBox(root).incident('animation_roundtrip','comparison',','.join(comparison['errors']),'HIGH','TRAJECTORY_GATE',True)
            if sha(source)!=spec['input_sha256']:raise ValueError('source changed during trial')
            paths={p.relative_to(root).as_posix():sha(p) for p in safe_path(root,output).iterdir() if p.is_file()}
            if exported:
                if sha(exported)!=spec['existing_export_sha256']:raise ValueError('export changed during trial')
                paths[existing_export]=sha(exported)
            spec['extra_inputs']=paths;capacity(root)
            return receipt(root,folder,{'schema':'vdn.animation-result/1','key':key,'state':comparison['state'],'spec':spec,'native_to_baked':internal,'roundtrip':comparison,'execution':{'bake':bake,'independent_probe':probe},'scope':'Actual trusted-copy Blender trial only; no Studio, aesthetic or production compatibility claim','truth_verified':False})
        try:return im.operation(root,work)
        except Exception as exc:
            from agent.reliability import BlackBox
            BlackBox(root).incident('animation_roundtrip','visual_bake',str(exc),'HIGH',type(exc).__name__,True);raise


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,required=True);p.add_argument('--input',required=True);p.add_argument('--actor',required=True);p.add_argument('--format',choices=['glb','fbx'],default='glb');p.add_argument('--existing-export');p.add_argument('--apply',action='store_true');p.add_argument('--license',default='UNKNOWN');p.add_argument('--attest-rights',action='store_true');p.add_argument('--trusted-copy',action='store_true');a=p.parse_args()
    r=trial(a.root,a.input,a.actor,a.format,a.apply,a.license,a.attest_rights,a.trusted_copy,a.existing_export);print(json.dumps(r,ensure_ascii=False,indent=2));return 2 if r['state'] in ('BLOCKED','FAIL') else 0


if __name__=='__main__':raise SystemExit(main())
