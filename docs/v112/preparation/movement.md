# Déplacement et transitions

État : BLOCKED ; candidat, pas de technique validée.

## Objectif
Définir et tester les transitions entre marche, sprint, accroupissement, glissade et enjambement.

## Contexte
Le Voisin de Noël [Horreur]

## Solution proposée
machine d’états explicite et validation des transitions

## Pourquoi
Comparaison isolée proposée à partir du problème du jeu ; aucune méthode optimale établie.

## Prérequis
- player-controller : UNKNOWN; provide or attest through a task-bound experiment

## Implémentation
- MovementStateHarness — Écrire une table état/entrée/condition de sortie pour marche, sprint, accroupissement, glissade et enjambement ; marquer les actions non validées. Attendu : Transitions et exclusions inspectables avant programmation.
- MovementStateHarness — Séparer détection, autorisation de transition et mouvement ; journaliser les refus au lieu de forcer un franchissement. Attendu : Reproduction des collisions et transitions impossibles.
- MovementStateHarness — Tester interruption, changement de direction, plafond bas et perte de contrôle ; consigner chaque retour à l’état sûr. Attendu : Aucun état coincé ; comportement validé seulement sur les contrôles testés.

## Sources
- https://create.roblox.com/docs/workspace/raycasting — unknown

## Compatibilité, confiance et lacunes
{"compatibility": {"target_blender": "5.2", "target_engine": "Roblox", "verified": false}, "confidence": {"scope": "secondary published preparation record; sources not revalidated in this clone", "states": ["ENGINEERING_PROPOSAL"], "truth_verified": false}, "issues": ["correct_but_off_topic", "software_version_unknown", "archived_sources_require_local_revalidation"]}

## Paramètres documentés
[]

## Alternatives
[{"decision": "à comparer, pas de gagnant présumé", "method": "locomotion témoin"}, {"decision": "à comparer, pas de gagnant présumé", "method": "actions avancées activées séparément"}]

## Test proposé
{"changed_variable": "un seul facteur identifié avant exécution", "controls": ["mêmes assets, versions, appareil, caméra et trajet hors variable étudiée"], "executed": false, "measures": ["observations brutes et coût mesuré", "captures si disponibles"], "success_criteria": ["critères et seuils à valider avant exécution", "aucune régression du comportement témoin"]}

## Risques
- compatibilité moteur et versions non présumée
- coût de rendu/physique à mesurer sur appareil cible

## Rollback
Restaurer les copies et paramètres témoins ; conserver les preuves et ne pas modifier le jeu publié.

## Prochaine action
Quel personnage est jouable dans la première version ?

Clé de fiche : `ba94f8c17e928389556f451377efce0c25adf30b2a254f5c3d511a884c8e0950` ; analyse : `98f07a5ba30d19a2e3708b39db2ac49e7afe5f4fdfdcec8027c6fa1aeff0aba1`.
