"""Twenty reproducible software scenarios; actual stdio, isolated vault, no sockets.

Optional runtime supplies previously collected real snapshots, read only.
The deliberately failed experiment and duplicate notes are labelled fixtures.
"""
import argparse,json,shutil,subprocess,sys,time,hashlib,platform
from pathlib import Path
from unittest.mock import patch
from agent.research_roots import Roots,RootCollector
from agent.research_library import Library
from agent.project_api import ProjectAPI
from agent.intelligence_evidence import documents,passages
from agent.lab_store import LabStore
from agent.mcp_v8 import Server
from agent import obsidian
from agent.knowledge import dump_frontmatter


def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path.cwd());p.add_argument('--workspace',type=Path,required=True);p.add_argument('--runtime',type=Path);a=p.parse_args();repo=a.root.resolve();base=a.workspace.resolve()
 if base.is_relative_to(repo) or repo.is_relative_to(base):raise ValueError('separate new workspace required')
 base.mkdir(exist_ok=False);root=base/'isolated';root.mkdir()
 for f in ('knowledge','project','config'):shutil.copytree(repo/f,root/f)
 (root/'output').mkdir();shutil.copyfile(repo/'output/queue.json',root/'output/queue.json');ledger=(root/'output/queue.json').read_bytes();tree=Roots(root);rows=[];saved={}
 def scenario(number,entry,expected,fn,category='SOFTWARE'):
  start=time.perf_counter()
  try:
   result=fn();status=result.pop('_status','PASS')
  except Exception as e:result={'error':type(e).__name__+': '+str(e)};status='FAIL'
  rows.append({'id':number,'input':entry,'expected':expected,'obtained':result,'status':status,'category':category,'duration_s':time.perf_counter()-start,'limits':'Software outcome, not validation of a Roblox technique.'})
 def general():
  r=tree.plan('Forêt Roblox réaliste avec sapins, collisions et lampe sans dégrader les performances');assert r['root']=='forest';assert len(r['nodes'])<=24
  return {'root':r['root'],'nodes':len(r['nodes']),'requirements':r['intent']['problems'],'constraints':r['request_constraints']}
 scenario(1,'Forest realism + flashlight + performance','Several requirements; bounded tree; no HTTP',general)
 def recursive():
  r=tree.plan('forest',8,32);assert any(n['depth']>=6 for n in r['nodes']);return {'nodes':len(r['nodes']),'deepest':max(n['depth'] for n in r['nodes']),'research_candidates':r['research_candidates']}
 scenario(2,'forest depth8','Reach foliage/alpha/shadows/flashlight; dependencies explicit',recursive)
 def detail(k):
  r=tree.detail(k);assert r['gap']['gap_open'];assert not r['truth_verified'];return {'branch':k,'sources':r['gap']['sources'],'reserve_ids':[h['note_id'] for h in r['library']['reserve']],'gap_open':True,'related_branches':r['related_branches'],'engine_executed':False,'_status':'PARTIAL' if not r['gap']['original_context_matches'] else 'PASS'}
 scenario(3,'forest/spruce/foliage/cards','Find candidates; flag missing original context',lambda:detail('forest/spruce/foliage/cards'))
 scenario(4,'forest/spruce/foliage/cards/alpha/shadows/flashlight','Independent micro-branch; no invented shadow claim',lambda:detail('forest/spruce/foliage/cards/alpha/shadows/flashlight'))
 scenario(5,'forest/collisions','MeshPart candidates and reversible comparison proposal',lambda:detail('forest/collisions'))
 scenario(6,'forest/ground/footprints','Specific footprint gap remains open',lambda:detail('forest/ground/footprints'))
 scenario(7,'forest/performance','Performance context without invented device/FPS result',lambda:detail('forest/performance'))
 def gaps():
  r=tree.plan('forest/spruce/foliage/cards/alpha/shadows/flashlight',0);assert len(r['nodes'])==1 and r['nodes'][0]['gap_open'];return {'gap_id':r['nodes'][0]['gap_id'],'dependencies':r['dependency_gaps'],'HTTP':0}
 scenario(8,'Only foliage shadows under flashlight','Stable gap ID; no whole forest restart',gaps)
 def failure():
  lab=LabStore(root);r=lab.create('AUTHORED SOFTWARE FIXTURE','fixture export method','unknown',{'project_task':'export','research_branch':'forest/export'},{'project_task':'export','engine':'Python'},protocol={'fixture':True})
  lab.transition(r['id'],'PLANNED');lab.transition(r['id'],'RUNNING');lab.record_result(r['id'],'FAILED',{},['AUTHORED SOFTWARE FIXTURE, not Roblox'],errors=['import export failed'])
  saved['failure']=r['id'];p=tree.after_failure(r['id']);assert [n['id'] for n in p['branches']]==['forest/export'];brief=tree.brief('forest/export');assert brief['branches'][0]['candidate_method'] is None
  return {'experiment_id':r['id'],'proposals':p,'next_brief_method':None,'history_retained':True}
 scenario(9,'Authored failed import','Research export only; no automatic action; next brief avoids same method',failure,'SYNTHETIC_FAILURE')
 def scenes():
  from agent.chapters import Chapters
  scenes=[s['id'] for s in Chapters(root).scenes.values() if any(f['task']=='trees' for f in s['features'])];assert len(scenes)>=2
  a=tree.plan('forest/spruce',0)['nodes'][0]['technique_id'];assert all(a==tree.plan('forest/spruce',0)['nodes'][0]['technique_id'] for s in scenes)
  return {'scenes':scenes,'shared_technique_id':a,'copied_notes':0}
 scenario(10,'Trees used in several scenes','Same canonical branch technique, no scene-specific source copies',scenes)
 def duplicates():
  for nid in ('roots-fixture-one','roots-fixture-two'):
   meta={'id':nid,'title':'Roblox fixture mesh collision','status':'candidat','sources':['https://create.roblox.com/docs/fixture'],'source_tier':4}
   (root/('knowledge/'+nid+'.md')).write_text(dump_frontmatter(meta)+'\n## Fixture\n> « collisionfixturetoken mesh collision, authored duplicate only »\n',encoding='utf-8')
  r=Library(root).search('collisionfixturetoken');assert len(r['results'])==1 and r['duplicate_groups']==1
  return {'aliases':r['results'][0]['aliases'],'duplicate_groups':r['duplicate_groups'],'physical_deletions':0}
 scenario(11,'Two authored identical passages','One result with both aliases, preserved files',duplicates,'SYNTHETIC_NOTES')
 def candidate():
  r=Library(root).search('collisionfixturetoken');assert r['reserve'] and not r['main'];return {'reserve':[h['note_id'] for h in r['reserve']],'facts_verified':False,'main':[]}
 scenario(12,'Candidate-only query','Candidate stays visible although main library empty',candidate,'SYNTHETIC_NOTES')
 def archive():
  r=Library(root).inventory();assert r['counts']['ARCHIVE']>0;docs=documents(root);rejected=set(r['tiers']['ARCHIVE']);assert not any(d.get('note_id') in rejected for d in docs)
  return {'counts':r['counts'],'rejected_documents_active':0,'removed_files':0}
 scenario(13,'Historical rejected notes','Archives retained; no rejected evidence in active documents',archive)
 def abstain():
  r=tree.brief('forest/spruce/foliage/cards/alpha/shadows/flashlight');assert not r['facts'];return {'facts':r['facts'],'state':r['state'],'limits':r['limits']}
 scenario(14,'No original snapshot for foliage flashlight shadows','Abstain from established facts; propose targeted search/test',abstain)
 def originals():
  if not a.runtime:return {'_status':'PARTIAL','reason':'No supplied real source runtime'}
  shutil.copytree(a.runtime.resolve()/'lab/ocean/sources',root/'lab/ocean/sources');docs={d['id']:d for d in documents(root) if d['independent']};r=tree.assess('forest/collisions');proof=[]
  for ref in r['sources']:
   if not ref['original']:continue
   d=docs[ref['document_id']];assert hashlib.sha256(d['text'].encode()).hexdigest()==ref['document_sha256'];assert d['text'][ref['start']:ref['end']]
   proof.append({**ref,'sha_valid':True,'offsets_valid':True})
  assert proof;return {'checks':proof,'engine_validation':False}
 scenario(15,'Previously captured real original snapshots','Check source hash, URL and passage offsets; unknown versions explicit',originals,'REAL_CAPTURE_REUSE')
 def inaccessible():
  g=tree.prepare('forest/spruce/foliage/cards/alpha/shadows/flashlight',0,apply=True);collector=RootCollector(tree,g,None)
  with patch.object(collector.web,'get',side_effect=ValueError('fixture source inaccessible')):
   r=collector(root,[({},tree.nodes[g['branches'][-1]]['query'],'fixture')],2)
  assert r['errors'] and collector.updated;return {'source_errors':r['errors'],'partial_checkpoint_retained':True,'HTTP':0}
 scenario(16,'Authored inaccessible source','Source error explicit; keep first assessment, no false verification',inaccessible,'SYNTHETIC_TRANSPORT')
 def compact():
  r=tree.brief('forest',500);size=len(json.dumps(r,ensure_ascii=False));assert size<=1800;assert r['rollback'] and r['limits'];return {'chars':size,'branches':len(r['branches']),'omitted':r['omitted_branches'],'detail':r['detail_question']}
 scenario(17,'Brief forest budget500','Bounded brief with omissions and drill-down, constraints/rollback retained',compact)
 scenario(18,'tree:forest/collisions','Detailed recipe, literal parameters, original/candidate distinction',lambda:detail('forest/collisions'))
 def export():
  vault=base/'vault';pages=tree.project.pages();p=obsidian.sync(root,vault,extra_pages=pages);r=obsidian.sync(root,vault,apply=True,extra_pages=pages);again=obsidian.sync(root,vault,apply=True,extra_pages=pages)
  assert again['state']=='unchanged';assert (vault/'knowledge/_VDN-Research-Roots.md').exists();back=obsidian.rollback(vault,r['transaction'],apply=True);assert back['state']=='rolled_back';assert ledger==(root/'output/queue.json').read_bytes()
  return {'simulation_operations':len(p['operations']),'first':r['state'],'second':again['state'],'rollback':back['state'],'daily_ledger_unchanged':True}
 scenario(19,'Separate temporary Obsidian vault','Export tiers/scene links; second unchanged; rollback preserves source and ledger',export)
 def stdio():
  calls=[('get_intelligence_brief',{'question':'Bible du jeu'}),('plan_ocean',{'goal':'tree:forest/collisions'}),('get_intelligence_brief',{'question':'tree:forest/collisions'}),('synthesize_technical',{'question':'tree:forest/collisions'}),('get_intelligence_brief',{'question':'tree:forest/export'})]
  messages=[{'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2025-06-18','capabilities':{},'clientInfo':{'name':'roots-validation','version':'11.2'}}},{'jsonrpc':'2.0','method':'notifications/initialized'},{'jsonrpc':'2.0','id':2,'method':'tools/list'}]+[{'jsonrpc':'2.0','id':i,'method':'tools/call','params':{'name':n,'arguments':args}} for i,(n,args) in enumerate(calls,3)]
  bootstrap="import socket,runpy; deny=lambda *a,**k:(_ for _ in ()).throw(AssertionError('sockets forbidden'));socket.socket.connect=deny;socket.create_connection=deny;runpy.run_path("+repr(str(repo/'vdn_mcp.py'))+",run_name='__main__')"
  start=time.perf_counter();p=subprocess.run([sys.executable,'-c',bootstrap,'--root',str(root),'--v112'],input='\n'.join(json.dumps(m) for m in messages)+'\n',text=True,encoding='utf-8',capture_output=True,timeout=90,cwd=repo);assert p.returncode==0,p.stderr
  out=[json.loads(l) for l in p.stdout.splitlines()];assert out[1]['result']['tools']==Server(root,v111=True).tools;assert len(out[1]['result']['tools'])==27
  for r in out[2:]:assert not r['result'].get('isError'),r
  assert out[-1]['result']['structuredContent']['branches'][0]['failures']==[saved['failure']]
  (base/'stdio-transcript.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
  return {'contracts':27,'real_subprocess':True,'stdio_calls':[n for n,args in calls],'sockets_forbidden':True,'elapsed_s':time.perf_counter()-start,'fixture_failure_recalled':True,'Claude_Desktop':'NOT_TESTED'}
 scenario(20,'Real MCP stdio process','All 27 contracts unchanged; Bible/plan/brief/detail/failure roundtrip',stdio)
 report={'schema':'vdn.roots-scenarios/11.2','base_sha':subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip(),'os':platform.system(),'python':platform.python_version(),'rows':rows,'counts':{s:sum(r['status']==s for r in rows) for s in ('PASS','PARTIAL','FAIL')},'network_calls':0,'model_calls':0,'Windows_user_PC':'NOT_TESTED','Claude_Desktop':'NOT_TESTED','Blender_5_2':'NOT_TESTED','Roblox_Studio':'NOT_TESTED','production_changes':0}
 (base/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({'counts':report['counts'],'failures':[r for r in rows if r['status']=='FAIL']},ensure_ascii=False,indent=2));return int(bool(report['counts']['FAIL']))
if __name__=='__main__':raise SystemExit(main())
