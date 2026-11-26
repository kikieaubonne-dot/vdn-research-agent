---
id: "vdn-b388cda6f2c8"
title: "How to make head and arms face camera LookVector IN FIRST PERSON?"
domain: "animation"
subdomain: "fp_hands"
status: "documente"
tested_in_studio: "non"
confidence: "moyenne"
confidence_reason: "3 passages techniques dont 1 avec action et objet identifiables, source de niveau 1 (réponse du personnel Roblox / doc officielle) ; indice technique seulement, procédure complète non garantie ; aucun test dans Roblox Studio."
engine_version: "inconnue"
source_tier: 1
provider: "devforum"
official: true
sources:
  - "https://devforum.roblox.com/t/2232713"
accessed: "2026-11-26"
queries:
  - "first person arms rig"
created: "2026-11-26"
updated: "2026-11-26"
tags:
  - "vdn"
  - "animation"
  - "fp_hands"
  - "documente"
staff_posts: 1
accepted_answer: true
last_posted: "2023-03-30"
---

# How to make head and arms face camera LookVector IN FIRST PERSON?

> **Documenté** · source [Roblox DevForum](https://devforum.roblox.com/t/how-to-make-head-and-arms-face-camera-lookvector-in-first-person/2232713) · consultée le 2026-11-26 · **non testée dans Roblox Studio**

## Objectif

Répondre à : *first person arms rig* (sujet : Mains et bras en vue FPS).

## Description technique

À rédiger à partir des extraits ci-dessous (analyse humaine ou Ollama). Rien n'est affirmé ici sans source.

## Étapes reproductibles

Instructions extraites automatiquement : procedure partielle, ordre et fonctionnement non verifies.

1. You could just use the new IK Control and a loop which moves a attachment that is parented to terrain, based on where the player is looking on the client. -- [Roblox DevForum](https://devforum.roblox.com/t/how-to-make-head-and-arms-face-camera-lookvector-in-first-person/2232713)

## Paramètres (sourcés)

- « Rig.Main.CFrame = workspace.CurrentCamera.CFrame » — [Roblox DevForum](https://devforum.roblox.com/t/how-to-make-head-and-arms-face-camera-lookvector-in-first-person/2232713)

## Limites connues de Roblox

Aucune limite explicite trouvée dans les extraits.

## Extraits justificatifs

> « You can weld the arms and head together to make what we call a “ViewModel” or “Rig” and set the CFrame to the Camera CFrame in a RenderStepped loop! »
> — [Roblox DevForum](https://devforum.roblox.com/t/how-to-make-head-and-arms-face-camera-lookvector-in-first-person/2232713), consulté le 2026-11-26

> « Rig.Main.CFrame = workspace.CurrentCamera.CFrame »
> — [Roblox DevForum](https://devforum.roblox.com/t/how-to-make-head-and-arms-face-camera-lookvector-in-first-person/2232713), consulté le 2026-11-26

> « You could just use the new IK Control and a loop which moves a attachment that is parented to terrain, based on where the player is looking on the client. »
> — [Roblox DevForum](https://devforum.roblox.com/t/how-to-make-head-and-arms-face-camera-lookvector-in-first-person/2232713), consulté le 2026-11-26


## Problèmes connus

À compléter.

## Alternatives

À compléter.

## Tests dans Roblox Studio

- Testé : **non**
- Conditions : —
- Résultat : —

## Questions ouvertes

- Quelles limites Roblox (performances, rendu à distance, appareils) pour « first person arms rig » ?
- Le résultat tient-il de nuit, à la lampe torche, sur mobile ?

## Scores (diagnostic, pas une preuve)

- Pertinence sujet : 0.667 · Contenu technique : 0.44 · Lien Roblox : oui
- Termes techniques repérés : rig, terrain
