---
id: "vdn-05e396579185"
title: "antzGames/Godot-Compatibility-Decal-Node — This plugin provides both instanced and non-instanced animated decal node functionality for all Renderers in Godot 4."
domain: "snow"
subdomain: "snow"
status: "candidat"
tested_in_studio: "non"
confidence: "faible"
confidence_reason: "8 passage(s) technique(s), 1 instruction(s) explicite(s) repérée(s), source de niveau 3 ; procédure à approfondir et à tester."
engine_version: "inconnue"
source_tier: 3
provider: "github"
official: false
sources:
  - "https://github.com/antzgames/godot-compatibility-decal-node"
accessed: "2026-11-22"
queries:
  - "Decal Transparency Roblox Studio implementation compatibility"
created: "2026-11-22"
updated: "2026-11-22"
tags:
  - "vdn"
  - "snow"
  - "snow"
  - "candidat"
stars: 48
pushed: "2026-10-19"
license: "MIT"
---

# antzGames/Godot-Compatibility-Decal-Node — This plugin provides both instanced and non-instanced animated decal node functionality for all Renderers in Godot 4.

> **Candidat** · source [GitHub](https://github.com/antzGames/Godot-Compatibility-Decal-Node) · consultée le 2026-11-22 · **non testée dans Roblox Studio**

## Objectif

Répondre à : *Decal Transparency Roblox Studio implementation compatibility* (sujet : Neige, givre et traces).

## Description technique

À rédiger à partir des extraits ci-dessous (analyse humaine ou Ollama). Rien n'est affirmé ici sans source.

## Étapes reproductibles

Instructions extraites automatiquement : procedure partielle, ordre et fonctionnement non verifies.

1. This plugin provides both instanced and non-instanced animated decal node functionality for all Renderers in Godot 4.4-4.7, packaged as an easy-to-use plugin. -- [GitHub](https://github.com/antzGames/Godot-Compatibility-Decal-Node)

## Paramètres (sourcés)

Aucun paramètre chiffré trouvé dans les extraits.

## Limites connues de Roblox

- « No limits set, unlike Godot's Compatibility/Mobile Decal limits of Max 8 decals per mesh and max 64 decals per frame. » — [GitHub](https://github.com/antzGames/Godot-Compatibility-Decal-Node)
- « - `DecalCompatibility` extends `MeshInstance3D`, which should be used when only one decal is needed. » — [GitHub](https://github.com/antzGames/Godot-Compatibility-Decal-Node)
- « - Full transparency support of the decal, but cannot project on semi-transparent geometry, only opaque geometry. » — [GitHub](https://github.com/antzGames/Godot-Compatibility-Decal-Node)

## Extraits justificatifs

> « This plugin provides both instanced and non-instanced animated decal node functionality for all Renderers in Godot 4.4-4.7, packaged as an easy-to-use plugin. »
> — [GitHub](https://github.com/antzGames/Godot-Compatibility-Decal-Node), consulté le 2026-11-22

> « No limits set, unlike Godot's Compatibility/Mobile Decal limits of Max 8 decals per mesh and max 64 decals per frame. »
> — [GitHub](https://github.com/antzGames/Godot-Compatibility-Decal-Node), consulté le 2026-11-22

> « > The [PR](https://github.com/godotengine/godot/pull/118070) to support the Decal Node for the Compatibility Renderer has been merged, »
> — [GitHub](https://github.com/antzGames/Godot-Compatibility-Decal-Node), consulté le 2026-11-22

> « - Stencil support, which allows you to exclude specific geometry from recieving decal (such as the player). »
> — [GitHub](https://github.com/antzGames/Godot-Compatibility-Decal-Node), consulté le 2026-11-22

> « - Instanced Flipbook `animation` support, with: »
> — [GitHub](https://github.com/antzGames/Godot-Compatibility-Decal-Node), consulté le 2026-11-22

> « - Frame offset support to randomize looping animation. »
> — [GitHub](https://github.com/antzGames/Godot-Compatibility-Decal-Node), consulté le 2026-11-22

> « - `DecalCompatibility` extends `MeshInstance3D`, which should be used when only one decal is needed. »
> — [GitHub](https://github.com/antzGames/Godot-Compatibility-Decal-Node), consulté le 2026-11-22

> « - Full transparency support of the decal, but cannot project on semi-transparent geometry, only opaque geometry. »
> — [GitHub](https://github.com/antzGames/Godot-Compatibility-Decal-Node), consulté le 2026-11-22


## Problèmes connus

À compléter.

## Alternatives

À compléter.

## Tests dans Roblox Studio

- Testé : **non**
- Conditions : —
- Résultat : —

## Questions ouvertes

- Quels réglages exacts (valeurs, propriétés) pour « Decal Transparency Roblox Studio implementation compatibility » ?
- Le résultat tient-il de nuit, à la lampe torche, sur mobile ?

## Scores (diagnostic, pas une preuve)

- Pertinence sujet : 0.75 · Contenu technique : 1.0 · Lien Roblox : oui
- Termes techniques repérés : roughness, transparency, lighting, texture, textures, rendering, import, animation, decal, terrain, draw call, 512
