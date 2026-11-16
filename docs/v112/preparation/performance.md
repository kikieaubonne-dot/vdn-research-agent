# Optimisation PC et mobile

État : BLOCKED ; candidat, pas de technique validée.

## Objectif
Établir un baseline et isoler géométrie, densité et rendu sur les appareils retenus.

## Contexte
Le Voisin de Noël [Horreur]

## Solution proposée
baseline par appareil et modification d’un facteur

## Pourquoi
Comparaison isolée proposée à partir du problème du jeu ; aucune méthode optimale établie.

## Prérequis
- forest-lab : UNKNOWN; provide or attest through a task-bound experiment

## Implémentation
- ForestProfileHarness — Consigner géométrie, matériaux, instances, résolution et trajet ; les objectifs de FPS restent inconnus tant que non validés. Attendu : Rapport de baseline avec conditions.
- ForestProfileHarness — Mesurer les segments coûteux avec les outils officiellement documentés ; séparer rendu, physique et logique. Attendu : Coût attribué à un segment et non à un FPS supposé.
- ForestProfileHarness — Comparer densité, géométrie ou gestion de distance séparément ; garder les mesures brutes et les défauts visuels. Attendu : Décision conditionnelle par appareil, pas de gain général inventé.

## Sources
Aucune source originale suffisamment attribuée ; recherche partielle.

## Compatibilité, confiance et lacunes
{"compatibility": {"target_blender": "5.2", "target_engine": "Roblox", "verified": false}, "confidence": {"scope": "secondary published preparation record; sources not revalidated in this clone", "states": ["ENGINEERING_PROPOSAL"], "truth_verified": false}, "issues": ["software_version_unknown", "no_sufficient_original_source", "archived_sources_require_local_revalidation"]}

## Paramètres documentés
[]

## Alternatives
[{"decision": "à comparer, pas de gagnant présumé", "method": "baseline"}, {"decision": "à comparer, pas de gagnant présumé", "method": "une optimisation documentée à la fois"}]

## Test proposé
{"changed_variable": "un seul facteur identifié avant exécution", "controls": ["mêmes assets, versions, appareil, caméra et trajet hors variable étudiée"], "executed": false, "measures": ["observations brutes et coût mesuré", "captures si disponibles"], "success_criteria": ["critères et seuils à valider avant exécution", "aucune régression du comportement témoin"]}

## Risques
- compatibilité moteur et versions non présumée
- coût de rendu/physique à mesurer sur appareil cible

## Rollback
Restaurer les copies et paramètres témoins ; conserver les preuves et ne pas modifier le jeu publié.

## Prochaine action
Quels appareils et budgets de performance doivent être validés pour la bêta ?

Clé de fiche : `e05273553c18a9966d51bc8cb349914c23d85deb3390a91af310fc0f8ff48fa9` ; analyse : `9df3584c4df2039a819b5fdc99a603bc2d93782683f44a980bf2e2997007f736`.
