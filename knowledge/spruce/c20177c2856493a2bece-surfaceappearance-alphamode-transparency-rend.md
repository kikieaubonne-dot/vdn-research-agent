---
id: "vdn-319f4403f590"
title: "SurfaceAppearance AlphaMode.Transparency renders in bands on opaque MeshParts"
domain: "vegetation"
subdomain: "spruce"
status: "documente"
tested_in_studio: "non"
confidence: "faible"
confidence_reason: "Ancienne fiche V1–V4 reclassée automatiquement : 4 passages techniques extraits d'une source de niveau 2 ; aucun test dans Roblox Studio."
engine_version: "inconnue"
source_tier: 2
provider: "devforum"
official: false
sources:
  - "https://devforum.roblox.com/t/4822477"
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
legacy_score_heuristique: 55
legacy_collected_utc: "2026-11-15T12:15:20+00:00"
---

> **Documenté** (reclassement V5 du 2026-11-15) · 4 passages techniques extraits d'une source de niveau 2 ; aucun test dans Roblox Studio.
> Le contenu historique ci-dessous est conservé tel quel.

# SurfaceAppearance AlphaMode.Transparency renders in bands on opaque MeshParts

**Sujet :** Épicéa enneigé réaliste

**Source :** [Roblox DevForum](https://devforum.roblox.com/t/surfaceappearance-alphamodetransparency-renders-in-bands-on-opaque-meshparts/4822477)

**Question de recherche :** Roblox SurfaceAppearance transparency foliage

## Extrait de découverte (non vérifié)

Alpha gradients in a SurfaceAppearance ColorMap render as hard bands instead of a smooth falloff when the MeshPart is fully opaque. Anywhere the alpha channel ramps from opaque to transparent you get visible stepping and a jittery, unstable transition rather than a clean gradient. Examples Two th...

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

**Source lue :** https://devforum.roblox.com/t/surfaceappearance-alphamodetransparency-renders-in-bands-on-opaque-meshparts/4822477  
**Contenu :** DevForum  
**Passages candidats :** 5

### Passages et paramètres repérés

- Examples 1098×1117 56.3 KB Two things narrow this down a lot: It does not happen on Decal or Texture .
- At Transparency = 0.011 it renders correctly.
- This looks like a blend-mode or sort-order selection issue rather than a hardware or texture-format limitation, which means it’s solvable.
- The 0.011 transparency trick is not a usable workaround.
- Impact This rules out a large amount of what AlphaMode.Transparency is supposed to enable for in-game assets: soft edges, dissolves, fades, foliage cards, glass falloff, wear and decay effects, and layered surface detail.

### Questions de recherche complémentaires

- spruce Roblox texture implementation limitations troubleshooting
- spruce Roblox transparency implementation limitations troubleshooting
- spruce Roblox texture implementation limitations troubleshooting

### Validation requise

- [ ] Vérifier chaque passage dans la source complète
- [ ] Confirmer les limitations Roblox actuelles
- [ ] Tester dans Roblox Studio ET Roblox Player
- [ ] Mesurer qualité et performance
