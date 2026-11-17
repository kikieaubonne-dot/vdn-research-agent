"""Operator-only local Blender measurement runner, not a shell or Studio bridge.

Transport/authentication: local files under lab/, same-user filesystem rights,
explicit CLI capability. No TCP listener, model tools or arbitrary script path.
"""
import hashlib,json,re,shutil,subprocess,time,uuid,math
from pathlib import Path
from agent import budget,intelligence_models as im
from agent.lab_store import LabStore,identity,lab_lock,clean_json
from agent.obsidian import safe_path
from agent.ocean_web import OceanWeb,settings
from agent.storage import atomic_write
from agent.ocean_lab import import_blender

SCRIPT=Path(__file__).resolve().parents[1]/'scripts/blender_ocean_measure.py'

class LocalLab:
 def __init__(self,root):self.root=Path(root).resolve();self.lab=LabStore(self.root)
 def path(self,job_id,name='job.json'):return safe_path(self.root,'lab/runner/'+identity(job_id)+'/'+name)
 def check_storage(self,extra=0):
  total=0;count=0
  for folder in ('lab/runner','lab/inbox/jobs','lab/inbox/forest'):
   for p in (self.root/folder).rglob('*') if (self.root/folder).exists() else []:
    if p.is_file():safe_path(self.root,p.relative_to(self.root).as_posix());total+=p.stat().st_size;count+=1
  if count>2000 or total+extra>settings(self.root)['storage_bytes']:raise ValueError('local runner storage cap reached')
  OceanWeb(self.root).storage_check(total+extra)
 def save(self,job):
  text=clean_json(job,64000);self.check_storage(len(text.encode('utf-8')));atomic_write(self.path(job['id']),text)
 def get(self,job_id):
  p=self.path(job_id)
  if p.stat().st_size>64000:raise ValueError('job oversized')
  job=json.loads(p.read_text(encoding='utf-8'));clean_json(job)
  if job.get('schema')!='vdn.local-lab-job/11.2' or job['id']!=identity(job_id) or job['spec_hash']!=hashlib.sha256(clean_json(job['spec']).encode()).hexdigest():raise ValueError('job integrity mismatch')
  if set(job['spec'])!={'capability','input','input_sha256','required_version','script_sha256','task','unit_scale'} or job['spec']['capability'] not in ('blender_demo_geometry','blender_copy_geometry'):raise ValueError('job capability/schema not approved')
  expected=('DEMO_A','DEMO_B') if job['spec']['capability']=='blender_demo_geometry' else ('ASSET',)
  if [r.get('method') for r in job['experiments']]!=list(expected) or any(r['id']!=str(uuid.uuid5(uuid.UUID(job['id']),r['method'])) for r in job['experiments']):raise ValueError('job experiment binding mismatch')
  return job
 def capabilities(self):
  return {'transport':'local files and explicit operator CLI; OS filesystem authorization','network_listener':False,'blender_binary_found':bool(shutil.which('blender')),'capabilities':['blender_demo_geometry','blender_copy_geometry'],'studio':{'state':'NOT_IMPLEMENTED','reason':'requires an installed, authorized Studio plugin/worker; no real Studio bridge is available'},'arbitrary_scripts':False,'publication':False,'automatic_models':False}
 def prepare(self,capability='blender_demo_geometry',input_path=None,required_version='5.2',task='trees',apply=False,unit_scale=None):
  if type(apply) is not bool:raise ValueError('apply must be boolean')
  from agent.project import Bible
  Bible(self.root).task(task)
  if capability not in ('blender_demo_geometry','blender_copy_geometry'):raise ValueError('only approved Blender geometry capabilities')
  if not isinstance(required_version,str) or not re.fullmatch(r'\d+\.\d+(?:\.\d+)?',required_version):raise ValueError('explicit Blender version required')
  checksum=None
  if capability=='blender_copy_geometry':
   if not isinstance(input_path,str) or not input_path.startswith('lab/inbox/') or not input_path.endswith('.blend'):raise ValueError('stage a trusted scene COPY in lab/inbox/*.blend')
   p=safe_path(self.root,input_path)
   if not p.is_file() or p.stat().st_size>8_000_000:raise ValueError('bounded scene copy required')
   checksum=hashlib.sha256(p.read_bytes()).hexdigest()
   if type(unit_scale) not in (int,float) or not math.isfinite(unit_scale) or unit_scale<=0:raise ValueError('explicit positive scene unit_scale required')
  elif input_path is not None:raise ValueError('demo refuses input assets')
  spec={'capability':capability,'input':input_path,'input_sha256':checksum,'required_version':required_version,'script_sha256':hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),'task':task,'unit_scale':1.0 if capability=='blender_demo_geometry' else unit_scale}
  preview={'state':'simulation','spec':spec,'engine_executed':False,'writes':0}
  if not apply:return preview
  def work():
   folder=safe_path(self.root,'lab/runner')
   if folder.exists() and len(list(folder.iterdir()))>=20:raise ValueError('local job count cap reached')
   job_id=str(uuid.uuid4());records=[]
   for method in (('DEMO_A','DEMO_B') if capability=='blender_demo_geometry' else ('ASSET',)):
    r=self.lab.create('Geometry laboratory; '+('generated primitives, NOT B3/C1' if input_path is None else 'operator supplied scene copy'),method,'Measure geometry only; no visual or Roblox success inferred.',parameters={'method':method,'project_task':task},environment={},protocol={'not_executed':True,'input_sha256':checksum},experiment_id=str(uuid.uuid5(uuid.UUID(job_id),method)))
    records.append({'id':r['id'],'method':method})
   job={'schema':'vdn.local-lab-job/11.2','id':job_id,'spec':spec,'spec_hash':hashlib.sha256(clean_json(spec).encode()).hexdigest(),'state':'PENDING','experiments':records,'attempts':0,'reports':[],'engine_executed':False,'verified':False}
   self.save(job);return job
  return im.operation(self.root,work)
 def run(self,job_id,executable=None,allow_blender=False):
  if allow_blender is not True:raise PermissionError('explicit --allow-blender operator capability required; absent from MCP')
  def work():
   with lab_lock(self.root,'.runner'):
    job=self.get(job_id)
    if job['state']=='SUCCEEDED':return {**job,'cache_hit':True}
    if job['state'] in ('FAILED','BLOCKED'):return job # inspect, preserve, create a revised design explicitly
    job['attempts']+=1
    if job['attempts']>2:raise ValueError('local job retry cap reached')
    if hashlib.sha256(SCRIPT.read_bytes()).hexdigest()!=job['spec']['script_sha256']:raise ValueError('approved measurement script changed; prepare a reviewed job')
    if job['spec']['input']:
     p=safe_path(self.root,job['spec']['input'])
     if hashlib.sha256(p.read_bytes()).hexdigest()!=job['spec']['input_sha256']:raise ValueError('scene copy changed after job preparation')
    binary=Path(executable or shutil.which('blender') or '')
    if not binary.is_file():job.update(state='BLOCKED',error_kind='BlenderUnavailable');self.save(job);return job
    try:
     version=subprocess.run([str(binary.resolve()),'--version'],capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=3,shell=False)
     match=re.search(r'Blender (\d+\.\d+(?:\.\d+)?)',version.stdout)
     if version.returncode or not match:raise ValueError('Blender version not identifiable')
     actual=match.group(1);required=job['spec']['required_version'];job['actual_blender_version']=actual
     if actual!=required and not actual.startswith(required+'.'):
      job.update(state='BLOCKED',error_kind='VersionMismatch');self.save(job);return job
     controls={'blender_version':actual,'unit_scale':job['spec']['unit_scale'],'measurement_method':'evaluated_loop_triangles_v1'}
     for rec in job['experiments']:
      r=self.lab.get(rec['id'])
      if r['status']=='HYPOTHESIS':r=self.lab.transition(r['id'],'PLANNED')
      if r['status']=='PLANNED':
       r=self.lab.configure(r['id'],r['parameters'],controls,{'controls':controls,'scope':'geometry measurement; no user asset or game validation inferred','input_sha256':job['spec']['input_sha256']},r['revision']);r=self.lab.transition(r['id'],'RUNNING',r['revision'])
     output='lab/inbox/jobs/'+job['id'];reports=[safe_path(self.root,output+'/blender-'+r['method']+'.json') for r in job['experiments']]
     if any(p.exists() for p in reports) and not all(p.exists() for p in reports):raise ValueError('partial output retained; inspect before a revised job')
     if not all(p.exists() for p in reports):
      job['state']='RUNNING';self.save(job);self.check_storage(128000)
      command=[str(binary.resolve()),'--background','--factory-startup','--disable-autoexec','--threads','1']
      if job['spec']['input']:command.append(str(safe_path(self.root,job['spec']['input'])))
      command+=['--python',str(SCRIPT),'--','--experiment-a',job['experiments'][0]['id'],'--output-dir',output]
      if job['spec']['capability']=='blender_demo_geometry':command+=['--demo','--experiment-b',job['experiments'][1]['id']]
      else:command+=['--method','ASSET']
      guard=budget.CURRENT.get();timeout=max(.1,min(18,guard.deadline-time.monotonic())) if guard else 18
      # A regular file bounds Python memory use; oversize output is refused and retained.
      log=self.path(job['id'],'attempt-'+str(job['attempts'])+'.log');log.parent.mkdir(parents=True,exist_ok=True)
      with log.open('x',encoding='utf-8') as stream:
       process=subprocess.run(command,cwd=self.root,stdout=stream,stderr=subprocess.STDOUT,timeout=timeout,shell=False)
      job['engine_executed']=True
      if log.stat().st_size>128000:raise ValueError('engine log cap exceeded; inspect retained output')
      if process.returncode:raise RuntimeError('approved engine measurement failed')
     results=[]
     for rec,p in zip(job['experiments'],reports):
      raw=json.loads(p.read_text(encoding='utf-8'))
      if raw['experiment_id']!=rec['id'] or raw['method']!=rec['method']:raise ValueError('output bound to another experiment')
      result=import_blender(self.root,p.relative_to(self.root).as_posix(),True);results.append({'id':result['id'],'status':result['status'],'metrics':result['results'][-1]['metrics'],'report_sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
     job.update(state='SUCCEEDED',reports=results,engine_executed=True,scope='real Blender geometry only; supplied scene copy or primitives, no visual quality, B3/C1 or Roblox performance inferred');self.save(job);return job
    except (OSError,ValueError,RuntimeError,subprocess.TimeoutExpired) as exc:
     job.update(state='FAILED',error_kind=type(exc).__name__)
     for rec in job['experiments']:
      r=self.lab.get(rec['id'])
      if r['status']=='RUNNING':self.lab.record_result(rec['id'],'FAILED',{},['Local approved runner failed; inspect retained logs'],errors=[type(exc).__name__],limits=['No successful engine validation inferred.'])
     self.save(job);return job
  return im.operation(self.root,work)
