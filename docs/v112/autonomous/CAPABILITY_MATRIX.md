# Capacités — laboratoire supervisé V11.2

Référence de départ 89c5323, PR #8 conservée. Les preuves historiques restent
consultables sous `../continuity/`. Les niveaux portent sur le code et les accès
réels, pas sur une promesse de réussite du jeu.

| Capacité | Implémentation | État / preuve | Limite |
|---|---|---|---|
| RAG lexical | rag, retrieval, engine | FAIT, benchmark 22 questions et tests historiques | Labels de développement limités |
| Exclusion des rejetées | intelligence_evidence.documents | FAIT après test rouge ; 84 extraits rejetés retirés | Notes et raisons conservées, accès explicite possible |
| Déduplication | documents, research_queue, ocean_knowledge | FAIT pour URL/SHA/identité ; différences de versions gardées | Paraphrases et indépendance sémantique PARTIELLES |
| Bible narrative | project/bible.json rev2, chapters.json | FAIT, intentions utilisateur et propositions séparées | Implémentation du jeu non inspectée |
| Anticipation A/B/C | chapters.plan, ProjectResearch | FAIT : scènes, tâches, dépendances, préparation bornée | Pas de progression du jeu détectée automatiquement |
| Brief chapitre via MCP | ProjectAPI, get_intelligence_brief/plan_ocean | FAIT dans de vrais processus stdio, 27 contrats conservés | Claude Desktop non accessible |
| Recherche multisource | OceanWeb + source_candidates opt-in | FAIT : chemins officiels et alternatives bornés ; DevForum JSON réel capturé | Un forum ne prouve pas une méthode ni une licence |
| Vidéo/transcription | Sources existantes et import humain futur | NON IMPLÉMENTÉ pour acquisition automatique | Aucun titre/page vidéo présenté comme transcription |
| Versions/fraîcheur | SHA/TTL/config/Bible/expériences | PARTIEL, contrôles mécaniques et refus de version | Pas de suivi exhaustif release notes/API dépréciées |
| Citations/critique | intelligence_evidence, intelligence | FAIT pour attribution mécanique | Pas de preuve sémantique ou de vérité moteur |
| Ollama/hybride | adaptateurs V11.1 conservés | PARTIEL : contrats testés ; aucun modèle réel sélectionné | Pas de recommandation de modèle, de téléchargement ou de gain annoncé |
| Description visuelle | visual_description, project_visual | FAIT pour description opérateur/Claude structurée et références | Analyse multimodale réelle NON TESTÉE |
| Retour d'échec | LabStore, failure_learning, ProjectAPI | FAIT : hypothèses, requêtes ciblées, garde de répétition | Diagnostic causal et correction automatique PARTIELS |
| Laboratoire Blender | lab_runner, script de mesure approuvé | FAIT sur primitives réelles Blender 4.3.2 | 5.2 BLOQUÉ ici ; copies B3/C1 NON TESTÉES |
| Mesure d'une copie .blend | job borné, hash/échelle/version, autoexec désactivé | PARTIEL, validation des entrées et import testés | Pas d'asset réel disponible ; pas un bac à sable formel |
| Rendu/export/édition automatique | Non exposés par le runner | NON IMPLÉMENTÉ dans le nouveau runner | Script arbitraire et publication refusés |
| Pont Studio | Ancien collecteur et import, architecture documentée | BLOQUÉ : aucun Studio/plugin local disponible | Pas de serveur ou contrôle Studio fictif |
| Expériences et preuves | LabStore/imports/artefacts | FAIT, journaux et état PARTIAL_SUCCESS | Rapport client ≠ VERIFIED ; revue humaine séparée |
| Obsidian | sync transactionnel, pages chapitres réservées | FAIT : index humain et rollback ; résumés exclus du RAG | Coffre personnel non modifié |
| Travail nocturne | sessions V10, pause/reprise, limites persistantes | FAIT pour l'exécution bornée existante | Aucun service permanent/schedule activé |
| Réduction quota Claude | Benchmark ancien et nouveau | NON MESURÉE | Caractères, métriques RAG ou tests ne prouvent pas ce gain |

Acceptation : niveau 1 PARTIEL (MCP opérationnel, utilité de jeu non mesurée),
niveau 2 FAIT pour planification/préparation logicielle, niveau 3 PARTIEL pour
Blender seulement, niveau 4 PARTIEL et supervisé, niveau 5 NON TESTÉ.
