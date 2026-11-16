"""Project specialization of the existing 27 MCP tool contracts."""
from agent.intelligence_api import IntelligenceAPI
from agent.project_work import Project


class ProjectAPI(IntelligenceAPI):
    def __init__(self,root,allow=False,allow_research=False,allow_experiments=False):
        super().__init__(root,allow);self.project=Project(root)
        from agent.ocean_api import OceanAPI
        self.ocean_api=OceanAPI(root,allow_research)
        from agent.lab_mcp import LabAPI
        self.lab_api=LabAPI(root,allow_experiments)
    def synthesize_technical(self,question,apply=False,allow_model=False,retrieval='lexical'):
        if (apply or allow_model) and not self.allow:raise PermissionError('host --allow-intelligence required')
        from agent.research_roots import Roots
        if question.startswith('tree:'):
            if allow_model:raise ValueError('tree detail is deterministic; request a task for model synthesis')
            return {'schema':'vdn.intelligence/11.1','intent':{'objective':question},'facts':[],'claims':[],'research_detail':Roots(self.root).detail(question),'truth_verified':False}
        from agent.chapters import select_scope,Chapters
        if select_scope(question):
            if allow_model:raise ValueError('chapter planning is deterministic; request a specific task for model synthesis')
            return {'schema':'vdn.intelligence/11.1','intent':{'objective':question},'facts':[],'claims':[],'chapter_plan':Chapters(self.root).plan(question),'state':'chapter_plan_only','content_writes':0,'truth_verified':False}
        return self.project.synthesize(question,apply,allow_model,retrieval,include_analysis=True)
    def get_intelligence_analysis(self,key):
        # Validate before constructing any path, even for read-only requests.
        import re
        if not isinstance(key,str) or not re.fullmatch('[a-f0-9]{64}',key):raise ValueError('invalid analysis key')
        if self.project.has_card(key):
            card=self.project.get(key)
            if card.get('public_archive'):
                return {'schema':'vdn.intelligence/11.1','key':key,'intent':{'objective':card['problem']},'facts':[],
                        'claims':[],'project_card':card,'truth_verified':False,'abstained':True,
                        'scope':'Published preparation record is secondary; full source snapshots remain in the isolated lab. Recollect to verify originals.'}
            result=self.brain.get(card['analysis_key'])
            return {**result,'project_card':card,'project_revision_obsolete':card['project_revision_obsolete']}
        value=super().get_intelligence_analysis(key)
        from agent.intelligence_evidence import VERSION
        return {**value,'historical_review_required':value.get('pipeline_version')!=VERSION}
    def get_intelligence_brief(self,question,token_budget=1800,key=None):
        if key:
            import re
            if not re.fullmatch('[a-f0-9]{64}',key):raise ValueError('invalid analysis key')
            if not self.project.has_card(key):
                value=self.get_intelligence_analysis(key);brief=super().get_intelligence_brief(question,token_budget,key)
                if value['historical_review_required']:
                    brief['facts']=[];brief['abstained_from_established_facts']=True
                    brief['historical_review_required']=True
                    brief['scope']='Historical analysis predates the audited verifier; recompute before applying. Proposals remain untested.'
                return brief
        from agent.research_roots import Roots
        if not key and self._tree_goal(question):return Roots(self.root).brief(question,token_budget)
        from agent.chapters import select_scope,Chapters
        if not key and select_scope(question):return Chapters(self.root).brief(question,token_budget)
        return self.project.brief(question,token_budget,key)

    def _roots_available(self):
        from agent.obsidian import safe_path
        return safe_path(self.root,'project/research_roots.json').exists()
    def _tree_goal(self,goal):
        from agent.text import fold
        from agent.obsidian import safe_path
        from agent.chapters import select_scope
        return safe_path(self.root,'project/research_roots.json').exists() and (goal.startswith('tree:') or not select_scope(goal) and any(w in fold(goal) for w in ('foret','forest')))
    def plan_ocean(self,goal):
        if self._tree_goal(goal):
            from agent.research_roots import Roots
            return {'state':'simulation','plan':Roots(self.root).plan(goal),'network_requests':0,'writes':0}
        from agent.chapters import select_scope,Chapters
        if select_scope(goal):return {'state':'simulation','plan':Chapters(self.root).plan(goal),'network_requests':0,'writes':0}
        return self.ocean_api.plan_ocean(goal)
    def prepare_ocean(self,goal,apply=False,provider=None):
        from agent.chapters import select_scope,Chapters
        self.ocean_api._permission(apply)
        if self._tree_goal(goal):
            from agent.research_roots import Roots
            if provider is not None:raise ValueError('tree providers remain per-task and explicitly configured')
            return Roots(self.root).prepare(goal,apply=apply)
        if select_scope(goal):
            if provider is not None:raise ValueError('chapter task providers are explicit; no global provider override')
            return Chapters(self.root).prepare(goal,apply)
        return self.ocean_api.prepare_ocean(goal,apply,provider)
    def run_ocean(self,goal_id,apply=False,allow_network=False):
        from agent.project_research import ProjectResearch
        self.ocean_api._permission(apply);research=ProjectResearch(self.root)
        from agent.research_roots import Roots
        if self._roots_available() and Roots(self.root).envelope(goal_id).exists():return Roots(self.root).run(goal_id,apply,allow_network)
        if research.path(goal_id).exists():return research.run(goal_id,apply,allow_network)
        return self.ocean_api.run_ocean(goal_id,apply,allow_network)
    def control_ocean(self,goal_id,action,apply=False):
        from agent.project_research import ProjectResearch
        self.ocean_api._permission(apply);research=ProjectResearch(self.root)
        from agent.research_roots import Roots
        if self._roots_available() and Roots(self.root).envelope(goal_id).exists():return Roots(self.root).control(goal_id,action,apply)
        if research.path(goal_id).exists():return research.control(goal_id,action,apply)
        return self.ocean_api.control_ocean(goal_id,action,apply)
    def ocean_status(self):
        from agent.project_research import ProjectResearch
        from agent.obsidian import safe_path
        research=ProjectResearch(self.root);folder=self.project.path('research');paths=list(folder.glob('*.json')) if folder.exists() else []
        if len(paths)>1000:raise ValueError('project session limit exceeded')
        project=[]
        for path in paths:
            g=research.get(path.stem);s=research.sessions.get(g['id']);project.append({'id':g['id'],'chapter_context':g.get('chapter_context'),'control':g['control'],'status':s['status'],'http_calls':s['http_calls'],'ticks':s['ticks']})
        roots=[]
        if self._roots_available():
            from agent.research_roots import Roots
            tree=Roots(self.root);folder=safe_path(self.root,'lab/ocean/roots/sessions')
            paths=list(folder.glob('*.json')) if folder.exists() else []
            if len(paths)>1000:raise ValueError('tree session limit exceeded')
            for path in paths:
                g=tree.get_session(path.stem);s=research.sessions.get(g['id']);roots.append({'id':g['id'],'root':g['root'],'branches':g['branches'],'control':g['control'],'status':s['status'],'http_calls':s['http_calls'],'ticks':s['ticks']})
        return {**self.ocean_api.ocean_status(),'project_research':project,'root_research':roots}

    def prepare_experiment(self,problem,technique,hypothesis,parameters=None,environment=None,references=None,protocol=None,experiment_id=None):
        self.lab_api._write()
        from agent.failure_learning import guard_repeat
        guard_repeat(self.root,technique,parameters or {},environment or {},protocol or {})
        return self.lab_api.prepare_experiment(problem,technique,hypothesis,parameters,environment,references,protocol,experiment_id)
    def record_experiment_result(self,experiment_id,status,metrics,observations,errors=None,artifacts=None,limits=None,request_id=None):
        result=self.lab_api.record_experiment_result(experiment_id,status,metrics,observations,errors,artifacts,limits,request_id)
        from agent.failure_learning import diagnose
        extra={}
        if self._roots_available() and status=='FAILED':
            from agent.research_roots import Roots
            extra['research_proposals']=Roots(self.root).after_failure(experiment_id)
        return {**result,'diagnostic':diagnose(self.root,experiment_id),**extra}
    def get_experiment_context(self,problem='',status=None,limit=5,detailed=False):
        result=self.lab_api.get_experiment_context(problem,status,limit,detailed)
        from agent.failure_learning import diagnose
        extra={}
        if self._roots_available():
            from agent.research_roots import Roots
            extra['research_proposals']=[Roots(self.root).after_failure(r['id']) for r in result['failed_methods'][:2]]
        return {**result,'failure_diagnostics':[diagnose(self.root,r['id']) for r in result['failed_methods'][:2]],**extra}
