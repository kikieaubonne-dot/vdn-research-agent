# Roadmap V9 fondée sur V8

## P0 — intégration réelle et fiabilité

1. Exécuter la suite et le smoke test MCP sur Windows avec et sans droits de
   création de symlinks. Vérifier démarrage depuis Claude Desktop, arrêt et reprise.
2. Ajouter une récupération du cache SQLite corrompu sous verrou, avec archivage
   des fichiers avant reconstruction et tests d'interruption.
3. Unifier les quotas des entrées manuelles de collecte selon la roadmap V7.
   Garder les commandes de lecture complètement hors ligne.

## P1 — procédures et preuves inspectables

1. Définir un registre de revues humaines distinct des rapports de clients.
   Réserver les promotions aux preuves inspectées : protocole, scène/version,
   paramètres, fichiers de sortie, mesures et identité du réviseur.
2. Compléter les prérequis, paramètres et étapes des branches sapin/forêt les plus
   pauvres. Mesurer la proportion de procédures reproductibles, pas leur longueur.
3. Réaliser des expériences Studio/Blender autorisées, puis enregistrer succès,
   échecs et conditions. Une affirmation de Claude reste non vérifiée par défaut.
4. Améliorer la sélection complémentaire et les contradictions intersources avec
   un corpus annoté indépendant, notamment moteurs incompatibles et versions.

## P2 — pertinence et performances

1. Étendre le jeu de développement et figer un nouveau jeu de test indépendant
   FR/EN avant réglage. Inclure les domaines hors arbres et les requêtes négatives.
2. Mesurer séparément le moteur, la façade enrichie, les plans et le client MCP
   sur 100/1 000/10 000 notes. Réduire les rescans de fichiers et la contention
   SQLite sans perdre la détection de changements ni la conservation du corpus.
3. Étudier des équivalences mieux désambiguïsées et des candidats par domaine,
   puis comparer à V8 avec budgets, hit@k, MRR et latences identiques.

## P3 — interfaces graphiques contrôlées

1. Exposer à Claude des propositions de scènes et scripts relisibles, avant toute
   exécution dans Blender/Roblox. Ajouter ensuite des connecteurs explicitement
   autorisés, avec droits minimaux, revue et annulation des modifications.
2. Aucune auto-fusion, auto-modification ou auto-publication de code en production.
   Toute évolution reste en branche, testée et revue humainement.
