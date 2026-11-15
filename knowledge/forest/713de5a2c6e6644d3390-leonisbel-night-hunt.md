---
status: a_verifier
source_type: "GitHub repositories"
topic: "forest"
score_heuristique: 45
collected_utc: "2026-11-15T12:15:20+00:00"
---

# leonisbel/night-hunt

**Sujet :** Forêt nocturne enneigée

**Source :** [GitHub repositories](https://github.com/leonisbel/night-hunt)

**Question de recherche :** Roblox realistic night forest lighting fog

## Extrait de découverte (non vérifié)

Night Hunt - fan-made multiplayer monster survival game

## Vérification Roblox / Blender

- [ ] Ouvrir et lire la source complète
- [ ] Vérifier la version du moteur et les limites techniques
- [ ] Extraire une procédure précise, des paramètres et les prérequis
- [ ] Tester dans Blender puis Roblox Studio
- [ ] Mesurer visuel, performances et reproductibilité

## Résultat du test

À compléter après expérimentation.

## Analyse V3 — éléments techniques à vérifier

**Statut :** passages candidats extraits de la source, **non validés** dans Roblox.

**Source lue :** https://github.com/leonisbel/night-hunt  
**Contenu :** GitHub README  
**Passages candidats :** 5

### Passages et paramètres repérés

- - **Volumetric fog and god rays:** moonlight shafts through the trees use the shadow map, and your flashlight beam lights the fog, with its own shadows.
- - **Dense foliage:** trees are rebuilt from alpha-card leaves and needles cut from plant scans.
- - **PBR surfaces on every monster:** each body part is mapped to a real material: animatronic teddy fur and rusted endoskeletons, scaly reptile hide with pale-belly countershading, wet glossy shark and sea-monster skin with clearcoat, slick Demogorgon skin, weathered gargoyle stone, dried Siren Head flesh, rubbery Cartoon Cat ink, see-through wing membranes and glossy eyes.
- - **Lighting:** a moonlit environment map adds reflections and specular highlights.
- - **Better anatomy:** smoother, curved (PN-triangle) silhouettes and smooth normals on the CC0 dinosaurs, sharks and dragons, and rounded joints on every limb.

### Questions de recherche complémentaires

- forest Roblox shadow implementation limitations troubleshooting
- forest Roblox foliage implementation limitations troubleshooting
- forest Roblox material implementation limitations troubleshooting

### Validation requise

- [ ] Vérifier chaque passage dans la source complète
- [ ] Confirmer les limitations Roblox actuelles
- [ ] Tester dans Roblox Studio ET Roblox Player
- [ ] Mesurer qualité et performance
