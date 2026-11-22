---
id: "vdn-aee340f3dc1c"
title: "kokusaitomita-blip/vrm-platform-preflight — Blender add-on that checks VRM 1.0 avatars against cluster's published upload limits — counted in triangles, the way"
domain: "performance"
subdomain: "performance"
status: "candidat"
tested_in_studio: "non"
confidence: "faible"
confidence_reason: "8 passage(s) technique(s), 5 instruction(s) explicite(s) repérée(s), source de niveau 3 ; procédure à approfondir et à tester."
engine_version: "inconnue"
source_tier: 3
provider: "github"
official: false
sources:
  - "https://github.com/kokusaitomita-blip/vrm-platform-preflight"
accessed: "2026-11-22"
queries:
  - "triangle count performance"
created: "2026-11-22"
updated: "2026-11-22"
tags:
  - "vdn"
  - "performance"
  - "performance"
  - "candidat"
stars: 0
pushed: "2026-11-06"
license: "GPL-3.0"
---

# kokusaitomita-blip/vrm-platform-preflight — Blender add-on that checks VRM 1.0 avatars against cluster's published upload limits — counted in triangles, the way

> **Candidat** · source [GitHub](https://github.com/kokusaitomita-blip/vrm-platform-preflight) · consultée le 2026-11-22 · **non testée dans Roblox Studio**

## Objectif

Répondre à : *triangle count performance* (sujet : Performances et niveaux de détail).

## Description technique

À rédiger à partir des extraits ci-dessous (analyse humaine ou Ollama). Rien n'est affirmé ici sans source.

## Étapes reproductibles

Instructions extraites automatiquement : procedure partielle, ordre et fonctionnement non verifies.

1. Check your avatar against cluster's VRM 1.0 upload limits **inside Blender, before you export** — with polygon counts done the way upload sites count them: as triangles. -- [GitHub](https://github.com/kokusaitomita-blip/vrm-platform-preflight)
2. - Triangle counts use the evaluated mesh (modifiers applied), matching what an exporter would produce. -- [GitHub](https://github.com/kokusaitomita-blip/vrm-platform-preflight)
3. - Texture totals count each unique image once, even if several materials use it. -- [GitHub](https://github.com/kokusaitomita-blip/vrm-platform-preflight)
4. - Images generated inside Blender (no source file) are counted for size but not judged on format, since their delivery format is decided at export time. -- [GitHub](https://github.com/kokusaitomita-blip/vrm-platform-preflight)
5. Spring-bone, collider, and constraint counts are planned for a future version and will use VRM add-on data when present. -- [GitHub](https://github.com/kokusaitomita-blip/vrm-platform-preflight)

## Paramètres (sourcés)

Aucun paramètre chiffré trouvé dans les extraits.

## Limites connues de Roblox

- « A model that looks fine in Blender (say, 45,000 polygons shown) can silently be over a platform limit once quads and n-gons are converted to triangles (the same model can be 84,000+ triangles). » — [GitHub](https://github.com/kokusaitomita-blip/vrm-platform-preflight)
- « | Texture formats (file-based images) | PNG / JPEG only | FAIL | » — [GitHub](https://github.com/kokusaitomita-blip/vrm-platform-preflight)
- « | Texture pixels, total | 12,000,000 | WARN — display-compression trigger in cluster, not an upload limit | » — [GitHub](https://github.com/kokusaitomita-blip/vrm-platform-preflight)

## Extraits justificatifs

> « Check your avatar against cluster's VRM 1.0 upload limits **inside Blender, before you export** — with polygon counts done the way upload sites count them: as triangles. »
> — [GitHub](https://github.com/kokusaitomita-blip/vrm-platform-preflight), consulté le 2026-11-22

> « A model that looks fine in Blender (say, 45,000 polygons shown) can silently be over a platform limit once quads and n-gons are converted to triangles (the same model can be 84,000+ triangles). »
> — [GitHub](https://github.com/kokusaitomita-blip/vrm-platform-preflight), consulté le 2026-11-22

> « | Texture formats (file-based images) | PNG / JPEG only | FAIL | »
> — [GitHub](https://github.com/kokusaitomita-blip/vrm-platform-preflight), consulté le 2026-11-22

> « | Texture pixels, total | 12,000,000 | WARN — display-compression trigger in cluster, not an upload limit | »
> — [GitHub](https://github.com/kokusaitomita-blip/vrm-platform-preflight), consulté le 2026-11-22

> « - Triangle counts use the evaluated mesh (modifiers applied), matching what an exporter would produce. »
> — [GitHub](https://github.com/kokusaitomita-blip/vrm-platform-preflight), consulté le 2026-11-22

> « - Texture totals count each unique image once, even if several materials use it. »
> — [GitHub](https://github.com/kokusaitomita-blip/vrm-platform-preflight), consulté le 2026-11-22

> « - Images generated inside Blender (no source file) are counted for size but not judged on format, since their delivery format is decided at export time. »
> — [GitHub](https://github.com/kokusaitomita-blip/vrm-platform-preflight), consulté le 2026-11-22

> « Spring-bone, collider, and constraint counts are planned for a future version and will use VRM add-on data when present. »
> — [GitHub](https://github.com/kokusaitomita-blip/vrm-platform-preflight), consulté le 2026-11-22


## Problèmes connus

À compléter.

## Alternatives

À compléter.

## Tests dans Roblox Studio

- Testé : **non**
- Conditions : —
- Résultat : —

## Questions ouvertes

- Quels réglages exacts (valeurs, propriétés) pour « triangle count performance » ?
- Le résultat tient-il de nuit, à la lampe torche, sur mobile ?

## Scores (diagnostic, pas une preuve)

- Pertinence sujet : 0.583 · Contenu technique : 1.0 · Lien Roblox : oui
- Termes techniques repérés : triangle, triangles, bone, bones, texture, export
