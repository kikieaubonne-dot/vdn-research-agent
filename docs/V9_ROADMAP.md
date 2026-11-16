# Après V9 — sans lancer V10

| Priorité | Étape | Impact | Effort / risque |
|---|---|---|---|
| P0 production | tester sauvegardes, collisions et frontière serveur dans un lieu isolé | évite perte de progression et blocages | moyen, nécessite Studio et critères d'arrêt |
| P1 production | reproduire poursuite parmi obstacles et limites serveur | gameplay principal jouable | moyen/élevé, perception et états encore candidats |
| P0 intégration | exécuter sync et rollback dans un coffre Windows de test réel | vérifier le workflow quotidien | faible/moyen, sauvegarde et autorisation du chemin |
| P1 logiciel | revue humaine distincte, versions et preuves inspectables | permet une promotion légitime des connaissances | moyen, ne pas confondre rapports et preuves |
| P2 logiciel | révisions append-only des sources déjà connues et cache expirant | réévaluation sans écraser les notes | moyen, migration d'identités/relations à tester |
| P2 logiciel | enrichir holdout indépendant, ambiguïtés et contradictions | limite les faux candidats et mesure l'abstention | moyen, labels externes nécessaires |
| P2 logiciel | diminuer rescans et mesurer à 1 000 notes | réactivité MCP | moyen, ne pas perdre détection des changements |
| P3 production | améliorer forêt/personnages après gameplay stable | finition visuelle | élevé, ne pas retarder la sortie |
| P4 production | casier, bonnet, sacoche et boutique | extension future | reportable, multijoueur non validé |

## V9.1 conditionnelle

Après essais Windows/Obsidian : étudier la récurrence explicitement autorisée,
les recherches contradictoires et la revue des expériences. Réutiliser le
scheduler existant avant d'en ajouter un. Plusieurs clones ne partagent pas un
verrou distribué : mesurer les quotas et conflits réels avant activation.

## V10 : uniquement une proposition

Prévoir ensuite un pont contrôlé Blender/Roblox : scripts relisibles, autorisation
d'exécution, scènes de test, mesures de performance et retour arrière. Aucun de
ces connecteurs, auto-déploiements, auto-modifications ou orchestrateurs graphiques
n'est implémenté ou lancé dans V9.

## Futur essai avec/sans Éponge

Comparer sur trois tâches figées (sauvegarde, poursuite, accessoire) : temps jusqu'à
un résultat reproductible, erreurs, sources utilisées, corrections et budget.
Même scène/version, critères de validation établis avant essai et revue humaine.
**Aucun résultat de productivité Claude n'est inventé pendant son indisponibilité.**
