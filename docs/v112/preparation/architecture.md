# Manoir et maison

État : BLOCKED ; candidat, pas de technique validée.

## Objectif
Préparer un blockout lisible du manoir et de la maison, conditionné à la séquence bêta.

## Contexte
Le Voisin de Noël [Horreur]

## Solution proposée
blockout conditionné à la séquence jouable

## Pourquoi
Comparaison isolée proposée à partir du problème du jeu ; aucune méthode optimale établie.

## Prérequis
- manor-blockout : UNKNOWN; provide or attest through a task-bound experiment

## Implémentation
- HouseBlockoutHarness — Marquer entrée, sortie, visibilité et espaces nécessaires à la séquence ; laisser les choix narratifs non confirmés visibles. Attendu : Plan de circulation et inconnues explicites.
- HouseBlockoutHarness — Parcourir le blockout avec le contrôleur témoin avant détails ; mesurer encombrement et blocages. Attendu : Circulation et lignes de vue annotées.
- HouseBlockoutHarness — Comparer variantes de parcours ; ne figer une pièce scénarisée qu’après décision humaine. Attendu : Blockout réversible avec décision et alternatives consignées.

## Sources
- https://create.roblox.com/docs/art/modeling/assign-textures — unknown
- https://create.roblox.com/docs/workspace/collisions — unknown

## Compatibilité, confiance et lacunes
{"compatibility": {"target_blender": "5.2", "target_engine": "Roblox", "verified": false}, "confidence": {"scope": "secondary published preparation record; sources not revalidated in this clone", "states": ["ENGINEERING_PROPOSAL"], "truth_verified": false}, "issues": ["software_version_unknown", "archived_sources_require_local_revalidation"]}

## Paramètres documentés
[]

## Alternatives
[{"decision": "à comparer, pas de gagnant présumé", "method": "blockout minimal"}, {"decision": "à comparer, pas de gagnant présumé", "method": "détails artistiques différés"}]

## Test proposé
{"changed_variable": "un seul facteur identifié avant exécution", "controls": ["mêmes assets, versions, appareil, caméra et trajet hors variable étudiée"], "executed": false, "measures": ["observations brutes et coût mesuré", "captures si disponibles"], "success_criteria": ["critères et seuils à valider avant exécution", "aucune régression du comportement témoin"]}

## Risques
- compatibilité moteur et versions non présumée
- coût de rendu/physique à mesurer sur appareil cible

## Rollback
Restaurer les copies et paramètres témoins ; conserver les preuves et ne pas modifier le jeu publié.

## Prochaine action
Quelle séquence jouable doit être terminée pour la bêta ?

Clé de fiche : `1f5c4dae0acbd8026761cabde86ce86e5755884e40a6ef9fbdf649c4ca2ace97` ; analyse : `99686011a5b8449c18addfd0e3652e5c4460d385575cab98884b68fefcbb987c`.
