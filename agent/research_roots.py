"""Adaptive bounded research roots, gap receipts and existing-session execution."""
import json,re,time,uuid
from pathlib import Path
from agent import budget,providers
from agent.engine import string,integer
from agent.intelligence_evidence import documents,passages,digest,analyze
from agent.lab_store import identity,clean_json,LabStore,lab_lock
from agent.obsidian import safe_path
from agent.ocean_web import OceanWeb,settings
from agent.project import Bible,request_context
from agent.project_work import Project,bound_experiments
from agent.project_quality import failure_applies_to_assets
from agent.project_recipes import recipe
from agent.research_library import Library
from agent.research_session import ResearchSessions
from agent.text import tokens,fold

class Roots:
 def __init__(self,root):
  self.root=Path(root).resolve();self.project=Project(root);p=safe_path(root,'project/research_roots.json')
  if p.stat().st_size>100000:raise ValueError('research catalog oversized')
  self.data=json.loads(p.read_text(encoding='utf-8'));clean_json(self.data,100000);self.nodes={}
  if self.data.get('schema')!='vdn.research-roots/11.2' or not 1<=len(self.data['nodes'])<=64:raise ValueError('invalid research catalog')
  integer(self.data['max_depth'],'max_depth',0,8);integer(self.data['max_nodes'],'max_nodes',1,64)
  for n in self.data['nodes']:
   if not re.fullmatch(r'[a-z0-9-]+(?:/[a-z0-9-]+)*',n['id']) or n['id'] in self.nodes:raise ValueError('invalid/duplicate branch ID')
   self.bible.task(n['task']);string(n['question'],'question');string(n['query'],'query');integer(n['importance'],'importance',1,5)
   if not isinstance(n['required_concepts'],list) or len(n['required_concepts'])>6 or any(not isinstance(g,list) or not g or any(not isinstance(v,str) for v in g) for g in n['required_concepts']):raise ValueError('invalid branch requirements')
   self.nodes[n['id']]=n
  def visit(key,chain):
   if key not in self.nodes or key in chain:raise ValueError('missing dependency or branch cycle')
   n=self.nodes[key]
   for d in ([n['parent']] if n['parent'] else [])+n['dependencies']:visit(d,chain+[key])
  for key in self.nodes:visit(key,[])
  self.fingerprint=digest(self.data)
 @property
 def bible(self):return Bible(self.root)
 def resolve(self,question):
  string(question,'question');q=question.removeprefix('tree:').strip()
  if q in self.nodes:return q
  words=set(tokens(q));rank=[]
  for n in self.nodes.values():
   score=max((len(set(tokens(a))&words)/max(1,len(set(tokens(a)))) for a in n['aliases']),default=0)
   if score:rank.append((score,n['id'].count('/'),n['id']))
  if not rank:raise ValueError('no mapped branch; use a catalog ID')
  # A broad multi-requirement forest question stays a whole tree.
  if any(w in fold(q) for w in ('foret','forest')) and len(words)>7:return 'forest'
  return max(rank)[2]
 def experiments(self,n):
  records=bound_experiments(self.root,n['task'])
  return [r for r in records if (r['parameters'].get('research_branch') or r['protocol'].get('research_branch')) in (None,n['id'])]
 def assess(self,key,docs=None,selected_passages=None):
  n=self.nodes[key];bible=self.bible;docs=documents(self.root) if docs is None else docs;ps=passages(docs) if selected_passages is None else selected_passages;refs=[];original=[]
  for p in ps:
   if p['engine']!='Roblox' and not (p['engine']=='Blender' and p['version']==bible.value('blender_version')):continue
   words=set(tokens(p['text']+' '+p['section']));matched=bool(n['required_concepts']) and all(words&set(tokens(' '.join(g))) for g in n['required_concepts'])
   if not matched or p['hostile'] or p.get('context_only'):continue
   ref={k:p[k] for k in ('id','document_id','url','document_sha256','section','start','end','version','source_type','accessed','published')};ref['version_known']=p['version'] not in ('unknown','UNKNOWN');ref['original']=p['independent'];ref['incomplete']=p['incomplete_context'];refs.append(ref)
   if p['independent'] and not p['incomplete_context'] and not p['hostile'] and p['retrieved_at'] and time.time()-p['retrieved_at']<=settings(self.root)['cache_ttl_s']:original.append(ref)
  records=self.experiments(n);all_failures=[r for r in records if r['results'] and r['results'][-1]['status']=='FAILED'];failures=[r for r in all_failures if failure_applies_to_assets(r,bible.task(n['task']))];reviewed=[r for r in records if (r['parameters'].get('research_branch') or r['protocol'].get('research_branch'))==key and r['status']=='VERIFIED' and r.get('review') and r['environment'].get('engine')=='Roblox' and bible.value('engine_version') not in ('UNKNOWN','unknown') and r['environment'].get('engine_version')==bible.value('engine_version') and set(bible.task(n['task'])['assets'])<=set(r['environment'].get('asset_ids',[]))]
  status='HUMAN_REVIEWED_UNDER_RECORDED_CONDITIONS' if reviewed else 'PARTIAL_SOURCE_CONTEXT' if original else 'CANDIDATE_ONLY' if refs else 'NO_EVIDENCE'
  # Keywords/source context never close the technical gap automatically.
  out={'gap_id':'gap-'+digest(key)[:24],'branch':key,'question':n['question'],'importance':n['importance'],'status':status,'sources':refs[:6],'source_matches':len(refs),'original_context_matches':len(original),'gap_open':not bool(reviewed),'required_concepts':n['required_concepts'],'dependencies':n['dependencies'],'failures':[r['id'] for r in failures],'experiment_revisions':[(r['id'],r['event_sha256']) for r in records],'reviewed_experiments':[r['id'] for r in reviewed],'next_query':n['query'],'test':'use task recipe '+n['task']+'; actual scene/build/assets and controls still required','scope':'mechanical context matching, not semantic entailment or engine validation'}
  out['other_context_failures']=[r['id'] for r in all_failures if r not in failures]
  out['input_fingerprint']=self.input_fingerprint(out,docs)
  p=safe_path(self.root,'lab/ocean/roots/assessments/'+out['input_fingerprint']+'.collection.json')
  out['collection_outcome']=None
  if p.exists():
   if p.stat().st_size>64000:raise ValueError('collection receipt oversized')
   receipt=json.loads(p.read_text(encoding='utf-8'))
   if receipt.get('fingerprint')!=out['input_fingerprint'] or receipt.get('state')!='PARTIAL_CONTEXT':raise ValueError('invalid collection receipt')
   out['collection_outcome']=receipt['state']
  return out
 def input_fingerprint(self,assessment,docs):
  cfg=settings(self.root);now=time.time()
  base={k:v for k,v in assessment.items() if k not in ('input_fingerprint','collection_outcome')}
  return digest([self.fingerprint,self.bible.fingerprint,cfg,base,[(d['id'],d['sha256'],d['version'],d['conditions'],bool(d['retrieved_at'] and now-d['retrieved_at']>cfg['cache_ttl_s'])) for d in docs]])
 def plan(self,question,max_depth=6,max_nodes=24):
  conflict,constraints=request_context(question,self.bible)
  if conflict:return conflict
  key=self.resolve(question);integer(max_depth,'max_depth',0,self.data['max_depth']);integer(max_nodes,'max_nodes',1,self.data['max_nodes']);docs=documents(self.root);ps=passages(docs);rows=[];omitted=[]
  def walk(k,depth):
   if len(rows)>=max_nodes:omitted.append(k);return
   n=self.nodes[k];a=self.assess(k,docs,ps);reason=None
   if a['reviewed_experiments']:reason='reviewed_under_conditions'
   elif a['original_context_matches'] and not a['failures']:reason='source_context_available_prepare_test_not_claim_coverage'
   elif a['collection_outcome'] and not a['failures']:reason='permitted_scope_exhausted_review_partial_evidence'
   elif n['importance']<=2 and not a['failures']:reason='low_priority_watch'
   elif depth>=max_depth:reason='depth_limit'
   rows.append({**a,'depth':depth,'searchable':n['searchable'],'stop_reason':reason,'priority_score':n['importance']*10+(15 if a['failures'] else 0)+(10 if not a['original_context_matches'] else 0),'technique_id':'technique-'+digest(k)[:24]})
   if depth<max_depth and reason!='low_priority_watch':
    for child in sorted((x for x in self.nodes.values() if x['parent']==k),key=lambda x:(-x['importance'],x['id'])):walk(child['id'],depth+1)
  walk(key,0)
  candidates=sorted([r for r in rows if r['searchable'] and r['gap_open'] and r['stop_reason'] not in ('low_priority_watch','source_context_available_prepare_test_not_claim_coverage','permitted_scope_exhausted_review_partial_evidence')],key=lambda r:(-r['priority_score'],-r['depth'],r['branch']))[:6]
  # Dependencies outside a selected subtree stay explicit and are researched
  # before their consumer; a micro-branch never restarts its whole parent tree.
  ordered=[];dependency_gaps={}
  def prerequisite(k):
   if k in ordered:return
   n=self.nodes[k]
   for dep in n['dependencies']:
    a=self.assess(dep,docs,ps);dependency_gaps[dep]=a
    if a['gap_open'] and not a['original_context_matches'] and not a['collection_outcome']:prerequisite(dep)
   if len(ordered)<6:ordered.append(k)
  for row in candidates:prerequisite(row['branch'])
  return {'intent':analyze(question),'request_constraints':constraints,'dependency_gaps':list(dependency_gaps.values()),'schema':'vdn.research-tree/11.2','root':key,'catalog_hash':self.fingerprint,'nodes':rows,'omitted_branches':omitted,'research_candidates':ordered,'max_depth':max_depth,'max_nodes':max_nodes,'network_requests':0,'content_writes':0,'state':'PARTIAL','rule':'conceptual depth is separate from unchanged V10 collection-depth/HTTP limits'}
 def detail(self,key):
  key=self.resolve(key);n=self.nodes[key];docs=documents(self.root);a=self.assess(key,docs);r=recipe(self.bible.task(n['task']));related=Library(self.root).search(n['question'],n)
  analysis=self.project.synthesize(n['task'],include_analysis=True);allowed={s['id'] for s in a['sources']}
  params=[p for p in analysis['documented_parameters'] if set(p['passage_ids'])&allowed]
  if a['failures']:r={**r,'steps':[],'blocked_reason':'inspect linked failed conditions and propose a justified alternative before retry'}
  return {'repeat_blocked':bool(a['failures']),'branch':n,'gap':a,'evidence_passages':[p for p in passages(docs) if p['id'] in allowed],'library':related,'procedure':r,'parameters':params,'parameter_scope':'literal attributed parameters only, no optimal settings inferred','alternatives':r['alternatives'],'known_failures':a['failures'],'other_context_failures':a['other_context_failures'],'related_branches':[x['id'] for x in self.nodes.values() if x['parent']==key]+n['dependencies'],'engine_executed':False,'truth_verified':False}
 def brief(self,question,token_budget=1800):
  integer(token_budget,'token_budget',500,8000);plan=self.plan(question)
  if plan['state']=='CONSTRAINT_CONFLICT':return {**plan,'facts':[]}
  key=plan['root'];rows=[]
  for r in sorted([r for r in plan['nodes'] if r['searchable']],key=lambda r:(-r['priority_score'],r['depth']))[:6]:
   n=self.nodes[r['branch']];found=Library(self.root).search(n['question'],n,3)
   rows.append({'branch':r['branch'],'technique_id':r['technique_id'],'question':r['question'],'gap_status':r['status'],'candidate_method':None if r['failures'] else recipe(self.bible.task(n['task']))['solution'],'failure_action':'Inspect recorded conditions; change one variable or justify a retry' if r['failures'] else None,'alternatives_to_investigate':recipe(self.bible.task(n['task']))['alternatives'][:2],'main':[{'id':h['note_id'],'sources':h['sources']} for h in found['main'][:1]],'reserve':[{'id':h['note_id'],'sources':h['sources']} for h in found['reserve'][:1]],'failures':r['failures'],'next_query':r['next_query']})
  out={'request_constraints':plan['request_constraints'],'context':{'project':'Le Voisin de Noël','target_engine':self.bible.value('engine'),'blender_target':self.bible.value('blender_version'),'scene_assets':self.bible.task(self.nodes[key]['task'])['assets']},'schema':'vdn.research-brief/11.2','root':key,'priority_response':'Comparer une méthode candidate sur copie, puis approfondir uniquement les lacunes.','branches':rows,'omitted_branches':[],'facts':[],'state':'PARTIAL','test':'baseline A, one declared variable B, same asset/build/controller/device and human-approved criteria','rollback':'Restore isolated baseline; retain sources, failures and counters. No production edit.','limits':'References are documentary candidates. No Roblox result, optimal settings or semantic proof inferred.','detail_tool':'synthesize_technical','detail_question':'tree:'+key}
  while len(json.dumps(out,ensure_ascii=False))>token_budget*3.6:
   if out['branches']:out['omitted_branches'].insert(0,out['branches'].pop()['branch'])
   else:out['omitted_branches']=out['omitted_branches'][:3];break
  return out
 def envelope(self,sid):return safe_path(self.root,'lab/ocean/roots/sessions/'+identity(sid)+'.json')
 def prepare(self,question,max_depth=6,max_nodes=24,apply=False,session_id=None):
  plan=self.plan(question,max_depth,max_nodes)
  if plan['state']=='CONSTRAINT_CONFLICT':return plan
  if not apply:return {'state':'simulation','plan':plan,'writes':0}
  if not plan['research_candidates']:return {'state':'NO_RESEARCH_NEEDED','plan':plan,'writes':0,'reason':'prepare a test or inspect stop reasons; no automatic repeated collection'}
  with lab_lock(self.root,'.roots-prepare'):
   sid=identity(session_id) if session_id else str(uuid.uuid4());p=self.envelope(sid)
   if p.exists():
    old=self.get_session(sid)
    if old['root']!=plan['root'] or old['catalog_hash']!=self.fingerprint or old['bible_hash']!=self.bible.fingerprint:raise ValueError('session_id content conflict')
    return old
   nodes=[{'id':k,'query':self.nodes[k]['query'],'topic':self.bible.task(self.nodes[k]['task'])['topic'],'priority':100-i,'requires':[d for d in self.nodes[k]['dependencies'] if d in plan['research_candidates'][:i]],'reason':'specific unresolved branch; not whole forest retry'} for i,k in enumerate(plan['research_candidates'])]
   state=ResearchSessions(self.root).prepare('Bounded research tree '+plan['root'],apply=True,session_id=sid,plan_nodes=nodes)
   g={'schema':'vdn.root-session/11.2','id':sid,'root':plan['root'],'branches':plan['research_candidates'],'catalog_hash':self.fingerprint,'bible_hash':self.bible.fingerprint,'control':'READY'};self.project.write(p,g,True);return g
 def get_session(self,sid):
  p=self.envelope(sid)
  if p.stat().st_size>64000:raise ValueError('tree session oversized')
  g=json.loads(p.read_text(encoding='utf-8'))
  if g.get('schema')!='vdn.root-session/11.2' or g['id']!=identity(sid) or g.get('control') not in ('READY','PAUSED','STOPPED') or not isinstance(g.get('branches'),list) or not 1<=len(g['branches'])<=6 or any(not isinstance(k,str) for k in g['branches']):raise ValueError('invalid tree session')
  return g
 def control(self,sid,action,apply=False):
  if action not in ('pause','resume','stop'):raise ValueError('invalid action')
  g=self.get_session(sid)
  if not apply:return {'state':'simulation','action':action}
  with lab_lock(self.root,'.roots-control'):
   g=self.get_session(sid)
   if g['control']=='STOPPED':raise ValueError('stopped session is terminal')
   g['control']={'pause':'PAUSED','resume':'READY','stop':'STOPPED'}[action];self.project.write(self.envelope(sid),g);return g
 def run(self,sid,apply=False,allow_network=False,opener=None):
  g=self.get_session(sid);sessions=ResearchSessions(self.root)
  if not apply:return sessions.run(sid)
  if not allow_network:raise PermissionError('explicit allow_network required; use offline plan/detail for cache only')
  if g['control']!='READY':return {'state':g['control'],'http_calls_this_run':0}
  if g['catalog_hash']!=self.fingerprint or g['bible_hash']!=self.bible.fingerprint:return {'state':'PROJECT_CHANGED','http_calls_this_run':0}
  collector=RootCollector(self,g,opener);r=sessions.run(sid,apply=True,allow_network=True,research_fn=collector,followup_fn=lambda *a:[],collect_existing=True)
  return {'remaining_gaps':[self.assess(k) for k in g['branches'] if self.assess(k)['gap_open']],'state':'PARTIAL' if r['state']=='COMPLETE' else r['state'],'acquisition_state':r['state'],'research':r,'branch_updates':collector.updated,'errors':collector.errors,'warnings':collector.warnings,'cache_hits':collector.web.cache_hits,'scope':'acquisition terminality never verifies a game technique'}
 def after_failure(self,experiment_id):
  from agent.failure_learning import diagnose
  d=diagnose(self.root,experiment_id);r=LabStore(self.root).get(experiment_id);c=r['results'][-1]['conditions'] if r['results'] else {};explicit=c.get('parameters',{}).get('research_branch') or c.get('protocol',{}).get('research_branch')
  categories=[h['category'] for h in d.get('hypotheses',[])] if d.get('reported_status')=='FAILED' else []
  if d.get('reported_status')!='FAILED':explicit=None
  mapping={'export':'forest/export','collision':'forest/collisions','lighting':'forest/lighting/flashlight','camera':'player/camera','materials':'forest/spruce/foliage/cards/alpha','geometry':'forest/spruce','performance':'forest/performance'}
  selected=list(dict.fromkeys(([explicit] if explicit in self.nodes else [])+[mapping[k] for k in categories if k in mapping]))[:3]
  return {'diagnostic':d,'branches':[{'id':k,'plan':self.plan(k,2,8)} for k in selected],'automatic_actions':[],'whole_forest_restarted':False}
 def pages(self):
  from agent.corpus import scan_notes
  inv=Library(self.root).inventory();notes={n['id']:n for n in scan_notes(self.root)};pages={}
  for tier,ids in inv['tiers'].items():
   links=['- [['+notes[i]['_path'][:-3]+'|'+i+']]' for i in ids]
   pages['knowledge/_VDN-Library-'+tier+'.md']='# '+tier+'\n\nCuration, not independent technical proof.\n\n'+'\n'.join(links)+'\n'
  scenes=[]
  if safe_path(self.root,'project/chapters.json').exists():
   from agent.chapters import Chapters
   scenes=list(Chapters(self.root).scenes.values())
  lines=[]
  for n in self.nodes.values():
   links=['[[_VDN-Chapter-'+s['chapter']+'|'+s['id']+']] ('+s['narrative_status']+')' for s in scenes if any(f['task']==n['task'] for f in s['features'])]
   lines += ['## '+n['id'],n['question'],'', 'Shared technique: `technique-'+digest(n['id'])[:24]+'`; task: '+n['task'], 'Scenes: '+(', '.join(links) or 'UNKNOWN'), 'Detail via MCP: `synthesize_technical(question="tree:'+n['id']+'")`', '']
  pages['knowledge/_VDN-Research-Roots.md']='# Technical research roots\n\nEngineering proposals; never engine validation.\n\n'+ '\n'.join(lines)+'\n'
  return pages

