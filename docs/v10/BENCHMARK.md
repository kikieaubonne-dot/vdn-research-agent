# V10 — mesures et protocole reproductible

Les mesures concernent le code local et les contrats d’intégration. Aucune mesure
Studio, Blender, gain de production ou réussite de création d’asset n’est déduite.

```sh
python -m tests.offline
python -m bench.demonstrate_v10 --root . --output docs/v10/demo.json
python -m bench.evaluate_v10 --root . --output docs/v10/holdout_v10.json
```

## Régression et sécurité

Baseline V9 reproduite : **251 tests**. Version livrée : **288 tests**, dont
37 nouveaux, avec sockets interdits jusque dans les sous-processus.
[Baseline](../validation/v10/baseline-tests.log) ·
[Suite finale](../validation/v10/final-tests.log).

Les nouveaux cas couvrent cycle de vie, échecs après reprise, révisions périmées,
résultats idempotents, corruption de contenu et de structure, interruption,
erreur disque, secrets, symlinks, preuves falsifiées, réservations HTTP avant
effet, quotas quotidiens, plafond de tentatives, temps nul, réduction de profondeur,
calendrier et allowlist. Le pipeline réel de collecte est exécuté avec un fournisseur
fixture ; aucun appel web V10 réel ni modèle distant n’est utilisé dans ces tests.

Intégrations : export/relecture/second sync/rollback dans un dossier temporaire,
exclusion des fiches d’expériences du RAG de sources, MCP stdio depuis un autre
dossier, permissions d’écriture et absence de revue MCP, adaptateurs de modèles
par transport simulé, annotations visuelles manuelles, import de mesures lié à
la bonne méthode et aux conditions. Les fixtures ne sont jamais comptées comme
preuves d’une technique Roblox. La CI exécute la suite sous Linux et Windows,
avec Python 3.11. Consulter les [résultats du commit courant](https://github.com/kikieaubonne-dot/vdn-research-agent/pull/4/checks),
sans inférer un succès Windows des tests Linux locaux. Le lanceur impose UTF-8
pour éviter CP1252 dans les lectures de fixtures et les échanges MCP des tests.

## Démonstration locale

[Données réellement produites](demo.json), sur copie temporaire du corpus :

| Mesure | Résultat |
|---|---|
| Profondeur observée | 2 |
| Branches totales | 13, plafond 24 |
| Ticks | READY puis BLOCKED |
| Raison du blocage | pas de preuve actionnable couvrant le tronc ; dépendances suivantes suspendues |
| Réseau / modèle externe | 0 / aucun |
| Expériences | 2 PLANNED, 1 FAILED synthétique explicitement étiquetée |
| Échec fixture retrouvé | oui |
| Procédures de jeu vérifiées / réutilisation mesurée | 0 / non mesurée |
| Export | 119 fichiers, second sync inchangé |
| RAG de sources après export | 98 fiches ; hubs/index/expériences exclus |
| Markdown d’origine | 110/110 inchangés |

Le temps de traitement et le budget coopératif consommé sont dans le JSON ; ils
dépendent de cette machine. Aucun lien avec un temps humain gagné n’est établi.
Les doublons évités sont comptés par session (0 dans cette démonstration), sans
inventer un taux d’amélioration. Les erreurs récurrentes sont des occurrences
de messages dans les essais, pas des causes automatiquement prouvées.
`agent.v10 status` expose états, budgets, erreurs d’intégration de recherche et
occurrences d’erreurs ; réutilisation et gain de productivité restent non mesurés.

Deux garde-fous additionnels utilisent une source artificielle datée de 2000,
contenant une contradiction et une instruction malveillante. Elle est signalée
ancienne/contestée et reste non vérifiée ; aucune instruction n’est exécutée.
Cette fixture ne fait pas partie des connaissances historiques ni du benchmark
de pertinence. La détection reste lexicale ; elle ne trouve pas toute contradiction.

## V8 / V9 / V10, corpus comparable

Même holdout V9 figé : 16 questions, dont 12 cas de récupération et quatre hors
domaine. Il comprend français/anglais/mixte, plusieurs étapes, ambiguïté, versions,
fausse hypothèse et absence de réponse. Les gardes de sources anciennes et
contradictoires sont évaluées séparément ci-dessus.

| Implémentation, corpus enrichi de 98 fiches indexables | hit@1 | hit@3 | hit@5 | MRR |
|---|---:|---:|---:|---:|
| V8, mesure conservée V9 | 0,917 | 1,000 | 1,000 | 0,958 |
| V9, mesure conservée | 0,917 | 1,000 | 1,000 | 0,958 |
| V10, exécutée ici | 0,917 | 1,000 | 1,000 | 0,958 |

[Résultat V10 et références des baselines](holdout_v10.json). Le moteur de
récupération n’a pas changé. V10 utilise l’évaluateur V9 sans retoucher ses
questions ; le test ne mesure pas l’utilité des nouvelles expériences dans Claude.
Le briefing de base s’abstient sur les quatre questions hors domaine. La mesure
V8 utilisait un proxy différent (résultat vide) : ne pas présenter cela comme un
gain directement comparable. Identité des citations : 1,0 ; vérité sémantique non
mesurée. Un hit exact ne prouve ni exactitude technique ni compatibilité de version.
Les timings ne justifient aucune affirmation de vitesse ou productivité accrue.

## Conservation

[Manifeste](preservation.json) : SHA256 de chaque Markdown de la base V9, comparaison
avec le travail V10. Les 106 historiques **et** les quatre candidates V9 restent
inchangés. Les fichiers contenant les 251 cas de test restent byte pour byte
identiques dans Git. Seul leur lanceur `tests/offline.py` impose désormais UTF-8
à la suite et ses sous-processus sur Windows, en conservant les refus réseau.
Les nouveaux exemples, plans et preuves de validation sont hors du corpus historique.
