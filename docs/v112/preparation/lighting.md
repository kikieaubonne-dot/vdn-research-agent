# Nuit et lampe torche

État : PARTIAL ; candidat, pas de technique validée.

## Objectif
Isoler les défauts de lisibilité nocturne et de faisceau de la lampe V2.

## Contexte
Le Voisin de Noël [Horreur]

## Solution proposée
isolation du faisceau et de l’ambiance nocturne

## Pourquoi
Comparaison isolée proposée à partir du problème du jeu ; aucune méthode optimale établie.

## Prérequis
- flashlight-v2 : UNKNOWN; provide or attest through a task-bound experiment

## Implémentation
- FlashlightNightHarness — Consigner propriétés réellement disponibles et valeurs actuelles ; fixer caméra, exposition et appareil. Attendu : Baseline restaurable et versions enregistrées.
- FlashlightNightHarness — Changer un seul facteur documenté de lumière, ombre ou brouillard ; conserver le reste. Attendu : Cause isolée des différences de lisibilité.
- FlashlightNightHarness — Capturer bord du faisceau, contact avec le sol, branches et silhouettes ; joindre coût de trame et avis humain. Attendu : Compromis visibilité/ambiance mesuré, aucune portée optimale présumée.

## Sources
- https://create.roblox.com/docs/effects/light-sources — unknown

## Compatibilité, confiance et lacunes
{"compatibility": {"target_blender": "5.2", "target_engine": "Roblox", "verified": false}, "confidence": {"scope": "secondary published preparation record; sources not revalidated in this clone", "states": ["ENGINEERING_PROPOSAL"], "truth_verified": false}, "issues": ["software_version_unknown", "archived_sources_require_local_revalidation"]}

## Paramètres documentés
[{"claim_id": "claim-50b5533f98fef5b1f14e300b", "documented_value": null, "kind": "literal_source_token", "name": "SpotLight", "optimal_value": null, "passage_ids": ["pass-06fcd1bde5752118fee17e15"], "project_applicability": "unverified"}, {"claim_id": "claim-853856f44ace166a478ca0d4", "documented_value": null, "kind": "literal_source_token", "name": "SpotLight", "optimal_value": null, "passage_ids": ["pass-d848fa2456fd2cfb3b537d45"], "project_applicability": "unverified"}, {"claim_id": "claim-c487710c3cc49738f1288c1f", "documented_value": null, "kind": "literal_source_token", "name": "Shadows", "optimal_value": null, "passage_ids": ["pass-9a158d2705729bbc32f32d43"], "project_applicability": "unverified"}, {"claim_id": "claim-bbe00550480d8f1d6ae6f11c", "documented_value": null, "kind": "literal_source_token", "name": "Shadows", "optimal_value": null, "passage_ids": ["pass-d08471f9b91ae5efdeca4347"], "project_applicability": "unverified"}, {"claim_id": "claim-cfb84d723d9d3b63f90ab067", "documented_value": null, "kind": "literal_source_token", "name": "SpotLight", "optimal_value": null, "passage_ids": ["pass-30bff1940bd598913f75a67c"], "project_applicability": "unverified"}, {"claim_id": "claim-a358fa706552edb74982af78", "documented_value": null, "kind": "literal_source_token", "name": "SpotLight", "optimal_value": null, "passage_ids": ["pass-16a3a45759831c66ec0642ba"], "project_applicability": "unverified"}, {"claim_id": "claim-cdff9688d099551acade5518", "documented_value": null, "kind": "literal_source_token", "name": "SpotLight", "optimal_value": null, "passage_ids": ["pass-2cf9fbc55e49931b83356d0f"], "project_applicability": "unverified"}]

## Alternatives
[{"decision": "à comparer, pas de gagnant présumé", "method": "lumière témoin"}, {"decision": "à comparer, pas de gagnant présumé", "method": "variante d’ombre ou d’atmosphère documentée"}]

## Test proposé
{"changed_variable": "un seul facteur identifié avant exécution", "controls": ["mêmes assets, versions, appareil, caméra et trajet hors variable étudiée"], "executed": false, "measures": ["observations brutes et coût mesuré", "captures si disponibles"], "success_criteria": ["critères et seuils à valider avant exécution", "aucune régression du comportement témoin"]}

## Risques
- compatibilité moteur et versions non présumée
- coût de rendu/physique à mesurer sur appareil cible

## Rollback
Restaurer les copies et paramètres témoins ; conserver les preuves et ne pas modifier le jeu publié.

## Prochaine action
Préparer les entrées puis exécuter le protocole isolé ; revue humaine requise.

Clé de fiche : `6f0766082a177fd45e6ab13c90041f0f2bcb13b185354a62d610177bac5eeab0` ; analyse : `13dcf7ac38186fba3009ea281add22d11c60e68392539506cbd776aa08de7f8f`.
