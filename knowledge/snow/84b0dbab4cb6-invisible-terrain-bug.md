---
id: "vdn-84b0dbab4cb6"
title: "Invisible terrain bug"
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
  - "https://devforum.roblox.com/t/1268524"
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
accepted_answer: false
last_posted: "2022-04-19"
---

# Invisible terrain bug

> **Candidat** · source [Roblox DevForum](https://devforum.roblox.com/t/invisible-terrain-bug/1268524) · consultée le 2026-11-16 · **non testée dans Roblox Studio**

## Objectif

Répondre à : *snow terrain material* (sujet : Neige, givre et traces).

## Description technique

À rédiger à partir des extraits ci-dessous (analyse humaine ou Ollama). Rien n'est affirmé ici sans source.

## Étapes reproductibles

Instructions extraites automatiquement : procedure partielle, ordre et fonctionnement non verifies.

Aucune instruction complete identifiee. Ne pas présenter cette fiche comme un tutoriel. Consulter la source.

## Paramètres (sourcés)

- « What is actually going on is that there is a single voxel that has a very low value, in a material that has a weird shape, which makes this voxel invisible (it renders as a box sized 0 studs) when up close, but it still shows something at further distances because of how the LODs work in the current terrain system. » — [Roblox DevForum](https://devforum.roblox.com/t/invisible-terrain-bug/1268524)
- « local materials, occupancies = game.Workspace.Terrain:ReadVoxels(Region3.new(Vector3.new(x,y,z), Vector3.new(x+step, y+step, z+step)), 4) » — [Roblox DevForum](https://devforum.roblox.com/t/invisible-terrain-bug/1268524)

## Limites connues de Roblox

Aucune limite explicite trouvée dans les extraits.

## Extraits justificatifs

> « What is actually going on is that there is a single voxel that has a very low value, in a material that has a weird shape, which makes this voxel invisible (it renders as a box sized 0 studs) when up close, but it still shows something at further distances because of how the LODs work in the current terrain system. »
> — [Roblox DevForum](https://devforum.roblox.com/t/invisible-terrain-bug/1268524), consulté le 2026-11-16

> « local materials, occupancies = game.Workspace.Terrain:ReadVoxels(Region3.new(Vector3.new(x,y,z), Vector3.new(x+step, y+step, z+step)), 4) »
> — [Roblox DevForum](https://devforum.roblox.com/t/invisible-terrain-bug/1268524), consulté le 2026-11-16

> « -- materials[ix][iy][iz] = Enum.Material.Grass; »
> — [Roblox DevForum](https://devforum.roblox.com/t/invisible-terrain-bug/1268524), consulté le 2026-11-16

> « -- game.Workspace.Terrain:WriteVoxels(Region3.new(Vector3.new(x,y,z), Vector3.new(x+step, y+step, z+step)), 4, materials, occupancies) »
> — [Roblox DevForum](https://devforum.roblox.com/t/invisible-terrain-bug/1268524), consulté le 2026-11-16


## Problèmes connus

À compléter.

## Alternatives

À compléter.

## Tests dans Roblox Studio

- Testé : **non**
- Conditions : —
- Résultat : —

## Questions ouvertes

- Quelles limites Roblox (performances, rendu à distance, appareils) pour « snow terrain material » ?
- Le résultat tient-il de nuit, à la lampe torche, sur mobile ?

## Scores (diagnostic, pas une preuve)

- Pertinence sujet : 0.5 · Contenu technique : 0.64 · Lien Roblox : oui
- Termes techniques repérés : material, rendering, terrain, 512
