# Continuité V11.2 — 16 novembre 2026

Mission poursuivie sur PR #8, sans nouvelle version. Référence retrouvée :
`72f1b9c6887ee62ef75470d7b9a8f35d127c9b1f`, branche
`codex/project-intelligence-v11-2`, destination `codex/eponge-intelligence-v11-1`.
PR #7 toujours ouverte sur d23aafa, base V11 04a3c4c ; PR #8 ouverte, non fusionnée.
Le run 43865177113 du commit de référence est confirmé réussi.

Modification préexistante : `output/queue.json`, et scratch non suivi `work/`.
Ils sont conservés hors commits. Une empreinte a été prise sur **146 fichiers**
existants knowledge/config/output/project/runtime avant cette mission. Les essais
emploient de nouvelles copies isolées ; le précédent laboratoire est lu, pas modifié.
Aucun AGENTS.md trouvé dans le dépôt ou ses parents autorisés. Le nouvel inventaire
analyse les 67 modules agent, leurs définitions et imports, et distingue les IDs
par type ; voir [INVENTORY](INVENTORY.md) et son JSON.

Environnement accessible : Linux, Python 3.12.14. La CI utilise Python 3.11.
Le bureau distant déclaré par l'environnement est celui du cloud ; il ne donne
pas accès au PC Windows utilisateur. Aucun Windows attaché, Claude Desktop,
Roblox Studio, fichier .rbxl/.rbxm/.blend B3/C1, lampe V2 ou contrôleur dans le dépôt.
Aucun accès à d'autres conversations n'est supposé.

## Cartographie et niveau de preuve

Les imports/définitions exacts de tous les modules sont dans `inventory.json`.
Cette table indique les responsabilités, dépendances et frontières réellement vérifiées.
« Testé » signifie contrat logiciel testé, jamais résultat moteur implicite.

| Capacité | Modules / dépendances | État constaté et preuves | Limites |
|---|---|---|---|
| Collecte historique, planification, rotation | core, run, planner, discovery, providers, topics/config | Implémentée, tests historiques | Ordonnanceurs non activés ; vieux profils conservés |
| File/depth/dépendances | decomposition, research_queue, followup_rules | Implémentée et testée hors ligne | Décomposition par règles, pas compréhension générale |
| Sessions/checkpoints/budgets | research_session, budget, autonomy.Lock, storage | Implémentée, tests interruption/reprise et CI | Pas de nouvelle collecte pendant cette mission |
| Web Océan | ocean, ocean_web, providers, ocean_plan | Implémentée, captures réelles de la mission précédente | Robots/404/proxy/quotas conservés ; pas de nouvelle visite |
| Pertinence/déduplication | relevance, corpus, text, ocean_knowledge | Implémentée, tests et corpus local | Pas de jugement humain exhaustif de pertinence |
| RAG lexical | rag, engine, knowledge, text.BM25 | Implémentée et testée sur 99 fiches | 42 notes sont rejetées ; citation secondaire ≠ original |
| Recherche sémantique/hybride | ocean_semantic, intelligence_semantic | Implémentée, validation partielle par fixtures | Aucun embedding réel exécuté ici |
| Intention/attribution | intelligence_evidence, intelligence | Implémentée et testée ; offsets/SHA d'un original réel contrôlés | Mécanique, pas preuve d'implication sémantique |
| Synthèse/critique/contradictions | intelligence, ocean_knowledge | Implémentée, tests adversariaux | Contradictions explicites seulement ; procédés proposés |
| Ollama/routage/matériel | intelligence_models, models, hardware | Implémentée, partiellement validée par fixtures | Aucun modèle réel sollicité, installé ou recommandé |
| Bible/arbre/priorités | project, project/bible.json | Implémentée, tests ; Bible récupérée par vrai stdio | Priorités proposées ; scénario bêta inconnu |
| Fiches/recettes/readiness | project_work, project_quality, project_recipes | Implémentée, quatre défauts de lecture reproduits puis corrigés | Aucune technique de jeu READY |
| Mémoire d'expériences | lab_store, lab_plan, lab_mcp | Implémentée ; échec synthétique propagé par vrai stdio | Aucun résultat réel B3/C1 importé ; revue opérateur séparée |
| Protocole/import Studio | lab_import, roblox/VDNLabCollector.client.luau | Import testé par fixtures, collecteur présent | Collecteur non exécuté dans Studio ; Heartbeat ≠ FPS rendu |
| Mesures Blender | ocean_lab, scripts/blender_ocean_measure.py | Historique réel Blender 4.3 documenté, conservé | Ne valide ni Blender 5.2 ni B3/C1 |
| Références visuelles | visual, project_visual, LabStore | Association et intégrité testées | Pas d'analyse multimodale réelle |
| Obsidian | obsidian, gaps, ocean_api.pages, lab_plan.pages | Export réel isolé, second export inchangé, rollback réussi | Coffre personnel non accessible, non modifié |
| MCP/CLI | mcp_v8, *_api, lab_mcp, v10/v11/v111/v112 | Vrais processus stdio, 27 outils, contrats historiques conservés | Claude Desktop non accessible ; gain Claude non mesuré |
| Sécurité et confidentialité | safe_path, corpus, providers, schémas, capacités hôte | Tests symlinks/SSRF/injections/bornes | Aucun modèle ou document n'obtient shell/Git/édition du jeu |
| Autonomie | V10 sessions et contrôles existants | Implémentée, bornée et testée | Aucun service permanent lancé |

