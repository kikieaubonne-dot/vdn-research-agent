"""Gap-only project acquisition using existing V10 sessions and V11 transport."""
import datetime as dt
import json
import uuid
from agent import budget,providers
from agent.engine import string
from agent.intelligence_evidence import digest
from agent.lab_store import identity,lab_lock,clean_json
from agent.ocean_web import OceanWeb
from agent.project_work import Project
from agent.research_session import ResearchSessions
from agent.storage import atomic_write
from agent.text import tokens


class ProjectResearch:
    def __init__(self,root):self.project=Project(root);self.root=self.project.root;self.sessions=ResearchSessions(self.root)
    def path(self,sid):return self.project.path('research/'+identity(sid)+'.json')
    def get(self,sid):
        p=self.path(sid)
        if p.stat().st_size>64000:raise ValueError('project session envelope oversized')
        g=json.loads(p.read_text(encoding='utf-8'));clean_json(g)
        if g.get('schema')!='vdn.project-research/11.2' or g['id']!=identity(sid):raise ValueError('invalid project research envelope')
        return g
    def prepare(self,tasks=None,apply=False,session_id=None):
        bible=self.project.bible;selected=tasks or [t['id'] for t in sorted(bible.tasks.values(),key=lambda t:t['order']) if t['priority'] in ('P0','P1')]
        if not isinstance(selected,list) or not selected or len(selected)>12 or len(set(selected))!=len(selected):raise ValueError('select 1–12 distinct project tasks')
        nodes=[]
        for index,key in enumerate(selected):
            t=bible.task(key)
            support=any(key in other['requires'] and other['priority'] in ('P0','P1') for other in bible.tasks.values())
            if t['priority']=='P3' or t['priority']=='P2' and not support:raise ValueError('P2/P3 deferred until primary preparation is sufficient; do not consume this P0/P1 session')
            nodes.append({'id':key,'topic':t['topic'],'query':t['query'],'priority':100-index,'requires':t['research_requires'],
                          'reason':'explicit initial user research order; production readiness is a separate checklist'})
        preview={'state':'simulation','bible_hash':bible.fingerprint,'tasks':selected,'nodes':nodes,
                 'ordering':'user Phase I initial order; independent acquisition; production dependencies remain in cards',
                 'network_requests':0,'writes':0}
        if not apply:return preview
        sid=identity(session_id) if session_id else str(uuid.uuid4())
        with lab_lock(self.root,'.project-prepare'):
            if self.path(sid).exists():
                old=self.get(sid)
                if old['tasks']!=selected or old['bible_hash']!=bible.fingerprint:raise ValueError('session id specification conflict')
                return old
            state=self.sessions.prepare('Préparation P0/P1 Le Voisin de Noël : '+', '.join(selected),apply=True,session_id=sid,plan_nodes=nodes)
            g={'schema':'vdn.project-research/11.2','id':sid,'tasks':selected,'bible_hash':bible.fingerprint,'control':'READY',
               'created_at':dt.datetime.now(dt.timezone.utc).isoformat(),'session_limits':state['limits']}
            self.project.write(self.path(sid),g,True);return g
    def control(self,sid,action,apply=False):
        if action not in ('pause','resume','stop'):raise ValueError('invalid control action')
        g=self.get(sid)
        if not apply:return {'state':'simulation','action':action,'control':g['control']}
        with lab_lock(self.root,'.project-control'):
            g=self.get(sid)
            if g['control']=='STOPPED':raise ValueError('stopped session is terminal; budgets are preserved')
            g['control']={'pause':'PAUSED','resume':'READY','stop':'STOPPED'}[action]
            self.project.write(self.path(sid),g);return {'state':g['control'],'id':sid,'counters_unchanged':True}
    def run(self,sid,apply=False,allow_network=False,allow_model=False,opener=None):
        g=self.get(sid)
        if not apply:return {'state':'simulation','research':self.sessions.run(sid),'bible_hash':g['bible_hash']}
        if not allow_network:raise PermissionError('project acquisition requires explicit allow_network; use offline task synthesis instead')
        if g['control']!='READY':return {'state':g['control'],'http_calls_this_run':0}
        if self.project.bible.fingerprint!=g['bible_hash']:return {'state':'PROJECT_CHANGED','reason':'prepare an explicitly revised plan; original session/counters preserved','http_calls_this_run':0}
        collector=Collector(self,g,allow_model,opener)
        result=self.sessions.run(sid,apply=True,allow_network=allow_network,research_fn=collector,collect_existing=True,followup_fn=lambda *a:[])
        plan=self.project.plan();ready={n['id']:n['readiness'] for n in plan['nodes']}
        state='PARTIAL' if result['state']=='COMPLETE' and not all(ready[t]=='READY' for t in g['tasks']) else result['state']
        return {'state':state,'acquisition_state':result['state'],'research':result,'preparation':plan,
                'last_tick_cards':collector.cards,'source_errors':collector.errors,'cache_hits':collector.web.cache_hits,
                'scope':'research queue completion is acquisition only, not task READY or engine validation','game_executed':False}


