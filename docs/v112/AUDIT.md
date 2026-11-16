# Audit du code V7 → V11.1, base d23aafa

Le code local correspond à PR #7, `d23aafa6a190ff69d951730dd39566ed3e33f7a0`.
Les 369 tests de la base ont été reproduits avant modification. Le compteur
runtime local de diagnostic était déjà modifié ; il a été conservé, pas restauré.
Une empreinte des 142 fichiers de connaissances, configurations et runtime
présents a été conservée avant les changements. Les essais nouveaux utilisent
des copies isolées. Aucun modèle, tâche permanente ou jeu n'est installé/lancé.

Les verdicts portent sur les contrats observables. **OK ne signifie pas utilité
en production démontrée.** Les tests simulant transport, modèle ou mesure ne
sont pas des exécutions Internet, Ollama, Blender ou Roblox réelles.

| Fonction attendue | Implémentation examinée | Preuve existante | Limites constatées | Verdict | Action |
|---|---|---|---|---|---|
| Planifier et décomposer | `planner`, `decomposition`, `ocean_plan.describe` | Tests de plans V7/V10/Océan | Profils/règles, pas compréhension générale ; priorités sans Bible | PARTIEL | Spécialiser le projet sans réécrire les profils |
| File, dépendances, priorité | `research_queue.add/next_batch/blocked_by` | Cycles, quotas, anti-doublons historiques | Dépendance de recherche distincte du prérequis de production | OK | Conserver, exposer les deux notions |
| Recherche récursive | `research_session.run`, `followup_rules` | Profondeur/stagnation/reprise | Relances lexicales ; une file terminale n'est pas une tâche validée | PARTIEL | Conserver les bornes, distinguer état de préparation |
| Découverte et collecte | `ocean_web.discover/get`, `providers.http_get` | HTTP réel V11/V11.1 + fixtures | Domaines/seeds limités, accès refusé possible ; pas de transcription vidéo | PARTIEL | Recherches de lacunes ciblées |
| Résultats partiels avant erreur | `ocean.Collector`, `ResearchSessions.last_collection`, résumé par tick | Test création puis erreur V11 | Dernière unité ≠ tick ; preuve déjà écrite à conserver | OK | Conserver et tester la nouvelle intégration |
| Robots, redirections, retries | `ocean_web.robots/_fetch`, `CheckedRedirect` | Refus 403/429, hôtes, cache | Proxy de confiance délègue une partie du filtrage ; aucun contournement | OK | Conserver les frontières documentées |
| Déduplication | `research_queue`, `ocean_knowledge.write_card`, cache Intelligence | Tests même source et source modifiée | Équivalence sémantique générale non prouvée | PARTIEL | Identités de tâches, contraintes distinctes |
| Filtrer la pertinence | `relevance`, `intelligence_evidence.retrieve` | Petits jeux de développement | Un passage correct peut être hors sujet ; gabarits forêt trop larges | PARTIEL | Requêtes/ancres propres aux tâches |
| RAG lexical | `rag`, `text.BM25`, `engine` | Corpus réel et tests FR/EN | Classement sans jugement humain exhaustif | PARTIEL | Conserver, mesurer sur tâches du jeu |
| Embeddings et hybride | `ocean_semantic`, `intelligence_semantic` | Vecteurs/indisponibilité par fixtures | Aucun modèle réel évalué | NON TESTÉ | Garder facultatif, ne pas annoncer de gain |
| Localiser les passages | `intelligence_evidence.documents/passages` | SHA/offsets, fenêtres et avertissements | Citations secondaires de plusieurs sources toutes liées à la première URL | DÉFAILLANT | Corrigé après test rouge |
| Comprendre l'intention | `intelligence_evidence.analyze` | 36 contrats synthétiques V11.1 | Cinq problèmes génériques ; caméra/interaction et projet mal contextualisés | PARTIEL | Associer aux tâches et à la Bible |
| Synthèse déterministe | `intelligence.deterministic`, `protocol` | Corpus réel + fixtures | Procédures génériques, non exécutées | PARTIEL | Recettes de laboratoire spécifiques, statut proposition |
| Ollama | `intelligence_models.Ollama/route` | NDJSON/JSON/timeout/annulation par fixtures | Pas de génération réelle disponible dans les validations précédentes | NON TESTÉ | Conserver ; aucun téléchargement implicite |
| Vérifier les affirmations | `intelligence_evidence.verify` | Nombres, version, SHA, citations | `engine=unknown` pouvait masquer une source Unreal | DÉFAILLANT | Corrigé après test rouge |
| Vérifier les procédures modèle | `intelligence.validate_model` | Nombres absents, schéma, injection | Identifiant autorisé s'il apparaissait ailleurs dans le lot non cité | DÉFAILLANT | Exiger le passage effectivement cité |
| Contradictions | `intelligence_evidence.contradictions` | Assignations booléennes/conditions | Pas d'implication sémantique générale ni d'exhaustivité | PARTIEL | Signaler, ne pas inventer un arbitre |
| Mémoire et invalidation | `Intelligence.run/get`, empreintes et LabStore | Source/config/digest/expérience changé | Pas de Bible ; ancres des requêtes équivalentes ne doivent pas perdre une version | PARTIEL | Ajouter empreinte du contexte, traiter conflits explicites |
| Échecs et réussites | `lab_store`, `lab_plan.context` | Hash chain, reprise, revue opérateur | Similarité lexicale ≠ même tâche/asset/conditions | PARTIEL | Lier explicitement tâche, recette, assets et build |
| Protocoles et preuves | `ocean_lab`, `lab_import`, scripts Blender/Studio | Blender 4.3.2 réel V11, imports par fixtures | Ni 5.2 ni B3/C1 ni Studio reproduits | PARTIEL | Conserver les limites de version et de portée |
| Obsidian/rollback | `obsidian.sync/_resume/rollback` | Exports réels isolés et interruptions | Coffre utilisateur non disponible ; conflits volontaires | OK | Réutiliser les pages réservées et transactions |
| Résumés hors RAG | `corpus.scan_notes` | `_VDN-*` exclus | Ne pas réintroduire la Bible comme preuve technique | OK | Garder source projet et sources techniques séparées |
| CLI et MCP | `v10/v11/v111`, `mcp_v8.Server` | Vrais processus stdio, 27 outils | Desktop non piloté ; usage effectif de Claude non mesuré | PARTIEL | Garder schémas, mode projet explicite |
| Budget de contexte MCP | `Intelligence.brief` | Cas courts | Question de 2 000 caractères dépassait 500 tokens estimés | DÉFAILLANT | Corrigé après test rouge |
| Abstention transmise | `Intelligence.brief` | Abstention du moteur testée | Briefing annulait l'abstention FPS inconnu dès qu'un fait périphérique existait | DÉFAILLANT | Corrigé après test rouge |
| HTTP/temps/stockage/coûts | `Budget`, sessions, `im.operation/reserve_model`, `OceanWeb.storage_check` | Réservations persistées, scopes, fixtures | Stockage Océan distinct des artefacts historiques ; coût réservé ≠ facture | PARTIEL | Ne pas augmenter les plafonds, préciser les périmètres |
| Checkpoints/annulation | `ResearchSessions`, journaux Intelligence, `atomic_write` | Interruptions, reprise, réservations | Coopératif ; lecture socket en cours jusqu'au timeout | OK | Conserver et tester le nouvel index |
| Sécurité/confidentialité | `safe_path`, `corpus`, TLS épinglé, schémas fermés, capacités hôte | Symlinks/SSRF/secrets/injections hors ligne | Pas de preuve formelle contre toute injection | PARTIEL | Aucun outil shell/Git/jeu donné aux sources ou au modèle |
| Windows/Linux/Python 3.11 | Workflow existant et UTF-8 | CI V11.1 : 369 × deux scénarios par OS | Nouvelle version à revalider ; Internet Windows non testé | OK sur la base | Exécuter les nouveaux checks |

