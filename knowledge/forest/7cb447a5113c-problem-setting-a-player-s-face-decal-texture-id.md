---
id: "vdn-7cb447a5113c"
title: "Problem setting a Player's face decal texture Id"
domain: "forest"
subdomain: "forest"
status: "candidat"
tested_in_studio: "non"
confidence: "faible"
confidence_reason: "2 passage(s) technique(s), 0 instruction(s) explicite(s) repérée(s), source de niveau 2 ; procédure à approfondir et à tester."
engine_version: "inconnue"
source_tier: 2
provider: "devforum"
official: false
sources:
  - "https://devforum.roblox.com/t/1277548"
accessed: "2026-11-17"
queries:
  - "Player settings"
created: "2026-11-17"
updated: "2026-11-17"
tags:
  - "vdn"
  - "forest"
  - "forest"
  - "candidat"
staff_posts: 0
accepted_answer: true
last_posted: "2021-06-07"
---

# Problem setting a Player's face decal texture Id

> **Candidat** · source [Roblox DevForum](https://devforum.roblox.com/t/problem-setting-a-players-face-decal-texture-id/1277548) · consultée le 2026-11-17 · **non testée dans Roblox Studio**

## Objectif

Répondre à : *Player settings* (sujet : Forêt nocturne enneigée).

## Description technique

À rédiger à partir des extraits ci-dessous (analyse humaine ou Ollama). Rien n'est affirmé ici sans source.

## Étapes reproductibles

Instructions extraites automatiquement : procedure partielle, ordre et fonctionnement non verifies.

Aucune instruction complete identifiee. Ne pas présenter cette fiche comme un tutoriel. Consulter la source.

## Paramètres (sourcés)

- « local Decal = Head:WaitForChild("face",15) or Head:WaitForChild("Face",15) » — [Roblox DevForum](https://devforum.roblox.com/t/problem-setting-a-players-face-decal-texture-id/1277548)
- « local DefaultFace = string.match(Decal.Texture,"%d+") » — [Roblox DevForum](https://devforum.roblox.com/t/problem-setting-a-players-face-decal-texture-id/1277548)

## Limites connues de Roblox

Aucune limite explicite trouvée dans les extraits.

## Extraits justificatifs

> « local Decal = Head:WaitForChild("face",15) or Head:WaitForChild("Face",15) »
> — [Roblox DevForum](https://devforum.roblox.com/t/problem-setting-a-players-face-decal-texture-id/1277548), consulté le 2026-11-17

> « local DefaultFace = string.match(Decal.Texture,"%d+") »
> — [Roblox DevForum](https://devforum.roblox.com/t/problem-setting-a-players-face-decal-texture-id/1277548), consulté le 2026-11-17


## Problèmes connus

À compléter.

## Alternatives

À compléter.

## Tests dans Roblox Studio

- Testé : **non**
- Conditions : —
- Résultat : —

## Questions ouvertes

- Quelles limites Roblox (performances, rendu à distance, appareils) pour « Player settings » ?
- Le résultat tient-il de nuit, à la lampe torche, sur mobile ?

## Scores (diagnostic, pas une preuve)

- Pertinence sujet : 0.5 · Contenu technique : 0.32 · Lien Roblox : oui
- Termes techniques repérés : texture, decal
