# VDN — Laboratoire et sapin A/B

Livraison **préparée**, sans exécution Roblox Studio ou Blender. Aucun `.rbxl`
n’est fabriqué ni publié. Créer manuellement un place privé distinct du jeu
principal, nommé **VDN — Laboratoire**, et neuf dossiers/zones : forêt et végétation,
éclairage, matériaux, personnages, vêtements, animations, gameplay et IA,
importation, performances. Définir l’attribut booléen `Workspace.VDNLab=true`.

## Référence reproductible

```sh
python -m agent.v10 spruce --dry-run
python -m agent.v10 spruce --apply
python -m agent.v10 find "sapin" --detailed
```

Deux identifiants stables dérivés du lot : **A géométrie simplifiée**, **B cartes
de feuillage**. `--batch autre-nom` prépare un nouveau lot. La préparation répétée
ne crée pas de doublon ni ne redémarre une expérience. Les plans contiennent
hypothèse, procédures, contrôles, critères, assets à renseigner et rollback.
[Plan JSON généré](../../examples/v10/spruce-plan.json).

1. Fixer silhouette, dimensions, tronc et quantité de neige cibles. Créer les deux
   prototypes dans Blender ou l’outil choisi ; consigner ses versions et exports.
2. A emploie une géométrie simplifiée pour branches/aiguilles. B emploie des cartes
   et atlas ; consigner alpha, UV et normales. Ce sont des méthodes candidates,
   pas une preuve de la technique originale d’une image.
3. Renseigner appareil, versions, qualité graphique, résolution, caméra, éclairage,
   nombre d’arbres, préchauffage et durée d’échantillonnage. Importer A et B dans
   des modèles isolés `VDNTest_A` et `VDNTest_B`. Désactiver l’autre modèle pendant
   chaque mesure ; garder les autres paramètres identiques.
4. Définir les seuils acceptables **avant** le test, sur l’appareil cible. Répéter
   au moins trois fois en alternant A/B. Conserver mesures brutes et captures.
5. Compter les triangles dans Blender et les octets des exports sur disque.
   Relever matériaux, textures, artefacts et coûts par les outils adaptés.
   La taille FBX ne mesure pas la mémoire GPU ni les octets téléchargés Roblox.
6. Capturer silhouette et rendu nocturne avec caméra identique. La lisibilité
   annotée 1–5 est subjective ; aucune précision physique n’en est déduite.
7. Comparer les répétitions, les limites et les preuves. Aucun gagnant n’est
   automatiquement déclaré. Le retour à l’état initial consiste à supprimer
   les copies du laboratoire, sans toucher au jeu principal.

## Configurer, démarrer et enregistrer

`get ID --detailed` fournit le document et sa révision. Construire un petit JSON
`design.json` avec **parameters, environment, protocol** complets, en conservant
les procédures du plan. Remplacer les contrôles `null`, les assets vides et les
versions inconnues par les conditions réellement utilisées.

```sh
python -m agent.v10 configure EXPERIMENT_UUID --input design.json --revision REVISION --apply
python -m agent.v10 get EXPERIMENT_UUID
python -m agent.v10 transition EXPERIMENT_UUID RUNNING --revision NEW_REVISION --apply
```

La révision est obligatoire pour amender ou démarrer : elle évite d’appliquer
une décision sur un état périmé. Les conditions d’un résultat sont copiées dans
son historique ; un nouvel essai ne réécrit pas les conditions du précédent.

Format manuel : [result-template.json](../../examples/v10/result-template.json).
Remplacer ses annotations d’exemple avant utilisation ; `null` veut dire inconnu,
jamais zéro mesuré. États rapportables : `FAILED` (erreurs obligatoires),
`PARTIAL_SUCCESS`, `SUCCESS`. Le registre ne permet pas `SUCCESS → VERIFIED`
par un simple résultat. Une réussite reste locale et rapportée.

```sh
python -m agent.v10 result EXPERIMENT_UUID --input real-result.json --apply
python -m agent.v10 compare A_UUID B_UUID
```

Comparaison : mesures rapportées côte à côte ; différences numériques seulement
si les contrôles sont présents et identiques, les environnements égaux et les
essais terminés. Elle ne contrôle pas automatiquement les répétitions ni leur
causalité. [Rapport livré](SPRUCE_COMPARISON.md) : résultats absents, gagnant inconnu.

## Collecteur candidat et import

Copier [VDNLabCollector.client.luau](../../roblox/VDNLabCollector.client.luau) dans
`StarterPlayerScripts` du laboratoire. Remplir UUID, méthode, modèle, environnement
et contrôles identiques au design Python. Tester en Play dans Studio. Le script
refuse hors Studio, sans attribut explicite ou sans modèle isolé. Il n’écrit ni
asset, ni réseau, ni code du jeu. Il compte des propriétés matériaux/IDs textures
et échantillonne les intervalles Heartbeat du client. **Heartbeat n’est pas le FPS
rendu** ; triangles, octets, score nocturne, artefacts et temps GPU restent absents.
Les decals et toutes les formes de textures ne sont pas inventoriés par ce script.

Copier uniquement le JSON entre `VDN_MEASUREMENT_BEGIN/END` dans
`lab/inbox/run.json`. L’import est strict : schéma `vdn.roblox-measurement/10`, UUID,
méthode, métriques, observations, erreurs, contrôles et environnement. Il refuse
une méthode ou des conditions différentes de l’expérience `RUNNING`.

```sh
python -m agent.v10 import-measurement lab/inbox/run.json --dry-run
python -m agent.v10 import-measurement lab/inbox/run.json --apply
```

Un rapport importé devient une preuve hachée et un résultat partiel rapporté,
jamais `VERIFIED`. Les mesures absentes deviennent `null`. Le script est relu
contre les API officielles, mais **ni compilé par Luau ni exécuté dans Studio**
ici. Seuls le format Python et ses contrôles d’import sont testés hors ligne.

Références consultées le 16 novembre 2026 :
[RunService](https://create.roblox.com/docs/reference/engine/classes/RunService),
[HttpService JSONEncode](https://create.roblox.com/docs/reference/engine/classes/HttpService#JSONEncode).
Les propriétés du moteur doivent encore être validées dans la version installée.

## Références visuelles

Déposer un PNG dans `lab/inbox`, l’importer comme `external_capture`, puis utiliser
le champ `id` de la preuve :

```sh
python -m agent.v10 artifact lab/inbox/reference.png --kind external_capture --apply
python -m agent.v10 visual-plan ARTIFACT_ID --input examples/v10/manual-visual.json
python -m agent.v10 visual-compare REFERENCE_ID RESULT_ID --input examples/v10/corrections.json
```

Remplacer les exemples par l’inspection réelle. Les observations créent des
sujets à rechercher ; hypothèses et incertitudes restent séparées. Les corrections
sont classées par impact humain/modèle, sans score perceptuel inventé. Mesures
objectives : octets, hash et dimensions d’en-tête PNG seulement, sans décodage
des pixels ni calibration du monde. Aucun modèle visuel n’a analysé de forêt ici.
`--backend local|remote` active l’adaptateur configuré, jamais par défaut.
