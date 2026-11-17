# Reprise exacte après mandat V10

Lire REPORT.md, BLACK_BOX.md, J0_J3.md, RESOURCE_INVENTORY.md, WINDOWS.md et `proofs/test-summary.json`. Commit et archive exacts : fichier `DELIVERY_SUMMARY.json` livré à côté du paquet. Source initiale `9821499`, même branche, aucun push ou PR.

## Acquis à ne pas recommencer

- Bake visuel réel : gestes des deux proxies préservés au roundtrip Blender4.3.2/GLB,25 poses, articulations/matrices de déformation/surfaces/durée. Les anciens GLB restent rejetés.
- Le premier contrôle de tails a échoué ; cette preuve reste conservée. L'importeur recrée les longueurs d'affichage. interop-2 compare les invariants encodés, avec la même tolérance1e-5, et conserve les écarts de tails.
- Vidéo locale V9 et ses protections conservées ; vision préparée, tests mockés, aucun modèle réel lancé. Pas de nouvelle collecte Web, YouTube ou transcription réelle.
- Bible r3, chapitres r2,36 ressources et déroulé A–E, fin F UNKNOWN ; anciennes révisions préservées. Le policier est jouable dès E. Sprint Shift seul si besoin pendant B.
- Prototype de progression et reprise testé en Python ; Luau fourni mais NON EXÉCUTÉ. Aucun prologue assemblé/joué dans Studio.

## Où récupérer le résultat

Artefacts :

- `artifacts/gesture-primary.blend` et `.glb` : acteur réparé `father_proxy-IK`. Le natif contient aussi d'autres anciens acteurs non réparés ; ne pas les promouvoir.
- `artifacts/gesture-transfer.blend` et `.glb` : gabarit plus étroit, bake et import contrôlés indépendamment.
- Rejets : `runtime/lab/inbox/learning/prologue-v2/*-IK.glb`. Conserver noms et empreintes, ne pas remplacer ces fichiers par les nouveaux.
- Specs, logs, rapports gzip et reçus : `runtime/lab/learning/animation/` et `runtime/lab/inbox/learning/animation-*`.

MCP existant, lecture seule :

```text
get_intelligence_brief(question="prologue:resources", token_budget=500)
synthesize_technical(question="prologue:resources")
get_intelligence_brief(question="learning:animation:7849ea8324d87ac30e9aa67ef731ba115041eaf014a31844a326b72557ae4523")
get_intelligence_brief(question="learning:animation:86eb50f9e07e8a0a318473653c6a1c93ac47e3cab9b95167487e28cada88f632")
get_intelligence_brief(question="learning:discovery:3e11c5a154a5df5eef2df53c8dc7b3f3120e155ac7e581ff13f176472732eb78")
```

`synthesize_technical` avec les mêmes références donne les détails. apply/modèle refusés pour ces lectures. Aucun outil ajouté aux27 contrats. Les deux expériences SUCCESS dans le LabStore restent non vérifiées humainement ; leurs IDs figurent dans `proofs/new-experiment-ids.json`.

## Prochaine action utile

Dans un environnement local autorisé, identifier **une copie de scène Studio**, son contrôleur et un rig cible. Tester d'abord l'import/retargeting d'un geste réparé sur ce rig, en choisissant un format réellement accepté par le pipeline local. FBX, Blender5.2, Windows, Studio et le contrôleur réel ne sont pas validés ici. Ne pas généraliser du proxy16 os à un personnage Roblox final.

En parallèle, assembler le trajet J0 A→E avec proxies et événements proposés : maison/post-it, départ de Maëlle, disparition, confrontation interactive, appel, enquêteur. Les fichiers ou composants inconnus restent UNKNOWN. Ne pas créer la fin officielle F ni un tutoriel complet pendant la première poursuite.

Les critères10s/30s/60s/20s et7–9min sont des hypothèses de design. Les mesurer avec de vrais joueurs sur le parcours copié ; le replay Python ne constitue pas cette preuve.

## Ressources et autorisations

Runtime précédent intact :59,596431/60s. Copie V10 temporairement autorisée à80s, compteur final77,058308s, HTTP9/fetch5 hérités inchangés, aucun modèle lancé. Extension ensuite clôturée : politique60s originale rétablie sans diminution du compteur, aucun calcul restant aujourd'hui ni allocation80s récurrente. La réserve de contenu supplémentaire est bloquée ; ne pas réinitialiser, relever les quotas, déplacer du contenu pour les contourner ou lancer une nouvelle enveloppe implicite. Les tests de développement sur fixtures sont séparés des véritables expériences.

Aucun worker ou service permanent n'est à reprendre. La restauration automatique reste réservée aux images explicitement approuvées dans le mécanisme historique. Les nouveaux commits et techniques de laboratoire ne sont pas automatiquement promus.

## Reprise et rollback

L'archive contient code, patch depuis9821499, runtime avec compteurs conservés, preuves, mandats et manifestes. Extraire dans un nouveau dossier et vérifier le checksum ; ne pas écraser le dossier Windows existant. Guide court dans WINDOWS.md. Une tâche préparée n'est pas déjà en cours. Si les fichiers ou l'environnement sont absents, signaler BLOCKED sans reconstruire des résultats fictifs.
