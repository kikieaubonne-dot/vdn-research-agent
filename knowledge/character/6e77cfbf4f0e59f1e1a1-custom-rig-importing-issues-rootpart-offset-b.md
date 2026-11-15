---
id: "vdn-1290b940c378"
title: "Custom Rig Importing Issues (RootPart Offset & Bone Visual Glitches)"
domain: "characters"
subdomain: "character"
status: "documente"
tested_in_studio: "non"
confidence: "faible"
confidence_reason: "Ancienne fiche V1–V4 reclassée automatiquement : 2 passages techniques extraits d'une source de niveau 2 ; aucun test dans Roblox Studio."
engine_version: "inconnue"
source_tier: 2
provider: "devforum"
official: false
sources:
  - "https://devforum.roblox.com/t/4747045"
accessed: "2026-11-15"
queries:
  - "Roblox skinned mesh facial animation"
created: "2026-11-15"
updated: "2026-11-15"
tags:
  - "vdn"
  - "characters"
  - "character"
  - "documente"
  - "migre-v5"
legacy_status: "a_verifier"
legacy_source_type: "Roblox DevForum"
legacy_topic: "character"
legacy_score_heuristique: 51
legacy_collected_utc: "2026-11-15T15:38:51+00:00"
---

> **Documenté** (reclassement V5 du 2026-11-15) · 2 passages techniques extraits d'une source de niveau 2 ; aucun test dans Roblox Studio.
> Le contenu historique ci-dessous est conservé tel quel.

# Custom Rig Importing Issues (RootPart Offset & Bone Visual Glitches)

**Sujet :** Personnages réalistes Roblox

**Source :** [Roblox DevForum](https://devforum.roblox.com/t/custom-rig-importing-issues-rootpart-offset-bone-visual-glitches/4747045)

**Question de recherche :** Roblox skinned mesh facial animation

## Extrait de découverte (non vérifié)

About Me Hello! I am working on a custom character rig in Blender that uses multiple meshes bound to a single Armature. I have applied all transforms in Blender before exporting, but I am running into two persistent issues when importing the FBX into Roblox Studio using the 3D Importer. The Issue...

## Vérification Roblox / Blender

- [ ] Ouvrir et lire la source complète
- [ ] Vérifier la version du moteur et les limites techniques
- [ ] Extraire une procédure précise, des paramètres et les prérequis
- [ ] Tester dans Blender puis Roblox Studio
- [ ] Mesurer visuel, performances et reproductibilité

## Résultat du test

À compléter après expérimentation.

## Analyse V3 — éléments techniques à vérifier

**Statut :** passages candidats extraits de la source, **non validés** dans Roblox.

**Source lue :** https://devforum.roblox.com/t/custom-rig-importing-issues-rootpart-offset-bone-visual-glitches/4747045  
**Contenu :** DevForum  
**Passages candidats :** 3

### Passages et paramètres repérés

- The Issues Issue 1: RootPart Displacement (Geometry Offset from Collision) The Problem: The RootPart behavior is broken.
- All transforms ( Ctrl + A → All Transforms) were applied to both the meshes and the armature in Blender prior to export.
- Issue 2: Eye Bones / Visual Bug with Face Rigging The Problem: I cannot animate the eyes because the eye bones or their associated geometry are glitching/not showing up correctly after import.

### Questions de recherche complémentaires

- character Roblox collision implementation limitations troubleshooting
- character Roblox export implementation limitations troubleshooting
- character Roblox bones implementation limitations troubleshooting

### Validation requise

- [ ] Vérifier chaque passage dans la source complète
- [ ] Confirmer les limitations Roblox actuelles
- [ ] Tester dans Roblox Studio ET Roblox Player
- [ ] Mesurer qualité et performance
