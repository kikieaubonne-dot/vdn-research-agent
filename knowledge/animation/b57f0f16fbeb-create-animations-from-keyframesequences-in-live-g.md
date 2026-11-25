---
id: "vdn-b57f0f16fbeb"
title: "Create Animations from KeyframeSequences in live games"
domain: "animation"
subdomain: "blender_animation"
status: "candidat"
tested_in_studio: "non"
confidence: "faible"
confidence_reason: "3 passage(s) technique(s), 0 instruction(s) explicite(s) repérée(s), source de niveau 2 ; procédure à approfondir et à tester."
engine_version: "inconnue"
source_tier: 2
provider: "devforum"
official: false
sources:
  - "https://devforum.roblox.com/t/2222384"
accessed: "2026-11-25"
queries:
  - "KeyframeSequence import"
created: "2026-11-25"
updated: "2026-11-25"
tags:
  - "vdn"
  - "animation"
  - "blender_animation"
  - "candidat"
staff_posts: 0
accepted_answer: false
last_posted: "2025-02-27"
---

# Create Animations from KeyframeSequences in live games

> **Candidat** · source [Roblox DevForum](https://devforum.roblox.com/t/create-animations-from-keyframesequences-in-live-games/2222384) · consultée le 2026-11-25 · **non testée dans Roblox Studio**

## Objectif

Répondre à : *KeyframeSequence import* (sujet : Animations Blender vers Roblox).

## Description technique

À rédiger à partir des extraits ci-dessous (analyse humaine ou Ollama). Rien n'est affirmé ici sans source.

## Étapes reproductibles

Instructions extraites automatiquement : procedure partielle, ordre et fonctionnement non verifies.

Aucune instruction complete identifiee. Ne pas présenter cette fiche comme un tutoriel. Consulter la source.

## Paramètres (sourcés)

Aucun paramètre chiffré trouvé dans les extraits.

## Limites connues de Roblox

- « Animations are unreliable for event-based programming, forcing you to write additional code in case a animation hasn’t loaded yet or fails to load entirely, such as for weapon reload animations or character actions where some logic only runs at specific keyframes. » — [Roblox DevForum](https://devforum.roblox.com/t/create-animations-from-keyframesequences-in-live-games/2222384)

## Extraits justificatifs

> « As of now, we have to manually publish each change to an Animation because there are no automated alternatives. »
> — [Roblox DevForum](https://devforum.roblox.com/t/create-animations-from-keyframesequences-in-live-games/2222384), consulté le 2026-11-25

> « This way we could easily create and modify animation keyframes at a whim and then turn them all into Animations during runtime without having to worry about reuploading animations constantly. »
> — [Roblox DevForum](https://devforum.roblox.com/t/create-animations-from-keyframesequences-in-live-games/2222384), consulté le 2026-11-25

> « Animations are unreliable for event-based programming, forcing you to write additional code in case a animation hasn’t loaded yet or fails to load entirely, such as for weapon reload animations or character actions where some logic only runs at specific keyframes. »
> — [Roblox DevForum](https://devforum.roblox.com/t/create-animations-from-keyframesequences-in-live-games/2222384), consulté le 2026-11-25


## Problèmes connus

À compléter.

## Alternatives

À compléter.

## Tests dans Roblox Studio

- Testé : **non**
- Conditions : —
- Résultat : —

## Questions ouvertes

- Quels réglages exacts (valeurs, propriétés) pour « KeyframeSequence import » ?
- Le résultat tient-il de nuit, à la lampe torche, sur mobile ?

## Scores (diagnostic, pas une preuve)

- Pertinence sujet : 0.5 · Contenu technique : 0.44 · Lien Roblox : oui
- Termes techniques repérés : rig, animation
