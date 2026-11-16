# Image et description : frontière de preuve

Aucun modèle visuel local ni image réelle n'a été analysé dans cette mission.
L'association d'images existante est conservée : fichiers bornés sous lab/inbox,
SHA/artefacts, cible, éléments à garder/éviter, version et avis humain. Le contrôle
d'entête n'est pas un décodage ou une analyse multimodale.

Le nouveau fallback accepte une description structurée **fournie par l'opérateur
ou Claude**. Il conserve observations rapportées, inférences HYPOTHESIS, inconnues,
contraintes et références déjà associées. Il propose jusqu'à six tâches techniques
par mots/ancres, sans exécuter réseau, modèle, code ou laboratoire.

Exemple de fichier privé JSON :

```json
{"description":"Forêt enneigée, silhouettes irrégulières et faisceau nocturne","observed":["Branches irrégulières décrites par l’opérateur"],"inferred":["La géométrie pourrait contribuer"],"unknown":["Asset et rendu non inspectés"],"keep":["silhouette"],"avoid":["répétition"],"reference_hashes":[],"provenance":"operator_description"}
```

```powershell
& $python -m agent.v112 visual-describe trees --input C:\lab\description.json
& $python -m agent.v112 visual-describe trees --input C:\lab\description.json --apply
```

Une référence SHA inconnue est refusée. Sans image, la description seule est
permise mais `visual_analysis_performed=false`. La dernière description rapportée
et les empreintes entrent dans le contexte/cache de tâche ; ses contraintes ne
sont pas une preuve de compatibilité moteur. Les révisions sont conservées, huit
maximum par tâche, sous le stockage privé projet, jamais dans le corpus primaire.

Étape suivante explicite : consulter les tâches proposées, inspecter leurs sources,
préparer une recherche bornée et un test isolé, puis comparer les vrais rendus.
Composition, densité, neige, sol, ciel, brouillard et lumière peuvent être des champs
d'observation humaine ; aucun détecteur de ces éléments n'est revendiqué.

Un modèle visuel futur doit être choisi avec modèles réellement installés,
licence, contexte et mémoire de la RTX 4060 Ti 8 Go observés. Pas de téléchargement
implicite ni promesse de tenue VRAM. Ne pas copier les assets d'une référence AAA.
