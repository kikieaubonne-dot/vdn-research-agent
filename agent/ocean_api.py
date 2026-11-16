"""Compact reference memory, without granting a model authority to execute code."""
import json
from agent.engine import KnowledgeEngine,string,integer
from agent.lab_mcp import LabAPI
from agent import ocean_knowledge,lab_plan,gaps
from agent.ocean import Ocean
from agent.ocean_plan import describe


class OceanAPI:
    def __init__(self,root,allow_research=False):
        self.root=root;self.engine=KnowledgeEngine(root);self.ocean=Ocean(root);self.allow_research=allow_research
    def search_ocean(self,query,limit=5,semantic=False):
        if type(semantic) is not bool:raise ValueError('semantic must be boolean')
        if semantic:
            from agent.ocean_semantic import hybrid
            return hybrid(self.root,query,limit)
        diagnostics=[];found=ocean_knowledge.search(self.root,query,limit,diagnostics)
        return {'schema':'vdn.ocean-search/11','results':found,'legacy':self.engine.search_knowledge(ocean_knowledge.expand(query),min(limit,3),1500)['results'] if not found else [],
                'policy':'lexical concepts and bilingual/domain expansion, not neural semantics','index_diagnostics':diagnostics,'truth_verified':False}
    def get_ocean_card(self,note_id,detailed=False):
        string(note_id,'note_id',120)
        if type(detailed) is not bool:raise ValueError('detailed must be boolean')
        c=next((c for c in ocean_knowledge.cards(self.root) if c['id']==note_id),None)
        if c is None:return {'error':'unknown Ocean note','id':note_id}
        c['source_refresh_needed']=ocean_knowledge.refresh_needed(self.root,c)
        from agent.obsidian import safe_path
        path=safe_path(self.root,'lab/ocean/analyses/'+c['id']+'.json')
        if path.exists():
            if path.stat().st_size>64000:raise ValueError('analysis too large')
            c['model_analysis']=json.loads(path.read_text(encoding='utf-8'))
        if detailed:return c
        return {k:c[k] for k in ('id','title','facet','states','sources','claims','procedure','uncertainties','truth_verified','source_refresh_needed')} | {'model_analysis':c.get('model_analysis')}
    def get_ocean_brief(self,goal,token_budget=1800):
        string(goal,'goal');integer(token_budget,'token_budget',500,8000)
        matches=ocean_knowledge.search(self.root,goal,3)
        memory=LabAPI(self.root).get_experiment_context(goal,limit=2)
        selected=[]
        for m in matches:
            c=self.get_ocean_card(m['id'],True)
            selected.append({'id':c['id'],'title':c['title'],'states':c['states'],'source_refresh_needed':c['source_refresh_needed'],'facts':c['claims'][:2],
                             'source_urls':[s['url'] for s in c['sources']],'proposed_steps':c['procedure'][:2],
                             'test_protocol':c['validation'][:2],'uncertainties':c['uncertainties'][:2],
                             'model_questions':c.get('model_analysis',{}).get('hypotheses',[])[:2],
                             'model_proposed_steps':c.get('model_analysis',{}).get('proposed_steps',[])[:2]})
        result={'schema':'vdn.ocean-brief/11','goal':goal[:240],'candidates':selected,
                'legacy_references':[] if selected else self.engine.get_task_brief(goal,token_budget=1000).get('procedures',[])[:1],
                'failed_methods':memory['failed_methods'],'reviewed_experiments':memory['reviewed_candidates'],
                'missing':['Project-specific reproduction and software compatibility remain unverified.'],
                'abstained':not selected,'truth_verified':False,'untrusted_data':True,
                'warning':'Source excerpts are evidence of attribution; project steps are unverified proposals. Inspect sources and experiments before changing the game.'}
        maximum=token_budget*3.6
        while len(json.dumps(result,ensure_ascii=False))>maximum:
            if len(result['candidates'])>1:result['candidates'].pop();continue
            if result['legacy_references']:result['legacy_references']=[];continue
            if result['reviewed_experiments']:result['reviewed_experiments']=[];continue
            if result['failed_methods']:result['failed_methods']=[];result['missing'].append('Ask get_experiment_context for omitted failures.');continue
            if result['candidates']:
                c=result['candidates'][0]
                if len(c['facts'])>1:c['facts'].pop();continue
                if c['proposed_steps']:c['proposed_steps']=[];continue
                if c['test_protocol']:c['test_protocol']=[];continue
                result['candidates']=[];result['abstained']=True;continue
            break
        return result
    def plan_ocean(self,goal):return self.ocean.prepare(goal)
    def ocean_status(self):return {'goals':self.ocean.list(),'game_execution':'not performed by research worker'}
    def _permission(self,apply):
        if type(apply) is not bool:raise ValueError('apply must be boolean')
        if apply and not self.allow_research:raise PermissionError('Ocean writes/collection disabled by host; enable --allow-research')
    def prepare_ocean(self,goal,apply=False,provider=None):
        self._permission(apply);return self.ocean.prepare(goal,apply=apply,provider=provider)
    def run_ocean(self,goal_id,apply=False,allow_network=False):
        self._permission(apply);return self.ocean.advance(goal_id,apply=apply,allow_network=allow_network)
    def control_ocean(self,goal_id,action,apply=False):
        self._permission(apply);return self.ocean.control(goal_id,action,apply=apply)
    def compare_techniques(self,note_ids):
        if not isinstance(note_ids,list) or not 2<=len(note_ids)<=3:raise ValueError('compare 2–3 Ocean notes')
        return {'candidates':[self.get_ocean_card(n) for n in note_ids],'winner':None,
                'rule':'Compare source versions, conditions and actual experiment results; no universal best method.'}


