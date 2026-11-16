"""Océan orchestration reuses V10 sessions, quotas, locks, retrieval and ledgers."""
import datetime as dt
import json
from pathlib import Path
import uuid
from agent import budget,models,providers,ocean_plan,ocean_knowledge
from agent.engine import KnowledgeEngine,string
from agent.lab_store import clean_json,identity,lab_lock
from agent.ocean_web import OceanWeb,settings
from agent.obsidian import safe_path
from agent.research_queue import item_key
from agent.research_session import ResearchSessions,config as v10_config
from agent.storage import atomic_write


class Ocean:
    def __init__(self,root):self.root=Path(root).resolve();self.sessions=ResearchSessions(self.root)
    def path(self,gid):return safe_path(self.root,'lab/ocean/goals/'+identity(gid)+'.json')
    def get(self,gid):
        p=self.path(gid)
        if not p.exists():raise ValueError('unknown Ocean goal')
        if p.stat().st_size>64000:raise ValueError('oversized Ocean goal')
        value=json.loads(p.read_text(encoding='utf-8'));clean_json(value)
        if value.get('schema')!='vdn.ocean-goal/11' or value.get('id')!=identity(gid):raise ValueError('invalid Ocean goal identity')
        return value
    def save(self,g):atomic_write(self.path(g['id']),clean_json(g)+'\n')
    def update(self,gid,**values):
        with lab_lock(self.root,'.ocean-control'):
            g=self.get(gid);g.update(values);self.save(g);return g

    def prepare(self,goal,*,apply=False,goal_id=None,provider=None):
        plan=ocean_plan.describe(goal)
        if provider is not None and (provider not in settings(self.root)['providers'] or not settings(self.root)['providers'][provider]['enabled']):raise ValueError('provider not configured/enabled')
        local=ocean_knowledge.cards(self.root)
        ttl=settings(self.root)['cache_ttl_s']
        usable={c['facet']:c for c in local if not set(c['states'])&{'DISPUTED','OUTDATED'} and ocean_knowledge.fresh(self.root,c,ttl)}
        for n in plan['nodes']:
            n['existing_ids']=[usable[n['id']]['id']] if n['id'] in usable else []
            n['gaps']=['project_reproduction_not_verified']+([] if n['existing_ids'] else ['no_Ocean_source_supported_card'])
        if not apply:return {'state':'simulation','plan':plan,'network_requests':0,'writes':0}
        if not plan['nodes']:raise ValueError('no approved technical domain profile; refine the goal or configure a domain')
        gid=identity(goal_id) if goal_id else str(uuid.uuid4())
        with lab_lock(self.root,'.ocean-control'):
            if self.path(gid).exists():
                old=self.get(gid)
                if old['goal']!=goal or old.get('provider')!=provider:raise ValueError('goal id specification conflict')
                return old
            web=OceanWeb(self.root);web.storage_check(64000)
            session=self.sessions.prepare(goal,apply=True,session_id=gid,plan_nodes=plan['nodes'])
            q=self.sessions.queue(session,False);reused=0
            for n in plan['nodes']:
                if n['existing_ids']:
                    item=q.data['items'].get(item_key(n['topic'],n['query']))
                    if item:
                        item.update(status='done',result={'knowledge_available':True,'created':0,'notes':n['existing_ids'],'truth_verified':False,'reason':'reuse source-supported candidate; project test still required'})
                        reused+=1
            q.save()
            g={'schema':'vdn.ocean-goal/11','id':gid,'session_id':gid,'goal':goal,'plan':plan,'control':'READY',
               'status':'READY','created_at':dt.datetime.now(dt.timezone.utc).isoformat(),'model_calls':0,'reserved_cost_usd':0,
               'memory_reused_units':reused,'queries_avoided_lower_bound':reused,'settings':settings(self.root),'provider':provider}
            self.save(g);return g

    def adopt(self,sid,*,apply=False):
        old=self.sessions.get(sid)
        preview={'state':'simulation','session_id':old['id'],'http_calls':old['http_calls'],'ticks':old['ticks'],
                 'migration':'additive envelope only; no session or note rewritten','reversible':'archive envelope; use V10 CLI directly'}
        if not apply:return preview
        with lab_lock(self.root,'.ocean-control'):
            if self.path(sid).exists():return self.get(sid)
            g={'schema':'vdn.ocean-goal/11','id':sid,'session_id':sid,'goal':old['question'],'plan':ocean_plan.describe(old['question']),
               'control':'READY','status':old['status'],'created_at':dt.datetime.now(dt.timezone.utc).isoformat(),
               'model_calls':0,'reserved_cost_usd':0,'memory_reused_units':0,'queries_avoided_lower_bound':0,'settings':settings(self.root),'adopted':True}
            self.save(g);return g

    def control(self,gid,action,*,apply=False):
        if action not in ('pause','resume','stop'):raise ValueError('unknown control action')
        if not apply:return {'state':'simulation','action':action,'goal':self.get(gid)}
        with lab_lock(self.root,'.ocean-control'):
            g=self.get(gid)
            if g['control']=='STOPPED':raise ValueError('stopped goal is terminal; budgets are not reset')
            g['control']={'pause':'PAUSED','resume':'READY','stop':'STOPPED'}[action]
            if action=='resume':g['status']='READY'
            self.save(g)
            return {'state':g['control'],'counters_unchanged':True,'id':gid}

    def list(self):
        folder=safe_path(self.root,'lab/ocean/goals');paths=sorted(folder.glob('*.json')) if folder.exists() else []
        if len(paths)>1000:raise ValueError('goal list limit exceeded')
        out=[]
        for path in paths:
            g=self.get(path.stem);s=self.sessions.get(g['session_id'])
            out.append({'id':g['id'],'goal':g['goal'][:200],'status':s['status'] if s['status']=='RUNNING' else g['status'],'control':g['control'],
                        'http_calls':s['http_calls'],'ticks':s['ticks'],'stop_details':s.get('stop_details'),
                        'model_calls':g['model_calls'],'reserved_cost_usd':g['reserved_cost_usd'],
                        'queries_avoided_lower_bound':g['queries_avoided_lower_bound']})
        return out

    def _model(self,gid,prompt,allowed):
        with lab_lock(self.root,'.ocean-control'):
            g=self.get(gid);cfg=g['settings'];backend=cfg['model_backend']
            if g['control'] in ('PAUSED','STOPPED'):return {'state':'operator_paused'}
            current=settings(self.root)
            if current['model_backend']!=backend:return {'state':'model_configuration_changed'}
            cfg={**cfg,**{k:min(cfg[k],current[k]) for k in ('max_model_calls','max_cost_usd')}}
            if backend=='none' or not allowed:return {'state':'deterministic_only'}
            if backend not in ('local','remote'):raise ValueError('unknown model backend')
            if not v10_config(self.root)['models'][backend]['enabled']:return {'state':'disabled'}
            path=safe_path(self.root,'lab/ocean/model-budget.json')
            day=dt.datetime.now(dt.timezone.utc).date().isoformat()
            daily=json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
            if daily.get('date')!=day:daily={'date':day,'calls':0,'reserved_cost_usd':0}
            amount=cfg['remote_reservation_usd'] if backend=='remote' else 0
            if g['model_calls']>=cfg['max_model_calls'] or daily['calls']>=cfg['max_model_calls']:return {'state':'model_budget_stop'}
            if backend=='remote' and (amount<=0 or g['reserved_cost_usd']+amount>cfg['max_cost_usd'] or daily['reserved_cost_usd']+amount>cfg['max_cost_usd']):return {'state':'cost_budget_stop'}
            g['model_calls']+=1;g['reserved_cost_usd']+=amount;self.save(g)
            daily['calls']+=1;daily['reserved_cost_usd']+=amount;atomic_write(path,clean_json(daily))
        # One bounded model call, never a separate critic-model swarm.
        return models.infer(self.root,prompt,backend)

    def advance(self,gid,*,apply=False,allow_network=False,opener=None):
        g=self.get(gid)
        if not apply:return {'state':'simulation','goal':g,'research':self.sessions.run(g['session_id'])}
        if g['control'] in ('PAUSED','STOPPED'):return {'state':g['control'],'network_requests':0}
        if g['plan']['profile']=='unmapped_goal':raise ValueError('goal needs an approved Ocean domain profile; existing V10 session remains usable')
        web=OceanWeb(self.root,opener)
        for key in ('storage_bytes','max_document_bytes','max_links','sources_per_unit'):web.cfg[key]=min(web.cfg[key],g['settings'][key])
        collector=Collector(self,gid,web,allow_network)
        result=self.sessions.run(g['session_id'],apply=True,allow_network=allow_network,research_fn=collector,followup_fn=collector.followups,collect_existing=True)
        # last_collection describes the last unit only, even if earlier units
        # committed notes before a later failure. Preserve both views.
        tick=result['session']['ticks']
        collections=[i['last_collection'] for i in self.sessions.queue(result['session'],False).data['items'].values()
                     if i.get('last_collection',{}).get('tick')==tick]
        collected={k:sum(c.get(k,0) or 0 for c in collections) for k in ('created','fetched','accepted','rejected','fetch_attempts','error_count')}
        collected['created_note_ids']=list(dict.fromkeys(n for c in collections for n in c.get('created_note_ids',[])))
        collected['scope']='last_executed_tick' if collections else 'no_collection'
        current=self.get(gid)
        final=current['control'] if current['control'] in ('PAUSED','STOPPED') else result['state']
        current=self.update(gid,status=final,last_summary={'state':result['state'],'http_this_tick':result.get('http_this_tick',0),
                                      'cache_hits':web.cache_hits,'http_responses_with_headers':web.successful_responses,'collection':collected})
        return {'state':final,'goal':current,'research':result,'external_game_executed':False}


