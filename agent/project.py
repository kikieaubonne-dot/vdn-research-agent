"""Human project truth, task identity and dependency-aware research priorities."""
import datetime as dt
import json
from pathlib import Path
import re
from agent.intelligence_evidence import digest
from agent.engine import string
from agent.lab_store import clean_json
from agent.obsidian import safe_path
from agent.text import fold,tokens
from agent.research_session import config
from agent.research_queue import load_config

STATUSES={'CONFIRMED','PROTOTYPE','PROPOSED','UNKNOWN','DEFERRED'}
PRIORITIES={'P0':0,'P1':1,'P2':2,'P3':3}


def request_context(question,bible):
    from agent.intelligence_evidence import analyze
    versions=analyze(question)['versions'];known=bible.value('blender_version')
    conflict=None
    if versions.get('Blender') and versions['Blender']!=known:
        conflict={'state':'CONSTRAINT_CONFLICT','requested_version':versions['Blender'],'project_version':known,
                  'question':'S’agit-il d’une comparaison de versions ou d’un changement humainement validé de la cible du projet ?',
                  'writes':0,'network_requests':0}
    extra_versions={k:v for k,v in versions.items() if k!='Blender' or v!=known}
    numbers=[n for n in re.findall(r'(?<![A-Za-z0-9])\d+(?:\.\d+)?',question) if n not in versions.values()]
    avoid=re.findall(r'(?i)(?:éviter|avoid|sans)\s+([^.!?]{1,160})',question)
    constraints={'versions':extra_versions,'numbers_from_user':numbers,'avoid_from_user':avoid,'status':'PROPOSED'} if extra_versions or numbers or avoid else {}
    return conflict,constraints


