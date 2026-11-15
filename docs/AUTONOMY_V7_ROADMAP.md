# Roadmap V7 — étapes fondées sur les limites mesurées

Les priorités ci-dessous concernent **l'ingénierie**, pas le classement des recherches.
Chaque étape doit conserver les notes historiques, des fixtures locales et une
validation humaine des modifications de code avant déploiement.

## P0 — suivi de fiabilité

1. Unifier la comptabilité des commandes manuelles `research`, `enrich` et outils
   hérités avec celle de `cycle`/`refresh`. Tester une interruption à chaque point
   d'entrée et une journée mélangeant les différentes commandes.
2. Tester sous Windows les verrous système, liens de création exclusive et
   remplacements atomiques. Ajouter une matrice CI séparée sans appel réseau.
3. Ajouter un journal transactionnel de reprise pour les compteurs et la fin de
   cycle. Tester les coupures entre note, registre, file et rapport ; conserver
   les fichiers corrompus avant toute reconstruction.
4. Vérifier sur une exécution GitHub Actions revue humainement les quotas réels,
   temps d'indexation, indisponibilités de sources et sauvegarde des diagnostics.
   Ne pas augmenter les plafonds avant ces observations.

## P1 — profondeur et plans utiles

1. Constituer un corpus annoté de questions et prérequis Roblox/Blender/Unreal :
   simple, sapin enneigé, rig animé, lumière nocturne, conversion d'assets.
   Mesurer couverture des prérequis, relances inutiles et accord entre deux
   évaluateurs avant d'étendre les profils déterministes.
2. Définir une réouverture contrôlée des prérequis terminés sans preuve suffisante.
   Aujourd'hui leurs dépendants restent explicitement bloqués ; ne pas les
   débloquer sur la seule base d'un score ou d'un statut `done`.
3. Relier les sources et versions aux affirmations, puis tester des contradictions
   explicites et implicites sur fixtures. Conserver les deux sources et l'état
   non résolu tant qu'aucun test ou arbitrage ne départage leurs conditions.
4. Évaluer les priorités lexicographiques sur des plans complets annotés et des
   budgets identiques. Comparer à la priorité de sujet de la baseline ; ne pas
   annoncer une meilleure pertinence sans cette mesure.
5. Étendre les sorties de `evaluate` avec protocoles de reproduction saisis et
   résultats datés. Réserver `verifie` à des preuves externes inspectables.

## P2 — validation technique et mémoire

1. Ajouter des bancs locaux Blender puis des protocoles Roblox Studio : scènes,
   versions, paramètres, matériel, mesure de rendu et répétitions. Exécuter les
   scripts tiers uniquement après revue humaine.
2. Améliorer les quatre faux positifs et le faux négatif du filtre existant avec
   un jeu de développement séparé du benchmark, pour éviter son surapprentissage.
3. Tester la déduplication de paraphrases et synonymes : mesurer faux doublons
   et doublons manqués avant toute fusion de recherches. Ne jamais fusionner ou
   supprimer automatiquement les fiches historiques.
4. Prévoir une archive de l'historique de file si sa croissance est mesurée comme
   un problème ; préserver les clés, les parents, les erreurs et les décisions.

## P3 — stratégies et propositions de code

1. Comparer les stratégies UCB existantes par sources utiles, lacunes effectivement
   résolues, coût HTTP, temps et variance ; distinguer récompense de collecte et
   exactitude technique. Définir une taille d'échantillon avant conclusions.
2. Autoriser uniquement des propositions de code en branche isolée : reproduction
   d'un défaut, test échouant, correction, non-régression, rapport puis revue humaine.
   Aucun auto-déploiement et aucune auto-fusion dans `main`.

## Critères de passage

Pour chaque étape : baseline archivée, scénario reproductible, tests sans réseau
par défaut, absence de perte de connaissances, budget respecté, mesure comparée
et limites explicites. Une étape bloquée doit rester visible dans le rapport.
