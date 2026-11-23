---
id: "vdn-550a8df9794e"
title: "Unity-Technologies/VolumetricLighting — Lighting effects implemented for the Adam demo: volumetric fog, area lights and tube lights"
domain: "lighting"
subdomain: "lighting"
status: "candidat"
tested_in_studio: "non"
confidence: "faible"
confidence_reason: "4 passage(s) technique(s), 0 instruction(s) explicite(s) repérée(s), source de niveau 3 ; procédure à approfondir et à tester."
engine_version: "inconnue"
source_tier: 3
provider: "github"
official: false
sources:
  - "https://github.com/unity-technologies/volumetriclighting"
accessed: "2026-11-23"
queries:
  - "Lighting limitations"
created: "2026-11-23"
updated: "2026-11-23"
tags:
  - "vdn"
  - "lighting"
  - "lighting"
  - "candidat"
stars: 1797
pushed: "2019-12-03"
license: "MIT"
---

# Unity-Technologies/VolumetricLighting — Lighting effects implemented for the Adam demo: volumetric fog, area lights and tube lights

> **Candidat** · source [GitHub](https://github.com/Unity-Technologies/VolumetricLighting) · consultée le 2026-11-23 · **non testée dans Roblox Studio**

## Objectif

Répondre à : *Lighting limitations* (sujet : Éclairage de nuit et lampe torche).

## Description technique

À rédiger à partir des extraits ci-dessous (analyse humaine ou Ollama). Rien n'est affirmé ici sans source.

## Étapes reproductibles

Instructions extraites automatiquement : procedure partielle, ordre et fonctionnement non verifies.

Aucune instruction complete identifiee. Ne pas présenter cette fiche comme un tutoriel. Consulter la source.

## Paramètres (sourcés)

Aucun paramètre chiffré trouvé dans les extraits.

## Limites connues de Roblox

- « - The lights only work in deferred rendering and won't affect any objects rendered in forward. » — [GitHub](https://github.com/Unity-Technologies/VolumetricLighting)
- « - The material emission of the light source mesh (the quad and the capsule) is only a rough approximation - needs to be calculated properly. » — [GitHub](https://github.com/Unity-Technologies/VolumetricLighting)
- « To fix aliasing, increase froxel resolution (controls coming, or decrease *Far Clip Max*), or make the features in the fog smoother (e.g. » — [GitHub](https://github.com/Unity-Technologies/VolumetricLighting)

## Extraits justificatifs

> « - Volumetric shadows in the fog use Variance Shadow Maps. »
> — [GitHub](https://github.com/Unity-Technologies/VolumetricLighting), consulté le 2026-11-23

> « - The lights only work in deferred rendering and won't affect any objects rendered in forward. »
> — [GitHub](https://github.com/Unity-Technologies/VolumetricLighting), consulté le 2026-11-23

> « - The material emission of the light source mesh (the quad and the capsule) is only a rough approximation - needs to be calculated properly. »
> — [GitHub](https://github.com/Unity-Technologies/VolumetricLighting), consulté le 2026-11-23

> « To fix aliasing, increase froxel resolution (controls coming, or decrease *Far Clip Max*), or make the features in the fog smoother (e.g. »
> — [GitHub](https://github.com/Unity-Technologies/VolumetricLighting), consulté le 2026-11-23


## Problèmes connus

À compléter.

## Alternatives

À compléter.

## Tests dans Roblox Studio

- Testé : **non**
- Conditions : —
- Résultat : —

## Questions ouvertes

- Quels réglages exacts (valeurs, propriétés) pour « Lighting limitations » ?
- Le résultat tient-il de nuit, à la lampe torche, sur mobile ?

## Scores (diagnostic, pas une preuve)

- Pertinence sujet : 0.833 · Contenu technique : 0.84 · Lien Roblox : oui
- Termes techniques repérés : transparency, shadow, shadows, lighting, material, render, rendering, density, resolution
