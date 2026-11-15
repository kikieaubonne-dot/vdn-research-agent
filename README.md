# VDN Research Agent V1 — 0 € / recherche programmée

Agent de **veille et découverte** de ressources techniques Roblox/Blender pour *Le Voisin de Noël*. Python standard library uniquement. **Aucune clé API, aucun LLM, aucun abonnement requis.**

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

## V2 — Analyse technique partielle, sans API payante

Après la collecte, le workflow exécute `python -m agent.analyzer --max-notes 4`.
Il lit les premières publications publiques des sujets DevForum via leur endpoint JSON
et les métadonnées publiques des dépôts GitHub via l'API officielle. Il ajoute une section
**Analyse V2** aux fiches Markdown, avec des passages techniques repérés, des questions
à approfondir et les limites de vérification. Les pages ne sont **pas** exécutées et
leur texte est traité comme une donnée non fiable.

**Limites honnêtes :** cette V2 n'est pas une IA de raisonnement et ne fait pas de
fine-tuning ; elle ne vérifie pas les techniques dans Roblox, ne lit pas toutes les
réponses d'un long fil, ne résume pas automatiquement les vidéos et ne garantit pas
une analyse complète. Les quotas gratuits GitHub/DevForum et les politiques d'accès
peuvent bloquer des requêtes. Les fiches restent non validées jusqu'à un test réel.

### Installation V2 sur le dépôt existant

Copier uniquement les nouveaux fichiers `agent/analyzer.py`, `tests/test_analyzer.py`,
le `README.md` mis à jour et `.github/workflows/research.yml` dans le dossier du dépôt
cloné, en conservant `knowledge/` et `output/` déjà présents. **Ne pas écraser les
fiches ni la mémoire déjà produites.** Dans GitHub Desktop, faire Commit puis Push.
Le prochain lancement dans Actions déclenchera l'enrichissement. Une fiche analysée
contiendra la section `## Analyse V2`.
