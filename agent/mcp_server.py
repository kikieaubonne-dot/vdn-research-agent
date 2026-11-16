"""Serveur MCP (stdio, JSON-RPC 2.0) en LECTURE SEULE pour Claude Desktop. Bibliothèque standard uniquement.

Outils exposés : search_knowledge, read_knowledge, get_topic_index. Aucun outil n'écrit, ne supprime ni ne lance
de recherche web. L'index est mis à jour au démarrage (incrémental) si la bibliothèque a changé.

Lancement manuel : python -m agent.mcp_server   (configuration Claude Desktop : voir README_V5.md)
"""
from __future__ import annotations
import json
import os
import sys
from pathlib import Path

from agent import rag

ROOT = Path(os.environ.get("VDN_ROOT", Path(__file__).resolve().parents[1]))
SERVER = {"name": "vdn-knowledge", "version": "5.0.0"}
SUPPORTED = ("2025-06-18", "2025-03-26", "2024-11-05")

TOOLS = [
    {"name": "search_knowledge",
     "description": ("Cherche dans la bibliothèque technique VDN (Roblox, Blender, forêt, neige, éclairage…) et renvoie "
                     "des passages courts classés (statut, confiance, niveau de source). À utiliser AVANT toute recherche web."),
     "inputSchema": {"type": "object", "properties": {
         "query": {"type": "string", "description": "Question ou mots-clés (français ou anglais)."},
         "top_k": {"type": "integer", "minimum": 1, "maximum": 10, "default": 5},
         "token_budget": {"type": "integer", "minimum": 200, "maximum": 8000, "default": 1500},
         "domain": {"type": "string", "description": "Optionnel : limiter à un domaine (vegetation, forest, lighting…)."},
         "include_rejected": {"type": "boolean", "default": False}},
         "required": ["query"]}},
    {"name": "read_knowledge",
     "description": "Lit une fiche complète par son identifiant (vdn-xxxxxxxxxxxx), tronquée au budget de tokens.",
     "inputSchema": {"type": "object", "properties": {
         "note_id": {"type": "string"},
         "token_budget": {"type": "integer", "minimum": 200, "maximum": 12000, "default": 3000}},
         "required": ["note_id"]}},
    {"name": "get_topic_index",
     "description": "Renvoie l'index Obsidian d'un domaine (liste des meilleures fiches, une ligne chacune). « index » = index général.",
     "inputSchema": {"type": "object", "properties": {
         "topic": {"type": "string"},
         "token_budget": {"type": "integer", "minimum": 200, "maximum": 8000, "default": 2500}},
         "required": ["topic"]}},
]


def call_tool(name: str, args: dict) -> dict:
    schema = next((t['inputSchema'] for t in TOOLS if t['name'] == name), None)
    if schema is None:
        raise KeyError(name)
    validate_arguments(args, schema)
    if name == "search_knowledge":
        return rag.search_knowledge(str(args["query"])[:500], int(args.get("top_k", 5)), int(args.get("token_budget", 1500)),
                                    root=ROOT, include_rejected=bool(args.get("include_rejected", False)), domain=args.get("domain"))
    if name == "read_knowledge":
        return rag.read_knowledge(str(args["note_id"])[:40], int(args.get("token_budget", 3000)), root=ROOT)
    if name == "get_topic_index":
        return rag.get_topic_index(str(args["topic"])[:60], root=ROOT, token_budget=int(args.get("token_budget", 2500)))
    raise KeyError(name)


def validate_arguments(args, schema):
    if not isinstance(args, dict):
        raise ValueError('arguments must be an object')
    properties = schema.get('properties', {})
    if set(args) - set(properties) or set(schema.get('required', [])) - set(args):
        raise ValueError('unknown or missing argument')
    for key, value in args.items():
        rule = properties[key]
        kind = rule.get('type')
        if kind == 'string' and (not isinstance(value, str) or not value.strip() or len(value) > rule.get('maxLength', 2000)):
            raise ValueError(f'invalid string: {key}')
        if kind == 'integer' and (type(value) is not int or value < rule.get('minimum', 0) or value > rule.get('maximum', 12000)):
            raise ValueError(f'invalid integer: {key}')
        if kind == 'boolean' and type(value) is not bool:
            raise ValueError(f'invalid boolean: {key}')


