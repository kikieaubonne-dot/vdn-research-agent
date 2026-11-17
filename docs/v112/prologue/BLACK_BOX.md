# Dossier de réparation et limites — delta V10

Les incidents append-only du runtime restent conservés. Le succès d'une variante n'efface pas le défaut de la méthode initiale ni les incidents exigeant revue humaine.

| Objectif / état | Symptôme et preuve | Diagnostic / prochaines actions |
|---|---|---|
| Export IK — MITIGATED dans Blender4.3.2 | Bras constants dans les anciens GLB malgré la contrainte native ; `proofs/animation-before-after.json` | Bake visuel testé sur deux gabarits ; utiliser la variante réparée dans sa portée. Import/retargeting sur copie du rig Roblox encore à vérifier. |
| Mesure des os — FAIL v1 conservé | Extrémités d'affichage divergent~0,146754 alors que surfaces et joints coïncident | Importeur reconstruit les longueurs. interop-2 mesure matrices de skinning, articulations et surfaces ; tolérance inchangée. Édition/retargeting peut dépendre des tails : ne pas le déclarer identique. |
| Stockage — BLOCKED pour fiche supplémentaire | Réserve1,2Mo refusée ; puis réservation16Ko pour une nouvelle fiche méthode B refusée | Rapports gzip mesurés, aucune suppression/hausse de quota. Continuer les lectures et travaux de développement ; prochaine collecte nécessite capacité autorisée suffisante. |
| Vision — NOT_TESTED | Configuration locale désactivée, aucun modèle exact sélectionné ; tests mockés seulement | Choisir explicitement un modèle installé, mesurer sur un jeu visuel autorisé et les quotas existants. Aucune installation implicite. |
| Prologue — PARTIAL | Inventaire36 ressources et automate de référence ; scène, contrôleur, voix/assets et Studio absents | Assembler A–E en copie réelle, mesurer rythme/compréhension ; ne pas valider la fin F par défaut. |
| Windows/Desktop/Studio — BLOCKED | Environnement cloud seulement | Ouvrir la copie livrée dans l'environnement local autorisé et effectuer le préflight ; aucun transport vers le PC supposé. |

## Reproduction minimale du défaut initial

Ancien fichier : `runtime/lab/inbox/learning/prologue-v2/father_proxy-IK.glb`. Comparer au natif source aux phases0/0,5/1 avec les anciennes inspections conservées. Les rotations des bras du GLB sont constantes. Le contrôleur de bake est `agent.animation_roundtrip`; ses specs, fichiers, journaux et reçus sont liés par empreintes. Les nouveaux résultats se consultent via les deux clés `learning:animation` indiquées dans HANDOFF.md.

Les traces d'échec de développement sont archivées : plan initial créant un verrou malgré `writes:0`, et reçu de comparaison FAIL n'atteignant pas BLACK BOX. Régressions ajoutées avant correction ; simulation de plan désormais sans écriture, et FAIL futur journalisé. Ce sont des défauts du nouveau composant, pas des régressions cachées des587 tests historiques.

## Dix composants critiques

Superviseur, réparateur, restauration, validateur, mémoire des erreurs, Métavision, ordonnanceur, détecteur de régressions, classement et BLACK BOX existants conservés. Aucun auto-patch de leurs protections/permissions. Nouveaux contrôles : source immuable, droits attestés, copie Blender de confiance, chemins sûrs, auto-run désactivé, sortie/temps bornés, cache d'entrées contrôlé, comparaison indépendante et refus avant budget insuffisant. Ces processus ne constituent pas une isolation OS de fichiers Blender hostiles.

Restent non clos : failover OS vivant, pause sous charge utilisateur, holdout réellement caché, entailment sémantique général, compte d'objets auxiliaires de l'ancien inspecteur, agrégation globale des ledgers copiés, panne physique de disque. Les tests verts ne certifient pas leur résolution. Le runtime précédent n'a pas été réactivé et aucun processus permanent ne reste actif.
