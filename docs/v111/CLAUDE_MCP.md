# Claude Desktop — mémoire et critique

Exemple `claude_desktop_config.json`, chemins à adapter :

```json
{"mcpServers":{"eponge":{"command":"C:\\Users\\kikie\\Documents\\vdn-research-agent\\.venv\\Scripts\\python.exe","args":["C:\\Users\\kikie\\Documents\\vdn-research-agent\\vdn_mcp.py","--root","C:\\Users\\kikie\\Documents\\vdn-research-agent","--v111"],"env":{"PYTHONUTF8":"1"}}}}
```

27 outils : les 22 V11 et `synthesize_technical`, `get_intelligence_analysis`,
`get_intelligence_brief`, `search_intelligence`, `diagnose_intelligence`.
Les modes historiques ne changent pas : `--v11` expose toujours 22 outils.
Le test lance réellement le processus stdio depuis un autre répertoire et
vérifie initialize, tools/list et tools/call sous protocole 2025-06-18.
Claude Desktop lui-même n'était pas disponible pour un test d'interface.

Lecture seule par défaut. Ajouter `--allow-intelligence` pour autoriser
`apply=true`, probes et générations demandées explicitement ; `--allow-research`
et `--allow-experiments` restent deux autorisations distinctes. Aucun outil
d'édition du jeu, de shell ou de publication n'est ajouté.

```json
{"question":"Mes arbres Roblox sont artificiels, leurs collisions gênent le joueur et le rendu de nuit manque de réalisme","token_budget":1800}
```

Le briefing contient diagnostic provisoire, faits attribués, inférences,
propositions, expériences, échecs, priorités, incertitudes et références.
Demander `get_intelligence_analysis` avec la clé pour les passages, offsets,
contrôles et critiques complets. Pour une analyse conservée :

```json
{"question":"Pourquoi le joueur accroche-t-il les branches Roblox ?","apply":true,"allow_model":true,"retrieval":"lexical"}
```

La génération exige aussi le modèle activé/configuré et les budgets. Un échec
conserve un résultat déterministe ; un journal interrompu reste explicitement
incomplet. Consulter `search_intelligence` pour les analyses et échecs modèles.
Les rapports d'expériences sont ceux de LabStore : utiliser les outils existants
pour préparer, démarrer et signaler FAILED/PARTIAL_SUCCESS/SUCCESS avec preuves.
L'analyse suivante retrouve ces résultats, sans promotion VERIFIED.

Instructions de projet recommandées : consulter le briefing avant les choix
techniques, lire la critique et les conditions, distinguer source originale et
note secondaire, préparer une comparaison contrôlée et obtenir les permissions
dans les outils qui modifient effectivement le projet. L'Éponge ne force pas
Claude à la consulter et aucun temps gagné dans Desktop n'a été mesuré.
