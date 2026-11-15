---
id: "vdn-0c907f49b2f4"
title: "Light sources"
domain: "lighting"
subdomain: "lighting"
status: "documente"
tested_in_studio: "non"
confidence: "moyenne"
confidence_reason: "8 passages techniques dont 4 avec action et objet identifiables, source de niveau 1 (réponse du personnel Roblox / doc officielle) ; indice technique seulement, procédure complète non garantie ; aucun test dans Roblox Studio."
engine_version: "inconnue"
source_tier: 1
provider: "roblox_docs"
official: true
sources:
  - "https://create.roblox.com/docs/effects/light-sources"
accessed: "2026-11-15"
queries:
  - "light shadows performance"
created: "2026-11-15"
updated: "2026-11-15"
tags:
  - "vdn"
  - "lighting"
  - "lighting"
  - "documente"
---

# Light sources

> **Documenté** · source [Documentation Roblox](https://create.roblox.com/docs/en-us/effects/light-sources.md) · consultée le 2026-11-15 · **non testée dans Roblox Studio**

## Objectif

Répondre à : *light shadows performance* (sujet : Éclairage de nuit et lampe torche).

## Description technique

À rédiger à partir des extraits ci-dessous (analyse humaine ou Ollama). Rien n'est affirmé ici sans source.

## Étapes reproductibles

À extraire de la source ; non disponibles automatiquement. Les indices d’action ci-dessous ne constituent pas un tutoriel complet.

## Paramètres (sourcés)

- « Then adjust the object's `Class.PointLight.Range|Range` as well as [shared properties](#shared-properties) like `Class.PointLight.Brightness|Brightness` and `Class.PointLight.Color|Color`. » — [Documentation Roblox](https://create.roblox.com/docs/en-us/effects/light-sources.md)
- « Then adjust the `Class.SpotLight.Angle|Angle` and `Class.SpotLight.Range|Range`, as well as [shared properties](#shared-properties) like `Class.SpotLight.Brightness|Brightness` and `Class.SpotLight.Color|Color`. » — [Documentation Roblox](https://create.roblox.com/docs/en-us/effects/light-sources.md)
- « Then adjust the `Class.SurfaceLight.Angle|Angle` and `Class.SurfaceLight.Range|Range`, as well as [shared properties](#shared-properties) like `Class.SurfaceLight.Brightness|Brightness` and `Class.SurfaceLight.Color|Color`. » — [Documentation Roblox](https://create.roblox.com/docs/en-us/effects/light-sources.md)

## Limites connues de Roblox

- « > **Info:** The `Class.Lighting.LightingStyle|LightingStyle` property, modifiable only in the [Properties](/docs/en-us/studio/properties.md) window for the global `Class.Lighting` object, sets your game's lighting style. » — [Documentation Roblox](https://create.roblox.com/docs/en-us/effects/light-sources.md)

## Indices de procédure (non vérifiés)

- « By using the different types of light sources instead of just general global lighting through the `Class.Lighting` service, you can create immersive environments such as cyberpunk cities, traditional light festivals, and moody detective scenes. » — [Documentation Roblox](https://create.roblox.com/docs/en-us/effects/light-sources.md)
- « Then adjust the object's `Class.PointLight.Range|Range` as well as [shared properties](#shared-properties) like `Class.PointLight.Brightness|Brightness` and `Class.PointLight.Color|Color`. » — [Documentation Roblox](https://create.roblox.com/docs/en-us/effects/light-sources.md)
- « Then adjust the `Class.SpotLight.Angle|Angle` and `Class.SpotLight.Range|Range`, as well as [shared properties](#shared-properties) like `Class.SpotLight.Brightness|Brightness` and `Class.SpotLight.Color|Color`. » — [Documentation Roblox](https://create.roblox.com/docs/en-us/effects/light-sources.md)
- « Then adjust the `Class.SurfaceLight.Angle|Angle` and `Class.SurfaceLight.Range|Range`, as well as [shared properties](#shared-properties) like `Class.SurfaceLight.Brightness|Brightness` and `Class.SurfaceLight.Color|Color`. » — [Documentation Roblox](https://create.roblox.com/docs/en-us/effects/light-sources.md)

## Extraits justificatifs

> « By using the different types of light sources instead of just general global lighting through the `Class.Lighting` service, you can create immersive environments such as cyberpunk cities, traditional light festivals, and moody detective scenes. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/effects/light-sources.md), consulté le 2026-11-15

> « > **Info:** The `Class.Lighting.LightingStyle|LightingStyle` property, modifiable only in the [Properties](/docs/en-us/studio/properties.md) window for the global `Class.Lighting` object, sets your game's lighting style. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/effects/light-sources.md), consulté le 2026-11-15

> « Then adjust the object's `Class.PointLight.Range|Range` as well as [shared properties](#shared-properties) like `Class.PointLight.Brightness|Brightness` and `Class.PointLight.Color|Color`. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/effects/light-sources.md), consulté le 2026-11-15

> « Then adjust the `Class.SpotLight.Angle|Angle` and `Class.SpotLight.Range|Range`, as well as [shared properties](#shared-properties) like `Class.SpotLight.Brightness|Brightness` and `Class.SpotLight.Color|Color`. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/effects/light-sources.md), consulté le 2026-11-15

> « ![A street lamp spotlight with a 30 degree angle of emission.](../assets/lighting-and-effects/light-sources/SpotLight-Angle-30.jpg) »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/effects/light-sources.md), consulté le 2026-11-15

> « ![The same street lamp spotlight with a 75 degree angle of emission.](../assets/lighting-and-effects/light-sources/SpotLight-Angle-75.jpg) »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/effects/light-sources.md), consulté le 2026-11-15

> « Then adjust the `Class.SurfaceLight.Angle|Angle` and `Class.SurfaceLight.Range|Range`, as well as [shared properties](#shared-properties) like `Class.SurfaceLight.Brightness|Brightness` and `Class.SurfaceLight.Color|Color`. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/effects/light-sources.md), consulté le 2026-11-15

> « ![A sign surface light with a 0 degree angle of emission.](../assets/lighting-and-effects/light-sources/SurfaceLight-Angle-0.jpg) »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/effects/light-sources.md), consulté le 2026-11-15


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
- Termes techniques repérés : shadows, lighting, brightness
