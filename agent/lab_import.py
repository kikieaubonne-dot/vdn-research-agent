"""Validate external collector reports against an explicitly configured design."""
from agent.lab_store import LabStore,clean_json,identity
from agent.lab_plan import METRICS,CONTROLS
import uuid
import hashlib


def measurement(root,relative_path,apply=False):
    import json
    from agent.obsidian import safe_path
    if not isinstance(relative_path,str) or not relative_path.startswith('lab/inbox/'):raise ValueError('stage measurement in lab/inbox')
    path=safe_path(root,relative_path)
    if path.stat().st_size>64000:raise ValueError('measurement report too large')
    raw=path.read_bytes();report=json.loads(raw);clean_json(report)
    required={'schema','experiment_id','method','metrics','observations','errors','controls','environment'}
    if not isinstance(report,dict) or set(report)!=required or report['schema']!='vdn.roblox-measurement/10':raise ValueError('invalid measurement report fields')
    lab=LabStore(root);r=lab.get(identity(report['experiment_id']))
    if r.get('error'):raise ValueError('unknown measurement experiment')
    request_id=str(uuid.uuid5(uuid.UUID(r['id']),hashlib.sha256(raw).hexdigest()))
    replay=any(e['request_id']==request_id and e['action']=='result' for e in lab._events(r['id']))
    if r['status']!='RUNNING' and not replay:raise ValueError('measurement requires a RUNNING experiment')
    if report['method'] not in ('A','B') or not isinstance(report['environment'],dict) or not isinstance(report['controls'],dict) or set(report['controls'])!=set(CONTROLS):raise ValueError('invalid collector design fields')
    if report['method']!=r['parameters'].get('method') or report['environment']!=r['environment'] or report['controls']!=r['protocol'].get('controls'):
        raise ValueError('measurement identity or conditions mismatch; configure the design explicitly before starting')
    metrics=report['metrics']
    if not isinstance(metrics,dict) or set(metrics)-set(METRICS):raise ValueError('unknown measurement metric')
    for value in metrics.values():
        if value is not None and (type(value) not in (int,float) or value<0):raise ValueError('invalid metric')
    for field in ('observations','errors'):
        if not isinstance(report[field],list) or not all(isinstance(s,str) and 0<len(s)<=4000 for s in report[field]):raise ValueError('invalid measurement observations')
    if not report['observations']:raise ValueError('observations required')
    if not apply:return {'state':'simulation','experiment_id':r['id'],'metrics':metrics,'verified':False}
    artifact=lab.import_artifact(relative_path,'external_measurement')
    return lab.record_result(r['id'],'PARTIAL_SUCCESS' if not report['errors'] else 'FAILED',
                             {k:metrics.get(k) for k in METRICS},report['observations'],errors=report['errors'],artifacts=[artifact['id']],
                             limits=['External report; no independent verification. Heartbeat is not rendered FPS.'],
                             request_id=request_id)
