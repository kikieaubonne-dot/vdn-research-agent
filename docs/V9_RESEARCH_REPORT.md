# Recherches V9 réellement effectuées

**5 pages officielles lues**, plus `robots.txt`, soit **6 requêtes HTTP**.
Accès autorisé par le parseur robots lors de la lecture ; aucun contournement,
aucun téléchargement massif, aucun fournisseur payant. Les limites de la session
ont été appliquées avec `agent.budget` et le transport existant.

| Candidate | Source principale et complément |
|---|---|
| Sauvegardes — `vdn-ac07d1c0fed7` | [Data stores](https://create.roblox.com/docs/cloud-services/data-stores), [DataStore API](https://create.roblox.com/docs/reference/engine/classes/DataStore) |
| Sécurité — `vdn-588169c7b940` | [Securing the client-server boundary](https://create.roblox.com/docs/scripting/security/client-server-boundary) |
| Poursuite/navigation — `vdn-939f03f673d6` | [Pathfinding](https://create.roblox.com/docs/characters/pathfinding) |
| Accessoires — `vdn-4782fa1e3cf5` | [Rigid accessories](https://create.roblox.com/docs/avatar/rigid-accessories) |

Les caches bruts de lecture restent locaux et ne sont pas publiés intégralement.
Les fiches conservent URLs, dates de source disponibles, date de collecte et SHA-256.
`v9/research_access.json` conserve la provenance ; `v9/citation_checks.json`
contrôle cinq courtes citations exactes, chacune de 24 mots au plus.

Les procédures françaises sont **éditoriales, candidates et non reproduites**.
Les hypothèses de conception, dont la machine à états de poursuite, sont signalées
comme propositions plutôt qu'attribuées à une preuve de fonctionnement. Les
paramètres documentés ne sont pas des réglages universels recommandés.

Le générateur utilise les sources enregistrées pour publier sans modifier les
fiches connues. Le collecteur ponctuel complet est testé sur fixtures : budgets
HTTP/temps, compteurs journaliers du clone, robots, cache, tentatives, arrêt sur
erreur et stagnation. Il n'a pas été activé comme tâche récurrente. Les autres
familles de sources citées dans la mission restent à évaluer selon les besoins ;
aucune vidéo n'a été présentée comme inspectée.
