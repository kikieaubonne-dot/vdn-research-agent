---
id: "vdn-4b3e4c63ddab"
title: "nightcycle/quick-part"
domain: "vegetation"
subdomain: "spruce"
status: "candidat"
tested_in_studio: "non"
confidence: "faible"
confidence_reason: "Ancienne fiche V1–V4 reclassée automatiquement : 3 passage(s) technique(s), source de niveau 3 ; à approfondir et à tester."
engine_version: "inconnue"
source_tier: 3
provider: "github"
official: false
sources:
  - "https://github.com/nightcycle/quick-part"
accessed: "2026-11-15"
queries:
  - "Roblox SurfaceAppearance transparency foliage"
created: "2026-11-15"
updated: "2026-11-15"
tags:
  - "vdn"
  - "vegetation"
  - "spruce"
  - "candidat"
  - "migre-v5"
legacy_status: "a_verifier"
legacy_source_type: "GitHub repositories"
legacy_topic: "spruce"
legacy_score_heuristique: 45
legacy_collected_utc: "2026-11-15T12:15:20+00:00"
---

> **Candidat** (reclassement V5 du 2026-11-15) · 3 passage(s) technique(s), source de niveau 3 ; à approfondir et à tester.
> Le contenu historique ci-dessous est conservé tel quel.

# nightcycle/quick-part

**Sujet :** Épicéa enneigé réaliste

**Source :** [GitHub repositories](https://github.com/nightcycle/quick-part)

**Question de recherche :** Roblox SurfaceAppearance transparency foliage

## Extrait de découverte (non vérifié)

using editable meshes to create roblox part handles that look identical, but can be redrawn much quicker. Made with GPT-6 Astra.

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

**Source lue :** https://github.com/nightcycle/quick-part  
**Contenu :** GitHub README  
**Passages candidats :** 5

### Passages et paramètres repérés

- Press **Play (F5)** to animate the real BaseParts/models on the left and their QuickPart versions on the right: five primitives changing properties, 100 moving cubes, a rotating/scaling 26-part arch, two birch trees with separate trunks and transparent leaf cards, and a woodland scene with a round tree, pine, bush, ferns, grass and boulder.
- Use Play, not the server-only Run mode, for the client animation.
- -- SurfaceAppearance = anExistingSurfaceAppearance,
- A \`PartHandle\` has \`Id: number\` (monotonically increasing integer, treat as read-only), \`Size\`, \`CFrame\`, \`PivotOffset\`, \`Color\`, and \`Transparency\`.
- This is an application allowance: Roblox does not expose remaining device EditableMesh memory or a conversion between triangle count and bytes.

### Questions de recherche complémentaires

- spruce Roblox transparent implementation limitations troubleshooting
- spruce Roblox animation implementation limitations troubleshooting
- spruce Roblox surfaceappearance implementation limitations troubleshooting

### Validation requise

- [ ] Vérifier chaque passage dans la source complète
- [ ] Confirmer les limitations Roblox actuelles
- [ ] Tester dans Roblox Studio ET Roblox Player
- [ ] Mesurer qualité et performance
