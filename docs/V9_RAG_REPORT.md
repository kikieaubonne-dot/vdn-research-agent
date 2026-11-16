# Comparaison V8/V9 sans nouveau moteur RAG

`bench/v9_holdout.json` contient 16 questions figées avant évaluation : FR, EN,
mixtes, ambiguës, techniques, multi-étapes, multi-sources, versions, hypothèse
fausse et quatre hors corpus. Douze ont des références attendues. Les règles
lexicales du RAG V8 n'ont pas été réglées sur ces questions.

| Mesure | V8 initial | V8 + 4 fiches | V9 + 4 fiches |
|---|---:|---:|---:|
| Notes indexées | 94 | 98 | 98 |
| Hit@1 | 0,500 | 0,917 | 0,917 |
| Hit@3 | 0,583 | 1,0 | 1,0 |
| Hit@5 | 0,583 | 1,0 | 1,0 |
| MRR | 0,542 | 0,958 | 0,958 |
| Identité des références restituées | 1,0 | 1,0 | 1,0 |

Le gain vient de la couverture documentaire. À corpus identique, il n'y a **aucun
gain de classement revendiqué**. Le benchmark historique reste inchangé : la
politique déployée conserve Hit@1/@3/@5 et MRR 1,0, et MRR de développement 0,847.

Le briefing V9 s'abstient sur les quatre hors corpus. V8 renvoie des candidats,
sans champ d'abstention ; le rapport utilise seulement son résultat vide comme
proxy explicite. Cette comparaison n'équivaut pas à une mesure de jugement par
Claude. Les versions demandées restent inconnues/non vérifiées. Une hypothèse
fausse est évaluée ici sur sa récupération de sources, pas sur une correction
sémantique automatique supposée.

Les citations sont contrôlées comme identités de notes/URLs et, pour les nouvelles
citations, comme fragments littéraux des pages lues. **La vérité sémantique, la
couverture complète des procédures et leur fonctionnement Studio ne sont pas
notés automatiquement.** Labels d'un seul ingénieur, petit échantillon, aucun
test utilisateur de productivité : limites importantes de généralisation.

Les temps de l'API enrichie sont de l'ordre de 70–80 ms médians sur ce petit lot,
indexation initiale de l'ordre de 80 ms. Ce n'est pas le moteur brut seul, ni une
preuve de gain de vitesse. Les JSON conservent les valeurs exactes de chaque
exécution et les rangs par question.

```sh
python -m bench.evaluate_v9 --root . --output work/v9-holdout.json
python -m bench.evaluate_v8 --root . --output work/v9-historical.json
```

Pour la baseline, un checkout propre de `8d83868` a été chargé via `--code-root`,
avec corpus initial puis enrichi, mêmes requêtes et mêmes budgets API. Les fichiers
`v9/holdout_v8_original.json`, `v9/holdout_v8_enriched.json` et
`v9/holdout_v9_enriched.json` rendent cette distinction inspectable.
