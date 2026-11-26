---
id: "vdn-0ac56bac073b"
title: "PBR textures"
domain: "rendering"
subdomain: "rendering"
status: "documente"
tested_in_studio: "non"
confidence: "moyenne"
confidence_reason: "8 passages techniques dont 4 avec action et objet identifiables, source de niveau 1 (réponse du personnel Roblox / doc officielle) ; indice technique seulement, procédure complète non garantie ; aucun test dans Roblox Studio."
engine_version: "inconnue"
source_tier: 1
provider: "roblox_docs"
official: true
sources:
  - "https://create.roblox.com/docs/art/modeling/surface-appearance"
accessed: "2026-11-26"
queries:
  - "SurfaceAppearance PBR textures"
created: "2026-11-26"
updated: "2026-11-26"
tags:
  - "vdn"
  - "rendering"
  - "rendering"
  - "documente"
---

# PBR textures

> **Documenté** · source [Documentation Roblox](https://create.roblox.com/docs/en-us/art/modeling/surface-appearance.md) · consultée le 2026-11-26 · **non testée dans Roblox Studio**

## Objectif

Répondre à : *SurfaceAppearance PBR textures* (sujet : Rendu PBR et maillages).

## Description technique

À rédiger à partir des extraits ci-dessous (analyse humaine ou Ollama). Rien n'est affirmé ici sans source.

## Étapes reproductibles

Instructions extraites automatiquement : procedure partielle, ordre et fonctionnement non verifies.

1. You can use these during the modeling and texturing phases of custom 3D object creation, provided that Roblox Studio [supports](/docs/en-us/avatar/character-bodies/specifications.md#textures) the specific texture maps you're using. -- [Documentation Roblox](https://create.roblox.com/docs/en-us/art/modeling/surface-appearance.md)
2. > **Info:** For information on how to properly connect PBR textures to your model in Blender and Maya for import into Studio, see [Blender / Maya texture settings](/docs/en-us/art/modeling/assign-textures.md). -- [Documentation Roblox](https://create.roblox.com/docs/en-us/art/modeling/surface-appearance.md)
3. This guide provides instructions on [setting up](#enable-surface-appearance) your mesh objects to use PBR texture maps, and describes common use-cases and best practices for Roblox's supported PBR [texture maps](#texture-maps). -- [Documentation Roblox](https://create.roblox.com/docs/en-us/art/modeling/surface-appearance.md)
4. Insert a `Class.SurfaceAppearance` from the contextual menu.![A SurfaceAppearance object parented within a MeshPart in Studio's Explorer window.](../../assets/studio/explorer/MeshPart-SurfaceAppearance.png) When you're ready to add texture maps to the `Class.SurfaceAppearance` object, you can click each map property in the **Properties** window and enter an asset ID. -- [Documentation Roblox](https://create.roblox.com/docs/en-us/art/modeling/surface-appearance.md)

## Paramètres (sourcés)

Aucun paramètre chiffré trouvé dans les extraits.

## Limites connues de Roblox

- « In general, you can't modify `Class.SurfaceAppearance` properties by scripts during a game because the engine requires some pre-processing to display these graphics. » — [Documentation Roblox](https://create.roblox.com/docs/en-us/art/modeling/surface-appearance.md)

## Extraits justificatifs

> « You can use these during the modeling and texturing phases of custom 3D object creation, provided that Roblox Studio [supports](/docs/en-us/avatar/character-bodies/specifications.md#textures) the specific texture maps you're using. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/art/modeling/surface-appearance.md), consulté le 2026-11-26

> « > **Info:** For information on how to properly connect PBR textures to your model in Blender and Maya for import into Studio, see [Blender / Maya texture settings](/docs/en-us/art/modeling/assign-textures.md). »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/art/modeling/surface-appearance.md), consulté le 2026-11-26

> « This guide provides instructions on [setting up](#enable-surface-appearance) your mesh objects to use PBR texture maps, and describes common use-cases and best practices for Roblox's supported PBR [texture maps](#texture-maps). »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/art/modeling/surface-appearance.md), consulté le 2026-11-26

> « In general, you can't modify `Class.SurfaceAppearance` properties by scripts during a game because the engine requires some pre-processing to display these graphics. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/art/modeling/surface-appearance.md), consulté le 2026-11-26

> « Similar to adding a basic texture, each texture image map must point to the appropriate uploaded image asset ID. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/art/modeling/surface-appearance.md), consulté le 2026-11-26

> « To enable surface appearance for a `Class.MeshPart`: »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/art/modeling/surface-appearance.md), consulté le 2026-11-26

> « Insert a `Class.SurfaceAppearance` from the contextual menu.![A SurfaceAppearance object parented within a MeshPart in Studio's Explorer window.](../../assets/studio/explorer/MeshPart-SurfaceAppearance.png) When you're ready to add texture maps to the `Class.SurfaceAppearance` object, you can click each map property in the **Properties** window and enter an asset ID. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/art/modeling/surface-appearance.md), consulté le 2026-11-26

> « Studio currently supports 5 types of PBR texture maps: [color](#color-albedo), [normal](#normal), [roughness](#roughness), [metalness](#metalness), and [emissive](#emissive-mask). »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/art/modeling/surface-appearance.md), consulté le 2026-11-26


## Problèmes connus

À compléter.

## Alternatives

À compléter.

## Tests dans Roblox Studio

- Testé : **non**
- Conditions : —
- Résultat : —

## Questions ouvertes

- Quels réglages exacts (valeurs, propriétés) pour « SurfaceAppearance PBR textures » ?
- Le résultat tient-il de nuit, à la lampe torche, sur mobile ?

## Scores (diagnostic, pas une preuve)

- Pertinence sujet : 0.9 · Contenu technique : 1.0 · Lien Roblox : oui
- Termes techniques repérés : surfaceappearance, alphamode, normalmap, roughness, metalness, colormap, meshpart, transparency, triangle, lighting, foliage, material, materialvariant, texture, textures
