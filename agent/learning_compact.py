"""Lossless compaction of this laboratory's OWN_CREATED blend artifacts only.

No game/personal files, quota change, guard patch or reliable-memory promotion.
"""
import gzip
import hashlib
import json
from pathlib import Path
import shutil

from agent import intelligence_models as im
from agent.learning_store import capacity,digest,run_tool,save,sha,staged
from agent.lab_store import lab_lock
from agent.obsidian import safe_path


def pack(data):
    if not data.startswith(b'BLENDER') or len(data)>8_000_000:raise ValueError('bounded uncompressed native blend required')
    result=gzip.compress(data,mtime=0)
    if gzip.decompress(result)!=data or len(result)>=len(data):raise ValueError('lossless size reduction not demonstrated')
    return result


def compact(root,relative,own_created=False):
    if own_created is not True or not relative.startswith('lab/inbox/learning/'):raise PermissionError('explicit OWN_CREATED learning artifact only')
    root=Path(root).resolve();source=staged(root,relative,('.blend',));binary=shutil.which('blender')
    if not binary:raise RuntimeError('Blender unavailable')
    before=sha(source);key=digest(['blend-gzip-1',relative,before]);folder='lab/learning/compact/'+key
    with lab_lock(root,'.learning-compact'):
        journal=safe_path(root,folder+'/journal.json')
        if journal.exists():raise ValueError('previous compaction retained; inspect journal before retry')
        raw=source.read_bytes();packed=pack(raw);capacity(root,len(packed)+10000)
        candidate=source.with_name(source.stem+'-gzip-candidate.blend')
        if candidate.exists():raise ValueError('candidate collision; preserve it')
        safe_path(root,folder).mkdir(parents=True);candidate.write_bytes(packed)
        record={'schema':'vdn.generated-compaction/1','state':'PREPARED','source':relative,'source_sha256_before':before,'source_bytes_before':len(raw),'candidate':candidate.relative_to(root).as_posix(),'packed_sha256':sha(candidate),'packed_bytes':len(packed),'codec':'GZIP_ENVELOPE','old_bytes_restorable_exactly':True,'permission':'operator OWN_CREATED only','promoted_reliable_memory':False}
        save(root,folder+'/journal.json',record)
        def work():
            # Fixed probe code, solely our own staged candidate; no downloaded script.
            code='import bpy,json; bpy.ops.wm.open_mainfile(filepath='+json.dumps(str(candidate))+',load_ui=False,use_scripts=False); print("OWN_BLEND_READ_OK",len(bpy.context.scene.objects),len(bpy.data.actions))'
            execution=run_tool(root,[binary,'--background','--factory-startup','--disable-autoexec','--threads','1','--python-exit-code','2','--python-expr',code],folder+'/independent-load.log',timeout=8,max_bytes=64000)
            if 'OWN_BLEND_READ_OK' not in safe_path(root,folder+'/independent-load.log').read_text():raise ValueError('no independent Blender load proof')
            if sha(source)!=before or hashlib.sha256(gzip.decompress(candidate.read_bytes())).hexdigest()!=before:raise ValueError('source or lossless candidate changed')
            # Atomic replacement changes the container, not the recoverable bytes.
            # PREPARED journal suffices to diagnose a crash before COMMITTED.
            candidate.replace(source)
            record.update(state='COMMITTED',source_sha256_after=sha(source),execution=execution,bytes_saved=len(raw)-len(packed),saved_fraction=1-len(packed)/len(raw),source_still_exactly_restorable=hashlib.sha256(gzip.decompress(source.read_bytes())).hexdigest()==before)
            save(root,folder+'/journal.json',record);return record
        return im.operation(root,work)
