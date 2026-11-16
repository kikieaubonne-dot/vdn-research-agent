"""Run the suite with socket connects forbidden, including subprocesses.

python -m tests.offline
"""
import os
from pathlib import Path
import subprocess
import sys
import tempfile


def main():
    with tempfile.TemporaryDirectory() as d:
        Path(d,'sitecustomize.py').write_text(
            "import socket\ndef denied(*a, **k):\n    raise AssertionError('network forbidden by offline harness')\n"
            "socket.socket.connect = denied\nsocket.create_connection = denied\n",encoding='utf-8')
        env=dict(os.environ)
        # The corpus and MCP wire format are UTF-8, including on CP1252 Windows.
        # Set startup flags for the suite and every subprocess it creates.
        env['PYTHONUTF8']='1'
        env['PYTHONIOENCODING']='utf-8'
        for name in ('GITHUB_TOKEN','VDN_ROOT','VDN_SEARXNG_URL','VDN_REMOTE_MODEL_KEY','OLLAMA_URL','OLLAMA_MODEL'):
            env.pop(name,None) # tests inject their own fake identities/endpoints
        env['PYTHONPATH']=d+os.pathsep+env.get('PYTHONPATH','')
        return subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],
                               cwd=Path(__file__).resolve().parents[1],env=env).returncode


if __name__=='__main__':raise SystemExit(main())
