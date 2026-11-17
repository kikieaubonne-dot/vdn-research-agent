"""One explicitly approved, bounded forest mission, reusing the existing worker.

Not the default worker, service or an automatic stable-code promotion.
"""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys
from agent import intelligence_models as im
from agent.lab_store import LabStore
from agent.learning_store import capacity,run_tool,save,load,receipt,sha
from agent.mission import Worker,write,REPOSITORY


def judge(generated,imported):
    rows=[]
    for before in generated['rows']:
        after=next(r for r in imported['rows'] if r['profile']==before['profile'] and r['method']==before['method']);issues=[]
        reference=before.get('native_reference',{});valid_source=reference.get('white_faces',0)>0 and reference.get('green_faces',0)>0
        if not valid_source:issues.append('native_reference_not_discriminating')
        if before['triangles']!=after['triangles']:issues.append('geometry_changed')
        if not after['white_material_factor'] or not after['needle_green_material_factor']:issues.append('snow_or_needles_color_not_encoded_as_plain_material')
        if after['textures']:issues.append('texture_semantics_require_review')
        rows.append({'profile':before['profile'],'method':before['method'],'state':'INVALID_NATIVE_COMPARISON' if not valid_source else 'PASS_LIMITED_GLTF' if not issues else 'REJECTED_FOR_THIS_EXPORT','issues':issues,'native':before,'imported':after})
    selected=[]
    for profile in ('primary','transfer'):
        eligible=[r for r in rows if r['profile']==profile and r['state']=='PASS_LIMITED_GLTF'];eligible.sort(key=lambda r:r['native']['triangles']);selected.append({'profile':profile,'selected_for_next_engine_test':eligible[0]['method'] if eligible else None,'reason':'minimum triangles among methods retaining declared material factors; NOT artistic/game approval'})
    return {'rows':rows,'selection':selected,'human_approved':False,'Roblox':'NOT_TESTED','realism':'INCONCLUSIVE','scope':'material-factor portability and geometry, not rendered equivalence or engine performance'}