class RootCollector:
 def __init__(self,tree,g,opener):self.tree=tree;self.g=g;self.web=OceanWeb(tree.root,opener);self.updated=[];self.errors=[];self.warnings=[]
 def __call__(self,root,planned,max_fetch,**kwargs):
  query=planned[0][1];key=next(k for k in self.g['branches'] if self.tree.nodes[k]['query']==query);n=self.tree.nodes[key];task=self.tree.bible.task(n['task']);stats={'created':0,'created_notes':[],'known_notes':[],'fetched':0,'accepted':0,'rejected':0,'fetch_attempts':0,'errors':[]}
  def checkpoint():
   a=self.tree.assess(key);fingerprint=a['input_fingerprint']
   p=safe_path(root,'lab/ocean/roots/assessments/'+fingerprint+'.json');existed=p.exists()
   if not existed:self.tree.project.write(p,{'fingerprint':fingerprint,'assessment':a},True);stats['created']+=1
   item={'id':fingerprint,'path':p.relative_to(root).as_posix()};stats['known_notes' if existed else 'created_notes'].append(item);self.updated.append({'branch':key,'fingerprint':fingerprint,'cache_hit':existed,'gap_status':a['status'],'gap_open':a['gap_open'],'collection_outcome':a['collection_outcome']});return a
  current=checkpoint()
  if not current['failures'] and (current['original_context_matches'] or current['collection_outcome']):stats['accepted']=int(bool(current['original_context_matches']));return stats
  candidates=[(c['url'],c['provider']) for c in task.get('source_candidates',[])] or [(u,task['provider']) for u in task['seeds']];seen=set()
  try:
   while candidates and stats['fetch_attempts']<min(2,max_fetch):
    budget.check()
    live=Roots(root)
    if live.fingerprint!=self.g['catalog_hash'] or live.bible.fingerprint!=self.g['bible_hash']:raise budget.BudgetExhausted('project changed during acquisition',scope='project',resource='revision')
    control=self.tree.get_session(self.g['id'])
    if control['control']!='READY':raise budget.BudgetExhausted('operator paused tree',scope='operator',resource='control')
    url,provider=candidates.pop(0)
    if url in seen:continue
    seen.add(url);spec=self.web.cfg['providers'].get(provider)
    if not spec or not spec['enabled']:self.warnings.append('provider not configured/enabled: '+provider);continue
    budget.fetch_attempt();stats['fetch_attempts']+=1
    try:
     doc=self.web.get(url,provider);stats['fetched']+=1;a=checkpoint()
     if a['original_context_matches']:stats['accepted']=1;break
     stats['rejected']+=1;terms=set(tokens(n['query']));links=sorted(doc['links'],key=lambda u:-len(set(tokens(u))&terms));candidates += [(u,provider) for u in links[:2]]
    except (ValueError,OSError,providers.FetchError) as exc:stats['errors'].append(type(exc).__name__+': permitted source unavailable or insufficient')
  except budget.BudgetExhausted as exc:stats.update(stop_reason=str(exc),stop_details=exc.details())
  if not stats['accepted'] and not stats['errors'] and not stats.get('stop_reason') and stats['fetched']:
   # Accessible but insufficient evidence is a partial research result, never
   # an integration failure. Freeze the exhausted allowed scope for reuse.
   a=self.tree.assess(key);fingerprint=a['input_fingerprint'];p=safe_path(root,'lab/ocean/roots/assessments/'+fingerprint+'.collection.json')
   if not p.exists():self.tree.project.write(p,{'fingerprint':fingerprint,'state':'PARTIAL_CONTEXT','attempted_urls':sorted(seen),'automatic_retry':False},True)
   stats['collection_state']='PARTIAL_CONTEXT'
  self.errors+=stats['errors'];return stats
