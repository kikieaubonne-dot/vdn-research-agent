# Vingt scénarios de recherche — V11.2

Résultats logiciels finaux : **15 PASS /5 PARTIAL /0 FAIL** sous Linux/Python3.12.14.
Les cinq PARTIAL sont les recherches documentaires initiales sans originaux suffisants.
PASS signifie que le comportement attendu a été observé ; aucune technique du jeu
n’est déclarée validée. Les fixtures d’échec/doublon/transport restent synthétiques.

[Données brutes complètes](proofs/scenarios.json) : entrées, attentes, résultats,
catégories, URLs/documents/offsets lorsqu’ils existent et durées. La reprise réelle
du réseau est publiée séparément dans [REPORT](REPORT.md).

| # | Entrée | Attendu | Obtenu | Sources / type | Durée s | État |
|---|---|---|---|---|---:|---|
| 1 | Forest realism + flashlight + performance | Several requirements; bounded tree; no HTTP | Plusieurs exigences et contraintes conservées ; plan borné. | SOFTWARE | 1.271 | PASS |
| 2 | forest depth8 | Reach foliage/alpha/shadows/flashlight; dependencies explicit | Descente jusqu’à la micro-branche lampe ; dépendances explicites. | SOFTWARE | 1.187 | PASS |
| 3 | forest/spruce/foliage/cards | Find candidates; flag missing original context | Candidates retrouvées ; originaux insuffisants. | SOFTWARE | 1.651 | PARTIAL |
| 4 | forest/spruce/foliage/cards/alpha/shadows/flashlight | Independent micro-branch; no invented shadow claim | Micro-branche séparée ; aucune affirmation d’ombre validée. | SOFTWARE | 1.384 | PARTIAL |
| 5 | forest/collisions | MeshPart candidates and reversible comparison proposal | Sources candidates et protocole réversible, sans validation B3/C1. | https://create.roblox.com/docs/performance-optimization/improve | 1.433 | PARTIAL |
| 6 | forest/ground/footprints | Specific footprint gap remains open | Lacune empreintes ouverte, aucun paramètre optimal inventé. | SOFTWARE | 1.165 | PARTIAL |
| 7 | forest/performance | Performance context without invented device/FPS result | Sources candidates ; appareils et mesures non inventés. | https://create.roblox.com/docs/performance-optimization/design ; https://create.roblox.com/docs/performance-optimization/improve | 1.184 | PARTIAL |
| 8 | Only foliage shadows under flashlight | Stable gap ID; no whole forest restart | ID de lacune stable, prérequis séparés, zéro HTTP. | https://create.roblox.com/docs/effects/light-sources ; https://create.roblox.com/docs/reference/engine/classes/SpotLight | 0.318 | PASS |
| 9 | Authored failed import | Research export only; no automatic action; next brief avoids same method | Échec synthétique conservé, branche export seule, méthode répétée suspendue. | https://create.roblox.com/docs/art/characters/creating/export-textures ; https://create.roblox.com/docs/art/accessories/creating-rigid/exporting | 1.066 | PASS |
| 10 | Trees used in several scenes | Same canonical branch technique, no scene-specific source copies | Même ID de technique réutilisé dans plusieurs scènes. | SOFTWARE | 0.735 | PASS |
| 11 | Two authored identical passages | One result with both aliases, preserved files | Deux notes de fixture identiques regroupées par alias, aucun effacement. | SYNTHETIC_NOTES | 0.281 | PASS |
| 12 | Candidate-only query | Candidate stays visible although main library empty | Réserve visible malgré bibliothèque principale vide. | SYNTHETIC_NOTES | 0.295 | PASS |
| 13 | Historical rejected notes | Archives retained; no rejected evidence in active documents | 42 notes archivées conservées ; aucune citation rejetée active. | SOFTWARE | 0.231 | PASS |
| 14 | No original snapshot for foliage flashlight shadows | Abstain from established facts; propose targeted search/test | Faits vides, méthode candidate et limites explicites. | SOFTWARE | 0.796 | PASS |
| 15 | Previously captured real original snapshots | Check source hash, URL and passage offsets; unknown versions explicit | SHA et offsets de captures réellement acquises vérifiés ; pas de preuve moteur. | https://create.roblox.com/docs/performance-optimization/improve ; https://create.roblox.com/docs/workspace/collisions | 0.592 | PASS |
| 16 | Authored inaccessible source | Source error explicit; keep first assessment, no false verification | Erreur d’accès simulée explicite ; premier reçu conservé. | SYNTHETIC_TRANSPORT | 2.185 | PASS |
| 17 | Brief forest budget500 | Bounded brief with omissions and drill-down, constraints/rollback retained | Brief ≤1800 caractères, omissions et accès au détail. | SOFTWARE | 6.937 | PASS |
| 18 | tree:forest/collisions | Detailed recipe, literal parameters, original/candidate distinction | Détail demandé ; protocole proposé, preuves/paramètres limités aux passages. | https://create.roblox.com/docs/performance-optimization/improve ; https://create.roblox.com/docs/workspace/collisions | 1.866 | PASS |
| 19 | Separate temporary Obsidian vault | Export tiers/scene links; second unchanged; rollback preserves source and ledger | Coffre isolé : simulation, committed, unchanged, rolled_back ; ledger intact. | SOFTWARE | 13.684 | PASS |
| 20 | Real MCP stdio process | All 27 contracts unchanged; Bible/plan/brief/detail/failure roundtrip | Vrai processus stdio : 27 contrats identiques, Bible/plan/brief/détail/échec. | SOFTWARE | 8.093 | PASS |

Les sources citées en étapes3–7 sont des références candidates lorsqu’un original
local manque. L’étape15 réutilise des captures originales du runtime isolé fourni ;
elle ne constitue pas une nouvelle consultation Web ni une validation moteur.
Les jeux de requêtes RAG demeurent séparés des fixtures fonctionnelles.

Reproduction sans accès réseau :

```sh
python -m bench.validate_research_roots --workspace /chemin/nouveau-hors-du-depot
```

Ajouter `--runtime /chemin/runtime-autorise` uniquement pour réutiliser ses captures
locales. Le répertoire de validation doit être nouveau et séparé du dépôt ; ses
expériences synthétiques ne doivent pas être importées dans la mémoire réelle.
