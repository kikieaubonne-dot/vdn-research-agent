# VDN Research Agent V1 — 0 € / recherche programmée

## V11.2 — Project Intelligence

Bible du jeu, priorités/dépendances, fiches techniques, contrôle de préparation,
échecs liés et briefings Claude spécialisés. Collecte manuelle bornée ; dix
préparations partielles, aucune technique déclarée validée dans le jeu.

```sh
python -m agent.v112 bible
python -m agent.v112 plan
python -m agent.v112 brief "Corriger les collisions des sapins Roblox"
python -m agent.v112 daily
python vdn_mcp.py --v112
```

[Continuité, inventaire et validation terrain partielle](docs/v112/continuity/CONTINUITY_AUDIT.md) ·
[Rapport et limites](docs/V11_2_REPORT.md) · [Audit](docs/v112/AUDIT.md) ·
[Windows et MCP](docs/v112/GUIDE.md) · [Dix fiches et session réelle](docs/v112/RESEARCH.md) ·
[Mesures](docs/v112/BENCHMARK.md) · [Rollback](docs/v112/MIGRATION.md).

## V11.1 — Éponge Intelligence

Analyse des problèmes, passages localisés, registre d'affirmations, critique,
protocoles A/B et mémoire cumulative. Ollama facultatif, sans téléchargement
automatique ; citation attribuée et procédure proposée restent distinctes.

```sh
python -m agent.v111 diagnose
python -m agent.v111 synthesize "Mes sapins Roblox sont artificiels et bloquent le joueur"
python -m agent.v111 brief "Quelles priorités pour ma forêt Roblox ?"
python vdn_mcp.py --v111
```

[Rapport V11.1 et limites](docs/V11_1_REPORT.md) ·
[Windows/Ollama](docs/v111/WINDOWS_OLLAMA.md) ·
[MCP Claude](docs/v111/CLAUDE_MCP.md) ·
[Évaluation](docs/v111/BENCHMARK.md).

## V11 — L'Éponge Océan

V11 ajoute la planification forêt, la découverte de liens autorisés, des fiches
sourcées séparant faits et procédures proposées, une mémoire persistante,
22 outils MCP et un import de mesures Blender. Aucun modèle payant requis.
Les modes automatiques restent désactivés ; les candidats ne sont pas vérifiés.

```sh
python -m agent.v11 plan "Forêt enneigée nocturne Roblox avec collisions"
python -m agent.v11 brief "Pourquoi mon personnage se bloque contre les sapins ?"
python vdn_mcp.py --v11
python -m tests.offline
python -m tests.personal_config
```

[Rapport V11 et limites](docs/V11_REPORT.md) ·
[Installation Windows](docs/v11/WINDOWS.md) ·
[Claude Desktop](docs/v11/CLAUDE_MCP.md) ·
[Preuves Internet et Blender réelles](docs/v11/LIVE_VALIDATION.md) ·
[Benchmark V10/V11](docs/v11/BENCHMARK.md).

## V10 — recherche locale et mémoire d’expériences

V10 ajoute des sessions récursives bornées, un registre persistant des réussites
et échecs, des preuves hachées, un plan A/B pour le sapin et une analyse visuelle
manuelle avec adaptateurs IA optionnels. Aucun modèle ni API payante obligatoire.
Les modes automatiques V10 et le réseau sont désactivés par défaut.

```sh
python -m agent.v10 research-prepare "Comment reproduire un sapin enneigé photoréaliste dans Roblox ?"
python -m agent.v10 spruce --dry-run
python -m agent.v10 status
python vdn_mcp.py --v10
python -m tests.offline
```

Utiliser `--apply` pour une écriture explicite. Les mesures Studio restent
inconnues ; `SUCCESS` n’est pas `VERIFIED`. Aucun jeu n’a été exécuté en V10.
[Rapport V10](docs/V10_REPORT.md) · [Windows et autonomie](docs/v10/WINDOWS.md) ·
[Laboratoire et sapin](docs/v10/LAB.md) · [Obsidian et MCP](docs/v10/INTEGRATIONS.md) ·
[Sécurité](docs/v10/SECURITY.md) · [Benchmark](docs/v10/BENCHMARK.md)

## V9 — connaissances de production et coffre Obsidian sûr

