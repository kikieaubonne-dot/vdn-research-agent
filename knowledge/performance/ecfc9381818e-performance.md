---
id: "vdn-ecfc9381818e"
title: "Performance"
domain: "performance"
subdomain: "performance"
status: "candidat"
tested_in_studio: "non"
confidence: "faible"
confidence_reason: "3 passage(s) technique(s), 0 instruction(s) explicite(s) repérée(s), source de niveau 1 ; procédure à approfondir et à tester."
engine_version: "inconnue"
source_tier: 1
provider: "roblox_docs"
official: true
sources:
  - "https://create.roblox.com/docs/production/analytics/performance"
accessed: "2026-11-15"
queries:
  - "MicroProfiler rendering"
created: "2026-11-15"
updated: "2026-11-15"
tags:
  - "vdn"
  - "performance"
  - "performance"
  - "candidat"
---

# Performance

> **Candidat** · source [Documentation Roblox](https://create.roblox.com/docs/en-us/production/analytics/performance.md) · consultée le 2026-11-15 · **non testée dans Roblox Studio**

## Objectif

Répondre à : *MicroProfiler rendering* (sujet : Performances et niveaux de détail).

## Description technique

À rédiger à partir des extraits ci-dessous (analyse humaine ou Ollama). Rien n'est affirmé ici sans source.

## Étapes reproductibles

À extraire de la source ; non disponibles automatiquement. Les indices d’action ci-dessous ne constituent pas un tutoriel complet.

## Paramètres (sourcés)

Aucun paramètre chiffré trouvé dans les extraits.

## Limites connues de Roblox

- « This image shows how you might use the Developer Console to investigate an issue with **PlaceMemory:GraphicsTexture** that you see in the dashboard:![The Developer Console showing the server memory view.](../../assets/analytics/performance/perf-dash-dev.png) » — [Documentation Roblox](https://create.roblox.com/docs/en-us/production/analytics/performance.md)

## Indices de procédure (non vérifiés)

Aucune instruction explicite identifiée dans les extraits. Ne pas présenter cette fiche comme un tutoriel.

## Extraits justificatifs

> « To access the performance dashboard, you must either be the game owner or have [analytics group permissions](/docs/en-us/production/analytics/analytics-dashboard.md#grant-group-permission). »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/production/analytics/performance.md), consulté le 2026-11-15

> « - CPU categories and tasks map to the ones in the [MicroProfiler](/docs/en-us/performance-optimization/microprofiler.md), so you can take [server dumps](/docs/en-us/performance-optimization/microprofiler.md#profile-the-server), select **Timers** mode, and then use the **Groups** menu to filter by the problematic process group. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/production/analytics/performance.md), consulté le 2026-11-15

> « This image shows how you might use the Developer Console to investigate an issue with **PlaceMemory:GraphicsTexture** that you see in the dashboard:![The Developer Console showing the server memory view.](../../assets/analytics/performance/perf-dash-dev.png) »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/production/analytics/performance.md), consulté le 2026-11-15


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
