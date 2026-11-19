---
id: "vdn-61a66cca6497"
title: "How do I make the camera follow the head in first person animation?"
domain: "gameplay"
subdomain: "fps_camera"
status: "candidat"
tested_in_studio: "non"
confidence: "faible"
confidence_reason: "4 passage(s) technique(s), 0 instruction(s) explicite(s) repérée(s), source de niveau 2 ; procédure à approfondir et à tester."
engine_version: "inconnue"
source_tier: 2
provider: "devforum"
official: false
sources:
  - "https://devforum.roblox.com/t/1899197"
accessed: "2026-11-19"
queries:
  - "first person camera"
created: "2026-11-19"
updated: "2026-11-19"
tags:
  - "vdn"
  - "gameplay"
  - "fps_camera"
  - "candidat"
staff_posts: 0
accepted_answer: false
last_posted: "2022-07-29"
---

# How do I make the camera follow the head in first person animation?

> **Candidat** · source [Roblox DevForum](https://devforum.roblox.com/t/how-do-i-make-the-camera-follow-the-head-in-first-person-animation/1899197) · consultée le 2026-11-19 · **non testée dans Roblox Studio**

## Objectif

Répondre à : *first person camera* (sujet : Caméra première personne immersive).

## Description technique

À rédiger à partir des extraits ci-dessous (analyse humaine ou Ollama). Rien n'est affirmé ici sans source.

## Étapes reproductibles

Instructions extraites automatiquement : procedure partielle, ordre et fonctionnement non verifies.

Aucune instruction complete identifiee. Ne pas présenter cette fiche comme un tutoriel. Consulter la source.

## Paramètres (sourcés)

- « local animation = Instance.new("Animation") » — [Roblox DevForum](https://devforum.roblox.com/t/how-do-i-make-the-camera-follow-the-head-in-first-person-animation/1899197)
- « animation.AnimationId = "rbxassetid://10406276727" -- 10405924371 » — [Roblox DevForum](https://devforum.roblox.com/t/how-do-i-make-the-camera-follow-the-head-in-first-person-animation/1899197)
- « local animationTrack = Animator:LoadAnimation(animation) » — [Roblox DevForum](https://devforum.roblox.com/t/how-do-i-make-the-camera-follow-the-head-in-first-person-animation/1899197)
- « animation.AnimationId = "rbxassetid://10405924371" -- 10406276727 10406528662 » — [Roblox DevForum](https://devforum.roblox.com/t/how-do-i-make-the-camera-follow-the-head-in-first-person-animation/1899197)

## Limites connues de Roblox

Aucune limite explicite trouvée dans les extraits.

## Extraits justificatifs

> « local animation = Instance.new("Animation") »
> — [Roblox DevForum](https://devforum.roblox.com/t/how-do-i-make-the-camera-follow-the-head-in-first-person-animation/1899197), consulté le 2026-11-19

> « animation.AnimationId = "rbxassetid://10406276727" -- 10405924371 »
> — [Roblox DevForum](https://devforum.roblox.com/t/how-do-i-make-the-camera-follow-the-head-in-first-person-animation/1899197), consulté le 2026-11-19

> « local animationTrack = Animator:LoadAnimation(animation) »
> — [Roblox DevForum](https://devforum.roblox.com/t/how-do-i-make-the-camera-follow-the-head-in-first-person-animation/1899197), consulté le 2026-11-19

> « animation.AnimationId = "rbxassetid://10405924371" -- 10406276727 10406528662 »
> — [Roblox DevForum](https://devforum.roblox.com/t/how-do-i-make-the-camera-follow-the-head-in-first-person-animation/1899197), consulté le 2026-11-19


## Problèmes connus

À compléter.

## Alternatives

À compléter.

## Tests dans Roblox Studio

- Testé : **non**
- Conditions : —
- Résultat : —

## Questions ouvertes

- Quelles limites Roblox (performances, rendu à distance, appareils) pour « first person camera » ?
- Le résultat tient-il de nuit, à la lampe torche, sur mobile ?

## Scores (diagnostic, pas une preuve)

- Pertinence sujet : 0.75 · Contenu technique : 0.52 · Lien Roblox : oui
- Termes techniques repérés : animation
