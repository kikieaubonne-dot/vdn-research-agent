# Limites V8

- Aucun test dans Claude Desktop réel, Windows, Blender, Roblox Studio ou Player.
  Le transport stdio a été testé par un client JSON-RPC local en sous-processus.
- Les niveaux effectifs sont `documentee`, `a_verifier`, `contestee`. Les catégories
  `testee_localement` et `preuve_externe_inspectee` sont prévues dans le modèle,
  mais restent des **déclarations** non promues sans vérification indépendante.
  Aucun vérificateur externe ni workflow de validation humaine n'est implémenté.
- Les instructions sont extraites des sources ; leur ordre et leur complétude ne
  sont pas validés. Les anciennes notes ont parfois trop peu de contenu pour
  proposer une procédure. Le moteur montre ces lacunes au lieu de les combler.
- La détection de contradictions vise les contradictions signalées explicitement.
  La compatibilité est un diagnostic de portée des sources, pas une preuve.
- La recherche reste lexicale avec équivalences FR/EN. Deux petits corpus annotés
  par un seul ingénieur ne prouvent pas une généralisation universelle.
- Les filtres se limitent au domaine et au niveau diagnostique de preuve. Les
  plans explicites couvrent les arbres et forêts ; autres demandes : nœud unique.
- `plan_research` n'enfile ni n'exécute de recherche. La collecte reste dans les
  commandes V7 avec leurs budgets. Aucun outil V8 ne pilote Blender ou Roblox.
- Les rapports d'expérience ne sont pas indexés comme connaissances ; ils restent
  séparés, non vérifiés et ignorés par Git. Leur revue et sauvegarde relèvent du
  propriétaire. Le serveur ne lit aucune variable secrète pour les remplir.
- Les symlinks sont refusés, les fichiers limités à 2 Mo, les entrées MCP à
  262 144 caractères, les rapports à 64 Ko. La défense suppose un dossier local
  sous contrôle de l'utilisateur ; pas de garantie contre un autre processus
  hostile remplaçant des fichiers pendant la lecture.
- Une base SQLite déjà corrompue produit une erreur explicite. La reconstruction
  automatique avec archivage du cache corrompu n'est pas implémentée.
- L'indexation est transactionnelle côté SQLite, sans transaction globale entre
  les Markdown externes. Le rafraîchissement utilise taille/date ; conserver
  artificiellement ces métadonnées peut demander un redémarrage.
- Les anciennes limites V7 des commandes manuelles `research`/Ollama et de la
  persistance multi-fichiers restent documentées. Aucun auto-déploiement.
