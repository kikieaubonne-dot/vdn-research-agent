---
id: "vdn-21ce8aee4188"
title: "Curve Editor"
domain: "animation"
subdomain: "blender_animation"
status: "candidat"
tested_in_studio: "non"
confidence: "faible"
confidence_reason: "7 passage(s) technique(s), 0 instruction(s) explicite(s) repérée(s), source de niveau 1 ; procédure à approfondir et à tester."
engine_version: "inconnue"
source_tier: 1
provider: "roblox_docs"
official: true
sources:
  - "https://create.roblox.com/docs/animation/curve-editor"
accessed: "2026-11-24"
queries:
  - "Animation Editor import fbx"
created: "2026-11-24"
updated: "2026-11-24"
tags:
  - "vdn"
  - "animation"
  - "blender_animation"
  - "candidat"
---

# Curve Editor

> **Candidat** · source [Documentation Roblox](https://create.roblox.com/docs/en-us/animation/curve-editor.md) · consultée le 2026-11-24 · **non testée dans Roblox Studio**

## Objectif

Répondre à : *Animation Editor import fbx* (sujet : Animations Blender vers Roblox).

## Description technique

À rédiger à partir des extraits ci-dessous (analyse humaine ou Ollama). Rien n'est affirmé ici sans source.

## Étapes reproductibles

Instructions extraites automatiquement : procedure partielle, ordre et fonctionnement non verifies.

Aucune instruction complete identifiee. Ne pas présenter cette fiche comme un tutoriel. Consulter la source.

## Paramètres (sourcés)

Aucun paramètre chiffré trouvé dans les extraits.

## Limites connues de Roblox

- « - If you load a `Class.KeyframeSequence` or a `Class.CurveAnimation` with a set quaternion rotation type then change the order, the new order doesn't affect the animation. » — [Documentation Roblox](https://create.roblox.com/docs/en-us/animation/curve-editor.md)

## Extraits justificatifs

> « Instead of using the default dope sheet editor's method of manually moving the scrubber from one frame to another to see how a rig's position and orientation change over time, the Curve Editor lets you quickly reference position and orientation values of your selected tracks through the **position ruler** on the left side of the timeline and the **rotation ruler** on the right side of the timeline. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/animation/curve-editor.md), consulté le 2026-11-24

> « > If you set the rotation type to quaternions, the conversion to curves preserves the quaternions and the animation remains the same. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/animation/curve-editor.md), consulté le 2026-11-24

> « How an animation changes when you set Euler angles order is dependent on **when** you change the order: »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/animation/curve-editor.md), consulté le 2026-11-24

> « - If you load a `Class.KeyframeSequence` or a `Class.CurveAnimation` with a set quaternion rotation type then change the order, the new order doesn't affect the animation. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/animation/curve-editor.md), consulté le 2026-11-24

> « This is because Studio uses quaternions to configure changes in your rig's orientation using the shortest path possible between its starting orientation to its next orientation. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/animation/curve-editor.md), consulté le 2026-11-24

> « - If you change the order of an existing Euler angle track, the animation might change since Studio preserves the values of each keyframe. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/animation/curve-editor.md), consulté le 2026-11-24

> « This means that the ordered path Studio takes to change your rig's orientation from its starting orientation to its next orientation changes with the Euler angles order. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/animation/curve-editor.md), consulté le 2026-11-24


## Problèmes connus

À compléter.

## Alternatives

À compléter.

## Tests dans Roblox Studio

- Testé : **non**
- Conditions : —
- Résultat : —

## Questions ouvertes

- Quels réglages exacts (valeurs, propriétés) pour « Animation Editor import fbx » ?
- Le résultat tient-il de nuit, à la lampe torche, sur mobile ?

## Scores (diagnostic, pas une preuve)

- Pertinence sujet : 0.5 · Contenu technique : 0.92 · Lien Roblox : oui
- Termes techniques repérés : rig, animation
