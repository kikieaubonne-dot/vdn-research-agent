"""Operator-only forest A/B, using existing budgets, experiments and artifacts.

Fixed local script, generated assets only, no public MCP execution permission.
Geometry result is distinct from artistic review and Roblox validation.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import uuid

from agent import budget, intelligence_models as im
from agent.lab_runner import LocalLab
from agent.lab_store import LabStore, identity, clean_json
from agent.obsidian import safe_path
from agent.reliability import BlackBox, checksum, manifest
from agent.storage import atomic_write

SCRIPT=Path(__file__).resolve().parents[1]/'scripts/blender_forest_ab.py'


def specification(version):
    return {'schema':'vdn.forest-ab/1','hypothesis':'Cambered branches increase per-branch vertical extent at equal triangle count; this does not demonstrate aesthetic realism.',
            'controls':{'seed':1549,'blender_version':version,'renderer':'CYCLES_CPU','samples':2,'resolution':256,'threads':1,'camera':[7,-10,4.5],'spot_position':[4,-6,5],'spot_power_W':1200},
            'assets':{'spruce':{'tiers':6,'branches':8,'height_m':4,'radius_m':1.5},'shrub':{'tiers':4,'branches':10,'height_m':2,'radius_m':1.2}},
            'variants':{'A':{'camber_ratio':0},'B':{'camber_ratio':.25}},
            'criteria':['same triangle and branch counts within each asset','B mean branch depth greater than A','separate Blender reload and OBJ reimport preserve triangle counts','four actual captures exist'],
            'classification':'ENGINEERING_PROPOSAL with self-generated assets; ratios are experimental, not optimal Roblox settings',
            'transfer':'shrub fixed before generation, not a protected blind holdout','aesthetic_result':'INCONCLUSIVE until human review','Roblox_result':'BLOCKED; no actual B3/C1 assets or Studio'}


def evaluate(plan,generated,reloaded):
    if generated.get('phase')!='generate' or reloaded.get('phase')!='verify':raise ValueError('missing independent reload phase')
    if any(r.get('blender_version')!=plan['controls']['blender_version'] for r in (generated,reloaded)):raise ValueError('engine version mismatch')
    keys={(a,v) for a in ('spruce','shrub') for v in ('A','B')}
    def keyed(rows):
        if len(rows)!=4 or {(r['asset'],r['variant']) for r in rows}!=keys:raise ValueError('missing or duplicated experiment arm')
        return {(r['asset'],r['variant']):r for r in rows}
    g=keyed(generated['rows']);r=keyed(reloaded['rows']);rows=[]
    for asset in ('spruce','shrub'):
        a=g[asset,'A']['metrics'];b=g[asset,'B']['metrics'];checks={'triangle_budget_equal':a['triangles']==b['triangles'] and a['triangles']>0,'branch_count_equal':a['branch_count']==b['branch_count'] and a['branch_count']>0,'depth_increased':b['mean_branch_depth_m']>a['mean_branch_depth_m']>=0}
        for variant in ('A','B'):
            original=g[asset,variant];repeat=r[asset,variant]
            checks[variant+'_capture']=original.get('capture_exists') is True
            checks[variant+'_roundtrip']=repeat['reopened']['triangles']==repeat['obj_imported']['triangles']==original['metrics']['triangles']
        rows.append({'asset':asset,'conclusion':'PASS' if all(checks.values()) else 'FAIL','checks':checks,'A':a,'B':b})
    return {'geometry_conclusion':'PASS' if all(r['conclusion']=='PASS' for r in rows) else 'FAIL','artistic_conclusion':'INCONCLUSIVE','Roblox_conclusion':'BLOCKED','rows':rows,'scope':'specific geometric hypothesis only; no FPS, GPU, aesthetic winner, B3/C1 or Blender5.2 success inferred'}


def run(root,allow_blender=False):
    if allow_blender is not True:raise PermissionError('explicit local Blender permission required')
    root=Path(root).resolve();binary=shutil.which('blender')
    if not binary:return {'state':'BLOCKED','reason':'Blender unavailable'}
    version=subprocess.run([binary,'--version'],capture_output=True,text=True,encoding='utf-8',timeout=3).stdout.splitlines()[0].removeprefix('Blender ')
    plan=specification(version);job=str(uuid.uuid4());relative='lab/inbox/forest/'+job;out=safe_path(root,relative);out.mkdir(parents=True,exist_ok=False)
    plan.update(script_sha256=checksum(SCRIPT),id=job);atomic_write(out/'spec.json',clean_json(plan))
    protected=manifest(root);lab=LabStore(root);ids=[]
    for asset in ('spruce','shrub'):
        eid=str(uuid.uuid5(uuid.UUID(job),asset));r=lab.create('Branches trop plates : silhouette de végétation enneigée procédurale '+asset,'Branch camber A/B at fixed triangle count',plan['hypothesis'],parameters={'project_task':'trees','research_branch':'forest/spruce','generated_asset':asset},environment={'engine':'Blender','blender_version':version,'asset_ids':['generated-'+asset]},protocol=plan,experiment_id=eid)
        lab.transition(eid,'PLANNED');lab.transition(eid,'RUNNING');ids.append(eid)
    runner=LocalLab(root)
    try:
        # Each phase has its own existing, persistent compute reservation.
        for phase in ('generate','verify'):
            def work():
                if checksum(SCRIPT)!=plan['script_sha256']:raise ValueError('trusted experiment script changed')
                runner.check_storage(2_000_000)
                remaining=budget.CURRENT.get().deadline-time.monotonic();timeout=max(.1,min(18,remaining))
                cmd=[binary,'--background','--factory-startup','--disable-autoexec','--threads','1','--python-exit-code','2','--python',str(SCRIPT),'--','--output',relative,'--phase',phase]
                env=dict(os.environ);env['BLENDER_USER_RESOURCES']=str(out/'blender-user')
                with (out/(phase+'.log')).open('x',encoding='utf-8') as log:
                    p=subprocess.run(cmd,cwd=root,stdout=log,stderr=subprocess.STDOUT,timeout=timeout,shell=False,env=env)
                if p.returncode:raise RuntimeError('Blender '+phase+' failed; retain experiment logs')
                if (out/(phase+'.log')).stat().st_size>128_000:raise ValueError('engine log oversized')
                if not (out/(phase+'.json')).exists():raise ValueError('missing Blender phase output')
            im.operation(root,work)
        generated=json.loads((out/'generate.json').read_text());reloaded=json.loads((out/'verify.json').read_text());result=evaluate(plan,generated,reloaded)
        if manifest(root)!=protected:raise ValueError('protected source changed')
        artifacts=[]
        for p in sorted(out.iterdir()):
            if p.suffix in ('.json','.obj','.png'):artifacts.append(lab.import_artifact(p.relative_to(root).as_posix())['id'])
        for eid,row in zip(ids,result['rows']):
            lab.record_result(eid,'PARTIAL_SUCCESS' if row['conclusion']=='PASS' else 'FAILED',{'A_triangles':row['A']['triangles'],'B_triangles':row['B']['triangles'],'A_branch_depth_m':row['A']['mean_branch_depth_m'],'B_branch_depth_m':row['B']['mean_branch_depth_m']},['Real Blender generation, capture, save, reload, export and independent reimport. Geometry conclusion: '+row['conclusion']],errors=[] if row['conclusion']=='PASS' else ['Preregistered geometric criterion failed'],artifacts=artifacts,limits=[result['scope'],'Human artistic feedback pending; laboratory criteria are proposed, not confirmed user preferences.'])
        result.update(schema='vdn.forest-ab-result/1',job=job,experiments=ids,output=relative,verified=False,protected_unchanged=True)
        atomic_write(out/'conclusion.json',clean_json(result));return result
    except Exception as exc:
        incident=BlackBox(root).incident('forest_lab','procedural_ab',str(exc),'MEDIUM',type(exc).__name__,True)
        for eid in ids:
            if lab.get(eid)['status']=='RUNNING':lab.record_result(eid,'FAILED',{},['Experiment stopped without promotion'],errors=[type(exc).__name__],limits=['No artistic or game success inferred'])
        return {'state':'BLOCKED','incident_id':incident['incident_id'],'job':job,'output':relative,'verified':False}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',required=True,type=Path);p.add_argument('--allow-blender',action='store_true');a=p.parse_args()
    try:
        r=run(a.root,a.allow_blender);print(json.dumps(r,ensure_ascii=False,indent=2));return 2 if r.get('state')=='BLOCKED' or r.get('geometry_conclusion')=='FAIL' else 0
    except (OSError,ValueError,RuntimeError) as exc:print(json.dumps({'state':'BLOCKED','type':type(exc).__name__}));return 2


if __name__=='__main__':raise SystemExit(main())
