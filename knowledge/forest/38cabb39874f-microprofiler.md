---
id: "vdn-38cabb39874f"
title: "MicroProfiler"
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
  - "https://create.roblox.com/docs/performance-optimization/microprofiler"
accessed: "2026-11-16"
queries:
  - "large forest performance"
created: "2026-11-16"
updated: "2026-11-16"
tags:
  - "vdn"
  - "forest"
  - "forest"
  - "documente"
---

# MicroProfiler

> **Documenté** · source [Documentation Roblox](https://create.roblox.com/docs/en-us/performance-optimization/microprofiler.md) · consultée le 2026-11-16 · **non testée dans Roblox Studio**

## Objectif

Répondre à : *large forest performance* (sujet : Forêt nocturne enneigée).

## Description technique

À rédiger à partir des extraits ci-dessous (analyse humaine ou Ollama). Rien n'est affirmé ici sans source.

## Étapes reproductibles

Instructions extraites automatiquement : procedure partielle, ordre et fonctionnement non verifies.

1. To use the MicroProfiler, you must understand the relationship between **frame time** and **frame rate**. -- [Documentation Roblox](https://create.roblox.com/docs/en-us/performance-optimization/microprofiler.md)

## Paramètres (sourcés)

Aucun paramètre chiffré trouvé dans les extraits.

## Limites connues de Roblox

- « Most players on Roblox use phones and tablets, and these devices have severe thermal and power constraints that limit their performance. » — [Documentation Roblox](https://create.roblox.com/docs/en-us/performance-optimization/microprofiler.md)
- « For example, you might only want to see **Render** tasks in the main thread.![The on-hover view for a label, with Group highlighted.](../../assets/optimization/microprofiler/micro-group.png) » — [Documentation Roblox](https://create.roblox.com/docs/en-us/performance-optimization/microprofiler.md)
- « Reproduce the issue, use MicroProfiler to find the cause, fix it, and retest." » — [Documentation Roblox](https://create.roblox.com/docs/en-us/performance-optimization/microprofiler.md)

## Extraits justificatifs

> « To use the MicroProfiler, you must understand the relationship between **frame time** and **frame rate**. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/performance-optimization/microprofiler.md), consulté le 2026-11-16

> « - On the mobile client, open the **Settings** menu and change the MicroProfiler to **On**. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/performance-optimization/microprofiler.md), consulté le 2026-11-16

> « Then from a development machine **on the same network**, use your web browser to navigate to the provided IP address and port.![The MicroProfiler UI on mobile.](../../assets/optimization/microprofiler/micro-mobile.png) This screenshot shows an IP address of `172.18.56.105` and a port of `1338`, so you navigate to `172.18.56.105:1338`. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/performance-optimization/microprofiler.md), consulté le 2026-11-16

> « Most players on Roblox use phones and tablets, and these devices have severe thermal and power constraints that limit their performance. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/performance-optimization/microprofiler.md), consulté le 2026-11-16

> « A typical workflow in the MicroProfiler is to use the frame time graph to identify a spike (a taller bar) and then use the timeline to identify which tasks caused the spike. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/performance-optimization/microprofiler.md), consulté le 2026-11-16

> « For example, you might only want to see **Render** tasks in the main thread.![The on-hover view for a label, with Group highlighted.](../../assets/optimization/microprofiler/micro-group.png) »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/performance-optimization/microprofiler.md), consulté le 2026-11-16

> « Wrap code with `Library.debug.profilebegin()` and `Library.debug.profileend()` to time everything done between those function calls and create a label on the MicroProfiler timeline. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/performance-optimization/microprofiler.md), consulté le 2026-11-16

> « Reproduce the issue, use MicroProfiler to find the cause, fix it, and retest." »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/performance-optimization/microprofiler.md), consulté le 2026-11-16


## Problèmes connus

À compléter.

## Alternatives

À compléter.

## Tests dans Roblox Studio

- Testé : **non**
- Conditions : —
- Résultat : —

## Questions ouvertes

- Quels réglages exacts (valeurs, propriétés) pour « large forest performance » ?
- Le résultat tient-il de nuit, à la lampe torche, sur mobile ?

## Scores (diagnostic, pas une preuve)

- Pertinence sujet : 0.633 · Contenu technique : 1.0 · Lien Roblox : oui
- Termes techniques repérés : triangle, lighting, texture, performance, render, rendering, export, density, microprofiler
