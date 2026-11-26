---
id: "vdn-60c115e3f8a7"
title: "How can I add working collisions to a custom character controller?"
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
  - "https://devforum.roblox.com/t/3052676"
accessed: "2026-11-26"
queries:
  - "custom character controller"
created: "2026-11-26"
updated: "2026-11-26"
tags:
  - "vdn"
  - "gameplay"
  - "movement"
  - "candidat"
staff_posts: 0
accepted_answer: false
last_posted: "2026-08-06"
---

# How can I add working collisions to a custom character controller?

> **Candidat** · source [Roblox DevForum](https://devforum.roblox.com/t/how-can-i-add-working-collisions-to-a-custom-character-controller/3052676) · consultée le 2026-11-26 · **non testée dans Roblox Studio**

## Objectif

Répondre à : *custom character controller* (sujet : Mouvements et contrôleur de personnage).

## Description technique

À rédiger à partir des extraits ci-dessous (analyse humaine ou Ollama). Rien n'est affirmé ici sans source.

## Étapes reproductibles

Instructions extraites automatiquement : procedure partielle, ordre et fonctionnement non verifies.

Aucune instruction complete identifiee. Ne pas présenter cette fiche comme un tutoriel. Consulter la source.

## Paramètres (sourcés)

- « local DoesFloorExist = workspace:Raycast(self.CFrame.Position, Vector3.new(0, -1, 0) * 2.6, PhysicsRaycastParams) » — [Roblox DevForum](https://devforum.roblox.com/t/how-can-i-add-working-collisions-to-a-custom-character-controller/3052676)

## Limites connues de Roblox

Aucune limite explicite trouvée dans les extraits.

## Extraits justificatifs

> « local DoesFloorExist = workspace:Raycast(self.CFrame.Position, Vector3.new(0, -1, 0) * 2.6, PhysicsRaycastParams) »
> — [Roblox DevForum](https://devforum.roblox.com/t/how-can-i-add-working-collisions-to-a-custom-character-controller/3052676), consulté le 2026-11-26

> « Then for forward collisions just use a raycast (or a few) going forwards and if they hit anything stop the character. »
> — [Roblox DevForum](https://devforum.roblox.com/t/how-can-i-add-working-collisions-to-a-custom-character-controller/3052676), consulté le 2026-11-26

> « Try canceling out the force as soon as the ground raycast detects an instance (by setting your player’s y value to 0) and then correct them onto the ground. »
> — [Roblox DevForum](https://devforum.roblox.com/t/how-can-i-add-working-collisions-to-a-custom-character-controller/3052676), consulté le 2026-11-26


## Problèmes connus

À compléter.

## Alternatives

À compléter.

## Tests dans Roblox Studio

- Testé : **non**
- Conditions : —
- Résultat : —

## Questions ouvertes

- Quelles limites Roblox (performances, rendu à distance, appareils) pour « custom character controller » ?
- Le résultat tient-il de nuit, à la lampe torche, sur mobile ?

## Scores (diagnostic, pas une preuve)

- Pertinence sujet : 0.5 · Contenu technique : 0.44 · Lien Roblox : oui
- Termes techniques repérés : rendering, raycast