class Collector:
    def __init__(self,owner,envelope,allow_model,opener):
        self.owner=owner;self.project=owner.project;self.envelope=envelope;self.allowed_model=allow_model
        self.web=OceanWeb(owner.root,opener);self.cards=[];self.errors=[]
    def check(self):
        budget.check();g=self.owner.get(self.envelope['id'])
        if g['control']!='READY':raise budget.BudgetExhausted('operator project control',scope='operator',resource='control')
        if self.project.bible.fingerprint!=self.envelope['bible_hash']:raise budget.BudgetExhausted('project revision changed',scope='project',resource='bible_revision')
        self.web.storage_check()
    def __call__(self,root,planned,max_fetch,**kwargs):
        query=planned[0][1];bible=self.project.bible;task=next(t for t in bible.tasks.values() if t['query']==query)
        stats={'created':0,'created_notes':[],'known_notes':[],'fetched':0,'accepted':0,'rejected':0,'fetch_attempts':0,'errors':[]}
        def commit():
            card=self.project.synthesize(task['id'],apply=True,allow_model=self.allowed_model)
            self.cards.append({'task':task['id'],'key':card['key'],'readiness':card['quality']['readiness']})
            item={'id':card['key'],'path':self.project.path('cards/'+card['key']+'.json').relative_to(self.project.root).as_posix()}
            if card['cache_hit']:stats['known_notes'].append(item)
            else:stats['created']+=1;stats['created_notes'].append(item)
            return card
        try:
            self.check();local=self.project.synthesize(task['id'])
            if local['quality']['checks']['original_sources_sufficient'] and 'source_obsolete' not in local['quality']['issues']:
                commit();stats['accepted']+=1;return stats
            candidates=list(task['seeds']);seen=set();limit=min(2,max_fetch)
            while candidates and stats['fetch_attempts']<limit:
                self.check();url=candidates.pop(0)
                if url in seen:continue
                seen.add(url);budget.fetch_attempt();stats['fetch_attempts']+=1
                try:
                    doc=self.web.get(url,task['provider']);stats['fetched']+=1
                    # Durable source cache first, then card, before another URL.
                    card=commit()
                    if card['quality']['checks']['original_sources_sufficient']:stats['accepted']+=1;break
                    stats['rejected']+=1
                    links=sorted(doc['links'],key=lambda u:-len(set(tokens(u))&set(tokens(task['query']))))
                    candidates+=links[:2]
                except (ValueError,OSError,providers.FetchError) as exc:
                    stats['errors'].append(type(exc).__name__+'(status='+str(getattr(exc,'status',None))+'): permitted source unavailable or insufficient')
            if not stats['accepted'] and not stats['errors']:stats['errors'].append('no sufficient compatible original passage; acquisition remains partial')
        except budget.BudgetExhausted as exc:stats.update(stop_reason=str(exc),stop_details=exc.details())
        self.errors+=stats['errors'];return stats
