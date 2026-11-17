"""Single bounded operations entry point; existing V11.2 engines remain authoritative."""
import argparse
from contextlib import closing
import datetime as dt
import hashlib
import html
import json
import os
from pathlib import Path
import platform
import shutil
import sqlite3
import subprocess
import sys
import threading
import time
import uuid

from agent.lab_store import LabStore,clean_json
from agent.obsidian import safe_path
from agent.reliability import BlackBox,manifest,snapshot,restore,checksum,redact,repair_index,belief
from agent.storage import atomic_write

REPOSITORY=Path(__file__).resolve().parents[1]
DEFAULT={'schema':'vdn.productive-mission/1','enabled':False,'duration_s':1800,'max_restarts':2,'heartbeat_timeout_s':20,'progress_timeout_s':180,'interval_s':30,'allow_network':False,'allow_blender':False,'max_http_calls':6,'threads':1,'daily_report_time':'11:00','timezone':'Europe/Paris'}


def write(root,name,value):atomic_write(safe_path(root,name),clean_json(value,2_000_000)+'\n')


def write_checkpoint(root,value):
    value={k:v for k,v in value.items() if k!='payload_sha256'}
    value['payload_sha256']=hashlib.sha256(clean_json(value,2_000_000).encode()).hexdigest();write(root,'checkpoint.json',value)


def read_checkpoint(root):
    p=safe_path(root,'checkpoint.json')
    if p.stat().st_size>2_000_000:raise ValueError('checkpoint oversized')
    cp=json.loads(p.read_text(encoding='utf-8'));base={k:v for k,v in cp.items() if k!='payload_sha256'}
    if cp.get('schema')!='vdn.mission-checkpoint/2' or cp.get('payload_sha256')!=hashlib.sha256(clean_json(base,2_000_000).encode()).hexdigest():raise ValueError('checkpoint integrity/version invalid; preserve it for review')
    uuid.UUID(cp['id'])
    if not isinstance(cp['steps'],dict) or len(cp['steps'])>20:raise ValueError('invalid task checkpoint')
    for step in cp['steps'].values():
        if step.get('state') not in ('RUNNING','DONE','BLOCKED') or type(step.get('attempts')) is not int or not 1<=step['attempts']<=2 or step['state']=='DONE' and not isinstance(step.get('result'),dict):raise ValueError('invalid persisted task state')
    return cp


def settings(workspace):
    p=safe_path(workspace,'mission.json')
    if p.stat().st_size>16000:raise ValueError('mission configuration oversized')
    cfg=json.loads(p.read_text(encoding='utf-8'))
    if set(cfg)!=set(DEFAULT) or cfg['schema']!=DEFAULT['schema']:raise ValueError('invalid mission configuration')
    for k in ('enabled','allow_network','allow_blender'):
        if type(cfg[k]) is not bool:raise ValueError('boolean mission permission required')
    for k,lo,hi in (('duration_s',1,3600),('max_restarts',0,2),('heartbeat_timeout_s',2,60),('progress_timeout_s',5,600),('interval_s',1,300),('max_http_calls',0,12),('threads',1,1)):
        if type(cfg[k]) is not int or not lo<=cfg[k]<=hi:raise ValueError('invalid mission hard limit '+k)
    if cfg['timezone']!='Europe/Paris' or cfg['daily_report_time']!='11:00':raise ValueError('unsupported report timezone/time; preserve explicit user schedule')
    return cfg


