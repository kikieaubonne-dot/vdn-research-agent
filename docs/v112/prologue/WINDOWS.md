# Reprise Windows — procédure préparée, non exécutée sur le PC utilisateur

Cette session a accès à Linux, Python3.12.14 et Blender4.3.2. Aucun accès confirmé à `C:\Users\kikie\Documents\Eponge-V11.2`, PowerShell local, Claude Desktop ou Studio.

Extraire l'archive dans un **nouveau dossier**, conserver le dossier de travail et les configurations existants. Le paquet contient `source/`, `runtime/`, les contre-exemples, mandats et manifestes. Ne pas remplacer un dépôt modifié par l'archive. Si appliquer le patch sur un dépôt existant : vérifier d'abord HEAD et `git apply --check`, sans reset/clean.

Depuis le dossier `source` de la livraison :

```powershell
Get-Location
py -3.11 --version
Get-Command blender, ffmpeg, ffprobe -ErrorAction SilentlyContinue
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
py -3.11 -m agent.prologue --root '..\runtime' inventory
py -3.11 -m agent.prologue --root '..\runtime' brief
py -3.11 -m agent.prologue --root '..\runtime' replay
py -3.11 -m tests.offline
# Seulement après la fin de la suite précédente :
py -3.11 -m tests.personal_config
```

Attendu : inventaire PARTIAL, fin UNKNOWN ; replay SIMULATION_ONLY, pas d'exécution Studio. Suites hors ligne sans changement des paramètres personnels. Aucune de ces sorties ne confirme les durées de gameplay ou l'accès au PC par Codex. Le lanceur `Eponge.cmd` existant reste disponible ; son diagnostic doit signaler BLOCKED si aucune mission n'a été préparée dans son workspace. Aucun nouveau service/planificateur n'est installé.

## MCP Claude Desktop

Sauvegarder la configuration Desktop avant toute édition. Utiliser le chemin absolu de Python local et de `source/vdn_mcp.py`, avec arguments `--root <chemin absolu vers runtime> --v112`. Lancer manuellement en stdio ; aucun port réseau n'est ouvert par ce serveur. Vérifier dans Desktop la découverte des27 outils, puis demander :

- `get_intelligence_brief`, `question: "prologue:resources"`, `token_budget:500`.
- `get_intelligence_brief`, `question: "learning:animation:7849ea8324d87ac30e9aa67ef731ba115041eaf014a31844a326b72557ae4523"`.
- `synthesize_technical`, même question, sans apply/modèle, pour le détail.

La connexion Desktop réelle reste NON TESTÉE jusqu'à cette action locale. Le stdio cloud ne la remplace pas. Lecture seule pour ces références, y compris si d'autres permissions générales existent.

## Reproduction animation

Les artefacts réparés sont déjà fournis ; ne pas les regénérer systématiquement. Pour obtenir uniquement le plan d'un nouvel essai :

```powershell
py -3.11 -m agent.animation_roundtrip --root '..\runtime' --input 'lab/inbox/learning/prologue-v2/prologue-proxies.blend' --actor 'father_proxy-IK' --license OWN_CREATED --attest-rights --trusted-copy
```

Attendu : PLANNED, sans processus Blender ni changement du ledger. Avec `--apply`, le logiciel refuse un budget insuffisant avant démarrage. L'extension ponctuelle étant clôturée, la politique60s est rétablie et les77,058308s réellement réservées restent inscrites : aucun calcul restant aujourd'hui. Ne pas remettre le compteur à zéro, augmenter un quota ou présenter un test sur fixtures comme une expérience réelle. FBX peut être choisi comme format candidat, mais son résultat est encore non validé.

## Vision facultative

Le code est disponible via `agent.learning_vision.analyze`, avec `apply=True` et `allow_model=True` seulement après configuration explicite. Vérifier `ollama list` et `ollama show <nom exact installé>` localement ; aucun modèle recommandé par défaut ou à télécharger. Configurer la copie de laboratoire pour un modèle réellement installé, les drapeaux local/vision et l'endpoint loopback existant. Les appels partagent les quotas HTTP/modèles/calcul ; aucune exception au quota n'est créée. Sans modèle choisi/configuré, BLOCKED_NOT_CONFIGURED. Les réponses JSON correctes ne sont pas une validation de perception ou de procédure.

## Rollback

Les anciennes révisions narratives sont dans `project/history/`; les anciens exports rejetés restent dans `runtime/lab/inbox/learning/prologue-v2/`. Comparer les commits dans une copie, sans écraser le travail courant. Les checkpoints devenus obsolètes sont conservés et refusés à la reprise automatique. Le coffre Obsidian de test a déjà été rollbacké ; aucun coffre personnel ciblé. Aucun nouveau commit n'est automatiquement promu comme image de récupération approuvée.
