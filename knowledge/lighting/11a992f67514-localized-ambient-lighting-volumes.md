---
id: "vdn-11a992f67514"
title: "Localized Ambient Lighting Volumes"
domain: "lighting"
subdomain: "lighting"
status: "documente"
tested_in_studio: "non"
confidence: "faible"
confidence_reason: "2 passages techniques dont 1 avec action et objet identifiables, source de niveau 2 ; indice technique seulement, procédure complète non garantie ; aucun test dans Roblox Studio."
engine_version: "inconnue"
source_tier: 2
provider: "devforum"
official: false
sources:
  - "https://devforum.roblox.com/t/5000799"
accessed: "2026-11-25"
queries:
  - "Lighting Ambient"
created: "2026-11-25"
updated: "2026-11-25"
tags:
  - "vdn"
  - "lighting"
  - "lighting"
  - "documente"
staff_posts: 0
accepted_answer: false
last_posted: "2026-11-22"
---

# Localized Ambient Lighting Volumes

> **Documenté** · source [Roblox DevForum](https://devforum.roblox.com/t/localized-ambient-lighting-volumes/5000799) · consultée le 2026-11-25 · **non testée dans Roblox Studio**

## Objectif

Répondre à : *Lighting Ambient* (sujet : Éclairage de nuit et lampe torche).

## Description technique

À rédiger à partir des extraits ci-dessous (analyse humaine ou Ollama). Rien n'est affirmé ici sans source.

## Étapes reproductibles

Instructions extraites automatiquement : procedure partielle, ordre et fonctionnement non verifies.

1. BaseParts inside Zone A will use its value (ex: Color3.new(0.5,0.5,0.5)) instead of Lighting.Ambient’s and become bright while BaseParts in Zone B will use its value (ex: Color3.new(0,0,0)) and their shadows will be dark. -- [Roblox DevForum](https://devforum.roblox.com/t/localized-ambient-lighting-volumes/5000799)

## Paramètres (sourcés)

Aucun paramètre chiffré trouvé dans les extraits.

## Limites connues de Roblox

Aucune limite explicite trouvée dans les extraits.

## Extraits justificatifs

> « BaseParts inside Zone A will use its value (ex: Color3.new(0.5,0.5,0.5)) instead of Lighting.Ambient’s and become bright while BaseParts in Zone B will use its value (ex: Color3.new(0,0,0)) and their shadows will be dark. »
> — [Roblox DevForum](https://devforum.roblox.com/t/localized-ambient-lighting-volumes/5000799), consulté le 2026-11-25

> « Developers would finally be able to have dark areas and bright areas side-by-side without having to choose a workaround that either is heavy on performance or makes dark areas bright just because you’re standing in a bright area. »
> — [Roblox DevForum](https://devforum.roblox.com/t/localized-ambient-lighting-volumes/5000799), consulté le 2026-11-25


## Problèmes connus

À compléter.

## Alternatives

À compléter.

## Tests dans Roblox Studio

- Testé : **non**
- Conditions : —
- Résultat : —

## Questions ouvertes

- Quels réglages exacts (valeurs, propriétés) pour « Lighting Ambient » ?
- Quelles limites Roblox (performances, rendu à distance, appareils) pour « Lighting Ambient » ?
- Le résultat tient-il de nuit, à la lampe torche, sur mobile ?

## Scores (diagnostic, pas une preuve)

- Pertinence sujet : 0.667 · Contenu technique : 0.4 · Lien Roblox : oui
- Termes techniques repérés : shadows, lighting, performance, brightness
