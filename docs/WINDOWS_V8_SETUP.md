# Installation locale Windows — V8

Statut : commandes et chemins préparés pour Python 3.12 ; tests exécutés sous
Linux, **pas sur un PC Windows réel**. Aucun déploiement sur le PC utilisateur
n'a été effectué. Git est utile pour récupérer les mises à jour ; aucune clé API.

## Installer et vérifier

Dans PowerShell, avec Python 3.12 installé et accessible via `py` :

```powershell
git clone --branch codex/knowledge-engine-v8 https://github.com/kikieaubonne-dot/vdn-research-agent.git C:\VDN\vdn-research-agent
Set-Location C:\VDN\vdn-research-agent
py -3.12 -m venv .venv
$env:PYTHONUTF8 = "1"
.\.venv\Scripts\python.exe -m tests.offline
```

Si le dossier existe déjà, conserver le clone et ses données avant de changer
de branche. Aucun `pip install` n'est nécessaire. Vérifier FTS5 :

```powershell
.\.venv\Scripts\python.exe -c "import sqlite3; c=sqlite3.connect(':memory:'); c.execute('create virtual table t using fts5(x)'); print('FTS5 disponible')"
```

Le fallback SQLite LIKE fonctionne sans FTS5, avec une pertinence et des
performances non garanties par le benchmark FTS5. Les tests de symlinks sont
ignorés si le compte Windows ne peut pas créer de liens symboliques ; les autres
tests ne requièrent pas de droits administrateur.

## Utiliser sans Claude et sans réseau

```powershell
.\.venv\Scripts\python.exe -m agent.local search "importer un squelette personnalisé, os qui buguent"
.\.venv\Scripts\python.exe -m agent.local get vdn-1290b940c378
.\.venv\Scripts\python.exe -m agent.local procedures "créer un sapin enneigé réaliste pour Roblox"
.\.venv\Scripts\python.exe -m agent.local plan "Je veux refaire entièrement la forêt enneigée de mon jeu d'horreur Roblox."
```

Les réponses sont du JSON. Les originaux dans `knowledge/` sont lus, jamais
réécrits. L'index dérivé `output/knowledge.db` est créé à la première lecture,
puis rafraîchi si les dates/tailles des Markdown changent. Un changement conservant
artificiellement ces métadonnées peut demander un redémarrage.
Les commandes historiques `python -m agent.run cycle`, `refresh`, `queue`, etc.
restent disponibles ; **cycle et refresh font du réseau**, contrairement à
`agent.local` et au serveur MCP V8.

## Reproduire les résultats

```powershell
.\.venv\Scripts\python.exe -m bench.evaluate_v8 --root . --output work\rag-v8.json
.\.venv\Scripts\python.exe -m bench.demonstrate_v8 --root . --output-dir work\demos-v8
```

Les outils utilisent une copie temporaire pour indexer le corpus. Les 106
fichiers de référence restent intacts. Voir [le guide MCP](CLAUDE_DESKTOP_V8.md)
pour l'accès depuis Claude Desktop.
