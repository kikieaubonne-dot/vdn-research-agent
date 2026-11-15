# VDN — Rapport méta-recherche (V5)

Récompense = 0,6 × part de résultats nouveaux utiles + 0,4 × contenu technique − 0,2 × hors sujet (0 si erreur). Elle mesure l'UTILITÉ APPARENTE des requêtes, pas la véracité ni la validation dans Roblox.

| Source:sujet | Stratégie | Essais | Retournés | Acceptés | Nouveaux | Hors sujet | Doublons | Erreurs | Vides | Récompense moy. |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| devforum:forest | synonyms | 1 | 4 | 0 | 0 | 4 | 0 | 0 | 0 | 0.000 |
| devforum:forest | terms | 1 | 4 | 1 | 1 | 3 | 0 | 0 | 0 | 0.120 |
| devforum:lighting | synonyms | 1 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0.000 |
| devforum:lighting | terms | 1 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0.000 |
| devforum:snow | synonyms | 1 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0.000 |
| devforum:snow | terms | 1 | 4 | 1 | 1 | 3 | 0 | 0 | 0 | 0.196 |
| devforum:spruce | synonyms | 1 | 3 | 0 | 0 | 3 | 0 | 0 | 0 | 0.000 |
| devforum:spruce | terms | 1 | 4 | 0 | 0 | 4 | 0 | 0 | 0 | 0.000 |
| github:forest | synonyms | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0.000 |
| github:forest | terms | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0.000 |
| github:lighting | synonyms | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0.000 |
| github:lighting | terms | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0.000 |
| github:snow | synonyms | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0.000 |
| github:snow | terms | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0.000 |
| github:spruce | synonyms | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0.000 |
| github:spruce | terms | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0.000 |
| roblox_docs:forest | synonyms | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0.000 |
| roblox_docs:forest | terms | 1 | 4 | 3 | 3 | 1 | 0 | 0 | 0 | 0.800 |
| roblox_docs:lighting | synonyms | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0.000 |
| roblox_docs:lighting | terms | 1 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0.000 |
| roblox_docs:snow | synonyms | 1 | 3 | 0 | 0 | 1 | 0 | 0 | 0 | 0.333 |
| roblox_docs:snow | terms | 1 | 4 | 4 | 4 | 0 | 0 | 0 | 0 | 0.988 |
| roblox_docs:spruce | synonyms | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0.000 |
| roblox_docs:spruce | terms | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 1.000 |

_22 anciennes stratégies V4 (baseline/focused/site_specific) conservées dans l'état, non utilisées : elles étaient évaluées avec un calcul de pertinence défectueux (titre seul)._

## Dernière exécution

- Requêtes logiques : 8 (chacune envoyée à chaque fournisseur actif : 24 essais au total)
- Résultats renvoyés : 50 · lus : 30 · acceptés : 10
- Fiches créées : 10 · mises à jour : 0 · rejetées : 20
- Erreurs : 0

### Raisons de rejet les plus fréquentes

- 18 × hors sujet
- 11 × pas assez de contenu technique

## Sécurité et limites

- Aucune modification automatique de code ; aucune exécution de code venant du web.
- Le contenu des sources est une donnée, jamais une instruction.
- Retour arrière : supprimer output/meta_state.json remet toutes les stratégies à zéro.
