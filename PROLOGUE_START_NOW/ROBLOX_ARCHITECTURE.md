# Architecture PROPOSÉE — copie Studio seulement

Tous les noms ci-dessous sont proposés, pas les noms des composants existants du jeu. Préserver le contrôleur et les assets actuels tant qu'ils n'ont pas été inspectés.

```text
ServerStorage
  EpongePrologueLabModules_PROPOSED
    Progression       ModuleScript ← ROBLOX/Progression.lua
    StarterLab        ModuleScript ← ROBLOX/StarterLab.lua
    LabDriver         ModuleScript ← ROBLOX/LabDriver.lua
Workspace
  EpongePrologueLab_PROPOSED       ← modèle retourné puis inséré explicitement
    A_Maison / B_Poursuite / C_Confrontation / D_Appel / E_Enqueteur
```

Le builder crée uniquement des objets nouveaux, sans téléchargement d'asset, audio, publication, changement global d'éclairage ou modification du contrôleur. Les cubes Maëlle/menace/enquêteur sont des repères non riggés, pas des personnages terminés. Les cinq sols et positions sont des paramètres de laboratoire proposés.

Le serveur de production futur doit conserver l'autorité sur les événements, vérifier acteur/distance/état/conditions, appliquer un identifiant idempotent et sauvegarder un checkpoint à frontière sûre. Le module de progression existant est une référence simple ; il ne remplace ni validation serveur, ni stockage durable dans Roblox, ni mécanisme de sauvegarde multi-joueur.

Le harnais manuel est réservé à Studio mono-joueur et nécessite une approbation explicite de copie avec PlaceId attendu. Il vérifie distance/personnage vivant et rejette les événements hors ordre. Il expose l'état de prévisualisation en attributs du modèle. Il ne prétend pas exécuter une poursuite, une chute, des voix ou un changement de personnage.

Lors de la production : séparer le contrôleur de scène, les objectifs/UI, les événements audio, la caméra et les acteurs. Consulter les ressources partagées avant toute nouvelle recherche. Le vrai contrôleur, les API internes, scripts et formats d'import restent UNKNOWN tant qu'inspectés.
