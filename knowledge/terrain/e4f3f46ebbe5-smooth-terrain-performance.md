---
id: "vdn-e4f3f46ebbe5"
title: "Smooth Terrain Performance"
domain: "terrain"
subdomain: "terrain"
status: "documente"
tested_in_studio: "non"
confidence: "faible"
confidence_reason: "3 passages techniques dont 3 avec action et objet identifiables, source de niveau 2 ; indice technique seulement, procédure complète non garantie ; aucun test dans Roblox Studio."
engine_version: "inconnue"
source_tier: 2
provider: "devforum"
official: false
sources:
  - "https://devforum.roblox.com/t/173087"
accessed: "2026-11-26"
queries:
  - "terrain texture realistic"
created: "2026-11-26"
updated: "2026-11-26"
tags:
  - "vdn"
  - "terrain"
  - "terrain"
  - "documente"
staff_posts: 0
accepted_answer: false
last_posted: "2018-09-06"
---

# Smooth Terrain Performance

> **Documenté** · source [Roblox DevForum](https://devforum.roblox.com/t/smooth-terrain-performance/173087) · consultée le 2026-11-26 · **non testée dans Roblox Studio**

## Objectif

Répondre à : *terrain texture realistic* (sujet : Terrain réaliste).

## Description technique

À rédiger à partir des extraits ci-dessous (analyse humaine ou Ollama). Rien n'est affirmé ici sans source.

## Étapes reproductibles

Instructions extraites automatiquement : procedure partielle, ordre et fonctionnement non verifies.

1. It should be fine but what i would advise is use the ‘Regions’ tool in the terrain editor and remove most of the bottom of the terain [See screenshot] to substantially decrease the voxels. -- [Roblox DevForum](https://devforum.roblox.com/t/smooth-terrain-performance/173087)
2. Also - use terrain to its fullest potential in terms of detail. -- [Roblox DevForum](https://devforum.roblox.com/t/smooth-terrain-performance/173087)
3. That video is basically useless now, instead if you navigate to the ‘TerrainToolsInLuaWidget.rbxmx’ file which is located under AppData>Local>Roblox>Versions>[LatestStudioVersion]>BuiltInPlugins (Provided you’re on windows), you can then add a new entry in the ‘kMapSizeChoices’ table to set a new terrain size. -- [Roblox DevForum](https://devforum.roblox.com/t/smooth-terrain-performance/173087)

## Paramètres (sourcés)

Aucun paramètre chiffré trouvé dans les extraits.

## Limites connues de Roblox

Aucune limite explicite trouvée dans les extraits.

## Extraits justificatifs

> « It should be fine but what i would advise is use the ‘Regions’ tool in the terrain editor and remove most of the bottom of the terain [See screenshot] to substantially decrease the voxels. »
> — [Roblox DevForum](https://devforum.roblox.com/t/smooth-terrain-performance/173087), consulté le 2026-11-26

> « Also - use terrain to its fullest potential in terms of detail. »
> — [Roblox DevForum](https://devforum.roblox.com/t/smooth-terrain-performance/173087), consulté le 2026-11-26

> « That video is basically useless now, instead if you navigate to the ‘TerrainToolsInLuaWidget.rbxmx’ file which is located under AppData>Local>Roblox>Versions>[LatestStudioVersion]>BuiltInPlugins (Provided you’re on windows), you can then add a new entry in the ‘kMapSizeChoices’ table to set a new terrain size. »
> — [Roblox DevForum](https://devforum.roblox.com/t/smooth-terrain-performance/173087), consulté le 2026-11-26


## Problèmes connus

À compléter.

## Alternatives

À compléter.

## Tests dans Roblox Studio

- Testé : **non**
- Conditions : —
- Résultat : —

## Questions ouvertes

- Quels réglages exacts (valeurs, propriétés) pour « terrain texture realistic » ?
- Quelles limites Roblox (performances, rendu à distance, appareils) pour « terrain texture realistic » ?
- Le résultat tient-il de nuit, à la lampe torche, sur mobile ?

## Scores (diagnostic, pas une preuve)

- Pertinence sujet : 0.5 · Contenu technique : 0.52 · Lien Roblox : oui
- Termes techniques repérés : lod, performance, terrain, 1024
