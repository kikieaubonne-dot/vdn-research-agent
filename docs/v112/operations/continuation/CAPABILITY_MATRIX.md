# Dix composants — réconciliation de reprise

Les preuves héritées527/campagne30min sont identifiées séparément dans REPORT ; les tests nouveaux et558 sont Linux uniquement. Aucun mécanisme n’est universellement déclaré fiable.

| Composant | Hérité, conservé | Nouveau / retesté | Verdict / frontière |
|---|---|---|---|
| Superviseur | Standard library, heartbeat, backoff, circuit | SIGKILL du superviseur, compagnon de vie, verrou worker, horloge future, groupes appartenant aux essais | DONE_VERIFIED pour pannes éprouvées ; OS/compagnon et Windows PARTIAL |
| Auto-réparation | Index SQLite dérivé, deux tentatives, quarantaine et retest | Tests SQLite historiques réexécutés dans558 ; arrêt critique et revue humaine non réductibles | DONE_VERIFIED pour index dérivé ; réparation générale/code/API PARTIAL, aucune promotion |
| Restauration | Snapshot553 fichiers, Obsidian transactionnel | Archive initiale579 fichiers relue ; image de code testée, copie runtime/checkpoint identique, MCP réel depuis restauration | DONE_VERIFIED sur copies ; failover vivant automatique PARTIAL |
| Validateur indépendant | Entrées/tests fixes, codes réels | Inclusion Windows.cmd/ps1,558 tests, refus image si source/test/log changés | DONE_VERIFIED logiciel ; holdout réellement caché BLOCKED |
| Mémoire des erreurs | Chaîne SHA, occurrences, historique | Gravité/revue monotones, secours temporaire et stderr, échecs Blender persistants | DONE_VERIFIED sur scénarios testés ; disque physique/acteur OS malveillant PARTIAL |
| Métavision | Croyances versionnées et contre-exemples | Résultats géométriques et limites consultables sans promotion | PARTIAL : confiance non calibrée, pas de modèle réel ni réentraînement |
| Ordonnanceur | Sessions, quotas, checkpoints, tâches reprises | Sérialisation des nouveaux superviseurs par utilisateur OS ; séparation fetch/HTTP corrigée | PARTIAL : campagne bornée utile ; charge GPU/CPU utilisateur, quotas agrégés et mode nuit non validés |
| Détecteur de régressions | Suites et gate STAGED |558 tests, lanceurs épinglés, rejet critique, refus source/image modifiée | DONE_VERIFIED dans périmètre structurel ; canary/holdout/production BLOCKED |
| Classement de recherches | Lexical/RRF, réserve/archives, correction des légendes |12 questions mêmes métriques ; échecs d’autres assets non universalisés, cache de qualité invalidé | PARTIAL : meilleure gestion du contexte d’échec, aucun gain Recall/MRR ; sémantique non démontrée |
| BLACK BOX | Journal hors moteur et rapports | Panne réelle débruiteur,13 incidents/limites conservés, secours testé, handoff et gravités | DONE_VERIFIED sur journalisation éprouvée ; causes inconnues et limites d’accès explicites |

Les DONE_VERIFIED ci-dessus qualifient des comportements testés, pas toute la ligne du contrat maître. Les clauses composées restent dans la matrice210 avec leurs limites.
