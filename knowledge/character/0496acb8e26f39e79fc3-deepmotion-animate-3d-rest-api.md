---
status: a_verifier
source_type: "GitHub repositories"
topic: "character"
score_heuristique: 41
collected_utc: "2026-11-15T15:38:51+00:00"
---

# DeepMotion/Animate-3D-REST-API

**Sujet :** Personnages réalistes Roblox

**Source :** [GitHub repositories](https://github.com/DeepMotion/Animate-3D-REST-API)

**Question de recherche :** Roblox skinned mesh facial animation

## Extrait de découverte (non vérifié)

The Animate 3D REST API can be used to create 3D animations, download FBX, BVH, and other formats, and much more.

## Vérification Roblox / Blender

- [ ] Ouvrir et lire la source complète
- [ ] Vérifier la version du moteur et les limites techniques
- [ ] Extraire une procédure précise, des paramètres et les prérequis
- [ ] Tester dans Blender puis Roblox Studio
- [ ] Mesurer visuel, performances et reproductibilité

## Résultat du test

À compléter après expérimentation.

## Analyse V2 — lecture partielle de la source

**Statut :** extrait source consulté ; conclusions non validées dans Roblox.

**Contenu accessible :** GitHub ; 0 publication(s) examinée(s).

### Passages techniques repérés (citations à contrôler dans la source)

Aucun passage technique précis extrait automatiquement.

### Questions à approfondir

Lecture humaine nécessaire pour définir les questions.

### Limites et validation

- Lecture automatique limitée : pas une revue exhaustive de la discussion.

- Aucune solution technique n’est déclarée confirmée.

- Les expériences Blender/Roblox Player restent à effectuer.

- Les extraits sont des indices, pas des instructions garanties.

## Analyse V3 — éléments techniques à vérifier

**Statut :** passages candidats extraits de la source, **non validés** dans Roblox.

**Source lue :** https://github.com/DeepMotion/Animate-3D-REST-API  
**Contenu :** GitHub README  
**Passages candidats :** 5

### Passages et paramètres repérés

- "params": [ "config=configDefault","formats=bvh,fbx,mp4","model=your_model_id_string" ]
- For static pose, png/jpg can be included in the formats parameter, like: formats=bvh,fbx,png (to output rendered image instead of rendered video)
- For example, if your input video speed moves at 1/2 speed, then set the speed multiplier to 2x to improve animation quality
- **render.bgColor=0,177,64,0** (RGBA color code in the range of 0-255 for each channel, please note, the last channel (alpha) value is not in effect )
- For example, if a processor outputs both bvh and fbx files, then the download link object will look like:

### Questions de recherche complémentaires

- character Roblox fbx implementation limitations troubleshooting
- character Roblox fbx implementation limitations troubleshooting
- character Roblox animation implementation limitations troubleshooting

### Validation requise

- [ ] Vérifier chaque passage dans la source complète
- [ ] Confirmer les limitations Roblox actuelles
- [ ] Tester dans Roblox Studio ET Roblox Player
- [ ] Mesurer qualité et performance
