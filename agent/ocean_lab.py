"""Explicit Blender/Roblox lab imports, bound to a planned isolated experiment."""
import json
from pathlib import Path
import uuid
import hashlib
from agent.lab_store import LabStore,clean_json
from agent.obsidian import safe_path

METRICS=('triangles','objects','materials','dimension_x_m','dimension_y_m','dimension_z_m')


def prepare(root,batch='B3-C1',methods=('B3','C1'),apply=False):
    if not isinstance(batch,str) or not 1<=len(batch)<=100:raise ValueError('invalid lab batch')
    lab=LabStore(root);out=[]
    for method in methods:
        if not isinstance(method,str) or not 1<=len(method)<=40:raise ValueError('invalid method')
        eid=str(uuid.uuid5(uuid.NAMESPACE_URL,'vdn-ocean:'+batch+':'+method))
        spec={'problem':'Comparer géométrie des sapins sous conditions identiques','technique':method,
              'hypothesis':'Comparer les mesures sans supposer un gagnant ni un gain visuel.',
              'parameters':{'method':method,'assets':[]},'environment':{},
              'protocol':{'controls':{'blender_version':None,'unit_scale':None,'measurement_method':None},
                          'inputs_needed':['copie locale des assets '+method,'version Blender','mesures et captures Roblox séparées'],
                          'validation':['Mêmes unités, méthode de comptage et version pour les deux variantes.','Conserver les fichiers et rapports bruts sans écraser les originaux.'],
                          'not_executed':True},'experiment_id':eid}
        r=lab.create(**spec) if apply else {**spec,'id':eid,'status':'PLANNED_PREVIEW'}
        if apply and r['status']=='HYPOTHESIS':r=lab.transition(eid,'PLANNED')
        out.append(r)
    return {'state':'planned' if apply else 'simulation','experiments':out,'assets_present':'not asserted','winner':None}


def import_blender(root,relative,apply=False):
    if not isinstance(relative,str) or not relative.startswith('lab/inbox/'):raise ValueError('stage Blender report in lab/inbox')
    path=safe_path(root,relative)
    if path.stat().st_size>64000:raise ValueError('report too large')
    raw=path.read_bytes();report=json.loads(raw);clean_json(report)
    required={'schema','experiment_id','method','environment','controls','metrics','objects','provenance','observations'}
    if not isinstance(report,dict) or set(report)!=required or report['schema']!='vdn.blender-measurement/11':raise ValueError('invalid Blender report')
    lab=LabStore(root);r=lab.get(report['experiment_id'])
    request_id=str(uuid.uuid5(uuid.UUID(report['experiment_id']),hashlib.sha256(raw).hexdigest()))
    replay=any(e['request_id']==request_id for e in lab._events(report['experiment_id']))
    if r.get('error') or r['status']!='RUNNING' and not replay:raise ValueError('Blender import requires RUNNING experiment')
    if report['method']!=r['parameters'].get('method') or report['environment']!=r['environment'] or report['controls']!=r['protocol'].get('controls'):raise ValueError('Blender identity/conditions mismatch')
    if set(report['metrics'])!=set(METRICS) or not isinstance(report['objects'],list) or len(report['objects'])>1000:raise ValueError('invalid Blender metrics/objects')
    for v in report['metrics'].values():
        if type(v) not in (int,float) or v<0:raise ValueError('invalid finite nonnegative Blender metric')
    if set(report['controls'])!={'blender_version','unit_scale','measurement_method'} or report['controls'].get('unit_scale',0)<=0:raise ValueError('invalid Blender controls')
    c=report['controls']
    if type(c['unit_scale']) not in (int,float) or not isinstance(c['blender_version'],str) or c['blender_version'] in ('','unknown','FILL_MANUALLY') or c['measurement_method']!='evaluated_loop_triangles_v1':raise ValueError('known Blender version and measurement method required')
    if any(type(report['metrics'][k]) is not int for k in ('triangles','objects','materials')):raise ValueError('mesh counts must be integers')
    for obj in report['objects']:
        if not isinstance(obj,dict) or set(obj)!={'name','triangles'} or not isinstance(obj['name'],str) or type(obj['triangles']) is not int or obj['triangles']<0:raise ValueError('invalid per-object measurement')
    if sum(o['triangles'] for o in report['objects'])!=report['metrics']['triangles'] or len(report['objects'])!=report['metrics']['objects']:raise ValueError('inconsistent Blender aggregate')
    if not report['observations'] or not all(isinstance(s,str) for s in report['observations']):raise ValueError('observations required')
    if not apply:return {'state':'simulation','report':report,'verified':False}
    artifact=lab.import_artifact(relative,'external_measurement')
    return lab.record_result(r['id'],'PARTIAL_SUCCESS',report['metrics'],report['observations'],artifacts=[artifact['id']],
                             limits=[report['provenance'],'Geometry import is not a Roblox performance or visual validation.'],request_id=request_id)


def compare(root,first,second):
    lab=LabStore(root);records=[lab.get(first),lab.get(second)]
    reasons=[]
    if any(r.get('error') or not r['results'] for r in records):return {'comparable':False,'reason':'missing experiment/result','winner':None}
    conditions=[r['results'][-1]['conditions'] for r in records]
    if conditions[0]['environment']!=conditions[1]['environment'] or conditions[0]['protocol'].get('controls')!=conditions[1]['protocol'].get('controls'):reasons.append('conditions differ')
    if not all(c['environment'].get(k) is not None for c in conditions for k in ('blender_version','unit_scale','measurement_method')):reasons.append('controls missing')
    metrics=[]
    for key in METRICS:
        a,b=[r['results'][-1]['metrics'].get(key) for r in records]
        metrics.append({'metric':key,'A':a,'B':b,'B_minus_A':b-a if not reasons and a is not None and b is not None else None})
    return {'comparable':not reasons,'reasons':reasons,'metrics':metrics,'winner':None,'truth_verified':False,
            'scope':'Reported geometry metrics only; no FPS or visual quality inferred.'}
