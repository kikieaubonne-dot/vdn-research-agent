# Collisions des arbres

État : PARTIAL ; candidat, pas de technique validée.

## Objectif
Réduire les blocages du contrôleur près des troncs et branches dans une scène témoin.

## Contexte
Le Voisin de Noël [Horreur]

## Solution proposée
comparaison du collider actuel et d’une variante simplifiée

## Pourquoi
Comparaison isolée proposée à partir du problème du jeu ; aucune méthode optimale établie.

## Prérequis
- B3 : UNKNOWN; provide or attest through a task-bound experiment
- C1 : UNKNOWN; provide or attest through a task-bound experiment

## Implémentation
- TreeCollisionHarness — Inventorier séparément troncs, branches, géométrie visible et volumes physiques ; relever uniquement les propriétés sourcées. Attendu : État témoin enregistré pour restauration.
- TreeCollisionHarness — Exécuter le trajet témoin et journaliser chaque blocage avec position, action et composant touché. Attendu : Liste reproductible des blocages.
- TreeCollisionHarness — Changer uniquement la représentation physique autorisée par les sources ; rejouer le même contrôleur et parcours. Attendu : Comparaison des blocages et du coût physique ; rollback si régression.

## Sources
- https://create.roblox.com/docs/workspace/collisions — unknown

## Compatibilité, confiance et lacunes
{"compatibility": {"target_blender": "5.2", "target_engine": "Roblox", "verified": false}, "confidence": {"scope": "secondary published preparation record; sources not revalidated in this clone", "states": ["ENGINEERING_PROPOSAL"], "truth_verified": false}, "issues": ["software_version_unknown", "archived_sources_require_local_revalidation"]}

## Paramètres documentés
[{"claim_id": "claim-f7801f0539ed59047bc7c6eb", "documented_value": null, "kind": "literal_source_token", "name": "CollisionFidelity", "optimal_value": null, "passage_ids": ["pass-69d881e72b912bf71c810aae"], "project_applicability": "unverified"}]

## Alternatives
[{"decision": "à comparer, pas de gagnant présumé", "method": "collider du mesh"}, {"decision": "à comparer, pas de gagnant présumé", "method": "volumes physiques séparés, à valider"}]

## Test proposé
{"changed_variable": "un seul facteur identifié avant exécution", "controls": ["mêmes assets, versions, appareil, caméra et trajet hors variable étudiée"], "executed": false, "measures": ["observations brutes et coût mesuré", "captures si disponibles"], "success_criteria": ["critères et seuils à valider avant exécution", "aucune régression du comportement témoin"]}

## Risques
- compatibilité moteur et versions non présumée
- coût de rendu/physique à mesurer sur appareil cible

## Rollback
Restaurer les copies et paramètres témoins ; conserver les preuves et ne pas modifier le jeu publié.

## Prochaine action
Préparer les entrées puis exécuter le protocole isolé ; revue humaine requise.

Clé de fiche : `a1e0d1ed3fe4b490300c43551f3321406babdecf55c18427f5932cff424f9a22` ; analyse : `98934c02b53a289ef6b1c7a7fa93cee05c3c406ceab98aeaa85120a675845f81`.
