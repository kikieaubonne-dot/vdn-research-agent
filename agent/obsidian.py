"""Incremental, journaled export bundles. Open destination/knowledge in Obsidian.

Only explicit apply writes. Untracked edits are conflicts, never overwritten.
Backups and rollback archives are retained; no user file is deleted.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import uuid

from agent.autonomy import Lock
from agent.corpus import library_path,MAX_NOTE_BYTES
from agent.storage import atomic_write

CONFIG_FILES=('research_domains.json','autonomy.json','production_v9.json')


def digest(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def exact_text(path):
    return path.read_bytes().decode('utf-8')


def safe_path(root, relative):
    root=Path(root).absolute()
    rel=Path(relative)
    if rel.is_absolute() or '..' in rel.parts or '\\' in str(relative):
        raise ValueError('unsafe export path')
    path=root/rel
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError('export path outside destination')
    current=path
    while True:
        if current.is_symlink():raise ValueError('symlink destination refused')
        if current==current.parent:break
        current=current.parent
    return path


def json_read(path, default=None):
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else default


def json_write(path, data):
    atomic_write(path,json.dumps(data,ensure_ascii=False,indent=2)+'\n')


def current_hash(path):
    return digest(exact_text(path)) if path.exists() else None


def payload(root, extra_pages=None):
    root=Path(root).resolve()
    files={}
    for path in sorted((root/'knowledge').rglob('*.md')):
        relative=path.relative_to(root).as_posix()
        if any(p.startswith('.') for p in path.relative_to(root/'knowledge').parts):continue
        safe=library_path(root,relative)
        if safe.stat().st_size>MAX_NOTE_BYTES:raise ValueError('oversized source note')
        files[relative]=exact_text(safe)
    for name in CONFIG_FILES:
        path=root/'config'/name
        if path.exists():
            if path.is_symlink() or path.stat().st_size>200000:raise ValueError('unsafe configuration export')
            text=exact_text(path);json.loads(text)
            files['config/'+name]=text
    if extra_pages:
        for relative,text in extra_pages.items():
            if not relative.startswith('knowledge/_VDN-') or not relative.endswith('.md'):
                raise ValueError('generated pages must use the reserved _VDN- prefix')
            files[relative]=text
    return files


def plan(root, destination, extra_pages=None):
    source=Path(root).resolve();destination=Path(destination).absolute()
    if source.is_relative_to(destination.resolve()) or destination.resolve().is_relative_to(source):
        raise ValueError('source and destination must be separate directories')
    safe_path(destination,'.vdn-sync/manifest.json')
    manifest=json_read(destination/'.vdn-sync/manifest.json',{'schema':'vdn.sync/9','files':{}})
    if manifest.get('schema')!='vdn.sync/9' or not isinstance(manifest.get('files'),dict):
        raise ValueError('invalid sync manifest')
    operations=[];conflicts=[];unchanged=0
    for relative,text in payload(root,extra_pages).items():
        path=safe_path(destination,relative)
        before=current_hash(path);after=digest(text);tracked=manifest['files'].get(relative)
        if before==after:
            unchanged+=1;continue
        if before is not None and (tracked is None or before!=tracked['hash']):
            conflicts.append({'path':relative,'reason':'untracked file or user changes','current_hash':before})
            continue
        operations.append({'path':relative,'before_hash':before,'after_hash':after,'content':text})
    pending=[]
    folder=safe_path(destination,'.vdn-sync/transactions')
    if folder.exists():
        for path in sorted(folder.glob('*.json')):
            record=json_read(safe_path(destination,path.relative_to(destination).as_posix()))
            if record['state'] in ('prepared','rolling_back'):pending.append(record['id'])
    return {'schema':'vdn.sync-plan/9','operations':operations,'conflicts':conflicts,
            'unchanged':unchanged,'pending':pending,'previous_manifest':manifest,'destination':str(destination)}


def _record_path(destination, identity):
    identity=str(uuid.UUID(identity))
    return safe_path(destination,f'.vdn-sync/transactions/{identity}.json')


def _resume(destination, record):
    path=_record_path(destination,record['id'])
    for op in record['operations']:
        allowed=(op['path'].startswith('knowledge/') and op['path'].endswith('.md')) or op['path'] in ['config/'+n for n in CONFIG_FILES]
        if not allowed or digest(op['content'])!=op['after_hash']:
            raise ValueError('transaction content integrity failure')
    if record['state']=='rolling_back':return _rollback(destination,record)
    conflicts=[]
    for op in record['operations']:
        target=safe_path(destination,op['path'])
        actual=current_hash(target)
        if actual not in (op['before_hash'],op['after_hash']):
            conflicts.append({'path':op['path'],'reason':'changed during interrupted synchronization'})
    if conflicts:return {'state':'conflict','conflicts':conflicts,'transaction':record['id']}
    for op in record['operations']:
        target=safe_path(destination,op['path'])
        if current_hash(target)==op['after_hash']:continue
        if current_hash(target)!=op['before_hash']:
            return {'state':'conflict','conflicts':[{'path':op['path'],'reason':'changed before write'}]}
        atomic_write(target,op['content'],create_only=op['before_hash'] is None)
    manifest={**record['previous_manifest'],'files':dict(record['previous_manifest']['files']),
              'last_transaction':record['id']}
    for op in record['operations']:manifest['files'][op['path']]={'hash':op['after_hash']}
    json_write(safe_path(destination,'.vdn-sync/manifest.json'),manifest)
    record['state']='committed';json_write(path,record)
    return {'state':'committed','transaction':record['id'],'written':len(record['operations']),
            'conflicts':[],'vault_path':str(Path(destination)/'knowledge')}


def sync(root, destination, *, apply=False, extra_pages=None):
    preview=plan(root,destination,extra_pages)
    if not apply:
        return {'state':'simulation',**{k:v for k,v in preview.items() if k not in ('previous_manifest','operations')},
                'operations':[{'path':o['path'],'action':'create' if o['before_hash'] is None else 'update'} for o in preview['operations']]}
    destination=Path(destination).absolute()
    with Lock(destination,7200):
        preview=plan(root,destination,extra_pages)
        if len(preview['pending'])>1:raise ValueError('multiple pending transactions require inspection')
        if preview['pending']:
            record=json_read(_record_path(destination,preview['pending'][0]))
            return {**_resume(destination,record),'resumed':True,'rerun_to_check_new_source_changes':True}
        if preview['conflicts']:return {'state':'conflict','written':0,'conflicts':preview['conflicts']}
        if not preview['operations']:return {'state':'unchanged','written':0,'conflicts':[],'transaction':None}
        identity=str(uuid.uuid4());ops=[]
        for index,op in enumerate(preview['operations']):
            target=safe_path(destination,op['path'])
            backup=None
            if op['before_hash'] is not None:
                if current_hash(target)!=op['before_hash']:
                    return {'state':'conflict','conflicts':[{'path':op['path'],'reason':'changed before backup'}]}
                backup=f'.vdn-sync/backups/{identity}/{index}.md'
                atomic_write(safe_path(destination,backup),exact_text(target),create_only=True)
            ops.append({**op,'backup':backup})
        record={'schema':'vdn.sync-transaction/9','id':identity,'state':'prepared',
                'operations':ops,'previous_manifest':preview['previous_manifest']}
        json_write(_record_path(destination,identity),record)
        return _resume(destination,record)


def _rollback(destination, record):
    conflicts=[]
    for op in record['operations']:
        target=safe_path(destination,op['path']);actual=current_hash(target)
        archive=safe_path(destination,f".vdn-sync/archives/{record['id']}/{op['path']}")
        reverted=(actual==op['before_hash'] and (op['before_hash'] is not None or current_hash(archive)==op['after_hash']))
        if actual!=op['after_hash'] and not reverted:conflicts.append({'path':op['path'],'reason':'modified after synchronization'})
    if conflicts:return {'state':'conflict','conflicts':conflicts,'transaction':record['id']}
    for op in record['operations']:
        if op['backup'] and current_hash(safe_path(destination,op['backup']))!=op['before_hash']:
            raise ValueError('backup integrity failure')
    record['state']='rolling_back';json_write(_record_path(destination,record['id']),record)
    for op in record['operations']:
        target=safe_path(destination,op['path'])
        if current_hash(target)==op['before_hash']:continue
        if op['backup']:
            backup=safe_path(destination,op['backup'])
            text=exact_text(backup)
            if digest(text)!=op['before_hash']:raise ValueError('backup integrity failure')
            atomic_write(target,text)
        else:
            archive=safe_path(destination,f".vdn-sync/archives/{record['id']}/{op['path']}")
            archive.parent.mkdir(parents=True,exist_ok=True)
            if archive.exists():raise ValueError('rollback archive already occupied')
            target.replace(archive)
    json_write(safe_path(destination,'.vdn-sync/manifest.json'),record['previous_manifest'])
    record['state']='rolled_back';json_write(_record_path(destination,record['id']),record)
    return {'state':'rolled_back','transaction':record['id'],'archives_retained':True,'conflicts':[]}


def rollback(destination, identity, *, apply=False):
    destination=Path(destination).absolute()
    record=json_read(_record_path(destination,identity))
    if record is None:raise ValueError('unknown transaction')
    if not apply:return {'state':'rollback_simulation','transaction':identity,'paths':[o['path'] for o in record['operations']]}
    with Lock(destination,7200):
        manifest=json_read(safe_path(destination,'.vdn-sync/manifest.json'),{})
        if record['state']=='rolled_back':return {'state':'rolled_back','transaction':identity,'unchanged':True}
        if manifest.get('last_transaction')!=identity and record['state']!='rolling_back':
            raise ValueError('only the latest committed transaction can be rolled back')
        return _rollback(destination,record)
