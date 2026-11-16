# Recherche et bibliothèque opérationnelle — V11.2

**Livraison PARTIELLE**, continuation de la PR #8, branche
`codex/project-intelligence-v11-2`. État initial vérifié :
`ad2fc6b6e211ccb686052273221cb35f26e30bf6`, PR ouverte vers
`codex/eponge-intelligence-v11-1`. Aucune fusion, nouvelle PR/version, modification
Studio, installation de modèle, publication ou tâche permanente.

La livraison améliore une chaîne documentaire utilisable par Claude. Elle ne
valide aucune technique sur B3/C1 et ne construit pas une intelligence universelle.

## Audit et continuité

Les rapports de [continuité](../continuity/CONTINUITY_AUDIT.md),
[validation](../continuity/VALIDATION_V112.md),
[suite](../continuity/NEXT_ACTIONS.md),
[handoff](../continuity/CLAUDE_HANDOFF.md) et les
[livrables suivants](../autonomous/IMPLEMENTATION_REPORT.md) ont été confrontés
aux modules, tests et captures présents. Les anciens rapports sont des snapshots
historiques ; leurs chiffres ne sont pas réécrits.

La CI initiale **43922540522**, associée à `ad2fc6b`, est réussie sur Ubuntu et
Windows : 460 tests hors ligne +460 dans une configuration personnelle isolée
par OS. Les 27 contrats MCP, les 84 citations rejetées exclues, les 22 questions,
la planification par chapitre et la mémoire des échecs sont présents. Les anciens
2 HTTP DevForum/cache et Blender 4.3.2 sur primitives sont des preuves antérieures,
pas des essais exécutés à nouveau. PC Windows utilisateur, Claude Desktop,
Blender 5.2 et Roblox Studio restent NON TESTÉS ici.

| Capacité | État initial / actuel | Code et preuve | Limites / décision |
|---|---|---|---|
| File, reprise, dépendances, quotas persistants | EXISTANT / TESTÉ | research_session, research_queue ; tests historiques et nouveaux arrêts tick/session | Conserver ; acquis documentaire terminal ≠ technique validée |
| Recherche récursive ciblée | PARTIEL / TESTÉ | research_roots, catalogue 24 branches ; scénarios 1–9 | Catalogue humain ; pas de génération ouverte de nouvelles branches |
| Lacunes et profondeur adaptative | PARTIEL / TESTÉ | assess/plan ; IDs, priorités, dépendances, limites et arrêts | Correspondance de concepts explicite, pas compréhension sémantique démontrée |
| Pertinence et absence de résultat | À CORRIGER / TESTÉ | rag SQL ; regression rouge avant correction | Les archives pouvaient saturer LIMIT avant filtrage |
| Bibliothèque principale/réserve/archives | PARTIEL / TESTÉ | research_library ; 32/25/42 notes ; scénarios 11–14 | Vues sans déplacement ; MAIN n’est pas une preuve originale |
| Déduplication | EXISTANT / PARTIEL | identités URL/SHA ; groupes d’extraits exacts avec alias | Pas de fusion automatique de paraphrases ou de sources dépendantes |
| RAG lexical et expansion par branche | EXISTANT / TESTÉ | 22 questions conservées +12 complémentaires figées | Amélioration descriptive sur petit jeu ; latence supérieure, premier essai régressif conservé |
| Sémantique/hybride | EXISTANT / NON TESTÉ réel | adaptateurs conservés | Pas de backend réellement sélectionné ; pas de gain annoncé |
| Provenance/citations/paramètres | EXISTANT / TESTÉ mécanique | intelligence_evidence, project_work ; hash, offsets, versions, injections | Une citation exacte ne prouve ni une causalité ni une compatibilité moteur |
| Synthèse déterministe/Ollama | EXISTANT / PARTIEL | tests historiques ; aucun appel modèle ajouté | Ollama réel non exécuté ; détail par branche déterministe |
| Critique/contradictions | EXISTANT / PARTIEL | vérificateur historique conservé | Détection explicite/lexicale, pas arbitre sémantique universel |
| Échecs, cache, propositions alternatives | EXISTANT / TESTÉ logiciel | LabStore, failure_learning +liaison branches ; scénario 9/MCP20 | Rapport synthétique séparé ; aucune promotion automatique |
| Collecte multisource bornée | EXISTANT / TESTÉ partiel | OceanWeb inchangé ; parcours réel 1 HTTP +cache | Seeds et liens autorisés ; pas de moteur Web général ni de contournement |
| Collecte accessible mais incomplète | À CORRIGER dans le nouveau parcours / TESTÉ | regression rouge puis PARTIAL, reçu de portée épuisée | Erreurs réelles conservées ; aucune preuve inventée pour terminer |
| YouTube/transcriptions/Reddit | ABSENT collecte spécialisée | Aucun nouveau collecteur | Reporter ; aucune transcription ou licence inventée |
| Scènes et Bible | EXISTANT / TESTÉ | 7 scènes/20 tâches conservées ; liens partagés Obsidian | Intentions confirmées/propositions conservées, pas d’état du jeu inspecté |
| MCP/permissions | EXISTANT / TESTÉ | 27 schémas identiques ; vrai processus stdio | Desktop réel NON TESTÉ ; permissions d’écriture existantes inchangées |
| Obsidian/rollback | EXISTANT / TESTÉ isolé | scénario 19 : export, inchangé, rollback | Coffre personnel non consulté/modifié |
| Windows/Linux/Python3.11 | EXISTANT / CI | workflow existant, résultats par SHA dans PR et CI.md | CI Windows ≠ fonctionnement sur PC utilisateur |
| Laboratoire moteur | EXISTANT / hors périmètre | Aucun nouveau code Blender/Studio | Pas d’essai B3/C1, de modification distante ou de validation 5.2 |

