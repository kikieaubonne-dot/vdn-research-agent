# Continuation V11 — démarrage du prologue et mission forêt

## Verdict

**PARTIEL : bibliothèque et laboratoires limités opérationnels dans le cloud.** Le paquet PROLOGUE_START_NOW a été livré avant les travaux approfondis. Il permet de préparer A→E immédiatement avec Bible r3,36ressources, dépendances, architecture proposée, modules Luau candidats, deux gestes réparés hérités et diagnostics Windows. Aucun accès au PC Windows utilisateur, Claude Desktop ou Roblox Studio. Aucun prologue joué, publication, modèle ou service permanent.

## Reprise et préservation

Départ vérifié17937baf41a3f626975525812e56c66a3fa3cbb9, branche codex/project-intelligence-v11-2. Les modifications préexistantes output/queue.json et work/ sont préservées hors commit.111Markdown historiques, sessions, Bible/historiques, preuves et anciens IK rejetés conservés. Aucun reset/clean, migration destructive ou push. Les mandats V6.4 (annexeA210exigences), V7, V7.5→V8, V9 et les rapports V10 accessibles ont été vérifiés ; aucune autre conversation n'est supposée accessible.

La matrice TRACEABILITY_210.json conserve les formulations et les verdicts hérités :55DONE_VERIFIED,118PARTIAL,29BLOCKED,8NOT_TESTED. Ces210exigences composées ne sont pas toutes réceptionnées à nouveau. CAPABILITIES.md distingue implémentation, tests isolés, outils réels et autonomie inactive.

## Premier paquet

Première livraison créée à11h34 (Paris), environ12minutes après le début documenté. Son archive/source17937ba reste conservée séparément. Le paquet final est une continuation, avec source au commit indiqué dans DELIVERY_SUMMARY.json et runtime cumulatif arrêté. Les scripts Windows ne téléchargent rien et ne modifient pas la configuration Desktop ; ils génèrent un candidat à fusionner après sauvegarde.

Les scènes A→E respectent la Bible : parents absents, Maëlle, poursuite avec Shift uniquement si nécessaire, disparition, confrontation, appel puis policier jouable. F demeure UNKNOWN. Le builder Luau retourne un modèle non parenté ; le driver exige Studio, copie approuvée, PlaceId concordant et un seul joueur, puis simule des marqueurs manuels. **Ces scripts n'ont pas été exécutés dans Studio ; ni IA, voix, personnages réalistes ni changement d'avatar automatique validés.**

## Mission forêt autorisée

Autorisation explicite : une mission isolée de900s,120s de calcul supplémentaires,8HTTP supplémentaires,32Mio de contenu, sans modèle/service/achat/publication. Activation11h54m11, échéance12h09m11 Paris. Le worker indépendant supervisé a exécuté six étapes en30,27s : collecte ciblée → fiches → essai Python → Blender → coffre Obsidian → MCP. Les étapes terminées ne signifient pas une recherche complète : neige CANDIDATE_ONLY/PARTIAL, matériaux réutilisés en mémoire, aucune nouvelle connaissance promue vérifiée.

