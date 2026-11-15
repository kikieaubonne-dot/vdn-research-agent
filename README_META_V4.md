# VDN V4 — Apprendre à mieux chercher (sans abonnement)

Cette version **conserve** les fonctionnalités V3 et ajoute une couche de méta-recherche mesurable. Elle ne prétend pas être plus intelligente que GPT-6 et ne réentraîne aucun modèle.

## Ce qui est réellement implémenté

- Trois formulations de recherche par source, sélectionnées par exploration/exploitation UCB1.
- Filtre de pertinence explicite avant création des fiches ; réduction des résultats manifestement hors sujet.
- Historique durable dans `output/meta_state.json` ; rapport dans `output/meta_report.md`.
- Exploration des stratégies non testées, puis adaptation progressive selon la pertinence apparente.
- Aucune modification autonome du code ; les changements de stratégie sont réversibles.
- Tests unitaires hors réseau.

## Ce qui reste à développer / mesurer

- Benchmark humain de référence (questions et réponses attendues) et mesures de précision/rappel.
- Comparaison factuelle de sources, vérification des affirmations et déduplication sémantique.
- Méta-recherche documentaire sur les méthodes de recherche ; cette V4 optimise d'abord des requêtes prédéfinies.
- Ollama en local, facultatif, pour raisonnement plus poussé.
- Tests dans Roblox Player / Studio (impossibles dans ce workflow Linux standard).

## Installation

Copier le contenu de ce ZIP **dans le dépôt existant**, sans supprimer `knowledge/` ni `output/`. Dans GitHub Desktop, `Commit to main` puis `Push origin`. Dans Actions, lancer manuellement le workflow. Lire `output/meta_report.md` et `output/last_run.json`.

## Attention aux limites gratuites

GitHub Actions planifié peut être retardé ou suspendu, notamment sur un dépôt public inactif. Les endpoints publics peuvent limiter les requêtes. Le filtre est heuristique : des sources utiles peuvent être écartées et des sources médiocres acceptées. Les scores ne prouvent jamais la validité des techniques.

## Protocole de vérification

1. Vérifier que les tests passent et que le workflow termine.
2. Vérifier que `strategy_trials` contient des variantes et que `meta_state.json` évolue.
3. Comparer manuellement 20 résultats acceptés/rejetés pour mesurer les faux positifs/négatifs.
4. Vérifier qu'une source hors sujet n'est pas devenue une fiche validée.
5. Ne jamais utiliser le score de pertinence comme preuve de compatibilité Roblox.
