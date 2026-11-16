"""Bounded resumable local research. Reuses V7 queue, V8 retrieval and transport.

Manual execution is explicit; autonomous/scheduled modes are disabled by default.
No code deployment, production-place execution or Markdown index rewriting.
"""
import datetime as dt
import json
import math
from pathlib import Path
import time
import uuid

from agent import budget,decomposition,planner,gaps,rag
from agent.autonomy import Lock
from agent.engine import KnowledgeEngine,string
from agent.followup_rules import followups_for_note
from agent.lab_store import LabStore,identity,clean_json,lab_lock
from agent.obsidian import safe_path
from agent.research_queue import ResearchQueue,load_config,item_key
from agent.storage import atomic_write


def config(root):
    cfg=json.loads((Path(root)/'config'/'v10.json').read_text(encoding='utf-8'))
    clean_json(cfg)
    keys={'max_depth','max_branches','max_items_per_tick','max_attempts','max_ticks','max_http_calls','http_per_tick','compute_budget_s','time_per_tick_s','stagnation_limit'}
    if set(cfg['research'])!=keys:raise ValueError('invalid research configuration fields')
    for name in ('autonomous_enabled','network_enabled'):
        if type(cfg[name]) is not bool:raise ValueError('invalid V10 activation flag')
    if type(cfg['schedule']['enabled']) is not bool:raise ValueError('invalid schedule flag')
    interval=cfg['schedule']['interval_s']
    if type(interval) is not int or interval<60:raise ValueError('schedule interval must be at least 60s')
    for key,value in cfg['research'].items():
        if type(value) not in (int,float) or not math.isfinite(value) or value<0:raise ValueError('invalid research limit: '+key)
        if not key.endswith('_s') and type(value) is not int:raise ValueError('integer research limit required')
    if not isinstance(cfg['allowed_goals'],list) or not all(isinstance(x,str) for x in cfg['allowed_goals']):raise ValueError('invalid goal allowlist')
    for model in ('local','remote'):
        for flag in ('enabled','vision'):
            if type(cfg['models'][model][flag]) is not bool:raise ValueError('invalid model activation flag')
    return cfg


