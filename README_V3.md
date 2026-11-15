# VDN Research Agent V3 — installation et limites

## Installation sur le dépôt existant

Copier les fichiers du ZIP **dans le dossier cloné `vdn-research-agent`**, en conservant l’arborescence, puis Commit et Push avec GitHub Desktop. Ne pas supprimer `knowledge/` ni `output/` existants. La V3 est compatible avec les fiches V1/V2 et conserve les recherches.

## Fonctionnement

Chaque heure (horaire indicatif, GitHub peut retarder ou ignorer des exécutions), GitHub Actions collecte jusqu’à 8 requêtes sur DevForum et GitHub, puis examine au maximum 12 fiches anciennes ou nouvelles réparties entre les sujets. Il essaie de lire jusqu’à cinq messages DevForum ou un README de dépôt GitHub. Il cherche des passages contenant à la fois un sujet technique et un détail exploitable. Les passages sont **candidats, non vérifiés**.

Si aucun passage utile n’est trouvé, la fiche n’est pas déclarée enrichie. Les questions complémentaires sont sauvegardées dans `output/v3_state.json` et résumées dans `output/v3_report.md` ; elles alimentent également les prochaines requêtes de recherche, sous réserve des limites de session. Le rapport est compatible Markdown/Obsidian. Les fiches de connaissances sont dans `knowledge/`.

## Contrôle

Dans Actions → VDN Research Agent → Run workflow, examiner l’étape `Analyze evidence and create followup questions` et les compteurs `evidence_extracted`, `insufficient`, `errors`. Une exécution verte n’est pas une validation scientifique. Pour synchroniser Obsidian, faire Fetch/Pull dans GitHub Desktop puis ouvrir le dossier `knowledge` comme coffre ou l’intégrer à un coffre existant.

## Contraintes

Aucune IA distante ni modèle de langage n’est inclus. Les questions sont générées par règles ; les pages peuvent être inaccessibles, incomplètes, ou non pertinentes. Pas d’expériences Roblox automatiques, pas de compréhension complète des vidéos YouTube, pas de recherche exhaustive, pas d’accès illimité aux API. L’usage gratuit de GitHub Actions est soumis aux quotas et politiques GitHub. Les sources sont des données non fiables ; aucune commande provenant d’une page n’est exécutée.
