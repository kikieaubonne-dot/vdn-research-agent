# Caméra immersive

État : BLOCKED ; candidat, pas de technique validée.

## Objectif
Préparer une caméra première personne sans clipping et avec une référence de mouvement reproductible.

## Contexte
Le Voisin de Noël [Horreur]

## Solution proposée
séparation du suivi, du mouvement et de l’obstruction

## Pourquoi
Comparaison isolée proposée à partir du problème du jeu ; aucune méthode optimale établie.

## Prérequis
- camera-prototype : UNKNOWN; provide or attest through a task-bound experiment

## Implémentation
- FirstPersonCameraHarness — Consigner état caméra et contrôleur ; désactiver les effets candidats dans la copie témoin, pas dans le jeu principal. Attendu : Reproduction du problème avec contrôles connus.
- FirstPersonCameraHarness — Séparer cible de suivi, contribution du mouvement et gestion d’obstruction ; tracer chaque contribution sans valeur de lissage inventée. Attendu : Origine de clipping ou mouvement parasite identifiée.
- FirstPersonCameraHarness — Comparer arrêt, virage, sprint et accroupissement ; vérifier retour de contrôle et confort humain. Attendu : Aucune traversée de décor et aucun état caméra bloqué dans le scénario de test.

## Sources
- https://create.roblox.com/docs/workspace/camera — unknown

## Compatibilité, confiance et lacunes
{"compatibility": {"target_blender": "5.2", "target_engine": "Roblox", "verified": false}, "confidence": {"scope": "secondary published preparation record; sources not revalidated in this clone", "states": ["ENGINEERING_PROPOSAL"], "truth_verified": false}, "issues": ["correct_but_off_topic", "software_version_unknown", "blender_version_unverified_or_incompatible", "rejected_claim_not_a_fact", "archived_sources_require_local_revalidation"]}

## Paramètres documentés
[]

## Alternatives
[{"decision": "à comparer, pas de gagnant présumé", "method": "suivi témoin"}, {"decision": "à comparer, pas de gagnant présumé", "method": "effet de mouvement candidat isolé"}]

## Test proposé
{"changed_variable": "un seul facteur identifié avant exécution", "controls": ["mêmes assets, versions, appareil, caméra et trajet hors variable étudiée"], "executed": false, "measures": ["observations brutes et coût mesuré", "captures si disponibles"], "success_criteria": ["critères et seuils à valider avant exécution", "aucune régression du comportement témoin"]}

## Risques
- compatibilité moteur et versions non présumée
- coût de rendu/physique à mesurer sur appareil cible

## Rollback
Restaurer les copies et paramètres témoins ; conserver les preuves et ne pas modifier le jeu publié.

## Prochaine action
Quel personnage est jouable dans la première version ?

Clé de fiche : `f9e459c52dfcddb92c5995a1e560ae60fe4aac2c61d7e54a7ef74c98983474a9` ; analyse : `1adf78dc0cfb1d50ec5b7fb021519214c822a42994f438a496252f0293ebfe47`.
