---
id: "vdn-0ded63993d38"
title: "[Regression] Major performance regression for text rendering"
domain: "performance"
subdomain: "performance"
status: "candidat"
tested_in_studio: "non"
confidence: "faible"
confidence_reason: "3 passage(s) technique(s), 0 instruction(s) explicite(s) repérée(s), source de niveau 2 ; procédure à approfondir et à tester."
engine_version: "inconnue"
source_tier: 2
provider: "devforum"
official: false
sources:
  - "https://devforum.roblox.com/t/195029"
accessed: "2026-11-25"
queries:
  - "MicroProfiler rendering"
created: "2026-11-25"
updated: "2026-11-25"
tags:
  - "vdn"
  - "performance"
  - "performance"
  - "candidat"
staff_posts: 0
accepted_answer: false
last_posted: "2018-10-31"
---

# [Regression] Major performance regression for text rendering

> **Candidat** · source [Roblox DevForum](https://devforum.roblox.com/t/regression-major-performance-regression-for-text-rendering/195029) · consultée le 2026-11-25 · **non testée dans Roblox Studio**

## Objectif

Répondre à : *MicroProfiler rendering* (sujet : Performances et niveaux de détail).

## Description technique

À rédiger à partir des extraits ci-dessous (analyse humaine ou Ollama). Rien n'est affirmé ici sans source.

## Étapes reproductibles

Instructions extraites automatiquement : procedure partielle, ordre et fonctionnement non verifies.

Aucune instruction complete identifiee. Ne pas présenter cette fiche comme un tutoriel. Consulter la source.

## Paramètres (sourcés)

Aucun paramètre chiffré trouvé dans les extraits.

## Limites connues de Roblox

- « This method is run very often in the default roblox ingame chat script, so this is likely a major performance hit for any game using it (Keep in mind you only have about 16ms per frame total!). » — [Roblox DevForum](https://devforum.roblox.com/t/regression-major-performance-regression-for-text-rendering/195029)
- « There’s a bug where a relayout is being mistakenly triggered every time a TextLabel gets parented, which is what that “UI Layout” step in the microprofiler means. » — [Roblox DevForum](https://devforum.roblox.com/t/regression-major-performance-regression-for-text-rendering/195029)

## Extraits justificatifs

> « This method is run very often in the default roblox ingame chat script, so this is likely a major performance hit for any game using it (Keep in mind you only have about 16ms per frame total!). »
> — [Roblox DevForum](https://devforum.roblox.com/t/regression-major-performance-regression-for-text-rendering/195029), consulté le 2026-11-25

> « A bit about robeats internals: I disable all chat rendering while the “rhythm game” portion is active, and do all the “skipped” updates when bringing up the “song end” menu. »
> — [Roblox DevForum](https://devforum.roblox.com/t/regression-major-performance-regression-for-text-rendering/195029), consulté le 2026-11-25

> « There’s a bug where a relayout is being mistakenly triggered every time a TextLabel gets parented, which is what that “UI Layout” step in the microprofiler means. »
> — [Roblox DevForum](https://devforum.roblox.com/t/regression-major-performance-regression-for-text-rendering/195029), consulté le 2026-11-25


## Problèmes connus

À compléter.

## Alternatives

À compléter.

## Tests dans Roblox Studio

- Testé : **non**
- Conditions : —
- Résultat : —

## Questions ouvertes

- Quels réglages exacts (valeurs, propriétés) pour « MicroProfiler rendering » ?
- Le résultat tient-il de nuit, à la lampe torche, sur mobile ?

## Scores (diagnostic, pas une preuve)

- Pertinence sujet : 0.75 · Contenu technique : 0.48 · Lien Roblox : oui
- Termes techniques repérés : performance, rendering, microprofiler
