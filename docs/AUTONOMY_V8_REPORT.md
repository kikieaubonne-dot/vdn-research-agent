# V7.5 → V8 : moteur local de connaissances — livraison

Date : **16 novembre 2026**. Départ V7 : `f5cb699`, branche
`codex/autonomy-v7`, PR #1 non fusionnée. Branche V8 :
`codex/knowledge-engine-v8`. Corpus de référence : `9abf775`, **106 fichiers**.

## Résultat démontré

Un programme local reçoit une demande technique Roblox, recherche les fiches,
présente leurs sources et leurs limites, extrait des instructions candidates et
prépare un plan de recherche hors ligne. Les mêmes fonctions sont accessibles
par Python, CLI JSON et MCP stdio. Aucun logiciel graphique n'est piloté.

**218 tests passent**, dont les 177 tests V7 et **41 nouveaux**, avec les
connexions socket interdites dans le processus de test **et ses sous-processus**.
Les 106 fichiers de `knowledge/` sont inchangés par SHA-256 ; aucune modification
des fiches, des notes Obsidian, du workflow ou des données de recherche `output/`.

## Phase A — audit indépendant et corrections bloquantes

L'[audit V8](AUTONOMY_V8_AUDIT.md) confronte les quatre commits de la PR #1,
le rapport/roadmap V7, les modules et les tests. Il reproduit les 177 tests et
le classement RAG dégradé du corpus `9abf775`, sans recherche réseau.

Cinq défauts supplémentaires ont été reproduits contre un checkout V7 inchangé :
**3 échecs et 2 erreurs sur 5**, puis cinq tests réussis après correction.

| Défaut | Correction et validation |
|---|---|
| Message MCP JSON non objet : arrêt du serveur | Erreur JSON-RPC puis poursuite ; test direct et sous-processus |
| Paramètres MCP convertis au lieu d'être validés, dont booléen pour top_k | Types, bornes, champs obligatoires et inconnus contrôlés |
| Index général symlink lisible hors bibliothèque | Résolution et refus des symlinks/chemins sortants, y compris les chemins venant de SQLite |
| Premier passage dépassant un très petit budget | En-tête et texte comptés ; aucun passage si le budget ne suffit pas |
| Une note corrompue bloquant tout l'index | Scan par note, diagnostics et exclusion ciblée ; originaux conservés |

Un contrôle supplémentaire refuse les budgets de durée NaN/infini passés directement
au cycle. La version V7 acceptait NaN (reproduction isolée conservée dans les logs) ;
la nouvelle validation précède toute écriture. Le prévisionnel respecte aussi une
profondeur maximale configurée à zéro.

Le scan refuse aussi les identités dupliquées, fichiers non UTF-8 et métadonnées
incohérentes. La mise à jour SQLite ferme la connexion et annule les modifications
si une interruption survient. Un test vérifie le rollback puis la reprise.

## Phases B à E — architecture et capacités

```text
Claude / CLI
  → MCP stdio ou API KnowledgeEngine
  → SQLite FTS5 existant (rag) + sélection de portée Roblox
  → Markdown lu sous knowledge/ + diagnostics de preuves
  → JSON structuré avec sources, limites, prérequis et instructions candidates
```

| Couche | Implémentation |
|---|---|
| Acquisition | Modules V7 conservés ; aucune acquisition dans les outils V8 |
| Lecture du corpus | `corpus.py`, lecture bornée et diagnostics sans réécriture |
| Index/recherche | SQLite FTS5 existant, mêmes identifiants et index incrémental |
| Normalisation/classement | `retrieval.py` + `rag.py`, groupes bilingues équilibrés et couverture explicable |
| Sélection et preuves | `engine.py` + évaluateur V7, score textuel séparé des déclarations de fiabilité |
| Procédures | Extracteur d'actions V7 réutilisé, preuves et ordre non vérifiés visibles |
| Plans | Fonction pure `decomposition.describe` partagée avec le planificateur persistant |
| Interface | `agent.local`, `agent.mcp_v8`, script absolu `vdn_mcp.py` |
| Retours d'expérience | JSON distincts + journal sous `experiments/`, activation explicite, idempotence |

### Recherche et sélection

Le score textuel n'est pas une preuve technique. L'API fournit identifiant, titre,
passage, rang explicable, chemin, sources, date/version, niveau diagnostique,
compatibilité et incertitudes. `get_knowledge` renvoie le Markdown complet sous
la limite de taille de lecture, sans modifier l'original.

Les demandes mentionnant Roblox privilégient les sources de portée Roblox,
à pertinence recherchée dans les candidats récupérés. Les autres moteurs restent
accessibles et sont signalés. La démo Babylon.js précédemment bien classée pour
la forêt porte désormais `other_engine`, avec besoin de portage ; elle n'est pas
présentée comme prête à l'emploi dans Roblox. Cette portée n'est pas une validation.

La classification effective distingue documentation structurée, contenu à vérifier
et contradiction signalée. Les statuts de test local et preuve externe déclarés
sont conservés séparément et ne sont jamais promus automatiquement.

### Procédures et plans

`find_procedures` retourne les actions extraites, prérequis, paramètres et limites,
les références de chaque instruction et les vérifications restantes. Si les
sources ne permettent pas une procédure, la sortie indique `insufficient_evidence`.
Une procédure issue d'un autre moteur indique `requires_porting`.

