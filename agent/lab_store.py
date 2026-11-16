"""Persistent experiments. An outcome is a report; VERIFIED requires operator review.

Each event contains a full bounded snapshot and a hash chain. There is no mutable
head file to lose after a crash. Artifact inputs are restricted to lab/inbox/.
"""
from __future__ import annotations
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import uuid

from agent.autonomy import Lock
from agent.engine import string,integer
from agent.obsidian import safe_path
from agent.storage import atomic_write,atomic_bytes
from agent.text import tokens

STATES=('HYPOTHESIS','PLANNED','RUNNING','FAILED','PARTIAL_SUCCESS','SUCCESS','VERIFIED','OBSOLETE')
NEXT={'HYPOTHESIS':{'PLANNED','OBSOLETE'},'PLANNED':{'RUNNING','OBSOLETE'},
      'RUNNING':{'FAILED','PARTIAL_SUCCESS','SUCCESS'},'FAILED':{'PLANNED','OBSOLETE'},
      'PARTIAL_SUCCESS':{'PLANNED','OBSOLETE'},'SUCCESS':{'PLANNED','VERIFIED','OBSOLETE'},
      'VERIFIED':{'PLANNED','OBSOLETE'},'OBSOLETE':set()}


def clean_json(value, maximum=64000):
    try:text=json.dumps(value,ensure_ascii=False,sort_keys=True,allow_nan=False)
    except (TypeError,ValueError,RecursionError) as exc:raise ValueError('invalid finite JSON data') from exc
    if len(text.encode('utf-8'))>maximum:raise ValueError('record exceeds size limit')
    if re.search(r'(?:gh[pousr]_|github_pat_)[A-Za-z0-9_]{30,}|\bsk-[A-Za-z0-9_-]{30,}',text):
        raise ValueError('possible credential; record refused')
    def check(obj):
        if isinstance(obj,dict):
            for key,item in obj.items():
                if str(key).lower() in ('password','api_key','secret_key','authorization'):raise ValueError('credential field refused')
                check(item)
        elif isinstance(obj,list):
            for item in obj:check(item)
    check(value)
    return text


def sha(value):return hashlib.sha256(clean_json(value).encode('utf-8')).hexdigest()
def identity(value):return str(uuid.UUID(string(value,'id',36)))
def now():return dt.datetime.now(dt.timezone.utc).isoformat()


def lab_lock(root,relative='.control'):
    for name in ('vdn.guard','vdn.lock'):
        safe_path(root,'lab/'+relative+'/output/'+name)
    return Lock(safe_path(root,'lab/'+relative),7200)


