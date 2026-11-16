"""Explicit V9 operations. Default sync/research/repair is simulation."""
import argparse
import json
from pathlib import Path
import sqlite3
import uuid
import sys

from agent.engine import KnowledgeEngine
from agent import factory,gaps,obsidian,rag
from agent.autonomy import Lock


def repair_index(root,apply=False):
    root=Path(root)
    path=root/'output'/'knowledge.db'
    if path.is_symlink() or path.parent.is_symlink():raise ValueError('symlink index refused')
    if not apply:return {'state':'simulation','index':str(path),'original_preserved':True}
    with Lock(root,7200):
        archived=[];identity=uuid.uuid4().hex
        for suffix in ('','-wal','-shm'):
            current=Path(str(path)+suffix)
            if current.is_symlink():raise ValueError('symlink index companion refused')
            if current.exists():
                target=path.parent/f'knowledge.corrupt-{identity}.db{suffix}'
                current.replace(target);archived.append(target.name)
        return {'state':'rebuilt','archived':archived,'index':rag.update_index(root),'source_notes_modified':False}


def main(argv=None):
    if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    sub=p.add_subparsers(dest='command',required=True)
    sub.add_parser('gaps')
    s=sub.add_parser('sync');s.add_argument('--destination',type=Path,required=True);s.add_argument('--apply',action='store_true');s.add_argument('--rollback')
    s=sub.add_parser('research');s.add_argument('--apply',action='store_true');s.add_argument('--max-items',type=int,default=None)
    s=sub.add_parser('brief');s.add_argument('task');s.add_argument('--mode',choices=['compact','detailed'],default='compact');s.add_argument('--token-budget',type=int,default=1800)
    s=sub.add_parser('repair-index');s.add_argument('--apply',action='store_true')
    args=p.parse_args(argv)
    try:
        if args.command=='gaps':r=gaps.inventory(args.root)
        elif args.command=='research':r=factory.collect(args.root,apply=args.apply,max_items=args.max_items)
        elif args.command=='repair-index':r=repair_index(args.root,args.apply)
        elif args.command=='brief':r=KnowledgeEngine(args.root).get_task_brief(args.task,args.mode,args.token_budget)
        elif args.rollback:r=obsidian.rollback(args.destination,args.rollback,apply=args.apply)
        else:r=obsidian.sync(args.root,args.destination,apply=args.apply,extra_pages=gaps.pages(args.root))
    except (ValueError,OSError,sqlite3.Error) as e:
        print(json.dumps({'error':str(e)},ensure_ascii=False));return 2
    print(json.dumps(r,ensure_ascii=False,indent=2));return 1 if r.get('state')=='conflict' or r.get('errors') else 0


if __name__=='__main__':raise SystemExit(main())
