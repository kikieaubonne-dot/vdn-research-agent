---
id: "vdn-a96e07091a68"
title: "Global lighting"
domain: "lighting"
subdomain: "lighting"
status: "documente"
tested_in_studio: "non"
confidence: "moyenne"
confidence_reason: "8 passages techniques dont 2 avec action et objet identifiables, source de niveau 1 (réponse du personnel Roblox / doc officielle) ; indice technique seulement, procédure complète non garantie ; aucun test dans Roblox Studio."
engine_version: "inconnue"
source_tier: 1
provider: "roblox_docs"
official: true
sources:
  - "https://create.roblox.com/docs/environment/lighting"
accessed: "2026-11-20"
queries:
  - "light shadows performance settings"
created: "2026-11-20"
updated: "2026-11-20"
tags:
  - "vdn"
  - "lighting"
  - "lighting"
  - "documente"
---

# Global lighting

> **Documenté** · source [Documentation Roblox](https://create.roblox.com/docs/en-us/environment/lighting.md) · consultée le 2026-11-20 · **non testée dans Roblox Studio**

## Objectif

Répondre à : *light shadows performance settings* (sujet : Éclairage de nuit et lampe torche).

## Description technique

À rédiger à partir des extraits ci-dessous (analyse humaine ou Ollama). Rien n'est affirmé ici sans source.

## Étapes reproductibles

Instructions extraites automatiquement : procedure partielle, ordre et fonctionnement non verifies.

1. The `Class.Lighting` service contains properties that you can adjust to update and customize the global lighting in a game. -- [Documentation Roblox](https://create.roblox.com/docs/en-us/environment/lighting.md)
2. In the following images, note that the lighting inside the garage and cafe doesn't change like it would if you were changing the [Ambient](#ambient) property. -- [Documentation Roblox](https://create.roblox.com/docs/en-us/environment/lighting.md)

## Paramètres (sourcés)

Aucun paramètre chiffré trouvé dans les extraits.

## Limites connues de Roblox

- « In the following images, note that the lighting inside the garage and cafe doesn't change like it would if you were changing the [Ambient](#ambient) property. » — [Documentation Roblox](https://create.roblox.com/docs/en-us/environment/lighting.md)

## Extraits justificatifs

> « The `Class.Lighting` service contains properties that you can adjust to update and customize the global lighting in a game. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/environment/lighting.md), consulté le 2026-11-20

> « The `Class.Lighting.Ambient|Ambient` property sets a hue for the **entirety** of a game. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/environment/lighting.md), consulté le 2026-11-20

> « This property affects the lighting for both outdoor and indoor environments. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/environment/lighting.md), consulté le 2026-11-20

> « ![Lighting.Ambient property of [0, 0, 0]](../assets/lighting-and-effects/lighting-properties/Ambient-0-0-0.jpg) »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/environment/lighting.md), consulté le 2026-11-20

> « ![Lighting.Ambient property of [160, 80, 0]](../assets/lighting-and-effects/lighting-properties/Ambient-160-80-0.jpg) »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/environment/lighting.md), consulté le 2026-11-20

> « ![Lighting.Ambient property of [25, 0, 125]](../assets/lighting-and-effects/lighting-properties/Ambient-25-0-125.jpg) »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/environment/lighting.md), consulté le 2026-11-20

> « The `Class.Lighting.OutdoorAmbient|OutdoorAmbient` property sets a hue for **outdoor areas** of a game. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/environment/lighting.md), consulté le 2026-11-20

> « In the following images, note that the lighting inside the garage and cafe doesn't change like it would if you were changing the [Ambient](#ambient) property. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/environment/lighting.md), consulté le 2026-11-20


## Problèmes connus

À compléter.

## Alternatives

À compléter.

## Tests dans Roblox Studio

- Testé : **non**
- Conditions : —
- Résultat : —

## Questions ouvertes

- Quels réglages exacts (valeurs, propriétés) pour « light shadows performance settings » ?
- Le résultat tient-il de nuit, à la lampe torche, sur mobile ?

## Scores (diagnostic, pas une preuve)

- Pertinence sujet : 0.5 · Contenu technique : 1.0 · Lien Roblox : oui
- Termes techniques repérés : shadows, lighting, rendering, brightness, exposure
