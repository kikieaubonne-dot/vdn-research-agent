# Première boucle expérimentale

La recherche prépare une proposition ; le laboratoire conserve les observations,
les conditions, les artefacts hachés et les limites. `SUCCESS`/`PARTIAL_SUCCESS`
ne signifient jamais `VERIFIED`. Les mesures ne modifient aucun jeu publié.

## Démonstration réelle reproductible

Avec Blender installé :

```powershell
& $python -m bench.measure_blender_ocean --blender "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" --output work\blender-demo-v11
```

Adapter le chemin à l'installation réelle. Le bench crée un laboratoire et un
profil Blender temporaires, exécute `--background --factory-startup
--disable-autoexec`, génère deux géométries primitives puis importe et compare
leurs rapports. Il ne sauve aucun `.blend` et n'ouvre pas les assets du jeu.
Employer une nouvelle destination de rapport pour chaque démonstration.

Exécution effective ici : **Blender 4.3.2**, pas 5.2 ; DEMO_A **42 triangles**,
DEMO_B **58**, deux objets, un matériau, dimensions 2 × 2 × 4 m chacun.
[Rapport et comparaison](blender-isolated/comparison.json),
[journal du processus](blender-isolated/blender.log), deux rapports bruts dans
le même dossier. Résultats `PARTIAL_SUCCESS`, aucun gagnant, aucun FPS ni rendu
visuel évalué. Les tests qui relisent ces rapports les identifient comme fixtures
pour ce test ; ils ne revendiquent pas de nouvelle exécution Blender.

## B3 et C1 : entrées manquantes

```powershell
& $python -m agent.v11 lab-prepare --dry-run
& $python -m agent.v11 lab-prepare --apply
```

Ces commandes préparent deux expériences, pas des résultats. Fournir des copies
locales B3/C1 autorisées, versions Blender/Studio, unités, méthode de comptage,
appareil, caméra et contrôles identiques. Aucun fichier B3/C1 n'était disponible.

Pour une mesure d'asset réel, utiliser une copie de confiance : un `.blend`
inconnu peut être hostile malgré la désactivation d'autoexec. Préparer via
`LabStore.configure` ou les outils Lab MCP les mêmes `environment` et
`protocol.controls` (`blender_version`, `unit_scale`,
`measurement_method="evaluated_loop_triangles_v1"`), puis la transition
`RUNNING`. Voir l'exemple exécutable `bench/measure_blender_ocean.py` pour
l'enchaînement exact du contrat.

Depuis la racine du laboratoire isolé, la commande de collecte est :

```powershell
& "CHEMIN\blender.exe" --background "COPIE_LOCALE\B3.blend" --disable-autoexec --python "CHEMIN_DEPOT\scripts\blender_ocean_measure.py" -- --experiment-a UUID_B3 --method B3 --output-dir lab/inbox
& $python -m agent.v11 --root "CHEMIN_LAB" lab-import lab/inbox/blender-B3.json --dry-run
& $python -m agent.v11 --root "CHEMIN_LAB" lab-import lab/inbox/blender-B3.json --apply
& $python -m agent.v11 --root "CHEMIN_LAB" lab-compare UUID_B3 UUID_C1
```

Le collecteur mesure les meshes évalués/loop triangles, objets, matériaux et
dimensions mondiales en mètres. Pas d'édition ni sauvegarde du fichier ouvert.
Sortie créée sans écrasement, uniquement sous `lab/inbox`, sans symlink/escape.
L'import exige UUID, méthode, conditions identiques à l'expérience RUNNING,
valeurs finies/cohérentes, provenance et observations. Rejouer le même rapport
est idempotent ; un import est un témoignage d'opérateur, pas une attestation
cryptographique du processus qui l'a produit.

## Roblox et captures

Roblox Studio indisponible ici. Réutiliser le [protocole V10](../v10/LAB.md),
les artefacts/images et `roblox/VDNLabCollector.client.luau` pour des mesures
explicitement exécutées dans une place de laboratoire autorisée. Conserver
résolution, appareil, caméra, contrôles et version ; comparer seulement des
conditions identiques. Aucune mesure Studio, capture du jeu, édition autonome
d'asset, validation visuelle ou publication Roblox n'est revendiquée en V11.
