---
id: "vdn-d03d2ba87091"
title: "EditableImage higher resolution and memory limit"
domain: "rendering"
subdomain: "rendering"
status: "candidat"
tested_in_studio: "non"
confidence: "faible"
confidence_reason: "3 passage(s) technique(s), 0 instruction(s) explicite(s) repérée(s), source de niveau 2 ; procédure à approfondir et à tester."
engine_version: "inconnue"
source_tier: 2
provider: "devforum"
official: false
sources:
  - "https://devforum.roblox.com/t/4389575"
accessed: "2026-11-22"
queries:
  - "texture resolution limit"
created: "2026-11-22"
updated: "2026-11-22"
tags:
  - "vdn"
  - "rendering"
  - "rendering"
  - "candidat"
staff_posts: 0
accepted_answer: false
last_posted: "2026-11-22"
---

# EditableImage higher resolution and memory limit

> **Candidat** · source [Roblox DevForum](https://devforum.roblox.com/t/editableimage-higher-resolution-and-memory-limit/4389575) · consultée le 2026-11-22 · **non testée dans Roblox Studio**

## Objectif

Répondre à : *texture resolution limit* (sujet : Rendu PBR et maillages).

## Description technique

À rédiger à partir des extraits ci-dessous (analyse humaine ou Ollama). Rien n'est affirmé ici sans source.

## Étapes reproductibles

Instructions extraites automatiquement : procedure partielle, ordre et fonctionnement non verifies.

Aucune instruction complete identifiee. Ne pas présenter cette fiche comme un tutoriel. Consulter la source.

## Paramètres (sourcés)

- « Having 4096x4096 resolution and a 128MB limit should be the minimum, but I would be fine seeing any higher resolution/memory limits being added to Extended Services. » — [Roblox DevForum](https://devforum.roblox.com/t/editableimage-higher-resolution-and-memory-limit/4389575)

## Limites connues de Roblox

- « Having 4096x4096 resolution and a 128MB limit should be the minimum, but I would be fine seeing any higher resolution/memory limits being added to Extended Services. » — [Roblox DevForum](https://devforum.roblox.com/t/editableimage-higher-resolution-and-memory-limit/4389575)
- « I’m using EditableImages for rendering SVGs (from pre-compiled list made by python script) and I had to make LRU cache to make sure limit is never exceeded even when I have many 64x64 icons. » — [Roblox DevForum](https://devforum.roblox.com/t/editableimage-higher-resolution-and-memory-limit/4389575)

## Extraits justificatifs

> « Having 4096x4096 resolution and a 128MB limit should be the minimum, but I would be fine seeing any higher resolution/memory limits being added to Extended Services. »
> — [Roblox DevForum](https://devforum.roblox.com/t/editableimage-higher-resolution-and-memory-limit/4389575), consulté le 2026-11-22

> « my specific use case relates to art games, and while yes i can tile 4 1024 * 1024 images together and implement loading zones to prevent memory issues »
> — [Roblox DevForum](https://devforum.roblox.com/t/editableimage-higher-resolution-and-memory-limit/4389575), consulté le 2026-11-22

> « I’m using EditableImages for rendering SVGs (from pre-compiled list made by python script) and I had to make LRU cache to make sure limit is never exceeded even when I have many 64x64 icons. »
> — [Roblox DevForum](https://devforum.roblox.com/t/editableimage-higher-resolution-and-memory-limit/4389575), consulté le 2026-11-22


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

- Pertinence sujet : 0.7 · Contenu technique : 0.52 · Lien Roblox : oui
- Termes techniques repérés : texture, rendering, resolution, 1024
