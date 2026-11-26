---
id: "vdn-06fe4174654e"
title: "Instance streaming"
domain: "performance"
subdomain: "performance"
status: "documente"
tested_in_studio: "non"
confidence: "moyenne"
confidence_reason: "8 passages techniques dont 3 avec action et objet identifiables, source de niveau 1 (réponse du personnel Roblox / doc officielle) ; indice technique seulement, procédure complète non garantie ; aucun test dans Roblox Studio."
engine_version: "inconnue"
source_tier: 1
provider: "roblox_docs"
official: true
sources:
  - "https://create.roblox.com/docs/workspace/streaming"
accessed: "2026-11-26"
queries:
  - "instance streaming level detail"
created: "2026-11-26"
updated: "2026-11-26"
tags:
  - "vdn"
  - "performance"
  - "performance"
  - "documente"
---

# Instance streaming

> **Documenté** · source [Documentation Roblox](https://create.roblox.com/docs/en-us/workspace/streaming.md) · consultée le 2026-11-26 · **non testée dans Roblox Studio**

## Objectif

Répondre à : *instance streaming level detail* (sujet : Performances et niveaux de détail).

## Description technique

À rédiger à partir des extraits ci-dessous (analyse humaine ou Ollama). Rien n'est affirmé ici sans source.

## Étapes reproductibles

Instructions extraites automatiquement : procedure partielle, ordre et fonctionnement non verifies.

1. > **Success:** Once you review this technical guide, it's recommended that you review the [streaming techniques](/docs/en-us/workspace/streaming/techniques.md) guide on how to use streaming efficiently and effectively, and the [SLIM](/docs/en-us/workspace/streaming/slim.md) guide for enabling high‑fidelity level‑of‑detail on models and avatars. -- [Documentation Roblox](https://create.roblox.com/docs/en-us/workspace/streaming.md)
2. | `Class.Workspace.ModelStreamingBehavior\|ModelStreamingBehavior` | Controls how [Nonatomic](#nonatomic) (default) models stream in and out.<br><br>**RECOMMENDED** Use `Enum.ModelStreamingBehavior.Improved\|Improved` to enable the most efficient streaming for `Class.Model\|Models` with `Class.BasePart` descendants. -- [Documentation Roblox](https://create.roblox.com/docs/en-us/workspace/streaming.md)
3. | `Class.Workspace.PredictiveStreamingMode\|PredictiveStreamingMode` | Opts in to [predictive streaming](#predictive-streaming) which uses engine signals to proactively stream areas a player is likely to need soon, such as respawn locations or regions the player recently left via `Datatype.CFrame` change. -- [Documentation Roblox](https://create.roblox.com/docs/en-us/workspace/streaming.md)

## Paramètres (sourcés)

- « Instance streaming is controlled through the `Class.Workspace.StreamingEnabled` property, enabled by default for new places created in Studio. » — [Documentation Roblox](https://create.roblox.com/docs/en-us/workspace/streaming.md)
- « When enabled, avatars render using SLIM in the same way that setting `Class.Model.LevelOfDetail` to `Enum.ModelLevelOfDetail.SLIM\|SLIM` works for other models. » — [Documentation Roblox](https://create.roblox.com/docs/en-us/workspace/streaming.md)

## Limites connues de Roblox

- « The only exception is when the assembly is [anchored](/docs/en-us/physics/assemblies.md#anchoring-behavior), in which case only the `Class.BasePart|BaseParts` within the streaming radius are streamed in alongside their associated `Class.Constraint|Constraints` and `Class.Attachment|Attachments`. » — [Documentation Roblox](https://create.roblox.com/docs/en-us/workspace/streaming.md)
- « However, the target radius is also the maximum distance players will be able to see the full detail of your game, so you should pick a value that creates a nice balance between these.<br><br>**RECOMMENDED** Use the default of `1024` to strike a good balance between visibility for players on high‑end devices and a reasonable memory footprint. » — [Documentation Roblox](https://create.roblox.com/docs/en-us/workspace/streaming.md)

## Extraits justificatifs

> « Instance streaming is controlled through the `Class.Workspace.StreamingEnabled` property, enabled by default for new places created in Studio. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/workspace/streaming.md), consulté le 2026-11-26

> « > **Success:** Once you review this technical guide, it's recommended that you review the [streaming techniques](/docs/en-us/workspace/streaming/techniques.md) guide on how to use streaming efficiently and effectively, and the [SLIM](/docs/en-us/workspace/streaming/slim.md) guide for enabling high‑fidelity level‑of‑detail on models and avatars. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/workspace/streaming.md), consulté le 2026-11-26

> « The only exception is when the assembly is [anchored](/docs/en-us/physics/assemblies.md#anchoring-behavior), in which case only the `Class.BasePart|BaseParts` within the streaming radius are streamed in alongside their associated `Class.Constraint|Constraints` and `Class.Attachment|Attachments`. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/workspace/streaming.md), consulté le 2026-11-26

> « When enabled, avatars render using SLIM in the same way that setting `Class.Model.LevelOfDetail` to `Enum.ModelLevelOfDetail.SLIM\|SLIM` works for other models. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/workspace/streaming.md), consulté le 2026-11-26

> « | `Class.Workspace.ModelStreamingBehavior\|ModelStreamingBehavior` | Controls how [Nonatomic](#nonatomic) (default) models stream in and out.<br><br>**RECOMMENDED** Use `Enum.ModelStreamingBehavior.Improved\|Improved` to enable the most efficient streaming for `Class.Model\|Models` with `Class.BasePart` descendants. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/workspace/streaming.md), consulté le 2026-11-26

> « | `Class.Workspace.PredictiveStreamingMode\|PredictiveStreamingMode` | Opts in to [predictive streaming](#predictive-streaming) which uses engine signals to proactively stream areas a player is likely to need soon, such as respawn locations or regions the player recently left via `Datatype.CFrame` change. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/workspace/streaming.md), consulté le 2026-11-26

> « However, the target radius is also the maximum distance players will be able to see the full detail of your game, so you should pick a value that creates a nice balance between these.<br><br>**RECOMMENDED** Use the default of `1024` to strike a good balance between visibility for players on high‑end devices and a reasonable memory footprint. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/workspace/streaming.md), consulté le 2026-11-26

> « | `Class.Workspace.StreamOutBehavior\|StreamOutBehavior` | This property sets the [streaming out](#stream-out) behavior according to the value of `Enum.StreamOutBehavior`. »
> — [Documentation Roblox](https://create.roblox.com/docs/en-us/workspace/streaming.md), consulté le 2026-11-26


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

- Pertinence sujet : 1.0 · Contenu technique : 1.0 · Lien Roblox : oui
- Termes techniques repérés : meshpart, performance, render, streaming, terrain, 1024