Le worker a fait1nouvelHTTP ; les diagnostics dirigés ensuite par Codex ont ajouté3HTTP (robots/page officielle puis recapture de l'article). Total4. Les écritures de données externes et les journaux Blender sont antérieurs à l'échéance ; la clôture administrative a été écrite à12h10m18. Aucun travail externe nouveau après échéance.

Calcul :77,058307807→103,751822960s, delta26,693515153s≤120. HTTP9→13. Deux tentatives directes diagnostiques ne passaient pas par RootCollector.fetch_attempt : compteur HTTP exact ; compteur fetch réconcilié de7à9 par correction monotone documentée dans la copie. V10 reste à77,058s/60 et9HTTP/5fetch, V9 à59,596s/60. La politique temporaire est refermée, politique60s restaurée sans diminuer le ledger, mission/control arrêtés, activation autonome et schedule désactivés.32Mio restent pour conserver ces preuves ; ce n'est pas un budget récurrent.

## Expérience réelle : neige et export

Deux profils propres de laboratoire (proposés3m/8étages et1,8m/6étages), seed13, même caméra/lumière,256², Cycles CPU1thread/2samples. A : neige géométrique « caps ». B : masque procédural dépendant de la normale. ExportGLB et import dans un nouveau processus Blender4.3.2.

PremierB invalide comme comparaison : seuil source0,65 rendait toutes les faces blanches. La décision initiale est conservée, puis qualifiée INVALID_NATIVE_COMPARISON ; elle ne prouve pas une perte à l'export. Codex a corrigé le protocole, avant nouvelle exécution, vers seuil source0,98 afin de créer les deux classes. Aucun critère d'acceptation ni tolérance abaissé. A réutilisé comme contrôle, B régénéré/réimporté. La sourceBv2 contient112/112faces blanc/vert sur le profil principal et84/84sur transfert ; l'import reste blanc sans facteur vert : REJECTED_FOR_THIS_EXPORT.

A conserve facteurs blanc/vert et940/716triangles sur les deux profils : PASS_LIMITED_GLTF, candidat pour prochain essai moteur. Aucune équivalence de rendu complète, performanceFPS, vent, B3/C1, Blender5.2, FBX ou Studio démontré. Les rendus sont des proxies anguleux ; réalisme INCONCLUSIVE. Sélection d'une alternative prédéfinie par runtime ; révision du protocole et code par Codex, pas auto-réparation de code autonome.

## Collecte et citations

Une documentation officielle Blender4.3glTF a révélé un défaut réel : navigation consommant32k avant l'article. Capture originale conservée, HTML brut recapturé légalement dans la fenêtre autorisée, article extrait puis tronqué à32k. Toujours incomplet ; ne prouve ni Blender5.2 ni Roblox. La réparation réelle dans la copie et le correctif du collecteur sont distingués : le correctif intégré est ensuite testé hors ligne. Il conserve les avertissements, refuse les murs d'accès avant extraction et signale les anciennes captures dominées par la navigation. Il ne les supprime pas et ne déclenche pas de réseau implicite. Cette heuristique est explicable, pas un validateur sémantique.

## Mémoire, RAG, MCP et Obsidian

Le runtime livré conserve les résultats et échecs, sans promotion VERIFIED/HUMAN_APPROVED. Un vrai processus stdio retrouve la branche forest/spruce/snow et les deux nouveaux échecs v2 ;27contrats strictement identiques. Les compteurs et configurations restent inchangés par la consultation. Export dans un coffre propre, révisions précédentes sauvegardées, répétition unchanged sans doublon. Le rollback d'export isolé reste couvert par les suites historiques et le précédent paquet ; aucun coffre personnel touché.

Le vérificateur du paquet distingue un seul cache dérivéSQLite pouvant changer après relocalisation des sources immuables ; cache changé signalé, contrôle structurel seulement. L'ancien échec du vérificateur est conservé. Aucun gain Recall/MRR/nDCG, réalisme ou économie du quota Claude annoncé. Desktop et Studio NON TESTÉS. Le cycle approfondi « tutoriel→compréhension visuelle→ressource réaliste→Studio » demeure incomplet.

## Corrections minimales

- agent/mission.py : conserver lab/learning et lab/inbox/learning lors d'une copie/seed/restauration ; ne pas perdre les preuves récentes.
- agent/ocean_web.py et html_content.py : article avant troncature, contrôles d'accès préservés, caches anciens suspects refusés pour collecte avec revue explicite.
- agent/intelligence_evidence.py : ces captures restent accessibles comme contexte, pas affirmations techniques.
- agent/forest_mission.py et script Blender : worker expérimental, référence source discriminante et comparaison limitée ; préflight refuse une session dont le plafond dépasse le budget restant plutôt que constater le dépassement après coup.
- project/research_roots.json : quatre branches ajoutées, toutes PROPOSED, sans prétention de couverture.
- PROLOGUE_START_NOW et tests : vérificateur portable, wrappers, montage manuel Luau proposé et régressions.

Les cas rouges et verts sont dans proofs/. Aucun garde/validateur indépendant existant réécrit. Le scénario personnel copie les nouveaux modèles du paquet dans sa copie jetable ; aucune assertion supprimée. Le Worker forêt exige une préparation de copie gelée dédiée ; pas de nouvelle commande générale activée.

## Tests et limites

634tests hors ligne puis634tests personnels séquentiels réussis ;23nouveaux cas par rapport aux611hérités. Voir proofs/test-summary.json et les logs. Linux/Python3.12.14 réellement exécuté ; suite offline sans sockets, scénario personnel séquentiel et ciblés. Aucune CI Windows du nouveau commit local : pas de push. Les anciens résultats Windows ne valent pas validation de cette continuation. Aucun interpréteur Luau ni application Windows disponible.

## Prochaines actions

1. Extraire le paquet final dans un NOUVEAU dossier Windows, lancer WINDOWS/setup.py verify, doctor puis test-mcp ; sauvegarder la configuration Desktop avant fusion du candidat. Vérifier ensuite les outils dans l'application.
2. Identifier une copie Studio autorisée, son build, rig et contrôleur ; tester les gestes/import/retargeting et les caps comme candidats, sans modification du jeu principal.
3. Monter le témoin A→E avec proxies/marqueurs, remplacer progressivement les événements simulés par comportements observés ; conserver F inconnue. Nouvelle recherche/calcul uniquement sous nouvelle autorisation applicable.