def tools(schema,TEXT):
    ident={'type':'string','minLength':36,'maxLength':36}
    def tool(name,description,props,required,write=False):return {'name':name,'description':description,'inputSchema':schema(props,required),
        'annotations':{'readOnlyHint':not write,'destructiveHint':False,'openWorldHint':write}}
    boolean={'type':'boolean'}
    return [tool('search_ocean','Find source-grounded project candidates; optional configured LOCAL embeddings, otherwise lexical.',{'query':TEXT,'limit':{'type':'integer','minimum':1,'maximum':10},'semantic':boolean},['query']),
            tool('get_ocean_card','Read a structured candidate; SOURCE_SUPPORTED does not mean tested.',{'note_id':TEXT,'detailed':boolean},['note_id']),
            tool('get_ocean_brief','Consult before technical decisions: short candidates, sources, failures, tests and gaps.',{'goal':TEXT,'token_budget':{'type':'integer','minimum':500,'maximum':8000}},['goal']),
            tool('plan_ocean','Preview independent technical gaps; no queue mutation or web request.',{'goal':TEXT},['goal']),
            tool('ocean_status','Read persistent goals, resource counters and stop diagnostics.',{},[]),
            tool('compare_techniques','Compare candidates under conditions without inventing a winner.',{'note_ids':{'type':'array','items':TEXT}},['note_ids']),
            tool('prepare_ocean','Prepare a bounded goal; apply requires host --allow-research.',{'goal':TEXT,'apply':boolean,'provider':TEXT},['goal'],True),
            tool('run_ocean','Execute one bounded tick. Network requires configuration and explicit allow_network.',{'goal_id':ident,'apply':boolean,'allow_network':boolean},['goal_id'],True),
            tool('control_ocean','Pause, resume or stop a goal without resetting counters.',{'goal_id':ident,'action':TEXT,'apply':boolean},['goal_id','action'],True)]


def pages(root,include_lab=False):
    cards=ocean_knowledge.cards(root);goals=Ocean(root).list()
    result={}
    groups={'Decouvertes':cards,'Contradictions':[c for c in cards if 'DISPUTED' in c['states']],
            'Obsoletes':[c for c in cards if 'OUTDATED' in c['states']],
            'Sources-a-verifier':[c for c in cards if c['uncertainties']],
            'Lacunes':cards}
    for name,items in groups.items():
        lines=['# Océan — '+name,'','Candidates et propositions ; aucune vérité de jeu automatiquement validée.','']
        for c in items:
            target=c['path'].removeprefix('knowledge/').removesuffix('.md')
            lines+=['- [['+target+']] — '+', '.join(c['states'])]
            if name=='Lacunes':lines+=['  - '+s for s in c['uncertainties'][:3]]
        result['knowledge/_VDN-Ocean-'+name+'.md']='\n'.join(lines)+'\n'
    result['knowledge/_VDN-Ocean-Recherches.md']='# Recherches Océan\n\n'+'\n'.join('- '+g['id']+' : '+g['status']+' / '+g['control']+' ; HTTP '+str(g['http_calls']) for g in goals)+'\n'
    result['knowledge/_VDN-Ocean-Accueil.md']='# Océan — tableau de bord\n\n'+'\n'.join('[[ _VDN-Ocean-'+n+' ]]'.replace(' ','') for n in (*groups,'Recherches'))+'\n\n[[_VDN-Experiences]]\n[[_VDN-Ocean-Echecs-et-solutions]]\n'
    if include_lab:
        failures=lab_plan.context(root,status='FAILED')['failed_methods']
        result['knowledge/_VDN-Ocean-Echecs-et-solutions.md']='# Échecs et solutions conditionnelles\n\n'+'\n'.join('- [[_VDN-Experience-'+r['id']+']] — '+r['technique'] for r in failures)+'\n'
    else:
        result['knowledge/_VDN-Experiences.md']='# Expériences\n\nMémoire privée conservée dans le clone ; exporter explicitement avec --include-lab.\n'
        result['knowledge/_VDN-Ocean-Echecs-et-solutions.md']='# Échecs et solutions\n\nConsulter get_experiment_context ou exporter explicitement avec --include-lab.\n'
    return result
