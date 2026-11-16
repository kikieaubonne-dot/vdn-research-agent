# Briefings Claude et vérification Windows

Statut : ENGINEERING_PROPOSAL / PARTIAL. Aucune édition ni publication du jeu.
Les fichiers B3/C1, la lampe V2 et le contrôleur ne sont pas accessibles ici.
La priorité rapportée est la forêt jouable, sans scénario de bêta confirmé.

## Collisions — première tâche

**Objectif.** Reproduire puis réduire les blocages du joueur contre les troncs et
branches de copies B3/C1. Aucun diagnostic confirmé sans inspection.

**Contexte.** Roblox, première personne, forêt d'épicéas enneigée de nuit.
Assets/contrôleur/build Studio/appareil : UNKNOWN. Préserver le visuel témoin,
les originaux et les paramètres de production. Composant `TreeCollisionHarness` :
PROPOSED ; emplacement réel : UNKNOWN.

**Hypothèses.** Un volume physique plus large que le passage visuel ou une
interaction du contrôleur avec les branches pourrait contribuer. D'autres causes
restent possibles ; aucune n'est déduite du seul nom de l'asset.

**Solution candidate.** Inventorier/visualiser les limites physiques, puis comparer
la représentation actuelle et une seule variante. Si le modèle utilise des
MeshParts, tester une autre fidélité uniquement après examen de sa géométrie et
du parcours. La séparation visuel/physique est une alternative d'ingénierie à
valider, pas une solution optimale présumée.

**Implémentation.** Identifier les vrais composants tronc/branches/feuillage et
leurs propriétés. Capturer les valeurs actuelles. Créer A témoin et B dans une
scène locale dédiée. Marquer un parcours identique près du tronc, sous les
branches et sur la pente. Mesurer A, changer un seul facteur dans B, rejouer avec
le même contrôleur. Si aucun passage ne reproduit le problème, arrêter et
clarifier le symptôme avant toute modification.

**Preuves.** Documentation officielle collisions, section Mesh and solid model
collisions ; [reçu complet et portée](DISCOVERIES.md). CollisionFidelity documente
l'alignement des limites physiques et visuelles ; aucune valeur idéale pour B3/C1
n'est connue. Pas de FPS, dimensions, nombre de colliders ou valeur numérique
inventés. Le clone sans snapshot ne dispose que d'une archive secondaire : demander
l'original local ou conserver l'abstention sur les faits.

**Tests.** [Protocole collisions](ROBLOX_TEST_PROTOCOL.md), observations de blocage,
position/action/composant et éventuelles mesures physiques sous mêmes conditions.
Critères proposés à confirmer : moins de blocages reproduits, pas de nouvelle
traversée de tronc, pas de régression du contrôleur. Coût admissible à décider
avant l'essai ; aucune valeur cible confirmée.

**Risques/rollback.** Nouvelle zone bloquante, traversée, coût physique ou résultat
limité à un contrôleur. Restaurer les copies et paramètres témoins, conserver les
preuves. Aucun changement au jeu publié.

**Question bloquante.** Où se trouve la copie autorisée de scène contenant B3/C1
et le contrôleur actuel ? Si uniquement sur le PC Windows, effectuer l'essai
humainement avec ce protocole, sans déclarer son exécution à distance.

## Sapins et lampe — tâches suivantes, proposées

- **Sapins :** même arbre/caméra/lumière, une variation de silhouette OU feuillage
  OU neige. Inspecter d'abord les sources et fichiers existants. Les cartes de
  feuillage, la géométrie et les cartes PBR sont des candidats connus, pas des
  gains démontrés. Captures proches/lointaines et avis humain séparés des mesures.
- **Lampe V2 :** inventorier le prototype réel, puis changer un seul facteur
  documenté du faisceau/lumière. Garder caméra, trajet, arbres et exposition fixes.
  Aucune portée/intensité/couleur optimale inventée ; [protocoles](ROBLOX_TEST_PROTOCOL.md).

## Requêtes MCP reproductibles

Lire les schémas renvoyés par tools/list avant les outils d'écriture.
Les 27 contrats restent identiques ; `--v112` est un mode explicite.

