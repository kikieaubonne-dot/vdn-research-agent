# Contrat d’acceptation V6.4

210 exigences reprises avec IDs stables. Aucun cumul de tests ne valide automatiquement une exigence composée.
Statuts : {'PASS': 21, 'FAIL': 0, 'BLOCKED': 75, 'NOT_TESTED': 114}. Les clauses partielles restent NOT_TESTED ou BLOCKED.

[Détail machine-readable](ACCEPTANCE.json) · [Preuves](REPORT.md)

| ID | Priorité | État | Exigence |
|---|---|---|---|
| R001 | P1 | NOT_TESTED | Inventorier modules, dépendances, scripts, tests, MCP, configs et chemins d'exécution. |
| R002 | P0 | PASS | Vérifier l'état Git et préserver les changements non committés. |
| R003 | P0 | PASS | Créer un point de restauration et prouver qu'il est lisible. |
| R004 | P1 | NOT_TESTED | Établir une matrice de capacités avec état initial, final et preuve. |
| R005 | P1 | NOT_TESTED | Cartographier les dépendances et identifier le chemin critique vers la démo réelle. |
| R006 | P0 | PASS | Conserver les interfaces publiques existantes ; versionner tout changement incompatible. |
| R007 | P1 | NOT_TESTED | Définir un contrat d'acceptation machine-readable avec ID stable par exigence. |
| R008 | P1 | NOT_TESTED | Relier chaque exigence P0 à un test automatique ou une preuve manuelle explicite. |
| R009 | P0 | PASS | Livrer un chemin de démarrage minimal qui marche avant les extensions avancées. |
| R010 | P1 | NOT_TESTED | Produire un rapport final « fait / testé / réel / bloqué / restant », sans affirmations non prouvées. |
| R011 | P1 | NOT_TESTED | Définir et valider ResearchFinding : ID, assertion, URL, date, licence, provenance, confiance, statut. |
| R012 | P1 | NOT_TESTED | Définir ExperimentSpec : hypothèse, baseline, variables, contrôles, métriques, seuils, budget. |
| R013 | P1 | NOT_TESTED | Définir ExperimentResult : exécution, versions, mesures, fichiers, logs, conclusion, erreurs. |
| R014 | P1 | NOT_TESTED | Définir MissionTask : ID, dépendances, permissions, statut, checkpoints, critères de fin. |
| R015 | P1 | NOT_TESTED | Définir UserFeedback : cible/version, commentaire original, défauts, critères, acceptation. |
| R016 | P1 | NOT_TESTED | Définir ValidatedSolution : méthode, preuves, compatibilité, limites, version, statut. |
| R017 | P1 | NOT_TESTED | Utiliser des schémas versionnés et des migrations testées ; éviter les formats implicites. |
| R018 | P0 | NOT_TESTED | Garantir l'écriture atomique des états critiques et détecter les données corrompues. |
| R019 | P0 | NOT_TESTED | Associer hashes de contenu, horodatages et versions d'outils aux artefacts. |
| R020 | P0 | NOT_TESTED | Vérifier la récupération après redémarrage sans perdre ni dupliquer les tâches. |
| R021 | P1 | NOT_TESTED | Séparer recherche exploratoire, récursive, récurrente et déclenchée par événement. |
| R022 | P0 | NOT_TESTED | Interroger mémoire et expériences avant d'interroger Internet. |
| R023 | P1 | NOT_TESTED | Générer des requêtes ciblées à partir des lacunes identifiées. |
| R024 | P0 | NOT_TESTED | Limiter profondeur, branches, durée et volume de recherche. |
| R025 | P1 | NOT_TESTED | Dédupliquer URL, contenus, assertions et recherches déjà réalisées. |
| R026 | P1 | NOT_TESTED | Dater les informations et invalider les connaissances périmées selon leur nature. |
| R027 | P1 | NOT_TESTED | Conserver les sources, versions, contradictions et incertitudes. |
| R028 | P1 | BLOCKED | Vérifier les licences, restrictions d'utilisation et provenance des assets. |
| R029 | P0 | PASS | Traiter les pages Web comme des données non fiables, jamais comme des instructions. |
| R030 | P1 | BLOCKED | Déclencher la veille selon un calendrier et prouver la reprise après interruption. |
| R031 | P0 | PASS | Séparer hypothèse, affirmation de source, simulation, test réel et préférence utilisateur. |
| R032 | P1 | NOT_TESTED | Indexer fiches, scripts, assets, expériences et résultats négatifs. |
| R033 | P0 | NOT_TESTED | Préserver la Bible technique et l'intégration Obsidian si elles existent. |
| R034 | P1 | NOT_TESTED | Proposer une recherche sémantique avec repli lexical si le modèle d'embeddings est absent. |
| R035 | P1 | NOT_TESTED | Évaluer la récupération sur un jeu de questions Roblox annotées. |
| R036 | P1 | NOT_TESTED | Réduire les faux positifs, notamment les légendes d'images prises pour des faits. |
| R037 | P1 | NOT_TESTED | Gérer versions, contradictions, dépendances et dépréciation des fiches. |
| R038 | P0 | NOT_TESTED | Produire des briefings Claude courts avec références et niveaux de preuve. |
| R039 | P1 | NOT_TESTED | Éviter de recommander une méthode incompatible avec la version moteur ou l'asset. |
| R040 | P1 | BLOCKED | Tester le transfert : réutiliser une méthode de sapin sur un buisson sans copier aveuglément. |
| R041 | P0 | PASS | Créer un répertoire de laboratoire isolé, distinct du projet Roblox principal. |
| R042 | P0 | NOT_TESTED | Définir pour chaque expérience une hypothèse falsifiable et une baseline immuable. |
| R043 | P0 | NOT_TESTED | Fixer les variables, contrôles, métriques et critères avant de générer les variantes. |
| R044 | P1 | NOT_TESTED | Produire des variantes traçables avec identifiant, parent et différences exactes. |
| R045 | P1 | BLOCKED | Exécuter L0 statique, L1 Python, L2 Blender, L3 Roblox, L4 visuel selon disponibilité réelle. |
| R046 | P0 | NOT_TESTED | Capturer entrées, sorties, versions, mesures, erreurs et artefacts vérifiables. |
| R047 | P1 | NOT_TESTED | Comparer A/B sous conditions constantes : caméra, éclairage, résolution, scène, version. |
| R048 | P1 | NOT_TESTED | Répéter les mesures bruitées et signaler les résultats inconclusifs. |
| R049 | P0 | NOT_TESTED | Enregistrer aussi les échecs pour éviter la répétition des mêmes expériences. |
| R050 | P1 | BLOCKED | Promouvoir une solution uniquement si les critères préalables sont atteints sans régression critique. |
| R051 | P1 | NOT_TESTED | Créer des benchmarks de développement visibles et un jeu de validation séparé. |
| R052 | P0 | BLOCKED | Garder un jeu de tests « holdout » hors du contexte des générateurs ; contrôler son accès. |
| R053 | P0 | BLOCKED | Empêcher les agents d'adapter directement leurs solutions aux réponses du holdout. |
| R054 | P1 | BLOCKED | Ajouter des tâches inédites : sapins, buissons, rochers, neige, lampe, caméra, rigging. |
| R055 | P1 | BLOCKED | Tester le transfert inter-domaines et distinguer succès réel de simple mémorisation. |
| R056 | P1 | NOT_TESTED | Comparer chaque nouvelle version à une baseline fixe et à la meilleure version précédente. |
| R057 | P1 | NOT_TESTED | Mesurer succès, régression, durée, coût, récupération et qualité par domaine séparément. |
| R058 | P1 | NOT_TESTED | Éviter un score global qui masque un échec grave ; définir des seuils éliminatoires. |
| R059 | P1 | BLOCKED | Détecter le « benchmark gaming » : tests modifiés, cas retirés, fuites et critères assouplis. |
| R060 | P1 | NOT_TESTED | Conserver un journal de progrès avec intervalle d'incertitude et contre-exemples. |
| R061 | P1 | NOT_TESTED | Boucler : défaut → hypothèse → patch/variante isolée → tests → décision → mémoire. |
| R062 | P1 | NOT_TESTED | Autoriser l'amélioration autonome des fiches, procédures, paramètres et prompts locaux. |
| R063 | P1 | NOT_TESTED | Autoriser la génération de scripts/artefacts expérimentaux dans un bac à sable. |
| R064 | P0 | PASS | Désactiver par défaut l'auto-modification de la branche principale et des règles de sécurité. |
| R065 | P1 | NOT_TESTED | Séparer générateur, exécuteur, évaluateur et gestionnaire de promotion. |
| R066 | P0 | NOT_TESTED | Utiliser des vérifications déterministes indépendantes du modèle générateur. |
| R067 | P1 | BLOCKED | Exiger rollback, preuves, compatibilité et absence de régression pour promouvoir. |
| R068 | P0 | NOT_TESTED | Limiter les tentatives ; arrêter les cycles stagnants ou qui se dégradent. |
| R069 | P1 | NOT_TESTED | Conserver les modifications refusées avec leur cause et éviter de les réessayer à l'identique. |
| R070 | P1 | BLOCKED | Démontrer une amélioration sur une tâche nouvelle, pas seulement sur le cas d'entraînement. |
| R071 | P0 | NOT_TESTED | Implémenter une machine à états persistante avec transitions valides et journalisées. |
| R072 | P0 | NOT_TESTED | Détecter dépendances circulaires, verrous, doubles exécutions et tâches orphelines. |
| R073 | P1 | NOT_TESTED | Garantir pause, reprise, annulation, timeout et retry borné avec backoff. |
| R074 | P1 | BLOCKED | Exposer modes MANUAL, SCHEDULED, IDLE, PAUSED et STOPPED. |
| R075 | P0 | BLOCKED | Respecter budgets CPU/GPU/RAM/disque ; un seul travail GPU lourd par défaut. |
| R076 | P1 | BLOCKED | Suspendre les travaux non urgents lorsque l'utilisateur sollicite fortement le PC. |
| R077 | P0 | PASS | Tester le mode autonome court avant toute session longue ; ne pas l'activer en secret. |
| R078 | P0 | NOT_TESTED | Appliquer permissions minimales, chemins autorisés, protection des secrets et arrêt d'urgence. |
| R079 | P0 | PASS | Interdire publication, dépenses, exécution Web non fiable et modification du jeu principal. |
| R080 | P0 | NOT_TESTED | Vérifier qu'une panne ou un crash n'endommage pas le projet ni les expériences validées. |
| R081 | P0 | PASS | Auditer et préserver les contrats MCP existants ; tester la découverte réelle des outils. |
| R082 | P1 | BLOCKED | Exposer mémoire, mission, expérience, feedback, statut, preuves, annulation et reprise via MCP. |
| R083 | P1 | BLOCKED | Tester un client MCP réel avec entrées valides, invalides, timeout et reconnexion. |
| R084 | P0 | BLOCKED | Tester Claude Desktop réellement si accessible ; sinon indiquer « non vérifié ». |
| R085 | P1 | BLOCKED | Tester Blender réel : génération, export, relecture, mesures et échec contrôlé. |
| R086 | P0 | BLOCKED | Tester Roblox uniquement dans une copie de scène, avec lecture, modification, vérification et rollback. |
| R087 | P1 | BLOCKED | Ne jamais assimiler un export Blender à une validation du rendu Roblox. |
| R088 | P1 | NOT_TESTED | Router les tâches déterministes vers Python et les raisonnements locaux vers Ollama si pertinent. |
| R089 | P1 | BLOCKED | Comparer missions avec/sans récupération mémoire : appels, tokens observables, temps et qualité. |
| R090 | P0 | PASS | Ne jamais déduire le pourcentage de quota Claude de simples estimations de tokens. |
| R091 | P1 | NOT_TESTED | Fournir un point d'entrée unique de diagnostic et de validation, compatible avec l'architecture existante. |
| R092 | P0 | PASS | Faire lancer par Codex lui-même tests statiques, unitaires, intégration et bout en bout accessibles. |
| R093 | P0 | BLOCKED | Conserver et réexécuter la suite existante ; référence historique : 492 tests, 8 ignorés. |
| R094 | P0 | PASS | Répéter les tests critiques, notamment test_second_cycle_continues_without_repeating. |
| R095 | P1 | NOT_TESTED | Injecter en environnement isolé : crash, réseau absent, Ollama arrêté, cache corrompu, disque plein simulé. |
| R096 | P0 | PASS | Tester qu'un défaut volontairement introduit est détecté et bloque la promotion. |
| R097 | P0 | PASS | Générer rapports JSON et HTML locaux avec commandes, logs, versions, résultats et preuves. |
| R098 | P1 | NOT_TESTED | Exiger pour chaque P0 un scénario d'acceptation et un résultat PASS/FAIL/BLOCKED explicite. |
| R099 | P0 | BLOCKED | Exécuter une démo complète : sapin enneigé → deux variantes → feedback « branches trop plates » → correction → mémoire → récupération MCP ; tester Roblox/Claude si accessibles. |
| R100 | P0 | NOT_TESTED | Livrer un état utilisable, la commande de démarrage, les preuves, les limites et les prochaines actions ; ne jamais annoncer « 100 % prêt » sans les tests réels requis. |
| R101 | P0 | BLOCKED | Avant tout développement, exécuter un diagnostic non destructif de Python, dépendances, chemins Windows, permissions, Ollama, MCP, Blender et accès Roblox ; conserver la sortie brute. |
| R102 | P0 | BLOCKED | Vérifier l'environnement exact d'exécution de Codex : accès au dépôt, au terminal, au réseau, à l'interface graphique et aux applications ; signaler toute frontière inaccessible. |
| R103 | P0 | NOT_TESTED | Créer un seul lanceur local documenté pour démarrer, arrêter et diagnostiquer L'Éponge ; ne pas exiger une succession de commandes manuelles. |
| R104 | P0 | NOT_TESTED | Prévoir un mode doctor --json dont le code de sortie distingue prêt, dégradé et bloqué ; aucune erreur silencieuse. |
| R105 | P0 | NOT_TESTED | Créer un orchestrateur de validation automatique qui exécute les contrôles dans l'ordre, sauvegarde les logs et ne masque jamais un code de sortie non nul. |
| R106 | P0 | NOT_TESTED | Produire un manifeste de livraison contenant commit Git, versions d'outils, chemins d'artefacts, empreintes, tests, limitations et instructions de rollback. |
| R107 | P0 | NOT_TESTED | Tester le lanceur sur un environnement propre ou une installation simulée propre ; détecter les dépendances implicites et chemins absolus invalides. |
| R108 | P0 | NOT_TESTED | Vérifier que chaque commande documentée correspond à une commande réellement existante et qu'elle fonctionne dans l'environnement accessible. |
| R109 | P0 | BLOCKED | Tester les scénarios d'arrêt brutal entre sauvegarde, mise à jour d'état et promotion ; imposer des écritures atomiques et une récupération vérifiée. |
| R110 | P0 | NOT_TESTED | Ajouter un watchdog de tâches avec timeout, heartbeat, détection de blocage et terminaison des processus enfants dans le périmètre autorisé. |
| R111 | P0 | PASS | Interdire les promotions automatiques en présence de régressions critiques, données manquantes, résultats incertains ou tests non exécutés obligatoires. |
| R112 | P0 | PASS | Séparer strictement l'environnement de test du jeu publié ; utiliser une allowlist des chemins autorisés et vérifier le refus des chemins interdits. |
| R113 | P0 | BLOCKED | Tester une simulation de panne de disque, réseau, Ollama, Blender et MCP sans détruire ni altérer l'installation réelle. |
| R114 | P1 | NOT_TESTED | Exécuter un essai autonome borné de 30 à 60 minutes, avec plusieurs cycles et un rapport de consommation CPU/RAM/GPU/disque lorsque mesurable. |
| R115 | P1 | BLOCKED | Mesurer le taux de réussite sur un ensemble fixe de scénarios, puis sur des scénarios tenus à l'écart ; signaler surapprentissage, fuite de données et progrès illusoires. |
| R116 | P1 | BLOCKED | Définir des objectifs de service distincts : zéro perte de données lors des tests, zéro écriture non autorisée, 100 % des contrôles critiques applicables réussis, et taux de réussite opérationnel estimé avec incertitude. |
| R117 | P1 | BLOCKED | Fournir un rapport quotidien lisible par l'utilisateur : découvertes, expériences, améliorations acceptées, échecs, ressources consommées et prochaines priorités. |
| R118 | P0 | NOT_TESTED | Prévoir un mode dégradé utile si Claude, Roblox, Blender ou Internet sont absents ; aucune fonctionnalité ne doit être présentée comme validée dans un outil indisponible. |
| R119 | P0 | BLOCKED | Exiger une démonstration réelle de bout en bout du chemin critique accessible ; si Claude Desktop ou Roblox nécessitent une action humaine, documenter exactement cette action minimale et conserver BLOCKED jusqu'à vérification. |
| R120 | P0 | NOT_TESTED | Livrer seulement après exécution d'un contrôle final indépendant : tests, contrats d'acceptation, restauration, logs, commandes de démarrage et inventaire des blocages. Ne pas promettre zéro bug ni 99 % sans preuve. |
| R121 | P0 | NOT_TESTED | Journal d'incidents persistant |
| R122 | P0 | NOT_TESTED | Contrat d'incident versionné |
| R123 | P0 | NOT_TESTED | Niveaux de gravité |
| R124 | P0 | NOT_TESTED | Dossier de réparation lisible |
| R125 | P0 | NOT_TESTED | Rapport machine pour Codex |
| R126 | P1 | BLOCKED | Diagnostic automatique |
| R127 | P0 | NOT_TESTED | Déduplication et causalité |
| R128 | P0 | NOT_TESTED | Auto-réparation limitée |
| R129 | P0 | NOT_TESTED | Surveillance et watchdog |
| R130 | P0 | NOT_TESTED | Validation de réparation |
| R131 | P1 | BLOCKED | Bilan avant retour utilisateur |
| R132 | P0 | NOT_TESTED | Interface sans PowerShell répétitif |
| R133 | P1 | BLOCKED | Tests obligatoires de la boîte noire |
| R134 | P0 | NOT_TESTED | Conditions d'acceptation |
| R135 | P0 | NOT_TESTED | Comportement en cas d'échec du rapporteur |
| R136 | P0 | NOT_TESTED | Définition du succès de la relève |
| R137 | P0 | BLOCKED | Préflight de mise en service |
| R138 | P0 | PASS | Consentement explicite au fonctionnement autonome |
| R139 | P0 | BLOCKED | Démarrage conditionnel après livraison |
| R140 | P0 | PASS | GitHub n'est pas un ordonnanceur |
| R141 | P1 | BLOCKED | Découverte et configuration Obsidian |
| R142 | P0 | NOT_TESTED | Export Obsidian sûr |
| R143 | P1 | BLOCKED | Synchronisation bidirectionnelle contrôlée |
| R144 | P1 | BLOCKED | Graphe Obsidian et qualité |
| R145 | P1 | BLOCKED | File de travail prioritaire nocturne |
| R146 | P0 | NOT_TESTED | Exécution sans Roblox Studio |
| R147 | P0 | NOT_TESTED | Exécution sans Claude/Codex |
| R148 | P1 | BLOCKED | Gestion des sessions Windows |
| R149 | P1 | BLOCKED | Échéance de bilan configurable |
| R150 | P0 | NOT_TESTED | Rapport de matinée actionnable |
| R151 | P0 | NOT_TESTED | Vérification de présence de vie |
| R152 | P1 | BLOCKED | Gestion du budget et de l'énergie |
| R153 | P0 | NOT_TESTED | Validation réelle du premier cycle |
| R154 | P0 | NOT_TESTED | Dossier de blocage pour Codex |
| R155 | P0 | NOT_TESTED | Livrable de mise en service sans PowerShell répétitif |
| R156 | P0 | NOT_TESTED | Registre des incidents normalisé |
| R157 | P1 | BLOCKED | Diagnostic différentiel avant réparation |
| R158 | P0 | NOT_TESTED | Politique de réparation à trois niveaux |
| R159 | P1 | BLOCKED | Réparation des connecteurs de recherche |
| R160 | P0 | NOT_TESTED | Réparation de la mémoire et d'Obsidian |
| R161 | P0 | NOT_TESTED | Réparation du laboratoire Python |
| R162 | P1 | BLOCKED | Réparation Blender versionnée |
| R163 | P1 | BLOCKED | Diagnostic Roblox Studio et pont MCP |
| R164 | P0 | NOT_TESTED | Réparation des procédures et scripts |
| R165 | P1 | BLOCKED | Contrôle de non-régression indépendant |
| R166 | P1 | BLOCKED | Détection de faux progrès |
| R167 | P1 | BLOCKED | Généralisation inter-domaines |
| R168 | P0 | NOT_TESTED | Surveillance et auto-récupération |
| R169 | P1 | BLOCKED | Tests de panne contrôlée |
| R170 | P0 | NOT_TESTED | Validation des ressources nocturnes |
| R171 | P0 | NOT_TESTED | Mise en service sans commandes manuelles répétées |
| R172 | P1 | BLOCKED | Contrat de disponibilité à 11 h |
| R173 | P0 | NOT_TESTED | Auto-triage avant escalade Codex |
| R174 | P0 | NOT_TESTED | Dossier de réparation prêt à exécuter |
| R175 | P0 | BLOCKED | Test final de réduction de dépendance à Codex |
| R176 | P0 | NOT_TESTED | Superviseur hors processus et hors IA. Fournir un petit programme autonome, testable sans Ollama ni agent principal, qui observe PID, heartbeat, progression et exit codes. Il ne doit importer aucun module critique du cœur qu'il surveille. Le lancer uniquement après accord sur le mode persistant. |
| R177 | P0 | BLOCKED | Chaîne de récupération en trois niveaux. (a) redémarrage borné du worker, (b) bascule vers dernière version saine signée/empreintée, (c) arrêt sûr et diagnostic hors ligne. Un échec du réparateur ne doit pas entraîner une boucle infinie ; plafonner les redémarrages et activer un coupe-circuit. |
| R178 | P0 | NOT_TESTED | Images de restauration vérifiées. Avant chaque promotion, capturer versions, dépendances, configurations non secrètes, schémas et données critiques. Vérifier l'intégrité des sauvegardes par checksum et tester réellement une restauration sur copie jetable. |
| R179 | P1 | BLOCKED | Transactions pour migrations et mises à jour. Toute évolution du schéma de mémoire, de file ou de configuration utilise un journal de migration, une copie et une procédure de retour arrière ; écriture atomique et verrouillage inter-processus. |
| R180 | P0 | NOT_TESTED | Panne du système de réparation. Injecter une exception et un blocage dans le moteur de réparation lui-même ; prouver que le superviseur indépendant constate la panne, maintient les autres workers sûrs et produit un rapport sans appeler ce moteur. |
| R181 | P0 | BLOCKED | Démarrage après crash. Tester coupure simulée au milieu d'une expérience, d'un export et d'un checkpoint. Au redémarrage, reprendre ou annuler sans duplications ni promotion d'artefact incomplet. |
| R182 | P0 | NOT_TESTED | Inventaire des versions et capacités. À chaque lancement, relever versions disponibles de Python, Blender, Ollama, dépendances et ponts Roblox/MCP, puis tester les fonctionnalités effectivement disponibles ; ne pas inférer la compatibilité du seul numéro de version. |
| R183 | P1 | BLOCKED | Adaptateurs isolés et versionnés. Séparer le cœur de la logique d'intégration ; définir interfaces, timeouts, codes d'erreur, fixtures et tests de contrat par adaptateur. Conserver un adaptateur précédemment validé comme repli quand c'est sûr. |
| R184 | P0 | NOT_TESTED | Détection précoce des changements. Effectuer des smoke tests non destructifs avant chaque campagne ; désactiver uniquement la fonction incompatible, poursuivre les autres, enregistrer la différence de contrat et la reproduction minimale. |
| R185 | P1 | BLOCKED | MCP/Claude : récupération graduée. Tester serveur, transport, authentification, schéma et appels de lecture ; reconnecter avec backoff uniquement sur erreurs transitoires. Si Claude est absent, continuer les cycles locaux. Ne jamais contourner une autorisation ou demander/collecter un secret dans un journal. |
| R186 | P0 | BLOCKED | Roblox : bac à sable obligatoire. Toute expérimentation modifiant une scène passe par une copie dédiée avec identifiant vérifié ; refus explicite si la cible est le projet principal ou publié. Test réel Studio uniquement si une session graphique, le plugin et les permissions sont présents. Sinon BLOCKED, avec tâche différée. |
| R187 | P1 | BLOCKED | Blender : matrice de tests. Vérifier lancement headless, chargement scène jetable, exécution script, sauvegarde, réouverture, export et contrôle de maillage. Sur erreur d'API, essayer uniquement des chemins de compatibilité connus et testés ; ne jamais installer une version ou un script distant automatiquement. |
| R188 | P0 | BLOCKED | Tests de contrat après mise à jour. Sur environnement de test, injecter réponses MCP malformées, indisponibilité de Studio, changements de signature Blender et échec d'export ; prouver la dégradation partielle sans corruption et la création d'un correctif candidat si admissible. |
| R189 | P1 | BLOCKED | Capacités du modèle mesurées. Tester localement les modèles disponibles sur des tâches courtes de planification, extraction, critique et génération de script. Enregistrer erreurs, temps et taux de validation ; ne pas supposer qu'un modèle sait programmer correctement parce qu'il produit du texte plausible. |
| R190 | P1 | BLOCKED | Escalade interne sans Codex. Pour un échec : décomposition en sous-problèmes → recherche dans mémoire → récupération d'exemples validés → variante indépendante → test exécutable → critique indépendante. Limiter profondeur, tentatives et budget ; après épuisement, signaler UNRESOLVED. |
| R191 | P0 | PASS | Pas de faux apprentissage. Améliorer les procédures, prompts locaux, paramètres et corpus validé ; ne jamais prétendre que les poids d'Ollama ont été réentraînés sans véritable procédure d'entraînement et mesure. |
| R192 | P0 | NOT_TESTED | Métavision : état de croyance versionné. Conserver hypothèses, preuves, contre-exemples, confiance calibrée, coût de vérification et dernière validation. Toute nouvelle observation peut diminuer la confiance, invalider une méthode ou ouvrir une expérience ; préserver la provenance. |
| R193 | P1 | BLOCKED | Priorisation du temps disponible. Ordonnancer les tâches par utilité attendue pour la forêt, gain d'information, probabilité de réussite, coût CPU/GPU, durée, risque et dépendances. Réévaluer à chaque cycle, sans scruter Internet en continu ni épuiser les ressources. |
| R194 | P0 | NOT_TESTED | Exploration contrôlée et arrêt intelligent. Réserver une part configurable aux pistes nouvelles, mais arrêter une branche stérile selon critères documentés. Reprendre les tâches interrompues grâce aux checkpoints. Dédupliquer les expériences et conserver les échecs informatifs. |
| R195 | P0 | BLOCKED | Évaluation aveugle des améliorations. Conserver un benchmark gelé inaccessible au générateur de variantes, avec cas inédits et critères de réussite. Refuser toute promotion qui régresse sur la sécurité, la stabilité, la reproductibilité ou le résultat artistique mesurable. |
| R196 | P1 | BLOCKED | Objectifs artistiques explicites. Transformer « forêt réaliste, nocturne, enneigée, torche » en critères observables : densité, silhouettes, variété, lisibilité du chemin, textures, budget triangles, temps image, cohérence visuelle. Garder les préférences subjectives comme décisions utilisateur, pas comme métriques inventées. |
| R197 | P1 | BLOCKED | Comparaisons A/B reproductibles. Pour chaque variante, enregistrer seed, paramètres, version Blender/Roblox, captures si possibles, métriques et différences ; ne pas déclarer une variante « plus belle » sur la seule opinion d'un modèle local. |
| R198 | P1 | BLOCKED | Préférences utilisateur comme contraintes. Permettre un retour simple (« trop plat », « trop clair », « trop répétitif ») ; transformer en hypothèses testables et mémoriser les choix, sans modifier automatiquement le jeu principal. |
| R199 | P0 | NOT_TESTED | Mémoire résistante à la corruption. Écriture atomique, snapshots, checksums, validation du schéma, détection de doublons, restauration sur copie et contrôle des liens Obsidian. Interdire la suppression automatique de notes personnelles. |
| R200 | P0 | NOT_TESTED | Contradictions et obsolescence. Ne pas écraser silencieusement une fiche : relier les versions, dater les sources, distinguer VERIFIED, HYPOTHESIS, REJECTED, STALE. Réévaluer lorsqu'une API ou une mesure change. |
| R201 | P1 | BLOCKED | Restauration Obsidian de bout en bout. Simuler fichier corrompu, conflit de nom, coupure pendant écriture et coffre indisponible. Vérifier qu'aucune note utilisateur n'est perdue et que les exportations reprennent sans doublon. |
| R202 | P0 | BLOCKED | Préflight Windows non destructif. Vérifier chemin, droits réels, espace disque, verrouillage session, veille, GPU, processus concurrents et ports. Décrire exactement les limitations de l'exécution en session verrouillée ou déconnectée ; ne pas modifier l'alimentation Windows sans accord. |
| R203 | P0 | NOT_TESTED | Aucune élévation silencieuse. Si permission, installation, pare-feu, secret, connexion à un compte ou planificateur Windows requiert l'utilisateur, suspendre cette opération, conserver le reste du service et générer UNE demande d'autorisation précise. Ne pas contourner les protections. |
| R204 | P0 | NOT_TESTED | Patchs autonomes à privilèges minimaux. Autoriser uniquement une liste explicite de fichiers/scripts non sensibles dans un worktree Git isolé. Refuser l'auto-modification des garde-fous, du superviseur, des permissions, de la politique d'approbation et des données du jeu principal. |
| R205 | P0 | BLOCKED | Pipeline de promotion strict. Un patch candidat doit passer formatage, typage si applicable, tests unitaires, intégration, scénarios de panne, benchmark gelé, contrôle de sécurité, test sur copie et sauvegarde. Promotion seulement si changement faible risque, réversible et explicitement préautorisé ; sinon préparer un dossier à approuver. |
| R206 | P0 | BLOCKED | Rollback automatique mesuré. Après promotion, canary limité et surveillance de métriques ; si seuil de régression franchi, revenir automatiquement à la dernière version saine, mettre le patch en quarantaine et créer un incident. |
| R207 | P0 | NOT_TESTED | Gestion de la dette technique. Maintenir un registre de correctifs candidats refusés, incompatibilités non résolues et interventions nécessitant autorisation. Ne pas répéter la même tentative indéfiniment ni cacher les erreurs derrière des retries. |
| R208 | P0 | BLOCKED | Huit scénarios d'acceptation obligatoires. Tester : (1) panne du réparateur ; (2) changement d'API Blender/Roblox simulé ; (3) MCP/Claude absent ; (4) modèle Ollama insuffisant ; (5) appréciation artistique ambiguë ; (6) corruption mémoire/Obsidian ; (7) refus de permission Windows ; (8) patch de code risqué. Pour chacun : preuve de diagnostic, comportement sûr, continuité partielle, récupération quand possible et escalade explicite quand nécessaire. |
| R209 | P0 | BLOCKED | Essai autonome et mesure. Exécuter une campagne locale bornée (30–60 minutes si ressources et temps disponibles), avec au moins une vraie recherche, une vraie écriture de fiche en coffre test, une expérience Python, une expérience Blender si installé et un test Studio si accessible. Produire chronologie, résultats, temps actif, consommation, incidents et preuve d'arrêt/reprise. Ne jamais simuler une intégration réelle pour valider le scénario. |
| R210 | P0 | NOT_TESTED | Livraison unique et décision honnête. Codex exécute lui-même les tests et fournit lanceur Windows, HEALTH_REPORT.md, REPAIR_BACKLOG.md, CODEX_HANDOFF.md, MORNING_BRIEF.md, résultats machine-readable et une matrice PASS / FAIL / BLOCKED / NOT_TESTED pour les exigences critiques. Afficher séparément « implémenté », « testé en simulation », « validé sur outils réels », « actif en autonomie ». Ne jamais annoncer « prêt à travailler toute la nuit » sans premier cycle réel, budget, autorisation et heartbeat vérifié. |
