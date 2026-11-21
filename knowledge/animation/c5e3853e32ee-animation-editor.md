---
id: "vdn-c5e3853e32ee"
title: "Animation Editor"
domain: "animation"
subdomain: "fp_hands"
status: "documente"
tested_in_studio: "non"
confidence: "moyenne"
confidence_reason: "8 passages techniques dont 2 avec action et objet identifiables, source de niveau 1 (réponse du personnel Roblox / doc officielle) ; indice technique seulement, procédure complète non garantie ; aucun test dans Roblox Studio."
engine_version: "inconnue"
source_tier: 1
provider: "roblox_docs"
official: true
sources:
  - "https://create.roblox.com/docs/animation/editor"
accessed: "2026-11-21"
queries:
  - "hands flashlight animation"
created: "2026-11-21"
updated: "2026-11-21"
tags:
  - "vdn"
  - "animation"
  - "fp_hands"
  - "documente"
---

# Animation Editor

> **Documenté** · source [Documentation Roblox](https://create.roblox.com/docs/en-us/animation/editor.md) · consultée le 2026-11-21 · **non testée dans Roblox Studio**

## Objectif

Répondre à : *hands flashlight animation* (sujet : Mains et bras en vue FPS).

## Description technique

À rédiger à partir des extraits ci-dessous (analyse humaine ou Ollama). Rien n'est affirmé ici sans source.

## Étapes reproductibles

Instructions extraites automatiquement : procedure partielle, ordre et fonctionnement non verifies.

1. You can create poses by moving or rotating bones or meshes, such as the rig's hands, feet, or torso. -- [Documentation Roblox](https://create.roblox.com/docs/en-us/animation/editor.md)
2. Whenever you adjust a specific bone or mesh, a new track displays in the track list and a new **keyframe** displays on the timeline for that bone or mesh at that specific frame position. -- [Documentation Roblox](https://create.roblox.com/docs/en-us/animation/editor.md)

## Paramètres (sourcés)

Aucun paramètre chiffré trouvé dans les extraits.

## Limites connues de Roblox

- « If the track only contains keyframes with default values, such as an `Datatype.CFrame.identity|identity` coordinate frame, or a `0` value for a curve animation, the entire track is removed from the animation. » — [Documentation Roblox](https://create.roblox.com/docs/en-us/animation/editor.md)

## Extraits justificatifs

> « You can move these joints to [create poses](#create-poses) and then smoothly animate the rig from pose to pose. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/animation/editor.md), consulté le 2026-11-21

> « From here, you can begin [creating poses](#create-poses) for your rig and modifying the animation settings, such as [looping the animation](#loop-an-animation) or [setting its priority](#set-a-priority). »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/animation/editor.md), consulté le 2026-11-21

> « You can create poses by moving or rotating bones or meshes, such as the rig's hands, feet, or torso. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/animation/editor.md), consulté le 2026-11-21

> « After you create multiple poses on different positions of the timeline, the animation editor runs between them with your [easing settings](#easing) to smoothly animate the rig from pose-to-pose. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/animation/editor.md), consulté le 2026-11-21

> « Whenever you adjust a specific bone or mesh, a new track displays in the track list and a new **keyframe** displays on the timeline for that bone or mesh at that specific frame position. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/animation/editor.md), consulté le 2026-11-21

> « Once you [create basic poses](#create-poses) for a rig, fine-tuning individual keyframes can significantly improve the final animation. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/animation/editor.md), consulté le 2026-11-21

> « If the track only contains keyframes with default values, such as an `Datatype.CFrame.identity|identity` coordinate frame, or a `0` value for a curve animation, the entire track is removed from the animation. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/animation/editor.md), consulté le 2026-11-21

> « To make the animation loop smoothly, duplicate the first keyframes and use them as the final keyframes. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/animation/editor.md), consulté le 2026-11-21


## Problèmes connus

À compléter.

## Alternatives

À compléter.

## Tests dans Roblox Studio

- Testé : **non**
- Conditions : —
- Résultat : —

## Questions ouvertes

- Quels réglages exacts (valeurs, propriétés) pour « hands flashlight animation » ?
- Le résultat tient-il de nuit, à la lampe torche, sur mobile ?

## Scores (diagnostic, pas une preuve)

- Pertinence sujet : 0.667 · Contenu technique : 1.0 · Lien Roblox : oui
- Termes techniques repérés : meshpart, bone, bones, rig, export, animation
