"""Bounded recovery of derived data; no code/permission/reliable-memory promotion."""
import datetime as dt
from contextlib import closing
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sqlite3
import sys
import tempfile
import uuid

from agent.lab_store import clean_json, lab_lock
from agent.obsidian import safe_path
from agent.storage import atomic_write, atomic_bytes


def checksum(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def redact(value):
    from scripts.eponge_guard import redact as redact_log
    return redact_log(value)[:4000]


def manifest(root, folders=('knowledge','config','project')):
    root=Path(root);out={}
    for folder in folders:
        for p in sorted((root/folder).rglob('*')) if (root/folder).exists() else []:
            if p.is_symlink():raise ValueError('symlink in protected data')
            if p.is_file():out[p.relative_to(root).as_posix()]=checksum(safe_path(root,p.relative_to(root).as_posix()))
    return out


def snapshot(root, destination, folders=('knowledge','config','project')):
    """Explicit local snapshot, refusing overwrite and verifying a disposable restore."""
    root=Path(root).resolve();dest=Path(destination).absolute()
    if dest.exists() or root==dest or root.is_relative_to(dest):raise ValueError('new separate snapshot required')
    safe_path(dest,'manifest.json');files=manifest(root,folders)
    dest.mkdir(parents=True)
    for name in files:
        p=safe_path(dest,'files/'+name);p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(safe_path(root,name),p)
    record={'schema':'vdn.restore-point/1','files':files,'created_at':dt.datetime.now(dt.timezone.utc).isoformat()}
    atomic_write(dest/'manifest.json',clean_json(record,2_000_000))
    for name,h in files.items():
        if checksum(safe_path(dest,'files/'+name))!=h:raise ValueError('snapshot verification failed')
    return record


def restore(snapshot_folder, destination):
    source=Path(snapshot_folder);dest=Path(destination).absolute();safe_path(dest,'probe')
    if dest.exists():raise ValueError('restore into a NEW disposable destination only')
    p=safe_path(source,'manifest.json')
    if p.stat().st_size>2_000_000:raise ValueError('restore manifest oversized')
    m=json.loads(p.read_text(encoding='utf-8'))
    if m.get('schema')!='vdn.restore-point/1' or len(m['files'])>10000:raise ValueError('invalid restore manifest')
    # Validate every source and destination before creating anything.
    for name,h in m['files'].items():
        if checksum(safe_path(source,'files/'+name))!=h:raise ValueError('corrupt restore point')
        safe_path(dest,name)
    dest.mkdir(parents=True)
    for name in m['files']:
        p=safe_path(dest,name);p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(safe_path(source,'files/'+name),p)
    if any(checksum(safe_path(dest,n))!=h for n,h in m['files'].items()):raise ValueError('restore verification failed')
    return {'state':'RESTORED_VERIFIED','files':len(m['files'])}


class BlackBox:
    """Append-only incident events. A broken journal degrades health, never disappears."""
    def __init__(self,root):self.root=Path(root).resolve()
    def path(self,name):return safe_path(self.root,'lab/operations/reports/'+name)
    def incidents(self):
        p=self.path('incidents.jsonl');items={};previous=None;sealed=False
        if not p.exists():return items
        if p.stat().st_size>4_000_000:raise ValueError('incident journal cap reached')
        for line in p.read_text(encoding='utf-8').splitlines():
            e=json.loads(line)
            if e.get('schema_version') not in ('vdn.incident/1','vdn.incident/2') or not re.fullmatch('[a-f0-9]{24}',e.get('incident_id','')):raise ValueError('corrupt incident journal')
            if e['schema_version']=='vdn.incident/2':
                base={k:v for k,v in e.items() if k!='event_sha256'}
                if e.get('previous')!=previous or e.get('event_sha256')!=hashlib.sha256(clean_json(base).encode()).hexdigest():raise ValueError('incident integrity chain corrupt')
                previous=e['event_sha256'];sealed=True
            else:
                if sealed:raise ValueError('legacy journal downgrade refused')
                previous=hashlib.sha256(clean_json([previous,e]).encode()).hexdigest()
            items[e['incident_id']]=e
        return items
    def _append(self,event):
        p=self.path('incidents.jsonl');p.parent.mkdir(parents=True,exist_ok=True)
        if p.exists() and p.stat().st_size>4_000_000:raise ValueError('incident journal cap reached')
        self.incidents();previous=None
        if p.exists():
            for line in p.read_text(encoding='utf-8').splitlines():
                old=json.loads(line);previous=old['event_sha256'] if old.get('schema_version')=='vdn.incident/2' else hashlib.sha256(clean_json([previous,old]).encode()).hexdigest()
        event={k:v for k,v in event.items() if k not in ('event_sha256','previous')};event.update(schema_version='vdn.incident/2',previous=previous);event['event_sha256']=hashlib.sha256(clean_json(event).encode()).hexdigest()
        with p.open('a',encoding='utf-8',newline='') as f:f.write(clean_json(event)+'\n');f.flush();os.fsync(f.fileno())
    def incident(self,component,operation,symptoms,severity='MEDIUM',exception_type=None,requires_human=False):
        if severity not in ('LOW','MEDIUM','HIGH','CRITICAL'):raise ValueError('invalid severity')
        symptom=redact(symptoms);identity=hashlib.sha256(clean_json([component,operation,symptom,exception_type]).encode()).hexdigest()[:24]
        with lab_lock(self.root,'.blackbox'):
            old=self.incidents().get(identity,{});now=dt.datetime.now(dt.timezone.utc).isoformat()
            # A recurrence must not erase an earlier safety escalation. Only a
            # separate explicit operator review can justify reducing severity.
            order=('LOW','MEDIUM','HIGH','CRITICAL')
            severity=max((severity,old.get('severity',severity)),key=order.index)
            requires_human=requires_human or old.get('requires_human',False)
            e={'schema_version':'vdn.incident/1','incident_id':identity,'first_seen':old.get('first_seen',now),'last_seen':now,'occurrences':old.get('occurrences',0)+1,'severity':severity,'component':component,'operation':operation,'environment':'current runtime only','status':'BLOCKED' if requires_human else 'OPEN','symptoms':symptom,'expected':'bounded successful operation with preserved protected inputs','observed':symptom,'reproduction':{'operation':operation,'scope':'isolated runtime'},'exception_type':exception_type,'stack_trace_redacted':'','log_refs':[],'artifact_refs':[],'suspected_causes':[{'status':'HYPOTHESIS','text':'Cause not established; use the scoped reproduction.'}],'confidence':'unknown','attempted_fixes':old.get('attempted_fixes',[]),'verification':None,'recommended_next_step':'Inspect retained evidence; do not change permissions or critical code automatically.','requires_human':requires_human,'related_incidents':[]}
            self._append(e);return self.incidents()[e['incident_id']]
    def attempt(self,incident_id,action):
        if action not in ('rebuild_derived_index','retry_transient','resume_checkpoint'):raise PermissionError('repair action not AUTO_SAFE')
        with lab_lock(self.root,'.blackbox'):
            e=dict(self.incidents()[incident_id])
            if e['severity']=='CRITICAL' or e['requires_human']:raise PermissionError('incident requires operator review')
            attempts=e['attempted_fixes']
            if len(attempts)>=2:raise RuntimeError('repair circuit open; two attempts already retained')
            e['attempted_fixes']=attempts+[{'action':action,'at':dt.datetime.now(dt.timezone.utc).isoformat(),'outcome':'ATTEMPT_RESERVED'}];self._append(e);return self.incidents()[e['incident_id']]
    def resolve(self,incident_id,verification):
        if verification.get('state')!='PASS' or not verification.get('protected_before') or verification.get('protected_before')!=verification.get('protected_after') or verification.get('protected_after')!=manifest(self.root) or not verification.get('checks'):raise ValueError('retest and unchanged current protected data required')
        with lab_lock(self.root,'.blackbox'):
            e=dict(self.incidents()[incident_id])
            if e['severity']=='CRITICAL' or e['requires_human']:raise PermissionError('operator review required; no automatic resolution')
            e.update(status='RESOLVED',verification=verification);self._append(e);return self.incidents()[e['incident_id']]
    def fallback(self,component,exc):
        # No overwrite of good telemetry; report failure remains visible to caller.
        p=self.path('emergency-'+uuid.uuid4().hex+'.json')
        record={'schema':'vdn.emergency/1','state':'DIAGNOSTIC_UNAVAILABLE','component':component,'exception_type':type(exc).__name__,'message':redact(exc),'primary_failed':False}
        try:
            atomic_write(p,clean_json(record),create_only=True);return p
        except (OSError,ValueError):record['primary_failed']=True
        try:
            folder=Path(tempfile.mkdtemp(prefix='eponge-emergency-',dir=tempfile.gettempdir()));p=folder/'incident.json'
            atomic_write(p,clean_json(record),create_only=True);return p
        except (OSError,ValueError):return None
        finally:
            try:sys.stderr.write(json.dumps({'state':'DIAGNOSTIC_UNAVAILABLE','component':component,'exception_type':type(exc).__name__,'primary_failed':True})+'\n');sys.stderr.flush()
            except (OSError,ValueError):pass
    def report(self):
        items=self.incidents();active=[e for e in items.values() if e['status']!='RESOLVED']
        text='# HEALTH REPORT\n\nState: '+('BLOCKED' if any(e['severity']=='CRITICAL' for e in active) else 'DEGRADED' if active else 'NO_RECORDED_INCIDENTS')+'\n\nNo recorded incident is not universal health.\n'
        for e in active:text+='\n- '+e['component']+' / '+e['severity']+' / '+e['status']+': '+e['symptoms']+'\n  Next: '+e['recommended_next_step']+'\n'
        for name in ('HEALTH_REPORT.md','REPAIR_BACKLOG.md','CODEX_HANDOFF.md'):atomic_write(self.path(name),text)
        atomic_write(self.path('REPAIR_HANDOFF.json'),clean_json({'schema':'vdn.repair-handoff/1','incidents':list(items.values())},4_000_000))
        return {'active':len(active),'total':len(items)}


def repair_index(root):
    """Rebuild only SQLite derived cache. Original bytes quarantined, never discarded."""
    from agent import rag
    from agent.autonomy import Lock
    root=Path(root).resolve();box=BlackBox(root);before=manifest(root)
    p=safe_path(root,'output/knowledge.db');iid=box.incident('memory','derived_index','derived index requires verified reconstruction')['incident_id'];box.attempt(iid,'rebuild_derived_index')
    with Lock(root,7200),lab_lock(root,'.index-repair'):
        with tempfile.TemporaryDirectory(prefix='vdn-index-') as td:
            temp=Path(td);shutil.copytree(root/'knowledge',temp/'knowledge');rag.update_index(temp)
            q=rag.db_path(temp)
            with closing(sqlite3.connect(q)) as c:
                if c.execute('PRAGMA integrity_check').fetchone()[0]!='ok':raise ValueError('rebuilt index invalid')
            if manifest(root)!=before:raise ValueError('protected input changed during repair')
            if p.exists():
                quarantine=box.path('index-'+checksum(p)+'.backup');
                if not quarantine.exists():atomic_bytes(quarantine,p.read_bytes(),create_only=True)
            atomic_bytes(p,q.read_bytes())
    with closing(sqlite3.connect(p)) as c:
        if c.execute('PRAGMA integrity_check').fetchone()[0]!='ok':raise ValueError('index retest failed')
    box.resolve(iid,{'state':'PASS','checks':['fresh SQLite integrity_check','protected content unchanged'],'protected_before':before,'protected_after':manifest(root)})
    return {'state':'PASS','incident_id':iid,'reliable_memory_modified':False}


def belief(root,key,hypothesis,evidence=None,counterexample=None):
    """Versioned epistemic note, separate from reliable knowledge and model weights."""
    if not re.fullmatch('[a-z0-9-]{1,80}',key):raise ValueError('invalid belief identity')
    p=safe_path(root,'lab/operations/beliefs/'+key+'.json')
    with lab_lock(root,'.beliefs'):
        history=json.loads(p.read_text(encoding='utf-8')) if p.exists() else []
        if len(history)>=100:raise ValueError('belief revision cap reached')
        row={'revision':len(history)+1,'hypothesis':redact(hypothesis),'evidence':evidence or [],'counterexample':redact(counterexample) if counterexample else None,'status':'NEEDS_REVIEW' if counterexample else 'HYPOTHESIS','confidence':'uncalibrated','truth_verified':False}
        atomic_write(p,clean_json(history+[row]));return row
