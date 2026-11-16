# Mesures V11.2 — critères et limites

## Compatibilité et contrats

La base exacte d23aafa passe 369 tests avant modification. V11.2 passe 416 tests
sous Linux, puis 416 avec la configuration personnelle autorisant le réseau dans
une copie jetable ; toutes les sockets restent interdites par le harnais hors
ligne. Les 47 ajouts incluent les régressions rouges avant correction, le vrai
processus MCP stdio (initialize/list/call), les 27 schémas, la chaîne
Bible → plan → collecte contrôlée → passage → synthèse → fiche → Obsidian/RAG → MCP,
ainsi que budget, interruptions, reprise, rollback, modèle indisponible, sources
hostiles, versions, doublons, faux paramètres et échec lié.
Les [journaux](../validation/v112) distinguent ces essais de la session réseau.

Les [36 contrats annotés](intelligence-contracts.json) V11.1 passent 36/36,
exactitude du contrat d'attribution 100 %. C'est un jeu synthétique de développement,
pas un échantillon indépendant de vérité Roblox ni une mesure de vérité sémantique.

## Comparaison de sept briefings sur le même corpus réel capturé

A : checkout exact V11.1 d23aafa. B : mode projet V11.2. Les deux lisent la même
copie isolée de connaissances et snapshots. Questions et critères sont fixés dans
`bench/evaluate_project.py`, les [résultats bruts](benchmark.json) conservent les
structures et hachent/retirent les extraits protégés. Les originaux complets restent
privés dans le laboratoire de livraison. Aucun appel Claude, modèle ou réseau.

| Critère mécanique | A V11.1 /7 | B V11.2 /7 |
|---|---:|---:|
| Jeu explicitement nommé | 0 | 7 |
| Moteur Roblox mentionné | 7 | 7 |
| Appareil inconnu visible | 7 | 7 |
| Rollback présent | 4 | 7 |
| Protocole de test structuré | 0 | 7 |
| Étapes avec composants | 0 | 7 |

Les identifiants des sept tâches attendues sont retrouvés 7/7 : collisions,
lampe, performance, texture, animation, interaction et export. Les annotations
attendues sont des identités de tâches, pas des réponses techniques fabriquées.

| Tâche | Caractères A | Caractères B |
|---|---:|---:|
| Collisions | 5 982 | 3 617 |
| Lampe | 5 688 | 3 430 |
| Performance | 5 596 | 3 249 |
| Texture | 5 765 | 3 404 |
| Animation | 5 404 | 3 337 |
| Interaction | 5 270 | 3 621 |
| Export | 6 164 | 4 504 |

Total 39 869 → 25 162 caractères, soit 36,9 % de moins sur ces sorties JSON.
Le compteur tokens est une estimation caractères/3,6, pas le tokenizer de Claude.
Ce résultat ne prouve ni économie de quota, ni baisse du coût d'implémentation.
Mémoire Python tracemalloc de l'évaluation : 2 209 978 octets de pic, ni RSS total
ni VRAM. Les latences brutes sont enregistrées : A inclut le démarrage Python et
B est en processus ; aucune accélération n'est déduite de cette comparaison.

## Régressions, compromis et non-mesures

Le mode projet choisit un seul problème ou demande une clarification ; une grande
question multi-thèmes doit passer par un pack ou plusieurs fiches. La synthèse
V11.1 générique reste disponible. Une archive publiée ne fournit pas les faits
revalidés d'un original local ; les faits peuvent donc être moins nombreux dans
un clone propre. Ce refus volontaire et la contrainte de détail sous petit budget
évitent de livrer une procédure tronquée comme complète. Certains passages restent
hors sujet, versions inconnues et documents tronqués ; la qualité les signale.
Les sources performance accessibles ne suffisent pas encore pour une fiche sourcée.

Pas de jugement humain aveugle de pertinence, pas de preuve d'implication sémantique,
pas de score réel Claude, ni Blender 5.2, Studio, B3/C1, multimodal, embeddings ou
Ollama exécuté. Pas de modèle recommandé par défaut. Les indicateurs de structure
sont utiles pour vérifier le contrat, pas pour annoncer un gain de jeu final.

Reproduction sans réseau, en fournissant le même corpus local et un checkout
séparé de d23aafa :

```powershell
& $python -m bench.evaluate_project --root C:\lab\v112 --baseline C:\lab\v111-baseline --output C:\lab\benchmark.json --private-output C:\lab\raw-private.json
& $python -m bench.evaluate_intelligence --output C:\lab\contracts.json
```

Le laboratoire n'est pas un jeu de test distribué avec les corps complets des
pages : `research-session.json` et la trace donnent les reçus et URL. Une nouvelle
capture peut changer les résultats ; conserver ses propres versions et budgets.
