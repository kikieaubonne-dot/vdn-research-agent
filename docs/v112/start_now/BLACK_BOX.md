# BLACK BOX — delta V11

Les20incidents ouverts annoncés par V10 ne sont pas clôturés globalement par cette livraison : consulter docs/v112/prologue/BLACK_BOX.md et les journaux hérités.

| Incident | Cause et gravité | État / prochaine action |
|---|---|---|
| Copie de mission omettant lab/learning et lab/inbox/learning | HIGH : reçus/artefacts récents absents de la nouvelle copie | CORRIGÉ ; régression rouge conservée, copie et compteurs vérifiés |
| Vérificateur du premier pack refusant le SQLite reconstruit après déplacement | MEDIUM : cache dérivé confondu avec source immuable | CORRIGÉ ; un seul chemin de cache explicitement signalé et contrôle SQLite, sources/compteurs toujours immuables |
| Capture HTML consommée par la navigation | HIGH : limite32k appliquée avant sélection de l'article | CORRIGÉ logiciel ; capture officielle réparée dans la copie, ancienne conservée ; autres captures suspectes à revoir sans nouveau réseau implicite |
| Premier essai procédural non discriminant | MEDIUM : seuil source0,65 ne créait aucun feuillage vert | Qualification INVALID_NATIVE_COMPARISON conservée ; protocolev2 fixé avant exécution, seuil source0,98, critères d'acceptation inchangés |
| Perte de couleur procédurale GLB v2 | MEDIUM : shader source non encodé dans les simples facteurs de matériaux exportés | OUVERT, REJET POUR CE PIPELINE ; choisir les caps pour le prochain essai moteur, ou prévoir un bake texture séparé autorisé |
| Deux collectes diagnostiques directes sans fetch_attempt externe | MEDIUM : le compteur HTTP était exact mais le compteur de tentatives dépend de l'appelant RootCollector | RÉCONCILIÉ +2 dans la copie isolée, sans diminution. Pour toute future collecte directe, réserver fetch_attempt avant l'opération ; ne pas doubler le RootCollector existant |
| Windows/Desktop/Studio et assets cibles absents | HIGH pour la réception terrain | BLOQUÉ ; exécuter WINDOWS/setup.py puis identifier une copie de scène et son rig/contrôleur autorisés |
| Réalisme et performance des sapins | MEDIUM : proxies géométriques seulement | NON TESTÉ sur moteur ; aucun FPS, performance mobile, vent, résultat B3/C1 ou appréciation artistique favorable inventé |

Aucune réparation critique, installation, garde-fou ou permission automatiquement modifié. Les sources Internet restent des données ; aucune commande générée à partir de leurs instructions.
