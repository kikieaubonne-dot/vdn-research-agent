# Livraison incrémentale — laboratoire et anticipation V11.2

**Résultat global PARTIEL**, PR #8 existante, base vérifiée
`89c53238ae2cea9765a95f064eb5b8a54704a89d`. Pas de nouvelle version/PR, fusion,
publication Roblox, installation de modèle ou service permanent. Le descriptif
de PR consigne les checks Ubuntu/Windows du commit final publié.

## FAIT

- Bible rev2 mise à jour à partir du récit explicitement fourni : Léo, Maëlle,
  policier, prologue/lobby/chapitre 1 et grenier PROPOSED. Les réponses confirmées
  ne disparaissent plus du briefing ; omissions et accès au détail sont signalés.
- Planificateur de 7 scènes /20 tâches, dépendances partagées et horizons A/B/C.
  Préparation et reprise via les sessions existantes, empreinte du catalogue,
  pas d'activation automatique ni de nouveau framework agentique.
- Routage des demandes de chapitre par les **27 contrats MCP existants**, avec
  permissions recherche/expériences/modèles séparées. Pages Obsidian réservées
  aux chapitres et exclues du RAG primaire.
- Filtrage des fiches rejetées dans Intelligence : 84 citations secondaires
  sorties du corpus actif, historique intact. Le RAG BM25 existant reste conservé.
- Alternatives de sources explicitement configurées, robots DevForum lisibles,
  extraction des posts JSON avec provenance/date/IDs et licence inconnue.
- Retour d'échec par les outils existants : hypothèses diagnostiques, requêtes
  ciblées, proposition d'essai et refus d'une répétition identique non justifiée.
  Aucun changement automatique de code/politique, réseau ou expérience.
- Description visuelle opérateur/Claude structurée, inférences et inconnues,
  références existantes et invalidation de cache ; aucune vision simulée comme réelle.
- Runner local d'une mesure Blender approuvée, contrôles version/échelle/input,
  identités liées, rapports/import/reprise, timeout/calcul/stockage bornés et
  capacité opérateur absente du MCP.

## Preuves et mesures

| Essai | Résultat vérifié |
|---|---|
| Référence 89c5323 | CI existante 420 +420 tests par OS confirmée |
| Nouveaux contrats | **40 tests OK**, avec cas négatifs et régressions rouges |
| Suite locale finale | **460 tests OK**, Linux Python 3.12.14 |
| Configuration personnelle isolée | **460 tests OK**, sockets toujours interdites |
| MCP | Reproduction de 7 processus réels + test stdio du plan de chapitre ; 27 schémas identiques |
| Benchmark RAG | 22 questions préannotées, même corpus ; rappel/MRR inchangés, rejetées supprimées des résultats actifs |
| Réseau réel isolé | 2 HTTP (robots/topic DevForum), 1 source capturée, Camera réutilisée en cache ; quotidien 24→26, 0 modèle, 0 note créée |
| Blender réel | 4.3.2, primitives A/B : 42/58 triangles, 2 objets et 1 matériau chacun ; rapports PARTIAL_SUCCESS |
| Version cible | Demande 5.2 bloquée sur le 4.3.2 installé, aucune compatibilité 5.2 annoncée |
| Mémoire/Obsidian | Échec synthétique propagé ; export isolé, second inchangé, rollback et RAG non contaminé |
| Préservation | 145 fichiers de données/config/source contrôlés hors SQLite dérivé ; 143 inchangés, seulement Bible JSON/Markdown changés volontairement, originaux sauvegardés |

Les anciens 99 IDs de fiches et 111 Markdown historiques restent inchangés. Le
runtime `output/queue.json` déjà modifié et le scratch préexistant sont conservés
hors commits. Les sources réelles antérieures et nouvelles, expériences et échecs
vivent dans des copies isolées ; pas de mutation du coffre personnel.

Le benchmark publie précision contre IDs listés, rappel, MRR/nDCG et latences brutes.
Il montre aussi que le RAG historique est meilleur qu'Intelligence sur ces labels.
Aucun gain sémantique, quota Claude, FPS ou qualité du jeu n'est déduit. Les modèles
et embeddings restent non exécutés, les catégories de preuve sont séparées.

## Défauts reproduits avant correction

- Rejetées réintroduites par Intelligence malgré le filtre RAG historique.
- Réponses confirmées de la Bible omises lors de la transmission.
- Requête robots DevForum refusée par la même allowlist qui devait permettre sa
  consultation. Seul le chemin exact robots.txt est ajouté ; pas de recherche/RSS.
- JSON de topic exposé brut plutôt que posts attribués.
- Sources Unreal/Blender incompatible présentes dans le nouveau briefing de chapitre.

Journaux rouges puis suites vertes sous [proofs](proofs/). Les défauts de nouveau
harnais/candidats d'URL ont été isolés avant l'essai réseau réussi, sans remise à
zéro ni contournement d'accès. Aucun résultat de fixture n'est publié comme moteur réel.

## PARTIEL / BLOQUÉ / NON TESTÉ

- **PARTIEL :** utilité de jeu, comparaison de méthodes, fraîcheur exhaustive,
  licences, paraphrases/indépendance des sources, autocorrection autonome. Le
  diagnostic est lexical et les recherches/essais suivants demandent une action
  explicite. Un score ou une hypothèse ne confirme pas une cause.
- **BLOQUÉ :** Studio et son plugin/transport réel, accès au PC utilisateur,
  scènes B3/C1/V2/contrôleur, test de la cible Blender 5.2. Les capacités Studio
  sont annoncées NOT_IMPLEMENTED, pas un pont fictif.
- **NON TESTÉ :** Claude Desktop effectif, modèles/embeddings/vision réels,
  rendus comparatifs, ouverture d'une vraie copie B3/C1 par le runner, multijoueur,
  télémétrie UX et réduction réelle des appels/quota Claude.

Aucune technique du jeu n'est promue READY/VERIFIED. La réussite du runner décrit
une collecte géométrique sur primitives, pas le sapin ou le jeu de l'utilisateur.
L'ancien protocole Studio et les scripts restent explicitement non exécutés ici.

## Fichiers principaux

`agent/chapters.py`, `failure_learning.py`, `lab_runner.py`, `visual_description.py` :
planification, diagnostic, exécution approuvée et fallback descriptif. Intégrations
ciblées dans project_api/work/research/recipes, v112 et mcp_v8 ; corrections dans
intelligence_evidence, ocean_web et providers. `project/bible.json`, BIBLE.md et
chapters.json : données utilisateur versionnées. `tests/test_lab_intelligence.py`
et fixtures figées nouvelles ; `bench/evaluate_lab_retrieval.py` : mesures.

Les rapports de continuité précédents restent des snapshots historiques ; les
nouveaux résultats sont dans ce dossier, sans réécrire leurs chiffres passés.
[Spécification complète](MASTER_SPEC.md) · [Matrice](CAPABILITY_MATRIX.md) ·
[Récit](PROJECT_STORY.md) · [Plan](CHAPTER_RESEARCH_PLAN.md) ·
[Sources](SOURCE_STRATEGY.md) · [RAG](RAG_QUALITY.md) ·
[Vision](VISUAL_PIPELINE.md) · [Laboratoire](AUTONOMOUS_LAB.md) ·
[Échecs](FAILURE_LEARNING.md) · [Claude](CLAUDE_MCP_WORKFLOW.md) ·
[Autonomie](AUTONOMY_OPERATIONS.md) · [Windows](WINDOWS_SETUP.md) ·
[Suite et rollback](NEXT_STEPS.md).
