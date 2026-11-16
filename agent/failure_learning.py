"""Conditional failure hypotheses; never automatic root-cause proof or execution."""
import copy
from agent.lab_store import LabStore,clean_json
from agent.project_work import bound_experiments
from agent.intelligence_evidence import digest
from agent.project import Bible

CAUSES={
 'export':('export','fbx','normals','scale','import'),
 'lighting':('shadow','ombre','light','éclairage','faisceau'),
 'geometry':('flat','plat','silhouette','branch','géométrie'),
 'collision':('collision','bloqu','stuck','traverse'),
 'performance':('fps','frame','latency','slow','performance'),
 'protocol':('control','missing','inconnu','baseline','témoin'),
 'materials':('texture','roughness','normalmap','matériau'),
 'camera':('camera','caméra','viewmodel','clipping')}

def conditions_signature(technique,parameters,environment,protocol):
 protocol={k:v for k,v in protocol.items() if k not in ('retry_justification','failure_learning')}
 return digest([technique,parameters,environment,protocol])

def guard_repeat(root,technique,parameters,environment,protocol):
 task=environment.get('project_task') or parameters.get('project_task')
 if task is None:return
 Bible(root).task(task)
 signature=conditions_signature(technique,parameters,environment,protocol)
 for r in bound_experiments(root,task):
  for result in r['results']:
   if result['status']!='FAILED':continue
   c=result['conditions']
   if signature==conditions_signature(r['technique'],c['parameters'],c['environment'],c['protocol']):
    reason=protocol.get('retry_justification')
    if not isinstance(reason,str) or not 12<=len(reason)<=1000:raise ValueError('same failed method/conditions; supply a specific retry_justification or change the conditions')

def diagnose(root,experiment_id):
 r=LabStore(root).get(experiment_id)
 if r.get('error'):raise ValueError('unknown experiment')
 if not r['results']:return {'state':'WAITING_EVIDENCE','experiment_id':r['id'],'engine_executed':False,'hypotheses':[],'automatic_actions':[]}
 last=r['results'][-1];c=last['conditions'];task=c['environment'].get('project_task') or c['parameters'].get('project_task')
 body=' '.join(last['errors']+last['observations']).lower();categories=[name for name,terms in CAUSES.items() if any(term in body for term in terms)][:3]
 task_spec=Bible(root).tasks.get(task);query=task_spec['query'] if task_spec else 'Roblox reported experiment conditions'
 hypotheses=[{'category':name,'status':'HYPOTHESIS','text':'Examiner la contribution de '+name+' sous les conditions enregistrées.','basis':'keywords in client errors/observations; not independent causal evidence'} for name in categories]
 return {'schema':'vdn.failure-diagnostic/11.2','state':'RESEARCH_PROPOSED' if last['status']=='FAILED' else 'REVIEW_REPORTED_RESULT','experiment_id':r['id'],'event_sha256':r['event_sha256'],'task':task,
  'reported_status':last['status'],'reported_conditions':c,'hypotheses':hypotheses,
  'targeted_queries':[query+' '+name for name in categories[:2]] or [query+' reproduction controls'],
  'next_experiment':{'status':'ENGINEERING_PROPOSAL','parent_failure':r['id'],'hypothesis':'Isoler une cause candidate avant de changer une seule variable.','changed_variable':categories[0] if categories else 'protocol controls to clarify','controls':'reuse the recorded baseline except the explicitly changed variable','evidence_needed':['actual engine/build and asset revision','raw observations or captures','baseline and candidate under comparable conditions']},
  'automatic_actions':[],'network_requests':0,'code_or_policy_modified':False,'verified':False,'visual_analysis_performed':False,'scope':'client reports retained; keywords are diagnostic hypotheses, never formal causality'}
