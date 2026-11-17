"""Run only isolated software checks; creates no real Studio experiment."""
import argparse,hashlib,json,os,shutil,subprocess,sys,tempfile
from pathlib import Path

NOTE='vdn-c2b-trunk-colliders-h001-h002'

def run(source,handoff):
    with tempfile.TemporaryDirectory(prefix='vdn-handoff-check-') as d:
        d=Path(d);root=d/'root';root.mkdir()
        for name in ('config','project'):
            original=source/('tests/fixtures/config' if name=='config' else 'project')
            shutil.copytree(original,root/name)
        (root/'knowledge').mkdir();shutil.copyfile(handoff/'knowledge/forest/c2b-h001-h002-collisions-troncs.md',root/'knowledge/candidate.md')
        initial={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for name in ('config','knowledge','project') for p in (root/name).rglob('*') if p.is_file()}
        deny=d/'deny';deny.mkdir();(deny/'sitecustomize.py').write_text("import socket\ndef deny(*a,**k): raise AssertionError('offline handoff check: no sockets')\nsocket.socket.connect=deny\nsocket.create_connection=deny\n")
        env=dict(os.environ);env.update(PYTHONPATH=str(deny),PYTHONUTF8='1',PYTHONIOENCODING='utf-8',PYTHONDONTWRITEBYTECODE='1')
        def batch(requests,writes=False):
            hello={'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2025-06-18','capabilities':{},'clientInfo':{'name':'SYNTHETIC_HANDOFF_SOFTWARE_CHECK','version':'1'}}}
            cmd=[sys.executable,'-B',str(source/'vdn_mcp.py'),'--root',str(root),'--v112']+(['--allow-experiments'] if writes else [])
            p=subprocess.run(cmd,input='\n'.join(json.dumps(x) for x in [hello]+requests)+'\n',capture_output=True,text=True,encoding='utf-8',timeout=40,cwd=source,env=env)
            if p.returncode:raise AssertionError('MCP child failed: '+p.stderr[-300:])
            rows=[json.loads(l) for l in p.stdout.splitlines()]
            assert len(rows)==len(requests)+1
            return {r['id']:r for r in rows}
        def call(i,name,args):return {'jsonrpc':'2.0','id':i,'method':'tools/call','params':{'name':name,'arguments':args}}
        initial_reads=batch([{'jsonrpc':'2.0','id':2,'method':'tools/list'},call(3,'search_knowledge',{'query':'C2B H001 H002 collisions sapin','top_k':3,'token_budget':1800}),call(4,'find_procedures',{'task':'C2B H001 H002 collisions sapin','top_k':3}),call(5,'get_knowledge',{'note_id':NOTE}),call(6,'prepare_experiment',{'problem':'SYNTHETIC_FIXTURE','technique':'fixture','hypothesis':'not a real Studio run'})])
        assert len(initial_reads[2]['result']['tools'])==27
        for i in (3,4,5):
            assert not initial_reads[i]['result'].get('isError'),initial_reads[i]
            assert NOTE in json.dumps(initial_reads[i]),'candidate not returned'
        assert initial_reads[6]['result']['isError'],'write must be refused by default'
        preparations=[]
        for i,label in enumerate(('B1','B2','B3'),10):
            data=json.loads((handoff/f'handoff/collisions_sapin/prepare_{label}.json').read_text());data['problem']='SYNTHETIC_HANDOFF_FIXTURE '+data['problem'];preparations.append(call(i,'prepare_experiment',data))
        prepared=batch(preparations,True);requests=[];ids=[]
        for j,i in enumerate((10,11,12)):
            result=prepared[i]['result'];assert not result.get('isError'),result
            value=result['structuredContent'];eid=value['id'];ids.append(eid)
            requests += [call(20+j*3,'start_experiment',{'experiment_id':eid,'expected_revision':value['revision']}),call(21+j*3,'record_experiment_result',{'experiment_id':eid,'status':'FAILED','metrics':{'synthetic_fixture':1},'observations':['AUTHORED SOFTWARE FIXTURE ONLY; no Studio execution.'],'errors':['AUTHORED FAILURE, not a game finding.'],'limits':['Temporary isolated directory removed after software check.']}),call(22+j*3,'get_experiment',{'experiment_id':eid,'detailed':True})]
        requests.append(call(40,'get_experiment_context',{'problem':'SYNTHETIC_HANDOFF_FIXTURE','limit':10,'detailed':True}));results=batch(requests,True)
        for i in (22,25,28):
            r=results[i]['result'];assert not r.get('isError'),r
            v=r['structuredContent'];assert v['status']=='FAILED' and v['verification']=='not_verified'
        assert all(eid in json.dumps(results[40]) for eid in ids)
        assert initial=={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for name in ('config','knowledge','project') for p in (root/name).rglob('*') if p.is_file()}
        return {'state':'PASS','category':'ISOLATED_SOFTWARE_FIXTURES_NOT_STUDIO','tools':27,'candidate_retrieved':True,'editorial_procedure_retrieved':True,'default_write_denied':True,'three_separate_prepare_start_record_read_roundtrips':True,'VERIFIED':False,'protected_inputs_unchanged':True,'network':'sockets forbidden','Studio':'NOT_EXECUTED','Desktop':'NOT_RETESTED','real_measurements':False}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--handoff',type=Path,default=Path(__file__).resolve().parents[2]);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=run(a.source.resolve(),a.handoff.resolve());a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
