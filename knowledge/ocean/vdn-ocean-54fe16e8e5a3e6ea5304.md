---
id: "vdn-ocean-54fe16e8e5a3e6ea5304"
title: "MeshPart collisions CanCollide — application à la forêt Roblox"
domain: "ocean"
subdomain: "collision"
status: "candidat"
schema: "vdn.knowledge/11"
ocean_states:
  - "DISCOVERED"
  - "EXTRACTED"
  - "SYNTHESIZED"
  - "SOURCE_SUPPORTED"
source_tier: 1
sources:
  - "https://create.roblox.com/docs/performance-optimization/improve"
accessed: "2026-11-16"
engine_version: "unknown"
tested_in_studio: "non"
review_status: "pending"
tags:
  - "vdn"
  - "ocean"
  - "candidate"
  - "collision"
---

# MeshPart collisions CanCollide — application à la forêt Roblox

## Problème
Comment obtenir une forêt d’épicéas Roblox nocturne avec des collisions correctes et une lampe torche ?

## Contexte
VDN isolated forest laboratory

## Résumé technique
Les sources citées documentent CollisionFidelity, CanCollide. Pour la forêt Roblox, la décision à préparer concerne les collisions des troncs et branches, les volumes simples séparés et le passage du contrôleur. La méthode proposée reste à comparer dans le laboratoire ; aucune valeur optimale ou compatibilité de version n’est déduite.

## Extraits justificatifs

