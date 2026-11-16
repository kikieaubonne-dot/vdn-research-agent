"""V10 local memory tools; operator verification and artifact import absent."""
from agent.lab_store import LabStore
from agent.lab_plan import context,summary
import json


def brief(engine,**args):
    result=engine.get_task_brief(**args)
    memory=context(engine.root,args['task'],limit=2)
    result['experiment_memory']={'failed_methods':memory['failed_methods'],'reviewed_candidates':memory['reviewed_candidates'],
                                 'scope':'bounded lexical matches; inspect get_experiment_context before reuse'}
    maximum=args.get('token_budget',1800)*3.6
    while len(json.dumps(result,ensure_ascii=False))>maximum:
        if result['procedures']:
            result['procedures'].pop()
            if not result['procedures']:result.update(abstained=True,status='response_budget_insufficient')
        elif result['experiment_memory']['reviewed_candidates']:result['experiment_memory']['reviewed_candidates'].pop()
        elif result['experiment_memory']['failed_methods']:result['experiment_memory']['failed_methods'].pop()
        else:break
    return result


class LabAPI:
    def __init__(self,root,allow_writes=False):self.root=root;self.lab=LabStore(root);self.allow_writes=allow_writes
    def get_experiment_context(self,problem='',status=None,limit=5,detailed=False):
        if type(detailed) is not bool:raise ValueError('detailed must be boolean')
        return context(self.root,problem,status,limit,detailed)
    def get_experiment(self,experiment_id,detailed=False):
        if type(detailed) is not bool:raise ValueError('detailed must be boolean')
        r=self.lab.get(experiment_id)
        return r if detailed or r.get('error') else summary(r)
    def _write(self):
        if not self.allow_writes:raise PermissionError('experiment writes disabled by host')
    def prepare_experiment(self,problem,technique,hypothesis,parameters=None,environment=None,references=None,protocol=None,experiment_id=None):
        self._write();r=self.lab.create(problem,technique,hypothesis,parameters,environment,references,experiment_id,protocol)
        if r['status']=='HYPOTHESIS':r=self.lab.transition(r['id'],'PLANNED')
        return summary(r)
    def start_experiment(self,experiment_id,expected_revision):
        self._write();return summary(self.lab.transition(experiment_id,'RUNNING',expected_revision))
    def record_experiment_result(self,experiment_id,status,metrics,observations,errors=None,artifacts=None,limits=None,request_id=None):
        self._write();return summary(self.lab.record_result(experiment_id,status,metrics,observations,errors,artifacts,limits,request_id))


def tools(schema,TEXT):
    identifier={'type':'string','minLength':36,'maxLength':36}
    strings={'type':'array','items':{'type':'string','maxLength':4000},'maxItems':30}
    def tool(name,description,properties,required,write=False):
        return {'name':name,'description':description,'inputSchema':schema(properties,required),
                'annotations':{'readOnlyHint':not write,'destructiveHint':False,'openWorldHint':False}}
    return [tool('get_experiment_context','Find failed methods and conditionally reviewed candidates; never infer a universal best technique.',
                 {'problem':TEXT,'status':{'type':'string'},'limit':{'type':'integer','minimum':1,'maximum':20},'detailed':{'type':'boolean'}},[]),
            tool('get_experiment','Read concise experiment status and limitations; detailed returns full evidence history snapshot.',
                 {'experiment_id':identifier,'detailed':{'type':'boolean'}},['experiment_id']),
            tool('prepare_experiment','Prepare a PLANNED experiment; does not execute Studio or verify results.',
                 {'problem':TEXT,'technique':TEXT,'hypothesis':TEXT,'parameters':{'type':'object'},'environment':{'type':'object'},
                  'references':strings,'protocol':{'type':'object'},'experiment_id':identifier},['problem','technique','hypothesis'],True),
            tool('start_experiment','Record explicit start; caller executes the external experiment. Revision required.',
                 {'experiment_id':identifier,'expected_revision':{'type':'integer','minimum':1}},['experiment_id','expected_revision'],True),
            tool('record_experiment_result','Store a client-reported outcome, errors and evidence receipt IDs. Cannot set VERIFIED.',
                 {'experiment_id':identifier,'status':{'type':'string','enum':['FAILED','PARTIAL_SUCCESS','SUCCESS']},
                  'metrics':{'type':'object'},'observations':strings,'errors':strings,'artifacts':strings,'limits':strings,'request_id':identifier},
                 ['experiment_id','status','metrics','observations'],True)]
