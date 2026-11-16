# V11.2 — Project Intelligence

**Livraison fonctionnelle partielle** : chaîne de préparation du projet utilisable,
aucune technique du jeu déclarée validée. Base exacte PR #7, d23aafa, nouvelle
branche `codex/project-intelligence-v11-2`, [PR #8](https://github.com/kikieaubonne-dot/vdn-research-agent/pull/8) vers
`codex/eponge-intelligence-v11-1`. Aucune fusion, tâche permanente, installation
de modèle, publication Roblox ou modification du jeu.

## Résultat réellement implémenté

L'Éponge conserve son moteur V10/V11/V11.1 et ajoute un contexte de projet
persistant : Bible avec statuts humains, treize tâches spécialisées, dépendances
et priorités proposées, dix fiches issues d'une session réelle bornée, protocoles
comparatifs et briefings compacts pour les 27 outils MCP existants. Les décisions
narratives, assets réels et versions manquantes restent inconnus.

Pipeline : Bible → identité/intention de tâche → requêtes/ancres spécifiques →
RAG lexical sur originaux et citations secondaires distinguées → synthèse
Intelligence déterministe ou Ollama explicitement autorisé → attribution et
critique mécanique → recette de laboratoire → contrôle qualité et readiness →
carte immuable, mémoire et invalidation → Obsidian et MCP. La recherche acquisition
ne traite que les lacunes avec les sessions/budgets/locks existants.

L'[audit détaillé](v112/AUDIT.md) examine les modules réels et les preuves de
29 capacités. Huit défauts historiques/admission/classement ont une régression
rouge avant correction : URL secondaire, contexte dépassé, propriété modèle mal
citée, moteur Unreal masqué, abstention perdue, sélection avant pondération,
snapshots identiques et type JSON corrompu. S'ajoutent des défauts d'intégration
nouvelle testés avant correction : complétude trompeuse, version explicite perdue,
import visuel après plafond et lecture de fiche périmée après source/échec changé.

## Fichiers et responsabilités

- `project/bible.json`, `project/BIBLE.md` : vision/contexte rapportés, prototypes,
  questions, priorités, arbre ; aucune invention de décisions.
- `project/prepared.json` : archive secondaire des dix préparations publiables.
- `agent/project.py` : validation de Bible, identité de tâche, ordre des
  dépendances, contraintes utilisateur et vue des budgets en lecture seule.
- `agent/project_work.py` : synthèse, empreintes/relecture, cartes/checkpoints,
  brief, pack de trois à cinq tâches, rapport manuel et pages réservées.
- `agent/project_recipes.py`, `project_quality.py` : étapes concrètes par tâche,
  quinze rubriques, critères explicables, états de preuve, échecs et validation
  opérateur liée à la recette/asset/build.
- `agent/project_research.py`, `project_visual.py` : collecte bornée des lacunes,
  pause/reprise et références visuelles manuelles sans analyse fictive.
- `agent/project_api.py`, `v112.py`, `mcp_v8.py` : spécialisation explicite des
  interfaces ; 27 outils et schémas conservés, modes historiques inchangés.
- `agent/intelligence.py`, `intelligence_evidence.py` : corrections ciblées de
  citations/claims/classement/abstention, contexte et version de vérificateur.
- `bench/evaluate_project.py`, `research_project.py` : comparaison exacte V11.1
  et session isolée manuelle ; résultats bruts distincts des fixtures.
- `tests/test_project.py`, `test_v112_regressions.py`, `fixtures/project/`,
  `personal_config.py` : 47 tests ajoutés et copie de configuration projet isolée.
- `README.md`, cette documentation et `docs/validation/v112/` : usages/preuves.

Le diff de PR est l'inventaire exhaustif des fichiers. Aucune dépendance externe
Python ajoutée ; Python 3.11 conservé. Configurations historiques inchangées.

## Validation et mesures

- Base : **369 tests OK** avant modification.
- Linux local : **416 tests OK**, puis **416 tests OK** en configuration personnelle
  autorisant le réseau dans une copie jetable, sockets toujours interdites.
- MCP : vrai stdio initialisation/liste/appels, contrats des 27 outils inchangés.
- Chaîne contrôlée jusqu'à Obsidian/RAG/MCP, reprise après interruption et rollback.
- CI Ubuntu **et Windows**, Python 3.11 : **416 + 416 tests OK par OS**,
  [run 43864474558](https://github.com/kikieaubonne-dot/vdn-research-agent/actions/runs/43864474558),
  code validé `1d33e84`, [extraits des journaux](v112/ci.json). Aucun Internet
  Windows, modèle ou moteur exécuté par ces suites hors ligne.
- **36/36 contrats synthétiques**, attribution mécanique 100 % sur ces contrats.
- Benchmark déterministe réel capturé, sept tâches, **identité 7/7** ; **36,9 % de
  caractères JSON en moins** sur ces sorties, sans économie de quota Claude prouvée.
- Internet réel : **10 HTTP/12, 8 ticks, 13 tentatives**, six documents nouvellement
  capturés, trois 404, un robots ; compteur existant 14→24, pas de remise à zéro.
- Préservation : **142 fichiers contrôlés, aucun manquant ni modifié**.

Voir [benchmark et compromis](v112/BENCHMARK.md), [session réelle et dix fiches](v112/RESEARCH.md),
[journaux](validation/v112), [empreintes](v112/preservation.json).
Le workflow historique à deux OS et deux scénarios est conservé sans le modifier.

## Limites et prochaines décisions

Aucune fiche READY : quatre PARTIAL, six BLOCKED. Les originaux cités ne prouvent
pas la recette ni le résultat sur B3/C1. Studio/build, appareils/performance et
plusieurs choix narratifs sont inconnus. Les heuristiques de pertinence/citation
ne démontrent pas l'implication sémantique. Contradictions limitées aux motifs
explicites ; lien distant non revérifié pendant le contrôle qualité hors ligne.
Documents partiels, 404 et échecs sont visibles et conservés.

Pas d'exécution Ollama/embeddings réelle, Blender 5.2, Roblox Studio, comparaison
visuelle ou Claude Desktop dans cette mission. Le cache Blender 5.3 est incompatible
avec la cible 5.2 et n'est pas une validation. Aucun modèle recommandé par défaut.
Le code Ollama robuste de V11.1 est réutilisé avec fallback déterministe testé
par transport simulé, pas une preuve de qualité IA réelle.

Une grande question multi-thèmes peut nécessiter plusieurs fiches ou une
clarification ; ce mode est spécialisé sur le jeu, pas un assistant universel.
Les succès du benchmark mécanique ne constituent pas un jugement humain d'utilité.
La session est terminée pour l'acquisition, **partielle pour la préparation**,
avec deux unités failed et cinq erreurs historiques conservées. Une fiche publiée
secondaire requiert de vrais snapshots locaux pour revalider ses faits.

Question décisive à confirmer dans la Bible : **quelle séquence doit être jouable
en premier dans la bêta ?** Les recherches indépendantes n'attendent pas cette
réponse ; les procédures et priorités d'implémentation qui en dépendent restent
bloquées. Le personnage jouable, motivation, solo/coop, casting et appareils sont
également enregistrés comme questions, sans réponse inventée.

## Guides et retour arrière

[Windows, diagnostic PowerShell, synthèse/recherche, MCP Claude, Ollama et Obsidian](v112/GUIDE.md) ·
[Sélection de modèles, pas de recommandation sans mesure](v111/MODELS.md) ·
[Migration et rollback](v112/MIGRATION.md) · [Bible](../project/BIBLE.md).
Les opérations manuelles sont explicites ; rien ne tourne en permanence. Arrêter
le mode `--v112` et revenir à `--v111` suffit au rollback fonctionnel, en conservant
toutes les nouvelles preuves et tous les compteurs.

## Validation de continuité complémentaire

La [mission de continuité](v112/continuity/CONTINUITY_AUDIT.md) distingue
99 fiches de 111 Markdown, contrôle 146 fichiers préexistants et corrige quatre
défauts de lecture d'archive/détail après régressions rouges. Les suites locales
passent à 420 tests par scénario. Voir [résultats et frontières](v112/continuity/VALIDATION_V112.md),
[instructions Claude/Windows](v112/continuity/CLAUDE_HANDOFF.md) et
[protocoles collisions/sapins/lampe](v112/continuity/ROBLOX_TEST_PROTOCOL.md).
Les résultats CI du commit publié sont consignés dans la PR #8 existante.
Aucun résultat Studio, B3/C1 ou Claude Desktop n'est revendiqué.
