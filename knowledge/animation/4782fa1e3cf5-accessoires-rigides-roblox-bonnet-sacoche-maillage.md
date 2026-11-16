---
id: "vdn-4782fa1e3cf5"
title: "Accessoires rigides Roblox — bonnet, sacoche, maillage et attachments"
domain: "animation"
subdomain: "accessories"
status: "candidat"
source_tier: 1
sources:
  - "https://create.roblox.com/docs/avatar/rigid-accessories"
provider: "roblox_docs"
official: true
accessed: "2026-11-16"
created: "2026-11-16"
updated: "2026-11-16"
engine_version: "inconnue"
tested_in_studio: "non"
confidence: "faible"
evidence_status: "a_verifier"
compatibility_status: "non_verifie"
procedure_status: "candidate"
review_status: "pending"
source_dates:
  - "2026-11-14T04:04:50Z"
source_sha256:
  - "26c7264ca2ce33ebe7a7a26e0c6d943d06d75d9d68e6a6257fd43d5479f2866c"
queries:
  - "accessories Attachment SurfaceAppearance"
editorial_steps:
  - "Préparer le maillage et les textures de l’accessoire ; utiliser les composants et points d’attache attendus par Roblox."
  - "Importer les composants depuis un même fichier FBX ou glTF et régler les textures sur MeshPart via SurfaceAppearance ou TextureID selon le cas."
  - "Configurer l’Attachment, éventuellement avec Accessory Fitting Tool ; vérifier l’alignement sur le personnage réel et ses animations."
procedure_origin: "source_based_editorial_candidate"
production_priority: 4
tags:
  - "vdn"
  - "v9"
  - "accessories"
  - "a-verifier"
---

# Accessoires rigides Roblox — bonnet, sacoche, maillage et attachments

> Procédure éditoriale candidate issue des sources listées ; aucun test Studio ni revue externe.

## Problème

accessories

## Contexte

Roblox ; version du projet et appareils à vérifier.

## Sources

- [1] https://create.roblox.com/docs/avatar/rigid-accessories — consulté le 2026-11-16

## Prérequis

- Personnage de test et points d’attache identifiés ; maillage et textures de l’accessoire. [source 1]

## Méthode candidate

- Préparer le maillage et les textures de l’accessoire ; utiliser les composants et points d’attache attendus par Roblox. [source 1]
- Importer les composants depuis un même fichier FBX ou glTF et régler les textures sur MeshPart via SurfaceAppearance ou TextureID selon le cas. [source 1]
- Configurer l’Attachment, éventuellement avec Accessory Fitting Tool ; vérifier l’alignement sur le personnage réel et ses animations. [source 1]

## Limites connues de Roblox

- Un accessoire rigide ne se déforme pas comme un accessoire layered ; les composants requis ne sont pas interchangeables. [source 1]
- La compatibilité d’un rig personnalisé et la réplication multijoueur ne sont pas prouvées par cette page seule. [source 1]

## Alternatives

- Comparer rigide et layered selon le besoin de déformation ; ne pas choisir layered uniquement pour une attache fixe. [source 1]

## Paramètres (sourcés)

- Formats cités pour l’import : FBX ou glTF ; points d’attache représentés par Attachment. [source 1]

## Protocole de reproduction proposé, non exécuté

Tester bonnet et sacoche au repos et en animation, puis deux clients ; relever attache, pénétrations et réplication. Cette validation n’a pas été exécutée.

## Diagnostic

Conserver erreurs, environnement, paramètres et observations. Les causes proposées restent des hypothèses.

## Retour arrière

Retirer uniquement l’accessoire de test et restaurer le personnage de référence ; conserver le rig original.

## Extraits justificatifs

> « You can create textures within a texture painting program or 3D modeling software. »
> — [source](https://create.roblox.com/docs/avatar/rigid-accessories)

## Niveau de preuve

Documentation officielle consultée ; exactitude de la procédure proposée et fonctionnement dans le jeu non vérifiés.
