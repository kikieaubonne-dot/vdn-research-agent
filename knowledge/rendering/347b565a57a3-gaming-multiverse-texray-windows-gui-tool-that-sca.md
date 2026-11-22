---
id: "vdn-347b565a57a3"
title: "gaming-multiverse/TexRay — Windows GUI tool that scans custom FiveM peds against server compliance rules (vertex/polygon limits, texture resolution & compressio"
domain: "rendering"
subdomain: "rendering"
status: "candidat"
tested_in_studio: "non"
confidence: "faible"
confidence_reason: "8 passage(s) technique(s), 0 instruction(s) explicite(s) repérée(s), source de niveau 3 ; procédure à approfondir et à tester."
engine_version: "inconnue"
source_tier: 3
provider: "github"
official: false
sources:
  - "https://github.com/gaming-multiverse/texray"
accessed: "2026-11-22"
queries:
  - "texture resolution limit"
created: "2026-11-22"
updated: "2026-11-22"
tags:
  - "vdn"
  - "rendering"
  - "rendering"
  - "candidat"
stars: 2
pushed: "2026-09-15"
license: "MIT"
---

# gaming-multiverse/TexRay — Windows GUI tool that scans custom FiveM peds against server compliance rules (vertex/polygon limits, texture resolution & compressio

> **Candidat** · source [GitHub](https://github.com/gaming-multiverse/TexRay) · consultée le 2026-11-22 · **non testée dans Roblox Studio**

## Objectif

Répondre à : *texture resolution limit* (sujet : Rendu PBR et maillages).

## Description technique

À rédiger à partir des extraits ci-dessous (analyse humaine ou Ollama). Rien n'est affirmé ici sans source.

## Étapes reproductibles

Instructions extraites automatiquement : procedure partielle, ordre et fonctionnement non verifies.

Aucune instruction complete identifiee. Ne pas présenter cette fiche comme un tutoriel. Consulter la source.

## Paramètres (sourcés)

- « | Max texture resolution (embedded + standalone) | **2048×2048 (2K)** | » — [GitHub](https://github.com/gaming-multiverse/TexRay)

## Limites connues de Roblox

- « | Max vertices per geometry | **60,000** | » — [GitHub](https://github.com/gaming-multiverse/TexRay)
- « | Max polygons (triangles) per geometry | **60,000** | » — [GitHub](https://github.com/gaming-multiverse/TexRay)
- « | Max vertices / polygons per whole clothing item (sum of its parts) | **60,000** | » — [GitHub](https://github.com/gaming-multiverse/TexRay)
- « | Max texture resolution (embedded + standalone) | **2048×2048 (2K)** | » — [GitHub](https://github.com/gaming-multiverse/TexRay)
- « Counts come from the **high-detail (LOD0) model only** — the Med/Low/VLow LOD copies a » — [GitHub](https://github.com/gaming-multiverse/TexRay)

## Extraits justificatifs

> « | Max vertices per geometry | **60,000** | »
> — [GitHub](https://github.com/gaming-multiverse/TexRay), consulté le 2026-11-22

> « | Max polygons (triangles) per geometry | **60,000** | »
> — [GitHub](https://github.com/gaming-multiverse/TexRay), consulté le 2026-11-22

> « | Max vertices / polygons per whole clothing item (sum of its parts) | **60,000** | »
> — [GitHub](https://github.com/gaming-multiverse/TexRay), consulté le 2026-11-22

> « | Max texture resolution (embedded + standalone) | **2048×2048 (2K)** | »
> — [GitHub](https://github.com/gaming-multiverse/TexRay), consulté le 2026-11-22

> « Counts come from the **high-detail (LOD0) model only** — the Med/Low/VLow LOD copies a »
> — [GitHub](https://github.com/gaming-multiverse/TexRay), consulté le 2026-11-22

> « Geometry and embedded-texture checks (and the texture auto-fix) apply equally to »
> — [GitHub](https://github.com/gaming-multiverse/TexRay), consulté le 2026-11-22

> « - **EXPORT HTML** writes the English compliance report (one table per violation category, »
> — [GitHub](https://github.com/gaming-multiverse/TexRay), consulté le 2026-11-22

> « - **FIX TEXTURES** repairs texture violations in place: oversized textures are downscaled »
> — [GitHub](https://github.com/gaming-multiverse/TexRay), consulté le 2026-11-22


## Problèmes connus

À compléter.

## Alternatives

À compléter.

## Tests dans Roblox Studio

- Testé : **non**
- Conditions : —
- Résultat : —

## Questions ouvertes

- Le résultat tient-il de nuit, à la lampe torche, sur mobile ?

## Scores (diagnostic, pas une preuve)

- Pertinence sujet : 0.8 · Contenu technique : 1.0 · Lien Roblox : oui
- Termes techniques repérés : lod, triangles, vertex, vertices, texture, textures, export, resolution
