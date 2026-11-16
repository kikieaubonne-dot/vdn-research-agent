"""Three deterministic demonstrations on a temporary copy of the real corpus."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import tempfile

from agent.engine import KnowledgeEngine

SCENARIOS = [
    ('snowy_tree', 'Comment créer un sapin enneigé extrêmement réaliste pour Roblox ?'),
    ('custom_skeleton', 'Pourquoi les os de mon squelette personnalisé bugguent-ils après importation dans Roblox ?'),
    ('snowy_forest', "Je veux refaire entièrement la forêt enneigée de mon jeu d'horreur Roblox."),
]


def demonstrate(source, destination):
    source, destination = Path(source), Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp)
        for name in ('knowledge','config'):
            shutil.copytree(source/name,root/name)
        engine=KnowledgeEngine(root)
        for name, question in SCENARIOS:
            result={'schema':'vdn.demonstration/8','scenario':name,'input':question,
                    'search':engine.search_knowledge(question,5,5000),
                    'procedures':engine.find_procedures(question,5),
                    'plan':engine.plan_research(question),
                    'executed_in_blender':False,'executed_in_roblox':False,'connected_to_claude':False}
            (destination/(name+'.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    manifest={p.relative_to(source).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted((source/'knowledge').rglob('*')) if p.is_file()}
    (destination/'corpus.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--root',type=Path,default=Path.cwd())
    parser.add_argument('--output-dir',type=Path,required=True)
    args=parser.parse_args();demonstrate(args.root,args.output_dir)


if __name__=='__main__':main()
