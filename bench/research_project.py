"""Explicit isolated P0/P1 session; retain same session and counters on rerun."""
import argparse
import json
from pathlib import Path
import shutil
from agent.project_research import ProjectResearch
from agent.project_work import Project,preparation_archive
from agent.storage import atomic_write
from agent.lab_store import clean_json


def prepare_copy(repository,workspace,runtime,allow_network=False,trust_proxy=False):
    repository=Path(repository).resolve();workspace=Path(workspace).resolve();runtime=Path(runtime).resolve()
    if workspace.is_relative_to(repository) or repository.is_relative_to(workspace):raise ValueError('demo must be separate from the active repository')
    workspace.mkdir(parents=True,exist_ok=True)
    for name in ('config','knowledge','project'):
        if not (workspace/name).exists():shutil.copytree(repository/name,workspace/name,ignore=shutil.ignore_patterns('.obsidian','__pycache__'))
    for name in ('sources','robots'):
        source=runtime/'lab/ocean'/name;dest=workspace/'lab/ocean'/name;dest.mkdir(parents=True,exist_ok=True)
        for path in source.glob('*.json') if source.exists() else []:
            if path.is_symlink():raise ValueError('symlink source refused')
            if not (dest/path.name).exists():shutil.copyfile(path,dest/path.name)
    (workspace/'output').mkdir(exist_ok=True)
    if not (workspace/'output/queue.json').exists():shutil.copyfile(runtime/'output/queue.json',workspace/'output/queue.json')
    if allow_network:
        p=workspace/'config/v10.json';value=json.loads(p.read_text(encoding='utf-8'));value['network_enabled']=True;atomic_write(p,json.dumps(value,indent=2)+'\n')
    if trust_proxy:
        p=workspace/'config/ocean.json';value=json.loads(p.read_text(encoding='utf-8'));value.update(network_mode='trusted_system_proxy',trust_system_proxy=True);atomic_write(p,json.dumps(value,indent=2)+'\n')
    return workspace


def run(workspace,max_ticks=12,allow_network=False):
    root=Path(workspace);project=Project(root);research=ProjectResearch(root);p=project.path('demo-session.json')
    before=json.loads((root/'output/queue.json').read_text(encoding='utf-8'))['daily']
    if p.exists():state=json.loads(p.read_text(encoding='utf-8'))
    else:
        goal=research.prepare(apply=True);state={'session_id':goal['id'],'history':[],'daily_before_first_run':before}
        project.write(p,state)
    for _ in range(max_ticks):
        result=research.run(state['session_id'],apply=True,allow_network=allow_network)
        s=result.get('research',{}).get('session',{})
        state['history'].append({'state':result['state'],'acquisition_state':result.get('acquisition_state'),
            'ticks':s.get('ticks'),'http_calls':s.get('http_calls'),'fetch_attempts':s.get('fetch_attempts'),
            'queue':result.get('research',{}).get('queue',{}).get('counts'),
            'stop_details':result.get('research',{}).get('stop_details'),'updated_cards':result.get('last_tick_cards',[]),
            'errors':result.get('source_errors',[])})
        project.write(p,state)
        if result['state'] in ('BUDGET_STOP','stopped','PROJECT_CHANGED','PAUSED','STOPPED') or result.get('acquisition_state')=='COMPLETE':break
    # One useful card per initial theme, including explicitly unsourced drafts.
    tasks=research.get(state['session_id'])['tasks'];cards=[]
    for task in tasks:cards.append(project.latest(task) or project.synthesize(task,apply=True))
    after=json.loads((root/'output/queue.json').read_text(encoding='utf-8'))['daily']
    report={'scope':'actual bounded agent requests; no model, Blender or Roblox execution',
        'session_id':state['session_id'],'session':research.sessions.get(state['session_id']),
        'history':state['history'],'daily_before_first_run':state['daily_before_first_run'],'daily_after':after,
        'cards':[{'task':c['task_id'],'key':c['key'],'readiness':c.get('current_readiness',c['quality']['readiness']),
                  'research_state':c['quality']['research_state'],'sources':c['sources'],'issues':c['quality']['issues']} for c in cards],
        'truth_verified':False,'model_calls':0,'engine_experiments_executed':False,'all_tasks_ready':False}
    return report,preparation_archive(cards)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repository',type=Path,default=Path.cwd());p.add_argument('--workspace',type=Path,required=True)
    p.add_argument('--runtime',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--archive-output',type=Path,required=True)
    p.add_argument('--allow-network',action='store_true');p.add_argument('--trust-system-proxy',action='store_true');p.add_argument('--max-ticks',type=int,default=12)
    a=p.parse_args()
    if not a.allow_network:p.error('live demo requires explicit --allow-network')
    if not 1<=a.max_ticks<=12:p.error('--max-ticks must be 1..12')
    root=prepare_copy(a.repository,a.workspace,a.runtime,a.allow_network,a.trust_system_proxy);report,archive=run(root,a.max_ticks,a.allow_network)
    a.output.parent.mkdir(parents=True,exist_ok=True);a.archive_output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(clean_json(report,1_000_000)+'\n',encoding='utf-8');a.archive_output.write_text(json.dumps(archive,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'session_id':report['session_id'],'http_calls':report['session']['http_calls'],'ticks':report['session']['ticks'],
        'cards':len(report['cards']),'all_tasks_ready':False,'stop_details':report['session'].get('stop_details')},ensure_ascii=False))


if __name__=='__main__':main()
