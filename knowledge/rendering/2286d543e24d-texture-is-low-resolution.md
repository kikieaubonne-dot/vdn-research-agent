---
id: "vdn-2286d543e24d"
title: "Texture is low resolution"
domain: "rendering"
subdomain: "rendering"
status: "documente"
tested_in_studio: "non"
confidence: "faible"
confidence_reason: "2 passages techniques dont 1 avec action et objet identifiables, source de niveau 1 (réponse du personnel Roblox / doc officielle) ; indice technique seulement, procédure complète non garantie ; aucun test dans Roblox Studio."
engine_version: "inconnue"
source_tier: 1
provider: "devforum"
official: true
sources:
  - "https://devforum.roblox.com/t/2084584"
accessed: "2026-11-22"
queries:
  - "texture resolution limit"
created: "2026-11-22"
updated: "2026-11-22"
tags:
  - "vdn"
  - "rendering"
  - "rendering"
  - "documente"
staff_posts: 1
accepted_answer: true
last_posted: "2022-12-23"
---

# Texture is low resolution

> **Documenté** · source [Roblox DevForum](https://devforum.roblox.com/t/texture-is-low-resolution/2084584) · consultée le 2026-11-22 · **non testée dans Roblox Studio**

## Objectif

Répondre à : *texture resolution limit* (sujet : Rendu PBR et maillages).

## Description technique

À rédiger à partir des extraits ci-dessous (analyse humaine ou Ollama). Rien n'est affirmé ici sans source.

## Étapes reproductibles

Instructions extraites automatiquement : procedure partielle, ordre et fonctionnement non verifies.

1. MaterialVariants (custom materials) allow you to set their own size which would fix the low resolution and also each MaterialVariant can have its own normal and metallic values to get the glossy look. -- [Roblox DevForum](https://devforum.roblox.com/t/texture-is-low-resolution/2084584)

## Paramètres (sourcés)

- « MaterialVariants (custom materials) allow you to set their own size which would fix the low resolution and also each MaterialVariant can have its own normal and metallic values to get the glossy look. » — [Roblox DevForum](https://devforum.roblox.com/t/texture-is-low-resolution/2084584)

## Limites connues de Roblox

- « I baked a few materials into one texture but because roblox only allows 1024x1024 its very pixelated can i fix this somehow or will i have to make a mesh for each material » — [Roblox DevForum](https://devforum.roblox.com/t/texture-is-low-resolution/2084584)

## Extraits justificatifs

> « I baked a few materials into one texture but because roblox only allows 1024x1024 its very pixelated can i fix this somehow or will i have to make a mesh for each material »
> — [Roblox DevForum](https://devforum.roblox.com/t/texture-is-low-resolution/2084584), consulté le 2026-11-22

> « MaterialVariants (custom materials) allow you to set their own size which would fix the low resolution and also each MaterialVariant can have its own normal and metallic values to get the glossy look. »
> — [Roblox DevForum](https://devforum.roblox.com/t/texture-is-low-resolution/2084584), consulté le 2026-11-22


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

- Pertinence sujet : 0.633 · Contenu technique : 0.44 · Lien Roblox : oui
- Termes techniques repérés : material, materialvariant, texture, textures, resolution
