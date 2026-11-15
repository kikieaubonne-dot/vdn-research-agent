---
id: "vdn-6055d2f0bb67"
title: "Atmospheric effects"
domain: "forest"
subdomain: "forest"
status: "documente"
tested_in_studio: "non"
confidence: "moyenne"
confidence_reason: "8 passages techniques dont 1 avec action et objet identifiables, source de niveau 1 (réponse du personnel Roblox / doc officielle) ; indice technique seulement, procédure complète non garantie ; aucun test dans Roblox Studio."
engine_version: "inconnue"
source_tier: 1
provider: "roblox_docs"
official: true
sources:
  - "https://create.roblox.com/docs/environment/atmosphere"
accessed: "2026-11-15"
queries:
  - "forest atmosphere fog"
created: "2026-11-15"
updated: "2026-11-15"
tags:
  - "vdn"
  - "forest"
  - "forest"
  - "documente"
---

# Atmospheric effects

> **Documenté** · source [Documentation Roblox](https://create.roblox.com/docs/en-us/environment/atmosphere.md) · consultée le 2026-11-15 · **non testée dans Roblox Studio**

## Objectif

Répondre à : *forest atmosphere fog* (sujet : Forêt nocturne enneigée).

## Description technique

À rédiger à partir des extraits ci-dessous (analyse humaine ou Ollama). Rien n'est affirmé ici sans source.

## Étapes reproductibles

Instructions extraites automatiquement : procedure partielle, ordre et fonctionnement non verifies.

1. The `Class.Atmosphere.Haze|Haze` property controls the haziness of the atmosphere to create a visible effect both above the horizon and far into the distance from the camera. -- [Documentation Roblox](https://create.roblox.com/docs/en-us/environment/atmosphere.md)

## Paramètres (sourcés)

- « The `Class.Atmosphere.Density|Density` property controls how many particles exist in the air of your game; the higher the density, the more particles, which obstruct a player's view of objects and terrain. » — [Documentation Roblox](https://create.roblox.com/docs/en-us/environment/atmosphere.md)
- « > **Info:** Density only **directly** affects objects and terrain; however, since you view a [skybox](/docs/en-us/environment/skybox.md) through those objects and terrain, the visibility of a skybox is also affected. » — [Documentation Roblox](https://create.roblox.com/docs/en-us/environment/atmosphere.md)
- « > **Warning:** Carefully balance the `Class.Atmosphere.Offset|Offset` property with the `Class.Atmosphere.Density|Density` property. » — [Documentation Roblox](https://create.roblox.com/docs/en-us/environment/atmosphere.md)
- « The `Class.Atmosphere.Haze|Haze` property controls the haziness of the atmosphere to create a visible effect both above the horizon and far into the distance from the camera. » — [Documentation Roblox](https://create.roblox.com/docs/en-us/environment/atmosphere.md)
- « The `Class.Atmosphere.Glare|Glare` property sets an atmospheric glare around the sun. » — [Documentation Roblox](https://create.roblox.com/docs/en-us/environment/atmosphere.md)

## Limites connues de Roblox

- « > **Info:** Density only **directly** affects objects and terrain; however, since you view a [skybox](/docs/en-us/environment/skybox.md) through those objects and terrain, the visibility of a skybox is also affected. » — [Documentation Roblox](https://create.roblox.com/docs/en-us/environment/atmosphere.md)

## Extraits justificatifs

> « Every property of the `Class.Atmosphere` object inside the `Class.Lighting` service works together to support the overall vision, themes, and mood of your game. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/environment/atmosphere.md), consulté le 2026-11-15

> « The `Class.Atmosphere.Density|Density` property controls how many particles exist in the air of your game; the higher the density, the more particles, which obstruct a player's view of objects and terrain. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/environment/atmosphere.md), consulté le 2026-11-15

> « > **Info:** Density only **directly** affects objects and terrain; however, since you view a [skybox](/docs/en-us/environment/skybox.md) through those objects and terrain, the visibility of a skybox is also affected. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/environment/atmosphere.md), consulté le 2026-11-15

> « The `Class.Atmosphere.Offset|Offset` property controls how light transmits between the camera and the sky background. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/environment/atmosphere.md), consulté le 2026-11-15

> « > **Warning:** Carefully balance the `Class.Atmosphere.Offset|Offset` property with the `Class.Atmosphere.Density|Density` property. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/environment/atmosphere.md), consulté le 2026-11-15

> « The `Class.Atmosphere.Haze|Haze` property controls the haziness of the atmosphere to create a visible effect both above the horizon and far into the distance from the camera. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/environment/atmosphere.md), consulté le 2026-11-15

> « The `Class.Atmosphere.Color|Color` property sets the hue of the atmosphere for subtle environmental moods and themes. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/environment/atmosphere.md), consulté le 2026-11-15

> « The `Class.Atmosphere.Glare|Glare` property sets an atmospheric glare around the sun. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/environment/atmosphere.md), consulté le 2026-11-15


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

- Pertinence sujet : 0.542 · Contenu technique : 1.0 · Lien Roblox : oui
- Termes techniques repérés : lighting, render, atmosphere, density, terrain
