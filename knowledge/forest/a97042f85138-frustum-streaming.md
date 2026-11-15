---
id: "vdn-a97042f85138"
title: "Frustum Streaming"
domain: "forest"
subdomain: "forest"
status: "documente"
tested_in_studio: "non"
confidence: "moyenne"
confidence_reason: "6 passages techniques dont 5 avec action et objet identifiables, source de niveau 1 (réponse du personnel Roblox / doc officielle) ; indice technique seulement, procédure complète non garantie ; aucun test dans Roblox Studio."
engine_version: "inconnue"
source_tier: 1
provider: "roblox_docs"
official: true
sources:
  - "https://create.roblox.com/docs/workspace/streaming/frustum"
accessed: "2026-11-15"
queries:
  - "forest streaming trees"
created: "2026-11-15"
updated: "2026-11-15"
tags:
  - "vdn"
  - "forest"
  - "forest"
  - "documente"
---

# Frustum Streaming

> **Documenté** · source [Documentation Roblox](https://create.roblox.com/docs/en-us/workspace/streaming/frustum.md) · consultée le 2026-11-15 · **non testée dans Roblox Studio**

## Objectif

Répondre à : *forest streaming trees* (sujet : Forêt nocturne enneigée).

## Description technique

À rédiger à partir des extraits ci-dessous (analyse humaine ou Ollama). Rien n'est affirmé ici sans source.

## Étapes reproductibles

Instructions extraites automatiquement : procedure partielle, ordre et fonctionnement non verifies.

1. When you enable frustum streaming for a player, the server also streams instances within a frustum shape matching the player's camera view, extending well beyond the normal streaming radius. -- [Documentation Roblox](https://create.roblox.com/docs/en-us/workspace/streaming/frustum.md)
2. - **Frustum**: the camera-view pyramid, active only when frustum streaming is on for that player. -- [Documentation Roblox](https://create.roblox.com/docs/en-us/workspace/streaming/frustum.md)
3. Roblox might adjust this allocation in the future if games commonly use both frustum streaming and replication foci and the frustum needs higher priority. -- [Documentation Roblox](https://create.roblox.com/docs/en-us/workspace/streaming/frustum.md)
4. On devices with reduced graphics quality or low frame rates, the engine might disable frustum streaming automatically. -- [Documentation Roblox](https://create.roblox.com/docs/en-us/workspace/streaming/frustum.md)
5. - **Not applicable to non-streaming experiences**: if your experience does not use instance streaming, all instances are already present on the client and frustum streaming has no effect. -- [Documentation Roblox](https://create.roblox.com/docs/en-us/workspace/streaming/frustum.md)

## Paramètres (sourcés)

Aucun paramètre chiffré trouvé dans les extraits.

## Limites connues de Roblox

- « - **Frustum**: the camera-view pyramid, active only when frustum streaming is on for that player. » — [Documentation Roblox](https://create.roblox.com/docs/en-us/workspace/streaming/frustum.md)
- « - **Not applicable to non-streaming experiences**: if your experience does not use instance streaming, all instances are already present on the client and frustum streaming has no effect. » — [Documentation Roblox](https://create.roblox.com/docs/en-us/workspace/streaming/frustum.md)

## Extraits justificatifs

> « When you enable frustum streaming for a player, the server also streams instances within a frustum shape matching the player's camera view, extending well beyond the normal streaming radius. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/workspace/streaming/frustum.md), consulté le 2026-11-15

> « - **Frustum**: the camera-view pyramid, active only when frustum streaming is on for that player. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/workspace/streaming/frustum.md), consulté le 2026-11-15

> « Frustum streaming is controlled per player through the `Class.Player.FrustumStreaming` property. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/workspace/streaming/frustum.md), consulté le 2026-11-15

> « Roblox might adjust this allocation in the future if games commonly use both frustum streaming and replication foci and the frustum needs higher priority. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/workspace/streaming/frustum.md), consulté le 2026-11-15

> « On devices with reduced graphics quality or low frame rates, the engine might disable frustum streaming automatically. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/workspace/streaming/frustum.md), consulté le 2026-11-15

> « - **Not applicable to non-streaming experiences**: if your experience does not use instance streaming, all instances are already present on the client and frustum streaming has no effect. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/workspace/streaming/frustum.md), consulté le 2026-11-15


## Problèmes connus

À compléter.

## Alternatives

À compléter.

## Tests dans Roblox Studio

- Testé : **non**
- Conditions : —
- Résultat : —

## Questions ouvertes

- Quels réglages exacts (valeurs, propriétés) pour « forest streaming trees » ?
- Le résultat tient-il de nuit, à la lampe torche, sur mobile ?

## Scores (diagnostic, pas une preuve)

- Pertinence sujet : 0.5 · Contenu technique : 0.88 · Lien Roblox : oui
- Termes techniques repérés : performance, animation, streaming, terrain
