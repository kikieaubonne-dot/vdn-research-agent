---
id: "vdn-a0af8915f7ed"
title: "Animation speed changes according to humanoid walkspeed"
domain: "gameplay"
subdomain: "movement"
status: "candidat"
tested_in_studio: "non"
confidence: "faible"
confidence_reason: "3 passage(s) technique(s), 0 instruction(s) explicite(s) repérée(s), source de niveau 2 ; procédure à approfondir et à tester."
engine_version: "inconnue"
source_tier: 2
provider: "devforum"
official: false
sources:
  - "https://devforum.roblox.com/t/847421"
accessed: "2026-11-25"
queries:
  - "Humanoid WalkSpeed smoothing"
created: "2026-11-25"
updated: "2026-11-25"
tags:
  - "vdn"
  - "gameplay"
  - "movement"
  - "candidat"
staff_posts: 0
accepted_answer: true
last_posted: "2021-05-14"
---

# Animation speed changes according to humanoid walkspeed

> **Candidat** · source [Roblox DevForum](https://devforum.roblox.com/t/animation-speed-changes-according-to-humanoid-walkspeed/847421) · consultée le 2026-11-25 · **non testée dans Roblox Studio**

## Objectif

Répondre à : *Humanoid WalkSpeed smoothing* (sujet : Mouvements et contrôleur de personnage).

## Description technique

À rédiger à partir des extraits ci-dessous (analyse humaine ou Ollama). Rien n'est affirmé ici sans source.

## Étapes reproductibles

Instructions extraites automatiquement : procedure partielle, ordre et fonctionnement non verifies.

Aucune instruction complete identifiee. Ne pas présenter cette fiche comme un tutoriel. Consulter la source.

## Paramètres (sourcés)

- « local speedFactor = 0.5 -- half animation speed » — [Roblox DevForum](https://devforum.roblox.com/t/animation-speed-changes-according-to-humanoid-walkspeed/847421)

## Limites connues de Roblox

Aucune limite explicite trouvée dans les extraits.

## Extraits justificatifs

> « What I mean by that is that if I change the humanoid walkspeed to 100, my run animation would look as if the walkspeed is set to the default 16. »
> — [Roblox DevForum](https://devforum.roblox.com/t/animation-speed-changes-according-to-humanoid-walkspeed/847421), consulté le 2026-11-25

> « I don’t want the animation to move that fast even tho the walkspeed value is set to 100, i want to to seem like it’s set to 16 or something natural. »
> — [Roblox DevForum](https://devforum.roblox.com/t/animation-speed-changes-according-to-humanoid-walkspeed/847421), consulté le 2026-11-25

> « local speedFactor = 0.5 -- half animation speed »
> — [Roblox DevForum](https://devforum.roblox.com/t/animation-speed-changes-according-to-humanoid-walkspeed/847421), consulté le 2026-11-25


## Problèmes connus

À compléter.

## Alternatives

À compléter.

## Tests dans Roblox Studio

- Testé : **non**
- Conditions : —
- Résultat : —

## Questions ouvertes

- Quelles limites Roblox (performances, rendu à distance, appareils) pour « Humanoid WalkSpeed smoothing » ?
- Le résultat tient-il de nuit, à la lampe torche, sur mobile ?

## Scores (diagnostic, pas une preuve)

- Pertinence sujet : 0.833 · Contenu technique : 0.4 · Lien Roblox : oui
- Termes techniques repérés : animation
