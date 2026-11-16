"""Six actual local demonstrations: corpus → vault → existing RAG → MCP stdio."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

from agent import gaps,obsidian
from agent.engine import KnowledgeEngine

SCENARIOS=[
 ('A_sapin','Comment fabriquer un sapin enneigé crédible pour Roblox ?'),
 ('B_rigging','Comment diagnostiquer des os ou attaches défectueux sur un squelette personnalisé Roblox ?'),
 ('C_foret','Comment construire une forêt enneigée nocturne optimisée pour Roblox ?'),
 ('D_poursuite','Comment créer un Père Noël capable de poursuivre un joueur dans une forêt avec obstacles Roblox ?'),
 ('E_accessoires','Comment attacher une sacoche et un bonnet à un personnage personnalisé animé Roblox ?'),
 ('F_insuffisant','Comment calculer une trajectoire orbitale des lunes de Jupiter ?')]


def demonstrate(source,destination):
    source=Path(source).resolve();destination=Path(destination);destination.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        project=Path(tmp)/'source';project.mkdir()
        for name in ('knowledge','config'):shutil.copytree(source/name,project/name)
        bundle=Path(tmp)/'bundle'
        pages=gaps.pages(project)
        preview=obsidian.sync(project,bundle,extra_pages=pages)
        first=obsidian.sync(project,bundle,apply=True,extra_pages=pages)
        second=obsidian.sync(project,bundle,apply=True,extra_pages=pages)
        if second['state']!='unchanged':raise AssertionError('second sync is not idempotent')
        broken=[]
        for path in (bundle/'knowledge').glob('_VDN-*.md'):
            for target in re.findall(r'\[\[([^]|]+)',path.read_text(encoding='utf-8')):
                if not (bundle/'knowledge'/(target.strip()+'.md')).exists():broken.append(target)
        engine=KnowledgeEngine(bundle)
        for name,question in SCENARIOS:
            brief=engine.get_task_brief(question)
            plan=engine.plan_research(question)
            plan={**{k:v for k,v in plan.items() if k!='nodes'},'nodes':[
                {**{k:v for k,v in n.items() if k!='references'},'references':[
                    {'id':r['id'],'title':r['title'],'sources':r['sources'],'compatibility':r['compatibility']['scope']}
                    for r in n['references']]} for n in plan['nodes']]}
            request={'jsonrpc':'2.0','id':1,'method':'tools/call','params':{'name':'get_task_brief','arguments':{'task':question}}}
            p=subprocess.run([sys.executable,str(source/'vdn_mcp.py'),'--root',str(bundle),'--v9'],
                             input=json.dumps(request)+'\n',text=True,capture_output=True,timeout=30,cwd=bundle)
            if p.returncode:raise AssertionError(p.stderr)
            response=json.loads(p.stdout)
            if response.get('result',{}).get('isError'):raise AssertionError(response)
            mcp=json.loads(response['result']['content'][0]['text'])
            if mcp!=brief:raise AssertionError('MCP/API mismatch')
            records=[{'id':p['note_id'],'exists':(bundle/engine.get_knowledge(p['note_id'])['path']).exists(),
                      'sources':engine.get_knowledge(p['note_id'])['sources']} for p in brief['procedures']]
            output={'schema':'vdn.demo/9','scenario':name,'input':question,'brief':brief,'plan':plan,
                    'vault_notes':records,'mcp_stdio_tested':True,'api_mcp_equal':True,
                    'first_sync_writes':first['written'],'second_sync_state':second['state'],
                    'generated_broken_links':broken,'obsidian_app_opened':False,'real_windows_vault_synced':False,
                    'studio_test_executed':False}
            (destination/(name+'.json')).write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        stats={'schema':'vdn.vault-demo/9','historical_corpus_files':106,
               'exported_markdown_files':len(list((bundle/'knowledge').rglob('*.md'))),
               'source_markdown_files':len(list((project/'knowledge').rglob('*.md'))),
               'second_sync_state':second['state'],'broken_generated_links':broken,
               'all_source_hashes_match':all(hashlib.sha256(path.read_bytes()).hexdigest()==hashlib.sha256((bundle/path.relative_to(project)).read_bytes()).hexdigest()
                                            for path in (project/'knowledge').rglob('*.md')),
               'live_windows_access':False}
        (destination/'vault_validation.json').write_text(json.dumps(stats,indent=2)+'\n')


def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path.cwd());p.add_argument('--output-dir',type=Path,required=True)
    a=p.parse_args();demonstrate(a.root,a.output_dir)


if __name__=='__main__':main()
