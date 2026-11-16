"""V11.1 intelligence CLI; default preview, no download or background task."""
import argparse
import json
from pathlib import Path
import sys
from agent.intelligence import Intelligence
from agent import intelligence_models as im,intelligence_semantic


def main(argv=None):
    if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    sub=p.add_subparsers(dest='cmd',required=True)
    a=sub.add_parser('diagnose');a.add_argument('--probe',action='store_true');a.add_argument('--model')
    a=sub.add_parser('synthesize');a.add_argument('question');a.add_argument('--apply',action='store_true');a.add_argument('--allow-model',action='store_true');a.add_argument('--retrieval',choices=['lexical','semantic','hybrid'],default='lexical')
    a=sub.add_parser('brief');a.add_argument('question');a.add_argument('--key');a.add_argument('--token-budget',type=int,default=1800)
    a=sub.add_parser('get');a.add_argument('key')
    a=sub.add_parser('search');a.add_argument('query');a.add_argument('--limit',type=int,default=5)
    a=sub.add_parser('embed-index');a.add_argument('--apply',action='store_true');a.add_argument('--max-items',type=int,default=10)
    a=sub.add_parser('sync');a.add_argument('--destination',type=Path,required=True);a.add_argument('--include-intelligence',action='store_true');a.add_argument('--apply',action='store_true');a.add_argument('--rollback')
    a=p.parse_args(argv);brain=Intelligence(a.root)
    try:
        if a.cmd=='diagnose':r=im.diagnose(a.root,a.probe,a.model)
        elif a.cmd=='synthesize':r=brain.run(a.question,apply=a.apply,allow_model=a.allow_model,retrieval=a.retrieval)
        elif a.cmd=='brief':r=brain.brief(a.question,a.token_budget,a.key)
        elif a.cmd=='get':r=brain.get(a.key)
        elif a.cmd=='search':r=brain.search(a.query,a.limit)
        elif a.cmd=='embed-index':r=intelligence_semantic.index(a.root,a.apply,a.max_items)
        else:
            from agent import obsidian,gaps
            from agent.ocean_api import pages
            r=obsidian.rollback(a.destination,a.rollback,apply=a.apply) if a.rollback else obsidian.sync(a.root,a.destination,apply=a.apply,
                extra_pages={**gaps.pages(a.root),**pages(a.root),**(brain.pages() if a.include_intelligence else {})})
    except (ValueError,OSError,RuntimeError,KeyError,TypeError) as exc:
        print(json.dumps({'error_kind':type(exc).__name__,'message':str(exc) if isinstance(exc,(ValueError,PermissionError)) else 'operation failed; inspect local logs'},ensure_ascii=False));return 2
    print(json.dumps(r,ensure_ascii=False,indent=2,allow_nan=False));return 0


if __name__=='__main__':raise SystemExit(main())
