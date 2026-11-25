---
id: "vdn-6714a9b2cd01"
title: "Shadow Draw Calls are broken"
domain: "performance"
subdomain: "performance"
status: "documente"
tested_in_studio: "non"
confidence: "faible"
confidence_reason: "6 passages techniques dont 2 avec action et objet identifiables, source de niveau 2 ; indice technique seulement, procédure complète non garantie ; aucun test dans Roblox Studio."
engine_version: "inconnue"
source_tier: 2
provider: "devforum"
official: false
sources:
  - "https://devforum.roblox.com/t/4045934"
accessed: "2026-11-25"
queries:
  - "draw calls instancing"
created: "2026-11-25"
updated: "2026-11-25"
tags:
  - "vdn"
  - "performance"
  - "performance"
  - "documente"
staff_posts: 0
accepted_answer: false
last_posted: "2026-01-29"
---

# Shadow Draw Calls are broken

> **Documenté** · source [Roblox DevForum](https://devforum.roblox.com/t/shadow-draw-calls-are-broken/4045934) · consultée le 2026-11-25 · **non testée dans Roblox Studio**

## Objectif

Répondre à : *draw calls instancing* (sujet : Performances et niveaux de détail).

## Description technique

À rédiger à partir des extraits ci-dessous (analyse humaine ou Ollama). Rien n'est affirmé ici sans source.

## Étapes reproductibles

Instructions extraites automatiquement : procedure partielle, ordre et fonctionnement non verifies.

1. Add approximately 16 or more PointLight objects (with Shadows.Enabled = true) and 50 or more assets (e.g., PBR meshes, shelves, barrels, or other complex geometry). -- [Roblox DevForum](https://devforum.roblox.com/t/shadow-draw-calls-are-broken/4045934)
2. Since this disables shadows from the sun, which by and far use most draw calls due to cascaded shadowmap. -- [Roblox DevForum](https://devforum.roblox.com/t/shadow-draw-calls-are-broken/4045934)

## Paramètres (sourcés)

- « Add approximately 16 or more PointLight objects (with Shadows.Enabled = true) and 50 or more assets (e.g., PBR meshes, shelves, barrels, or other complex geometry). » — [Roblox DevForum](https://devforum.roblox.com/t/shadow-draw-calls-are-broken/4045934)

## Limites connues de Roblox

- « I expect that when an object moves under light sources, it should only force those specific lights to recalculate their shadows, rather than causing a near-global recalculation of the entire shadow map. » — [Roblox DevForum](https://devforum.roblox.com/t/shadow-draw-calls-are-broken/4045934)
- « The other reason being that that would require another shadow map for the static parts which can then get copied to the shadow map for dynamic parts, which would then be re-rendering only the dynamic parts. » — [Roblox DevForum](https://devforum.roblox.com/t/shadow-draw-calls-are-broken/4045934)

## Extraits justificatifs

> « Recently, during the summer, I asked a colleague to create a post regarding severe FPS drops in games caused by an excessive number of “Draw Shadow Calls.” This forces the engine to calculate massive amounts of data on seemingly non-complex locations, especially when compared to modern-day games. »
> — [Roblox DevForum](https://devforum.roblox.com/t/shadow-draw-calls-are-broken/4045934), consulté le 2026-11-25

> « Additionally, a strangely high percentage of “Schedule Render” has appeared, reaching up to 90% (in my case, it consumes almost 50 FPS from the total). »
> — [Roblox DevForum](https://devforum.roblox.com/t/shadow-draw-calls-are-broken/4045934), consulté le 2026-11-25

> « Add approximately 16 or more PointLight objects (with Shadows.Enabled = true) and 50 or more assets (e.g., PBR meshes, shelves, barrels, or other complex geometry). »
> — [Roblox DevForum](https://devforum.roblox.com/t/shadow-draw-calls-are-broken/4045934), consulté le 2026-11-25

> « I expect that when an object moves under light sources, it should only force those specific lights to recalculate their shadows, rather than causing a near-global recalculation of the entire shadow map. »
> — [Roblox DevForum](https://devforum.roblox.com/t/shadow-draw-calls-are-broken/4045934), consulté le 2026-11-25

> « Since this disables shadows from the sun, which by and far use most draw calls due to cascaded shadowmap. »
> — [Roblox DevForum](https://devforum.roblox.com/t/shadow-draw-calls-are-broken/4045934), consulté le 2026-11-25

> « The other reason being that that would require another shadow map for the static parts which can then get copied to the shadow map for dynamic parts, which would then be re-rendering only the dynamic parts. »
> — [Roblox DevForum](https://devforum.roblox.com/t/shadow-draw-calls-are-broken/4045934), consulté le 2026-11-25


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

- Pertinence sujet : 0.583 · Contenu technique : 1.0 · Lien Roblox : oui
- Termes techniques repérés : triangles, shadow, shadows, lighting, performance, render, rendering, draw call
