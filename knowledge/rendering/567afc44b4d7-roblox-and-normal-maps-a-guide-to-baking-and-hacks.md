---
id: "vdn-567afc44b4d7"
title: "Roblox and normal maps: a guide to baking and hacks for 3D modeling"
domain: "rendering"
subdomain: "rendering"
status: "documente"
tested_in_studio: "non"
confidence: "moyenne"
confidence_reason: "8 passages techniques dont 3 avec action et objet identifiables, source de niveau 1 (réponse du personnel Roblox / doc officielle) ; indice technique seulement, procédure complète non garantie ; aucun test dans Roblox Studio."
engine_version: "inconnue"
source_tier: 1
provider: "devforum"
official: true
sources:
  - "https://devforum.roblox.com/t/370063"
accessed: "2026-11-25"
queries:
  - "normal map baking Blender"
created: "2026-11-25"
updated: "2026-11-25"
tags:
  - "vdn"
  - "rendering"
  - "rendering"
  - "documente"
staff_posts: 1
accepted_answer: false
last_posted: "2019-10-17"
---

# Roblox and normal maps: a guide to baking and hacks for 3D modeling

> **Documenté** · source [Roblox DevForum](https://devforum.roblox.com/t/roblox-and-normal-maps-a-guide-to-baking-and-hacks-for-3d-modeling/370063) · consultée le 2026-11-25 · **non testée dans Roblox Studio**

## Objectif

Répondre à : *normal map baking Blender* (sujet : Rendu PBR et maillages).

## Description technique

À rédiger à partir des extraits ci-dessous (analyse humaine ou Ollama). Rien n'est affirmé ici sans source.

## Étapes reproductibles

Instructions extraites automatiquement : procedure partielle, ordre et fonctionnement non verifies.

1. In this tutorial, I will be showing the modelers of Roblox a (somewhat tedious) hack for getting a higher level of detail on your mesh through the use of baking a static lighting into your diffuse from a normal map. -- [Roblox DevForum](https://devforum.roblox.com/t/roblox-and-normal-maps-a-guide-to-baking-and-hacks-for-3d-modeling/370063)
2. You will need to create a new material for your low poly and have it UV unwrapped, assuming you are using Blender. -- [Roblox DevForum](https://devforum.roblox.com/t/roblox-and-normal-maps-a-guide-to-baking-and-hacks-for-3d-modeling/370063)
3. After you texture your model in Substance Painter or whatever software you use, import it to your 3D modeling software of choice (I will be using blender for this example) and apply all the maps you get from your texturing software. -- [Roblox DevForum](https://devforum.roblox.com/t/roblox-and-normal-maps-a-guide-to-baking-and-hacks-for-3d-modeling/370063)

## Paramètres (sourcés)

- « Your low poly mesh should be under 10k triangles by the time you are done. » — [Roblox DevForum](https://devforum.roblox.com/t/roblox-and-normal-maps-a-guide-to-baking-and-hacks-for-3d-modeling/370063)

## Limites connues de Roblox

Aucune limite explicite trouvée dans les extraits.

## Extraits justificatifs

> « DISCLAIMER: This tutorial is not made for the purpose of directly using normal maps in ROBLOX, rather using normal maps to bake AO to your diffuse to get a higher level of detail. »
> — [Roblox DevForum](https://devforum.roblox.com/t/roblox-and-normal-maps-a-guide-to-baking-and-hacks-for-3d-modeling/370063), consulté le 2026-11-25

> « In this tutorial, I will be showing the modelers of Roblox a (somewhat tedious) hack for getting a higher level of detail on your mesh through the use of baking a static lighting into your diffuse from a normal map. »
> — [Roblox DevForum](https://devforum.roblox.com/t/roblox-and-normal-maps-a-guide-to-baking-and-hacks-for-3d-modeling/370063), consulté le 2026-11-25

> « If you are unaware of the workflow for creating and baking normal maps, skip to CREATING NORMAL MAPS If you already know how to make and bake normal maps, skip to THE HACK »
> — [Roblox DevForum](https://devforum.roblox.com/t/roblox-and-normal-maps-a-guide-to-baking-and-hacks-for-3d-modeling/370063), consulté le 2026-11-25

> « Your low poly mesh should be under 10k triangles by the time you are done. »
> — [Roblox DevForum](https://devforum.roblox.com/t/roblox-and-normal-maps-a-guide-to-baking-and-hacks-for-3d-modeling/370063), consulté le 2026-11-25

> « In this step, you will be baking your high poly to your low poly. »
> — [Roblox DevForum](https://devforum.roblox.com/t/roblox-and-normal-maps-a-guide-to-baking-and-hacks-for-3d-modeling/370063), consulté le 2026-11-25

> « You will need to create a new material for your low poly and have it UV unwrapped, assuming you are using Blender. »
> — [Roblox DevForum](https://devforum.roblox.com/t/roblox-and-normal-maps-a-guide-to-baking-and-hacks-for-3d-modeling/370063), consulté le 2026-11-25

> « Then, click your high poly mesh and shift click your low poly mesh, and then Bake it. »
> — [Roblox DevForum](https://devforum.roblox.com/t/roblox-and-normal-maps-a-guide-to-baking-and-hacks-for-3d-modeling/370063), consulté le 2026-11-25

> « After you texture your model in Substance Painter or whatever software you use, import it to your 3D modeling software of choice (I will be using blender for this example) and apply all the maps you get from your texturing software. »
> — [Roblox DevForum](https://devforum.roblox.com/t/roblox-and-normal-maps-a-guide-to-baking-and-hacks-for-3d-modeling/370063), consulté le 2026-11-25


## Problèmes connus

À compléter.

## Alternatives

À compléter.

## Tests dans Roblox Studio

- Testé : **non**
- Conditions : —
- Résultat : —

## Questions ouvertes

- Quelles limites Roblox (performances, rendu à distance, appareils) pour « normal map baking Blender » ?
- Le résultat tient-il de nuit, à la lampe torche, sur mobile ?

## Scores (diagnostic, pas une preuve)

- Pertinence sujet : 0.833 · Contenu technique : 1.0 · Lien Roblox : oui
- Termes techniques repérés : uv, bake, baking, triangles, lighting, material, texture, render, import, resolution
