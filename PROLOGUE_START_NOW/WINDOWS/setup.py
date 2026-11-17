"""Portable starter checks. No install, quota change, service or Desktop edit."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sqlite3
import sys

ROOT=Path(__file__).resolve().parents[1]


def paths(root):
    root=Path(root).resolve();source=root/'Eponge/source';runtime=root/'Eponge/runtime'
    if verify(root)['state']!='PASS':raise ValueError('bundle integrity failed; no MCP process launched')
    for p in (source/'vdn_mcp.py',runtime/'project/prologue.json'):
        if not p.is_file() or p.is_symlink():raise ValueError('missing or unsafe bundle input: '+p.name)
    return source,runtime


def verify(root):
    root=Path(root).resolve();mp=root/'MANIFEST.json'
    if mp.is_symlink():raise ValueError('symlink manifest refused')
    manifest=json.loads(mp.read_text(encoding='utf-8'));bad=[];cache_changes=[]
    for name,row in manifest['files'].items():
        p=root/name
        if Path(name).is_absolute() or '..' in Path(name).parts or '\\' in name or ':' in name or not p.resolve().is_relative_to(root) or p.is_symlink():raise ValueError('unsafe manifest path')
        for parent in p.parents:
            if parent==root:break
            if parent.is_symlink():raise ValueError('symlink manifest ancestor refused')
        changed=not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']
        if changed and name=='Eponge/runtime/output/knowledge.db' and p.is_file():
            # Existing lexical retrieval may rebuild its DERIVED SQLite index
            # after relocation. Never treat this cache as trusted source data.
            try:
                with sqlite3.connect(p.as_uri()+'?mode=ro&immutable=1',uri=True) as db:
                    if db.execute('PRAGMA quick_check').fetchone()[0]!='ok':bad.append(name)
                    else:cache_changes.append(name)
            except sqlite3.Error:bad.append(name)
        elif changed:bad.append(name)
    return {'state':'FAIL' if bad else 'PASS','checked':len(manifest['files']),'changed_or_missing':bad,'derived_cache_changes':cache_changes,'scope':'immutable code/source integrity; changed derived index checked structurally, not promoted as source truth; not game validation'}


def doctor(root):
    source,runtime=paths(root);cfg=json.loads((runtime/'config/v10.json').read_text(encoding='utf-8'));ledger=json.loads((runtime/'lab/ocean/intelligence/compute.json').read_text(encoding='utf-8'))
    return {'state':'PARTIAL','platform':sys.platform,'python':sys.version.split()[0],'python_executable':sys.executable,'python_supported':sys.version_info>=(3,11),'source':str(source),'runtime':str(runtime),'integrity':verify(root),'agent_autonomy_enabled':cfg['autonomous_enabled'],'schedule_enabled':cfg['schedule']['enabled'],'compute_recorded':ledger,'compute_policy_s':cfg['research']['compute_budget_s'],'Claude_Desktop':'NOT_TESTED','Roblox_Studio':'NOT_TESTED','note':'Detection/configuration and MCP stdio do not validate the Desktop UI or a Studio session.'}


def config_candidate(root):
    if sys.platform!='win32':return {'state':'BLOCKED','reason':'Generate the candidate on target Windows to use its real Python path. No Desktop configuration changed.'}
    source,runtime=paths(root)
    if sys.version_info<(3,11):raise ValueError('Python3.11 or newer required')
    return {'state':'CANDIDATE_ONLY','configuration':{'mcpServers':{'eponge_prologue':{'command':sys.executable,'args':[str(source/'vdn_mcp.py'),'--root',str(runtime),'--v112'],'env':{'PYTHONUTF8':'1','PYTHONIOENCODING':'utf-8','PYTHONDONTWRITEBYTECODE':'1'}}}},'instructions':'Save a copy of the existing Desktop JSON, inspect name collisions, then merge this server manually. Never replace the entire existing mcpServers map.','Desktop_tested':False}


def test_mcp(root):
    source,runtime=paths(root);messages=[{'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2025-06-18','capabilities':{},'clientInfo':{'name':'prologue-start-now','version':'1'}}},{'jsonrpc':'2.0','method':'notifications/initialized'},{'jsonrpc':'2.0','id':2,'method':'tools/list'}]
    questions=['prologue:resources','learning:animation:7849ea8324d87ac30e9aa67ef731ba115041eaf014a31844a326b72557ae4523','learning:animation:86eb50f9e07e8a0a318473653c6a1c93ac47e3cab9b95167487e28cada88f632','tree:forest/spruce/foliage/cards/alpha/shadows/flashlight']
    messages += [{'jsonrpc':'2.0','id':i,'method':'tools/call','params':{'name':'get_intelligence_brief','arguments':{'question':q,'token_budget':500}}} for i,q in enumerate(questions,3)]
    messages.append({'jsonrpc':'2.0','id':7,'method':'tools/call','params':{'name':'synthesize_technical','arguments':{'question':'prologue:resources','apply':True}}})
    env=dict(os.environ);env.update(PYTHONUTF8='1',PYTHONIOENCODING='utf-8',PYTHONDONTWRITEBYTECODE='1')
    result=subprocess.run([sys.executable,'-B',str(source/'vdn_mcp.py'),'--root',str(runtime),'--v112'],input='\n'.join(json.dumps(m) for m in messages)+'\n',text=True,encoding='utf-8',capture_output=True,timeout=20,cwd=source,env=env,shell=False)
    if result.returncode or len(result.stdout)>1000000:raise ValueError('MCP process failed or output exceeded cap')
    rows=[json.loads(line) for line in result.stdout.splitlines()];tools=next(row['result']['tools'] for row in rows if 'tools' in row.get('result',{}));expected=json.loads((Path(root)/'PROOFS/mcp-contracts.json').read_text(encoding='utf-8'))
    if tools!=expected or len(tools)!=27:raise ValueError('MCP contract drift')
    calls={row['id']:row.get('result',{}) for row in rows if row.get('id') in (3,4,5,6,7)}
    if any(calls[i].get('isError') for i in (3,4,5,6)) or not calls[7].get('isError'):raise ValueError('read/permission contract failed')
    if calls[6]['structuredContent'].get('detail_question')!=questions[3]:raise ValueError('wrong forest microbranch')
    return {'state':'PASS','transport':'actual subprocess stdio','tools':len(tools),'briefs_read':4,'exact_forest_branch':questions[3],'write_denied':True,'Claude_Desktop':'NOT_TESTED','Studio':'NOT_TESTED','network_or_model_request':False}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['verify','doctor','config-candidate','test-mcp']);p.add_argument('--root',type=Path,default=ROOT);a=p.parse_args()
    try:
        fn={'verify':verify,'doctor':doctor,'config-candidate':config_candidate,'test-mcp':test_mcp}[a.command];r=fn(a.root);print(json.dumps(r,ensure_ascii=False,indent=2));return 2 if r['state'] in ('FAIL','BLOCKED') else 0
    except (OSError,ValueError,KeyError,StopIteration,subprocess.TimeoutExpired) as exc:
        print(json.dumps({'state':'BLOCKED','operation':a.command,'reason_type':type(exc).__name__,'message':'Check START_HERE.md and the bundle paths. No installation, permission or Desktop changes were attempted.'}));return 2


if __name__=='__main__':raise SystemExit(main())
