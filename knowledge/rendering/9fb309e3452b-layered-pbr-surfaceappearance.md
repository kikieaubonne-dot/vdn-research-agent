---
id: "vdn-9fb309e3452b"
title: "Layered PBR SurfaceAppearance"
domain: "rendering"
subdomain: "rendering"
status: "documente"
tested_in_studio: "non"
confidence: "faible"
confidence_reason: "8 passages techniques dont 4 avec action et objet identifiables, source de niveau 2 ; indice technique seulement, procédure complète non garantie ; aucun test dans Roblox Studio."
engine_version: "inconnue"
source_tier: 2
provider: "devforum"
official: false
sources:
  - "https://devforum.roblox.com/t/4501956"
accessed: "2026-11-26"
queries:
  - "SurfaceAppearance PBR textures"
created: "2026-11-26"
updated: "2026-11-26"
tags:
  - "vdn"
  - "rendering"
  - "rendering"
  - "documente"
staff_posts: 0
accepted_answer: false
last_posted: "2026-03-21"
---

# Layered PBR SurfaceAppearance

> **Documenté** · source [Roblox DevForum](https://devforum.roblox.com/t/layered-pbr-surfaceappearance/4501956) · consultée le 2026-11-26 · **non testée dans Roblox Studio**

## Objectif

Répondre à : *SurfaceAppearance PBR textures* (sujet : Rendu PBR et maillages).

## Description technique

À rédiger à partir des extraits ci-dessous (analyse humaine ou Ollama). Rien n'est affirmé ici sans source.

## Étapes reproductibles

Instructions extraites automatiquement : procedure partielle, ordre et fonctionnement non verifies.

1. You may currently only apply one set of PBR textures to a mesh. -- [Roblox DevForum](https://devforum.roblox.com/t/layered-pbr-surfaceappearance/4501956)
2. Layered PBR textures will allow us to create dirt / mud effects for the dinosaur when muddy/dirty. -- [Roblox DevForum](https://devforum.roblox.com/t/layered-pbr-surfaceappearance/4501956)
3. Layered PBR textures will allow us to create wounded / bloody looks to our dinosaurs when low HP. -- [Roblox DevForum](https://devforum.roblox.com/t/layered-pbr-surfaceappearance/4501956)
4. Simply just implement a ZIndex property for SurfaceAppearance, so that we can apply multiple to one mesh. -- [Roblox DevForum](https://devforum.roblox.com/t/layered-pbr-surfaceappearance/4501956)

## Paramètres (sourcés)

Aucun paramètre chiffré trouvé dans les extraits.

## Limites connues de Roblox

- « You may currently only apply one set of PBR textures to a mesh. » — [Roblox DevForum](https://devforum.roblox.com/t/layered-pbr-surfaceappearance/4501956)
- « So we need a universal solution, to limit us from having to spend 7 years making effect-textures for each scenario built-into each texture, haha. » — [Roblox DevForum](https://devforum.roblox.com/t/layered-pbr-surfaceappearance/4501956)

## Extraits justificatifs

> « You may currently only apply one set of PBR textures to a mesh. »
> — [Roblox DevForum](https://devforum.roblox.com/t/layered-pbr-surfaceappearance/4501956), consulté le 2026-11-26

> « This is why we first need LAYERED PBR support & later DECAL PROJECTION support within the Roblox engine. »
> — [Roblox DevForum](https://devforum.roblox.com/t/layered-pbr-surfaceappearance/4501956), consulté le 2026-11-26

> « Layered PBR textures will allow us to create dirt / mud effects for the dinosaur when muddy/dirty. »
> — [Roblox DevForum](https://devforum.roblox.com/t/layered-pbr-surfaceappearance/4501956), consulté le 2026-11-26

> « Layered PBR textures will allow us to create wounded / bloody looks to our dinosaurs when low HP. »
> — [Roblox DevForum](https://devforum.roblox.com/t/layered-pbr-surfaceappearance/4501956), consulté le 2026-11-26

> « Simply just implement a ZIndex property for SurfaceAppearance, so that we can apply multiple to one mesh. »
> — [Roblox DevForum](https://devforum.roblox.com/t/layered-pbr-surfaceappearance/4501956), consulté le 2026-11-26

> « I’m no technical expert, so I have no easy solution for the implementation of Decal Projection. »
> — [Roblox DevForum](https://devforum.roblox.com/t/layered-pbr-surfaceappearance/4501956), consulté le 2026-11-26

> « We need a dynamic solution for it, that simply just allows us to stack the SurfaceAppearance using the Transparency-filter. »
> — [Roblox DevForum](https://devforum.roblox.com/t/layered-pbr-surfaceappearance/4501956), consulté le 2026-11-26

> « So we need a universal solution, to limit us from having to spend 7 years making effect-textures for each scenario built-into each texture, haha. »
> — [Roblox DevForum](https://devforum.roblox.com/t/layered-pbr-surfaceappearance/4501956), consulté le 2026-11-26


## Problèmes connus

À compléter.

## Alternatives

À compléter.

## Tests dans Roblox Studio

- Testé : **non**
- Conditions : —
- Résultat : —

## Questions ouvertes

- Quels réglages exacts (valeurs, propriétés) pour « SurfaceAppearance PBR textures » ?
- Le résultat tient-il de nuit, à la lampe torche, sur mobile ?

## Scores (diagnostic, pas une preuve)

- Pertinence sujet : 0.8 · Contenu technique : 1.0 · Lien Roblox : oui
- Termes techniques repérés : surfaceappearance, uv, transparency, texture, textures, decal
