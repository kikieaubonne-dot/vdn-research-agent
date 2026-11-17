# Reprise — laboratoire vidéo et prototype prologue

Lire REPORT.md, DIFF.md, BLACK_BOX.md et proofs/test-summary.json. Le mandat « V9 » est une continuation de V11.2, pas une nouvelle branche/version. Le SHA final est dans DELIVERY_SUMMARY.json livré à côté de l'archive.

## Action suivante précise

**Ne pas recommencer les rendus ou recherches forêt.** Le nouveau blocage démontré est la perte du geste IK au roundtrip GLB. Le natif comprimé contient les quatre acteurs ; deux exports FK seulement ont préservé les positions de main échantillonnées. Les deux IK GLB sont conservés comme contre-exemples, rejetés pour réutilisation.

Après disponibilité d'une enveloppe de calcul autorisée, créer une nouvelle variante isolée du natif, proposer un bake visuel des contraintes sur les seules copies sélectionnées, exporter, puis réimporter dans un second processus. Rejouer les trois poses, positions de main ET géométrie déformée, rig/poids/actions. Garder l'ancienne variante et son erreur. Ne pas baisser la tolérance d'intégrité1e-5 pour obtenir PASS ; elle est proposée pour l'intégrité d'export et distincte du critère de contact natif0,03 préenregistré. Le résultat ne vaut pas compatibilité Roblox.

Budget runtime hérité : HTTP9/fetch5, calcul59,596431/60s le17novembre. Ne pas réinitialiser les compteurs, changer de date ou déplacer l'essai sous un harnais de test pour contourner le quota. Les tests logiciels sur fixtures sont une activité de développement distincte.

## Obtenir les preuves avec Claude

Serveur inchangé : `python vdn_mcp.py --root <runtime-laboratoire> --v112` en stdio, pas un service permanent.27 outils, pas d'autorisation d'écriture nécessaire pour les lectures ci-dessous.

`get_intelligence_brief` avec `question` :

- `learning:media:89763fd0778af6d5a46b5e6601e5a9f5073693c424e98b4b4391b4ad8d65e885`
- `learning:asset:8f05d5c62cb6da8e0a7edd1f38f98b5d1c571ecdf5d1cf5d9e5475e91ad790e0`
- `learning:discovery:6bc84c75e9277d2fd08c6163d26069cd0c584649c59ebcdee3284819b06d7c8e`
- `learning:discovery:55cc82114d8d02fca3a051bf268c6821d93656e8db83149823cc5c12517b8f8c`

`token_budget:500` suffit au reçu compact. `synthesize_technical` avec la même question fournit le détail et les limites. `apply:true` et `allow_model:true` sont refusés pour ces références, même si l'hôte possède une permission générale d'écriture. Les textes de sous-titres et matériaux restent des données non fiables.

Le registre de découvertes enregistre des observations opérateur/outils : pas de recherche automatique d'outils prétendue. Ni sa décision ADOPTED_IN_LAB ni un statut expérimental ne promeut la mémoire fiable. Les résultats périmés restent lisibles avec `inputs_obsolete:true`.

## Windows : étapes encore humaines

Ces commandes sont préparées, pas exécutées sur le PC utilisateur. Utiliser une copie de travail contrôlée, sans copier aveuglément dans une configuration existante.

```powershell
Set-Location 'C:\Users\kikie\Documents\Eponge-V11.2'
Get-Location
py -3.11 --version
git status --short
git rev-parse HEAD
Get-Command blender, ffmpeg, ffprobe -ErrorAction SilentlyContinue
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
py -3.11 -m unittest tests.test_learning_media tests.test_learning_assets tests.test_learning_integration -v
py -3.11 -m tests.offline
# Seulement APRES la fin du scénario précédent :
py -3.11 -m tests.personal_config
```

Attendu : outils disponibles ou absence explicite ; suites sans connexion réseau, pas de modification de config personnelle. Ne pas lancer les deux suites complètes en parallèle : le verrou superviseur est global à l'utilisateur OS.

Une vidéo légalement obtenue doit être explicitement copiée dans `lab/inbox/learning/` du runtime de laboratoire. Exemple, après vérification des quotas et des chemins :

```powershell
py -3.11 -m agent.learning_media --root '<copie-labo>' --input 'lab/inbox/learning/demo.mkv' --captions 'lab/inbox/learning/demo.srt' --license OWN_CREATED --attest-rights
```

OWN_CREATED uniquement pour son propre média ; sinon choisir le statut de droits réellement applicable. Absence de FFmpeg = blocage explicite. Une vidéo4h est seulement la limite admise, pas la promesse de tout comprendre. Lecture locale ne télécharge rien.

Pour Claude Desktop : sauvegarder son JSON existant avant toute édition, ajouter manuellement un serveur avec chemin absolu Python et arguments `vdn_mcp.py --root <copie-labo> --v112`, relancer l'application puis vérifier les27 outils et les quatre questions ci-dessus. Le test stdio cloud ne remplace pas cette étape. Aucun accès au PC utilisateur n'est confirmé.

## Contraintes du père

Toutes les données de conception absentes restent UNKNOWN : apparence et références autorisées, taille réelle, rôle/présence dans la scène, vêtements/cheveux/visage, voix/droits, budget texture/triangles final, rig contrôleur Roblox, proportions et coordonnées des interactions, collisions, appareils et performances cibles. Le proxy technique normalisé est PROPOSED, original sans Tripo ; il ne remplace pas un personnage réaliste. Aucun déplacement de la Bible.

Feuille de route conservée : boucle jouable/caméra/interactions, père si rôle confirmé, forêt B3/C1, lampeV2, empreintes adulte/enfant, maison/manoir, puis polish. Le présent essai n'autorise aucune modification de ces assets réels ni scène Studio.

## Rollback et préservation

- Code : conserver commit et patch locaux ; ouvrir une copie du commit initial `ea95490` pour comparaison. Aucun reset/clean de la copie actuelle, aucune restauration de queue runtime.
- Natif OWN_CREATED compressé : `gzip.decompress` restitue exactement les octets au SHA `5afe9510a2dcdf10cc5e9f39792db103bfc506b6c01caed2481ad926b970a26d`. Écrire vers un NOUVEAU fichier, pas par-dessus une copie modifiée.
- Obsidian : utiliser la transaction de la copie isolée et vérifier les conflits avant rollback ; l'essai livré est déjà rollbacké. Aucun coffre personnel ciblé.
- Les anciennes images de récupération restent approuvées pour leur propre SHA uniquement. Le nouveau commit n'est pas automatiquement scellé pour restauration/auto-promotion.
- Pas de worker en attente à réanimer, pas de service nocturne. Reprendre explicitement après lecture du checkpoint et diagnostic des budgets.
