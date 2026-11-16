# Évaluation V10/V11

Protocole reproductible :

```powershell
& $python -m bench.evaluate_ocean --output work\ocean-benchmark.json
```

[Mesures JSON](benchmark.json) : même copie de **111 Markdown** pour les deux
façades, dont 110 historiques inchangés et la candidate collisions issue de la
collecte réelle. V10 utilise la recherche existante ; V11 ajoute concepts et
briefing. Huit questions de développement : problème utilisateur, synonyme,
termes techniques, anglais, versions, FPS B3 inconnu et deux domaines étrangers.
La référence choisie pour les cinq premières est **cette candidate précise**,
pas une annotation exhaustive de toutes les fiches pertinentes.

| Mesure | V10 | V11 |
|---|---:|---:|
| Cible retrouvée dans les trois premiers (5 cas) | 0,4 | 1,0 |
| Rang réciproque moyen de cette cible | 0,4 | 1,0 |
| Abstention briefing sur les 3 cas hors preuve | non comparée | 3/3 |
| Modèle / HTTP / coût API dans ce bench | 0 / 0 / 0 | 0 / 0 / 0 |

Les alias ont été conçus pour ce domaine : jeu de développement, pas holdout
aveugle. Une fiche V10 différente peut être utile même si la cible manque.
Les timings bruts et tracemalloc sont dans le JSON ; V11 est plus lent ici
et inclut un briefing absent du chemin V10. Aucun gain de vitesse n'est déduit.
Tracemalloc mesure les allocations Python, pas toute la RAM ni la VRAM.

La rubrique structurelle constate un extrait sourcé, sept propositions,
contexte et trois éléments de protocole. Elle ne juge pas leur utilité réelle.
Pas de revue humaine, gain de temps Claude, qualité sémantique avec modèle,
validité Roblox, contradictions naturelles ou qualité visuelle mesurés.

## Autres critères et preuves

| Critère | Évidence et limite |
|---|---|
| Attribution | Extraits littéraux contrôlés ; candidats tous non vérifiés |
| Déduplication / reprise | Tests même source, nouvelle version et interruption après écriture |
| Mémoire | Deuxième recherche réelle : une unité réutilisée, une nouvelle candidate, puis ERROR explicite |
| HTTP | Réservations réelles 10 puis 1 ; robots/retries/cache séparés dans trace et tests |
| Coût IA | Zéro appel réel ; réservation et plafonds testés par fixtures |
| MCP | Processus stdio et briefing borné testés, pas comportement Claude Desktop |
| Contradictions | États DISPUTED/OUTDATED exposés et non réutilisés, pas juge général automatique |
| Procédures | Rubrique explicite, étapes proposées, revue humaine encore nécessaire |
| Blender | Comparaison réelle 42/58 triangles sous 4.3.2, pas FPS ni B3/C1 |

Les [logs](../validation/v11/) conservent les résultats du socle et de la suite
enrichie. Les fixtures de transport/embeddings ne sont pas des mesures Internet
ou IA. Le rapport ne revendique aucun pourcentage général d'amélioration.