class Bible:
    def __init__(self,root):
        self.root=Path(root).resolve();path=safe_path(self.root,'project/bible.json')
        if path.stat().st_size>200000:raise ValueError('project Bible oversized')
        self.data=json.loads(path.read_text(encoding='utf-8'));clean_json(self.data,200000)
        if self.data.get('schema')!='vdn.project-bible/11.2' or type(self.data['revision']) is not int:raise ValueError('invalid project Bible schema/revision')
        self.tasks={};seen=set()
        for group in ('items','questions','tasks','visual_references','deferred','groups'):
            if not isinstance(self.data[group],list) or len(self.data[group])>100:raise ValueError('invalid project list')
            for item in self.data[group]:
                if item['status'] not in STATUSES or not re.fullmatch(r'[a-z0-9-]{1,64}',item['id']):raise ValueError('invalid project item identity/status')
                key=(group,item['id'])
                if key in seen:raise ValueError('duplicate project identity')
                seen.add(key)
        questions={q['id'] for q in self.data['questions']}
        for q in self.data['questions']:
            if q['status']=='CONFIRMED' and (not isinstance(q['answer'],str) or not q['answer'].strip()):raise ValueError('confirmed question needs a human answer')
        for field in self.data['technical'].values():
            if field['status'] not in STATUSES:raise ValueError('technical constraint status missing')
        for t in self.data['tasks']:
            if t['priority'] not in PRIORITIES or t['priority_status'] not in STATUSES:raise ValueError('invalid proposed priority')
            if not set(t['blocking_questions'])<=questions:raise ValueError('unknown blocking question')
            if not t['query'] or not t['anchors'] or not t['seeds']:raise ValueError('research question, anchors and permitted source seeds required')
            candidates=t.get('source_candidates',[])
            if not isinstance(candidates,list) or len(candidates)>4 or any(not isinstance(c,dict) or set(c)!={'url','provider','role'} or any(not isinstance(v,str) or not 1<=len(v)<=500 for v in c.values()) for c in candidates):raise ValueError('invalid bounded source candidates')
            self.tasks[t['id']]=t
        if any(t['parent'] not in {g['id'] for g in self.data['groups']} for t in self.tasks.values()):raise ValueError('unknown knowledge-tree parent')
        self.order=self._topological()
        self.fingerprint=digest(self.data)
    def _topological(self):
        out=[];visiting=set();visited=set()
        def visit(key):
            if key not in self.tasks:raise ValueError('unknown project dependency')
            if key in visiting:raise ValueError('project dependency cycle')
            if key in visited:return
            visiting.add(key)
            for child in self.tasks[key]['requires']+self.tasks[key]['research_requires']:visit(child)
            visiting.remove(key);visited.add(key);out.append(key)
        for key in sorted(self.tasks,key=lambda k:(self.tasks[k]['order'],k)):visit(key)
        return out
    def value(self,key):return self.data['technical'][key]['value']
    def task(self,key):
        if key not in self.tasks:raise ValueError('unknown project task')
        return self.tasks[key]
    def questions(self,task):
        by_id={q['id']:q for q in self.data['questions']}
        return [by_id[k] for k in task['blocking_questions'] if by_id[k]['status']!='CONFIRMED']
    def match(self,question):
        string(question,'question');q=fold(question)
        if question in self.tasks:return {'state':'matched','task':question,'method':'stable_identity'}
        ranked=[];words=set(tokens(question))
        generic={'sapin','epicea','nuit','branche','deplacement'}
        for key,t in self.tasks.items():
            aliases={tuple(tokens(alias)) for alias in t['aliases']}
            score=sum(1 if set(alias)<=generic else 4 for alias in aliases if alias and set(alias)<=words)
            if score:ranked.append((score,key))
        # Distinct specific problems must not collapse merely on shared words.
        if 'camera' in q and {k for s,k in ranked}<={'camera','collisions','trees'}:
            ranked=[(s+4 if k=='camera' else s,k) for s,k in ranked]
        ranked.sort(key=lambda x:(-x[0],x[1]))
        if not ranked:return {'state':'out_of_scope','tasks':[],'question':'Préciser une tâche du jeu ; aucune nouvelle fonctionnalité narrative n’est ajoutée.'}
        if len(ranked)>1 and ranked[0][0]==ranked[1][0]:return {'state':'ambiguous','tasks':[k for s,k in ranked if s==ranked[0][0]],'question':'Quel problème précis faut-il traiter parmi ces tâches ?'}
        return {'state':'matched','task':ranked[0][1],'method':'explicit_project_aliases'}
    def context(self,task):
        return {'schema':'vdn.project-context/11.2','bible_hash':self.fingerprint,'revision':self.data['revision'],
            'project':'Le Voisin de Noël [Horreur]','task_id':task['id'],'target_engine':self.value('engine'),
            'blender_target':self.value('blender_version'),'device_target':self.value('target_devices'),'fps_target':self.value('fps_target'),
            'vision':'Première personne, horreur cinématographique, nuit de Noël enneigée.',
            'avoid':['transfert direct Unreal vers Roblox','paramètres optimaux inventés','décisions narratives inventées','publication du jeu'],
            'unresolved_questions':[q['text'] for q in self.questions(task)],
            'retrieval_queries':[task['query']],'retrieval_anchors':task['anchors']}
    def plan(self):
        effective={k:PRIORITIES[t['priority']] for k,t in self.tasks.items()}
        def propagate(key,priority):
            for dep in self.tasks[key]['requires']:
                if effective[dep]>priority:effective[dep]=priority;propagate(dep,priority)
        for key in self.tasks:propagate(key,effective[key])
        rank={k:i for i,k in enumerate(self.order)}
        ordered=sorted(self.tasks,key=lambda k:(effective[k],rank[k]))
        return {'schema':'vdn.project-plan/11.2','bible_hash':self.fingerprint,'priority_status':'PROPOSED',
                'nodes':[{**self.tasks[k],'effective_research_priority':'P'+str(effective[k]),
                          'priority_reason':'technical prerequisite inherits urgency; gameplay priority unchanged' if effective[k]<PRIORITIES[self.tasks[k]['priority']] else 'proposed game research priority',
                          'production_dependencies':self.tasks[k]['requires'],'research_dependencies':self.tasks[k]['research_requires'],
                          'readiness':'UNKNOWN','sources_available':'inspect task card','gaps':['assets/versions/measurements require inspection'],
                          'last_research':None} for k in ordered],
                'network_requests':0,'writes':0,'scope':'research priority is separate from implementation readiness'}
    def markdown(self):
        lines=['# Bible — Le Voisin de Noël [Horreur]','',
               'Source : contexte utilisateur V11.2. CONFIRMED décrit une intention rapportée, pas un test moteur.',
               'Révision : '+str(self.data['revision'])+' ; empreinte : `'+self.fingerprint+'`.','']
        sections=list(dict.fromkeys(i['section'] for i in self.data['items']))
        for section in sections:
            lines+=['## '+section,'']+[f"- **{i['status']}** — {i['text']}" for i in self.data['items'] if i['section']==section]+['']
        lines+=['## Questions non résolues','']+[f"- **{q['status']}** — {q['text']}"+(' Réponse : '+q['answer'] if q['answer'] else '') for q in self.data['questions']]
        lines+=['','## Priorités et dépendances — proposées','']+[f"- {t['id']} : {t['priority']} ({t['priority_status']}) ; prérequis : "+(', '.join(t['requires']) or 'aucun lien de dépendance imposé') for t in self.data['tasks']]
        return '\n'.join(lines)+'\n'


def budgets(root):
    """Read-only view: reporting never resets or saves a daily ledger."""
    path=safe_path(root,'output/queue.json');q=json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
    daily=q.get('daily',{});today=dt.datetime.now(dt.timezone.utc).date().isoformat();limit=load_config(root)['daily']['max_http_calls']
    used=daily.get('http_calls',0) if daily.get('date')==today else 0
    cfg=config(root)
    return {'daily_recorded':daily,'daily_http_remaining':max(0,limit-used),'daily_limit':limit,
            'session_http_cap':cfg['research']['max_http_calls'],'tick_http_cap':cfg['research']['http_per_tick'],
            'mutated':False,'note':'new-day availability calculated without modifying historical counters'}
