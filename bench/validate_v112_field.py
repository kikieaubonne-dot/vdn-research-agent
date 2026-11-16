"""Isolated software validation with real stdio and prior captures, no engine execution.

The failure records created here are authored fixtures. A new workspace is
required, sockets are forbidden, and the runtime sources are read only.
"""
import json,shutil,subprocess,sys,hashlib,time,platform
from pathlib import Path
from agent.project_work import Project
from agent.lab_store import LabStore
from agent.intelligence_evidence import documents
from agent import obsidian,lab_plan
from agent.corpus import scan_notes


def main():
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repository',type=Path,default=Path.cwd());p.add_argument('--workspace',type=Path,required=True);p.add_argument('--runtime',type=Path,required=True);a=p.parse_args()
 REPO=a.repository.resolve();BASE=a.workspace.resolve()
 if BASE.is_relative_to(REPO) or REPO.is_relative_to(BASE):raise ValueError('validation workspace must be separate from repository')
 BASE.mkdir(exist_ok=False);root=BASE/'isolated';root.mkdir()
 for folder in ('knowledge','config','project'):shutil.copytree(REPO/folder,root/folder)
 (root/'output').mkdir();shutil.copyfile(REPO/'output/queue.json',root/'output/queue.json');ledger=(root/'output/queue.json').read_bytes()
 bootstrap="import ssl,socket,runpy,sys; sys.path.insert(0,"+repr(str(REPO))+");  deny=lambda *a,**k: (_ for _ in ()).throw(RuntimeError('network forbidden in field software validation')); socket.socket=deny; socket.create_connection=deny; socket.getaddrinfo=deny; runpy.run_path("+repr(str(REPO/'vdn_mcp.py'))+",run_name='__main__')"
 transcripts=[]
 def rpc(calls,writes=False):
  messages=[{'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2025-06-18','capabilities':{},'clientInfo':{'name':'field-continuity-validation','version':'11.2'}}},{'jsonrpc':'2.0','method':'notifications/initialized'}]
  for i,(name,args) in enumerate(calls,2):messages.append({'jsonrpc':'2.0','id':i,'method':'tools/list'} if name=='LIST' else {'jsonrpc':'2.0','id':i,'method':'tools/call','params':{'name':name,'arguments':args}})
  start=time.perf_counter();p=subprocess.run([sys.executable,'-c',bootstrap,'--root',str(root),'--v112']+(['--allow-experiments'] if writes else []),input='\n'.join(json.dumps(m) for m in messages)+'\n',text=True,encoding='utf-8',capture_output=True,timeout=30,cwd=BASE)
  assert p.returncode==0,p.stderr
  rows=[json.loads(l) for l in p.stdout.splitlines()];assert len(rows)==len(calls)+1
  assert rows[0]['result']['serverInfo']['version']=='11.2.0'
  results=[]
  for row,(name,args) in zip(rows[1:],calls):
   assert 'error' not in row,row
   value=row['result'];assert not value.get('isError'),value
   results.append(value if name=='LIST' else value['structuredContent'])
  transcripts.append({'tools':[c[0] for c in calls],'elapsed_s':time.perf_counter()-start,'real_process':True,'sockets_forbidden':True,'results':results})
  return results
 archive=Project(root).latest('collisions');listed,bible,brief,detail=rpc([('LIST',{}),('get_intelligence_brief',{'question':'Bible du jeu'}),('get_intelligence_brief',{'question':'collisions'}),('get_intelligence_analysis',{'key':archive['key']})])
 assert len(listed['tools'])==27;assert bible['project']['kind']=='bible';assert brief['abstained_from_established_facts'];assert not detail['facts'];assert not detail['project_card']['parameters']
 # Original captures reused from the previous authorized isolated acquisition.
 source=a.runtime.resolve()/'lab/ocean/sources';shutil.copytree(source,root/'lab/ocean/sources')
 project=Project(root);card=project.synthesize('collisions',True)
 brief,detail=rpc([('get_intelligence_brief',{'question':'collisions'}),('get_intelligence_analysis',{'key':card['key']})])
 assert card['quality']['facts'];assert not brief['abstained_from_established_facts'];proofs=[]
 docs={d['id']:d for d in documents(root)}
 for ref in card['sources']:
  d=docs[ref['document_id']];assert hashlib.sha256(d['text'].encode()).hexdigest()==ref['document_sha256']
  passage=next(p for p in detail['passages'] if p['id']==ref['id']);assert passage['text']==d['text'][ref['start']:ref['end']]
  proofs.append({**ref,'sha_and_offsets_valid':True,'truncated':d['truncated'],'retrieved_at':d['retrieved_at']})
 first_bytes=project.path('cards/'+card['key']+'.json').read_bytes()
 spec={'problem':'Authored continuity fixture; NOT a Roblox experiment','technique':'fixture collider method','hypothesis':'Test failure propagation, no engine execution','parameters':{'project_task':'collisions','test_kind':'AUTHORED_SOFTWARE_FIXTURE'},'environment':{'project_task':'collisions','engine':'Python','engine_version':platform.python_version(),'asset_ids':[]},'protocol':{'executed_in_roblox':False,'fixture':True}}
 created=rpc([('prepare_experiment',spec)],True)[0]
 started=rpc([('start_experiment',{'experiment_id':created['id'],'expected_revision':created['revision']})],True)[0]
 failed=rpc([('record_experiment_result',{'experiment_id':created['id'],'status':'FAILED','metrics':{},'observations':['AUTHORED FIXTURE; no Studio, no actual B3/C1 result'],'errors':['fixture blocked path'],'limits':['Software memory propagation test only']})],True)[0]
 after,analysis=rpc([('get_intelligence_brief',{'question':'collisions'}),('synthesize_technical',{'question':'collisions','apply':False})])
 assert after['project']['readiness']=='BLOCKED';assert not after['project']['implementation'];assert analysis['project_card']['quality']['failures']
 assert project.get(card['key'])['inputs_obsolete'];assert first_bytes==project.path('cards/'+card['key']+'.json').read_bytes()
 # Different conditions may be proposed explicitly; the old failure is retained.
 new={**spec,'parameters':{**spec['parameters'],'conditions_change':'AUTHORED DIFFERENT METHOD'},'technique':'fixture alternative method'}
 newrecord=rpc([('prepare_experiment',new)],True)[0];assert newrecord['id']!=created['id'];assert newrecord['status']=='PLANNED'
 # Export includes the lab memory explicitly, never the personal vault.
 vault=BASE/'vault';pages={**project.pages(),**lab_plan.pages(root)}
 preview=obsidian.sync(root,vault,extra_pages=pages);applied=obsidian.sync(root,vault,apply=True,extra_pages=pages);again=obsidian.sync(root,vault,apply=True,extra_pages=pages)
 assert applied['state']=='committed';assert again['state']=='unchanged'
 assert {n['id'] for n in scan_notes(vault)}=={n['id'] for n in scan_notes(root)}
 assert 'FAILED' in (vault/('knowledge/_VDN-Experience-'+created['id']+'.md')).read_text()
 rollback=obsidian.rollback(vault,applied['transaction'],apply=True);assert rollback['state']=='rolled_back',rollback
 assert ledger==(root/'output/queue.json').read_bytes()
 report={'schema':'vdn.field-software-validation/11.2','base_sha':subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),'product_code_sha256':{'agent/project_work.py':hashlib.sha256((REPO/'agent/project_work.py').read_bytes()).hexdigest()},'python':platform.python_version(),'os':platform.system(),'state':'PARTIAL','MCP_stdio':'EXECUTED_REAL_PROCESSES','MCP_tools':27,'network_calls':0,'model_calls':0,'Windows_user_PC':'NOT_AVAILABLE','Claude_Desktop':'NOT_AVAILABLE','Roblox_Studio':'NOT_AVAILABLE','B3_C1_assets':'NOT_AVAILABLE','original_source_checks':proofs,'archive_without_originals_abstains':True,'fixture_failure_propagates':True,'historical_card_preserved':True,'new_conditions_can_be_planned':True,'Obsidian':{'preview':preview['state'],'apply':applied['state'],'second_export':again['state'],'rollback':rollback['state'],'generated_pages_excluded_from_RAG':True},'daily_ledger_unchanged':True,'experiment_provenance':'AUTHORED SOFTWARE FIXTURES ONLY; no real engine result','stdio_calls':[{'tools':t['tools'],'elapsed_s':t['elapsed_s'],'sockets_forbidden':True} for t in transcripts]}
 (BASE/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 (BASE/'private-transcripts.json').write_text(json.dumps(transcripts,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
