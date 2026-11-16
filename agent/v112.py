"""Manual project preparation CLI; no daemon, model install or game execution."""
import argparse
import json
from pathlib import Path
import sys
from agent.project_work import Project
from agent.project_research import ProjectResearch
from agent.project import budgets


def main(argv=None):
    if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);sub=p.add_subparsers(dest='cmd',required=True)
    s=sub.add_parser('bible');s.add_argument('--markdown',action='store_true')
    sub.add_parser('plan');sub.add_parser('daily');sub.add_parser('budget')
    s=sub.add_parser('task');s.add_argument('task');s.add_argument('--key')
    s=sub.add_parser('synthesize');s.add_argument('question');s.add_argument('--apply',action='store_true');s.add_argument('--allow-model',action='store_true')
    s=sub.add_parser('brief');s.add_argument('question');s.add_argument('--token-budget',type=int,default=1800);s.add_argument('--key')
    s=sub.add_parser('pack');s.add_argument('--limit',type=int,default=3)
    s=sub.add_parser('research-prepare');s.add_argument('--tasks',nargs='+');s.add_argument('--apply',action='store_true');s.add_argument('--session-id')
    s=sub.add_parser('research-run');s.add_argument('id');s.add_argument('--apply',action='store_true');s.add_argument('--allow-network',action='store_true');s.add_argument('--allow-model',action='store_true')
    s=sub.add_parser('control');s.add_argument('id');s.add_argument('action',choices=['pause','resume','stop']);s.add_argument('--apply',action='store_true')
    s=sub.add_parser('sync');s.add_argument('--destination',type=Path,required=True);s.add_argument('--apply',action='store_true');s.add_argument('--rollback')
    s=sub.add_parser('visual-link');s.add_argument('task');s.add_argument('path');s.add_argument('--target',required=True);s.add_argument('--keep',nargs='*',default=[]);s.add_argument('--avoid',nargs='*',default=[]);s.add_argument('--render-version',required=True);s.add_argument('--human-opinion',default='UNKNOWN');s.add_argument('--apply',action='store_true')
    a=p.parse_args(argv);project=Project(a.root);research=ProjectResearch(a.root)
    try:
        if a.cmd=='bible':
            if a.markdown:print(project.bible.markdown(),end='');return 0
            r=project.bible.data
        elif a.cmd=='plan':r=project.plan()
        elif a.cmd=='daily':r=project.daily()
        elif a.cmd=='budget':r=budgets(a.root)
        elif a.cmd=='task':r=project.get(a.key) if a.key else project.latest(a.task) or project.synthesize(a.task)
        elif a.cmd=='synthesize':r=project.synthesize(a.question,a.apply,a.allow_model)
        elif a.cmd=='brief':r=project.brief(a.question,a.token_budget,a.key)
        elif a.cmd=='pack':r=project.pack(a.limit)
        elif a.cmd=='research-prepare':r=research.prepare(a.tasks,a.apply,a.session_id)
        elif a.cmd=='research-run':r=research.run(a.id,a.apply,a.allow_network,a.allow_model)
        elif a.cmd=='control':r=research.control(a.id,a.action,a.apply)
        elif a.cmd=='visual-link':
            from agent.project_visual import link
            r=link(project,a.task,a.path,a.target,a.keep,a.avoid,a.render_version,a.human_opinion,a.apply)
        else:
            from agent import obsidian,gaps
            from agent.ocean_api import pages
            r=obsidian.rollback(a.destination,a.rollback,apply=a.apply) if a.rollback else obsidian.sync(a.root,a.destination,apply=a.apply,extra_pages={**gaps.pages(a.root),**pages(a.root),**project.pages()})
    except (ValueError,OSError,KeyError,TypeError,RuntimeError) as exc:
        print(json.dumps({'error_kind':type(exc).__name__,'message':str(exc) if isinstance(exc,(ValueError,PermissionError)) else 'project operation failed; state preserved'},ensure_ascii=False));return 2
    print(json.dumps(r,ensure_ascii=False,indent=2,allow_nan=False));return 0


if __name__=='__main__':raise SystemExit(main())
