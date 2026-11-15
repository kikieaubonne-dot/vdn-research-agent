# VDN Research Agent — V5

Agent de recherche gratuit (0 € d'abonnement, 0 € d'API) qui remplit une bibliothèque Obsidian de techniques Roblox (rendu, forêt, neige, éclairage, parkour…) et la rend interrogeable par Claude via un petit serveur MCP en lecture seule.

## Ce que fait la V5

| Étape | Module | Rôle |
|---|---|---|
| Planification | `agent/planner.py` | Requêtes courtes (2–4 mots), rotation par priorité de sujet, relances issues des notes précédentes (au plus 1/4 des requêtes) |
| Sources | `agent/providers.py` | 1. Doc officielle Roblox (index `llms.txt`, ~2 400 pages) · 2. DevForum (sitemap, pas la recherche interdite par robots.txt) · 3. GitHub (API) · 4. SearXNG local (optionnel) |
| Filtrage | `agent/relevance.py` | Score sujet + technique, liste de bruit (portfolios, recrutement, simulateurs…), raisons de rejet écrites |
| Notes | `agent/knowledge.py` | 1 note par source/technique, frontmatter obligatoire, statuts, extraits cités avec source et date, dédoublonnage |
| Méta-recherche | `agent/meta.py` | Bandit UCB1 par fournisseur × sujet, récompense mesurée, retour arrière si une stratégie régresse, journal `output/meta_journal.jsonl` |
| Index + RAG | `agent/rag.py` | SQLite FTS5 (BM25), synonymes FR/EN, budget de tokens respecté |
| MCP | `agent/mcp_server.py` | `search_knowledge`, `read_knowledge`, `get_topic_index` — lecture seule |
| IA locale | `agent/llm.py` | Ollama **optionnel** ; toute affirmation doit citer un extrait, sinon elle est supprimée ; section marquée « non vérifiée » |
| Benchmark | `agent/benchmark.py` | Précision/rappel du filtre, hit@k/MRR du RAG, tokens, historique et détection de régression |

### Statuts des notes

`candidat` → `documenté` → `reproduit` → `validé`, plus `rejeté` et `obsolète`.
L'agent ne pose **jamais** `reproduit` ni `validé` : ces statuts demandent un essai réel dans Roblox Studio, à cocher à la main dans la note (champ `tested_in_studio`).

## Installation sous Windows

1. **Python 3.11 ou plus** : <https://www.python.org/downloads/> — cocher « Add python.exe to PATH ». Aucune bibliothèque à installer (bibliothèque standard uniquement).
2. **Git** : <https://git-scm.com/download/win>.
3. Récupérer le dépôt :
   ```powershell
   cd $HOME\Documents
   git clone https://github.com/kikieaubonne-dot/vdn-research-agent.git
   cd vdn-research-agent
   python -m unittest discover -s tests
   ```
   La dernière ligne doit afficher `OK`.
4. Construire l'index local :
   ```powershell
   python -m agent.run index
   python -m agent.run ask "feuillage transparent de loin"
   ```

### Optionnel : Ollama (analyse IA locale, PC allumé seulement)

```powershell
winget install Ollama.Ollama
ollama pull qwen2.5:7b-instruct
python -m agent.run enrich --max-notes 5
```
Variables possibles : `VDN_OLLAMA_URL` (défaut `http://localhost:11434`), `VDN_OLLAMA_MODEL`.
Si Ollama est éteint, la commande l'affiche et n'écrit rien : aucune analyse n'est simulée.

### Optionnel : SearXNG (méta-moteur local)

Si tu as un SearXNG sur ta machine (par exemple via Docker) : `setx VDN_SEARXNG_URL http://localhost:8888`. Seuls les liens vers la doc Roblox, le DevForum et GitHub sont gardés.

## Utilisation

| Commande | Effet |
|---|---|
| `python -m agent.run research` | Un cycle de recherche (8 requêtes par défaut) |
| `python -m agent.run refresh` | Recharge l'index de la doc officielle + quelques pages du sitemap DevForum |
| `python -m agent.run index` | Régénère les `_index.md` et la base SQLite |
| `python -m agent.run ask "question"` | Interroge la bibliothèque (ce que verra Claude) |
| `python -m agent.run bench` | Benchmark hors ligne ; `--online` pour les tests réseau |
| `python -m agent.run migrate` | Migration des anciennes notes (déjà faite ; relançable sans risque) |

Rapports produits : `output/last_run.json`, `output/meta_report.md`, `output/benchmark_report.md`, `output/rejected.jsonl` (chaque rejet avec sa raison).

## Fonctionnement PC éteint : GitHub Actions

Le workflow `.github/workflows/research.yml` tourne gratuitement sur GitHub :
- toutes les heures : tests → recherche → benchmark → commit des notes ;
- chaque nuit (3 h 23 UTC) : rafraîchissement des index de sources ;
- les tests passent **avant** toute écriture : si un test échoue, rien n'est commité.

Sur ton PC, un simple `git pull` récupère les nouvelles notes. Ollama, lui, ne tourne que quand le PC est allumé (`enrich`).

## Brancher Claude (MCP, lecture seule)

Dans Claude Desktop → Paramètres → Développeur → Modifier la config (`%APPDATA%\Claude\claude_desktop_config.json`) :

```json
{
  "mcpServers": {
    "vdn-knowledge": {
      "command": "python",
      "args": ["-m", "agent.mcp_server"],
      "cwd": "C:\\Users\\TON_NOM\\Documents\\vdn-research-agent",
      "env": { "VDN_ROOT": "C:\\Users\\TON_NOM\\Documents\\vdn-research-agent", "PYTHONUTF8": "1" }
    }
  }
}
```

Redémarre Claude Desktop. Outils disponibles :
- `search_knowledge(query, top_k=5, token_budget=1500)` : meilleurs passages, budget respecté ;
- `read_knowledge(note_id)` : une note complète (chemin confiné à `knowledge/`) ;
- `get_topic_index(topic)` : index d'une branche (ex. `vegetation`).

Le serveur n'écrit rien dans les notes ; il met seulement à jour sa base de recherche `output/knowledge.db` (reconstructible, ignorée par git).

## Obsidian

Ouvre le dossier `knowledge/` comme coffre, ou copie/lie-le dans ton coffre existant. Le point d'entrée est `knowledge/_index.md`, puis un `_index.md` par branche (`vegetation`, `forest`, `lighting`…), avec des liens `[[...]]`.

## Migration depuis la V4

La V5 a été appliquée **sans rien supprimer** :
- les 54 notes existantes gardent leur texte ; un frontmatter V5 et un bandeau « note migrée » ont été ajoutés en tête ;
- les anciens fichiers `output/state.json` et `meta_state.json` sont relus tels quels (anciens bras marqués « hérités ») ;
- l'ancien point d'entrée `python -m agent.core` existe toujours.

Pour revenir en arrière : `git revert` du commit V5.

## Limites connues

Voir `RAPPORT_TEST_V5.md`, section « Limites ».