def initialize(workspace,source=REPOSITORY,seed_runtime=None):
    """New private workspace only, no personal configuration or queue rewrite."""
    workspace=Path(workspace).absolute();source=Path(source).resolve();safe_path(workspace,'probe')
    forbidden=('agent','scripts','knowledge','config','project','lab/ocean','lab/research','lab/experiments','lab/artifacts')
    if workspace.exists() or source.is_relative_to(workspace) or any(workspace.is_relative_to(source/f) for f in forbidden):raise ValueError('choose a NEW workspace outside protected input folders')
    for folder in ('agent','scripts','config'):
        for p in (source/folder).rglob('*'):
            safe_path(source,p.relative_to(source).as_posix())
    workspace.mkdir(parents=True)
    before=manifest(source)
    snapshot(source,workspace/'restore-point',folders=('knowledge','config','project','output','lab/research','lab/experiments','lab/ocean','lab/learning','lab/inbox/learning'))
    recovery=restore(workspace/'restore-point',workspace/'restoration-check')
    code=workspace/'code';code.mkdir();runtime=workspace/'runtime';runtime.mkdir()
    for name in ('agent','scripts','config'):
        shutil.copytree(source/name,code/name,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    for name in ('eponge.py','vdn_mcp.py'):shutil.copyfile(source/name,code/name)
    for name in ('knowledge','config','project'):
        shutil.copytree(source/name,runtime/name)
    (runtime/'output').mkdir();source_queue=safe_path(source,'output/queue.json')
    if source_queue.exists():shutil.copyfile(source_queue,runtime/'output/queue.json')
    # Existing source-side ledgers, experiments and sessions stay in the copy.
    for name in ('research','ocean','experiments','artifacts','learning','inbox/learning'):
        folder=safe_path(source,'lab/'+name)
        if folder.exists():shutil.copytree(folder,runtime/('lab/'+name))
    if seed_runtime:
        seed=Path(seed_runtime).resolve();q=json.loads((runtime/'output/queue.json').read_text(encoding='utf-8'));old=json.loads(safe_path(seed,'output/queue.json').read_text(encoding='utf-8'))
        if q['daily']['date']!=old['daily']['date']:raise ValueError('explicit ledger reconciliation required for different dates')
        for k in ('items','fetch','http_calls'):q['daily'][k]=max(q['daily'][k],old['daily'][k])
        write(runtime,'output/queue.json',q)
        # Preserve known compute/model/session/experiment ledgers as well as caches.
        for name in ('ocean','research','experiments','artifacts','runner','learning','inbox/learning'):
            for p in safe_path(seed,'lab/'+name).rglob('*'):
                safe_path(seed,p.relative_to(seed).as_posix())
                if not p.is_file() or p.name in ('vdn.guard','vdn.lock'):continue
                dest=safe_path(runtime,p.relative_to(seed).as_posix())
                if dest.exists() and checksum(dest)!=checksum(p):raise ValueError('cache conflict; no silent replacement')
                if not dest.exists():dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
        # Transport permission is inherited only from the explicitly supplied runtime.
        shutil.copyfile(safe_path(seed,'config/ocean.json'),runtime/'config/ocean.json')
    cfg=dict(DEFAULT);write(workspace,'mission.json',cfg);write(workspace,'control.json',{'state':'READY'})
    files={p.relative_to(code).as_posix():checksum(p) for p in code.rglob('*') if p.is_file()}
    write(workspace,'code-manifest.json',{'schema':'vdn.frozen-code/1','files':files})
    state={'schema':'vdn.mission-checkpoint/2','id':str(uuid.uuid4()),'steps':{},'created_at':time.time(),'baseline_protected':manifest(runtime),'source_protected':before,'recovery_test':recovery,'repairs':[]}
    write_checkpoint(workspace,state)
    if manifest(source)!=before:raise ValueError('source changed during initialization')
    return {'state':'PREPARED_DISABLED','workspace':str(workspace),'recovery':recovery,'source_unchanged':True}


def doctor(workspace):
    from agent.intelligence_models import hardware
    root=Path(workspace);cfg=settings(root);runtime=safe_path(root,'runtime');checks={};checks['Python']='PASS' if sys.version_info>=(3,11) else 'BLOCKED'
    checks['Windows_user_PC']='NOT_TESTED' if os.name=='nt' else 'BLOCKED'
    checks['Claude_Desktop']='NOT_TESTED';checks['Roblox_Studio']='BLOCKED';checks['Ollama']='NOT_TESTED_OPTIONAL'
    b=shutil.which('blender');checks['Blender']='UNAVAILABLE';version=None
    if b:
        try:
            p=subprocess.run([b,'--version'],capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=3);version=p.stdout.splitlines()[0] if p.stdout else None;checks['Blender']='VERSION_DETECTED_NOT_ENGINE_TESTED' if p.returncode==0 else 'FAIL'
        except (OSError,subprocess.TimeoutExpired):checks['Blender']='FAIL'
    disk=shutil.disk_usage(root);checks['disk']='PASS' if disk.free>=64_000_000 else 'BLOCKED'
    from agent.project import Bible
    from agent.research_session import config
    try:Bible(runtime);config(runtime);checks['config']='PASS'
    except (OSError,ValueError,KeyError):checks['config']='BLOCKED'
    try:
        from importlib.util import spec_from_file_location,module_from_spec
        spec=spec_from_file_location('independent_guard',REPOSITORY/'scripts/eponge_guard.py');guard=module_from_spec(spec);spec.loader.exec_module(guard);guard.verify_code(root);checks['frozen_code']='PASS'
    except (OSError,ValueError,KeyError):checks['frozen_code']='BLOCKED'
    p=safe_path(runtime,'output/knowledge.db')
    if p.exists():
        try:
            with closing(sqlite3.connect(p.as_uri()+'?mode=ro',uri=True)) as c:checks['derived_index']='PASS' if c.execute('PRAGMA integrity_check').fetchone()[0]=='ok' else 'FAIL'
        except sqlite3.Error:checks['derived_index']='FAIL'
    else:checks['derived_index']='NOT_BUILT_DERIVED_CACHE'
    blocked=any(checks[k]=='BLOCKED' for k in ('Python','disk','config','frozen_code'))
    return {'schema':'vdn.operations-doctor/1','state':'BLOCKED' if blocked else 'DEGRADED','exit_code':2 if blocked else 1,'os':platform.system(),'python':platform.python_version(),'checks':checks,'blender_version':version,'hardware':hardware(False),'disk_free_bytes':disk.free,'network':'AUTHORIZED_ON_START_ONLY' if cfg['allow_network'] else 'DISABLED','code_complete':False,'Windows_local_ready':False,'cloud_core_ready':not blocked,'automatic_download':False}


def status(workspace,max_age=30):
    root=Path(workspace);p=safe_path(root,'guard-status.json')
    if not p.exists():return {'state':'STOPPED','reason':'supervisor not started','autonomy_running':False}
    value=json.loads(p.read_text(encoding='utf-8'));age=time.time()-value['last_heartbeat']
    if value['state'] in ('RUNNING','PAUSED') and (age>max_age or age<0):return {**value,'state':'STALE','heartbeat_age_s':age,'autonomy_running':False}
    return {**value,'heartbeat_age_s':age,'autonomy_running':value['state']=='RUNNING'}


def control(workspace,action):
    if action not in ('pause','resume','stop'):raise ValueError('invalid mission action')
    old=json.loads(safe_path(workspace,'control.json').read_text(encoding='utf-8'))
    if old['state']=='STOPPED' and action=='resume':raise ValueError('stop is terminal; start explicitly after diagnosis')
    write(workspace,'control.json',{'state':{'pause':'PAUSED','resume':'READY','stop':'STOPPED'}[action]});return {'state':{'pause':'PAUSED','resume':'READY','stop':'STOPPED'}[action]}


class Worker:
    def __init__(self,workspace,worker_id):
        self.workspace=Path(workspace);self.root=safe_path(workspace,'runtime');self.cfg=settings(workspace);self.box=BlackBox(self.root);self.worker_id=worker_id;self.lock=threading.RLock();self.done=threading.Event();self.started=time.time()
        self.checkpoint=read_checkpoint(workspace)
        self.current={'schema':'vdn.worker-status/1','worker_id':worker_id,'worker_pid':os.getpid(),'state':'RUNNING','activity':'startup','last_heartbeat':time.time(),'last_progress':time.time(),'last_completed_cycle':None,'queue_depth':6,'source_version':'frozen snapshot','Windows_user_PC':'BLOCKED','Roblox_Studio':'BLOCKED'}
    def save(self):
        with self.lock:
            self.current.update(last_heartbeat=time.time(),elapsed_wall_s=time.time()-self.started,CPU_self_s=time.process_time(),disk_free_bytes=shutil.disk_usage(self.root).free)
            write(self.workspace,'reports/status.json',self.current)
    def heartbeat(self):
        while not self.done.wait(1):
            try:self.save()
            except Exception as exc:
                try:self.box.fallback('heartbeat',exc)
                finally:self.done.set()
    def persist(self):write_checkpoint(self.workspace,self.checkpoint)
    def task(self,name,fn):
        old=self.checkpoint['steps'].get(name,{})
        if old.get('state')=='DONE':return old['result']
        if old.get('state')=='BLOCKED':return {'state':'BLOCKED','reason':'retained failure requires explicit review; no identical retry'}
        if old.get('attempts',0)>=2:
            old['state']='BLOCKED';self.checkpoint['steps'][name]=old;self.persist()
            self.box.incident(name,'checkpoint_recovery','task retry limit reached','HIGH',requires_human=True)
            return {'state':'BLOCKED','reason':'task retry limit; inspect incident history'}
        old={'state':'RUNNING','attempts':old.get('attempts',0)+1};self.checkpoint['steps'][name]=old;self.persist();self.current.update(activity=name,last_progress=time.time());self.save();t=time.monotonic()
        try:
            result=fn();old.update(state='DONE',result=result,elapsed_s=time.monotonic()-t)
        except Exception as exc:
            e=self.box.incident(name,'mission_task',str(exc),'HIGH',type(exc).__name__,requires_human=True);old.update(state='BLOCKED',exception_type=type(exc).__name__,incident_id=e['incident_id'],elapsed_s=time.monotonic()-t);result={'state':'BLOCKED','incident_id':e['incident_id']}
        self.current.update(last_progress=time.time(),last_completed_cycle=time.time());self.persist();self.save();return result
    def research(self):
        from agent.research_roots import Roots
        tree=Roots(self.root)
        if not self.cfg['allow_network']:return {'state':'OFFLINE_MEMORY_ONLY','plan':tree.plan('forest')}
        sid=self.checkpoint.get('research_session')
        if not sid:
            g=tree.prepare('forest',apply=True)
            if 'id' not in g:return g
            sid=g['id'];self.checkpoint['research_session']=sid;self.persist()
        rows=[]
        for _ in range(6):
            r=tree.run(sid,True,True);rows.append(r);write(self.workspace,'reports/research.json',{'state':r['state'],'cycles':rows})
            if r.get('acquisition_state') in ('COMPLETE','BLOCKED'):break
            if r['state']=='BUDGET_STOP' and r['research'].get('stop_details',{}).get('scope')!='tick':break
            if r['research']['session'].get('integration_failures',0)>=2:break
        last=rows[-1]
        for gap in tree.plan('forest')['nodes']:
            belief(self.root,gap['gap_id'],'Investigate '+gap['branch']+' under recorded conditions',[s['id'] for s in gap['sources']],counterexample='Failed experiment(s): '+', '.join(gap['failures']) if gap['failures'] else None)
        if last['state'] in ('ERROR','BUDGET_STOP'):
            self.box.incident('research','bounded_acquisition',last['state']+'; inspect local reports/research.json','MEDIUM',requires_human=False)
        return {'state':last['state'],'session_id':sid,'acquisition_state':last.get('acquisition_state'),'verified_game_knowledge_created':0}
    def cards(self):
        from agent.project_work import Project
        project=Project(self.root);rows=[]
        for task in ('trees','collisions','ground','lighting','performance'):
            r=project.synthesize(task,True);rows.append({'task':task,'key':r['key'],'readiness':r['quality']['readiness'],'source_count':len(r['sources'])})
        return {'state':'DOCUMENTARY_PREPARATIONS','cards':rows,'model_calls':0,'game_executed':False}
    def python_lab(self):
        lab=LabStore(self.root);eid=str(uuid.uuid5(uuid.UUID(self.checkpoint['id']),'python-retrieval-consistency'));r=lab.get(eid)
        if not r.get('error') and r['results']:return {'id':eid,'state':'REUSED_RESULT','outcome':r['results'][-1]['status']}
        r=lab.create('Lexical memory repeatability, not game technique','repeat identical read-only query','same fixed corpus gives identical top IDs',environment={'engine':'Python','version':platform.python_version()},protocol={'criteria':['identical IDs on same source corpus','no protected-source writes'],'preregistered':True},experiment_id=eid)
        if r['status']=='HYPOTHESIS':r=lab.transition(eid,'PLANNED')
        if r['status']=='PLANNED':lab.transition(eid,'RUNNING')
        from agent.engine import KnowledgeEngine
        engine=KnowledgeEngine(self.root);before=manifest(self.root);a=engine.search_knowledge('Roblox MeshPart collision');b=engine.search_knowledge('Roblox MeshPart collision');same=[x['id'] for x in a['results']]==[x['id'] for x in b['results']] and bool(a['results']) and manifest(self.root)==before
        lab.record_result(eid,'SUCCESS' if same else 'FAILED',{'results':len(a['results'])},['Actual Python repeatability check; no engine or semantic-truth inference'],errors=[] if same else ['repeatability criterion failed'],request_id=str(uuid.uuid5(uuid.UUID(eid),'result')))
        if not same:raise ValueError('independent memory repeatability check failed')
        return {'state':'SUCCESS','id':eid,'scope':'Python retrieval only'}
    def blender_lab(self):
        if not self.cfg['allow_blender']:return {'state':'BLOCKED_PERMISSION','game_executed':False}
        from agent.lab_runner import LocalLab
        binary=shutil.which('blender')
        if not binary:return {'state':'BLOCKED_MISSING_BLENDER'}
        p=subprocess.run([binary,'--version'],capture_output=True,text=True,encoding='utf-8',timeout=3)
        import re
        m=re.search(r'Blender (\d+\.\d+(?:\.\d+)?)',p.stdout)
        if p.returncode or not m:raise ValueError('Blender version unavailable')
        runner=LocalLab(self.root);jid=self.checkpoint.get('blender_job')
        if not jid:
            job=runner.prepare(required_version=m.group(1),apply=True);jid=job['id'];self.checkpoint['blender_job']=jid;self.persist()
        r=runner.run(jid,allow_blender=True)
        if r['state']!='SUCCEEDED':raise RuntimeError('Blender smoke test blocked/failed: '+r.get('error_kind','unknown'))
        return {'state':r['state'],'job_id':jid,'version':m.group(1),'reports':r['reports'],'scope':'generated primitive geometry only; not B3/C1, Blender5.2 or Roblox validation'}
    def export(self):
        from agent import obsidian,lab_plan
        from agent.project_work import Project
        pages={**Project(self.root).pages(),**lab_plan.pages(self.root)};vault=safe_path(self.workspace,'vault');first=obsidian.sync(self.root,vault,apply=True,extra_pages=pages);again=obsidian.sync(self.root,vault,apply=True,extra_pages=pages)
        if again['state']!='unchanged':raise ValueError('duplicate/non-idempotent export')
        p=next(vault.glob('knowledge/_VDN-Project-*.md'))
        if not p.read_text(encoding='utf-8'):raise ValueError('empty generated vault card')
        return {'state':'OBSIDIAN_SYNC_VERIFIED','first':first['state'],'second':again['state'],'sample':str(p.relative_to(vault)),'sha256':checksum(p),'personal_vault':False}
    def mcp(self):
        messages=[{'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2025-06-18','capabilities':{},'clientInfo':{'name':'operations-worker','version':'1'}}},{'jsonrpc':'2.0','id':2,'method':'tools/list'},{'jsonrpc':'2.0','id':3,'method':'tools/call','params':{'name':'get_intelligence_brief','arguments':{'question':'tree:forest/collisions'}}}]
        p=subprocess.run([sys.executable,str(REPOSITORY/'vdn_mcp.py'),'--root',str(self.root),'--v112'],input='\n'.join(json.dumps(m) for m in messages)+'\n',capture_output=True,text=True,encoding='utf-8',timeout=45)
        if p.returncode:raise RuntimeError('MCP subprocess failed')
        rows=[json.loads(l) for l in p.stdout.splitlines()]
        if len(rows)!=3 or len(rows[1]['result']['tools'])!=27 or any('error' in r or r['result'].get('isError') for r in rows):raise ValueError('MCP contract/reply invalid')
        write(self.workspace,'reports/mcp.json',rows);return {'state':'MCP_REAL_STDIO_VERIFIED','tools':27,'Claude_Desktop':'NOT_TESTED'}
    def reports(self):
        self.box.report();d={'schema':'vdn.productive-report/1','updated_at':time.time(),'status':self.current,'steps':self.checkpoint['steps'],'Windows_local_access':False,'Roblox_Studio':'BLOCKED','model_weights_trained':False,'source_claims_are_not_game_validation':True}
        write(self.workspace,'reports/report.json',d)
        text='# MORNING BRIEF\n\nEnvironment: '+platform.system()+'; Windows user PC: BLOCKED.\n\n'
        for name,row in self.checkpoint['steps'].items():text+='- '+name+': '+row['state']+' / '+str(row.get('result',{}).get('state','see incident'))+'\n'
        text+='\nNo automatic VERIFIED or code/security promotion. Blender primitives are not user assets.\n'
        atomic_write(safe_path(self.workspace,'reports/MORNING_BRIEF.md'),text);atomic_write(safe_path(self.workspace,'reports/report.html'),'<!doctype html><meta charset="utf-8"><pre>'+html.escape(text)+'</pre>')
        return {'state':'REPORTS_WRITTEN'}
    def repair_derived_index_if_needed(self):
        if not self.cfg['enabled']:raise PermissionError('automatic recovery requires an activated mission')
        p=safe_path(self.root,'output/knowledge.db')
        if not p.exists():return {'state':'NOT_REQUIRED'}
        valid=False
        try:
            with closing(sqlite3.connect(p.as_uri()+'?mode=ro',uri=True)) as c:valid=c.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
        except sqlite3.Error:pass
        return {'state':'NOT_REQUIRED'} if valid else repair_index(self.root)
    def run(self):
        if not self.cfg['enabled']:raise PermissionError('mission disabled')
        threading.Thread(target=self.heartbeat,daemon=True).start();self.save()
        tasks=[('research',self.research),('cards',self.cards),('python_lab',self.python_lab),('blender_lab',self.blender_lab),('obsidian',self.export),('mcp',self.mcp)]
        try:
            try:
                recovery=self.repair_derived_index_if_needed();self.checkpoint['repairs'].append(recovery);self.persist()
            except Exception as exc:
                self.box.incident('memory','automatic_derived_index_repair',str(exc),'HIGH',type(exc).__name__,True)
            for index,(name,fn) in enumerate(tasks):
                while json.loads(safe_path(self.workspace,'control.json').read_text(encoding='utf-8'))['state']=='PAUSED':self.current['state']='PAUSED';time.sleep(.2)
                if json.loads(safe_path(self.workspace,'control.json').read_text(encoding='utf-8'))['state']=='STOPPED' or self.done.is_set():break
                # Previous protected files must remain identical; new lab records are separate.
                if any(checksum(safe_path(self.root,n))!=h for n,h in self.checkpoint['baseline_protected'].items()):raise ValueError('protected baseline changed; worker stopped')
                self.task(name,fn);self.current['queue_depth']=len(tasks)-index-1;self.reports()
            self.current.update(activity='IDLE',last_progress=time.time());self.save();self.reports()
            return 1 if any(s['state']=='BLOCKED' for s in self.checkpoint['steps'].values()) else 0
        except Exception as exc:
            try:self.box.incident('worker','run',str(exc),'CRITICAL',type(exc).__name__,True);self.reports()
            except Exception as logger_exc:self.box.fallback('worker_or_reporter',logger_exc)
            return 2
        finally:
            self.done.set();self.current['state']='STOPPED'
            if self.checkpoint['steps'] and all(s['state']=='DONE' for s in self.checkpoint['steps'].values()):
                self.checkpoint['completed_inputs']=manifest(self.root,folders=('knowledge','config','project','lab/ocean/sources','lab/experiments'));self.persist()
            self.save()
            try:self.reports()
            except Exception as exc:self.box.fallback('final_report',exc)


