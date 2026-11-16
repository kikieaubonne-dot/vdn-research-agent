# Sapins enneigés réalistes

État : PARTIAL ; candidat, pas de technique validée.

## Objectif
Comparer silhouette, géométrie et feuillage de copies B3/C1 sans supposer un gain visuel.

## Contexte
Le Voisin de Noël [Horreur]

## Solution proposée
comparaison silhouette/géométrie et feuillage

## Pourquoi
Comparaison isolée proposée à partir du problème du jeu ; aucune méthode optimale établie.

## Prérequis
- B3 : UNKNOWN; provide or attest through a task-bound experiment
- C1 : UNKNOWN; provide or attest through a task-bound experiment

## Implémentation
- TreeVariantsLab — Aligner les copies sur la même échelle ; capturer silhouette proche et lointaine. Attendu : Silhouettes annotées et dimensions consignées.
- TreeVariantsLab — Modifier un seul facteur : géométrie ou représentation du feuillage ; conserver matériaux, caméra et lumière. Attendu : Variantes A/B différant seulement par le facteur choisi.
- TreeVariantsLab — Comparer répétition, contours, ombres et coût mesuré ; conserver les défauts signalés par un humain. Attendu : Revue visuelle et mesures jointes, sans gagnant présumé.

## Sources
- https://create.roblox.com/docs/art/modeling/surface-appearance — unknown

## Compatibilité, confiance et lacunes
{"compatibility": {"target_blender": "5.2", "target_engine": "Roblox", "verified": false}, "confidence": {"scope": "secondary published preparation record; sources not revalidated in this clone", "states": ["ENGINEERING_PROPOSAL"], "truth_verified": false}, "issues": ["correct_but_off_topic", "software_version_unknown", "archived_sources_require_local_revalidation"]}

## Paramètres documentés
[{"claim_id": "claim-60c64c25d1865877862e9b76", "documented_value": null, "kind": "literal_source_token", "name": "SurfaceAppearance", "optimal_value": null, "passage_ids": ["pass-52d67a51e3db722468b01802"], "project_applicability": "unverified"}, {"claim_id": "claim-228448dc659cd483356945d5", "documented_value": null, "kind": "literal_source_token", "name": "RoughnessMap", "optimal_value": null, "passage_ids": ["pass-5fddff40277ca77f9f591334"], "project_applicability": "unverified"}, {"claim_id": "claim-228448dc659cd483356945d5", "documented_value": null, "kind": "literal_source_token", "name": "SurfaceAppearance", "optimal_value": null, "passage_ids": ["pass-5fddff40277ca77f9f591334"], "project_applicability": "unverified"}, {"claim_id": "claim-04d06ec97c8bc0bcfd9cc1b7", "documented_value": null, "kind": "literal_source_token", "name": "ColorMap", "optimal_value": null, "passage_ids": ["pass-f55a682f6067ced48bd22b7e"], "project_applicability": "unverified"}, {"claim_id": "claim-04d06ec97c8bc0bcfd9cc1b7", "documented_value": null, "kind": "literal_source_token", "name": "SurfaceAppearance", "optimal_value": null, "passage_ids": ["pass-f55a682f6067ced48bd22b7e"], "project_applicability": "unverified"}, {"claim_id": "claim-9d5e6af30b1244f07a6f4af6", "documented_value": null, "kind": "literal_source_token", "name": "NormalMap", "optimal_value": null, "passage_ids": ["pass-61230ca3e993f0c3c2e763f5"], "project_applicability": "unverified"}, {"claim_id": "claim-9d5e6af30b1244f07a6f4af6", "documented_value": null, "kind": "literal_source_token", "name": "SurfaceAppearance", "optimal_value": null, "passage_ids": ["pass-61230ca3e993f0c3c2e763f5"], "project_applicability": "unverified"}, {"claim_id": "claim-2d9ddf3b9da9035b1c5eae8a", "documented_value": null, "kind": "literal_source_token", "name": "ColorMap", "optimal_value": null, "passage_ids": ["pass-c76f012ffa7a5245219a0528"], "project_applicability": "unverified"}, {"claim_id": "claim-2d9ddf3b9da9035b1c5eae8a", "documented_value": null, "kind": "literal_source_token", "name": "SurfaceAppearance", "optimal_value": null, "passage_ids": ["pass-c76f012ffa7a5245219a0528"], "project_applicability": "unverified"}]

## Alternatives
[{"decision": "à comparer, pas de gagnant présumé", "method": "géométrie"}, {"decision": "à comparer, pas de gagnant présumé", "method": "cartes de feuillage"}]

## Test proposé
{"changed_variable": "un seul facteur identifié avant exécution", "controls": ["mêmes assets, versions, appareil, caméra et trajet hors variable étudiée"], "executed": false, "measures": ["observations brutes et coût mesuré", "captures si disponibles"], "success_criteria": ["critères et seuils à valider avant exécution", "aucune régression du comportement témoin"]}

## Risques
- compatibilité moteur et versions non présumée
- coût de rendu/physique à mesurer sur appareil cible

## Rollback
Restaurer les copies et paramètres témoins ; conserver les preuves et ne pas modifier le jeu publié.

## Prochaine action
Préparer les entrées puis exécuter le protocole isolé ; revue humaine requise.

Clé de fiche : `6fe4dd8189e285d666da32f7c41c4d1fb27b68eab4c86e229e4bd35a86baa1d8` ; analyse : `c8ac4d3784256df334b8405f64ac50bf9a2927c5a8d3ed257015da6600ee730a`.
