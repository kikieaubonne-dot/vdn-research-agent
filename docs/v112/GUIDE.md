# Utilisation Windows et Claude

V11.2 est un mode explicite, sur la branche `codex/project-intelligence-v11-2`.
Python 3.11, Git et la bibliothèque standard suffisent. Dans un clone existant,
commencer par la [sauvegarde](MIGRATION.md), conserver les modifications locales
et éviter les changements de branche si des fichiers personnels entrent en conflit.
Pour une installation distincte :

```powershell
git clone --branch codex/project-intelligence-v11-2 https://github.com/kikieaubonne-dot/vdn-research-agent.git vdn-v112
Set-Location vdn-v112
$env:PYTHONUTF8 = "1"
py -3.11 -m venv .venv
$python = Join-Path $PWD ".venv\Scripts\python.exe"
& $python -m tests.offline
& $python -m tests.personal_config
& $python -m agent.v112 bible
& $python -m agent.v112 plan
& $python -m agent.v112 budget
& $python -m agent.v112 daily
& $python -m agent.v112 pack --limit 3
```

La Bible est `project/bible.json`. Le Markdown [BIBLE](../../project/BIBLE.md)
est une vue générée. Modifier explicitement le JSON après décision humaine,
augmenter sa révision, puis régénérer le Markdown. Une question CONFIRMED exige
une réponse explicite. Les priorités P0/P1 restent PROPOSED. Une ancienne idée
n'est jamais confirmée par le seul passage du temps.

## Consultation et synthèse

```powershell
& $python -m agent.v112 task collisions
& $python -m agent.v112 brief "Corriger les collisions des sapins Roblox" --token-budget 1800
& $python -m agent.v112 synthesize "collisions"
& $python -m agent.v112 synthesize "collisions" --apply
& $python -m agent.v111 search "collisions"
& $python -m agent.v11 search "SurfaceAppearance"
```

`task` consulte d'abord une préparation conservée. `synthesize` réévalue les
sources locales. Sans `--apply`, aucun résultat n'est écrit et aucun modèle
n'est appelé. La nouvelle synthèse d'un clone sans snapshots pourra avoir moins
de preuves que la préparation publiée : les notes historiques et l'archive ne
remplacent pas les originaux. Une version Blender explicitement incompatible
produit CONSTRAINT_CONFLICT. Une question ambiguë appelle une seule clarification.
Les nombres fournis par l'utilisateur demeurent des contraintes proposées.

## Collecte bornée, lancée manuellement

Faire ces essais dans une copie isolée conservant ses propres compteurs. Activer
explicitement `network_enabled` dans sa configuration V10 sans changer les quotas.
Le transport direct reste la valeur normale ; un proxy de confiance n'est
activé que si l'opérateur reconnaît et autorise ce proxy. Les robots/refus sont
conservés. Un tick ne représente pas toute la session :

```powershell
& $python -m agent.v112 research-prepare --tasks trees collisions lighting
$session = (& $python -m agent.v112 research-prepare --tasks trees collisions lighting --apply | ConvertFrom-Json)
& $python -m agent.v112 research-run $session.id --apply --allow-network
& $python -m agent.v112 control $session.id pause --apply
& $python -m agent.v112 control $session.id resume --apply
& $python -m agent.v112 research-run $session.id --apply --allow-network
```

Relancer le même identifiant poursuit la session avec ses budgets. Ne pas effacer
la file ni modifier ses compteurs. Un plafond de session atteint exige une
nouvelle décision de recherche bornée, pas une remise à zéro. STOPPED est terminal.
PROJECT_CHANGED impose un nouveau plan explicite ; la session antérieure demeure.
`acquisition_state=COMPLETE` signifie file terminale ; `state=PARTIAL` conserve
les lacunes. Le rapport d'erreurs indique les sources indisponibles ou insuffisantes.
Une tentative de récupération peut être servie par cache ; les HTTP effectifs,
robots et reprises réseau sont comptés par le transport existant.

La session de livraison `52974000-e519-42d0-a653-01fc97e89a60` est terminale dans
le laboratoire isolé de livraison, pas installée sur le PC Windows. Les fiches
publiques sont consultables immédiatement ; ses snapshots privés doivent être
transférés explicitement ou collectés à nouveau dans votre environnement avant
vérification des citations originales.

