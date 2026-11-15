# Audit initial V7 — 16 novembre 2026

Dépôt inspecté avant modification : `728235577c27deeb274195fc3534feffa8537afe`.
Ce document était absent. Aucun AGENTS.md trouvé. Baseline : **134 tests passent**,
`python -m unittest discover -s tests -v`, sans réseau ni service payant.

## Capacités effectivement présentes

| Composant | Observation dans le code et les tests | Défaut / limite |
|---|---|---|
| `run.research`, `providers` | Recherche docs Roblox, sitemap DevForum, GitHub ; fixtures réseau locales | Lectures échouées exclues du compteur ; retries HTTP non bornés par cycle ; durée contrôlée entre recherches seulement |
| `research_queue` | File persistante, historique, profondeur 2, 3 tentatives, déduplication inter-sujets par tokens | Ce n'est pas une déduplication sémantique complète : les stopwords effacent des facettes ; récupération déclenchée même en lecture de statut |
| `autonomy.cycle` | Verrou, reprise, limites journalières, relances, indexation en fin de cycle | Quota journalier compté après traitement ; lectures restantes non transmises ; verrou JSON partiel considéré périmé |
| `recursive_gaps`, `followup_rules` | Lacunes des fiches et sources rejetées déclenchant des questions | Suffixes longs tronqués par le planificateur ; plafond appliqué par fiche, pas par recherche ; pas de stagnation de branche |
| `planner`, `meta` | Requêtes courtes, UCB déterministe et retour arrière de stratégies | Priorité de file héritée du sujet, sans dépendances ni réévaluation des lacunes ; récompense heuristique, pas une validation technique |
| `knowledge` | Une fiche par URL canonique, extraits sourcés, statuts prudents, historique conservé | Écritures Markdown directes ; crash avant sauvegarde du registre pouvant dupliquer/réécrire une source ; registre dérivé fragile |
| `procedure`, `structure`, `relevance` | Extraction conservatrice action + objet, paramètres et API | Aucune preuve de vérité technique ni test Studio ; alternatives/prérequis souvent vides ; contradictions intersources non analysées |
| `rag`, `mcp_server` | SQLite/FTS local, récupération FR/EN avec budget de contexte | Pertinence lexicale, pas de graphe explicite des prérequis |
| `llm` | Ollama facultatif, références d'extraits et chiffres contrôlés | Grounding lexical insuffisant pour prouver une affirmation ; non activé dans cette mission |
| tests et bench | 134 tests, 54 cas de pertinence, 10 requêtes RAG | Couverture nominale utile mais garde-fous incomplets aux frontières et interruptions |

## Baseline mesurée sur une copie temporaire

`benchmark.run` hors ligne : précision pertinence **0,667**, rappel **0,889**,
F1 **0,762** (4 faux positifs, 1 faux négatif), RAG hit@1 **0,9**, hit@3 **1,0**,
MRR **0,933**, négatifs propres **1,0**, planificateur conforme.
Ces métriques ne mesurent pas la vérité des connaissances. 100 fichiers de
`knowledge/` sont inventoriés par SHA-256 avant travaux.

## Priorités d'ingénierie

- **P0** : respecter les quotas pendant chaque recherche, compter les tentatives
  avant l'effet réseau, conserver le budget après interruption ; empêcher la
  reprise concurrente via un verrou partiellement écrit ; protéger les notes et
  reconstruire leur registre après crash ; préserver les archives corrompues.
- **P1** : relances courtes ciblées, plafond global par parent, stagnation,
  décomposition déterministe configurable et prérequis, classement explicable,
  évaluation de complétude/traçabilité sans verdict de vérité automatique.
- **P2/P3** : étendre les domaines et le corpus annoté ; validation Studio/Blender,
  contradictions sémantiques, calibration des stratégies sur davantage de preuves.

## GitHub Actions

Workflow existant conservé : cron horaire + rafraîchissement quotidien,
`contents: write`, sérialisation `cancel-in-progress: false`, timeout 25 minutes,
cycle configuré 1 200 secondes. Les tests sont locaux, le benchmark non bloquant.
Le workflow publie les données collectées dans sa branche courante ; aucune
modification automatique de code ni aucun déploiement de code ne sont ajoutés.
Le rafraîchissement séparé n'a pas de budget journalier partagé dans la baseline.
Le contrôle anti-secret existant et les secrets ne sont pas modifiés.