class ResearchSessions:
    def __init__(self,root):
        self.root=Path(root).resolve()

    def folder(self,sid):return safe_path(self.root,'lab/research/'+identity(sid))
    def session_path(self,sid):return safe_path(self.root,'lab/research/'+identity(sid)+'/session.json')
    def save(self,state):atomic_write(self.session_path(state['id']),clean_json(state)+'\n')
    def get(self,sid):
        path=self.session_path(sid)
        if not path.exists():raise ValueError('unknown session')
        if path.stat().st_size>64000:raise ValueError('oversized session')
        state=json.loads(path.read_text(encoding='utf-8'));clean_json(state)
        if state.get('id')!=identity(sid) or state.get('schema')!='vdn.research-session/10':raise ValueError('invalid session identity')
        for field in ('ticks','http_calls','fetch_attempts','compute_reserved_s','duplicates_avoided'):
            if type(state[field]) not in (int,float) or state[field]<0:raise ValueError('invalid session counter')
        if set(state['limits'])!=set(config(self.root)['research']):raise ValueError('invalid session limits')
        for value in state['limits'].values():
            if type(value) not in (int,float) or value<0:raise ValueError('invalid session limit')
        for key,value in state['limits'].items():
            if not key.endswith('_s') and type(value) is not int:raise ValueError('invalid integer session limit')
        return state

    def queue(self,state,recover=True):
        cfg=load_config(self.root);limits=state['limits']
        cfg['queue'].update(max_depth=limits['max_depth'],max_size=limits['max_branches'],max_attempts=limits['max_attempts'])
        return ResearchQueue(self.root,cfg,recover=recover,state_dir=self.folder(state['id']))

    def prepare(self,question,topic='spruce',*,apply=False,session_id=None):
        string(question,'question');cfg=config(self.root);base=load_config(self.root)
        allowed=ResearchQueue(self.root,recover=False).topics
        if topic not in allowed:raise ValueError('unknown research topic')
        limits={**cfg['research'],'max_depth':min(cfg['research']['max_depth'],base['queue']['max_depth']),
                'max_branches':min(cfg['research']['max_branches'],base['queue']['max_size'])}
        nodes=decomposition.describe(self.root,question)['nodes']
        if nodes and limits['max_depth']==0:nodes=[]
        if len(nodes)>base['queue']['max_plan_nodes']:raise ValueError('decomposition exceeds global plan budget')
        if len(nodes)+1>limits['max_branches']:raise ValueError('decomposition exceeds branch budget')
        preview={'question':question,'topic':topic,'nodes':nodes,'limits':limits,'network_requests':0}
        if not apply:return {'state':'simulation',**preview}
        sid=identity(session_id) if session_id else str(uuid.uuid4())
        with lab_lock(self.root,'.research-control'):
            path=self.session_path(sid)
            if path.exists():
                old=self.get(sid)
                if old['question']!=question or old['topic']!=topic:raise ValueError('session_id content conflict')
                return old
            state={'schema':'vdn.research-session/10','id':sid,'question':question,'topic':topic,'limits':limits,
                   'status':'READY','ticks':0,'http_calls':0,'fetch_attempts':0,'compute_reserved_s':0,
                   'attempts':{},'duplicates_avoided':0,'decisions':[],'integration_failures':0,'failures':[]}
            q=self.queue(state)
            ok,why=q.add(topic,question,allowed[topic].get('priority',5),origin='v10_question')
            if not ok:raise ValueError(why)
            parent=q.data['items'][item_key(topic,question)]
            if nodes:
                parent['status']='skipped';keys={}
                for n in nodes:
                    deps=[keys[d] for d in n.get('requires',[])]
                    target=q.best_topic(n['query'],topic)
                    ok,why=q.add(target,n['query'],parent['priority'],origin='decomposition',depth=1,parent=parent['key'],reason=n['reason'],dependencies=deps)
                    if not ok:raise ValueError(why)
                    keys[n['id']]=item_key(target,n['query'])
            q.save();self.save(state)
            return state

    def run(self,sid,*,apply=False,allow_network=False,provs=None,research_fn=None):
        state=self.get(sid)
        if not apply:return {'state':'simulation','session':state,'queue':self.queue(state,False).summary()}
        cfg=config(self.root);limits=state['limits']
        if type(allow_network) is not bool or allow_network and not cfg['network_enabled']:raise PermissionError('network is disabled in V10 configuration')
        for name in ('vdn.guard','vdn.lock','queue.json','queue_history.jsonl'):safe_path(self.root,'output/'+name)
        with Lock(self.root,7200):
            state=self.get(sid)
            limits={k:min(v,cfg['research'][k]) for k,v in state['limits'].items()}
            base=load_config(self.root)
            for key in ('max_depth','max_attempts'):limits[key]=min(limits[key],base['queue'][key])
            limits['max_branches']=min(limits['max_branches'],base['queue']['max_size'])
            state['limits']=limits;q=self.queue(state);daily_q=ResearchQueue(self.root,recover=False);daily=daily_q.daily()
            for field in ('stop_reason','stop_details','error'):state.pop(field,None)
            for item in q.data['items'].values():
                if item['depth']>limits['max_depth'] and item['status'] in ('pending','running'):
                    item['status']='skipped';item['reason']='depth budget reduced by operator'
            q.save() # also persist recovery of legacy/crash-left running items on early exit

            def record_stop(exc):
                details=exc.details()
                if details['scope']=='session' and details['resource']=='http_calls':
                    details.update(limit=limits['max_http_calls'],used=state['http_calls'])
                if details['scope']=='session' and details['resource']=='compute_s':
                    details.update(limit=limits['compute_budget_s'],used=state['compute_reserved_s'])
                details['resume_policy']={'tick':'new_tick_with_remaining_session_budgets',
                                          'session':'session_limit_reached_no_automatic_reset',
                                          'daily':'wait_for_next_UTC_day_or_run_without_network'}.get(details['scope'],'inspect_stop_reason')
                if details['scope']=='daily' and details['resource']=='items':details['resume_policy']='wait_for_next_UTC_day'
                state.update(status='BUDGET_STOP',stop_reason=str(exc),stop_details=details)

            if state['status']=='COMPLETE':
                self.save(state);q.save()
                return {'state':'COMPLETE','reason':'terminal','session':state,'queue':q.summary()}
            if state['ticks']>=limits['max_ticks']:
                record_stop(budget.BudgetExhausted('session tick limit reached',scope='session',resource='ticks',limit=limits['max_ticks'],used=state['ticks']))
                self.save(state)
                return {'state':'stopped','reason':'max_ticks','session':state,'queue':q.summary(),'stop_details':state['stop_details']}
            remaining=limits['compute_budget_s']-state['compute_reserved_s']
            if remaining<=0:
                record_stop(budget.BudgetExhausted('session compute budget reached',scope='session',resource='compute_s',limit=limits['compute_budget_s'],used=state['compute_reserved_s']))
                self.save(state)
                return {'state':'stopped','reason':'compute_budget','session':state,'queue':q.summary(),'stop_details':state['stop_details']}
            # A refused request must not consume another unit attempt or tick.
            preflight=[]
            if allow_network:
                preflight=[('session','http_calls',limits['max_http_calls'],state['http_calls']),
                           ('tick','http_calls',limits['http_per_tick'],0),
                           ('daily','http_calls',base['daily']['max_http_calls'],daily['http_calls']),
                           ('daily','fetch_attempts',base['daily']['max_fetch'],daily['fetch'])]
            for scope,resource,maximum,used_count in preflight:
                if used_count>=maximum:
                    record_stop(budget.BudgetExhausted('budget '+scope+' '+resource+' atteint',scope=scope,resource=resource,limit=maximum,used=used_count))
                    self.save(state)
                    return {'state':'BUDGET_STOP','session':state,'queue':q.summary(),'http_this_tick':0,'stop_details':state['stop_details']}
            reserve=min(remaining,limits['time_per_tick_s'])
            # Reserve computation before effects; a hard crash keeps a conservative reservation.
            state['compute_reserved_s']+=reserve;state['ticks']+=1;state['status']='RUNNING';self.save(state)
            start=time.monotonic();used=set();engine=KnowledgeEngine(self.root);active=None
            http_before=state['http_calls'];fetch_before=state['fetch_attempts']

            def settle_active(reason):
                if active is not None and active['status']=='running':
                    attempts=state['attempts'].get(active['key'],0)
                    active.update(status='pending' if attempts<limits['max_attempts'] else 'failed',
                                  attempts=max(active.get('attempts',0),attempts),last_stop=reason)
                    q.save();q.log('controlled_stop',{'key':active['key'],'status':active['status'],'reason':reason})

            def checkpoint(resource):
                field='http_calls' if resource=='http_calls' else 'fetch_attempts'
                global_field='http_calls' if resource=='http_calls' else 'fetch'
                maximum=load_config(self.root)['daily']['max_http_calls' if resource=='http_calls' else 'max_fetch']
                if daily[global_field]>=maximum:raise budget.BudgetExhausted('daily quota',scope='daily',resource=field,limit=maximum,used=daily[global_field])
                if field=='http_calls' and state[field]>=limits['max_http_calls']:raise budget.BudgetExhausted('session HTTP budget',scope='session',resource=field,limit=limits['max_http_calls'],used=state[field])
                state[field]+=1;self.save(state) # persist local reservation first, then global, before network
                daily[global_field]+=1;daily_q.save()
            http_remaining=max(0,limits['max_http_calls']-state['http_calls'])
            guard=budget.Budget(reserve,min(limits['http_per_tick'],http_remaining) if allow_network else 0,checkpoint,
                                http_scope='session' if http_remaining<=limits['http_per_tick'] else 'tick',
                                time_scope='session' if remaining<=limits['time_per_tick_s'] else 'tick')
            try:
                with budget.using(guard):
                    for _ in range(min(limits['max_items_per_tick'],load_config(self.root)['cycle']['max_items'])):
                        guard.check()
                        batch=[i for i in q.next_batch(limits['max_branches']) if i['key'] not in used]
                        if not batch:state['status']='BLOCKED' if q.pending_count() else 'COMPLETE';break
                        item=batch[0];used.add(item['key'])
                        if daily['items']>=load_config(self.root)['daily']['max_items']:raise budget.BudgetExhausted('daily item budget',scope='daily',resource='items',limit=base['daily']['max_items'],used=daily['items'])
                        attempt=state['attempts'].get(item['key'],0)
                        if attempt>=limits['max_attempts']:
                            item['status']='failed';q.save();continue
                        state['attempts'][item['key']]=attempt+1;self.save(state)
                        daily['items']+=1;daily_q.save();active=item;q.mark_running(item)
                        found=engine.find_procedures(item['query'],3)
                        guard.check()
                        refs=[p for p in found['procedures'] if p['candidate_steps'] and p['ranking']['coverage']==1 and p['compatibility']['scope']!='other_engine']
                        stats={'created':0,'created_notes':[],'errors':[]}
                        if not refs and allow_network:
                            from agent.run import research
                            fn=research_fn or research
                            stats=fn(self.root,max_queries=1,per_source=2,max_fetch=min(4,load_config(self.root)['daily']['max_fetch']-daily['fetch']),
                                     pause=.5,provs=provs,planned=[(q.topics[item['topic']],item['query'],'v10')],finalize=False,touch_existing=False)
                            collection={'tick':state['ticks'],'item_key':item['key'],
                                **{k:stats.get(k,0) for k in ('created','fetched','accepted','rejected','fetch_attempts')},
                                'error_count':len(stats.get('errors',[])), 'errors':[str(e)[:250] for e in stats.get('errors',[])[:5]],
                                'created_note_ids':[n['id'] for n in stats.get('created_notes',[])[:10]],'truth_verified':False}
                            clean_json(collection)
                            state['last_collection']=collection;item['last_collection']=collection
                            if stats.get('stop_reason'):
                                d=stats.get('stop_details') or {}
                                raise budget.BudgetExhausted(stats['stop_reason'],**{k:d[k] for k in ('scope','resource','limit','used') if k in d})
                            if stats.get('errors'):raise ValueError('research source error; inspect last_collection.errors')
                            if stats.get('created'):
                                refs=[p for p in engine.find_procedures(item['query'],3)['procedures'] if p['candidate_steps'] and p['ranking']['coverage']==1 and p['compatibility']['scope']!='other_engine']
                        parent=q.data['items'].get(item.get('parent'),{})
                        stagnant=0 if stats.get('created') else (parent.get('result') or {}).get('stagnation',0)+1
                        children=[]
                        if item['depth']<limits['max_depth'] and stagnant<limits['stagnation_limit']:
                            proposals=[]
                            for ref in refs:
                                note=engine.get_knowledge(ref['note_id'])
                                proposals+=followups_for_note(self.root/note['path'],item['query'],2)
                            if not refs:proposals=[{'query':planner.short(item['query'],3)+' tutorial','reason':'no attributed actionable evidence for this branch'}]
                            for proposal in proposals[:2]:
                                if len(q.data['items'])>=limits['max_branches']:break
                                target=q.best_topic(proposal['query'],item['topic'])
                                ok,why=q.add(target,proposal['query'],item['priority']-.5,origin='v10_gap',depth=item['depth']+1,parent=item['key'],reason=proposal['reason'])
                                if ok:children.append(proposal['query'])
                                else:state['duplicates_avoided']+=int('doublon' in why)
                        result={'created':stats.get('created',0),'knowledge_available':bool(refs),'notes':[p['note_id'] for p in refs],
                                'stagnation':stagnant,'children':children,'truth_verified':False}
                        q.mark_done(item,result)
                        state['decisions'].append({'query':item['query'],'depth':item['depth'],'result':result})
                        state['decisions']=state['decisions'][-64:];self.save(state)
                    if state['status']=='RUNNING':state['status']='READY' if q.pending_count() else 'COMPLETE'
            except budget.BudgetExhausted as exc:
                record_stop(exc);settle_active(state['stop_details'])
            except Exception as exc:
                state['status']='ERROR';state['error']=f'{type(exc).__name__}: {exc}'[:250]
                state['integration_failures']=state.get('integration_failures',0)+1
                state['failures']=(state.get('failures',[])+[{'tick':state['ticks'],'error':state['error'],'at':dt.datetime.now(dt.timezone.utc).isoformat()}])[-64:]
                settle_active({'kind':'collection_or_local_error','reason':state['error']})
            finally:
                elapsed=time.monotonic()-start
                state['compute_reserved_s']-=max(0,reserve-min(reserve,elapsed))
                state['last_tick']={'tick':state['ticks'],'http_calls':state['http_calls']-http_before,
                                    'fetch_attempts':state['fetch_attempts']-fetch_before,'effective_http_limit':guard.max_http,
                                    'session_http_limit':limits['max_http_calls'],
                                    'session_http_remaining':max(0,limits['max_http_calls']-state['http_calls']),
                                    'daily':{k:daily[k] for k in ('date','http_calls','fetch','items')}}
                self.save(state);q.save()
            return {'state':state['status'],'session':state,'queue':q.summary(),'http_this_tick':guard.http_calls,
                    **({'stop_details':state['stop_details']} if 'stop_details' in state else {})}

    def tick(self,mode='autonomous',*,apply=False,allow_network=False):
        if mode not in ('autonomous','scheduled'):raise ValueError('invalid automatic mode')
        cfg=config(self.root)
        if not apply:return {'state':'simulation','mode':mode,'autonomous_enabled':cfg['autonomous_enabled'],'network_requests':0}
        if not cfg['autonomous_enabled'] or mode=='scheduled' and not cfg['schedule']['enabled']:
            return {'state':'disabled','network_requests':0}
        runtime=safe_path(self.root,'lab/automation/runtime.json')
        with lab_lock(self.root,'.tick-control'):
            state=json.loads(runtime.read_text()) if runtime.exists() else {'last_tick':0,'goals':{}}
            current=time.time()
            if mode=='scheduled' and current-state['last_tick']<cfg['schedule']['interval_s']:return {'state':'not_due','network_requests':0}
            state['last_tick']=current;atomic_write(runtime,clean_json(state)+'\n')
            allowed=[g for g in gaps.inventory(self.root)['tasks'] if g['id'] in cfg['allowed_goals']]
            goal=next((g for g in allowed if state['goals'].get(g['id'],{}).get('state') not in ('COMPLETE','BLOCKED','ERROR','BUDGET_STOP')),None)
            if goal is None:return {'state':'no_allowed_work','network_requests':0}
            old=state['goals'].get(goal['id'])
            if old:sid=old['session_id']
            else:
                topics=ResearchQueue(self.root,recover=False)
                topic=topics.best_topic(goal['query'],next(iter(topics.topics)))
                sid=str(uuid.uuid4());self.prepare(goal['query'],topic,apply=True,session_id=sid)
                state['goals'][goal['id']]={'session_id':sid,'state':'READY'};atomic_write(runtime,clean_json(state)+'\n')
            result=self.run(sid,apply=True,allow_network=allow_network)
            state['goals'][goal['id']]['state']=result['state'];atomic_write(runtime,clean_json(state)+'\n')
            expid=str(uuid.uuid5(uuid.UUID(sid),'experiment'))
            lab=LabStore(self.root)
            experiment=lab.get(expid)
            if experiment.get('error'):
                experiment=lab.create(goal['need'],goal['query'],'Tester une procédure candidate dans un environnement isolé.',
                                      references=goal['references'][:10],protocol={'validation':goal['validation'],'not_executed':True},experiment_id=expid)
            if experiment['status']=='HYPOTHESIS':experiment=lab.transition(expid,'PLANNED')
            return {'state':result['state'],'goal':goal['id'],'research':result,'planned_experiment_id':experiment['id'],'game_executed':False}
