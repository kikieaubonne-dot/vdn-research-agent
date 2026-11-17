# Importer les gestes — portée et essai cible

Disponibles : ASSETS/gesture-primary.blend/.glb et gesture-transfer.blend/.glb. Le principal contient aussi d'autres anciens acteurs : seul father_proxy-IK y est la variante réparée. Le transfert est isolé. Ces noms ne confirment aucun personnage narratif.

Réellement vérifié : bake visuel Blender4.3.2, réouverture et import GLB dans un processus distinct,25 poses, articulations/matrices de déformation/surfaces/triangles et2s. Tolérance1e-5 ; erreurs contrôlées<1e-6. Les extrémités d'affichage d'os sont reconstruites par l'importeur ; leur écart et le premier FAIL restent dans PROOFS.

Procédure PROPOSÉE sur cible :

1. Copier un rig Roblox autorisé et relever noms/hiérarchie, pose de repos, échelle, build Studio et Blender réel. Garder un témoin ; ne pas mapper le rig16 os du laboratoire à R15 sans inspection.
2. Vérifier le format accepté par le pipeline Studio réel dans la documentation/outil accessible. GLB n'est ici qu'un intermédiaire Blender validé. FBX, export/import Studio et retargeting restent NON TESTÉS.
3. Sur copie Blender, choisir seulement l'acteur et ses meshes ; conserver les2s et les poses de référence. Préparer un bake visuel si contraintes ; n'exporter ni les autres acteurs ni des cibles non nécessaires.
4. Réimporter le format choisi dans une scène vierge et mesurer trajectoires/temps avant d'entrer dans Studio. Comparer joints et déformation, pas seulement présence d'un rig/action ou extrémités d'affichage.
5. Importer sur la copie du rig Studio. Vérifier idle, début/milieu/fin du geste, transitions, ancrages et contrôleur. Enregistrer les erreurs ; pas de résultat ni FPS inventé.
6. En cas d'échec : conserver fichier, versions, réglages, logs et conditions ; revenir au témoin. Une réussite Blender ne devient jamais TESTED_IN_ROBLOX.

Aucune nouvelle expérience Blender n'est autorisée par le budget épuisé de la livraison. Le contrôleur agent.animation_roundtrip peut préparer un plan sans apply ; une nouvelle enveloppe nécessite l'autorisation prévue, sans remise à zéro historique.
