# Continuation du mandat V10 — socle V11.2 / contrat V6.4

17 novembre 2026. **Mission PARTIELLE**, avec progrès réel sur le roundtrip d'animation Blender. Aucun changement de branche, push, PR, fusion, service permanent ou modification de Studio.

## État réellement retrouvé

Commit initial `9821499822b16f2af91509bfc151480afd56f92b`, branche `codex/project-intelligence-v11-2`. Le code correspondait à la référence des587 tests précédente. Archive précédente présente et vérifiable.653 fichiers suivis sauvegardés et relus ; `output/queue.json` déjà modifié et `work/` non suivi conservés et exclus du commit.

Les mandats V6.4, V7, V7.5→V8 et dernière continuation V9 sont disponibles dans les pièces jointes. Les210 exigences numérotées du contrat fondateur sont présentes ; inventaire et hashes dans `proofs/mandates.json`. Aucun accès aux autres conversations ou au PC Windows n'est supposé. Les rapports `learning/`, la Bible, les chapitres, BLACK BOX, contrats MCP et artefacts conservés ont servi de base. Les états historiques55 DONE_VERIFIED /118 PARTIAL /29 BLOCKED /8 NOT_TESTED ne sont pas promus globalement.

## Budget et isolation

Le runtime V9 reste intact : calcul59,596431/60s, HTTP9/fetch5. Autorisation humaine explicite reçue : **20s supplémentaires uniquement pour bake/export/réimport Blender dans une copie isolée**. Le runtime `/workspace/eponge-v10/runtime` reprend ses compteurs, avec plafond80s et activation autonome toujours désactivée. Aucun autre quota relevé.

État après essais :77,058308s réservées sous le plafond temporaire80s, soit17,461877s ajoutées, contrôles d'orchestration compris. L'extension ponctuelle est ensuite **clôturée** : la politique60s originale est rétablie exactement dans la copie, sans diminuer les77,058308s du ledger. Il ne reste donc aucun calcul autorisé aujourd'hui ; aucune allocation80s quotidienne récurrente n'est créée.0 nouvel HTTP,0 appel modèle réel. La réserve initiale de stockage1,2Mo a été refusée ; les rapports de poses sont désormais compressés sans perte et décodés sous limite1Mo. Le plafond de contenu Ocean reste8 000 000 octets. Une fiche de comparaison supplémentaire reste bloquée faute de réserve, sans déplacement de son contenu pour contourner ce plafond. Les journaux opérationnels et petits résultats LabStore utilisent leurs mécanismes existants.

## P1 — diagnostic et réparation mesurée

Constats vérifiables avant correction :

- Actions natives : courbes de tête et influence de contrainte IK, aucune courbe explicite de rotation des bras ; NLA0 pour l'acteur inspecté.
- GLB rejetés : rotations des bras constantes, tête animée. Les joints divergent de0,413767 et0,408915 unité normalisée aux trois poses communes. Ces contre-exemples restent identifiables et rejetés.
- Même squelette/maillage et contrôles ; variante FK précédente conservait les positions échantillonnées. Pas de retargeting utilisé. Aucune cause FBX affirmée : il s'agit d'un export GLB.

Correction : charger la copie attestée, capturer25 poses, bake visuel des os à chaque frame source1–25, convertir le résultat évalué en clés, retirer les contraintes uniquement dans la copie, exporter l'action puis réimporter dans un **second processus Blender vierge**. Le source conserve son empreinte. Une voie FBX est préparée mais non exécutée ; GLB est un format intermédiaire testé ici, pas une garantie d'import direct dans Studio.

### Contre-preuve et changement de mesure explicite