> « - **Overly precise collision detection** - Mesh parts have a `Class.MeshPart.CollisionFidelity|CollisionFidelity` property for detecting collision which offers a variety of modes with different levels »
> — [source](https://create.roblox.com/docs/performance-optimization/improve), consultée le 2026-11-16

## Prérequis
- isolated asset copies
- recorded software versions
- target device and controller

## Procédure candidate — propositions non validées
- Travailler dans une copie du laboratoire, avec versions, appareil, caméra et assets consignés.
- Inspecter les troncs, branches, décor et MeshParts ; relever les propriétés documentées CollisionFidelity, CanCollide, sans présumer de leur valeur optimale.
- Proposition à tester : séparer la géométrie visuelle des volumes de collision simples, en conservant le comportement initial pour comparaison.
- Tester le contrôleur réel entre les troncs, sur les pentes et près des branches ; consigner les blocages et paramètres de collision de chaque variante.
- Préparer deux variantes ne différant que par la méthode étudiée ; consigner les valeurs réellement choisies.
- Répéter le protocole sous les mêmes conditions et conserver mesures, captures et échecs.
- Comparer les limites observées avant réutilisation ; conserver la variante initiale pour rollback.

## Alternatives et compromis
- Proposition non validée : comparer collisions du mesh et proxies simples séparés ; mesurer le compromis précision/coût.
- Ne pas désactiver une collision sur la seule base de cette fiche ; vérifier les besoins de gameplay.

## Limites et incertitudes
- No result reproduced in the user project.
- Software version and target device not independently verified.
- Source cache truncated; unseen sections may add constraints: source-1

## Protocole de reproduction proposé, non exécuté
- Fix comparison controls before running.
- Repeat traversal and rendering checks; record raw measurements.
- Compare movement blockages, collision accuracy and measured frame cost; no FPS assumed.

## Paramètres documentés
Only literal source tokens are documented; no numeric recommendation inferred.
Tokens présents : CollisionFidelity, CanCollide

## Connaissances associées
- [[forest/5aa463725976-improve-performance]]
- [[snow/fe4c577081af-collisions-on-meshs]]
- [[vegetation/d5dda0d02f6d-manage-level-of-detail-settings-on-roblox]]

## Expériences associées
Identifiants : aucune expérience liée ; protocole proposé seulement

## Retour arrière
Conserver et restaurer les copies initiales ; aucune édition du jeu de production.

## Données structurées Océan
```json
{"alternatives": ["Proposition non validée : comparer collisions du mesh et proxies simples séparés ; mesurer le compromis précision/coût.", "Ne pas désactiver une collision sur la seule base de cette fiche ; vérifier les besoins de gameplay."], "claims": [{"id": "claim-1", "kind": "literal_source_excerpt", "quote": "- **Overly precise collision detection** - Mesh parts have a `Class.MeshPart.CollisionFidelity|CollisionFidelity` property for detecting collision which offers a variety of modes with different levels", "scope": "source statement; applicability requires test", "source_id": "source-1"}], "confidence_reason": "Literal attribution checked mechanically; engineering correctness and project applicability unverified.", "context": "VDN isolated forest laboratory", "documented_tokens": ["CollisionFidelity", "CanCollide"], "experiment_ids": [], "facet": "collision", "hypotheses": [], "id": "vdn-ocean-54fe16e8e5a3e6ea5304", "model_proposed_steps": [], "model_state": "not_used", "parameters": "Only literal source tokens are documented; no numeric recommendation inferred.", "prerequisites": ["isolated asset copies", "recorded software versions", "target device and controller"], "problem": "Comment obtenir une forêt d’épicéas Roblox nocturne avec des collisions correctes et une lampe torche ?", "procedure": [{"origin": "engineering_proposal", "text": "Travailler dans une copie du laboratoire, avec versions, appareil, caméra et assets consignés.", "verified": false}, {"origin": "engineering_proposal", "text": "Inspecter les troncs, branches, décor et MeshParts ; relever les propriétés documentées CollisionFidelity, CanCollide, sans présumer de leur valeur optimale.", "verified": false}, {"origin": "engineering_proposal", "text": "Proposition à tester : séparer la géométrie visuelle des volumes de collision simples, en conservant le comportement initial pour comparaison.", "verified": false}, {"origin": "engineering_proposal", "text": "Tester le contrôleur réel entre les troncs, sur les pentes et près des branches ; consigner les blocages et paramètres de collision de chaque variante.", "verified": false}, {"origin": "engineering_proposal", "text": "Préparer deux variantes ne différant que par la méthode étudiée ; consigner les valeurs réellement choisies.", "verified": false}, {"origin": "engineering_proposal", "text": "Répéter le protocole sous les mêmes conditions et conserver mesures, captures et échecs.", "verified": false}, {"origin": "engineering_proposal", "text": "Comparer les limites observées avant réutilisation ; conserver la variante initiale pour rollback.", "verified": false}], "related_note_paths": ["forest/5aa463725976-improve-performance", "snow/fe4c577081af-collisions-on-meshs", "vegetation/d5dda0d02f6d-manage-level-of-detail-settings-on-roblox"], "related_notes": ["vdn-5aa463725976", "vdn-fe4c577081af", "vdn-d5dda0d02f6d"], "schema": "vdn.knowledge/11", "sources": [{"accessed": "2026-11-16", "id": "source-1", "policy": "public documentation; metadata, links and short excerpts", "provider": "roblox", "published": null, "raw_text_sha256": "dd915a6b96745d4e082e0d12a9e824bb784ad724911115362061339377159fc1", "retrieved_at": 1794810391.7479572, "text_sha256": "3517d9d6e0db2f5a3febf2023c9828687af332427af9cea618ce5edb1716a99e", "truncated": true, "url": "https://create.roblox.com/docs/performance-optimization/improve", "version": "unknown"}], "states": ["DISCOVERED", "EXTRACTED", "SYNTHESIZED", "SOURCE_SUPPORTED"], "summary": "Les sources citées documentent CollisionFidelity, CanCollide. Pour la forêt Roblox, la décision à préparer concerne les collisions des troncs et branches, les volumes simples séparés et le passage du contrôleur. La méthode proposée reste à comparer dans le laboratoire ; aucune valeur optimale ou compatibilité de version n’est déduite.", "title": "MeshPart collisions CanCollide — application à la forêt Roblox", "truth_verified": false, "uncertainties": ["No result reproduced in the user project.", "Software version and target device not independently verified.", "Source cache truncated; unseen sections may add constraints: source-1"], "validation": ["Fix comparison controls before running.", "Repeat traversal and rendering checks; record raw measurements.", "Compare movement blockages, collision accuracy and measured frame cost; no FPS assumed."]}
```
