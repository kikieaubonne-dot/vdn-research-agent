---
id: "vdn-fc8ba15fa1f6"
title: "Why does the same mesh use more than 1 draw call when duped a lot?"
domain: "performance"
subdomain: "performance"
status: "documente"
tested_in_studio: "non"
confidence: "faible"
confidence_reason: "3 passages techniques dont 1 avec action et objet identifiables, source de niveau 2 ; indice technique seulement, procédure complète non garantie ; aucun test dans Roblox Studio."
engine_version: "inconnue"
source_tier: 2
provider: "devforum"
official: false
sources:
  - "https://devforum.roblox.com/t/3988136"
accessed: "2026-11-25"
queries:
  - "draw calls instancing"
created: "2026-11-25"
updated: "2026-11-25"
tags:
  - "vdn"
  - "performance"
  - "performance"
  - "documente"
staff_posts: 0
accepted_answer: false
last_posted: "2026-06-02"
---

# Why does the same mesh use more than 1 draw call when duped a lot?

> **Documenté** · source [Roblox DevForum](https://devforum.roblox.com/t/why-does-the-same-mesh-use-more-than-1-draw-call-when-duped-a-lot/3988136) · consultée le 2026-11-25 · **non testée dans Roblox Studio**

## Objectif

Répondre à : *draw calls instancing* (sujet : Performances et niveaux de détail).

## Description technique

À rédiger à partir des extraits ci-dessous (analyse humaine ou Ollama). Rien n'est affirmé ici sans source.

## Étapes reproductibles

Instructions extraites automatiquement : procedure partielle, ordre et fonctionnement non verifies.

1. When set to Vulkan, on the 74 instances i had 2 draw calls, on 147 i had 3, on 220 4, thats new draw call each 73 instances. -- [Roblox DevForum](https://devforum.roblox.com/t/why-does-the-same-mesh-use-more-than-1-draw-call-when-duped-a-lot/3988136)

## Paramètres (sourcés)

Aucun paramètre chiffré trouvé dans les extraits.

## Limites connues de Roblox

- « So for example; if you have multiple identical meshes stored into the same Grid, the draw call will always stay at 1 only. » — [Roblox DevForum](https://devforum.roblox.com/t/why-does-the-same-mesh-use-more-than-1-draw-call-when-duped-a-lot/3988136)

## Extraits justificatifs

> « When set to Vulkan, on the 74 instances i had 2 draw calls, on 147 i had 3, on 220 4, thats new draw call each 73 instances. »
> — [Roblox DevForum](https://devforum.roblox.com/t/why-does-the-same-mesh-use-more-than-1-draw-call-when-duped-a-lot/3988136), consulté le 2026-11-25

> « All you need to do is to right click them in the explorer and export them. »
> — [Roblox DevForum](https://devforum.roblox.com/t/why-does-the-same-mesh-use-more-than-1-draw-call-when-duped-a-lot/3988136), consulté le 2026-11-25

> « So for example; if you have multiple identical meshes stored into the same Grid, the draw call will always stay at 1 only. »
> — [Roblox DevForum](https://devforum.roblox.com/t/why-does-the-same-mesh-use-more-than-1-draw-call-when-duped-a-lot/3988136), consulté le 2026-11-25


## Problèmes connus

À compléter.

## Alternatives

À compléter.

## Tests dans Roblox Studio

- Testé : **non**
- Conditions : —
- Résultat : —

## Questions ouvertes

- Quels réglages exacts (valeurs, propriétés) pour « draw calls instancing » ?
- Le résultat tient-il de nuit, à la lampe torche, sur mobile ?

## Scores (diagnostic, pas une preuve)

- Pertinence sujet : 1.0 · Contenu technique : 0.76 · Lien Roblox : oui
- Termes techniques repérés : surfaceappearance, lod, material, texture, performance, render, rendering, export, import, draw call