def start(workspace,activate=False,allow_network=False,allow_blender=False):
    cfg=settings(workspace)
    if not activate:raise PermissionError('explicit activation required; no Windows/system scheduler installed')
    cp=read_checkpoint(workspace);runtime=safe_path(workspace,'runtime')
    requested_scope={'network':allow_network,'blender':allow_blender}
    if cp.get('execution_scope') is not None and cp['execution_scope']!=requested_scope and cp['steps']:raise ValueError('permissions changed after work; explicitly prepare a revised mission seeded from this runtime')
    if cp.get('completed_inputs') and cp['completed_inputs']!=manifest(runtime,folders=('knowledge','config','project','lab/ocean/sources','lab/experiments')):raise ValueError('completed mission inputs changed; previous results retained for review')
    if any(checksum(safe_path(runtime,n))!=h for n,h in cp['baseline_protected'].items()):raise ValueError('protected data changed after preparation; explicit review required')
    diagnosis=doctor(workspace)
    if diagnosis['state']=='BLOCKED':raise ValueError('core preflight blocked; no startup or permission change')
    cfg.update(enabled=True,allow_network=allow_network,allow_blender=allow_blender);write(workspace,'mission.json',cfg)
    p=safe_path(runtime,'config/v10.json');v=json.loads(p.read_text(encoding='utf-8'));v['network_enabled']=allow_network;v['autonomous_enabled']=True;v['research']['max_http_calls']=min(v['research']['max_http_calls'],cfg['max_http_calls']);write(runtime,'config/v10.json',v)
    cp=read_checkpoint(workspace);cp['baseline_protected']=manifest(runtime);cp['execution_scope']=requested_scope;write_checkpoint(workspace,cp)
    write(workspace,'control.json',{'state':'READY'})
    write(workspace,'activation.json',{'schema':'vdn.activation/1','at':time.time(),'source':'explicit operator CLI','duration_s':cfg['duration_s'],'network':allow_network,'blender':allow_blender,'system_startup_installed':False})
    command=[sys.executable,str(REPOSITORY/'scripts/eponge_guard.py'),'supervise',str(Path(workspace).absolute())]
    return subprocess.run(command,shell=False).returncode


