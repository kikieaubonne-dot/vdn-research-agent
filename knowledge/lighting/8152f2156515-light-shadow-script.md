---
id: "vdn-8152f2156515"
title: "Light shadow script"
domain: "lighting"
subdomain: "lighting"
status: "candidat"
tested_in_studio: "non"
confidence: "faible"
confidence_reason: "4 passage(s) technique(s), 0 instruction(s) explicite(s) repérée(s), source de niveau 2 ; procédure à approfondir et à tester."
engine_version: "inconnue"
source_tier: 2
provider: "devforum"
official: false
sources:
  - "https://devforum.roblox.com/t/1764474"
accessed: "2026-11-18"
queries:
  - "light shadows performance"
created: "2026-11-18"
updated: "2026-11-18"
tags:
  - "vdn"
  - "lighting"
  - "lighting"
  - "candidat"
staff_posts: 0
accepted_answer: true
last_posted: "2022-04-22"
---

# Light shadow script

> **Candidat** · source [Roblox DevForum](https://devforum.roblox.com/t/light-shadow-script/1764474) · consultée le 2026-11-18 · **non testée dans Roblox Studio**

## Objectif

Répondre à : *light shadows performance* (sujet : Éclairage de nuit et lampe torche).

## Description technique

À rédiger à partir des extraits ci-dessous (analyse humaine ou Ollama). Rien n'est affirmé ici sans source.

## Étapes reproductibles

Instructions extraites automatiquement : procedure partielle, ordre et fonctionnement non verifies.

Aucune instruction complete identifiee. Ne pas présenter cette fiche comme un tutoriel. Consulter la source.

## Paramètres (sourcés)

- « if magnitude > 20 then workspace.Part.PointLight.Shadows = false » — [Roblox DevForum](https://devforum.roblox.com/t/light-shadow-script/1764474)
- « else workspace.Part.PointLight.Shadows = true » — [Roblox DevForum](https://devforum.roblox.com/t/light-shadow-script/1764474)
- « if magnitude > 20 then light.Shadows = false » — [Roblox DevForum](https://devforum.roblox.com/t/light-shadow-script/1764474)

## Limites connues de Roblox

- « as you can see here it will make pointlight shadows dissapear, but only in one part, when i duplicate part, same name, same everything, it doesn’t work » — [Roblox DevForum](https://devforum.roblox.com/t/light-shadow-script/1764474)

## Extraits justificatifs

> « if magnitude > 20 then workspace.Part.PointLight.Shadows = false »
> — [Roblox DevForum](https://devforum.roblox.com/t/light-shadow-script/1764474), consulté le 2026-11-18

> « else workspace.Part.PointLight.Shadows = true »
> — [Roblox DevForum](https://devforum.roblox.com/t/light-shadow-script/1764474), consulté le 2026-11-18

> « as you can see here it will make pointlight shadows dissapear, but only in one part, when i duplicate part, same name, same everything, it doesn’t work »
> — [Roblox DevForum](https://devforum.roblox.com/t/light-shadow-script/1764474), consulté le 2026-11-18

> « if magnitude > 20 then light.Shadows = false »
> — [Roblox DevForum](https://devforum.roblox.com/t/light-shadow-script/1764474), consulté le 2026-11-18


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

- Pertinence sujet : 0.583 · Contenu technique : 0.52 · Lien Roblox : oui
- Termes techniques repérés : shadows