Le premier bake conserve le natif (écarts de l'ordre de0,0000003), mais son contrôle v1 échoue sur les extrémités d'os. Ce FAIL est conservé. Le code installé de l'importeur (`vnode.py`, `pick_bone_length`) reconstruit les longueurs d'affichage par heuristique. glTF conserve joints et matrices de liaison, pas les extrémités d'affichage Blender.

Le critère **interop-2**, enregistré avant les nouvelles sondes, garde la tolérance1e-5 et remplace cet invariant non transporté par les matrices de déformation. Il exige25 poses, têtes de tous les os, matrices de skinning, bornes et centroïdes surfaciques de tous les meshes déformés, triangles et durée. Les écarts d'extrémités restent rapportés séparément. Ce n'est pas un PASS sous le critère v1 ; ni son échec ni le changement de mesure ne sont effacés.

| Mesure / gabarit | Principal | Transfert plus étroit |
|---|---:|---:|
| Poses comparées |25|25|
| Durée native et réimportée |2s|2s|
| Écart maximal des articulations |2,8741e-7|1,4752e-7|
| Écart maximal des éléments des matrices de déformation |5,8115e-7|6,2585e-7|
| Écart maximal des surfaces contrôlées |2,6152e-7|2,4756e-7|
| Écart de durée |0|0|
| Extrémités d'affichage, diagnostic conservé |~0,146754|~0,146754|
| Verdict interop-2 |PASS Blender4.3.2|PASS Blender4.3.2|

Le principal est aussi réouvert depuis le `.blend` sauvegardé avant une nouvelle importation GLB. Le second gabarit est baké et contrôlé indépendamment. Tous les exports et natifs sont livrés, avec les contre-exemples dans le runtime conservé. La différence de FPS d'import12→24 ne modifie pas les2s ; comparaison par temps normalisé, pas par même numéro de frame.

**Portée : geste préservé dans Blender4.3.2↔GLB pour ces proxies originaux.** Ni déformation à tout instant continu, ni retargeting, réalisme, R15, contrôleur Roblox, Studio, FBX, Windows ou Blender5.2 ne sont validés. Les os d'affichage différents peuvent compter pour une édition/retargeting ultérieur. Le père de famille n'est pas ajouté à la scène : ses anciens noms de gabarits ne constituent pas une décision de casting.

## P2 — vidéo et vision

Pipeline vidéo V9 conservé, reçus/entrées/captures contrôlables, régressions FFmpeg/timestamps/déduplication toujours couvertes. Le seul média réel reste le clip original2s de V9 ; aucun nouveau YouTube ou tutoriel long n'a été collecté/décodé ici.

`learning_vision.py` fournit un adaptateur local optionnel : permission explicite, configuration désactivée par défaut, nom exact installé, capacité vision annoncée, endpoint loopback strict, annulation, délais, images scellées≤64Ko, contexte/génération bornés, économie CPU, JSON strict, provenance du modèle/version et partage des ledgers HTTP/modèle/calcul existants. Aucun téléchargement. Erreur → repli déterministe. Perceptions du modèle toujours non vérifiées, sans affirmation SOURCE_SUPPORTED ou approbation humaine.

Tests de protocole sur réponses Ollama **mockées** uniquement. Aucun modèle réel sélectionné/activé/exécuté ; service non sondé, disponibilité réelle UNKNOWN. Compréhension visuelle locale **NOT_TESTED**, transcription réelle **NOT_TESTED**, YouTube **NOT_VALIDATED**.

## P3 — prologue entier et ressources

La Bible passe à révision3, chapitres à révision2, sur décisions humaines explicites de cette mission. Anciennes révisions conservées dans `project/history/`. A maison → B poursuite → C confrontation → D appel → E enquêteur ; F reste UNKNOWN avec trois options PROPOSED. Première poursuite : seulement sprint Shift si nécessaire ; apprentissage approfondi en E, pas de tutoriel forcé d'escalade/glissade/accroupissement/enjambement en B.

`project/prologue.json` décrit36 ressources avec catégories, scènes, priorités, dépendances, formats, création, licences/coûts inconnus, validation, fichiers et problèmes. Les budgets/durées de production, assets réels et performances ne sont pas inventés. Voir `RESOURCE_INVENTORY.md` et `J0_J3.md`.

`agent/prologue.py` fournit inventaire, brief, parcours de référence, checkpoints contrôlés et reprise invalidée après révision narrative. Le module original `roblox/prologue/Progression.lua` est une proposition sans réseau ni publication : non exécuté, aucun interpréteur Lua/Luau disponible. Le parcours Python A–E est une simulation logicielle qui s'arrête avant une fin non approuvée ; ce n'est pas une partie jouée, un timing de rétention ni une scène Studio construite.

Deux exports GLB réparés et leurs fichiers natifs sont disponibles dans `artifacts/`. Le natif principal contient aussi d'autres acteurs non modifiés : seul `father_proxy-IK` y correspond à la variante réparée. Le natif transfert est isolé. Visages, cheveux, vêtements réalistes, voix, environnement et interfaces finales restent à produire/valider. Les réelles copies B3/C1, lampeV2, contrôleur et scène ne sont pas accessibles ici.

## P4/P5 — mémoire, coordination et amélioration mesurable

La méthode de bake est comparée à l'export précédent avec **la même métrique avant/après** : positions des16 joints aux trois temps communs0/0,5/1 ; les25 poses/matrices/surfaces supplémentaires restent des mesures séparées. Fiche dans le registre existant, réutilisable par MCP, adoption limitée au laboratoire. Deux résultats SUCCESS enregistrés dans LabStore, sans VERIFIED/HUMAN_APPROVED ; anciennes erreurs conservées.

Compression des nouvelles preuves observée sur deux fichiers :191 577→22 679 et191 204→21 177 octets, soit88,16% et88,92% sur ces fichiers. La référence brute est la taille des octets JSON décodés, pas une autre campagne chronométrée. Pas de vitesse ou de qualité de raisonnement déduite. La publication d'une fiche B supplémentaire est BLOCKED par stockage ; mesures dans le rapport et incident conservé.

Il s'agit d'une amélioration conçue par Codex et de comparaisons enregistrées, **pas d'une auto-modification du code ni d'une double boucle autonome entièrement démontrée**. Les moteurs de recherche, RAG, expériences et supervision existants restent en place. Aucun changement RAG/hybride, benchmark inédit caché ou économie Claude n'est revendiqué.

## Validation et livraison

Voir `proofs/test-summary.json` pour résultats exacts, SHA des sources épinglées et journaux. **611 tests hors ligne et611 dans le scénario personnel séquentiel passent**, avec33 tests ciblés de cette tranche et87 contrôles narratifs/projet après la clarification finale des réponses textuelles de la Bible. Le logiciel épinglé est inchangé après les suites complètes ; cette clarification de données est identifiée séparément. Les tests sont exécutés séquentiellement pour respecter le verrou global des superviseurs. Fichiers projet épinglés par un manifeste complémentaire, sans modification du validateur critique.

MCP stdio réel :27 outils, quatre nouveaux briefings, refus d'écriture. Obsidian isolé :132 fichiers incluant contenu hérité, expériences et une page de production ; répétition inchangée, rollback réussi. Pas132 nouvelles connaissances. Claude Desktop non testé.

Le contenu historique de `knowledge/`, les paramètres de sécurité, compteurs du runtime V9 et changements préexistants restent préservés. Seules les révisions narratives explicitement autorisées sont changées dans le projet. Les dix composants critiques ne sont pas réécrits ; les risques persistants restent dans `BLACK_BOX.md` et les rapports hérités.

Commit local et archive vérifiée : `DELIVERY_SUMMARY.json` à côté du paquet final. Aucune nouvelle CI GitHub sans publication. Processus de recherche **STOPPED**, aucune autonomie permanente activée. La mission complète reste PARTIELLE jusqu'aux validations locales et à l'assemblage réel du prologue.