V9 conserve V8 et ajoute inventaire des lacunes, quatre candidates officielles
Roblox, collecte ponctuelle bornée, export incrémental avec conflits/reprise et
briefing compact. Aucune tâche récurrente ni exécution graphique n'est activée.

```sh
python -m agent.v9 gaps
python -m agent.v9 brief "Comment poursuivre un joueur parmi des obstacles Roblox ?"
python -m agent.v9 sync --destination /chemin/separe/VDN-Obsidian
# Simulation par défaut ; vérifier le chemin et les conflits avant --apply.
python vdn_mcp.py --v9
```

Ouvrir `DESTINATION/knowledge` comme coffre. Les outils MCP V8 restent disponibles.
[Rapport V9](docs/V9_REPORT.md) · [Obsidian](docs/V9_OBSIDIAN.md) ·
[Windows](docs/V9_WINDOWS.md) · [Démonstrations](docs/V9_DEMOS.md) ·
[Mesures comparées](docs/V9_RAG_REPORT.md)

## V8 — moteur local de connaissances pour Claude

V8 réutilise les fiches et le SQLite existants : recherche FR/EN, lecture complète,
instructions candidates sourcées, plan hors ligne et retours d'expérience séparés.
Aucune dépendance pip, aucun service payant obligatoire et aucune exécution graphique.

```sh
python -m agent.local search "Pourquoi les os de mon squelette personnalisé bugguent-ils après importation dans Roblox ?"
python -m agent.local procedures "créer un sapin enneigé réaliste pour Roblox"
python -m agent.local plan "Je veux refaire entièrement la forêt enneigée de mon jeu d'horreur Roblox."
python vdn_mcp.py
python -m tests.offline
```

Le serveur MCP V8 utilise stdio, sans port réseau ; les écritures d'expérience
sont désactivées par défaut. Les commandes V7 et le serveur historique restent
disponibles. Le benchmark historique passe à hit@3 = 1,0 et MRR = 1,0 sur son petit
corpus ; ce résultat ne valide pas les techniques dans Roblox.

[Installation Windows](docs/WINDOWS_V8_SETUP.md) ·
[Claude Desktop/MCP](docs/CLAUDE_DESKTOP_V8.md) ·
[Rapport V8](docs/AUTONOMY_V8_REPORT.md) ·
[Benchmark](docs/AUTONOMY_V8_RAG_REPORT.md) ·
[Démonstrations](docs/demos/v8/README.md)

Agent de **veille et découverte** de ressources techniques Roblox/Blender pour *Le Voisin de Noël*. Python standard library uniquement. **Aucune clé API, aucun LLM, aucun abonnement requis.**

## Évolution V7 — recherche bornée et diagnostics de preuves

Les commandes du workflow existant restent utilisables. V7 renforce les budgets,
la conservation des fiches, les relances et leur classement explicable. Un premier
profil configurable décompose le cas du sapin enneigé avec ses prérequis :

```sh
python -m agent.run plan --topic spruce "Comment créer un sapin enneigé réaliste et performant dans Roblox ?"
python -m agent.run queue
python -m agent.run cycle
python -m agent.run evaluate
python bench/evaluate_v7.py --repo .
```

`plan` et `evaluate` ne font aucun appel réseau. `cycle` et `refresh` partagent
le quota HTTP quotidien de `config/autonomy.json`. Les diagnostics ne prouvent
pas l'exactitude d'une technique. Les commandes historiques `research`, `enrich`
et les appels directs aux fournisseurs restent des outils manuels ; utiliser
`cycle` pour la boucle autonome avec ses quotas persistants.

