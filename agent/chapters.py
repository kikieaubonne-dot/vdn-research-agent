"""Bounded chapter anticipation over the existing Bible, evidence and sessions."""
import json,re
from pathlib import Path
from agent.engine import string,integer
from agent.intelligence_evidence import digest,documents,retrieve
from agent.lab_store import clean_json
from agent.obsidian import safe_path
from agent.project import Bible,STATUSES
from agent.project_work import Project,bound_experiments
from agent.project_recipes import recipe
from agent.text import fold


def select_scope(question):
 string(question,'question');q=fold(question);found=[]
 for key,pattern in [('prologue',r'\bprologue\b'),('lobby',r'\blobby\b'),('chapter1',r'\b(?:chapter|chapitre)\s*1\b'),('chapter2',r'\b(?:chapter|chapitre)\s*2\b')]:
  if re.search(pattern,q):found.append(key)
 if len(found)>1:raise ValueError('Sélectionner un seul chapitre pour conserver un objectif borné.')
 return found[0] if found else None


class Chapters:
 def __init__(self,root):
  self.root=Path(root).resolve();self.bible=Bible(root);path=safe_path(self.root,'project/chapters.json')
  if path.stat().st_size>100000:raise ValueError('chapter catalog oversized')
  self.data=json.loads(path.read_text(encoding='utf-8'));clean_json(self.data,100000)
  if self.data.get('schema')!='vdn.chapters/11.2' or not isinstance(self.data['scenes'],list) or not 1<=len(self.data['scenes'])<=40:raise ValueError('invalid chapter catalog')
  self.chapters={};self.scenes={}
  for chapter in self.data['chapters']:
   if not re.fullmatch('[a-z0-9-]{1,64}',chapter['id']) or chapter['id'] in self.chapters or chapter['status'] not in STATUSES:raise ValueError('invalid chapter identity/status')
   self.chapters[chapter['id']]=chapter
  for chapter in self.chapters.values():
   if chapter['next'] is not None and chapter['next'] not in self.chapters:raise ValueError('unknown next chapter')
  for scene in self.data['scenes']:
   if not re.fullmatch('[a-z0-9-]{1,64}',scene['id']) or scene['id'] in self.scenes or scene['chapter'] not in self.chapters or scene['narrative_status'] not in STATUSES:raise ValueError('invalid scene identity/context')
   if len(scene['features'])>12:raise ValueError('scene feature cap')
   for feature in scene['features']:
    self.bible.task(feature['task'])
    if feature['priority'] not in ('P0','P1','P2','P3') or feature['status'] not in STATUSES:raise ValueError('invalid feature priority/status')
   self.scenes[scene['id']]=scene
  self.fingerprint=digest(self.data)
 def resolve(self,value):
  chapter=value if value in self.chapters else select_scope(value)
  if chapter not in self.chapters:raise ValueError('unknown chapter; select prologue, lobby, chapter1 or chapter2')
  return chapter
 def plan(self,chapter):
  key=self.resolve(chapter);next_id=self.chapters[key]['next'];tasks={};scenes=[]
  # Current chapter first, next dependencies second, future watch last.
  for scene in self.scenes.values():
   horizon='A' if scene['chapter']==key else 'B' if scene['chapter']==next_id else 'C'
   scenes.append({**scene,'horizon':horizon})
   for f in scene['features']:
    task=self.bible.task(f['task']);entry=tasks.setdefault(task['id'],{'task':task['id'],'objective':task['objective'],'horizon':horizon,'priority':f['priority'],'scenes':[],'dependencies':task['requires'],'test_status':'NOT_TESTED','next_action':task['next_action']})
    if horizon<entry['horizon']:entry['horizon']=horizon;entry['priority']=f['priority']
    elif horizon==entry['horizon'] and f['priority']<entry['priority']:entry['priority']=f['priority']
    entry['scenes'].append(scene['id'])
  # Include prerequisites even when not a separate scene feature.
  def dependency(task_id,horizon,priority,chain):
   if task_id in chain:raise ValueError('dependency cycle')
   for d in self.bible.task(task_id)['requires']:
    old=tasks.get(d);task=self.bible.task(d)
    if not old:tasks[d]={'task':d,'objective':task['objective'],'horizon':horizon,'priority':priority,'scenes':[],'dependencies':task['requires'],'test_status':'NOT_TESTED','next_action':task['next_action'],'reason':'technical prerequisite; gameplay priority unchanged'}
    elif horizon<old['horizon']:old['horizon']=horizon
    dependency(d,horizon,priority,chain+[task_id])
  for task in list(tasks.values()):dependency(task['task'],task['horizon'],task['priority'],[])
  ordered=sorted(tasks.values(),key=lambda t:(t['horizon'],t['priority'],self.bible.order.index(t['task'])))
  return {'schema':'vdn.chapter-plan/11.2','chapter':self.chapters[key],'chapter_hash':self.fingerprint,'bible_hash':self.bible.fingerprint,'scenes':sorted(scenes,key=lambda s:(s['horizon'],s['id'])),'tasks':ordered,'research_candidates':[t['task'] for t in ordered if t['horizon']=='A' and t['priority'] in ('P0','P1')][:12],
   'open_decisions':self.data['open_decisions'],'deferred':self.data['deferred'],'state':'PARTIAL','network_requests':0,'content_writes':0,'rule':'A deep/current; B prerequisite preparation; C watch only; no automatic queue or engine execution'}
 def prepare(self,chapter,apply=False):
  from agent.project_research import ProjectResearch
  plan=self.plan(chapter)
  return ProjectResearch(self.root).prepare(plan['research_candidates'],apply=apply,chapter_context={'id':plan['chapter']['id'],'fingerprint':self.fingerprint})
 def brief(self,chapter,token_budget=1800):
  integer(token_budget,'token_budget',500,8000);plan=self.plan(chapter);all_docs=documents(self.root);docs=[d for d in all_docs if d['engine']=='Roblox' or d['engine']=='Blender' and d['version']==self.bible.value('blender_version')];rows=[]
  for t in [t for t in plan['tasks'] if t['horizon']=='A'][:12]:
   task=self.bible.task(t['task']);refs=retrieve(task['query'],docs,3,queries=[task['query']],anchors=task['anchors']);records=bound_experiments(self.root,task['id'])
   failures=[r for r in records if r['results'] and r['results'][-1]['status']=='FAILED']
   r=recipe(task)
   rows.append({'task':task['id'],'priority':t['priority'],'objective':task['objective'],'method':r['solution'],'status':'ENGINEERING_PROPOSAL','dependencies':t['dependencies'],
    'source_references':[{'url':p['url'],'document_id':p['document_id'],'passage_id':p['id'],'section':p['section'],'version':p['version'],'original_snapshot':p['independent'],'incomplete':p['incomplete_context']} for p in refs[:2]],
    'source_scope':'retrieval candidates, not a verified justification of the procedure','gaps':['scene-specific evidence and engine/build applicability to verify'],'failed_experiments':[r['id'] for r in failures],'next_action':'Inspecter les conditions de l’échec avant une nouvelle hypothèse.' if failures else task['next_action'],'detail_question':task['id']})
  out={'schema':'vdn.chapter-brief/11.2','chapter':plan['chapter'],'chapter_hash':self.fingerprint,'engine_version_filtered_documents':len(all_docs)-len(docs),'objective':'Préparer les tâches du chapitre, sans confirmer les détails proposés ni exécuter le jeu.','tasks':rows,'omitted_tasks':[],'horizons':{'A':'current chapter research','B':'next chapter dependencies','C':'future watch only'},'state':'PARTIAL','facts':[],'truth_verified':False,'visual_analysis_performed':False,'engine_executed':False,'risk':'sources and engine/build applicability require validation; do not transfer Unreal features directly','rollback':'Restaurer les copies témoins, conserver les preuves et budgets ; aucune publication.','detail':'synthesize_technical for each detail_question; plan_ocean for all scenes and dependencies'}
  if plan['chapter']['id']=='prologue' and safe_path(self.root,'project/prologue.json').exists():
   from agent.prologue import Prologue
   production=Prologue(self.root);out['production_constraints']=production.data['confirmed_constraints'];out['ending_status']='UNKNOWN';out['production_detail_question']='prologue:resources'
  while len(json.dumps(out,ensure_ascii=False))>token_budget*3.6:
   if out['tasks']:out['omitted_tasks'].insert(0,out['tasks'].pop()['task'])
   else:
    out['omitted_tasks']=out['omitted_tasks'][:4];out['detail']='Context budget insufficient; request plan_ocean or a larger budget.';break
  return out
 def pages(self):
  p={}
  for key in self.chapters:
   plan=self.plan(key);scene_lines=['- '+s['id']+' — '+s['objective']+' ('+s['narrative_status']+', '+s['validation']+')' for s in plan['scenes'] if s['horizon']=='A']
   tasks=['- '+t['task']+' — '+t['priority']+' ; dépendances : '+(', '.join(t['dependencies']) or 'aucune imposée') for t in plan['tasks'] if t['horizon']=='A']
   p['knowledge/_VDN-Chapter-'+key+'.md']='# '+self.chapters[key]['title']+'\n\nStatut narratif : '+self.chapters[key]['status']+' ; validation moteur : NON TESTÉE.\n\n## Scènes\n'+'\n'.join(scene_lines)+'\n\n## Préparation\n'+'\n'.join(tasks)+'\n\nPropositions de laboratoire ; résumés exclus du RAG primaire.\n'
  return p
