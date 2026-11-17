# Audit différentiel V11 — environnements séparés

| Capacité | État réel | Preuve / limite |
|---|---|---|
| Bibliothèque, Bible r3,36 ressources et J0–J3 | VALIDÉE DANS UN ENVIRONNEMENT LIMITÉ | Héritage17937ba ; scénarios Python Linux, aucune partie Studio jouée |
| Animation IK,2proxies,25poses,2s | VALIDÉE DANS UN ENVIRONNEMENT LIMITÉ | Preuves V10 Blender4.3.2/GLB, interop-2 ; aucun retargeting/FBX/Roblox |
| Pack Windows, scripts MCP, candidats Luau A–E | PRÉPARÉE MAIS NON TESTÉE SUR LA CIBLE | Commandes et fichiers présents ; tests du vérificateur Linux, aucun Windows utilisateur |
|27contrats MCP, lecture directe de branche, échecs récents | VALIDÉE DANS UN ENVIRONNEMENT LIMITÉ | Vrais processus stdio Linux ; ce n'est pas Claude Desktop |
| Arbre forêt, lacunes et sessions réutilisables | PARTIELLEMENT FONCTIONNELLE | Catalogue28nœuds ; un chemin ciblé exécuté, profondeur bornée ; aucune couverture globale démontrée |
| Collecte Internet réelle | PARTIELLEMENT FONCTIONNELLE |4nouveauxHTTP au total ;1du worker puis3de diagnostic/correction dirigés par Codex, pas recherche exhaustive |
| Sapin enneigé | VALIDÉE DANS UN ENVIRONNEMENT LIMITÉ |2proxies propres, géométrie/matériaux GLB ; réalisme INCONCLUSIVE, B3/C1/vent/FPS NON TESTÉS |
| Correction autonome | PARTIELLEMENT FONCTIONNELLE | Sélection d'une alternative prédéfinie ; correction du protocole et du collecteur par Codex, pas auto-modification du runtime |
| Autonomie | VALIDÉE DANS UN ENVIRONNEMENT LIMITÉ, INACTIVE | Un cycle worker/guard réel de30,27s, puis arrêté ; aucune nuit autonome ni installation permanente |
| RAG et économie Claude | PARTIEL / NON MESURÉ | Récupération ciblée oui ; aucun nouveau gain Recall/MRR ou benchmark A/B Claude mesuré |
| Multimodal | PRÉPARÉ / LIMITÉ | Pipeline vidéo hérité ; pas de compréhension visuelle locale réelle ni YouTube validé |
| Windows utilisateur, Desktop, Studio, Blender5.2 | BLOQUÉ DANS CET ENVIRONNEMENT | Cloud Linux uniquement ; pas de connexion au PC personnel |

Les critères des laboratoires sont distincts : A logiciel = suites et intégrité ; B Blender = mesures de source/export/réimport ; C Studio = import/retargeting et parcours A–E réels ; D Desktop = interface et outils réellement consultés ; E multimodal = procédure extraite puis reproduite face à une référence indépendante ; F autonomie = heartbeat, cycle autorisé, budgets, mémoire et arrêt. A et certains scénarios B/F passent ici. C/D et la compréhension visuelle E restent non exécutés. Aucun laboratoire n'est universellement validé.