## Défauts reproduits avant correction

Les cinq contre-exemples V11.1 échouaient tous dans
`tests/test_v112_regressions.py` :

1. URL de la seconde citation remplacée par celle de la première source.
2. Brief de 2 654 caractères pour un plafond de 1 800 caractères estimés.
3. `CanCollide` accepté avec une citation ne documentant que la lumière.
4. Citation Unreal acceptée comme fait pour Roblox si le modèle déclarait son
   moteur « unknown ».
5. Abstention sur le FPS exact de B3 perdue dans le briefing.

Les cinq tests passent après les corrections ciblées. Les signatures des
27 outils sont conservées. L'objectif complet reste consultable dans l'analyse
détaillée ; sa représentation courte est tronquée explicitement.

Deux défauts de l'intégration nouvelle ont aussi été reproduits : une file
d'acquisition terminale produisait un état global COMPLETE malgré une tâche
partielle ; et la normalisation d'une question d'export perdait un Blender 4.3
explicitement demandé face à la cible 5.2. Les tests précèdent leurs corrections.
L'état global reste PARTIAL et un conflit de version exige une clarification,
sans modifier la Bible ni les compteurs.

Les analyses historiques sont conservées, mais le mode projet n'en réaffirme
pas les anciens faits comme issus du vérificateur corrigé. Aucune migration
des notes, expériences ou sessions n'est faite en silence.

## Défauts révélés par les sources réelles et la transmission finale

Trois contre-exemples supplémentaires échouaient avant correction (journal
`docs/validation/v112/ranking-before-fix.log`) :

- La troncature BM25 précédait la pondération de qualité. Une source originale
  complète sur les collisions était éliminée au profit de citations secondaires.
  Les candidats sont maintenant pondérés avant de retenir les meilleurs.
- Deux noms de cache pour un snapshot canonique identique occupaient deux places
  et pouvaient donner une fausse impression de preuves multiples. Les reçus
  identiques sont dédupliqués ; les différences de version/conditions demeurent.
- Un cache JSON valide contenant un texte de type entier arrêtait l'admission.
  Les types sont contrôlés et le reçu incorrect est isolé avec un diagnostic.

Deux tests rouges supplémentaires montrent qu'un briefing direct pouvait encore
utiliser la dernière fiche après suppression de sa source ou ajout d'un échec
lié. La lecture compare désormais les empreintes des sources, leur expiration,
la configuration, le vérificateur, la Bible, les expériences, les visuels et les
clés des dépendances. Un briefing courant recalcule hors ligne sans écrire ; une
clé historique reste consultable et porte `inputs_obsolete`, avec ses étapes
retirées du briefing. Aucune ancienne preuve n'est effacée.

Le plafond de références visuelles a aussi été testé avant correction : le
quatrième artefact était importé avant son refus. Le refus précède maintenant
l'import, sans supprimer les trois références existantes.

Les 47 tests V11.2 sont des tests de contrats et d'intégration contrôlée, pas
47 validations de techniques dans Roblox. Le benchmark réel de récupération et
la session réseau sont publiés séparément.
