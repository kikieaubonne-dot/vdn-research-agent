---
id: "vdn-0e2647f71d95"
title: "Custom characters"
domain: "gameplay"
subdomain: "movement"
status: "documente"
tested_in_studio: "non"
confidence: "moyenne"
confidence_reason: "8 passages techniques dont 2 avec action et objet identifiables, source de niveau 1 (réponse du personnel Roblox / doc officielle) ; indice technique seulement, procédure complète non garantie ; aucun test dans Roblox Studio."
engine_version: "inconnue"
source_tier: 1
provider: "roblox_docs"
official: true
sources:
  - "https://create.roblox.com/docs/resources/beyond-the-dark/custom-characters"
accessed: "2026-11-26"
queries:
  - "custom character controller"
created: "2026-11-26"
updated: "2026-11-26"
tags:
  - "vdn"
  - "gameplay"
  - "movement"
  - "documente"
---

# Custom characters

> **Documenté** · source [Documentation Roblox](https://create.roblox.com/docs/en-us/resources/beyond-the-dark/custom-characters.md) · consultée le 2026-11-26 · **non testée dans Roblox Studio**

## Objectif

Répondre à : *custom character controller* (sujet : Mouvements et contrôleur de personnage).

## Description technique

À rédiger à partir des extraits ci-dessous (analyse humaine ou Ollama). Rien n'est affirmé ici sans source.

## Étapes reproductibles

Instructions extraites automatiquement : procedure partielle, ordre et fonctionnement non verifies.

1. You can import custom meshes to create everything from NPCs to an animated cloth of a sail boat. -- [Documentation Roblox](https://create.roblox.com/docs/en-us/resources/beyond-the-dark/custom-characters.md)
2. In the [Importer](/docs/en-us/studio/importer.md), import the custom `.fbx` or `.obj` file.![Creature Imported Into Studio](../../assets/resources/beyond-the-dark/custom-characters/Custom-Import-2.png) -- [Documentation Roblox](https://create.roblox.com/docs/en-us/resources/beyond-the-dark/custom-characters.md)

## Paramètres (sourcés)

- « - Meshes are all under 10,000 triangles for each part of the mesh. » — [Documentation Roblox](https://create.roblox.com/docs/en-us/resources/beyond-the-dark/custom-characters.md)

## Limites connues de Roblox

- « - Skinning influences (meaning they affect a part of the model when moved) should be a maximum of 4 influences per vertex. » — [Documentation Roblox](https://create.roblox.com/docs/en-us/resources/beyond-the-dark/custom-characters.md)
- « - Any joint you want to import into Studio must have some influence on the model's skinning, otherwise the engine doesn't import it. » — [Documentation Roblox](https://create.roblox.com/docs/en-us/resources/beyond-the-dark/custom-characters.md)

## Extraits justificatifs

> « You can import custom meshes to create everything from NPCs to an animated cloth of a sail boat. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/resources/beyond-the-dark/custom-characters.md), consulté le 2026-11-26

> « - Individual joints and bones must have unique names. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/resources/beyond-the-dark/custom-characters.md), consulté le 2026-11-26

> « - Meshes must not have the same name as joints and bones. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/resources/beyond-the-dark/custom-characters.md), consulté le 2026-11-26

> « - Skinning influences (meaning they affect a part of the model when moved) should be a maximum of 4 influences per vertex. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/resources/beyond-the-dark/custom-characters.md), consulté le 2026-11-26

> « - Any joint you want to import into Studio must have some influence on the model's skinning, otherwise the engine doesn't import it. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/resources/beyond-the-dark/custom-characters.md), consulté le 2026-11-26

> « Export the character from the DCC application and ensure the following: »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/resources/beyond-the-dark/custom-characters.md), consulté le 2026-11-26

> « - Meshes are all under 10,000 triangles for each part of the mesh. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/resources/beyond-the-dark/custom-characters.md), consulté le 2026-11-26

> « In the [Importer](/docs/en-us/studio/importer.md), import the custom `.fbx` or `.obj` file.![Creature Imported Into Studio](../../assets/resources/beyond-the-dark/custom-characters/Custom-Import-2.png) »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/resources/beyond-the-dark/custom-characters.md), consulté le 2026-11-26


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

- Pertinence sujet : 0.5 · Contenu technique : 1.0 · Lien Roblox : oui
- Termes techniques repérés : surfaceappearance, transparency, triangles, vertex, skinned, skinning, bone, bones, rig, lighting, material, texture, performance, rendering, fbx
