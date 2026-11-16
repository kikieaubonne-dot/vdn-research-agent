"""Non-destructive real Blender measurement, explicit execution and local profile."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import uuid
from agent.ocean_lab import prepare,import_blender,compare
from agent.lab_store import LabStore


def measure(output,executable='blender'):
    binary=shutil.which(executable)
    if not binary:return {'state':'unavailable','blender_executed':False,'measurements':None}
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    version=subprocess.check_output([binary,'--version'],text=True,timeout=10).splitlines()[0].removeprefix('Blender ')
    with tempfile.TemporaryDirectory(prefix='ocean-blender-') as d:
        root=Path(d);env=dict(os.environ)
        for name,suffix in (('BLENDER_USER_CONFIG','config'),('BLENDER_USER_SCRIPTS','scripts'),('BLENDER_USER_DATAFILES','data'),('BLENDER_USER_EXTENSIONS','extensions'),('BLENDER_USER_RESOURCES','resources')):
            p=root/'profile'/suffix;p.mkdir(parents=True);env[name]=str(p)
        planned=prepare(root,'generated-demo-'+str(uuid.uuid4()),('DEMO_A','DEMO_B'),True);lab=LabStore(root)
        conditions={'blender_version':version,'unit_scale':1.0,'measurement_method':'evaluated_loop_triangles_v1'}
        for r in planned['experiments']:
            protocol=r['protocol'];protocol['controls']=conditions
            current=lab.configure(r['id'],r['parameters'],conditions,protocol,r['revision']);lab.transition(r['id'],'RUNNING',current['revision'])
        ids=[r['id'] for r in planned['experiments']]
        script=Path(__file__).resolve().parents[1]/'scripts/blender_ocean_measure.py'
        command=[binary,'--background','--factory-startup','--disable-autoexec','--python',str(script),'--','--demo',
                 '--experiment-a',ids[0],'--experiment-b',ids[1],'--output-dir','lab/inbox']
        result=subprocess.run(command,cwd=root,env=env,text=True,capture_output=True,timeout=90)
        (output/'blender.log').write_text((result.stdout+result.stderr).replace(str(root),'<temporary-lab>'),encoding='utf-8')
        if result.returncode:raise ValueError('Blender process failed; inspect blender.log, no measurements claimed')
        for method in ('DEMO_A','DEMO_B'):
            name='blender-'+method+'.json';import_blender(root,'lab/inbox/'+name,True);shutil.copyfile(root/'lab/inbox'/name,output/name)
        report={'state':'measured','blender_executed':True,'blender_version':version,
                'scope':'REAL generated primitive geometry, not B3/C1 assets or Roblox performance',
                'comparison':compare(root,*ids),'experiment_ids':ids,'verified':False,'profile':'isolated temporary directories'}
        (output/'comparison.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        return report


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--blender',default='blender')
    a=p.parse_args();r=measure(a.output,a.blender);print(json.dumps(r,ensure_ascii=False,indent=2));return 0 if r['state']=='measured' else 2


if __name__=='__main__':raise SystemExit(main())
