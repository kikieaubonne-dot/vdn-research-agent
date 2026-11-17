# Continuation V9 du mandat — V11.2 / contrat V6.4

17 novembre 2026, environnement cloud Linux. **Livraison PARTIELLE.** Cette continuation ajoute des capacités de laboratoire et leurs preuves ; elle ne valide pas un père réaliste utilisable dans Roblox, ni un agent intégralement autonome de recherche multimodale.

## Reprise et préservation

Départ réellement retrouvé : `codex/project-intelligence-v11-2`, `ea9549092b2cbca9cabe19c63b6a2dd0efb18277`, local non poussé. Snapshot de 618 fichiers suivis, relu avec empreintes. Modification préexistante `output/queue.json` et dossier non suivi `work/` préservés, exclus du commit. Aucune restauration de compteur, configuration personnelle ou ancien état Git. Aucun push, PR, service permanent ou téléchargement de modèle.

Le runtime arrêté précédent a été copié dans `/workspace/eponge-v9/runtime`, en conservant sa filiation et ses compteurs : HTTP9/fetch5, calcul33,822064s au départ. Le runtime précédent reste intact. Calcul réservé final59,596431s/60 ; nouvelle collecte réseau0, appels modèle0. Il reste moins d'une seconde : aucune nouvelle expérience lourde n'est lancée. Ce sont des secondes réservées par le ledger applicatif, pas une mesure CPU de toute la session Codex. Tests de développement et préparation documentaire sont comptés séparément dans leurs journaux.

## Architecture réellement implémentée

| Composant | Fonction utilisable | Preuve et limites |
|---|---|---|
| `learning_media.py` | Vidéo locale attestée, métadonnées, fenêtre audio, SRT/VTT, au plus8 captures, PTS réels, déduplication des images avec occurrences temporelles conservées, cache partiel | Clip original2s réellement décodé avec FFmpeg7.1.5. Pas de téléchargement URL, transcription ou compréhension visuelle locale. |
| `learning_assets.py`, inspecteur Blender | Copies attestées, auto-run désactivé, dépendances glTF locales bornées, métriques, rig/poids/actions, poses échantillonnées et contrôle de roundtrip | Natif et4 GLB réellement réouverts dans des processus séparés Blender4.3.2. OBJ/FBX/glTF textuel : interfaces présentes, non exécutées ici. Compte auxiliaire glTF encore imparfait. |
| `learning_store.py` | Processus possédé, délai/sortie bornés, journaux expurgés, chemins sûrs, reçus avec empreintes et obsolescence des entrées/dépendances | Tests ciblés, décodages et imports réels. Un reçu assure l'intégrité, pas la vérité, ni une frontière OS contre fichier hostile. |
| `learning_compact.py` | Enveloppe gzip sans perte sur `.blend` OWN_CREATED seulement, journal PREPARED/COMMITTED, contrôle indépendant avant remplacement atomique | Réouverture Blender et restitution exacte des octets. Ancienne empreinte conservée. Ce changement de conteneur ne concerne ni les assets utilisateur ni la mémoire fiable. |
| `learning_discovery.py` | Comparaison bornée2–4 approches,1–4 essais, critère explicite, conservation immuable, réutilisation/invalidation, adoption limitée au labo | Deux investigations réelles enregistrées. Les observations sont enregistrées par l'opérateur ; recherche automatique d'outils et auto-réparation du code NON implémentées. |
| `learning_api.py`, `project_api.py` | Brief/détail en lecture seule via les outils existants, résultats de comparaison liés aux assets, refus apply/modèle |27 contrats inchangés, vrai stdio avec preuves réelles. Claude Desktop non testé. |

## Vidéo : résultats et défauts réellement rencontrés

Entrée OWN_CREATED : images de notre ancienne végétation procédurale réutilisées, séquence A/A/B/A, tonalité originale440Hz sans voix, sous-titres écrits pour cet essai. Ce n'est ni un tutoriel YouTube ni une capture d'interface Blender. Le résultat expose les sous-titres comme données non fiables et ne prétend observer aucune opération à l'écran.

1. Un seek proche de la fin retournait FFmpeg0 sans image. Ancien log conservé. Correction : bornage au dernier instant possible selon FPS, une reprise antérieure au maximum, validation PNG et PTS observés. Sans image, statut explicite ; exit0 ne suffit pas.
2. Le milieu d'un sous-titre ratait l'état bref B. Une borne de fin inclusive associait la capture suivante à la mauvaise étape. Correction : début des étapes et intervalle semi-ouvert. Résultat :2 images distinctes contre1 auparavant ; B récupéré à PTS1s.5/6 captures et l'audio réutilisés, une seule capture supplémentaire décodée.
3. Deux captures identiques à des instants différents partagent les octets mais gardent leurs occurrences et timestamps.

Les règles de sampling de vidéos longues sont testées sur données synthétiques ; aucune vidéo longue réelle n'a été décodée. Les étapes restent CANDIDATE ou QUARANTINED, jamais commandes exécutables. Vision locale : **NOT_TESTED**, adaptateur multimodal autonome non livré. Transcription : **NOT_TESTED**. URL/YouTube : **NOT_VALIDATED**.

## Père/prologue : prototype et contre-preuve

