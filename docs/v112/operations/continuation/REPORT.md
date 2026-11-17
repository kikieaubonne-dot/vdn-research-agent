# Reprise ciblée V11.2 / contrat V6.4 — 17 novembre 2026

**Verdict PARTIEL.** Les actions accessibles ont produit des sources, un essai forestier et des protections supplémentaires. Ce rapport n’accepte pas intégralement les 210 exigences et ne valide pas le PC Windows utilisateur. Aucune mission de recherche n’est laissée active, aucune publication ni installation permanente effectuée.

## Continuité vérifiée

Branche retrouvée : `codex/project-intelligence-v11-2`, HEAD local `ebac8f3478efee05e0e88af635de3dcbc848cace`, un commit devant la référence distante locale `c93fe9b`. File `output/queue.json` déjà modifiée et `work/` non suivi préservés. Aucun reset, nettoyage ou nouvel historique. Pas de nouvelle vérification réseau de la PR ; aucun push ou changement de PR effectué.

Les hashes des entrées et du log de validation précédents correspondent au dépôt retrouvé ; l’archive précédente est lisible. Les 527 tests, la restauration de 553 fichiers et la campagne de 1800,359 s sont des **preuves héritées vérifiées par leurs artefacts**, pas de nouvelles exécutions de ces campagnes. Un nouveau point de reprise de 579 fichiers suivis a été relu intégralement. Les 126 fichiers de données suivis contrôlés, dont **111 Markdown actuellement présents sous knowledge/**, ont conservé leurs empreintes. Le nombre annoncé historiquement de 110 n’a pas été substitué au nombre réellement constaté.

## Défauts reproduits puis corrigés

| Défaut | Reproduction avant correction | Correction et contrôle |
|---|---|---|
| Un worker survit à la mort brutale de son superviseur | `GuardParentLossTests`, véritable SIGKILL Linux sur processus de fixture | Compagnon transitoire indépendant du cœur, pipe de vie, délai et verrou du worker ; il arrête seulement son groupe enfant. Reprise de fixture sans duplication de l’effet. Pas de service OS. |
| Heartbeat futur neutralisant le watchdog | Horodatage de fixture dans le futur | Rejet de cette présence de vie incohérente ; arrêt borné. |
| Secrets JSON non masqués | Clés et valeurs entre guillemets dans incidents et stdout | Masquage partagé standard library ; tests JSON, headers et formes key=value. Ce n’est pas une garantie universelle d’absence de secrets. |
| Secours du journal sur le même arbre indisponible | ENOSPC injecté sur stockage principal | Essai borné dans le répertoire temporaire, puis stderr minimal si les deux lieux échouent ; état DIAGNOSTIC_UNAVAILABLE, jamais sain. |
| Une récurrence abaisse CRITICAL en LOW | Deux événements de même signature | Gravité et besoin de revue humaine monotones ; aucune clôture critique automatique. |
| Deux workspaces supervisés travaillent simultanément | Deux vrais superviseurs de fixture | Verrou OS partagé par identité utilisateur pour les nouveaux superviseurs. Pas de promesse d’agrégation de tous les compteurs de copies séquentielles. |
| `fetch_attempt()` débite le compteur HTTP de l’Intelligence | Fixture rouge, puis observation réelle : 4 HTTP mais 7 réservations | Comptabilisation séparée des fetch et HTTP, plafonds inchangés. Réconciliation des fetch manquants uniquement vers le haut. |
| Une panne Blender sur objets générés bloque toute préparation B3/C1 | Fiche réelle devenue BLOCKED après l’échec du débruiteur | Échecs d’assets explicitement disjoints conservés séparément ; assets inconnus ou en recouvrement restent bloquants. Le refus de répéter une même méthode échouée via MCP reste testé. Nouvelle fiche PARTIAL, jamais READY. |
| Changer le validateur de fiches ne périme pas l’ancien cache | Version de qualité changée dans une fixture | Version du pipeline Project incluse dans l’empreinte de réutilisation. Anciennes fiches conservées, signalées périmées. |
| Lanceurs Windows absents des entrées épinglées | Modification `.cmd` indétectable | `.cmd` / `.ps1` inclus dans la validation ; `Eponge.cmd` inclus dans l’image de code. Ceci ne constitue pas une exécution Windows. |
| Débruiteur absent du Blender disponible | Échec réel, trace OpenImageDenoise conservée | Denoising désactivé explicitement et symétriquement ; nouvelle variante du script testée, sans installation ni modification personnelle. |

Les régressions rouges, les validations candidates échouées et les premiers essais demeurent dans le dossier privé. Un test additionnel visait initialement le stockage interne au lieu de la frontière publique MCP de préparation : le harnais a été corrigé pour tester cette frontière, sans changer le critère d’interdiction de reprise identique. Les fixtures de superviseur ont aussi reçu leur propre groupe de processus ; la validation finale ne présente plus leur avertissement de processus non récolté. Une ancienne référence de chemin dans les métadonnées d’un harnais de restauration a été rectifiée après comparaison des hashes de l’approbation ; original conservé. Aucun de ces ajustements ne transforme un résultat moteur manquant en PASS.

## Valeur documentaire et budgets

La collecte réelle ciblée a consommé **6 tentatives HTTP**, dont les reprises ; robots réutilisés depuis leur cache vérifié. Deux nouvelles captures originales exploitables : [SpotLight](https://create.roblox.com/docs/reference/engine/classes/SpotLight) et [Instance streaming](https://create.roblox.com/docs/workspace/streaming). La tentative Camera a reçu deux HTTP502 puis s’est arrêtée. Deux réponses HTML200 n’ont pas donné de capture ; leur cause précise n’a pas été conservée par le premier harnais et reste inconnue. Les endpoints Markdown documentés ont ensuite été utilisés dans l’enveloppe restante, sans élargir les autorisations.

Le changement de jour UTC est conservé dans les preuves avant/après. Le ledger du 17 novembre reste volontairement **HTTP=9 pour 6 tentatives réelles** : les trois réservations excédentaires antérieures au correctif ne sont pas effacées. Les fetch manquants ont été remontés de2 à5 sur preuve, jamais diminués. La file source personnelle n’a pas changé. Les budgets de calcul historiques et nouveaux sont conservés ; aucun modèle n’est appelé ni téléchargé.

Le [briefing forêt](FOREST_BRIEF.md) couvre huit thèmes demandés avec huit passages attribués de sept URL, hypothèses et prochaines validations. Les empreintes/positions sont contrôlées ; licences et build Studio restent UNKNOWN. Empreintes adulte/enfant : BLOCKED, faute de méthode et gabarits suffisamment établis. Une capture correcte ne valide pas une technique. Atmosphere documente notamment la diffusion solaire : cela ne prouve pas un faisceau volumétrique de torche.

## Essai forestier réel

Blender **4.3.2 CPU**, assets créés localement, sans assets tiers ni B3/C1 : épicéa procédural et buisson de transfert défini avant génération. A : branches planes ; B : même géométrie avec courbure déclarée. Seed, caméra, éclairage, résolution et nombre de branches constants dans chaque paire. Les paramètres sont proposés pour l’essai, pas optimaux pour Roblox.

| Mesure | Épicéa A / B | Buisson A / B |
|---|---|---|
| Triangles | 812 / 812 | 684 / 684 |
| Branches | 48 / 48 | 40 / 40 |
| Étendue verticale moyenne par branche | 0 / 0,253125 | 0 / 0,21225 |
| Capture réelle | PNG / PNG | PNG / PNG |
| Sauvegarde .blend puis réouverture | comptes conservés | comptes conservés |
| Export OBJ puis réimport dans un second processus | comptes conservés | comptes conservés |

Les étendues utilisent la convention du prototype d’une unité de scène pour un mètre ; aucune conversion Roblox n’est établie. Durées internes Blender : génération/captures0,629 s, vérification0,031 s, hors démarrage et orchestration. Ces durées ne sont pas des FPS du jeu.

**Hypothèse géométrique PASS ; esthétique INCONCLUSIVE ; Roblox BLOCKED.** Le transfert porte sur deux objets synthétiques, pas un holdout aveugle ni une preuve de réalisme. Quatre captures sont consultables dans [proofs](proofs/forest-artifacts.json). Deux dossiers du premier lot sont FAILED après arrêt du processus (le buisson n’a pas été rendu dans ce lot), et deux nouveaux PARTIAL_SUCCESS persistent ; aucun VERIFIED/HUMAN_APPROVED.

## Mémoire, MCP et Obsidian

Processus MCP stdio réel en lecture seule : 27 contrats strictement identiques au transcript précédent, Bible, briefing, détail de branche, deux expériences réelles récupérées et erreur contrôlée sur entrée invalide. Le briefing trees devient PARTIAL tout en exposant les deux échecs d’autres assets ; 4060 caractères observés, sans affirmation d’économie de quota Claude. Claude Desktop reste BLOCKED.

Export dans coffre isolé : contenu relu, second export unchanged. Dans une copie du coffre, transaction ajoutée puis rollback réel, **123 fichiers knowledge restaurés à l’identique**, réexport unchanged. Ce sont surtout des fichiers hérités : pas123 nouvelles découvertes. Le coffre personnel n’est pas modifié.

## Restauration exécutable

`scripts/eponge_recovery.py` scelle une image uniquement depuis des entrées épinglées, un résultat indépendant PASS de la suite complète et son log correspondant, avec approbation opérateur explicite limitée au laboratoire. Une empreinte externe lie l’image approuvée. Corruption/incompatibilité ou données fiables modifiées : refus avant restauration.

Essai réel : exécutable corrompu dans copie jetable, refus du code altéré, restauration vers une **nouvelle** copie désactivée, tous les fichiers runtime et octets du checkpoint conservés, mêmes budgets, puis véritable lecture MCP depuis le code restauré. Le workspace fautif reste intact. [Preuve](proofs/executable-recovery.json).

**Pas de bascule automatique vivante, pas de promotion en production, pas de redémarrage après panne OS.** La mort du superviseur seul est couverte par le compagnon ; celle du compagnon/OS nécessite encore une reprise externe autorisée.

## Tests et mesures

- **558 tests hors ligne PASS** sur Linux/Python3.12.14, sockets interdits dans les sous-processus, validateur indépendant et entrées inchangées.
- **558 tests scénario configuration personnelle**, copie isolée et configuration source inchangée ; résultat final et empreinte du log dans les preuves de livraison.
- 31 nouveaux cas distincts par rapport aux527 hérités ; aucun test historique supprimé. Les quatre régressions historiques de `project_work` restent couvertes.
- Syntaxe de83 fichiers analysée avec grammaire Python3.11 ; **ce n’est pas un test d’interpréteur3.11**.
- Contrôle RAG12 questions : mêmes annotations/corpus, mêmes Recall/Precision/MRR/nDCG/couverture/doublons avant/après. Aucun gain de ranking revendiqué ; latence non utilisée pour conclure à un gain. Benchmark22 antérieur conservé sans répétition inutile.
- Pas de nouvelle CI Windows, pas de test sur Windows utilisateur, Desktop, Blender5.2 ou Studio. Les anciennes CI n’acceptent pas ce nouveau code.

La [réconciliation210](ACCEPTANCE_RECONCILIATION.json) distingue55 DONE_VERIFIED dans leur périmètre,118 PARTIAL,29 BLOCKED,8 NOT_TESTED. Ce classement d’audit n’est pas une mesure de gain de compétence ni une acceptation globale. Les descriptions complètes121–175 sont conservées ; leurs titres seuls ne suffisent pas.

## Relève

[Audit des dix composants](CAPABILITY_MATRIX.md), [BLACK BOX](BLACK_BOX.md), [reprise locale](LOCAL_HANDOFF.md), [relève exacte](CODEX_HANDOFF.md). Le bilan unique du17 novembre11 h Europe/Paris doit lire les preuves actuelles et indiquer STOPPED ou BLOCKED si l’environnement devient inaccessible. Aucun travail nocturne continu n’est revendiqué. Le code est conservé localement sur la branche existante ; SHA final et archives dans le manifeste de livraison.
