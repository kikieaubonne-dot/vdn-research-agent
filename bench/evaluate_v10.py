"""Reuse the frozen V9 holdout without tuning retrieval or editing old reports."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile


def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path.cwd());p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();root=a.root.resolve()
    with tempfile.TemporaryDirectory() as tmp:
        out=Path(tmp)/'holdout.json'
        subprocess.run([sys.executable,'-m','bench.evaluate_v9','--root',str(root),'--output',str(out)],check=True,capture_output=True,text=True)
        result=json.loads(out.read_text(encoding='utf-8'))
    result.update(schema='vdn.holdout/10',implementation='V10; unchanged V9 retrieval implementation',protocol='bench/v9_holdout.json, frozen 16-case V9 holdout')
    result['comparisons']=[]
    for version,path in (('V8','docs/v9/holdout_v8_enriched.json'),('V9','docs/v9/holdout_v9_enriched.json')):
        old=json.loads((root/path).read_text(encoding='utf-8'))
        result['comparisons'].append({'version':version,'source':path,'index_notes':old['index_notes'],
                                      **{k:old[k] for k in ('hit_at_1','hit_at_3','hit_at_5','mrr')},
                                      'abstention_protocol':old['abstention_protocol']})
    result['interpretation']='Same enriched corpus and questions; no V10 retrieval quality gain claimed. V8 abstention uses a different proxy. Timings are environment-dependent.'
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='details'},ensure_ascii=False,indent=2))


if __name__=='__main__':main()
