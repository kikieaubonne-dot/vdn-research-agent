"""Project cards and compact handoffs over the existing intelligence pipeline."""
import datetime as dt
import json
from pathlib import Path
import re
from agent import intelligence_models as im
from agent.intelligence import Intelligence
from agent.intelligence_evidence import digest,analyze
from agent.lab_store import clean_json,LabStore
from agent.obsidian import safe_path
from agent.ocean_web import OceanWeb
from agent.project import Bible,budgets,request_context
from agent.project_quality import quality,drift
from agent.project_recipes import recipe
from agent.storage import atomic_write

VERSION='project-11.2.3'


def bound_experiments(root,task_id):
    lab=LabStore(root);folder=lab.path('experiments');out=[]
    paths=list(folder.iterdir()) if folder.exists() else []
    if len(paths)>1000:raise ValueError('experiment limit exceeded')
    for path in paths:
        r=lab.get(path.name)
        if r.get('error'):continue
        if r['environment'].get('project_task')==task_id or r['parameters'].get('project_task')==task_id:out.append(r)
    out.sort(key=lambda r:(r['updated_at'],r['id']),reverse=True)
    return out[:20]


class Project:
    def __init__(self,root):self.root=Path(root).resolve();self.brain=Intelligence(self.root)
    @property
    def bible(self):return Bible(self.root) # live revision, including long-running MCP servers
    def path(self,relative):return safe_path(self.root,'lab/ocean/project/'+relative)
    def write(self,path,value,create_only=False):
        text=clean_json(value,1_000_000);OceanWeb(self.root).storage_check(len(text.encode('utf-8')));atomic_write(path,text,create_only=create_only)
    def index(self):
        p=self.path('latest.json')
        if not p.exists():return {}
        if p.stat().st_size>64000:raise ValueError('project index oversized')
        data=json.loads(p.read_text(encoding='utf-8'));clean_json(data)
        if data.get('schema')!='vdn.project-index/11.2' or not isinstance(data['tasks'],dict):raise ValueError('invalid project index')
        return data['tasks']
    def archive(self):
        path=safe_path(self.root,'project/prepared.json')
        if not path.exists():return {}
        if path.stat().st_size>1_000_000:raise ValueError('prepared project archive oversized')
        value=json.loads(path.read_text(encoding='utf-8'));clean_json(value,1_000_000)
        if value.get('schema')!='vdn.project-prepared/11.2' or not isinstance(value['cards'],list):raise ValueError('invalid prepared project archive')
        out={}
        for item in value['cards']:
            if item['payload_hash']!=digest(item['card']) or item['key']!=item['card']['key']:raise ValueError('prepared card integrity mismatch')
            if not item['card'].get('public_archive'):raise ValueError('archive must declare its secondary provenance')
            out[item['key']]=item['card']
        return out
    def reuse_fingerprint(self,task_id):
        # Check the inputs again on reads; a saved result is not evidence that
        # sources, operator reports or configuration are still current.
        import time
        from agent.intelligence_evidence import documents,VERSION as pipeline_version
        from agent.project_visual import references
        diagnostics=[];docs=documents(self.root,diagnostics)
        return digest({'bible':self.bible.fingerprint,'pipeline':pipeline_version,'configuration':im.settings(self.root),
            'sources':[{k:d[k] for k in ('id','sha256','version','conditions','truncated','independent')} for d in docs],
            'expired':[d['id'] for d in docs if d['retrieved_at'] and time.time()-d['retrieved_at']>86400],
            'diagnostics':diagnostics,
            'experiments':[(r['id'],r['revision'],r['event_sha256']) for r in bound_experiments(self.root,task_id)],
            'visuals':references(self,task_id),
            'dependencies':{d:self.index().get(d) for d in self.bible.task(task_id)['requires']}})
    def has_card(self,key):return self.path('cards/'+key+'.json').exists() or key in self.archive()
    def get(self,key):
        if not isinstance(key,str) or not re.fullmatch('[a-f0-9]{64}',key):raise ValueError('invalid project card key')
        path=self.path('cards/'+key+'.json')
        if path.exists():
            if path.stat().st_size>1_000_000:raise ValueError('project card oversized')
            item=json.loads(path.read_text(encoding='utf-8'));clean_json(item,1_000_000)
            if item.get('key')!=key or item.get('payload_hash')!=digest(item['card']):raise ValueError('project card integrity mismatch')
            card=item['card']
        else:
            card=self.archive().get(key)
            if card is None:raise ValueError('unknown project card')
        changed=card['bible_hash']!=self.bible.fingerprint
        obsolete=not card.get('public_archive') and card.get('reuse_fingerprint')!=self.reuse_fingerprint(card['task_id'])
        if card.get('public_archive'):
            current=[{'id':r['id'],'revision':r['revision'],'event_sha256':r['event_sha256']} for r in bound_experiments(self.root,card['task_id'])]
            obsolete=card['context'].get('experiment_revisions',[])!=current
            qa=card['quality'];card={**card,'parameters':[],'archived_parameter_candidates':card.get('parameters',[]),'quality':{**qa,'facts':[],
                'issues':list(dict.fromkeys(qa['issues']+['archived_sources_require_local_revalidation'])),
                'checks':{**qa['checks'],'original_sources_sufficient':False,'compatibility_and_assets_human_reviewed':False}},
                'compatibility':{**card['compatibility'],'verified':False},
                'confidence':{'states':['ENGINEERING_PROPOSAL'],'truth_verified':False,'scope':'secondary published preparation record; sources not revalidated in this clone'}}
        return {**card,'project_revision_obsolete':changed,'inputs_obsolete':obsolete,
                'current_readiness':'PARTIAL' if changed or obsolete or card.get('public_archive') and card['quality']['readiness']!='BLOCKED' else card['quality']['readiness']}
    def latest(self,task_id):
        key=self.index().get(task_id)
        if key:return self.get(key)
        matches=[c for c in self.archive().values() if c['task_id']==task_id]
        return self.get(max(matches,key=lambda c:c['created_at'])['key']) if matches else None
    def plan(self):
        bible=self.bible;plan=bible.plan();diagnostics=[]
        for node in plan['nodes']:
            try:card=self.latest(node['id'])
            except (ValueError,OSError,KeyError,TypeError):card=None;diagnostics.append({'task':node['id'],'error':'corrupt card; inspect before reuse'})
            if card:
                node.update(readiness=card['current_readiness'],research_state=card['quality']['research_state'],
                            sources_available=len(card['sources']),gaps=card['quality']['issues'],last_research=card['created_at'],
                            next_action=card['next_action'],card_key=card['key'])
        plan['diagnostics']=diagnostics;return plan
    def synthesize(self,question,apply=False,allow_model=False,retrieval='lexical',include_analysis=False):
        if type(apply) is not bool or type(allow_model) is not bool:raise ValueError('explicit booleans required')
        bible=self.bible;found=bible.match(question)
        if found['state']!='matched':return {**found,'writes':0,'network_requests':0,'drift':drift(bible,question)}
        conflict,requested=request_context(question,bible)
        if conflict:return conflict
        task=bible.task(found['task'])
        def work():
            records=bound_experiments(self.root,task['id']);context=bible.context(task)
            context['request_constraints']=requested
            from agent.project_visual import references
            visuals=references(self,task['id'])
            context['visual_references']=[{k:v[k] for k in ('sha256','target','keep','avoid','render_version','human_opinion','visual_analysis_performed')} for v in visuals]
            context['experiment_revisions']=[{'id':r['id'],'revision':r['revision'],'event_sha256':r['event_sha256']} for r in records]
            context['bound_failures']=[{'id':r['id'],'technique':r['technique'][:200],'errors':r['results'][-1]['errors'][:2]} for r in records if r['results'] and r['results'][-1]['status']=='FAILED'][:2]
            result=self.brain.run(task['query'],apply=apply,allow_model=allow_model,retrieval=retrieval,project_context=context)
            proposal=recipe(task);deps={}
            for dep in task['requires']:
                old=self.latest(dep);deps[dep]=old['current_readiness'] if old else 'UNKNOWN'
            qa=quality(bible,task,result,proposal,deps,records)
            parameters=[p for p in result['documented_parameters'] if p['claim_id'] in {c['id'] for c in qa['facts']}]
            next_action=(qa['blocking_questions'][0]['text'] if qa['blocking_questions'] else
                         'Inspecter l’échec et changer explicitement les conditions avant de répéter.' if qa['failures'] else
                         'Collecter un passage original pertinent et compatible.' if not qa['facts'] else
                         'Préparer les entrées puis exécuter le protocole isolé ; revue humaine requise.')
            reuse=self.reuse_fingerprint(task['id'])
            key=digest({'reuse_fingerprint':reuse,'version':VERSION,'bible':bible.fingerprint,'task':task['id'],'analysis':result['key'],
                        'analysis_outcome':{'state':result['state'],'model_error':result['model_error'],
                            'facts':[(c['id'],c['support']) for c in result['facts']]},
                        'dependencies':deps,'experiment_revisions':context['experiment_revisions']})
            card={'schema':'vdn.project-card/11.2','key':key,'bible_hash':bible.fingerprint,'task_id':task['id'],'reuse_fingerprint':reuse,
                'problem':task['objective'],'context':context,'priority':task['priority'],'priority_status':task['priority_status'],
                'solution':proposal['solution'],'choice_reason':'Comparaison isolée proposée à partir du problème du jeu ; aucune méthode optimale établie.',
                'prerequisites':[{'asset':a,'availability':'UNKNOWN; provide or attest through a task-bound experiment'} for a in task['assets']],
                'implementation':proposal,'parameters':parameters,'alternatives':proposal['alternatives'],
                'sources':qa['sources'],'compatibility':{'target_engine':bible.value('engine'),'target_blender':bible.value('blender_version'),
                    'verified':qa['checks']['compatibility_and_assets_human_reviewed']},
                'risks':proposal['risks'],'test':proposal['test'],'rollback':proposal['rollback'],
                'confidence':{'states':qa['evidence_states'],'truth_verified':False,'scope':'attribution and reported test conditions; no universal guarantee'},
                'next_action':next_action,'quality':qa,'analysis_key':result['key'],'analysis_state':result['state'],
                'created_at':dt.datetime.now(dt.timezone.utc).isoformat(),'cache_hit':False,'model_calls_this_run':result['model_calls_this_run']}
            if apply:
                p=self.path('cards/'+key+'.json')
                existed=p.exists()
                if existed:card={**self.get(key),'cache_hit':True,'model_calls_this_run':result['model_calls_this_run']}
                else:self.write(p,{'key':key,'payload_hash':digest(card),'card':card},True)
                index=self.index();index[task['id']]=key;self.write(self.path('latest.json'),{'schema':'vdn.project-index/11.2','tasks':index})
            return {**result,'project_card':card} if include_analysis else card
        return im.operation(self.root,work) if apply else work()
    def brief(self,question,token_budget=1800,key=None):
        from agent.engine import integer
        from agent.engine import string
        string(question,'question');integer(token_budget,'token_budget',500,8000);bible=self.bible
        conflict,requested=request_context(question,bible)
        q=question.lower()
        if conflict:payload=conflict
        elif key:
            card=self.get(key);payload=self._handoff(card,token_budget)
        elif any(word in q for word in ('bible','scénario','scenario','personnages','chronologie')):
            entries=[{'id':i['id'],'status':i['status'],'text':i['text']} for i in bible.data['items']]
            payload={'kind':'bible','revision':bible.data['revision'],'bible_hash':bible.fingerprint,'items':entries,
                     'questions':[{'id':x['id'],'text':x['text'],'status':x['status']} for x in bible.data['questions']],
                     'scope':'user context; studied ideas are not confirmed game decisions'}
            while len(json.dumps(payload,ensure_ascii=False))>token_budget*2.4 and payload['items']:payload['items'].pop()
        elif any(word in q for word in ('pack','prochaines tâches','prochaines taches','rapport quotidien')):
            payload=self.pack(3,token_budget)
        else:
            found=bible.match(question)
            if found['state']!='matched':payload=found
            else:
                card=self.latest(found['task'])
                if not card or card.get('inputs_obsolete') or card.get('project_revision_obsolete') or card['context'].get('request_constraints',{})!=requested:card=self.synthesize(question)
                payload=self._handoff(card,token_budget) if card.get('schema')=='vdn.project-card/11.2' else card
        # Existing core field names remain available; the project handoff carries
        # its own readiness, evidence and decisive question within the same cap.
        out={'schema':'vdn.intelligence-brief/11.1','key':payload.get('card_key') or digest({'bible':bible.fingerprint,'question':question}),
             'question':question[:200],'facts':[],'problems':[payload['task_id']] if payload.get('task_id') else [],
             'provisional_diagnosis':[],'inferences':[],'procedures':[],'experiments':[],'contradictions':[],
             'uncertainties':payload.get('uncertainties',[]),'priority_actions':[],'references':[],
             'failed_methods':[],'reviewed_experiments':[],'detail_tool':'get_intelligence_analysis',
             'abstained_from_established_facts':not payload.get('source_attribution_available',False),'truth_verified':False,'untrusted_data':True,
             'project':payload,'scope':'Propositions de laboratoire, compatibilité et conditions à vérifier ; aucune édition du jeu.'}
        if payload.get('task_id') and not self.has_card(out['key']):
            out['detail_tool']='synthesize_technical'
            out['detail_note']='Unsaved read-only preview: request synthesize_technical with the same question and apply=false for complete current evidence.'
        if len(json.dumps(out,ensure_ascii=False))>token_budget*3.6:
            out['project']={'state':'PARTIAL','reason':'context budget insufficient for the complete handoff','detail_task':payload.get('task_id'),
                            'rollback':'Conserver et restaurer les copies témoins.','question':payload.get('question'),
                            'scope':'Fetch the detailed task card before implementation; no safety constraint silently removed.'}
            out['abstained_from_established_facts']=True
        return out
    def _handoff(self,card,token_budget):
        steps=card['implementation']['steps'];sources=card['sources'][:3]
        payload={'task_id':card['task_id'],'card_key':card['key'],'analysis_key':card['analysis_key'],
            'objective':card['problem'],'context':{k:card['context'][k] for k in ('project','target_engine','blender_target','device_target')},
            'request_constraints':card['context'].get('request_constraints',{}),
            'readiness':card.get('current_readiness',card['quality']['readiness']),'solution':card['solution'],
            'prerequisites':card['prerequisites'],
            'implementation':[{'component':s['component'],'input':s['input'],'action':s['action'],'expected':s['expected_observation']} for s in steps],
            'sources':sources,'source_attribution_available':bool(card['quality']['facts']) and not card.get('inputs_obsolete') and not card.get('project_revision_obsolete'),'evidence_scope':card['confidence']['states'],'risks':card['risks'],
            'tests':card['test'],'rollback':card['rollback'],'uncertainties':card['quality']['issues'],
            'question':card['quality']['blocking_questions'][0]['text'] if card['quality']['blocking_questions'] else None,
            'next_action':card['next_action'],'project_revision_obsolete':card.get('project_revision_obsolete',False)}
        if card.get('inputs_obsolete') or card.get('project_revision_obsolete'):
            payload['solution']='Fiche historique périmée : recalculer avec les entrées actuelles avant implémentation.'
            payload['implementation']=[];payload['sources']=[]
            payload['uncertainties']=list(dict.fromkeys(payload['uncertainties']+['inputs_changed_reanalysis_required']))
        if card['quality']['failures']:
            payload['solution']='Examiner l’échec lié ; aucune répétition recommandée dans les mêmes conditions sans justification nouvelle.'
            payload['implementation']=[]
        while len(json.dumps(payload,ensure_ascii=False))>token_budget*2.6:
            if len(payload['sources'])>1:payload['sources'].pop()
            elif len(payload['implementation'])>1:payload['implementation'].pop()
            elif len(payload['uncertainties'])>3:payload['uncertainties'].pop()
            else:break
        return payload
    def pack(self,limit=3,token_budget=1800):
        from agent.engine import integer
        integer(limit,'limit',3,5);plan=self.plan();chosen=[n for n in plan['nodes'] if n['priority'] in ('P0','P1') or n['effective_research_priority'] in ('P0','P1')][:limit]
        return {'kind':'quickstart_pack','bible_hash':plan['bible_hash'],'tasks':[{'id':t['id'],'objective':t['objective'],
            'readiness':t['readiness'],'priority':t['priority'],'effective_research_priority':t['effective_research_priority'],
            'prerequisites':t['requires'],'required_assets':t['assets'],'next_action':t['next_action'],'card_key':t.get('card_key')} for t in chosen],
            'scope':'next useful research/preparation tasks, not a claim that implementation is ready'}
    def daily(self):
        plan=self.plan();return {'bible_hash':plan['bible_hash'],'ready':[n['id'] for n in plan['nodes'] if n['readiness']=='READY'],
            'partial':[n['id'] for n in plan['nodes'] if n['readiness']=='PARTIAL'],
            'blocked':[n['id'] for n in plan['nodes'] if n['readiness']=='BLOCKED'],
            'unknown':[n['id'] for n in plan['nodes'] if n['readiness']=='UNKNOWN'],
            'blocking_questions':self.bible.data['questions'],'budget':budgets(self.root),'next':self.pack()['tasks'],
            'new_knowledge':list(self.index().values()),'failed_runs':self.brain.search('Roblox')['incomplete_or_failed_runs'],
            'schedule_activated':False,'scope':'manual snapshot, not a daily daemon'}
    def pages(self):
        bible=self.bible;pages={'knowledge/_VDN-Bible.md':bible.markdown(),
            'knowledge/_VDN-Project-Quickstart.md':'# Prochaines tâches proposées\n\n```json\n'+clean_json(self.pack())+'\n```\n'}
        for task in bible.data['tasks']:
            card=self.latest(task['id'])
            if not card:continue
            if card.get('inputs_obsolete') or card.get('project_revision_obsolete'):card=self.synthesize(task['id'])
            lines=['# '+task['title'],'','État : '+card.get('current_readiness',card['quality']['readiness'])+' ; candidat, pas de technique validée.',
                '', '## Objectif',card['problem'],'','## Contexte',card['context']['project'],
                '', '## Solution proposée',card['solution'],'','## Pourquoi',card['choice_reason'],'','## Prérequis']
            lines+=['- '+p['asset']+' : '+p['availability'] for p in card['prerequisites']]
            lines+=['','## Implémentation']+['- '+s['component']+' — '+s['action']+' Attendu : '+s['expected_observation'] for s in card['implementation']['steps']]
            lines+=['','## Sources']+['- '+s['url']+' — '+s['version'] for s in card['sources']]
            if not card['sources']:lines+=['Aucune source originale suffisamment attribuée ; recherche partielle.']
            lines+=['','## Compatibilité, confiance et lacunes',clean_json({'compatibility':card['compatibility'],'confidence':card['confidence'],'issues':card['quality']['issues']}),
                '', '## Paramètres documentés',clean_json(card['parameters']),
                '', '## Alternatives',clean_json(card['alternatives']),
                '', '## Test proposé',clean_json(card['test']),'','## Risques']+['- '+s for s in card['risks']]
            lines+=['','## Rollback',card['rollback'],'','## Prochaine action',card['next_action'],'',
                'Clé de fiche : `'+card['key']+'` ; analyse : `'+card['analysis_key']+'`.']
            pages['knowledge/_VDN-Project-'+task['id']+'.md']='\n'.join(lines)+'\n'
        return pages


def preparation_archive(cards):
    """Publish authored procedures and source metadata, never bodies or private reports."""
    import copy
    out=[]
    for original in cards:
        card=copy.deepcopy(original)
        card['public_archive']=True
        card['publication_scope']='secondary preparation captured in an isolated lab; originals and experiments must be revalidated before use'
        card['quality']['facts']=[{k:c[k] for k in ('id','passage_ids','source_ids','support','version','engine','truth_verified')} for c in card['quality']['facts']]
        card['quality']['experiments']=[];card['quality']['failures']=[]
        card['context']['bound_failures']=[];card['context']['visual_references']=[]
        card['current_readiness']='BLOCKED' if card['quality']['blocking_questions'] else 'PARTIAL'
        card['quality']['readiness']=card['current_readiness'];card['quality']['research_state']='PARTIAL' if card['sources'] else 'UNKNOWN'
        out.append({'key':card['key'],'payload_hash':digest(card),'card':card})
    return {'schema':'vdn.project-prepared/11.2','scope':'secondary project memory, not independent technical sources','cards':out}