## Architecture réellement ajoutée

- `project/research_roots.json` : **24** questions techniques organisées, dont la
  micro-branche `forest/spruce/foliage/cards/alpha/shadows/flashlight`. Objectifs,
  concepts requis, importance, dépendances, requêtes et liens vers tâches existantes.
  Deux inspirations artistiques restent PROPOSED, sans sources techniques affirmées.
- `agent/research_roots.py` : plan limité (6 niveaux/24 nœuds par défaut,
  plafonds configurables 8/32), lacunes stables, ordonnancement des prérequis,
  arrêt des branches peu prioritaires ou du périmètre déjà exploré. Un contexte
  parent ne ferme jamais les questions des enfants. Six unités maximum par
  préparation, dans le moteur V10 existant ; aucune hausse de quotas réseau/calcul.
- Les reçus `lab/ocean/roots/` conservent les évaluations et la portée examinée.
  Empreinte des sources/versions/conditions/expiration, Bible, configuration,
  catalogue et révisions d’expériences. Une collecte partielle accessible reste
  PARTIAL ; un reçu évite une répétition identique automatique. Un changement
  pertinent invalide le reçu sans effacer les anciennes révisions.
- `agent/research_library.py` : vues MAIN/RESERVE/ARCHIVE et fusion de deux requêtes
  lexicales au maximum pour un contexte de branche explicite/inféré. Les candidates
  restent visibles sans résultat MAIN. Les rejets restent archivés et exclus.
  Un corps de note normalisé exact peut avoir plusieurs alias et sources. Les valeurs,
  versions, conditions et niveaux différents ne sont pas fusionnés.
- `ProjectAPI` expose ce parcours par `plan_ocean`, `prepare/run/control_ocean`,
  `get_intelligence_brief`, `synthesize_technical`, `ocean_status` et les outils
  d’expérience existants. Le préfixe `tree:` demande une branche précise. Les
  questions de chapitre gardent leur routage. Le RAG historique reste disponible.
- Pages Obsidian `_VDN-Library-*` et `_VDN-Research-Roots` : liens vers notes
  originales et scènes, même ID de technique pour plusieurs scènes. Elles restent
  exclues du corpus primaire ; aucune autocitation de synthèse comme preuve.

## Défauts démontrés et corrections

1. **Faux résultat vide** : 210 notes rejetées pouvaient masquer une candidate
   car LIMIT 200 précédait le filtrage. Statut/domaine sont maintenant filtrés
   dans les requêtes SQL FTS et de repli, avec paramètres liés. L’archive explicite
   reste accessible. [Test rouge](proofs/filter-before.log).
2. **Diagnostic du nouveau collecteur** : la capture réelle DevForum contenait
   des fenêtres de contexte incomplètes. Leur insuffisance était transformée en
   erreur d’intégration. La régression reproduit le défaut puis vérifie PARTIAL,
   zéro nouvelle erreur d’intégration, lacunes visibles et réutilisation.
   [Test rouge](proofs/partial-before.log). Un provider facultatif désactivé est
   signalé comme avertissement ; une véritable erreur de collecte reste explicite.

