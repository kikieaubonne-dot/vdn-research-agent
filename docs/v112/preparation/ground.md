# Sol, relief et empreintes

État : PARTIAL ; candidat, pas de technique validée.

## Objectif
Comparer le sol enneigé et les empreintes sur un même relief et trajet.

## Contexte
Le Voisin de Noël [Horreur]

## Solution proposée
comparaison de deux représentations de sol et d’empreintes

## Pourquoi
Comparaison isolée proposée à partir du problème du jeu ; aucune méthode optimale établie.

## Prérequis
- snow-ground : UNKNOWN; provide or attest through a task-bound experiment

## Implémentation
- SnowGroundHarness — Consigner relief, matériau et trajectoire ; capturer les contacts du joueur avant toute empreinte. Attendu : Baseline de déplacement et de raccords.
- SnowGroundHarness — Ajouter la représentation d’empreintes candidate dans une copie ; conserver un sol témoin. Attendu : Effet isolé, durée et nettoyage observables.
- SnowGroundHarness — Rejouer arrêts, virages et passages répétés ; relever flottement, intersections, persistance et coût. Attendu : Défauts annotés et mesures, sans durée optimale inventée.

## Sources
- https://create.roblox.com/docs/parts/terrain — unknown
- https://create.roblox.com/docs/art/modeling/surface-appearance — unknown

## Compatibilité, confiance et lacunes
{"compatibility": {"target_blender": "5.2", "target_engine": "Roblox", "verified": false}, "confidence": {"scope": "secondary published preparation record; sources not revalidated in this clone", "states": ["ENGINEERING_PROPOSAL"], "truth_verified": false}, "issues": ["software_version_unknown", "archived_sources_require_local_revalidation"]}

## Paramètres documentés
[]

## Alternatives
[{"decision": "à comparer, pas de gagnant présumé", "method": "terrain"}, {"decision": "à comparer, pas de gagnant présumé", "method": "surface mesh et effet d’empreinte documenté"}]

## Test proposé
{"changed_variable": "un seul facteur identifié avant exécution", "controls": ["mêmes assets, versions, appareil, caméra et trajet hors variable étudiée"], "executed": false, "measures": ["observations brutes et coût mesuré", "captures si disponibles"], "success_criteria": ["critères et seuils à valider avant exécution", "aucune régression du comportement témoin"]}

## Risques
- compatibilité moteur et versions non présumée
- coût de rendu/physique à mesurer sur appareil cible

## Rollback
Restaurer les copies et paramètres témoins ; conserver les preuves et ne pas modifier le jeu publié.

## Prochaine action
Préparer les entrées puis exécuter le protocole isolé ; revue humaine requise.

Clé de fiche : `674022316a32056e910e350f4baeafbe8f4c2f0dbef0bbbf1f170e4f0537d32c` ; analyse : `cd7cf55bdf8f011a79b0e36a67daaf7cb35943cdfe60e49b52b4f27057accb2c`.
