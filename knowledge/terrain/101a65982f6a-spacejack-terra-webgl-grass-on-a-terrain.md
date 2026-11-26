---
id: "vdn-101a65982f6a"
title: "spacejack/terra — WebGL grass on a terrain"
domain: "terrain"
subdomain: "terrain"
status: "candidat"
tested_in_studio: "non"
confidence: "faible"
confidence_reason: "7 passage(s) technique(s), 3 instruction(s) explicite(s) repérée(s), source de niveau 3 ; procédure à approfondir et à tester."
engine_version: "inconnue"
source_tier: 3
provider: "github"
official: false
sources:
  - "https://github.com/spacejack/terra"
accessed: "2026-11-26"
queries:
  - "terrain decoration grass"
created: "2026-11-26"
updated: "2026-11-26"
tags:
  - "vdn"
  - "terrain"
  - "terrain"
  - "candidat"
stars: 524
pushed: "2023-02-20"
license: "NOASSERTION"
---

# spacejack/terra — WebGL grass on a terrain

> **Candidat** · source [GitHub](https://github.com/spacejack/terra) · consultée le 2026-11-26 · **non testée dans Roblox Studio**

## Objectif

Répondre à : *terrain decoration grass* (sujet : Terrain réaliste).

## Description technique

À rédiger à partir des extraits ci-dessous (analyse humaine ou Ollama). Rien n'est affirmé ici sans source.

## Étapes reproductibles

Instructions extraites automatiquement : procedure partielle, ordre et fonctionnement non verifies.

1. The terrain geometry can be a flat grid mesh that moves with the camera, using height values from the texture to set the height component of each vertex. -- [GitHub](https://github.com/spacejack/terra)
2. Determining which texture type to use is pretty simple here - if the elevation of the current position is above or below a certain point (just above water level.) -- [GitHub](https://github.com/spacejack/terra)
3. Earlier I had planned to create a channel for wind, however found that the lighting channel worked really well instead. -- [GitHub](https://github.com/spacejack/terra)

## Paramètres (sourcés)

- « ![terrain transition](screenshots/terrain-transition.jpg?raw=true) » — [GitHub](https://github.com/spacejack/terra)

## Limites connues de Roblox

- « Since we're dealing with static sunlight only, we can pre-compute all of the lighting. » — [GitHub](https://github.com/spacejack/terra)
- « This skydome implementation only renders the top half of a sphere and uses just one panoramic skydome texture mapped on to that sphere. » — [GitHub](https://github.com/spacejack/terra)

## Extraits justificatifs

> « The terrain geometry can be a flat grid mesh that moves with the camera, using height values from the texture to set the height component of each vertex. »
> — [GitHub](https://github.com/spacejack/terra), consulté le 2026-11-26

> « Similarly when rendering grass blades, that same height data can be sampled to adjust the elevation of each blade. »
> — [GitHub](https://github.com/spacejack/terra), consulté le 2026-11-26

> « Since we're dealing with static sunlight only, we can pre-compute all of the lighting. »
> — [GitHub](https://github.com/spacejack/terra), consulté le 2026-11-26

> « Determining which texture type to use is pretty simple here - if the elevation of the current position is above or below a certain point (just above water level.) »
> — [GitHub](https://github.com/spacejack/terra), consulté le 2026-11-26

> « Earlier I had planned to create a channel for wind, however found that the lighting channel worked really well instead. »
> — [GitHub](https://github.com/spacejack/terra), consulté le 2026-11-26

> « ![terrain transition](screenshots/terrain-transition.jpg?raw=true) »
> — [GitHub](https://github.com/spacejack/terra), consulté le 2026-11-26

> « This skydome implementation only renders the top half of a sphere and uses just one panoramic skydome texture mapped on to that sphere. »
> — [GitHub](https://github.com/spacejack/terra), consulté le 2026-11-26


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

- Pertinence sujet : 0.833 · Contenu technique : 1.0 · Lien Roblox : oui
- Termes techniques repérés : vertex, shadow, shadows, lighting, texture, textures, render, rendering, animation, terrain, resolution