Les quatre régressions historiques `tests/test_v112_continuity.py` sont conservées
et passent. Aucun composant stable n’a été réécrit pour changer d’architecture.

3. **Déduplication du nouveau parcours** : deux aperçus de 700 caractères identiques
   pouvaient masquer des paramètres différents dans la suite du texte. La clé
   compare désormais le corps complet et ses conditions/version ; une régression
   conserve les deux variantes. [Test rouge](proofs/dedup-before.log).

4. **Détail de branche incomplet** : le premier détail exposait les offsets mais
   pas le texte original à consulter. Il fournit désormais les passages bornés,
   empreintes, contexte et limites depuis le même snapshot ; le test vérifie le
   texte de référence attendu. [Régression](proofs/detail-before.log).

## Résultats reproductibles

- **490 tests OK** sous Linux/Python 3.12.14, sockets interdits jusque dans les
  sous-processus ; configuration personnelle isolée validée séparément. Résultats
  CI par SHA dans [CI.md](CI.md) et dans la PR ; aucun succès anticipé.
- **20 scénarios : 15 PASS, 5 PARTIAL, 0 FAIL**. Les cinq recherches initiales sans
  originaux suffisants restent PARTIAL, même avec des candidates pertinentes.
  [Entrées, attentes, résultats, sources, durées](SCENARIOS.md).
- MCP stdio réel : Bible → plan → briefing court → détail ; l’échec synthétique
  est retrouvé lors de la consultation suivante ; 27 contrats inchangés. Ce test
  ne lance pas Claude Desktop.
- Obsidian isolé : simulation, export commis, deuxième export inchangé, rollback
  réussi, notes sources et compteur quotidien préservés.
- **146/146 fichiers protégés identiques**, dont 111 Markdown/99 IDs historiques,
  Bible, préparations, config et runtime initial. `output/queue.json` déjà modifié
  et `work/` préexistant restent hors commit. SQLite dérivé peut être réindexé.

### RAG : progrès mesuré et régression

Sur les **22 questions historiques**, rappel/MRR et IDs retournés sont inchangés :
coverage Recall@5 = 0,977273 ; MRR = 0,916667. Pas de nouveau gain annoncé sur ce jeu.

La comparaison suivante porte sur le composant `Library.search(query, branch)`,
pas sur la qualité d’une réponse Claude complète. Les briefings utilisent aussi
des requêtes normalisées par nœud ; leur utilité terrain reste à mesurer.

Sur les **12 questions complémentaires**, annotations de sujets/sources figées
avant développement du retrieval, jeu séparé mais pas holdout aveugle :

| Stratégie | Recall@5 | P@5 contre labels listés | MRR | nDCG@5 | Couverture | Latence moyenne observée |
|---|---:|---:|---:|---:|---:|---:|
| Historique coverage | 0,791667 | 0,216667 | 0,669444 | 0,677683 | 11/12 | 0,0251 s |
| Fusion avec branche inférée | 0,875000 | 0,250000 | 0,783333 | 0,761622 | 12/12 | 0,4553 s |
| Fusion avec branche fournie | 0,916667 | 0,266667 | 0,833333 | 0,806331 | 12/12 | 0,5110 s |

Une première mesure avant correction des aperçus fusionnés régressait sur `roots-7`
(sol enneigé). Le test indépendant des paramètres tronqués a révélé la cause :
l’aperçu commun fusionnait des notes distinctes. La correction du texte complet
supprime cette régression sur ce jeu, sans changer requêtes/labels/poids. La
première mesure brute reste publiée pour comparaison. Latence supérieure, zéro résultat
vide dans les trois stratégies et zéro doublon d’ID dans le top5. Les annotations
ne sont pas exhaustives : P@5 indique les seuls IDs listés, pas une vérité complète
de pertinence. Sur les 12 cas, P@5 utilise le dénominateur fixe5 ; le benchmark
historique22 conserve sa définition contre les résultats effectivement retournés.
Ces deux jeux ne doivent pas être comparés comme une seule série. La branche fournie utilise une information supplémentaire et n’est
pas assimilée au routage inféré. Aucun réglage postérieur aux scores n’a été ajouté
pour améliorer artificiellement ces cas. Pas de preuve statistique ni d’économie
Claude ; le moteur historique n’est pas remplacé globalement.

