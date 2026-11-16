"""Project specialization of the existing 27 MCP tool contracts."""
from agent.intelligence_api import IntelligenceAPI
from agent.project_work import Project


class ProjectAPI(IntelligenceAPI):
    def __init__(self,root,allow=False):super().__init__(root,allow);self.project=Project(root)
    def synthesize_technical(self,question,apply=False,allow_model=False,retrieval='lexical'):
        if (apply or allow_model) and not self.allow:raise PermissionError('host --allow-intelligence required')
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
        return self.project.brief(question,token_budget,key)