Voir [le rapport V7](docs/AUTONOMY_V7_REPORT.md),
[l'audit initial](docs/AUTONOMY_AUDIT.md) et
[la roadmap](docs/AUTONOMY_V7_ROADMAP.md).

## Ce que cette V1 fait vraiment

- Chaque session choisit les questions les moins explorées, pondérées par la priorité du sujet.
- Interroge **Roblox DevForum** et la recherche publique des **dépôts GitHub** (quand les services acceptent les requêtes).
- Déduplique par URL, attribue un **score de pertinence heuristique** et sauvegarde une fiche Markdown par découverte.
- Maintient un état `output/state.json` et un rapport `output/last_run.json`.
- Exécute une session toutes les heures via GitHub Actions, sous réserve de la disponibilité et des limites du service.
- Chaque fiche est explicitement marquée **à vérifier**. Le contenu des sources n'est pas traité comme une instruction.

**Ce qu'elle ne fait pas encore :** elle ne lit pas intégralement les pages, ne regarde pas de vidéos, ne raisonne pas avec un modèle IA, ne vérifie pas les méthodes en Roblox Studio et n'entraîne pas de modèle. C'est une base fiable de collecte et de mémoire, pas un chercheur autonome expert déjà abouti. Les sous-thèmes dans `config/topics.json` servent de feuille de route pour les futures versions ; la V1 ne génère pas encore de nouvelles requêtes récursivement.

## Installation GitHub (gratuite dans les limites applicables)

1. Créer un compte GitHub si nécessaire.
2. Créer un **dépôt privé** nommé `vdn-research-agent`.
3. Importer **le contenu du dossier** du ZIP à la racine du dépôt (y compris `.github/workflows/research.yml`). Le plus simple est `git` sur Windows :

   ```powershell
   git init
   git add .
   git commit -m "Initial VDN research agent"
   git branch -M main
   git remote add origin https://github.com/VOTRE_PSEUDO/vdn-research-agent.git
   git push -u origin main
   ```

   Si le dépôt distant a été créé avec un README, partir d'un dépôt vide évite les conflits.
4. Dans GitHub, aller à **Settings → Actions → General → Workflow permissions** et autoriser les permissions d'écriture nécessaires au `GITHUB_TOKEN` si l'organisation ou le dépôt les restreint. Le workflow demande `contents: write`.
5. Dans l'onglet **Actions**, activer les workflows si GitHub le demande, puis ouvrir **VDN Research Agent → Run workflow** pour le premier test.
6. Regarder `output/last_run.json` et `knowledge/` après l'exécution. Les erreurs HTTP (403, 429...) sont consignées ; elles ne signifient pas que les recherches ont réussi.

GitHub Actions sur un dépôt privé possède des quotas gratuits dépendant du type de compte et des règles en vigueur. Le cron peut être retardé, ignoré ou désactivé après une longue inactivité du dépôt. Vérifier les limites et la facturation dans les paramètres GitHub ; **ne pas activer de dépassement payant**. Les services interrogés ont également leurs propres limites et peuvent refuser les requêtes.

## Test local Windows

```powershell
py -3.12 -m unittest discover -s tests -v
py -3.12 -m agent.core --max-queries 3 --per-source 2
```

Python 3.12 conseillé ; aucune dépendance `pip`.

## Connexion Obsidian

La solution la plus simple : cloner ce dépôt sur le PC, puis dans Obsidian, **Open folder as vault** et sélectionner le dossier `knowledge` (ou copier/synchroniser son contenu vers un coffre existant). `git pull` récupère les nouvelles fiches. Un dépôt privé exige une authentification GitHub ; ne pas exposer de jeton dans les fichiers du dépôt.

## Personnalisation

Modifier `config/topics.json` pour ajouter des sujets, priorités et requêtes. `priority: 10` = prioritaire. Modifier `--max-queries 8` dans le workflow pour ajuster la consommation. Chaque requête entraîne jusqu'à **deux appels HTTP** (DevForum + GitHub), soit jusqu'à 16 appels pour 8 requêtes par session. Ne pas augmenter brutalement : les limites externes sont réelles. Le score reflète seulement la concordance des mots, **pas** la qualité ou la véracité.

## Roadmap

- **V1.1** : analyse des pages accessibles et extraction de procédures avec références, tout en respectant les règles des sites.
- **V1.2** : questions récursives contrôlées, tests de pertinence et file d'attente de sujets.
- **V2** : moteur IA optionnel (local Ollama sur un PC allumé, ou fournisseur disposant d'une offre gratuite), avec vérification des affirmations.
- **V3** : banc de test Blender/Roblox assisté, validation humaine et rapports de performance.

**Sécurité** : ne jamais exécuter automatiquement des scripts téléchargés depuis les résultats ; conserver les citations et vérifier manuellement avant d'appliquer des méthodes au projet.
