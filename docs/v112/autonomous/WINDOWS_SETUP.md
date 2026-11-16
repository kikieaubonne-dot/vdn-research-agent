# Windows — installation existante et validations séparées

Préserver le clone, la configuration Claude et les données avant mise à jour.
La PR #8 reste non fusionnée ; consulter sa branche sans toucher main. En cas de
modifications personnelles en conflit, employer un clone/worktree séparé et garder
les compteurs courants, pas une copie d'anciens budgets pour obtenir plus de quota.
Python 3.11 et bibliothèque standard ; aucun pip/model download implicite.

```powershell
Set-Location "C:\chemin\vdn-research-agent"
$env:PYTHONUTF8 = "1"
$python = Join-Path $PWD ".venv\Scripts\python.exe"
& $python --version
git status --short
& $python -m agent.v112 bible
& $python -m agent.v112 chapters chapter1
& $python -m agent.v112 brief "chapitre 2" --token-budget 1800
& $python -m agent.v112 lab-capabilities
& $python -m agent.v112 budget
```

Attendu : rôles Léo/policier distingués, chapitre 2 PROPOSED, pas de preuve moteur,
runner sans publication/Studio, budget lu sans remise à zéro. Les archives d'ancienne
Bible restent historiques ; elles peuvent être périmées et requérir une nouvelle
analyse hors ligne. Aucun ancien fichier n'est effacé pour cela.

Pour Claude Desktop, sauvegarder sa configuration puis intégrer l'entrée en
conservant ses autres serveurs :

```json
{"mcpServers":{"eponge":{"command":"C:\\chemin\\vdn-research-agent\\.venv\\Scripts\\python.exe","args":["C:\\chemin\\vdn-research-agent\\vdn_mcp.py","--root","C:\\chemin\\vdn-research-agent","--v112"],"env":{"PYTHONUTF8":"1"}}}}
```

Relancer Desktop, vérifier connexion/27 outils puis les requêtes de
[CLAUDE_MCP_WORKFLOW](CLAUDE_MCP_WORKFLOW.md). Relever version Desktop/SHA/résultats ;
ne pas confondre CI Windows, stdio et validation effective sur ce PC.

## Blender — aucun installateur automatique

Utiliser uniquement un Blender déjà installé, chemin explicite à adapter :

```powershell
$blender = "C:\chemin\Blender 5.2\blender.exe"
& $blender --version
$job = (& $python -m agent.v112 lab-prepare --required-version 5.2 --apply | ConvertFrom-Json)
& $python -m agent.v112 lab-run $job.id --executable $blender --allow-blender
```

C'est une démonstration sur primitives, pas B3/C1 ni une mesure de qualité visuelle.
Version différente → BLOCKED. Pour mesurer une copie de confiance seulement :

```powershell
$copyJob = (& $python -m agent.v112 lab-prepare --input "lab/inbox/copie.blend" --unit-scale 1 --required-version 5.2 --apply | ConvertFrom-Json)
& $python -m agent.v112 lab-run $copyJob.id --executable $blender --allow-blender
```

**Remplacer 1 par l'échelle réellement enregistrée dans la copie**, pas une valeur
optimale ni présumée. Version/échelle non concordantes → échec d'import conservé.
Le runner n'enregistre/modifie pas le .blend source et ne publie rien. Des rapports
PARTIAL_SUCCESS restent non vérifiés ; leurs métriques ne sont pas des FPS Roblox.
Pas de script arbitraire, de plugin téléchargé ou de libération GPU automatique.

## Studio, images et Obsidian

Aucun pont Studio actif n'est livré. Utiliser le protocole B3/C1 de
`../continuity/ROBLOX_TEST_PROTOCOL.md` dans une scène copiée ; ne pas installer le
collecteur historique dans le jeu publié. Fournir de vraies observations/captures
et version/controller. Heartbeat n'est pas le framerate rendu.

Pour une référence sans modèle visuel, utiliser `visual-describe` selon le guide
[VISUAL_PIPELINE](VISUAL_PIPELINE.md) ; aucune analyse automatique annoncée.

```powershell
$vault = Join-Path $env:TEMP ("VDN-lab-" + [guid]::NewGuid())
& $python -m agent.v112 sync --destination $vault
$export = (& $python -m agent.v112 sync --destination $vault --apply | ConvertFrom-Json)
& $python -m agent.v112 sync --destination $vault --apply
& $python -m agent.v112 sync --destination $vault --rollback $export.transaction --apply
```

Attendu : simulation, committed, unchanged, rolled_back. Ne pas utiliser le coffre
personnel pour cette validation. Les pages de chapitres sont réservées et exclues
du RAG technique. Pour mémoire expérimentale privée, exporter explicitement via
le mécanisme include-lab historique ; elle n'est pas une source primaire.

Ollama reste facultatif ; guides V11.1 conservés pour diagnostic RAM/VRAM, modèles
réellement installés et comparaison. Aucun modèle par défaut recommandé sur les
seuls 8 Go annoncés. Pas de gains de quota Claude mesurés.