| Besoin | Outil / arguments |
|---|---|
| Bible | get_intelligence_brief : `{"question":"Bible du jeu","token_budget":1800}` |
| Collisions | get_intelligence_brief : `{"question":"collisions","token_budget":1800}` |
| Préparation détaillée conservée | get_intelligence_analysis : `{"key":"CLE_RENVOYEE"}` |
| Prévisualisation actuelle non conservée | synthesize_technical : `{"question":"collisions","apply":false,"allow_model":false,"retrieval":"lexical"}` |
| Sources dans les notes | search_knowledge : `{"query":"Roblox collisions CollisionFidelity"}` |
| Alternatives et procédure | Détail de la carte : alternatives, implementation, test, sources |
| Échecs | get_experiment_context : `{"problem":"collision","status":"FAILED","detailed":true}` ; get_experiment avec son ID |
| Tâches/prérequis | get_intelligence_brief : `{"question":"pack prochaines tâches","token_budget":1800}` |
| Recherche bornée proposée | plan_ocean/prepare_ocean, puis run_ocean uniquement sous capacités/reseau explicites du contrat existant |

Respecter `detail_tool` du briefing : une prévisualisation peut avoir une clé
non persistée et demande alors `synthesize_technical` avec la même question.
Ne pas tenter de récupérer cette clé comme une analyse enregistrée. Une archive
publique conserve ses candidats de paramètres dans `archived_parameter_candidates`,
pas dans les paramètres actuellement documentés.

## Windows — procédure courte, sans installation implicite

Dans le clone existant, relever `git status`, conserver les modifications et
sauvegarder configuration/runtime avant toute mise à jour. Le nouveau commit
corrige le mode projet ; ne pas remettre une ancienne queue pour le tester.
Les commandes ci-dessous supposent une installation Python déjà existante.

```powershell
Set-Location "C:\chemin\vdn-research-agent"
$env:PYTHONUTF8 = "1"
$python = Join-Path $PWD ".venv\Scripts\python.exe"
& $python --version
& $python -m agent.v112 bible
& $python -m agent.v112 brief "collisions" --token-budget 1800
& $python -m agent.v112 task collisions
& $python -m agent.v112 budget
```

Attendu : Bible avec statuts ; briefing PARTIAL ; B3/C1 inconnus ; abstention sur
les faits dans un clone sans originaux ; budget lu sans changement. `task` peut
montrer l'archive et ses métadonnées ; elle ne devient pas une preuve primaire.

Sauvegarder le fichier Claude Desktop existant et fusionner manuellement une
entrée, sans remplacer ses autres serveurs. Chemins à adapter :

```json
{"mcpServers":{"eponge":{"command":"C:\\chemin\\vdn-research-agent\\.venv\\Scripts\\python.exe","args":["C:\\chemin\\vdn-research-agent\\vdn_mcp.py","--root","C:\\chemin\\vdn-research-agent","--v112"],"env":{"PYTHONUTF8":"1"}}}}
```

Relancer l'application, vérifier la connexion et les 27 outils, puis demander
Bible → collisions → détail → sources → échecs avec les requêtes du tableau.
Attendu : aucune revendication d'essai B3/C1, sources secondaires signalées,
permissions d'écriture refusées par défaut. Noter version Desktop, SHA du dépôt,
message d'erreur éventuel et résultats ; ne pas déclarer Desktop validé avant cela.
Pour les expériences, `--allow-experiments` autorise les opérations MCP concernées,
pas la revue VERIFIED. `--allow-intelligence` reste séparé ; aucun modèle nécessaire.

## Obsidian isolé et rollback

```powershell
$vault = Join-Path $env:TEMP ("VDN-validation-" + [guid]::NewGuid())
& $python -m agent.v112 sync --destination $vault
$export = (& $python -m agent.v112 sync --destination $vault --apply | ConvertFrom-Json)
& $python -m agent.v112 sync --destination $vault --apply
& $python -m agent.v112 sync --destination $vault --rollback $export.transaction --apply
```

Attendu : simulation, committed, unchanged, rolled_back. Conserver l'identifiant.
Le coffre personnel ne doit pas être utilisé. Pour exporter explicitement le détail
privé des expériences, le CLI historique `agent.v10 sync --include-lab` reste
nécessaire ; le sync projet par défaut ne publie pas ces expériences privées.
Les pages `_VDN-*` restent exclues du corpus technique.

Reproduction logicielle complète, si un laboratoire avec originaux est disponible :

```powershell
& $python -m bench.validate_v112_field --workspace C:\lab\nouvelle-validation --runtime C:\lab\ancien-laboratoire
```

Le répertoire de validation doit être nouveau et hors du dépôt. Cette commande
crée des **expériences synthétiques étiquetées**, bloque les sockets et teste de
vrais processus stdio ; elle n'exécute ni Studio ni Claude Desktop. Les traces
complètes restent privées sous ce répertoire. Aucun original ni budget source
n'est remplacé. Sans originaux, effectuer les lectures/abstentions ci-dessus.
