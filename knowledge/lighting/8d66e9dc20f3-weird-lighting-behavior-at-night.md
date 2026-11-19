---
id: "vdn-8d66e9dc20f3"
title: "Weird lighting behavior at night"
domain: "lighting"
subdomain: "lighting"
status: "documente"
tested_in_studio: "non"
confidence: "faible"
confidence_reason: "4 passages techniques dont 2 avec action et objet identifiables, source de niveau 2 ; indice technique seulement, procédure complète non garantie ; aucun test dans Roblox Studio."
engine_version: "inconnue"
source_tier: 2
provider: "devforum"
official: false
sources:
  - "https://devforum.roblox.com/t/1944091"
accessed: "2026-11-19"
queries:
  - "Future lighting night"
created: "2026-11-19"
updated: "2026-11-19"
tags:
  - "vdn"
  - "lighting"
  - "lighting"
  - "documente"
staff_posts: 0
accepted_answer: true
last_posted: "2022-09-04"
---

# Weird lighting behavior at night

> **Documenté** · source [Roblox DevForum](https://devforum.roblox.com/t/weird-lighting-behavior-at-night/1944091) · consultée le 2026-11-19 · **non testée dans Roblox Studio**

## Objectif

Répondre à : *Future lighting night* (sujet : Éclairage de nuit et lampe torche).

## Description technique

À rédiger à partir des extraits ci-dessous (analyse humaine ou Ollama). Rien n'est affirmé ici sans source.

## Étapes reproductibles

Instructions extraites automatiquement : procedure partielle, ordre et fonctionnement non verifies.

1. tweenService:Create(game.Lighting,TweenInfo.new(waitTime,Enum.EasingStyle.Quad,Enum.EasingDirection.In),{ClockTime = toTween}):Play() -- [Roblox DevForum](https://devforum.roblox.com/t/weird-lighting-behavior-at-night/1944091)
2. I’ve tried deleting all lighting descendants, resetting lighting to default, and even removing all property changes in my day and night module to hopefully even notice a slight change but nothing. -- [Roblox DevForum](https://devforum.roblox.com/t/weird-lighting-behavior-at-night/1944091)

## Paramètres (sourcés)

- « local toTween = game.Lighting.ClockTime+timeShift » — [Roblox DevForum](https://devforum.roblox.com/t/weird-lighting-behavior-at-night/1944091)
- « tweenService:Create(game.Lighting,TweenInfo.new(waitTime,Enum.EasingStyle.Quad,Enum.EasingDirection.In),{ClockTime = toTween}):Play() » — [Roblox DevForum](https://devforum.roblox.com/t/weird-lighting-behavior-at-night/1944091)
- « To compensate for the brightness, the sky must be very bright. » — [Roblox DevForum](https://devforum.roblox.com/t/weird-lighting-behavior-at-night/1944091)

## Limites connues de Roblox

Aucune limite explicite trouvée dans les extraits.

## Extraits justificatifs

> « local toTween = game.Lighting.ClockTime+timeShift »
> — [Roblox DevForum](https://devforum.roblox.com/t/weird-lighting-behavior-at-night/1944091), consulté le 2026-11-19

> « tweenService:Create(game.Lighting,TweenInfo.new(waitTime,Enum.EasingStyle.Quad,Enum.EasingDirection.In),{ClockTime = toTween}):Play() »
> — [Roblox DevForum](https://devforum.roblox.com/t/weird-lighting-behavior-at-night/1944091), consulté le 2026-11-19

> « I’ve tried deleting all lighting descendants, resetting lighting to default, and even removing all property changes in my day and night module to hopefully even notice a slight change but nothing. »
> — [Roblox DevForum](https://devforum.roblox.com/t/weird-lighting-behavior-at-night/1944091), consulté le 2026-11-19

> « To compensate for the brightness, the sky must be very bright. »
> — [Roblox DevForum](https://devforum.roblox.com/t/weird-lighting-behavior-at-night/1944091), consulté le 2026-11-19


## Problèmes connus

À compléter.

## Alternatives

À compléter.

## Tests dans Roblox Studio

- Testé : **non**
- Conditions : —
- Résultat : —

## Questions ouvertes

- Quelles limites Roblox (performances, rendu à distance, appareils) pour « Future lighting night » ?
- Le résultat tient-il de nuit, à la lampe torche, sur mobile ?

## Scores (diagnostic, pas une preuve)

- Pertinence sujet : 0.5 · Contenu technique : 0.56 · Lien Roblox : oui
- Termes techniques repérés : lighting, brightness