Présent uniquement comme proposition/documentation : paramètres optimaux du jeu,
procédures B3/C1/lampe après inspection, objectifs appareils/FPS. Non implémenté :
édition/exécution automatique Roblox via ces outils, entraînement des poids,
analyse vidéo sans contenu accessible, vérification sémantique formelle, audit
systématique des licences. Ces absences ne justifient pas une nouvelle architecture.
Les anciens modes MCP/CLI sont conservés comme interfaces historiques, pas supprimés.

## Liaisons effectivement vérifiées

| Liaison | Vérification | Frontière |
|---|---|---|
| Claude → MCP | Requêtes reproduites via stdio | Interface Desktop non testée |
| MCP → mémoire/Bible/fiche | initialize, liste 27, appels réels | Sources absentes donnent abstention |
| Recherche → preuves | Captures originales antérieures relues et SHA/offsets contrôlés | Aucun nouvel HTTP |
| Preuves → synthèse → Claude | Fiche collisions et détail par stdio | Procédure ENGINEERING_PROPOSAL |
| Claude → Blender/Roblox | Protocole et instructions fournis | Non exécuté, assets absents |
| Expérience → mémoire → MCP | Échec explicitement synthétique via outils existants | Aucune promotion VERIFIED |
| Mémoire → Obsidian | Export privé explicitement demandé dans une copie, RAG inchangé, rollback | Pas de coffre personnel |

## Écarts confirmés et corrections minimales

Quatre tests rouges sont conservés dans `regressions-before.log` :
1. L'archive sans originaux renvoyait une abstention fausse malgré `facts=[]`.
2. Ses paramètres restaient présentés comme documentés après retrait des faits.
3. Un nouvel échec local n'invalidait pas une archive publiée sans carte privée.
4. Le détail d'une prévisualisation recalculée pointait vers une clé non sauvegardée.

Correction uniquement dans `agent/project_work.py` : attribution disponible explicite,
paramètres archivés séparés des paramètres revalidés, comparaison des révisions
expérimentales de l'archive et route de détail `synthesize_technical` pour une
prévisualisation non persistée. Les fichiers archivés ne sont pas modifiés.
Aucun outil ajouté, aucune permission élargie, aucune écriture implicite du briefing.

L'ancien rapport disait « 110 notes historiques » : ce nombre désigne des Markdown,
avec leurs index. Le détail exact est 98 fiches +12 pages de structure avant V11,
puis 99 +12 à partir de V11. Le nombre de fichiers ne mesure pas leur qualité.

Un échec conserve un blocage de préparation conservateur. Une nouvelle expérience
avec conditions différentes peut être PLANNED, ce qui a été vérifié. Cela ne résout
pas automatiquement l'échec précédent ni ne rend la nouvelle méthode READY.

Le nouveau contexte utilisateur rapporte forêt jouable → sapins/sol/collisions →
lampe → caméra/mouvements → extérieur manoir → maison → intérieurs. Il est retenu
pour les prochaines actions, sans le transformer en scénario de bêta confirmé.
La Bible existante et ses empreintes historiques ne sont pas réécrites pour cela.
