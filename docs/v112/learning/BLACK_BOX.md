# Frontières impactées et risques ouverts

Audit delta des dix composants ; les protections historiques ne sont pas réécrites. La suite complète épinglée couvre leur non-régression logicielle, pas une panne physique globale.

| Composant | Frontière conservée / preuve | Risque et action |
|---|---|---|
| Superviseur | Lease du parent, arrêt groupe possédé, verrou global inchangés | MEDIUM : deux suites de tests simultanées se bloquent volontairement. Exécuter les campagnes séquentiellement. Pas de preuve OS Windows. |
| Auto-réparation | Limite2 et refus de modification critique inchangés | HIGH : IK GLB perd le geste ; aucune auto-réparation ou promotion. Tester un bake dans une nouvelle variante. |
| Restauration | Image approuvée vers copie désactivée conservée | MEDIUM : nouvelle version non approuvée automatiquement ; failover vivant non validé. |
| Validateur indépendant | Inventaire et critères inchangés, fichiers épinglés avant suite | MEDIUM : holdout caché absent ; auto-évaluation sémantique non prouvée. |
| Mémoire d'erreurs | Échecs initiaux et résultats partiels conservés ; empreintes entrées/sidecars | MEDIUM : empreintes ≠ preuve de vérité ni protection contre propriétaire OS malveillant. |
| Métavision | Résultats numériques séparés du jugement visuel | HIGH : pas de vision/transcription locale opérationnelle ; esthétique INCONCLUSIVE. Les PNG ne prouvent pas le réalisme. |
| Ordonnanceur | Aucun mode permanent ajouté ; quotas conservés | MEDIUM : calcul59,596/60s, STOPPED. Aucun travail futur fictif ou nouvelle enveloppe détournée. |
| Détecteur de régressions | Gate de poses et tests mauvais export/entrées obsolètes | HIGH : seules3 poses/1 landmark, autres déformations non couvertes. Le bake proposé reste non exécuté. |
| Classement/recherche | Aucun changement RAG ; comparaison candidate bornée et source non fiable | MEDIUM : découverte d'outils automatique non livrée ; registre opérateur seulement, pas de gain Recall/MRR revendiqué. |
| BLACK BOX | Incidents et journaux expurgés, secours historiques préservés | MEDIUM : ENOSPC total matériel reste ouvert ; aucun log local ne garantit la survie du disque. |

Autres anomalies : l'importeur ajoute un objet auxiliaire80 triangles, non reconnu par notre règle conservatrice dans cet essai. Afficher à la fois les752 triangles de scène et les672 du payload ; ne pas supprimer par nom. Source `.blend` tierce : `--disable-autoexec` n'est pas un bac à sable OS ; exiger une copie explicitement attestée et une isolation adaptée. OBJ/FBX non exécutés dans cette reprise.

Les incidents de l'essai initial de chemin relatif, du stockage, des images de fin et de la perte de pose restent dans les preuves ; aucune clôture automatique de risque nécessitant revue humaine. Les dix composants n'ont pas reçu une nouvelle certification globale.
