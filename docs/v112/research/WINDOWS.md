# Mise en service Windows et reprise

PC Windows utilisateur, interface Claude Desktop et Roblox Studio : **NON TESTÉS**
dans cette mission. La CI Windows valide Python/MCP stdio dans une machine GitHub.
Les commandes suivantes utilisent le dépôt existant ; aucun service permanent.

## Vérifier sans écraser

Dans PowerShell, depuis votre copie du dépôt :

```powershell
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"
git status --short
git branch --show-current
git rev-parse HEAD
py -3.11 --version
```

Attendu : branche `codex/project-intelligence-v11-2`, SHA publié dans la PR #8,
Python3.11 disponible. Si votre copie contient des changements, les préserver ;
ni reset/clean, ni restauration de queue/config. Un fetch seul ne remplace pas
vos fichiers. Examiner les différences avant toute mise à jour locale.

## Recherche sans modèle ni réseau

```powershell
py -3.11 -m agent.v112 library
py -3.11 -m agent.v112 roots "forest" --depth 6 --nodes 24
py -3.11 -m agent.v112 roots "forest/spruce/foliage/cards/alpha/shadows/flashlight" --depth 0
py -3.11 -m agent.v112 brief "tree:forest/collisions"
py -3.11 -m agent.v112 synthesize "tree:forest/collisions"
```

Attendu : vues MAIN/RESERVE/ARCHIVE (32/25/42 sur le corpus livré), arbre borné,
lacunes ouvertes et dépendances, briefing PARTIAL avec candidats et `detail_question`,
puis `research_detail` avec protocole proposé, sources et limites. Un clone sans
originaux ne doit pas affirmer des faits validés. SQLite peut être réindexé ; aucune
collecte, appel Ollama, modification d’asset ou promotion de statut moteur.

```powershell
py -3.11 -m agent.v112 root-prepare "forest/spruce/foliage/cards" --depth 0
```

Attendu : simulation, aucune session créée. Pour une collecte manuelle, sur un
runtime **isolé et déjà autorisé/configuré** avec les quotas existants :

```powershell
$EpongeRuntime = "D:\chemin-explicitement-autorise\runtime-isole"
py -3.11 -m agent.v112 --root $EpongeRuntime root-prepare "forest/spruce/foliage/cards" --depth 0 --apply
# Reprendre exactement l'id retourné, sans nouvelle session pour contourner une limite.
$SessionId = "REMPLACER-PAR-ID-RETOURNE"
py -3.11 -m agent.v112 --root $EpongeRuntime root-run $SessionId --apply --allow-network
py -3.11 -m agent.v112 --root $EpongeRuntime root-control $SessionId pause --apply
py -3.11 -m agent.v112 --root $EpongeRuntime root-control $SessionId resume --apply
```

Le serveur CLI ne reconfigure pas votre réseau. Si `network_enabled=false`, provider
non autorisé, budget atteint ou configuration changée : refus/arrêt explicite,
sans hausse de quota. Après limite tick, reprendre le même ID si budget session
restant ; après limite session, ne pas remettre les compteurs à zéro. Une portée
épuisée peut renvoyer NO_RESEARCH_NEEDED avec lacunes encore ouvertes : examiner
les preuves partielles et les arrêts, pas proclamer la technique prête.

## MCP stdio et Claude Desktop

```powershell
py -3.11 .\vdn_mcp.py --root (Get-Location).Path --v112
```

Attendu : processus stdio attendant des messages JSON-RPC. Il n’affiche pas une
interface et ne démarre pas de service réseau. Ctrl+C ferme ce processus. Les
permissions de recherche/expérience/modèle ne sont pas activées par cette commande.

Pour une vérification logicielle reproductible, sans toucher au coffre personnel :

```powershell
$ValidationDir = Join-Path $env:TEMP ("eponge-roots-" + [guid]::NewGuid())
py -3.11 -m bench.validate_research_roots --workspace $ValidationDir
```

Attendu : 20 lignes de résultat, aucun FAIL. Sans `--runtime` contenant des captures
réelles autorisées, la vérification des originaux est PARTIAL ; les tests de mémoire
sont synthétiques. Ce harnais utilise un vrai sous-processus MCP, pas Desktop.

Si vous décidez d’ajouter L’Éponge à Desktop, préserver la configuration existante :

```powershell
$ClaudeConfig = Join-Path $env:APPDATA "Claude\claude_desktop_config.json"
if (Test-Path $ClaudeConfig) {
  Copy-Item -LiteralPath $ClaudeConfig -Destination ($ClaudeConfig + ".bak-" + (Get-Date -Format "yyyyMMdd-HHmmss"))
}
py -3.11 -c "import sys; print(sys.executable)"
```

Ajouter manuellement une entrée au `mcpServers` existant, en remplaçant les chemins
par les chemins absolus effectivement présents ; conserver toutes les autres entrées :

```json
"eponge": {
  "command": "C:\\chemin\\python.exe",
  "args": ["D:\\vdn-research-agent\\vdn_mcp.py", "--root", "D:\\vdn-research-agent", "--v112"]
}
```

Relancer Desktop humainement. Attendus : les 27 outils, puis demander la Bible,
`get_intelligence_brief(question="tree:forest/collisions")` et
`synthesize_technical(question="tree:forest/collisions")`. Vérifier URLs, captures
absentes, versions et inconnues. Desktop réel reste NON TESTÉ tant que vous n’avez
pas relevé ces résultats sur votre PC. Les processus et logs stdio seuls ne prouvent
pas le fonctionnement de son interface.

## Retour d’expérience et rollback

Exécuter les essais humains exclusivement sur copies : témoin A, variante B avec
une seule variable. Garder build Studio, contrôleur, assets/révisions, appareil,
observations brutes, erreurs et artefacts. Employer les outils existants
`prepare_experiment/start_experiment/record_experiment_result` avec permission
`--allow-experiments` explicitement choisie. Lier dans `parameters` :
`project_task="collisions"`, `research_branch="forest/collisions"`. Ne jamais
importer une fixture comme résultat B3/C1 ni forcer VERIFIED ; revue humaine séparée.
Après FAILED, consulter le même briefing et `get_experiment_context` : échec,
conditions, hypothèses et recherche ciblée doivent apparaître.

Rollback logiciel : arrêter le processus, préserver runtime/config/exports et
consulter `ad2fc6b` dans un clone séparé. Ce code ne comprend pas les nouvelles
commandes roots et réintroduit le faux vide corrigé ; conserver le runtime courant
intact. Aucun downgrade/migration automatique des données.

Rollback Obsidian : utiliser la transaction renvoyée par `agent.obsidian.sync`
et `agent.obsidian.rollback(destination, transaction_id, apply=True)` dans le coffre
**isolé**. Les conflits manuels sont refusés ; ne pas effacer le coffre pour les
contourner. Le scénario 19 exerce cette séquence et conserve les notes sources.

## Mesures reproductibles

```powershell
py -3.11 -m tests.offline
py -3.11 -m tests.personal_config
py -3.11 -m bench.evaluate_lab_retrieval --output (Join-Path $env:TEMP "eponge-rag22.json")
py -3.11 -m bench.evaluate_roots --output (Join-Path $env:TEMP "eponge-rag12.json")
```

Pas de modèle téléchargé, aucune API payante et aucun accès au jeu publié. La
configuration personnelle est copiée pour les tests, jamais écrasée pour produire
un résultat. [Rapport et limites](REPORT.md).
