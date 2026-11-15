---
id: "vdn-5aa463725976"
title: "Improve performance"
domain: "forest"
subdomain: "forest"
status: "documente"
tested_in_studio: "non"
confidence: "moyenne"
confidence_reason: "8 passages techniques dont 1 avec action et objet identifiables, source de niveau 1 (réponse du personnel Roblox / doc officielle) ; aucun test dans Roblox Studio."
engine_version: "inconnue"
source_tier: 1
provider: "roblox_docs"
official: true
sources:
  - "https://create.roblox.com/docs/performance-optimization/improve"
accessed: "2026-11-15"
queries:
  - "large forest performance"
created: "2026-11-15"
updated: "2026-11-15"
tags:
  - "vdn"
  - "forest"
  - "forest"
  - "documente"
---

# Improve performance

> **Documenté** · source [Documentation Roblox](https://create.roblox.com/docs/en-us/performance-optimization/improve.md) · consultée le 2026-11-15 · **non testée dans Roblox Studio**

## Objectif

Répondre à : *large forest performance* (sujet : Forêt nocturne enneigée).

## Description technique

À rédiger à partir des extraits ci-dessous (analyse humaine ou Ollama). Rien n'est affirmé ici sans source.

## Étapes reproductibles

À extraire de la source ; non disponibles automatiquement.

## Paramètres (sourcés)

- « - **Overly precise collision detection** - Mesh parts have a `Class.MeshPart.CollisionFidelity|CollisionFidelity` property for detecting collision which offers a variety of modes with different levels of performance impact. » — [Documentation Roblox](https://create.roblox.com/docs/en-us/performance-optimization/improve.md)
- « Alternatively, you can apply the `CollisionFidelity=PreciseConvexDecomposition` filter to the [Explorer](/docs/en-us/studio/explorer.md#property-filters) which shows a count of all mesh parts with the precise fidelity and allows you to easily select them. » — [Documentation Roblox](https://create.roblox.com/docs/en-us/performance-optimization/improve.md)
- « - For an in-depth walkthrough on how to choose a collision fidelity option that balances your precision and performance requirements, see [Set physics and rendering parameters](/docs/en-us/tutorials/curriculums/environmental-art/assemble-an-asset-library.md#collisionfidelity). » — [Documentation Roblox](https://create.roblox.com/docs/en-us/performance-optimization/improve.md)
- « Mesh parts have a `Class.MeshPart.CollisionFidelity|CollisionFidelity` property that determines the approach that's used to evaluate the collision bounds of the mesh. » — [Documentation Roblox](https://create.roblox.com/docs/en-us/performance-optimization/improve.md)
- « - Reduce fidelity of collisions using the `Class.MeshPart.CollisionFidelity|CollisionFidelity` setting. » — [Documentation Roblox](https://create.roblox.com/docs/en-us/performance-optimization/improve.md)
- « - It's generally safe to set any small anchored part's collision fidelity to `Enum.CollisionFidelity.Box|Box`. » — [Documentation Roblox](https://create.roblox.com/docs/en-us/performance-optimization/improve.md)

## Limites connues de Roblox

Aucune limite explicite trouvée dans les extraits.

## Indices de procédure (non vérifiés)

- « Alternatively, you can apply the `CollisionFidelity=PreciseConvexDecomposition` filter to the [Explorer](/docs/en-us/studio/explorer.md#property-filters) which shows a count of all mesh parts with the precise fidelity and allows you to easily select them. » — [Documentation Roblox](https://create.roblox.com/docs/en-us/performance-optimization/improve.md)

## Extraits justificatifs

> « description: "Lists common performance problems and steps to mitigate them." »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/performance-optimization/improve.md), consulté le 2026-11-15

> « - **Overly precise collision detection** - Mesh parts have a `Class.MeshPart.CollisionFidelity|CollisionFidelity` property for detecting collision which offers a variety of modes with different levels of performance impact. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/performance-optimization/improve.md), consulté le 2026-11-15

> « - For objects that don't require collisions, disable collisions and use box or hull fidelity, since the collision geometry is still stored in memory. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/performance-optimization/improve.md), consulté le 2026-11-15

> « Alternatively, you can apply the `CollisionFidelity=PreciseConvexDecomposition` filter to the [Explorer](/docs/en-us/studio/explorer.md#property-filters) which shows a count of all mesh parts with the precise fidelity and allows you to easily select them. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/performance-optimization/improve.md), consulté le 2026-11-15

> « - For an in-depth walkthrough on how to choose a collision fidelity option that balances your precision and performance requirements, see [Set physics and rendering parameters](/docs/en-us/tutorials/curriculums/environmental-art/assemble-an-asset-library.md#collisionfidelity). »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/performance-optimization/improve.md), consulté le 2026-11-15

> « Mesh parts have a `Class.MeshPart.CollisionFidelity|CollisionFidelity` property that determines the approach that's used to evaluate the collision bounds of the mesh. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/performance-optimization/improve.md), consulté le 2026-11-15

> « - Reduce fidelity of collisions using the `Class.MeshPart.CollisionFidelity|CollisionFidelity` setting. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/performance-optimization/improve.md), consulté le 2026-11-15

> « - It's generally safe to set any small anchored part's collision fidelity to `Enum.CollisionFidelity.Box|Box`. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/performance-optimization/improve.md), consulté le 2026-11-15


## Problèmes connus

À compléter.

## Alternatives

À compléter.

## Tests dans Roblox Studio

- Testé : **non**
- Conditions : —
- Résultat : —

## Questions ouvertes

- Quelles limites Roblox (performances, rendu à distance, appareils) pour « large forest performance » ?
- Le résultat tient-il de nuit, à la lampe torche, sur mobile ?

## Scores (diagnostic, pas une preuve)

- Pertinence sujet : 0.833 · Contenu technique : 1.0 · Lien Roblox : oui
- Termes techniques repérés : surfaceappearance, meshpart, transparency, triangles, skinned, shadow, shadows, texture, textures, performance, render, rendering, renderfidelity, collisionfidelity, collision
