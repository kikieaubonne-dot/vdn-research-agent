"""Explicit image associations, not automated visual analysis or engine evidence."""
import json
import hashlib
from agent.engine import string
from agent.intelligence_evidence import digest
from agent.lab_store import LabStore
from agent.obsidian import safe_path
from agent import intelligence_models as im


def references(project,task_id):
    project.bible.task(task_id);folder=project.path('visuals/'+task_id)
    paths=sorted(folder.glob('*.json')) if folder.exists() else []
    if len(paths)>3:raise ValueError('at most three visual references per task')
    out=[]
    for p in paths:
        p=project.path('visuals/'+task_id+'/'+p.name)
        if p.stat().st_size>16000:raise ValueError('visual descriptor oversized')
        value=json.loads(p.read_text(encoding='utf-8'))
        if value['key']!=digest(value['descriptor']):raise ValueError('visual descriptor integrity mismatch')
        LabStore(project.root).artifact(value['descriptor']['artifact_id']);out.append(value['descriptor'])
    return out


def link(project,task_id,path,target,keep,avoid,render_version,human_opinion='UNKNOWN',apply=False):
    project.bible.task(task_id)
    for name,value in (('target',target),('render_version',render_version),('human_opinion',human_opinion)):string(value,name,500)
    for values in (keep,avoid):
        if not isinstance(values,list) or len(values)>5 or any(not isinstance(s,str) or not 1<=len(s)<=150 for s in values):raise ValueError('invalid visual criteria')
    if not isinstance(path,str) or not path.startswith('lab/inbox/'):raise ValueError('stage image in lab/inbox')
    p=safe_path(project.root,path)
    if p.stat().st_size>1_000_000 or p.suffix.lower() not in ('.png','.jpg','.jpeg','.webp'):raise ValueError('bounded image input required')
    raw=p.read_bytes()
    if not (raw.startswith(b'\x89PNG\r\n\x1a\n') or raw.startswith(b'\xff\xd8\xff') or raw.startswith(b'RIFF') and raw[8:12]==b'WEBP'):raise ValueError('unrecognized image header')
    if not apply:return {'state':'simulation','bytes':len(raw),'visual_analysis_performed':False,'writes':0}
    def work():
        previous=references(project,task_id)
        all_refs=[r for t in project.bible.tasks for r in references(project,t)]
        checksum=hashlib.sha256(raw).hexdigest()
        value={'task_id':task_id,'artifact_id':checksum+'-external_capture','sha256':checksum,'bytes':len(raw),
               'target':target,'keep':keep,'avoid':avoid,'render_version':render_version,'human_opinion':human_opinion,
               'visual_analysis_performed':False,'engine_feasibility':'UNKNOWN','provenance':'operator supplied reference and opinion'}
        key=digest(value);dest=project.path('visuals/'+task_id+'/'+key+'.json')
        if not dest.exists():
            if len(previous)>=3:raise ValueError('visual reference cap reached; retain existing records')
            if sum(r['bytes'] for r in all_refs)+len(raw)>8_000_000:raise ValueError('project visual attachment storage budget reached')
            from agent.ocean_web import OceanWeb
            OceanWeb(project.root).storage_check(len(json.dumps(value,ensure_ascii=False).encode('utf-8'))+1000)
            LabStore(project.root).import_artifact(path,'external_capture')
            project.write(dest,{'key':key,'descriptor':value},True)
        return {'state':'associated','key':key,'reference':value,'visual_analysis_performed':False}
    return im.operation(project.root,work)