class ForestWorker(Worker):
    def research(self):
        from agent.research_roots import Roots
        from agent.research_queue import ResearchQueue
        from agent.research_session import config
        ceiling=config(self.root)['research']['max_http_calls'];cap=min(8,self.cfg['max_http_calls'])
        if self.cfg['allow_network'] and ceiling>cap:
            return {'state':'SESSION_DOES_NOT_FIT_MISSION_BUDGET','http_calls':0,'session_ceiling':ceiling,'mission_ceiling':cap}
        tree=Roots(self.root)
        if not self.cfg['allow_network']:return {'state':'OFFLINE_MEMORY_ONLY','plan':tree.plan('forest/spruce')}
        before=ResearchQueue(self.root,recover=False).daily()['http_calls'];results=[]
        for branch in ('forest/spruce/snow','forest/spruce/materials'):
            # Refuse before a session can spend beyond the remaining grant.
            # Do not rewrite its quotas or rely on an after-the-fact assertion.
            if ceiling>cap-(ResearchQueue(self.root,recover=False).daily()['http_calls']-before):break
            prepared=tree.prepare('tree:'+branch,apply=True)
            if 'id' not in prepared:results.append({'branch':branch,'state':prepared['state']});continue
            result=tree.run(prepared['id'],True,True);results.append({'branch':branch,'session':prepared['id'],'state':result['state'],'errors':result.get('errors',[]),'sources_context':[r['status'] for r in result.get('remaining_gaps',[])]});write(self.workspace,'reports/forest-research.json',{'rows':results})
        used=ResearchQueue(self.root,recover=False).daily()['http_calls']-before
        if used>cap:raise ValueError('mission HTTP allowance exceeded')
        return {'state':'BOUNDED_COLLECTION_PARTIAL','http_calls':used,'rows':results,'verified_game_knowledge_created':0}
    def blender_lab(self):
        if not self.cfg['allow_blender']:raise PermissionError('Blender permission required')
        binary=shutil.which('blender')
        if not binary:raise RuntimeError('Blender unavailable')
        script=REPOSITORY/'scripts/blender_snow_portability.py';folder='lab/inbox/learning/snow-portability-'+self.checkpoint['id'];path=self.root/folder
        if path.exists():raise ValueError('previous trial retained; no identical automatic retry')
        spec={'schema':'vdn.snow-portability-spec/1','seed':13,'profiles':['primary','transfer'],'proposed_lab_dimensions_m':{'primary_height':3,'transfer_height':1.8},'methods':['caps','procedural'],'snow_mask_threshold':.98,'hypothesis':'Material-only snow may reduce geometry but may fail procedural-color export; geometry caps are a predefined fallback, not a code auto-patch.','criteria':{'native_reference_both_color_classes':True,'triangle_count_preserved':True,'imported_white_and_green_material_factors':True,'texture_present':'requires human review; not automatically accepted'},'controls':{'camera':[3.7,-5.5,3],'light':[2,-3,4],'resolution':256,'samples':2,'renderer':'Cycles CPU','threads':1},'licence':'OWN_CREATED','script_sha256':sha(script),'Roblox':'NOT_TESTED','realism':'INCONCLUSIVE','research_branch':'forest/spruce/snow'}
        lab=LabStore(self.root);experiments=[]
        for profile in spec['profiles']:
            for method in spec['methods']:
                e=lab.create('Snowy spruce owned research proxy '+profile,method,spec['hypothesis'],parameters={'project_task':'trees','research_branch':'forest/spruce/snow','method':method,'asset_ids':['owned-snow-'+profile]},environment={'engine':'Blender','expected_version':'4.3.2','asset_ids':['owned-snow-'+profile]},protocol=spec);lab.transition(e['id'],'PLANNED');lab.transition(e['id'],'RUNNING');experiments.append((profile,method,e['id']))
        def work():
            capacity(self.root,2500000);path.mkdir(parents=True);save(self.root,folder+'/spec.json',spec);args=[binary,'--background','--factory-startup','--disable-autoexec','--threads','1','--python-exit-code','2','--python',str(script),'--','--folder',folder]
            generation=run_tool(self.root,args+['--phase','generate'],folder+'/generation.log',timeout=16);inspection=run_tool(self.root,args+['--phase','inspect'],folder+'/inspection.log',timeout=4);generated=load(self.root,folder+'/generated.json');imported=load(self.root,folder+'/imported.json');decision=judge(generated,imported);save(self.root,folder+'/decision.json',decision);capacity(self.root)
            artifact=lab.import_artifact(folder+'/decision.json')
            for profile,method,eid in experiments:
                row=next(r for r in decision['rows'] if r['profile']==profile and r['method']==method);status='PARTIAL_SUCCESS' if row['state']=='PASS_LIMITED_GLTF' else 'FAILED';lab.record_result(eid,status,{'triangles':row['native']['triangles'],'glb_bytes':row['native']['glb_bytes']},['Actual native generation and independent Blender import.','A predefined alternative can be selected only when its own export gate passes.'],errors=row['issues'] if status=='FAILED' else [],artifacts=[artifact['id']],limits=['No artistic approval, Studio, target device, actual B3/C1 or wind validation.'])
            result={'state':'PARTIAL_SUCCESS' if any(s['selected_for_next_engine_test'] for s in decision['selection']) else 'FAILED','decision':decision,'folder':folder,'generation':generation,'inspection':inspection,'experiment_ids':[e[2] for e in experiments],'auto_correction':'selection among predefined candidates, no autonomous code patch'};write(self.workspace,'reports/forest-experiment.json',result);return result
        try:return im.operation(self.root,work)
        except Exception as exc:
            for _,_,eid in experiments:
                if lab.get(eid)['status']=='RUNNING':lab.record_result(eid,'FAILED',{},['Actual attempt interrupted or failed; artifacts retained'],errors=[type(exc).__name__],limits=['No successful experiment inferred.'])
            raise
    def export(self):
        from agent import obsidian,lab_plan
        from agent.project_work import Project
        from agent.research_roots import Roots
        experiment=load(self.workspace,'reports/forest-experiment.json') if (self.workspace/'reports/forest-experiment.json').exists() else {'state':'BLOCKED'}
        pages={**Project(self.root).pages(),**lab_plan.pages(self.root),**Roots(self.root).pages(),'knowledge/_VDN-SnowPortability.md':'# Snow portability — PARTIAL, not Studio/artistic validation\n\n'+json.dumps(experiment,ensure_ascii=False,indent=2)+'\n'}
        vault=self.workspace/'vault';first=obsidian.sync(self.root,vault,apply=True,extra_pages=pages);again=obsidian.sync(self.root,vault,apply=True,extra_pages=pages)
        if again['state']!='unchanged':raise ValueError('duplicate export')
        return {'state':'OBSIDIAN_SYNC_VERIFIED','files':first.get('written',0),'transaction':first.get('transaction'),'repeat':again['state'],'personal_vault':False,'retained_publication':True}
    def mcp(self):
        messages=[{'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2025-06-18','capabilities':{},'clientInfo':{'name':'forest-mission','version':'1'}}},{'jsonrpc':'2.0','id':2,'method':'tools/list'},{'jsonrpc':'2.0','id':3,'method':'tools/call','params':{'name':'get_intelligence_brief','arguments':{'question':'tree:forest/spruce/snow','token_budget':1000}}},{'jsonrpc':'2.0','id':4,'method':'tools/call','params':{'name':'get_experiment_context','arguments':{'problem':'Snowy spruce','limit':5,'detailed':True}}}]
        p=subprocess.run([sys.executable,'-B',str(REPOSITORY/'vdn_mcp.py'),'--root',str(self.root),'--v112'],input='\n'.join(json.dumps(m) for m in messages)+'\n',capture_output=True,text=True,encoding='utf-8',timeout=45);rows=[json.loads(l) for l in p.stdout.splitlines()]
        if p.returncode or len(rows)!=4 or len(rows[1]['result']['tools'])!=27 or any('error' in r or r.get('result',{}).get('isError') for r in rows):raise ValueError('mission MCP contract/retrieval failed')
        if rows[2]['result']['structuredContent'].get('detail_question')!='tree:forest/spruce/snow':raise ValueError('wrong branch retrieved')
        write(self.workspace,'reports/mcp.json',rows);return {'state':'MCP_REAL_STDIO_VERIFIED','tools':27,'forest_microbranch':'tree:forest/spruce/snow','experiment_context_read':True,'Claude_Desktop':'NOT_TESTED'}


def main():
    # This entry is used only in the mission's frozen copy. Existing guard,
    # permissions, checkpoint validation and stop behavior are unchanged.
    from agent import mission
    mission.Worker=ForestWorker
    return mission.main()


if __name__=='__main__':raise SystemExit(main())
