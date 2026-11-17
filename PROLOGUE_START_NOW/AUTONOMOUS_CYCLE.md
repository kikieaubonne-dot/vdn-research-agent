# Mission fondamentale — laboratoire indépendant de Claude

Objectif conservé : cahier des charges → branches → mémoire/lacunes → recherche ciblée → comparaison → essai isolé → correction bornée → preuves → export/RAG → récupération MCP.

Le dépôt contient déjà le planificateur récursif, sessions, collecteurs, mémoire d'expériences, superviseur et export Obsidian. Le paquet ne les remplace pas. Les ressources et procédures restent accessibles à Claude sans modèle local activé ; cela ne prouve pas que la recherche autonome tourne.

**État actuel : bibliothèque cumulative consultable, autonomie arrêtée.** Une mission ponctuelle a été autorisée et exécutée dans le cloud, puis clôturée :4HTTP supplémentaires et26,694s de calcul enregistrées. Le worker autonome a terminé son cycle en30,27s ; la correction du protocole et de la capture ont ensuite été dirigées par Codex dans la même fenêtre autorisée. Ce n'est pas15minutes de recherche continue ni une autonomie complète.

Le ledger livré conserve103,752s ; la politique60s est restaurée sans diminuer ce compteur. Les copies V10/V9 n'ont pas été remises à zéro. Les32Mio de contenu de cette copie conservent ses preuves. Aucun modèle ni service permanent n'a été lancé. Toute nouvelle expérience requiert un budget applicable et approuvé.

`FOREST_FIRST_BENCHMARK.json` précise le résultat réel partiel. Les branches tronc, branches, neige et matériaux sont ajoutées au catalogue comme PROPOSED ; aiguilles/cartes, vent et performances restent distincts. Leur existence ne prouve pas leur couverture. Seule la portabilité limitée des matériaux/géométries a été testée ici, sur deux propres proxies.

Depuis Claude : demander directement `tree:forest/spruce` ou une microbranche connue, puis le détail par synthesize_technical. L'essai de transport du paquet contrôle en particulier la branche ombres des cartes sous lampe, sans envoyer toute la bibliothèque. Il ne mesure pas des tokens Claude ni une amélioration Recall/MRR.

Pour un démarrage autonome réel : utiliser une NOUVELLE mission isolée du lanceur existant, **seedée depuis le runtime livré pour conserver les compteurs** ; préflight ; budget/cible explicitement approuvés ; activation explicite ; vérifier processus, heartbeat et un cycle complet. Ne pas installer de tâche permanente. Une configuration générée ou un doctor réussi ne constitue pas AUTONOMY_RUNNING.

La politique future par mission/outil doit être approuvée avant application. Elle ne peut modifier aucun quota Claude/Codex/API externe. Sans budget autorisé et stockage suffisant, continuer consultation/préparation et signaler BLOCKED, sans prétendre que le laboratoire recherche en arrière-plan.

`agent/forest_mission.py` est un Worker expérimental pour une copie gelée explicitement préparée : l’essai conservé utilisait un eponge.py dédié et des sessions plafonnées à4HTTP. Ce module n’est pas une nouvelle commande de production générale. Le lanceur stable, ses gardes et la configuration Windows restent inchangés. Un préflight supplémentaire refuse maintenant une session dont le plafond ne tient pas dans le budget restant de mission.