class Collector:
    def __init__(self,ocean,gid,web,allowed):self.ocean=ocean;self.gid=gid;self.web=web;self.allowed=allowed;self.last_card=None
    def check(self):
        budget.check()
        if self.ocean.get(self.gid)['control'] in ('PAUSED','STOPPED'):raise budget.BudgetExhausted('operator pause/stop',scope='operator',resource='control')
        self.web.storage_check()
    def followups(self,item,refs,stats):
        # Curated alternatives and missing parameters; never append raw page/model instructions.
        f=ocean_plan.facet_for(item['query'])
        if self.last_card and len(self.last_card['documented_tokens'])>=2:return []
        return [{'query':q,'reason':'approved domain follow-up: missing documented parameters or alternative'} for q in f[5]][:2]
    def __call__(self,root,*,planned,max_fetch,**kwargs):
        stats={'created':0,'created_notes':[],'known_notes':[],'errors':[],'fetched':0,'fetch_attempts':0,
               'accepted':0,'rejected':0,'stop_reason':None,'stop_details':None}
        query=planned[0][1];facet=ocean_plan.facet_for(query)[0];goal=self.ocean.get(self.gid)['goal']
        self.last_card=None
        existing=next((c for c in ocean_knowledge.cards(root) if c['facet']==facet and not set(c['states'])&{'DISPUTED','OUTDATED'} and ocean_knowledge.fresh(root,c,self.web.cfg['cache_ttl_s'])),None)
        if existing:
            stats['known_notes']=[{'id':existing['id'],'path':existing['path']}];self.last_card=existing
            self.web.trace('librarian_reused',facet=facet);return stats
        try:
            self.check();self.web.trace('planner_gap',facet=facet)
            provider=self.ocean.get(self.gid).get('provider') or ('blender' if facet=='export' else 'unreal' if facet=='comparison' else 'roblox')
            self.web.trace('researcher_discovery',facet=facet)
            urls=self.web.discover(provider,query)
            docs=[]
            for url in urls:
                self.check()
                if stats['fetch_attempts']>=min(max_fetch,self.web.cfg['sources_per_unit']):break
                budget.fetch_attempt();stats['fetch_attempts']+=1
                try:
                    doc=self.web.get(url,provider);stats['fetched']+=1;self.check()
                    if not ocean_knowledge.excerpts(doc,query):stats['rejected']+=1;continue
                    docs.append(doc);self.web.trace('reader_extracted',url,facet=facet)
                    # First grounded card is committed before attempting another URL/model.
                    prompt=clean_json({'task':'Select literal evidence only; propose questions, never numeric recommendations.',
                                       'goal':goal,'sources':[{'source_id':'source-'+str(i+1),'quote':ocean_knowledge.excerpts(d,query)} for i,d in enumerate(docs)]})
                    card=ocean_knowledge.synthesis(goal,facet,docs)
                    card['related_notes']=[n['id'] for n in KnowledgeEngine(root).search_knowledge(query,3,1000)['results']]
                    self.web.trace('analyst_synthesized',facet=facet,model_state=card['model_state'])
                    self.web.trace('critic_attribution_checked',facet=facet,claims=len(card['claims']),truth_verified=False)
                    result=ocean_knowledge.write_card(root,card,self.web);self.last_card=card
                    if result['action']=='created':stats['created']+=1;stats['created_notes'].append(result)
                    else:stats['known_notes'].append(result)
                    stats['accepted']+=1;self.web.trace('librarian_candidate',facet=facet,note_id=card['id'])
                    self.check()
                    prompt=clean_json({'task':'Source evidence selection and research questions only.',
                                      'evidence':card['claims'],'goal':goal,
                                      'response_schema':{'evidence':[{'source_id':'source-1','quote':'exact provided quote'}],
                                                         'questions':['Question without invented measurements'],
                                                         'proposals':[{'text':'Proposed project step without numeric claims or executable commands','source_ids':['source-1']}]}})
                    model=self.ocean._model(self.gid,prompt,self.allowed)
                    self.web.trace('analyst_model_result',facet=facet,state=model.get('state','unknown'))
                    if model.get('state')=='model_claims':
                        analyzed=ocean_knowledge.synthesis(goal,facet,docs,model)
                        analysis={'card_id':card['id'],'model_state':analyzed['model_state'],'hypotheses':analyzed['hypotheses'],'proposed_steps':analyzed['model_proposed_steps'],
                                  'uncertainties':analyzed['uncertainties'],'truth_verified':False}
                        text=clean_json(analysis);self.web.storage_check(len(text.encode('utf-8')))
                        atomic_write(self.web.path('analyses/'+card['id']+'.json'),text)
                    break # one synthesis/model budget reservation per unit; deeper follow-ups are separate queued work
                except (ValueError,OSError,providers.FetchError) as exc:
                    stats['errors'].append(type(exc).__name__+': source extraction/synthesis failed');self.web.trace('source_rejected',url,reason=type(exc).__name__)
            if not docs and not stats['errors']:stats['errors'].append('No permitted relevant content; inspect web trace and source configuration.')
        except budget.BudgetExhausted as exc:
            stats['stop_reason']=str(exc);stats['stop_details']=exc.details()
        except (ValueError,OSError,KeyError,providers.FetchError) as exc:
            stats['errors'].append(type(exc).__name__+': discovery failed; inspect web trace')
        return stats
