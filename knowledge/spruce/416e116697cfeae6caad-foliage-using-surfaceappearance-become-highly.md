---
id: "vdn-9f9338e2736f"
title: "Foliage Using SurfaceAppearance Become Highly Transparent at Distance in Roblox Player (Graphics +9) but Renders Correctly in Studio"
domain: "vegetation"
subdomain: "spruce"
status: "documente"
tested_in_studio: "non"
confidence: "faible"
confidence_reason: "Ancienne fiche V1–V4 reclassée automatiquement : 2 passages techniques extraits d'une source de niveau 2 ; aucun test dans Roblox Studio."
engine_version: "inconnue"
source_tier: 2
provider: "devforum"
official: false
sources:
  - "https://devforum.roblox.com/t/4525371"
accessed: "2026-11-15"
queries:
  - "Roblox SurfaceAppearance transparency foliage"
created: "2026-11-15"
updated: "2026-11-15"
tags:
  - "vdn"
  - "vegetation"
  - "spruce"
  - "documente"
  - "migre-v5"
legacy_status: "a_verifier"
legacy_source_type: "Roblox DevForum"
legacy_topic: "spruce"
legacy_score_heuristique: 75
legacy_collected_utc: "2026-11-15T12:15:20+00:00"
---

> **Documenté** (reclassement V5 du 2026-11-15) · 2 passages techniques extraits d'une source de niveau 2 ; aucun test dans Roblox Studio.
> Le contenu historique ci-dessous est conservé tel quel.

# Foliage Using SurfaceAppearance Become Highly Transparent at Distance in Roblox Player (Graphics +9) but Renders Correctly in Studio

**Sujet :** Épicéa enneigé réaliste

**Source :** [Roblox DevForum](https://devforum.roblox.com/t/foliage-using-surfaceappearance-become-highly-transparent-at-distance-in-roblox-player-graphics-9-but-renders-correctly-in-studio/4525371)

**Question de recherche :** Roblox SurfaceAppearance transparency foliage

## Extrait de découverte (non vérifié)

Foliage meshes using SurfaceAppearances with "Transparency" AlphaMode will render correctly in Roblox Studio regardless of Editor Quality Level, but become incorrectly transparent when viewed from a distance in the Roblox Player. In studio the leaves in my scene appear dense and opaque, as expect...

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

**Source lue :** https://devforum.roblox.com/t/foliage-using-surfaceappearance-become-highly-transparent-at-distance-in-roblox-player-graphics-9-but-renders-correctly-in-studio/4525371  
**Contenu :** DevForum  
**Passages candidats :** 2

### Passages et paramètres repérés

- The transparency change appears to happen gradually with distance from the camera.
- I tested each render fidelity setting, it had no impact.

### Questions de recherche complémentaires

- spruce Roblox transparency implementation limitations troubleshooting
- spruce Roblox render implementation limitations troubleshooting

### Validation requise

- [ ] Vérifier chaque passage dans la source complète
- [ ] Confirmer les limitations Roblox actuelles
- [ ] Tester dans Roblox Studio ET Roblox Player
- [ ] Mesurer qualité et performance