def main(argv=None):
    if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--workspace',type=Path,default=REPOSITORY/'lab/productive');sub=p.add_subparsers(dest='command',required=True)
    s=sub.add_parser('init');s.add_argument('--source',type=Path,default=REPOSITORY);s.add_argument('--seed-runtime',type=Path)
    s=sub.add_parser('start');s.add_argument('--activate',action='store_true');s.add_argument('--allow-network',action='store_true');s.add_argument('--allow-blender',action='store_true')
    s=sub.add_parser('worker');s.add_argument('--worker-id',required=True)
    for name in ('doctor','status','report','pause','resume','stop','repair-index'):sub.add_parser(name)
    a=p.parse_args(argv)
    try:
        if a.command=='init':r=initialize(a.workspace,a.source,a.seed_runtime)
        elif a.command=='start':return start(a.workspace,a.activate,a.allow_network,a.allow_blender)
        elif a.command=='worker':return Worker(a.workspace,a.worker_id).run()
        elif a.command=='doctor':r=doctor(a.workspace);print(json.dumps(r,ensure_ascii=False,indent=2));return r['exit_code']
        elif a.command=='status':r=status(a.workspace)
        elif a.command in ('pause','resume','stop'):r=control(a.workspace,a.command)
        elif a.command=='repair-index':r=repair_index(safe_path(a.workspace,'runtime'))
        else:r={**json.loads(safe_path(a.workspace,'reports/report.json').read_text(encoding='utf-8')),'live_supervisor_status':status(a.workspace)}
        print(json.dumps(r,ensure_ascii=False,indent=2));return 0
    except (OSError,ValueError,RuntimeError,KeyError,TypeError) as exc:
        print(json.dumps({'state':'BLOCKED','exception_type':type(exc).__name__,'message':redact(exc)},ensure_ascii=False));return 2


if __name__=='__main__':raise SystemExit(main())