[Résultats bruts : 22 avant](proofs/baseline22.json) · [22 après](proofs/after22.json) ·
[12 premier essai](proofs/metrics12-initial.json) · [12 final](proofs/metrics12-final.json).

### Réseau réel et reprise, séparés des fixtures

[Étude initiale](proofs/network-initial.json) : copie d’un runtime déjà autorisé,
compteurs quotidiens **HTTP 26→27**, **fetch 21→23** ; 1 HTTP contenu DevForum,
robots déjà en cache, 1 cache officiel, 2 tentatives de collecte. Nouvelle session
limitée à 2 HTTP (réduction locale, jamais hausse/remise à zéro). Une nouvelle
capture, sept posts reçus de `https://devforum.roblox.com/t/3171224` ; SHA et offsets
vérifiés, version/licence inconnues, date 2024-09-24, thread non exhaustif.

Un document nouveau correspond mécaniquement à la branche atlas/feuillage. Les
fenêtres de passage sont incomplètes : **zéro nouvelle connaissance vérifiée**,
pas de recommandation technique déduite de la seule correspondance lexicale.
L’erreur initialement mal classée est conservée comme historique.

[Reprise du même ID](proofs/network-resume.json), après correction : PARTIAL,
acquisition terminale COMPLETE, **0 HTTP supplémentaire**, deux lectures cache,
aucune nouvelle erreur. HTTP reste 27, fetch 23→25 ; les fetch comptent aussi
les tentatives utilisant le cache. Le compteur historique d’une erreur reste à 1.
Le plan suivant garde la lacune ouverte mais arrête cette portée déjà examinée ;
il faut examiner les limites, élargir explicitement les sources ou modifier une
hypothèse justifiée. Aucun nouveau modèle ou test moteur.

## Limites et prochaine étape

La décomposition est un catalogue spécialisé avec heuristiques explicables. Elle
n’invente pas de nouvelles micro-branches depuis Internet. Les équivalences de
paraphrases, contradictions sémantiques, licences, compatibilités Studio et
techniques suffisamment documentées pour le jeu restent partielles. La réserve
préserve les pistes ; elle ne les transforme pas en faits ni en VERIFIED.

Aucun accès au PC utilisateur, Claude Desktop ou Studio ; pas d’essai B3/C1,
pas d’optimisation FPS démontrée, modèle/embedding réel non exécuté. Le parcours
logiciel est opérationnel ; son bénéfice dans le jeu exige encore un essai humain.

Prochaine action : sur le PC Windows, démarrer le MCP en lecture seule, demander
`tree:forest/collisions`, consulter les références et les limites, puis adapter
le [protocole existant](../continuity/ROBLOX_TEST_PROTOCOL.md) aux copies B3/C1 et
au contrôleur réel. Relever build, conditions, observations et preuve avant
l’enregistrement. [Commandes et rollback](WINDOWS.md) · [Architecture](ARCHITECTURE.md).

## Fichiers de cette livraison

- `agent/rag.py` : filtre SQL avant plafonnement.
- `agent/research_library.py`, `agent/research_roots.py` : vues, retrieval par branche,
  arbre/lacunes, reçus et exécution bornée.
- `agent/project_api.py`, `agent/project_work.py`, `agent/v112.py` : MCP existant,
  export réservé et commandes CLI.
- `project/research_roots.json` : catalogue technique ; Bible/chapitres/préparations
  historiques inchangés.
- `tests/test_research_roots.py`, `tests/fixtures/roots_project/` : 30 nouveaux tests
  et fixtures figées ; anciennes suites inchangées.
- `bench/evaluate_roots.py`, `bench/roots_evaluation.json`, `bench/acquire_roots.py`,
  `bench/validate_research_roots.py` : comparaison, étude autorisée et 20 scénarios.
- `README.md`, `docs/v112/research/` : guides, audit et preuves de cette mission.

Les empreintes du code testé, journaux, données brutes et contrôle de préservation
sont sous [proofs](proofs/). Le scratch et le runtime préexistants restent hors commit.

La couverture est mesurée sur les seuls labels fournis. Le faux rejet de candidate
est reproduit dans un cas adversarial (candidate masquée avant /retrouvée après),
mais aucun taux global de faux rejet en production n’est estimé faute d’annotations
exhaustives. De même, le regroupement de doublons exacts est prouvé sur des fixtures ;
aucune réduction artificielle du nombre de notes historiques n’est revendiquée.
