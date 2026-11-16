# Évaluation RAG V8 — avant / après

Corpus exact : `knowledge/` de `9abf775`, 106 fichiers, 94 notes indexables.
Base de code V7 : `f5cb699`. Les résultats bruts et empreintes sont dans
[AUTONOMY_V8_RAG_METRICS.json](AUTONOMY_V8_RAG_METRICS.json).

## Reproduction et diagnostic

La baseline indépendante reproduit hit@1 **0,9**, hit@3 **0,9**, MRR **0,925**.
Pour « importer un squelette personnalisé, os qui buguent », la fiche
`vdn-1290b940c378` est quatrième. Devant elle : erreur d'export Blender,
performances et export générique.

L'expansion des synonymes utilisait une limite globale de douze entrées,
consommée par les premiers mots. Le vocabulaire d'acquisition associait aussi
`os` à `wind` et `squelette` à l'animation générale ; les formes FR d'import et
de glitch étaient peu couvertes. Un long passage générique pouvait gagner par
BM25 et par les poids de statut/confiance déclarés.

V8 utilise des groupes d'équivalences techniques bilingues équilibrés, notamment
rig/armature/squelette, bone/os, import et export séparés. Les notions API
Atmosphere, Density et Haze sont distinguées du brouillard général. Le classement
choisi compare couverture des concepts, couverture du titre, puis BM25. La
fiabilité technique est renvoyée séparément ; aucune exception liée à une
question précise ou à un identifiant de fiche n'est codée.

## Comparaison sur développement et benchmark historique

Douze requêtes de développement ont été rédigées à partir du contenu des sources,
avant le choix final. Elles sont distinctes des dix requêtes historiques, avec
des sujets communs ; ce n'est pas un grand jeu de test indépendant. Une première
version confondait encore les notions atmosphériques ; les cas de développement
ont permis de resserrer ces équivalences avant le choix final.

| Politique | Dev hit@1 | Dev hit@3 | Dev MRR | Historique hit@1/@3/@5 | Historique MRR |
|---|---:|---:|---:|---|---:|
| Legacy | 0,75 | 0,917 | 0,822 | 0,9 / 0,9 / 1,0 | 0,925 |
| Expansion équilibrée + BM25 | 0,75 | 0,917 | 0,854 | 1,0 / 1,0 / 1,0 | 1,0 |
| Couverture puis titre et BM25 — retenue | 0,75 | 1,0 | 0,847 | 1,0 / 1,0 / 1,0 | 1,0 |
| Couverture + anciens poids déclarés | 0,75 | 1,0 | 0,833 | 1,0 / 1,0 / 1,0 | 1,0 |

Le choix privilégie la récupération de références complémentaires dans les trois
premières positions, sans perte de hit@1 de développement et avec un MRR supérieur
à la baseline. La variante BM25 seule conserve un MRR de développement un peu
meilleur : ce compromis est explicite. Tous les négatifs historiques restent
propres. Le scénario naturel du squelette retrouve aussi la fiche attendue en
première position.

## Latence et indexation

Mesures locales Linux/Python 3.12, SQLite FTS5 ; aucun coût API ni appel réseau.
Les latences sont celles de `rag.search_knowledge`, hors enrichissement de façade,
mesurées sur un lot de dix requêtes historiques, sans garantie de significativité.

| Indicateur | Legacy / V7 | V8 |
|---|---:|---:|
| Recherche médiane sur les requêtes historiques | 4,25 ms | 6,16 ms |
| Recherche p95 sur ce petit lot | 10,41 ms | 11,51 ms |
| Index initial, médiane de 5 lancements | 56,13 ms | 73,53 ms |
| Index incrémental inchangé, médiane de 5 lancements | 17,61 ms | 32,38 ms |

**V8 n'est pas annoncé plus rapide.** La validation des chemins/métadonnées et
le calcul des couvertures ajoutent du travail. Le coût absolu reste faible sur
ce corpus, mais une montée en taille devra être mesurée. L'API enrichie et les
plans consultent plusieurs fiches ; leurs latences sont supérieures au moteur
brut et ne sont pas couvertes par cette table.

## Reproduire

```sh
python -m bench.evaluate_v8 --root . --output work/rag-v8.json
python -m tests.offline
```

Les quatre politiques réutilisent le même index. L'ancienne politique est gardée
pour comparaison, pas comme second RAG. Le benchmark historique original n'a pas
été modifié. Les cinq mesures d'index avant/après et la baseline indépendante
sont conservées dans le JSON brut. Aucun de ces scores ne mesure la vérité d'une
technique ni son fonctionnement dans Studio.
