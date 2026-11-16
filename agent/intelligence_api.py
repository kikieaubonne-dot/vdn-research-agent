"""Additive MCP surface: reads remain usable without model/write permission."""
from agent.intelligence import Intelligence
from agent import intelligence_models as im


class IntelligenceAPI:
    def __init__(self,root,allow=False):self.root=root;self.brain=Intelligence(root);self.allow=allow
    def synthesize_technical(self,question,apply=False,allow_model=False,retrieval='lexical'):
        if (apply or allow_model) and not self.allow:raise PermissionError('host --allow-intelligence required')
        return self.brain.run(question,apply=apply,allow_model=allow_model,retrieval=retrieval)
    def get_intelligence_analysis(self,key):return self.brain.get(key)
    def get_intelligence_brief(self,question,token_budget=1800,key=None):return self.brain.brief(question,token_budget,key)
    def search_intelligence(self,query,limit=5):return self.brain.search(query,limit)
    def diagnose_intelligence(self,probe=False,model=None):
        if probe and not self.allow:raise PermissionError('model probe consumes shared HTTP quota; host --allow-intelligence required')
        return im.diagnose(self.root,probe,model)


def tools(schema,TEXT):
    key={'type':'string','minLength':64,'maxLength':64};boolean={'type':'boolean'}
    def tool(name,description,props,required,write=False):return {'name':name,'description':description,'inputSchema':schema(props,required),
        'annotations':{'readOnlyHint':not write,'destructiveHint':False,'openWorldHint':write}}
    return [tool('synthesize_technical','Analyze intent, retrieve original/secondary passages, verify claims and critique. Model/apply requires host permission.',
                {'question':TEXT,'apply':boolean,'allow_model':boolean,'retrieval':{'type':'string','enum':['lexical','semantic','hybrid']}},['question'],True),
            tool('get_intelligence_analysis','Read a saved analysis, claims, source offsets, critiques and experiment protocols.',{'key':key},['key']),
            tool('get_intelligence_brief','Compact provisional diagnosis, facts, proposals, failures and uncertainty. No model call.',{'question':TEXT,'token_budget':{'type':'integer','minimum':500,'maximum':8000},'key':key},['question']),
            tool('search_intelligence','Find prior analyses; generated analyses never become independent evidence.',{'query':TEXT,'limit':{'type':'integer','minimum':1,'maximum':10}},['query']),
            tool('diagnose_intelligence','Hardware diagnostic; explicit local Ollama probe requires host permission and shared HTTP budget.',{'probe':boolean,'model':TEXT},[])]
