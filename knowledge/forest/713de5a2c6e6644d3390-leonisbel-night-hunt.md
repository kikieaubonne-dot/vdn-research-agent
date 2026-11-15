---
id: "vdn-713de5a2c6e6"
title: "leonisbel/night-hunt"
domain: "forest"
subdomain: "forest"
status: "candidat"
tested_in_studio: "non"
confidence: "faible"
confidence_reason: "Ancienne fiche V1–V4 reclassée automatiquement : 1 passage(s) technique(s), source de niveau 3 ; à approfondir et à tester."
engine_version: "inconnue"
source_tier: 3
provider: "github"
official: false
sources:
  - "https://github.com/leonisbel/night-hunt"
accessed: "2026-11-15"
queries:
  - "Roblox realistic night forest lighting fog"
created: "2026-11-15"
updated: "2026-11-15"
tags:
  - "vdn"
  - "forest"
  - "forest"
  - "candidat"
  - "migre-v5"
legacy_status: "a_verifier"
legacy_source_type: "GitHub repositories"
legacy_topic: "forest"
legacy_score_heuristique: 45
legacy_collected_utc: "2026-11-15T12:15:20+00:00"
---

> **Candidat** (reclassement V5 du 2026-11-15) · 1 passage(s) technique(s), source de niveau 3 ; à approfondir et à tester.
> Le contenu historique ci-dessous est conservé tel quel.

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