## MCP Claude Desktop

Adapter tous les chemins, ne pas modifier le fichier existant sans sauvegarde :

```json
{"mcpServers":{"eponge":{"command":"C:\\projets\\vdn-v112\\.venv\\Scripts\\python.exe","args":["C:\\projets\\vdn-v112\\vdn_mcp.py","--root","C:\\projets\\vdn-v112","--v112"],"env":{"PYTHONUTF8":"1"}}}}
```

Les **27 outils**, schémas d'entrée et annotations restent identiques à V11.1.
`get_intelligence_brief` accepte par exemple :

```json
{"question":"Corriger les collisions des sapins Roblox","token_budget":1800}
```

Utiliser aussi `question="Bible du jeu"` ou `question="pack prochaines tâches"`.
`get_intelligence_analysis` accepte la clé de fiche ou d'analyse pour obtenir le
détail. Une archive publique est marquée secondaire, sans faits revalidés dans
ce clone. `synthesize_technical` conserve les champs de l'analyse et ajoute
`project_card`. `search_intelligence` reste la recherche des analyses locales ;
les cartes publiques passent par les briefs/clés, pas par un faux index de sources.

Ajouter `--allow-intelligence` au serveur uniquement pour les écritures/modèles
explicitement demandés ; les capacités recherche/expériences restent distinctes.
Les outils V10 d'expériences permettent de conserver les échecs avec
`parameters.project_task="collisions"` ou `environment.project_task`.
Lier la tâche n'atteste ni B3/C1, ni la recette, ni la version. La revue humaine
avec preuves et conditions reste nécessaire. Aucun outil ne modifie le jeu.
Le stdio a été testé ; l'interface Claude Desktop et le quota Claude n'ont pas
été mesurés.

## Ollama facultatif et diagnostic matériel

L'adaptateur V11.1 est conservé. Voir [installation Windows](../v111/WINDOWS_OLLAMA.md)
et [choix/comparaison de modèles](../v111/MODELS.md). Ne télécharger aucun modèle
sur la seule base d'un nombre de paramètres. Qwen3/Gemma3 sont des candidats,
pas des recommandations validées pour ce corpus.

```powershell
ollama --version
ollama list
ollama ps
nvidia-smi
Get-CimInstance Win32_OperatingSystem | Select-Object TotalVisibleMemorySize,FreePhysicalMemory
& $python -m agent.v111 diagnose
$model = Read-Host "Nom exact d'un modèle déjà installé, tag inclus"
ollama show $model
& $python -m agent.v111 diagnose --probe --model $model
& $python -m agent.v112 synthesize "collisions" --apply --allow-model
```

Le dernier appel exige aussi la configuration Intelligence activée et le modèle
exact choisi. Le probe consomme ses réservations HTTP locales. Le mode economy
et le contexte borné sont conservés. VRAM libre, quantification, KV cache et
Studio/Blender/Unreal ouverts comptent ; aucune capacité 8 Go n'est garantie.
Un échec renvoie une fiche déterministe partielle et conserve le journal.
Aucun modèle réel ni embeddings réels n'a été exécuté pour V11.2.

## Obsidian et références visuelles

```powershell
$vault = "C:\projets\VDN-Obsidian"
& $python -m agent.v112 sync --destination $vault
& $python -m agent.v112 sync --destination $vault --apply
& $python -m agent.v112 sync --destination $vault --rollback TRANSACTION_ID --apply
```

Prévisualiser, conserver l'identifiant de transaction. Une page réservée par tâche
évite les doublons ; les conflits ne sont pas écrasés et les pages générées sont
exclues du RAG technique. La Bible, le pack et les dix fiches préparées sont inclus.

Pour une image choisie par l'opérateur, la placer sous `lab/inbox/`, puis :

```powershell
& $python -m agent.v112 visual-link trees "lab/inbox/reference.png" --target "Silhouette nordique" --keep "irrégularité" --avoid "symétrie répétitive" --render-version "B3-prototype" --human-opinion "À comparer humainement" --apply
```

Trois références maximum par tâche, 1 Mo chacune, 8 Mo cumulés de pièces liées.
L'entête du fichier est contrôlé, pas l'image décodée ni interprétée. L'avis est
celui de l'opérateur ; `visual_analysis_performed=false`. Une image n'établit
aucune faisabilité Roblox.
