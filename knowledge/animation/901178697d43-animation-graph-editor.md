---
id: "vdn-901178697d43"
title: "Animation Graph Editor"
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
  - "https://create.roblox.com/docs/animation/graph-editor"
accessed: "2026-11-24"
queries:
  - "Animation Editor import fbx"
created: "2026-11-24"
updated: "2026-11-24"
tags:
  - "vdn"
  - "animation"
  - "blender_animation"
  - "documente"
---

# Animation Graph Editor

> **Documenté** · source [Documentation Roblox](https://create.roblox.com/docs/en-us/animation/graph-editor.md) · consultée le 2026-11-24 · **non testée dans Roblox Studio**

## Objectif

Répondre à : *Animation Editor import fbx* (sujet : Animations Blender vers Roblox).

## Description technique

À rédiger à partir des extraits ci-dessous (analyse humaine ou Ollama). Rien n'est affirmé ici sans source.

## Étapes reproductibles

Instructions extraites automatiquement : procedure partielle, ordre et fonctionnement non verifies.

1. In the new Clip node, set the Animation ID. -- [Documentation Roblox](https://create.roblox.com/docs/en-us/animation/graph-editor.md)
2. Add another clip node by repeating steps 4-5 using the default Wave animation: `507770239`.![Two clip nodes with a populated Animation ID](../assets/animation/graph-editor/Clip-Nodes-With-IDs.png) -- [Documentation Roblox](https://create.roblox.com/docs/en-us/animation/graph-editor.md)
3. A new parameter node displays.![Click and dragging connector from Speed port of Clip node.](../assets/animation/graph-editor/Parameter-Noodle.png) -- [Documentation Roblox](https://create.roblox.com/docs/en-us/animation/graph-editor.md)

## Paramètres (sourcés)

Aucun paramètre chiffré trouvé dans les extraits.

## Limites connues de Roblox

Aucune limite explicite trouvée dans les extraits.

## Extraits justificatifs

> « - **Animation Graph Editor**: Use this tool to take those clips and organize them into a logic tree to drive sophisticated gameplay behavior. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/animation/graph-editor.md), consulté le 2026-11-24

> « The following steps demonstrate how to initialize a rig and construct a basic node network using default walking and waving animations. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/animation/graph-editor.md), consulté le 2026-11-24

> « To create your own animation graph, similar to the basic example provided in the reference, use the following steps: »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/animation/graph-editor.md), consulté le 2026-11-24

> « In the new Clip node, set the Animation ID. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/animation/graph-editor.md), consulté le 2026-11-24

> « To submit a specific animation asset ID, click **Import**.![Indicated a field on the animation import module to add Animation ID](../assets/animation/graph-editor/Import-AnimationID.png) »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/animation/graph-editor.md), consulté le 2026-11-24

> « Add another clip node by repeating steps 4-5 using the default Wave animation: `507770239`.![Two clip nodes with a populated Animation ID](../assets/animation/graph-editor/Clip-Nodes-With-IDs.png) »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/animation/graph-editor.md), consulté le 2026-11-24

> « A new parameter node displays.![Click and dragging connector from Speed port of Clip node.](../assets/animation/graph-editor/Parameter-Noodle.png) »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/animation/graph-editor.md), consulté le 2026-11-24

> « You can also access this [programmatically](#api-integration).![Parameter pane, parameter node, and clip node showing shared values.](../assets/animation/graph-editor/Parameter-Pane.png) »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/animation/graph-editor.md), consulté le 2026-11-24


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
- Quelles limites Roblox (performances, rendu à distance, appareils) pour « Animation Editor import fbx » ?
- Le résultat tient-il de nuit, à la lampe torche, sur mobile ?

## Scores (diagnostic, pas une preuve)

- Pertinence sujet : 0.875 · Contenu technique : 1.0 · Lien Roblox : oui
- Termes techniques repérés : rig, import, animation