Quatre proxies originaux : deux gabarits normalisés, chacun FK/IK,672 triangles et16 os par acteur. Capture256×256, CyclesCPU,2 samples, débruitage désactivé symétriquement ; caméra/lumière fixes. Geste de portée aux frames1/13/25 à12fps. Aucune identité, taille humaine, voix, topologie faciale ou texture réaliste inventée. Les parents déjà partis dans la Bible ne deviennent pas une nouvelle scène confirmée.

Critères natifs fixés avant essai : erreur IK≤0,03 unité normalisée et moindre que le brouillon FK, triangles égaux, déplacement du pied≤0,000001. FK n'est pas optimisé ; ceci ne démontre pas la supériorité générale de l'IK.

| Gabarit | Erreur main native FK | Erreur main native IK | Écart maximal main native/réimport FK | Écart main native/réimport IK |
|---|---:|---:|---:|---:|
| Père proposé |0,657720|0,00000782|~0,0000000683|~0,413767|
| Transfert plus étroit |0,654675|0,00001751|~0,0000000666|~0,408915|

**IK natif : critère géométrique satisfait. Export IK : REJETÉ.** La présence d'un rig et d'une action ne prouve pas la conservation du geste. Les trois poses réimportées révèlent sa perte, sur les deux gabarits. Les variantes FK conservent les trois positions de main échantillonnées, sans validation exhaustive des déformations. Les résultats sont PARTIAL_SUCCESS avec erreur d'export conservée, jamais VERIFIED/HUMAN_APPROVED.

L'option d'export `force_sampling` était activée : cela n'a pas suffi pour ce fichier/Blender4.3.2. Baking visuel des contraintes = prochaine hypothèse de réparation, **non exécutée**, pas correctif déclaré validé. Ne pas utiliser les IK GLB comme livraison jouable.

L'importeur crée aussi une Icosphere auxiliaire80 triangles :672 triangles du payload GLB deviennent752 dans la scène importée. Une règle conservatrice pour formes d'os explicitement masquées ne reconnaît pas ce cas réel ; anomalie encore ouverte. L'analyse indépendante du JSON GLB confirme14 primitives et672 triangles,48 canaux sans doublon. Ne pas supprimer des objets par leur nom pour forcer un PASS.

## Découverte imprévue utile

Le plafond de stockage a effectivement bloqué l'inspection indépendante. Comparaison : conteneur natif brut contre enveloppe gzip standard, sans changement du quota et sans suppression de preuves.1 344 596→146 793 octets, gain1 197 803 octets (**89,08% sur ce fichier uniquement**). Décompression restitue le SHA initial et Blender ouvre le conteneur compressé dans un autre processus. L'inspection du natif et des quatre GLB a ensuite pu se terminer.

Cette découverte a été faite et mise en œuvre par Codex pendant le développement. Elle n'est pas une auto-modification de l'agent. Le registre ne la classe que PARTIAL : transfert sur un second fichier non exécuté. L'autre investigation rejette la voie d'export IK par mesure indépendante sur deux objets. Aucune découverte artistique, amélioration RAG ou économie de quota Claude n'est démontrée.

## Tests, intégration et portée

Voir [proofs/test-summary.json](proofs/test-summary.json) et les journaux archivés pour les nombres et SHA épinglés.29 nouveaux cas ciblés passent ; les587 tests (558 historiques +29) passent dans la suite hors ligne épinglée et dans le scénario personnel séquentiel. Validation complète lancée seulement après stabilisation. La première exécution concurrente du scénario personnel a8 échecs liés au verrou global de superviseur ; cet échec est conservé, la reprise séquentielle passe. Aucun assouplissement du verrou ni des tests. Temps respectifs :69,181s pour les tests hors ligne,60,176s pour le scénario personnel séquentiel.

Vrai processus MCP Linux :27 outils,4 briefings de preuves réelles réussis, refus d'écriture testé. Le bref média fait1152 caractères JSON dans cette exécution, ce n'est pas une mesure d'économie Claude. Obsidian : destination isolée,118 fichiers exportés (connaissances/configurations héritées et4 pages de labo, pas118 découvertes), deuxième export inchangé, rollback réussi avec archives. Aucun coffre personnel touché.

Linux/Python3.12.14, FFmpeg7.1.5, Blender4.3.2 réellement exécutés. Syntaxe Python3.11 vérifiable statiquement, mais aucune exécution Python3.11/Windows dans cette continuation. Pas de push : aucune nouvelle CI distante. Anciennes CI ne valident pas les changements actuels.

## Réconciliation du contrat et limites

Les210 exigences restent55 DONE_VERIFIED /118 PARTIAL /29 BLOCKED /8 NOT_TESTED dans leur portée historique. Delta :0 promotion globale. Vidéo locale, inspection et mémoire de comparaisons progressent par sous-capacités ; leurs objectifs complets restent PARTIAL. Les autres limites historiques restent ouvertes : failover vivant, pause sous charge, holdout caché, entailment sémantique, modèles réels, licence/versions inconnues.

Windows utilisateur, Claude Desktop, Blender5.2, Roblox Studio et B3/C1 réels : BLOCKED par l'environnement disponible. Pas de service permanent ni recherche en arrière-plan laissés actifs. État final : **STOPPED / PARTIAL**, prochaine étape exacte dans [HANDOFF.md](HANDOFF.md).
