"""Stable JSON CLI for the local V8 knowledge facade."""
import argparse
import json
import sys
from pathlib import Path
from agent.engine import KnowledgeEngine


def main(argv=None):
    if hasattr(sys.stdout,'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    parser=argparse.ArgumentParser()
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    sub=parser.add_subparsers(dest='command',required=True)
    for name,argument in (('search','query'),('get','note_id'),('procedures','task'),('plan','question')):
        p=sub.add_parser(name);p.add_argument(argument)
        if name in ('search','procedures'):
            p.add_argument('--top-k',type=int,default=5)
    sub.choices['search'].add_argument('--domain')
    sub.choices['search'].add_argument('--evidence-level')
    p=sub.add_parser('experiment');p.add_argument('--input',type=Path,required=True)
    p.add_argument('--allow-experiments',action='store_true')
    args=parser.parse_args(argv)
    engine=KnowledgeEngine(args.root,allow_experiments=getattr(args,'allow_experiments',False))
    try:
        if args.command=='search':
            result=engine.search_knowledge(args.query,args.top_k,domain=args.domain,evidence_level=args.evidence_level)
        elif args.command=='get':result=engine.get_knowledge(args.note_id)
        elif args.command=='procedures':result=engine.find_procedures(args.task,args.top_k)
        elif args.command=='plan':result=engine.plan_research(args.question)
        else:
            if args.input.stat().st_size>64000:raise ValueError('input exceeds 64 KB')
            result=engine.report_experiment(**json.loads(args.input.read_text(encoding='utf-8')))
    except (ValueError,TypeError,PermissionError,OSError) as e:
        print(json.dumps({'error':str(e)},ensure_ascii=False));return 2
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 1 if result.get('error') else 0


if __name__=='__main__':
    raise SystemExit(main())