`plan_research` réutilise les profils et leurs prérequis, avec un nouveau profil
forêt : terrain, implantation, arbres, matériaux, neige, éclairage, performances,
export, collisions, vent, audio. Les références sont recherchées par branche.
Prérequis manquants et prérequis non vérifiés restent distincts. La file n'est
jamais ouverte ou modifiée par ce prévisionnel, même si son JSON est corrompu.
Les limites de profondeur et de nombre de nœuds sont reprises de V7.

### Expériences

`report_experiment` est refusé tant que l'hôte n'a pas activé les écritures.
Il enregistre tâche, résultat, paramètres, environnement, observations et IDs
de référence ; aucun environnement local ni secret n'est automatiquement collecté.
L'UUID explicite permet la reprise idempotente et refuse un contenu différent.
Une interruption entre rapport et journal conserve le rapport ; la répétition
répare le journal. Les tests le reproduisent.

Ces observations restent `unverified_report`, `truth_verified: false` et
`promotes_knowledge: false`. Elles ne sont pas automatiquement réindexées comme
connaissances et ne changent aucune fiche historique.

## Phase C — amélioration mesurée du RAG

Voir [le rapport détaillé](AUTONOMY_V8_RAG_REPORT.md) et
[les mesures brutes](AUTONOMY_V8_RAG_METRICS.json).

| Corpus historique, 10 requêtes FR/EN | V7 | V8 |
|---|---:|---:|
| Hit@1 | 0,9 | 1,0 |
| Hit@3 | 0,9 | 1,0 |
| Hit@5 | 1,0 | 1,0 |
| MRR | 0,925 | 1,0 |
| Négatifs historiques propres | oui | oui |

Le petit jeu de développement distinct passe de hit@3 11/12 à 12/12 et MRR
0,822 à 0,847, avec hit@1 inchangé à 9/12. Quatre variantes ont été comparées.
Aucune exception spéciale n'est codée pour la requête du squelette. Le benchmark
historique n'est pas modifié. Aucun score ne prouve la vérité des techniques.

La latence brute médiane passe d'environ 4,25 à 6,16 ms ; l'index incrémental
médian de 17,61 à 32,38 ms sur cinq essais. Ce surcoût des contrôles et du
classement est documenté, sans annonce de gain de vitesse.

## Phase F — démonstrations

Les [trois entrées et sorties](demos/v8/README.md) sont générées depuis le vrai
corpus sur copie temporaire, puis comparées octet par octet dans un test.

- **Sapin** : sources SurfaceAppearance, LOD et atlas retrouvées ; onze branches
  relient matériaux, géométrie, neige, export et performances, en conservant les lacunes.
- **Squelette** : fiche Custom Rig / RootPart / Bone Glitches première pour la
  question naturelle ; les sources ne sont pas présentées comme une correction prouvée.
- **Forêt** : onze sous-problèmes avec ordre de construction et références
  complémentaires. La sortie dit explicitement qu'aucune forêt n'a été construite.

## Phases G et H — état des fonctionnalités

| Fonctionnalité | État |
|---|---|
| Recherche FR/EN, filtres, sources et limites | Implémentée et testée hors ligne |
| Lecture complète, sécurité des chemins, corpus absent/partiellement corrompu | Implémentée et testée |
| Extraction d'instructions, prérequis et compatibilité | Implémentée et testée comme diagnostic ; vérité technique non établie |
| Plans sans réseau et sans changement de file | Implémentés et testés |
| Rapports isolés, idempotence, interruption et journal | Implémentés et testés |
| MCP initialize/list/call, erreurs, stdio et lancement absolu | Implémentés et testés en processus réel |
| Installation Windows / Claude Desktop | Documentée, non testée dans ces applications réelles |
| Niveaux test local / preuve externe inspectée | Déclarations séparées ; vérification et promotion partiellement implémentées |
| Contradictions sémantiques générales | Non implémentées ; seuls signalements explicites détectés |
| Pilotage Blender/Roblox et reconstruction graphique | Non implémentés |

Exécution finale : `python -m tests.offline`, **218 tests, zéro échec**.
Le harnais interdit les connexions dans les sous-processus par `sitecustomize`.
Les traces initiales, cinq défauts reproduits et exécution finale sont conservés
sous `docs/validation/v8/`. Les tests incluent l'API, la CLI et le serveur stdio,
la non-régression RAG, les faux statuts validés, les chemins trafiqués, les notes
illisibles/dupliquées, les expériences et la reproductibilité des démonstrations.

## Livraison et limites

[Installation Windows](WINDOWS_V8_SETUP.md), [intégration MCP](CLAUDE_DESKTOP_V8.md),
[limitations détaillées](AUTONOMY_V8_LIMITATIONS.md), [roadmap V9](AUTONOMY_V9_ROADMAP.md).
Le workflow existant et les budgets V7 sont préservés, sans nouveau service payant
ou dépendance pip. La [PR V8 #2](https://github.com/kikieaubonne-dot/vdn-research-agent/pull/2)
est ouverte au-dessus de `codex/autonomy-v7`, pour isoler la revue V8. La PR #1
reste ouverte ; aucune PR n'a été fusionnée et aucun auto-merge n'est activé.
