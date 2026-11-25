---
id: "vdn-8a2ae33e44e7"
title: "Import emotes"
domain: "animation"
subdomain: "blender_animation"
status: "documente"
tested_in_studio: "non"
confidence: "moyenne"
confidence_reason: "8 passages techniques dont 3 avec action et objet identifiables, source de niveau 1 (réponse du personnel Roblox / doc officielle) ; indice technique seulement, procédure complète non garantie ; aucun test dans Roblox Studio."
engine_version: "inconnue"
source_tier: 1
provider: "roblox_docs"
official: true
sources:
  - "https://create.roblox.com/docs/avatar/emotes/import"
accessed: "2026-11-25"
queries:
  - "KeyframeSequence import"
created: "2026-11-25"
updated: "2026-11-25"
tags:
  - "vdn"
  - "animation"
  - "blender_animation"
  - "documente"
---

# Import emotes

> **Documenté** · source [Documentation Roblox](https://create.roblox.com/docs/en-us/avatar/emotes/import.md) · consultée le 2026-11-25 · **non testée dans Roblox Studio**

## Objectif

Répondre à : *KeyframeSequence import* (sujet : Animations Blender vers Roblox).

## Description technique

À rédiger à partir des extraits ci-dessous (analyse humaine ou Ollama). Rien n'est affirmé ici sans source.

## Étapes reproductibles

Instructions extraites automatiquement : procedure partielle, ordre et fonctionnement non verifies.

1. The following instructions detail how to import a `.fbx` file with animation data into Studio, convert it into a `CurveAnimation` object with an asset ID, then use that asset ID in `Class.Animation` objects that you can use in your games, upload to the Marketplace, or share with other creators. -- [Documentation Roblox](https://create.roblox.com/docs/en-us/avatar/emotes/import.md)
2. In the **Animation Editor**, select **⋯** > **Import** > **From File** and select your `.fbx` file. -- [Documentation Roblox](https://create.roblox.com/docs/en-us/avatar/emotes/import.md)
3. To submit an emote to the Marketplace, you must submit an `Class.Animation` object with the `AnimationId` property set to the asset ID of your `CurveAnimation` object. -- [Documentation Roblox](https://create.roblox.com/docs/en-us/avatar/emotes/import.md)

## Paramètres (sourcés)

Aucun paramètre chiffré trouvé dans les extraits.

## Limites connues de Roblox

Aucune limite explicite trouvée dans les extraits.

## Extraits justificatifs

> « description: "Use the Animation Editor to import and convert animations into emotes." »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/avatar/emotes/import.md), consulté le 2026-11-25

> « Studio's [Animation Editor](/docs/en-us/animation/editor.md) lets you import animations into your projects. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/avatar/emotes/import.md), consulté le 2026-11-25

> « The following instructions detail how to import a `.fbx` file with animation data into Studio, convert it into a `CurveAnimation` object with an asset ID, then use that asset ID in `Class.Animation` objects that you can use in your games, upload to the Marketplace, or share with other creators. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/avatar/emotes/import.md), consulté le 2026-11-25

> « In the **Animation Editor**, select **⋯** > **Import** > **From File** and select your `.fbx` file. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/avatar/emotes/import.md), consulté le 2026-11-25

> « To generate an asset ID for your animation, you must first convert your animation data in the timeline into a `CurveAnimation` object. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/avatar/emotes/import.md), consulté le 2026-11-25

> « > **Warning:** The animation data for emotes must be a `Class.CurveAnimation` object instead of a `Class.KeyframeSequence` object. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/avatar/emotes/import.md), consulté le 2026-11-25

> « To submit an emote to the Marketplace, you must submit an `Class.Animation` object with the `AnimationId` property set to the asset ID of your `CurveAnimation` object. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/avatar/emotes/import.md), consulté le 2026-11-25

> « To create an `Class.Animation` object you can publish as an emote: »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/avatar/emotes/import.md), consulté le 2026-11-25


## Problèmes connus

À compléter.

## Alternatives

À compléter.

## Tests dans Roblox Studio

- Testé : **non**
- Conditions : —
- Résultat : —

## Questions ouvertes

- Quels réglages exacts (valeurs, propriétés) pour « KeyframeSequence import » ?
- Quelles limites Roblox (performances, rendu à distance, appareils) pour « KeyframeSequence import » ?
- Le résultat tient-il de nuit, à la lampe torche, sur mobile ?

## Scores (diagnostic, pas une preuve)

- Pertinence sujet : 1.0 · Contenu technique : 1.0 · Lien Roblox : oui
- Termes techniques repérés : rig, fbx, import, animation
