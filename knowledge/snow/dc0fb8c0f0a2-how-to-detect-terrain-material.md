---
id: "vdn-dc0fb8c0f0a2"
title: "How to Detect Terrain Material"
domain: "snow"
subdomain: "snow"
status: "candidat"
tested_in_studio: "non"
confidence: "faible"
confidence_reason: "4 passage(s) technique(s), 0 instruction(s) explicite(s) repérée(s), source de niveau 2 ; procédure à approfondir et à tester."
engine_version: "inconnue"
source_tier: 2
provider: "devforum"
official: false
sources:
  - "https://devforum.roblox.com/t/1274032"
accessed: "2026-11-16"
queries:
  - "snow terrain material"
created: "2026-11-16"
updated: "2026-11-16"
tags:
  - "vdn"
  - "snow"
  - "snow"
  - "candidat"
staff_posts: 0
accepted_answer: true
last_posted: "2021-06-05"
---

# How to Detect Terrain Material

> **Candidat** · source [Roblox DevForum](https://devforum.roblox.com/t/how-to-detect-terrain-material/1274032) · consultée le 2026-11-16 · **non testée dans Roblox Studio**

## Objectif

Répondre à : *snow terrain material* (sujet : Neige, givre et traces).

## Description technique

À rédiger à partir des extraits ci-dessous (analyse humaine ou Ollama). Rien n'est affirmé ici sans source.

## Étapes reproductibles

Instructions extraites automatiquement : procedure partielle, ordre et fonctionnement non verifies.

Aucune instruction complete identifiee. Ne pas présenter cette fiche comme un tutoriel. Consulter la source.

## Paramètres (sourcés)

- « local _, _, _, material = workspace:FindPartOnRayWithWhitelist(ray, {workspace.Terrain}) » — [Roblox DevForum](https://devforum.roblox.com/t/how-to-detect-terrain-material/1274032)
- « local _, _, _, material = workspace:FindPartOnRayWithWhitelist(ray, {workspace.Terrain}, true)) » — [Roblox DevForum](https://devforum.roblox.com/t/how-to-detect-terrain-material/1274032)

## Limites connues de Roblox

- « Basically what he said is that the material of the terrain object is technically undefined so the only thing you can do is raycast it below the part. » — [Roblox DevForum](https://devforum.roblox.com/t/how-to-detect-terrain-material/1274032)

## Extraits justificatifs

> « Detect smooth terrain material under part Scripting Support »
> — [Roblox DevForum](https://devforum.roblox.com/t/how-to-detect-terrain-material/1274032), consulté le 2026-11-16

> « Basically what he said is that the material of the terrain object is technically undefined so the only thing you can do is raycast it below the part. »
> — [Roblox DevForum](https://devforum.roblox.com/t/how-to-detect-terrain-material/1274032), consulté le 2026-11-16

> « local _, _, _, material = workspace:FindPartOnRayWithWhitelist(ray, {workspace.Terrain}) »
> — [Roblox DevForum](https://devforum.roblox.com/t/how-to-detect-terrain-material/1274032), consulté le 2026-11-16

> « local _, _, _, material = workspace:FindPartOnRayWithWhitelist(ray, {workspace.Terrain}, true)) »
> — [Roblox DevForum](https://devforum.roblox.com/t/how-to-detect-terrain-material/1274032), consulté le 2026-11-16


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

- Pertinence sujet : 0.5 · Contenu technique : 0.6 · Lien Roblox : oui
- Termes techniques repérés : material, raycast, terrain