def handle(msg: dict, *, tools=None, dispatcher=None, server=None):
    if not isinstance(msg, dict) or not isinstance(msg.get('method'), str):
        return {'jsonrpc': '2.0', 'id': None, 'error': {'code': -32600, 'message': 'Invalid Request'}}
    if msg.get('jsonrpc','2.0')!='2.0' or type(msg.get('id')) not in (str,int,type(None)):
        return {'jsonrpc':'2.0','id':None,'error':{'code':-32600,'message':'Invalid Request'}}
    method, mid = msg.get("method"), msg.get("id")
    if 'params' in msg and not isinstance(msg['params'], dict):
        return {'jsonrpc': '2.0', 'id': mid, 'error': {'code': -32602, 'message': 'params must be an object'}}
    if method == "initialize":
        asked = (msg.get("params") or {}).get("protocolVersion")
        return {"jsonrpc": "2.0", "id": mid, "result": {
            "protocolVersion": asked if asked in SUPPORTED else SUPPORTED[0],
            "capabilities": {"tools": {"listChanged": False}}, "serverInfo": server or SERVER,
            "instructions": "Bibliothèque VDN en lecture seule. Commencer par search_knowledge ; lire une fiche seulement si nécessaire."}}
    if method in ("notifications/initialized", "notifications/cancelled") or mid is None:
        return None
    if method == "ping":
        return {"jsonrpc": "2.0", "id": mid, "result": {}}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": mid, "result": {"tools": TOOLS if tools is None else tools}}
    if method == "tools/call":
        params = msg.get("params") or {}
        try:
            data = (dispatcher or call_tool)(params.get("name"), params.get("arguments") or {})
            return {"jsonrpc": "2.0", "id": mid, "result": {
                "content": [{"type": "text", "text": json.dumps(data, ensure_ascii=False, indent=1)}],
                "isError": bool(isinstance(data, dict) and data.get("error"))}}
        except (KeyError, ValueError, TypeError) as e:
            return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32602, "message": f"outil ou argument inconnu : {e}"}}
        except Exception as e:  # ne jamais faire tomber le serveur
            return {"jsonrpc": "2.0", "id": mid, "result": {"content": [{"type": "text", "text": f"Erreur : {type(e).__name__}: {e}"}], "isError": True}}
    return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": f"méthode inconnue : {method}"}}


def serve(handler=handle, *, initialize_index=True):
    # Windows : forcer l'UTF-8 sur stdin/stdout (sinon les accents cassent le JSON)
    for stream in (sys.stdin, sys.stdout):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    if initialize_index:
        try:
            rag.update_index(ROOT)
        except Exception as e:
            print(f"[vdn-knowledge] index non mis à jour : {e}", file=sys.stderr)
    while True:
        line = sys.stdin.readline(262146)
        if not line:
            break
        if len(line) > 262144:
            while line and not line.endswith('\n'):
                line = sys.stdin.readline(262146)
            sys.stdout.write(json.dumps({'jsonrpc':'2.0','id':None,'error':{'code':-32600,'message':'message too large'}})+'\n')
            sys.stdout.flush()
            continue
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line, parse_constant=lambda value: (_ for _ in ()).throw(ValueError('invalid JSON number')))
        except (ValueError, RecursionError):
            out = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "JSON invalide"}}
        else:
            out = handler(msg)
        if out is not None:
            sys.stdout.write(json.dumps(out, ensure_ascii=False) + "\n")
            sys.stdout.flush()


def main():
    serve()


if __name__ == "__main__":
    main()
