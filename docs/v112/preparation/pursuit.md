# Poursuite et détection

État : BLOCKED ; candidat, pas de technique validée.

## Objectif
Comparer détection et suivi du joueur sur un parcours témoin, sans inventer le personnage antagoniste.

## Contexte
Le Voisin de Noël [Horreur]

## Solution proposée
séparation détection, décision et déplacement

## Pourquoi
Comparaison isolée proposée à partir du problème du jeu ; aucune méthode optimale établie.

## Prérequis
- npc-lab : UNKNOWN; provide or attest through a task-bound experiment

## Implémentation
- PursuitDetectionHarness — Définir observations visibles, états de détection et sorties ; ne pas attribuer le rôle au Père Noël sans décision. Attendu : Table de transitions et conditions de perte de cible.
- PursuitDetectionHarness — Journaliser observation, décision et demande de déplacement ; tester les obstacles sans supposer une visibilité traversante. Attendu : Erreur localisée entre détection et navigation.
- PursuitDetectionHarness — Comparer apparition, perte de vue, chemin indisponible et cible immobile ; conserver les échecs et conditions. Attendu : Poursuite bornée et sortie d’état sûre, sans résultat inventé.

## Sources
- https://create.roblox.com/docs/workspace/raycasting — unknown

## Compatibilité, confiance et lacunes
{"compatibility": {"target_blender": "5.2", "target_engine": "Roblox", "verified": false}, "confidence": {"scope": "secondary published preparation record; sources not revalidated in this clone", "states": ["ENGINEERING_PROPOSAL"], "truth_verified": false}, "issues": ["correct_but_off_topic", "software_version_unknown", "archived_sources_require_local_revalidation"]}

## Paramètres documentés
[]

## Alternatives
[{"decision": "à comparer, pas de gagnant présumé", "method": "détection témoin"}, {"decision": "à comparer, pas de gagnant présumé", "method": "navigation candidate sourcée"}]

## Test proposé
{"changed_variable": "un seul facteur identifié avant exécution", "controls": ["mêmes assets, versions, appareil, caméra et trajet hors variable étudiée"], "executed": false, "measures": ["observations brutes et coût mesuré", "captures si disponibles"], "success_criteria": ["critères et seuils à valider avant exécution", "aucune régression du comportement témoin"]}

## Risques
- compatibilité moteur et versions non présumée
- coût de rendu/physique à mesurer sur appareil cible

## Rollback
Restaurer les copies et paramètres témoins ; conserver les preuves et ne pas modifier le jeu publié.

## Prochaine action
La première version est-elle solo ou coopérative ?

Clé de fiche : `ecaed9bb3accf05f43dbac5f6f59cae32cb62ea52dedceb1c19cce35086f560f` ; analyse : `571e68bd0f5e50f688d0aa466eb97f6480cea8ea597eb84f7ec7259c68c5e824`.