class LabStore:
    def __init__(self,root):
        self.root=Path(root).resolve()

    def path(self,relative):return safe_path(self.root,'lab/'+relative)

    def _events(self,experiment_id):
        folder=self.path('experiments/'+identity(experiment_id)+'/events')
        previous=None;events=[]
        paths=sorted(folder.glob('*.json')) if folder.exists() else []
        if len(paths)>1000:raise ValueError('event history limit exceeded')
        for index,path in enumerate(paths,1):
            path=self.path(path.relative_to(self.root/'lab').as_posix())
            if path.name!=f'{index:06d}.json' or path.stat().st_size>64000:raise ValueError('event sequence corrupt')
            event=json.loads(path.read_text(encoding='utf-8'))
            required={'schema','revision','previous','request_id','intent','action','recorded_at','snapshot','sha256'}
            if not isinstance(event,dict) or set(event)!=required or event['schema']!='vdn.experiment-event/10' or not isinstance(event['snapshot'],dict):raise ValueError('invalid experiment event structure')
            snapshot=event['snapshot']
            if not {'id','status','results','verification'}<=set(snapshot) or snapshot['status'] not in STATES or not isinstance(snapshot['results'],list):raise ValueError('invalid experiment snapshot')
            checksum=event.get('sha256');data={k:v for k,v in event.items() if k!='sha256'}
            if event.get('previous')!=previous or event.get('revision')!=index or sha(data)!=checksum:
                raise ValueError('experiment hash chain corrupt')
            if event['snapshot']['id']!=identity(experiment_id):raise ValueError('experiment identity mismatch')
            events.append(event);previous=checksum
        return events

    def get(self,experiment_id):
        events=self._events(experiment_id)
        if not events:return {'error':'unknown experiment','id':experiment_id}
        return {**events[-1]['snapshot'],'revision':len(events),'event_sha256':events[-1]['sha256'],
                'created_at':events[0]['recorded_at'],'updated_at':events[-1]['recorded_at']}

    def _append(self,experiment_id,snapshot,action,request_id=None):
        events=self._events(experiment_id)
        request_id=identity(request_id) if request_id else str(uuid.uuid4())
        intent=sha({'action':action,'snapshot':snapshot})
        for event in events:
            if event['request_id']==request_id:
                if event['intent']!=intent:raise ValueError('request_id already used for different content')
                return self.get(experiment_id)
        if len(events)>=1000:raise ValueError('event history limit reached')
        event={'schema':'vdn.experiment-event/10','revision':len(events)+1,'previous':events[-1]['sha256'] if events else None,
               'request_id':request_id,'intent':intent,'action':action,'recorded_at':now(),'snapshot':snapshot}
        event['sha256']=sha(event)
        path=self.path(f"experiments/{experiment_id}/events/{event['revision']:06d}.json")
        atomic_write(path,clean_json(event)+'\n',create_only=True)
        return self.get(experiment_id)

    def create(self,problem,technique,hypothesis,parameters=None,environment=None,references=None,experiment_id=None,protocol=None):
        for name,value in (('problem',problem),('technique',technique),('hypothesis',hypothesis)):string(value,name)
        parameters={} if parameters is None else parameters;environment={} if environment is None else environment
        references=[] if references is None else references;protocol={} if protocol is None else protocol
        if not all(isinstance(v,dict) for v in (parameters,environment,protocol)) or not isinstance(references,list):raise ValueError('invalid experiment structure')
        if not all(isinstance(r,str) and len(r)<=200 for r in references):raise ValueError('invalid references')
        experiment_id=identity(experiment_id) if experiment_id else str(uuid.uuid4())
        spec={'problem':problem,'technique':technique,'hypothesis':hypothesis,'parameters':parameters,
              'environment':environment,'references':references,'protocol':protocol}
        fingerprint=sha(spec)
        with lab_lock(self.root):
            old=self.get(experiment_id)
            if not old.get('error'):
                if old['spec_sha256']!=fingerprint:raise ValueError('experiment_id already used for another specification')
                return old
            snapshot={'id':experiment_id,**spec,'spec_sha256':fingerprint,'status':'HYPOTHESIS',
                      'results':[],'review':None,'verification':'not_verified','reuse_conditions':[]}
            return self._append(experiment_id,snapshot,'created')

    def transition(self,experiment_id,status,expected_revision=None):
        if status in ('SUCCESS','PARTIAL_SUCCESS','FAILED','VERIFIED'):raise ValueError('use result or operator review; no direct promotion')
        with lab_lock(self.root):
            record=self.get(experiment_id)
            self._check(record,status,expected_revision)
            record=self._snapshot(record);record['status']=status;record['review']=None;record['verification']='not_verified'
            record['reuse_conditions']=[]
            return self._append(experiment_id,record,'transition:'+status)

    def configure(self,experiment_id,parameters,environment,protocol,expected_revision):
        """Explicit design amendment before a run; past results retain their conditions."""
        if not all(isinstance(v,dict) for v in (parameters,environment,protocol)):raise ValueError('invalid design')
        with lab_lock(self.root):
            r=self.get(experiment_id)
            if r.get('error') or r['status'] not in ('HYPOTHESIS','PLANNED') or type(expected_revision) is not int or r['revision']!=expected_revision:
                raise ValueError('design amendment requires current HYPOTHESIS/PLANNED revision')
            r=self._snapshot(r);r.update(parameters=parameters,environment=environment,protocol=protocol)
            return self._append(experiment_id,r,'design_amendment')

    def _snapshot(self,record):return {k:v for k,v in record.items() if k not in ('revision','event_sha256','created_at','updated_at')}

    def _check(self,record,status,expected_revision=None):
        if record.get('error'):raise ValueError('unknown experiment')
        if expected_revision is not None and (type(expected_revision) is not int or record['revision']!=expected_revision):raise ValueError('stale experiment revision')
        if status not in NEXT.get(record['status'],set()):raise ValueError('invalid experiment transition')

    def import_artifact(self,relative_path,kind='self_generated'):
        if kind not in ('self_generated','external_measurement','external_capture'):raise ValueError('invalid artifact kind')
        relative=Path(relative_path)
        if not str(relative).replace('\\','/').startswith('lab/inbox/'):raise ValueError('artifact must be staged in lab/inbox')
        path=safe_path(self.root,relative_path)
        if not path.is_file() or path.stat().st_size>8_000_000:raise ValueError('invalid or oversized artifact')
        if path.suffix.lower() not in ('.json','.csv','.txt','.png','.jpg','.jpeg','.webp','.obj'):raise ValueError('artifact type not allowed')
        data=path.read_bytes()
        if path.suffix.lower() in ('.json','.csv','.txt','.obj'):clean_json({'content':data.decode('utf-8')},8_100_000)
        checksum=hashlib.sha256(data).hexdigest();artifact_id=checksum+'-'+kind
        dest=self.path('artifacts/'+artifact_id+path.suffix.lower())
        receipt={'id':artifact_id,'sha256':checksum,'path':dest.relative_to(self.root).as_posix(),
                 'bytes':len(data),'kind':kind,'verified':False}
        with lab_lock(self.root):
            receipt_path=self.path('artifacts/'+artifact_id+'.receipt.json')
            if receipt_path.exists():return self.artifact(artifact_id)
            if not dest.exists():atomic_bytes(dest,data,create_only=True)
            if not receipt_path.exists():atomic_write(receipt_path,clean_json(receipt)+'\n',create_only=True)
        return receipt

    def artifact(self,artifact_id):
        if not isinstance(artifact_id,str) or not re.fullmatch(r'[0-9a-f]{64}-(self_generated|external_measurement|external_capture)',artifact_id):raise ValueError('invalid artifact id')
        path=self.path('artifacts/'+artifact_id+'.receipt.json')
        if not path.exists():raise ValueError('unknown artifact')
        receipt=json.loads(path.read_text(encoding='utf-8'))
        if not isinstance(receipt,dict) or set(receipt)!={'id','sha256','path','bytes','kind','verified'} or not isinstance(receipt['path'],str):raise ValueError('invalid artifact receipt')
        if receipt.get('id')!=artifact_id or receipt.get('sha256')!=artifact_id[:64] or artifact_id!=receipt.get('sha256','')+'-'+receipt.get('kind',''):
            raise ValueError('artifact receipt identity failure')
        actual=safe_path(self.root,receipt['path'])
        if not receipt['path'].startswith('lab/artifacts/'+artifact_id+'.') or actual.stat().st_size>8_000_000 or actual.stat().st_size!=receipt.get('bytes') or hashlib.sha256(actual.read_bytes()).hexdigest()!=receipt['sha256']:
            raise ValueError('artifact integrity failure')
        return receipt

    def record_result(self,experiment_id,status,metrics,observations,errors=None,artifacts=None,limits=None,request_id=None):
        if status not in ('FAILED','PARTIAL_SUCCESS','SUCCESS'):raise ValueError('result cannot verify an experiment')
        if not isinstance(metrics,dict) or not isinstance(observations,list) or not observations:raise ValueError('metrics and observations required')
        for value in metrics.values():
            if value is not None and (type(value) not in (int,float) or value<0):raise ValueError('metrics must be nonnegative finite numbers or null')
        if not all(isinstance(v,str) and len(v)<=4000 for v in observations):raise ValueError('invalid observations')
        errors=[] if errors is None else errors;limits=[] if limits is None else limits;artifacts=[] if artifacts is None else artifacts
        if not all(isinstance(v,list) and all(isinstance(s,str) and len(s)<=4000 for s in v) for v in (errors,limits,artifacts)):raise ValueError('invalid result lists')
        if status=='FAILED' and not errors:raise ValueError('failed experiment must preserve errors')
        result={'status':status,'metrics':metrics,'observations':observations,'errors':errors,'artifacts':artifacts,'limits':limits,
                'provenance':'client_report_not_independently_verified'}
        clean_json(result)
        with lab_lock(self.root):
            record=self.get(experiment_id)
            if request_id:
                for event in self._events(experiment_id):
                    if event['request_id']==identity(request_id):
                        previous=event['snapshot']['results'][-1]
                        if event['action']!='result' or {k:previous[k] for k in result}!=result:raise ValueError('request_id content conflict')
                        return record
            self._check(record,status)
            for artifact_id in artifacts:self.artifact(artifact_id)
            result['conditions']={k:record[k] for k in ('parameters','environment','protocol')}
            record=self._snapshot(record);record['results'].append(result);record['status']=status
            record['review']=None;record['verification']='not_verified'
            return self._append(experiment_id,record,'result',request_id)

    def review(self,experiment_id,reviewer,conditions,attest=False):
        """Operator-only CLI boundary; deliberately absent from MCP and automatic workers."""
        string(reviewer,'reviewer',200)
        if attest is not True or not isinstance(conditions,list) or not conditions or not all(isinstance(c,str) and c.strip() for c in conditions):
            raise ValueError('explicit inspection attestation and reuse conditions required')
        with lab_lock(self.root):
            record=self.get(experiment_id);self._check(record,'VERIFIED')
            result=record['results'][-1]
            artifacts=[self.artifact(a) for a in result['artifacts']]
            if not artifacts or not any(a['kind'] in ('external_measurement','external_capture') for a in artifacts):
                raise ValueError('self-generated content is not independent experiment evidence')
            if not record['environment']:raise ValueError('software and environment conditions must be documented')
            record=self._snapshot(record);record['status']='VERIFIED'
            record['review']={'reviewer':reviewer,'attested_inspection':True,'conditions':conditions,'artifact_hashes':[a['sha256'] for a in artifacts]}
            record['reuse_conditions']=conditions;record['verification']='operator_reviewed_under_stated_conditions'
            return self._append(experiment_id,record,'operator_review')

    def find(self,problem='',status=None,limit=5,*,outcome=None):
        integer(limit,'limit',1,20)
        if not isinstance(problem,str) or len(problem)>2000:raise ValueError('invalid problem')
        if status is not None and status not in STATES:raise ValueError('invalid state')
        if outcome is not None and outcome not in ('FAILED','PARTIAL_SUCCESS','SUCCESS'):raise ValueError('invalid outcome filter')
        folder=self.path('experiments');records=[];diagnostics=[]
        paths=sorted(folder.iterdir()) if folder.exists() else []
        if len(paths)>1000:raise ValueError('experiment count limit exceeded')
        terms=set(tokens(problem))
        for path in paths:
            try:record=self.get(path.name)
            except (ValueError,OSError) as exc:diagnostics.append({'id':path.name,'error':str(exc)});continue
            if record.get('error') or status and record['status']!=status:continue
            if outcome and not any(r['status']==outcome for r in record['results']):continue
            matches=len(terms&set(tokens(record['problem']+' '+record['technique'])))
            if terms and not matches:continue
            records.append((matches,record))
        records.sort(key=lambda r:(-r[0],r[1]['id']))
        return {'experiments':[r for _,r in records[:limit]],'diagnostics':diagnostics,
                'warning':'Reported outcomes are not universal solutions; inspect conditions and evidence.'}
