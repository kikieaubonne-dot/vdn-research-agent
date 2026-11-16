"""Operator/Claude description fallback; no claimed multimodal observation."""
import json
import datetime as dt
from agent.engine import string
from agent.intelligence_evidence import digest
from agent.lab_store import clean_json
from agent.project_visual import references
from agent.text import tokens
from agent import intelligence_models as im

def descriptions(project,task_id):
 project.bible.task(task_id);folder=project.path('visual-descriptions/'+task_id);paths=sorted(folder.glob('*.json')) if folder.exists() else []
 if len(paths)>8:raise ValueError('visual description revision cap reached')
 out=[]
 for p in paths:
  p=project.path('visual-descriptions/'+task_id+'/'+p.name)
  if p.stat().st_size>16000:raise ValueError('visual description oversized')
  r=json.loads(p.read_text(encoding='utf-8'))
  if r['hash']!=digest(r['description']):raise ValueError('visual description integrity mismatch')
  out.append(r)
 return sorted(out,key=lambda r:r.get('created_at',''))

def describe(project,task_id,data,apply=False):
 if type(apply) is not bool:raise ValueError('explicit apply boolean required')
 project.bible.task(task_id);clean_json(data,8000)
 required={'description','observed','inferred','unknown','keep','avoid','reference_hashes','provenance'}
 if not isinstance(data,dict) or set(data)!=required or data['provenance'] not in ('operator_description','claude_description'):raise ValueError('explicit description provenance and structured fields required')
 string(data['description'],'description',1500)
 for key in ('observed','inferred','unknown','keep','avoid'):
  if not isinstance(data[key],list) or len(data[key])>8 or any(not isinstance(s,str) or not 1<=len(s)<=200 for s in data[key]):raise ValueError('invalid description list')
 known={r['sha256'] for r in references(project,task_id)}
 if not isinstance(data['reference_hashes'],list) or len(data['reference_hashes'])>3 or not set(data['reference_hashes'])<=known:raise ValueError('unknown image association; description alone remains allowed with empty references')
 words=set(tokens(data['description']+' '+' '.join(data['observed'])));matches=[]
 for task in project.bible.tasks.values():
  candidates=set(tokens(' '.join(task['aliases']+task['anchors'])))
  if words&candidates:matches.append(task)
 matches.sort(key=lambda t:(t['priority'],t['order']))
 value={**data,'task_id':task_id,'bible_hash':project.bible.fingerprint,'visual_analysis_performed':False,'observation_scope':'reported description, not independently observed image','inference_status':'HYPOTHESIS','candidate_tasks':[t['id'] for t in matches[:6]],'network_requests':0,'engine_executed':False,'next_action':'Inspect candidate sources, then explicitly prepare a bounded research session or isolated test.'}
 key=digest(value);path=project.path('visual-descriptions/'+task_id+'/'+key+'.json')
 if apply:
  def work():
   existing=descriptions(project,task_id)
   if not path.exists():
    if len(existing)>=8:raise ValueError('visual description cap reached; retain previous revisions')
    project.write(path,{'hash':key,'description':value,'created_at':dt.datetime.now(dt.timezone.utc).isoformat()},True)
   return {'state':'stored','hash':key,'description':value}
  return im.operation(project.root,work)
 return {'state':'simulation','hash':key,'description':value,'content_writes':0}
