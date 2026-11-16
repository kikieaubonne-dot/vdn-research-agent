"""Explicit Windows-compatible Océan operations. Mutations default to simulation."""
import argparse
import json
import platform
from pathlib import Path
import shutil
import subprocess
import sys
import time
from agent import obsidian,gaps,lab_plan,ocean_knowledge,ocean_lab
from agent.ocean import Ocean
from agent.ocean_api import OceanAPI,pages
from agent.ocean_web import settings
from agent.research_session import config as v10_config
from agent.lab_store import clean_json,lab_lock
from agent.obsidian import safe_path
from agent.storage import atomic_write


def hardware():
    result={'platform':platform.platform(),'python':platform.python_version(),'cpu':platform.processor(),
            'gpu':None,'memory_bytes':None,'model_fit':'not measured; weights, KV cache, context and runtime overhead must all fit'}
    try:
        if sys.platform=='win32':
            import ctypes
            class Memory(ctypes.Structure):
                _fields_=[('length',ctypes.c_ulong),('load',ctypes.c_ulong)]+[(n,ctypes.c_ulonglong) for n in ('total','available','page_total','page_available','virtual_total','virtual_available','extended')]
            info=Memory();info.length=ctypes.sizeof(info)
            if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(info)):result['memory_bytes']=info.total
        else:
            import os
            result['memory_bytes']=os.sysconf('SC_PAGE_SIZE')*os.sysconf('SC_PHYS_PAGES')
        if shutil.which('nvidia-smi'):
            r=subprocess.run(['nvidia-smi','--query-gpu=name,memory.total','--format=csv,noheader,nounits'],capture_output=True,text=True,timeout=3)
            if r.returncode==0:result['gpu']=r.stdout.strip()[:300]
    except (OSError,ValueError,subprocess.TimeoutExpired):pass
    return result


def tick(root,mode='autonomous',apply=False,allow_network=False):
    cfg=v10_config(root);ocfg=settings(root)
    if not apply:return {'state':'simulation','network_requests':0}
    if not ocfg['enabled'] or not cfg['autonomous_enabled'] or mode=='scheduled' and not cfg['schedule']['enabled']:return {'state':'disabled','network_requests':0}
    runtime=safe_path(root,'lab/ocean/scheduler.json')
    with lab_lock(root,'.ocean-scheduler'):
        previous=json.loads(runtime.read_text(encoding='utf-8')) if runtime.exists() else {'last_tick':0}
        now=time.time()
        if mode=='scheduled' and now-previous['last_tick']<cfg['schedule']['interval_s']:return {'state':'not_due'}
        atomic_write(runtime,clean_json({'last_tick':now}))
        ocean=Ocean(root)
        for g in ocean.list():
            if g['control']!='READY' or g['status'] in ('COMPLETE','ERROR','BLOCKED','stopped'):continue
            if g.get('stop_details',{} ) and g['stop_details'].get('scope')=='session':continue
            return ocean.advance(g['id'],apply=True,allow_network=allow_network)
        return {'state':'no_authorized_goal','hint':'prepare one general goal explicitly; no autonomous creation of unapproved goals'}


def main(argv=None):
    if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    sub=p.add_subparsers(dest='cmd',required=True)
    def cmd(name,write=False):
        s=sub.add_parser(name)
        if write:
            flags=s.add_mutually_exclusive_group();flags.add_argument('--apply',action='store_true');flags.add_argument('--dry-run',action='store_true')
        return s
    s=cmd('plan');s.add_argument('goal')
    s=cmd('prepare',True);s.add_argument('goal');s.add_argument('--goal-id');s.add_argument('--provider')
    s=cmd('adopt',True);s.add_argument('id')
    s=cmd('run',True);s.add_argument('id');s.add_argument('--allow-network',action='store_true')
    s=cmd('control',True);s.add_argument('id');s.add_argument('action',choices=['pause','resume','stop'])
    cmd('status');cmd('hardware');cmd('legacy-view')
    s=cmd('tick',True);s.add_argument('--mode',choices=['autonomous','scheduled'],default='autonomous');s.add_argument('--allow-network',action='store_true')
    s=cmd('search');s.add_argument('query');s.add_argument('--limit',type=int,default=5);s.add_argument('--semantic',action='store_true')
    s=cmd('semantic-index',True);s.add_argument('--max-items',type=int,default=4)
    s=cmd('brief');s.add_argument('goal');s.add_argument('--token-budget',type=int,default=1800)
    s=cmd('card');s.add_argument('id');s.add_argument('--detailed',action='store_true')
    s=cmd('sync',True);s.add_argument('--destination',type=Path,required=True);s.add_argument('--rollback');s.add_argument('--include-lab',action='store_true')
    s=cmd('lab-prepare',True);s.add_argument('--batch',default='B3-C1')
    s=cmd('lab-import',True);s.add_argument('path')
    s=cmd('lab-compare');s.add_argument('first');s.add_argument('second')
    a=p.parse_args(argv);ocean=Ocean(a.root);api=OceanAPI(a.root)
    try:
        if a.cmd=='plan':r=ocean.prepare(a.goal)
        elif a.cmd=='prepare':r=ocean.prepare(a.goal,apply=a.apply,goal_id=a.goal_id,provider=a.provider)
        elif a.cmd=='adopt':r=ocean.adopt(a.id,apply=a.apply)
        elif a.cmd=='run':r=ocean.advance(a.id,apply=a.apply,allow_network=a.allow_network)
        elif a.cmd=='control':r=ocean.control(a.id,a.action,apply=a.apply)
        elif a.cmd=='status':r=api.ocean_status()
        elif a.cmd=='hardware':r=hardware()
        elif a.cmd=='legacy-view':r={'notes':ocean_knowledge.legacy_view(a.root),'writes':0}
        elif a.cmd=='search':r=api.search_ocean(a.query,a.limit,a.semantic)
        elif a.cmd=='semantic-index':
            from agent.ocean_semantic import index
            r=index(a.root,a.apply,a.max_items)
        elif a.cmd=='brief':r=api.get_ocean_brief(a.goal,a.token_budget)
        elif a.cmd=='card':r=api.get_ocean_card(a.id,a.detailed)
        elif a.cmd=='tick':r=tick(a.root,a.mode,a.apply,a.allow_network)
        elif a.cmd=='sync':
            r=obsidian.rollback(a.destination,a.rollback,apply=a.apply) if a.rollback else obsidian.sync(a.root,a.destination,apply=a.apply,extra_pages={**gaps.pages(a.root),**(lab_plan.pages(a.root) if a.include_lab else {}),**pages(a.root,a.include_lab)})
        elif a.cmd=='lab-prepare':r=ocean_lab.prepare(a.root,a.batch,apply=a.apply)
        elif a.cmd=='lab-import':r=ocean_lab.import_blender(a.root,a.path,a.apply)
        elif a.cmd=='lab-compare':r=ocean_lab.compare(a.root,a.first,a.second)
        else:raise ValueError('unknown command')
    except (ValueError,OSError,KeyError,TypeError,RuntimeError) as exc:
        print(json.dumps({'error':str(exc) if isinstance(exc,(ValueError,PermissionError)) else type(exc).__name__},ensure_ascii=False));return 2
    print(json.dumps(r,ensure_ascii=False,indent=2,allow_nan=False));return 1 if r.get('state') in ('ERROR','conflict') or r.get('error') else 0


if __name__=='__main__':raise SystemExit(main())
