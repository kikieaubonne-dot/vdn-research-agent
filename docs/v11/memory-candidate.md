---
id: "vdn-ocean-0104f5080582c698eb53"
title: "foliage cards transparency — application à la forêt Roblox"
domain: "ocean"
subdomain: "cards"
status: "candidat"
schema: "vdn.knowledge/11"
ocean_states:
  - "DISCOVERED"
  - "EXTRACTED"
  - "SYNTHESIZED"
  - "SOURCE_SUPPORTED"
source_tier: 1
sources:
  - "https://create.roblox.com/docs/art/modeling/surface-appearance"
accessed: "2026-11-16"
engine_version: "unknown"
tested_in_studio: "non"
review_status: "pending"
tags:
  - "vdn"
  - "ocean"
  - "candidate"
  - "cards"
---

# foliage cards transparency — application à la forêt Roblox

## Problème
Compléter les matériaux et performances autour des collisions de la forêt Roblox

## Contexte
VDN isolated forest laboratory

## Résumé technique
Les sources citées documentent foliage, transparency, alpha. Pour la forêt Roblox, la décision à préparer concerne cards. La méthode proposée reste à comparer dans le laboratoire ; aucune valeur optimale ou compatibilité de version n’est déduite.

## Extraits justificatifs

> « - When alpha is used to cut out the shape of mostly opaque objects with hard edges such as foliage, lace fabric, and netting, »
> — [source](https://create.roblox.com/docs/art/modeling/surface-appearance), consultée le 2026-11-16

## Prérequis
- isolated asset copies
- recorded software versions
- target device and controller

## Procédure candidate — propositions non validées
- Travailler dans une copie du laboratoire, avec versions, appareil, caméra et assets consignés.
- Inspecter les éléments documentés : foliage, transparency, alpha.
- Construire deux copies de même silhouette : géométrie et cartes de feuillage ; conserver les exports séparés.
- Consigner atlas, UV, normales et mode de transparence réellement disponibles ; vérifier chaque option dans la version Studio installée.
- Comparer contours, chevauchements, ombres et changements à distance sous la même lampe torche ; photographier les défauts.
- Préparer deux variantes ne différant que par la méthode étudiée ; consigner les valeurs réellement choisies.
- Répéter le protocole sous les mêmes conditions et conserver mesures, captures et échecs.
- Comparer les limites observées avant réutilisation ; conserver la variante initiale pour rollback.

## Alternatives et compromis
- Proposition de comparaison contrôlée ; aucun résultat ou compromis optimal n’est établi par cette fiche.

## Limites et incertitudes
- No result reproduced in the user project.
- Software version and target device not independently verified.

## Protocole de reproduction proposé, non exécuté
- Fix comparison controls before running.
- Repeat traversal and rendering checks; record raw measurements.
- Compare movement blockages, collision accuracy and measured frame cost; no FPS assumed.

## Paramètres documentés
Only literal source tokens are documented; no numeric recommendation inferred.
Tokens présents : foliage, transparency, alpha

## Connaissances associées
- [[forest/713de5a2c6e6644d3390-leonisbel-night-hunt]]
- [[spruce/4b3e4c63ddab358ee1df-nightcycle-quick-part]]
- [[spruce/c20177c2856493a2bece-surfaceappearance-alphamode-transparency-rend]]

## Expériences associées
Identifiants : aucune expérience liée ; protocole proposé seulement

## Retour arrière
Conserver et restaurer les copies initiales ; aucune édition du jeu de production.

## Données structurées Océan
```json
{"alternatives": ["Proposition de comparaison contrôlée ; aucun résultat ou compromis optimal n’est établi par cette fiche."], "claims": [{"id": "claim-1", "kind": "literal_source_excerpt", "quote": "- When alpha is used to cut out the shape of mostly opaque objects with hard edges such as foliage, lace fabric, and netting,", "scope": "source statement; applicability requires test", "source_id": "source-1"}], "confidence_reason": "Literal attribution checked mechanically; engineering correctness and project applicability unverified.", "context": "VDN isolated forest laboratory", "documented_tokens": ["foliage", "transparency", "alpha"], "experiment_ids": [], "facet": "cards", "hypotheses": [], "id": "vdn-ocean-0104f5080582c698eb53", "model_proposed_steps": [], "model_state": "not_used", "parameters": "Only literal source tokens are documented; no numeric recommendation inferred.", "prerequisites": ["isolated asset copies", "recorded software versions", "target device and controller"], "problem": "Compléter les matériaux et performances autour des collisions de la forêt Roblox", "procedure": [{"origin": "engineering_proposal", "text": "Travailler dans une copie du laboratoire, avec versions, appareil, caméra et assets consignés.", "verified": false}, {"origin": "engineering_proposal", "text": "Inspecter les éléments documentés : foliage, transparency, alpha.", "verified": false}, {"origin": "engineering_proposal", "text": "Construire deux copies de même silhouette : géométrie et cartes de feuillage ; conserver les exports séparés.", "verified": false}, {"origin": "engineering_proposal", "text": "Consigner atlas, UV, normales et mode de transparence réellement disponibles ; vérifier chaque option dans la version Studio installée.", "verified": false}, {"origin": "engineering_proposal", "text": "Comparer contours, chevauchements, ombres et changements à distance sous la même lampe torche ; photographier les défauts.", "verified": false}, {"origin": "engineering_proposal", "text": "Préparer deux variantes ne différant que par la méthode étudiée ; consigner les valeurs réellement choisies.", "verified": false}, {"origin": "engineering_proposal", "text": "Répéter le protocole sous les mêmes conditions et conserver mesures, captures et échecs.", "verified": false}, {"origin": "engineering_proposal", "text": "Comparer les limites observées avant réutilisation ; conserver la variante initiale pour rollback.", "verified": false}], "related_note_paths": ["forest/713de5a2c6e6644d3390-leonisbel-night-hunt", "spruce/4b3e4c63ddab358ee1df-nightcycle-quick-part", "spruce/c20177c2856493a2bece-surfaceappearance-alphamode-transparency-rend"], "related_notes": ["vdn-319f4403f590", "vdn-4b3e4c63ddab", "vdn-713de5a2c6e6"], "schema": "vdn.knowledge/11", "sources": [{"accessed": "2026-11-16", "id": "source-1", "policy": "public documentation; metadata, links and short excerpts", "provider": "roblox", "published": null, "raw_text_sha256": "cf02d3f01584a51f0622086732d89ae69a27a1902abe321bf0008c3adc014ca4", "retrieved_at": 1794810177.2209241, "text_sha256": "cf02d3f01584a51f0622086732d89ae69a27a1902abe321bf0008c3adc014ca4", "truncated": false, "url": "https://create.roblox.com/docs/art/modeling/surface-appearance", "version": "unknown"}], "states": ["DISCOVERED", "EXTRACTED", "SYNTHESIZED", "SOURCE_SUPPORTED"], "summary": "Les sources citées documentent foliage, transparency, alpha. Pour la forêt Roblox, la décision à préparer concerne cards. La méthode proposée reste à comparer dans le laboratoire ; aucune valeur optimale ou compatibilité de version n’est déduite.", "title": "foliage cards transparency — application à la forêt Roblox", "truth_verified": false, "uncertainties": ["No result reproduced in the user project.", "Software version and target device not independently verified."], "validation": ["Fix comparison controls before running.", "Repeat traversal and rendering checks; record raw measurements.", "Compare movement blockages, collision accuracy and measured frame cost; no FPS assumed."]}
```
