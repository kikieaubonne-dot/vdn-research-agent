"""Local Windows-compatible V10 CLI. All mutation commands default to dry-run."""
import argparse
import json
from pathlib import Path
import sqlite3
import sys
from agent import gaps,obsidian,lab_plan,visual
from agent.lab_store import LabStore,clean_json
from agent.lab_import import measurement
from agent.research_session import ResearchSessions,config


def read_json(path):
    if path is None:return None
    p=Path(path)
    if p.stat().st_size>64000:raise ValueError('input JSON exceeds 64 KB')
    value=json.loads(p.read_text(encoding='utf-8'));clean_json(value);return value


def metrics(root):
    lab=LabStore(root);result=lab.find(limit=20);counts={};failures={}
    folder=lab.path('experiments');paths=list(folder.iterdir()) if folder.exists() else []
    if len(paths)>1000:raise ValueError('experiment count limit exceeded')
    for path in paths:
        r=lab.get(path.name)
        if r.get('error'):continue
        counts[r['status']]=counts.get(r['status'],0)+1
        for outcome in r['results']:
            for error in outcome['errors']:failures[error]=failures.get(error,0)+1
    sessions=[];folder=lab.path('research')
    if folder.exists():
        paths=list(folder.iterdir())
        if len(paths)>1000:raise ValueError('session count limit exceeded')
        for p in paths:
            state=ResearchSessions(root).get(p.name)
            sessions.append({k:state[k] for k in ('id','status','ticks','http_calls','fetch_attempts','compute_reserved_s','duplicates_avoided')} |
                            {'integration_failures':state.get('integration_failures',0),'last_error':state.get('error'),
                             'stop_reason':state.get('stop_reason'),'stop_details':state.get('stop_details'),
                             'last_tick':state.get('last_tick'),'last_collection':state.get('last_collection')})
    return {'schema':'vdn.metrics/10','experiment_states':counts,'error_occurrences':failures,'sessions':sessions,
            'diagnostics':result['diagnostics'],'solution_reuse':'not measured','productivity_gain':'not measured',
            'game_execution':'not measured by Python','ai_required':False,
            'policy':{k:config(root)[k] for k in ('autonomous_enabled','network_enabled','allowed_goals','schedule','research')}}


def main(argv=None):
    if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    sub=p.add_subparsers(dest='command',required=True)
    def command(name,mutates=False):
        s=sub.add_parser(name)
        if mutates:
            flags=s.add_mutually_exclusive_group();flags.add_argument('--apply',action='store_true');flags.add_argument('--dry-run',action='store_true')
        return s
    command('status');command('quality')
    s=command('create',True);s.add_argument('--input',required=True)
    s=command('get');s.add_argument('id');s.add_argument('--detailed',action='store_true')
    s=command('find');s.add_argument('problem',nargs='?',default='');s.add_argument('--status');s.add_argument('--detailed',action='store_true')
    s=command('transition',True);s.add_argument('id');s.add_argument('status');s.add_argument('--revision',type=int,required=True)
    s=command('configure',True);s.add_argument('id');s.add_argument('--input',required=True);s.add_argument('--revision',type=int,required=True)
    s=command('result',True);s.add_argument('id');s.add_argument('--input',required=True)
    s=command('review',True);s.add_argument('id');s.add_argument('--reviewer',required=True);s.add_argument('--condition',action='append',required=True);s.add_argument('--attest-human-inspection',action='store_true')
    s=command('artifact',True);s.add_argument('path');s.add_argument('--kind',default='self_generated',choices=['self_generated','external_measurement','external_capture'])
    s=command('import-measurement',True);s.add_argument('path')
    s=command('research-prepare',True);s.add_argument('question');s.add_argument('--topic',default='spruce');s.add_argument('--session-id')
    s=command('research-run',True);s.add_argument('id');s.add_argument('--allow-network',action='store_true')
    s=command('tick',True);s.add_argument('--mode',choices=['autonomous','scheduled'],default='autonomous');s.add_argument('--allow-network',action='store_true')
    s=command('spruce',True);s.add_argument('--batch',default='snowy-spruce-v10')
    s=command('compare');s.add_argument('first');s.add_argument('second')
    s=command('visual-plan');s.add_argument('artifact');s.add_argument('--input');s.add_argument('--backend',choices=['none','local','remote'],default='none')
    s=command('visual-compare');s.add_argument('reference');s.add_argument('result');s.add_argument('--input');s.add_argument('--backend',choices=['none','local','remote'],default='none')
    s=command('sync',True);s.add_argument('--destination',type=Path,required=True);s.add_argument('--include-lab',action='store_true');s.add_argument('--rollback')
    a=p.parse_args(argv);lab=LabStore(a.root);sessions=ResearchSessions(a.root);cmd=a.command
    try:
        if cmd=='status':r=metrics(a.root)
        elif cmd=='quality':r=gaps.inventory(a.root)
        elif cmd=='research-prepare':r=sessions.prepare(a.question,a.topic,apply=a.apply,session_id=a.session_id)
        elif cmd=='research-run':r=sessions.run(a.id,apply=a.apply,allow_network=a.allow_network)
        elif cmd=='tick':r=sessions.tick(a.mode,apply=a.apply,allow_network=a.allow_network)
        elif cmd=='spruce':r=lab_plan.spruce(a.root,a.apply,a.batch)
        elif cmd=='compare':r=lab_plan.compare(a.root,a.first,a.second)
        elif cmd=='get':
            r=lab.get(a.id)
            if not a.detailed and not r.get('error'):r=lab_plan.summary(r)
        elif cmd=='find':r=lab_plan.context(a.root,a.problem,a.status,detailed=a.detailed)
        elif cmd=='visual-plan':r=visual.plan(a.root,a.artifact,read_json(a.input),a.backend)
        elif cmd=='visual-compare':r=visual.compare(a.root,a.reference,a.result,read_json(a.input),a.backend)
        elif cmd=='import-measurement':r=measurement(a.root,a.path,a.apply)
        elif cmd=='sync':
            r=obsidian.rollback(a.destination,a.rollback,apply=a.apply) if a.rollback else obsidian.sync(a.root,a.destination,apply=a.apply,extra_pages={**gaps.pages(a.root),**(lab_plan.pages(a.root) if a.include_lab else {})})
        elif not a.apply:
            r={'state':'simulation','command':cmd,'writes':0,'input':read_json(a.input) if hasattr(a,'input') else None}
        elif cmd=='create':r=lab.create(**read_json(a.input))
        elif cmd=='configure':r=lab.configure(a.id,**read_json(a.input),expected_revision=a.revision)
        elif cmd=='transition':r=lab.transition(a.id,a.status,a.revision)
        elif cmd=='result':r=lab.record_result(a.id,**read_json(a.input))
        elif cmd=='review':r=lab.review(a.id,a.reviewer,a.condition,a.attest_human_inspection)
        elif cmd=='artifact':r=lab.import_artifact(a.path,a.kind)
        else:raise ValueError('unknown command')
    except (ValueError,OSError,sqlite3.Error,KeyError,TypeError) as exc:
        # Do not echo provider payloads, credentials or a traceback into CLI logs.
        print(json.dumps({'error':str(exc) if isinstance(exc,(ValueError,PermissionError)) else type(exc).__name__},ensure_ascii=False));return 2
    print(json.dumps(r,ensure_ascii=False,indent=2,allow_nan=False));return 1 if r.get('state') in ('ERROR','conflict') or r.get('error') else 0


if __name__=='__main__':raise SystemExit(main())
