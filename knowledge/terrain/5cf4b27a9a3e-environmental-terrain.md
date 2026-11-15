---
id: "vdn-5cf4b27a9a3e"
title: "Environmental terrain"
domain: "terrain"
subdomain: "terrain"
status: "documente"
tested_in_studio: "non"
confidence: "moyenne"
confidence_reason: "8 passages techniques dont 3 avec action et objet identifiables, source de niveau 1 (réponse du personnel Roblox / doc officielle) ; indice technique seulement, procédure complète non garantie ; aucun test dans Roblox Studio."
engine_version: "inconnue"
source_tier: 1
provider: "roblox_docs"
official: true
sources:
  - "https://create.roblox.com/docs/parts/terrain"
accessed: "2026-11-15"
queries:
  - "terrain decoration grass"
created: "2026-11-15"
updated: "2026-11-15"
tags:
  - "vdn"
  - "terrain"
  - "terrain"
  - "documente"
---

# Environmental terrain

> **Documenté** · source [Documentation Roblox](https://create.roblox.com/docs/en-us/parts/terrain.md) · consultée le 2026-11-15 · **non testée dans Roblox Studio**

## Objectif

Répondre à : *terrain decoration grass* (sujet : Terrain réaliste).

## Description technique

À rédiger à partir des extraits ci-dessous (analyse humaine ou Ollama). Rien n'est affirmé ici sans source.

## Étapes reproductibles

À extraire de la source ; non disponibles automatiquement. Les indices d’action ci-dessous ne constituent pas un tutoriel complet.

## Paramètres (sourcés)

- « Terrain is made up of grids of **voxels** which are 4×4×4 stud regions in the 3D world with a set material. » — [Documentation Roblox](https://create.roblox.com/docs/en-us/parts/terrain.md)

## Limites connues de Roblox

- « Materials affect both the shape and appearance of terrain in the world; for example, [animated grass](#grass-animation) renders only on the `Enum.Material.Grass|Grass` material and the `Enum.Material.Water|Water` material [ripples and shimmers](#water-appearance) with a subtle motion. » — [Documentation Roblox](https://create.roblox.com/docs/en-us/parts/terrain.md)

## Indices de procédure (non vérifiés)

- « Terrain is made up of grids of **voxels** which are 4×4×4 stud regions in the 3D world with a set material. » — [Documentation Roblox](https://create.roblox.com/docs/en-us/parts/terrain.md)
- « You can also paint [custom terrain materials](/docs/en-us/parts/custom-terrain-materials.md) after you enable **Expanded Terrain**, or apply [custom materials](/docs/en-us/parts/materials.md#custom-materials) as overrides. » — [Documentation Roblox](https://create.roblox.com/docs/en-us/parts/terrain.md)
- « Adjust the grass length by entering a value between `0.1` and `1` for the `Class.Terrain.GrassLength|GrassLength` property.![GrassLength property of Terrain object in Properties window of Studio](../assets/studio/properties/Terrain-GrassLength.png)![GrassLength comparison depicted on rolling grassland hills.](../assets/modeling/terrain/Terrain-GrassLength.jpg) » — [Documentation Roblox](https://create.roblox.com/docs/en-us/parts/terrain.md)

## Extraits justificatifs

> « Terrain is made up of grids of **voxels** which are 4×4×4 stud regions in the 3D world with a set material. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/parts/terrain.md), consulté le 2026-11-15

> « You can also paint [custom terrain materials](/docs/en-us/parts/custom-terrain-materials.md) after you enable **Expanded Terrain**, or apply [custom materials](/docs/en-us/parts/materials.md#custom-materials) as overrides. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/parts/terrain.md), consulté le 2026-11-15

> « Materials affect both the shape and appearance of terrain in the world; for example, [animated grass](#grass-animation) renders only on the `Enum.Material.Grass|Grass` material and the `Enum.Material.Water|Water` material [ripples and shimmers](#water-appearance) with a subtle motion. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/parts/terrain.md), consulté le 2026-11-15

> « By default, grass sways gently in a simulated wind, and you can adjust the direction/strength of its animation through [global wind](/docs/en-us/environment/global-wind.md). »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/parts/terrain.md), consulté le 2026-11-15

> « In the **Properties** window, toggle on the `Class.Terrain.Decoration|Decoration` property.![Decoration property of Terrain object in Properties window of Studio](../assets/studio/properties/Terrain-Decoration.png) »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/parts/terrain.md), consulté le 2026-11-15

> « Adjust the grass length by entering a value between `0.1` and `1` for the `Class.Terrain.GrassLength|GrassLength` property.![GrassLength property of Terrain object in Properties window of Studio](../assets/studio/properties/Terrain-GrassLength.png)![GrassLength comparison depicted on rolling grassland hills.](../assets/modeling/terrain/Terrain-GrassLength.jpg) »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/parts/terrain.md), consulté le 2026-11-15

> « Adjust the direction and strength of its animation through [global wind](/docs/en-us/environment/global-wind.md). »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/parts/terrain.md), consulté le 2026-11-15

> « All materials display with their RGB code.![MaterialColors property shown in Properties window of Studio](../assets/studio/properties/Terrain-MaterialColors-Expand.png) »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/parts/terrain.md), consulté le 2026-11-15


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

- Pertinence sujet : 1.0 · Contenu technique : 1.0 · Lien Roblox : oui
- Termes techniques repérés : colormap, material, import, animation, terrain
