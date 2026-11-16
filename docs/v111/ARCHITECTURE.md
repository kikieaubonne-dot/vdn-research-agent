# Chaîne d'intelligence implémentée

Python 3.11+, bibliothèque standard uniquement. Les responsabilités sont des
fonctions/modules, pas dix agents nécessitant dix appels IA.

| Responsabilité | Implémentation effective |
|---|---|
| ProblemAnalyzer | `intelligence_evidence.analyze` : symptômes, problèmes, logiciels, versions, hypothèses et informations manquantes |
| EvidenceRetriever / Selector | caches V11 + citations des notes ; BM25, concepts FR/EN, priorité aux sources originales, diversité par problème et contexte Blender |
| TechnicalSynthesizer | `intelligence.py` : candidat déterministe puis une génération facultative JSON bornée |
| ClaimVerifier | identité du document, SHA, offsets, texte exact, nombres, version, logiciel, source secondaire et contexte incomplet |
| ContradictionDetector | assignations booléennes explicites ; conflit seulement sous mêmes versions et conditions déclarées |
| ExperimentPlanner | protocoles hypothèse/contrôles/variable/étapes/mesures/critères/risques/rollback |
| KnowledgeCurator | résultats immuables, journaux de progression hachés, empreintes de sources/configuration/modèle, échecs consultables |
| ModelRouter | niveau 0 déterministe ; modèle compact ou capable installé ; économie/mémoire ; distant public explicitement autorisé |
| QualityEvaluator | 36 contrats annotés et huit tâches A/B sur un corpus identique ; métriques et sorties brutes |

## Sources et affirmations

Une source enregistrée conserve URL, identifiant, titre, section, offsets,
ligne, date, version, empreinte et conditions. Un avertissement adjacent reste
attaché au paragraphe. Les fenêtres de documents longs et les caches tronqués
sont marqués incomplets. Une version Blender n'est extraite automatiquement
que si l'en-tête contient littéralement `Blender X.Y Manual` ; un `latest`
ne prouve pas la compatibilité avec Blender 5.2.

Les citations des 111 notes de V11 sont des **références secondaires** si le
snapshot original n'est pas disponible. Les résumés, analyses et pages Obsidian
ne deviennent pas des sources indépendantes. Une source enregistrée est une
preuve de capture/attribution, pas une attestation de vérité ou d'authenticité
cryptographique du site.

Chaque affirmation porte identifiant, texte, passages et sources, version,
logiciel, type, soutien, contradictions, vérification et date. États distincts :
`SOURCE_SUPPORTED`, `INFERRED`, `HYPOTHESIS`, `EXPERIMENT_PROPOSAL`, `UNSUPPORTED`,
`CONTRADICTED`, `OUTDATED`. Seules les citations littérales de sources originales
complètes, compatibles et non périmées peuvent entrer dans `facts`.
Une paraphrase reste inférée. Un nombre doit être un token numérique réellement
présent : `90` n'est pas soutenu par `900`. Aucun calcul libre du modèle n'est
admis comme fait ; les deltas expérimentaux restent ceux du laboratoire V11.

La critique est un code séparé du générateur. Elle conserve les rejets et
corrections, signale versions inconnues, procédures non exécutées, contextes
incomplets et confusions de logiciels. Une section sur les collisions entre
personnages n'est pas présentée comme correctif confirmé des sapins.
Ce contrôle mécanique n'est pas une preuve d'implication sémantique générale.
Les contradictions implicites et les jugements de qualité nécessitent une revue.

## Modèles, contrôle et budgets

Endpoint local : HTTP loopback **littéral**, sans proxy ni redirection.
Détection `/api/tags`, digest installé exact ; version serveur et métriques
de génération enregistrées. Diagnostic supplémentaire `/api/ps` et `/api/show`
pour modèles chargés, quantification, capacités et licence. Aucun endpoint pull,
aucun téléchargement automatique.

Contexte estimé conservativement, non par tokenizer exact ; `num_ctx`,
`num_predict`, streaming NDJSON, taille totale et schéma final limités.
Annulation coopérative avant/après les lectures ; Ctrl+C conserve le checkpoint.
Une lecture socket peut rester engagée jusqu'au timeout. Aucun worker ni
processus n'est tué. Un HTTP 200 ou du JSON valide ne suffit pas à accepter une
synthèse : le schéma et chaque affirmation sont contrôlés.

Les HTTP locaux comptent aussi dans le quota journalier V11. Une opération
isolée conserve les plafonds V10 : au plus 6 HTTP et 20 s. Un journal de calcul
propre à Intelligence réserve avant effet, plafonné à la limite de calcul V10
(60 s) **sur le jour UTC** ; le temps inutilisé est rendu après arrêt contrôlé.
Un crash dur garde sa réservation. Ce plafond additionnel ne réinitialise pas
les sessions existantes. En collecteur V11, le Budget et le verrou de la session
sont utilisés directement. Une seule génération par analyse, et quota modèles
V11 commun par jour, 1 par défaut. Métadonnées, retries et embeddings ne sont
pas gratuits en HTTP. Aucun quota historique n'est augmenté.

`config/intelligence.json.enabled=true` intègre le pipeline au collecteur V11
après l'écriture du candidat. Il remplace l'ancien appel modèle de cette unité,
sans le doubler. Les automatismes V11 restent désactivés par défaut.

Le distant nécessite de plus une classification opérateur `public`, les
activations V10/V11 et une réserve de coût explicite. La réserve n'est pas une
facture ; aucune exactitude de coût réel n'est inventée. Aucun appel payant ici.

## Mémoire, MCP et expériences

`lab/ocean/intelligence/results/` : révisions immuables liées aux empreintes ;
`runs/` : preuves avant génération, état, critique et échec éventuel ;
`compute.json` : réservation persistante ; `embeddings.json` : données dérivées.
Une source, condition, version, configuration ou digest modèle modifié invalide
le cache approprié. Les erreurs modèles restent retentables, sans être mises
en cache comme succès. Les journaux incomplets sont lisibles avec avertissement.

`--v111` ajoute cinq outils aux 22 V11 ; `--v11` garde son contrat. Les lectures
n'autorisent pas la génération. `--allow-intelligence` est distinct des capacités
recherche et expérience. Les résultats LabStore, échecs et revue humaine sont
récupérés par le briefing ; importer un résultat via les outils Lab existants
le rend disponible à l'analyse suivante. Aucune promotion automatique VERIFIED.

Les protocoles sont des propositions d'expériences, jamais des tests exécutés.
Aucun accès arbitraire à Blender, Studio, au shell ou à Git n'est donné au modèle.
