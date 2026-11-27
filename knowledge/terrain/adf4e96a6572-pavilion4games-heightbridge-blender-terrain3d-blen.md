---
id: "vdn-adf4e96a6572"
title: "pavilion4games/heightbridge-blender-terrain3d — Blender extension that exports terrain meshes as heightmaps (32-bit EXR or R16) for Godot's Terrain3D, with regi"
domain: "terrain"
subdomain: "terrain"
status: "candidat"
tested_in_studio: "non"
confidence: "faible"
confidence_reason: "8 passage(s) technique(s), 1 instruction(s) explicite(s) repérée(s), source de niveau 3 ; procédure à approfondir et à tester."
engine_version: "inconnue"
source_tier: 3
provider: "github"
official: false
sources:
  - "https://github.com/pavilion4games/heightbridge-blender-terrain3d"
accessed: "2026-11-27"
queries:
  - "terrain heightmap import settings"
created: "2026-11-27"
updated: "2026-11-27"
tags:
  - "vdn"
  - "terrain"
  - "terrain"
  - "candidat"
stars: 0
pushed: "2026-11-07"
license: "GPL-3.0"
---

# pavilion4games/heightbridge-blender-terrain3d — Blender extension that exports terrain meshes as heightmaps (32-bit EXR or R16) for Godot's Terrain3D, with regi

> **Candidat** · source [GitHub](https://github.com/pavilion4games/heightbridge-blender-terrain3d) · consultée le 2026-11-27 · **non testée dans Roblox Studio**

## Objectif

Répondre à : *terrain heightmap import settings* (sujet : Terrain réaliste).

## Description technique

À rédiger à partir des extraits ci-dessous (analyse humaine ou Ollama). Rien n'est affirmé ici sans source.

## Étapes reproductibles

Instructions extraites automatiquement : procedure partielle, ordre et fonctionnement non verifies.

1. Blender extension that exports terrain meshes as heightmaps (32-bit EXR or R16) for Godot's Terrain3D, with region-aligned bounds and a JSON file holding the exact import settings. -- [GitHub](https://github.com/pavilion4games/heightbridge-blender-terrain3d)

## Paramètres (sourcés)

Aucun paramètre chiffré trouvé dans les extraits.

## Limites connues de Roblox

Aucune limite explicite trouvée dans les extraits.

## Extraits justificatifs

> « Blender extension that exports terrain meshes as heightmaps (32-bit EXR or R16) for Godot's Terrain3D, with region-aligned bounds and a JSON file holding the exact import settings. »
> — [GitHub](https://github.com/pavilion4games/heightbridge-blender-terrain3d), consulté le 2026-11-27

> « When you import it, Terrain3D needs the height range and image size; both are in the `.json` sidecar. »
> — [GitHub](https://github.com/pavilion4games/heightbridge-blender-terrain3d), consulté le 2026-11-27

> « Select your terrain mesh(es), then use either: »
> — [GitHub](https://github.com/pavilion4games/heightbridge-blender-terrain3d), consulté le 2026-11-27

> « - **File › Export › Terrain3D Heightmap (.exr/.r16)**, or »
> — [GitHub](https://github.com/pavilion4games/heightbridge-blender-terrain3d), consulté le 2026-11-27

> « - **3D Viewport › Sidebar (N) › Terrain3D › Export Terrain3D Heightmap** »
> — [GitHub](https://github.com/pavilion4games/heightbridge-blender-terrain3d), consulté le 2026-11-27

> « It must match `vertex_spacing` on the Terrain3D node (default 1.0). »
> — [GitHub](https://github.com/pavilion4games/heightbridge-blender-terrain3d), consulté le 2026-11-27

> « Moves the top-left corner onto Terrain3D's region grid and pads the image to whole regions, so the **Import Position** is an exact integer. »
> — [GitHub](https://github.com/pavilion4games/heightbridge-blender-terrain3d), consulté le 2026-11-27

> « | Write Info JSON | Writes `<name>.json` with the size, height range and suggested Terrain3D import settings. »
> — [GitHub](https://github.com/pavilion4games/heightbridge-blender-terrain3d), consulté le 2026-11-27


## Problèmes connus

À compléter.

## Alternatives

À compléter.

## Tests dans Roblox Studio

- Testé : **non**
- Conditions : —
- Résultat : —

## Questions ouvertes

- Quels réglages exacts (valeurs, propriétés) pour « terrain heightmap import settings » ?
- Quelles limites Roblox (performances, rendu à distance, appareils) pour « terrain heightmap import settings » ?
- Le résultat tient-il de nuit, à la lampe torche, sur mobile ?

## Scores (diagnostic, pas une preuve)

- Pertinence sujet : 1.0 · Contenu technique : 1.0 · Lien Roblox : oui
- Termes techniques repérés : vertex, export, import, geometry nodes, terrain
