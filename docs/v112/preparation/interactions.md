# Interactions, portes et cachettes

État : BLOCKED ; candidat, pas de technique validée.

## Objectif
Préparer une interaction de porte et cachette vérifiable sans décider le scénario.

## Contexte
Le Voisin de Noël [Horreur]

## Solution proposée
contrat d’interaction avec validation de l’état

## Pourquoi
Comparaison isolée proposée à partir du problème du jeu ; aucune méthode optimale établie.

## Prérequis
- interaction-prototype : UNKNOWN; provide or attest through a task-bound experiment

## Implémentation
- InteractionDoorHarness — Définir action, portée autorisée, préconditions et état avant/après ; les valeurs restent à choisir à partir des sources et tests. Attendu : Contrat d’interaction et erreurs explicites.
- InteractionDoorHarness — Séparer présentation, requête et décision ; rejeter les demandes répétées ou incompatibles avec l’état courant. Attendu : Aucun double déclenchement ni changement d’état impossible.
- InteractionDoorHarness — Tester annulation, obstacle, entrée déjà occupée et reconnexion si le mode retenu le requiert. Attendu : Résultats et limites réseau consignés avant réutilisation.

## Sources
- https://create.roblox.com/docs/ui/proximity-prompts — unknown

## Compatibilité, confiance et lacunes
{"compatibility": {"target_blender": "5.2", "target_engine": "Roblox", "verified": false}, "confidence": {"scope": "secondary published preparation record; sources not revalidated in this clone", "states": ["ENGINEERING_PROPOSAL"], "truth_verified": false}, "issues": ["correct_but_off_topic", "software_version_unknown", "archived_sources_require_local_revalidation"]}

## Paramètres documentés
[]

## Alternatives
[{"decision": "à comparer, pas de gagnant présumé", "method": "interaction minimale"}, {"decision": "à comparer, pas de gagnant présumé", "method": "variante de cachette conditionnée au scénario"}]

## Test proposé
{"changed_variable": "un seul facteur identifié avant exécution", "controls": ["mêmes assets, versions, appareil, caméra et trajet hors variable étudiée"], "executed": false, "measures": ["observations brutes et coût mesuré", "captures si disponibles"], "success_criteria": ["critères et seuils à valider avant exécution", "aucune régression du comportement témoin"]}

## Risques
- compatibilité moteur et versions non présumée
- coût de rendu/physique à mesurer sur appareil cible

## Rollback
Restaurer les copies et paramètres témoins ; conserver les preuves et ne pas modifier le jeu publié.

## Prochaine action
La première version est-elle solo ou coopérative ?

Clé de fiche : `130b480353d9811c3c21dbf03c45cad06fe5215cbe22fd187e258b7d10e2cf19` ; analyse : `ebb540b27978d7111cda912942c97315be111dcc19c37cd0bee7751508b7f2c3`.
