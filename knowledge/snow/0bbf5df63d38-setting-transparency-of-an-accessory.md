---
id: "vdn-0bbf5df63d38"
title: "Setting transparency of an accessory?"
domain: "snow"
subdomain: "snow"
status: "documente"
tested_in_studio: "non"
confidence: "faible"
confidence_reason: "6 passages techniques dont 2 avec action et objet identifiables, source de niveau 2 ; indice technique seulement, procédure complète non garantie ; aucun test dans Roblox Studio."
engine_version: "inconnue"
source_tier: 2
provider: "devforum"
official: false
sources:
  - "https://devforum.roblox.com/t/1777283"
accessed: "2026-11-23"
queries:
  - "Decal Transparency settings"
created: "2026-11-23"
updated: "2026-11-23"
tags:
  - "vdn"
  - "snow"
  - "snow"
  - "documente"
staff_posts: 0
accepted_answer: true
last_posted: "2022-05-02"
---

# Setting transparency of an accessory?

> **Documenté** · source [Roblox DevForum](https://devforum.roblox.com/t/setting-transparency-of-an-accessory/1777283) · consultée le 2026-11-23 · **non testée dans Roblox Studio**

## Objectif

Répondre à : *Decal Transparency settings* (sujet : Neige, givre et traces).

## Description technique

À rédiger à partir des extraits ci-dessous (analyse humaine ou Ollama). Rien n'est affirmé ici sans source.

## Étapes reproductibles

Instructions extraites automatiquement : procedure partielle, ordre et fonctionnement non verifies.

1. Each accessory comes with a Part called “Handle” (Which represents the accessory itself, It comes with the Mesh, etc) So you would just need to change the Handle’s Transparency. -- [Roblox DevForum](https://devforum.roblox.com/t/setting-transparency-of-an-accessory/1777283)
2. When looping through the descendants of the Character model, make sure to check that the Instance on each iteration of the loop is a BasePart, as that will ensure it doesn’t try to modify the Transparency property for any objects that don’t have that property. -- [Roblox DevForum](https://devforum.roblox.com/t/setting-transparency-of-an-accessory/1777283)

## Paramètres (sourcés)

Aucun paramètre chiffré trouvé dans les extraits.

## Limites connues de Roblox

- « The problem is that I cannot get the transparency of the accessory to display correctly as transparency is not a child of the accessory. » — [Roblox DevForum](https://devforum.roblox.com/t/setting-transparency-of-an-accessory/1777283)
- « An accessory itself, does not have neither a “visible” nor a “transparency” property. » — [Roblox DevForum](https://devforum.roblox.com/t/setting-transparency-of-an-accessory/1777283)
- « Changing the transparency of the handle causes some strange clipping issues but I guess that’s the only current option. » — [Roblox DevForum](https://devforum.roblox.com/t/setting-transparency-of-an-accessory/1777283)

## Extraits justificatifs

> « The problem is that I cannot get the transparency of the accessory to display correctly as transparency is not a child of the accessory. »
> — [Roblox DevForum](https://devforum.roblox.com/t/setting-transparency-of-an-accessory/1777283), consulté le 2026-11-23

> « Each accessory comes with a Part called “Handle” (Which represents the accessory itself, It comes with the Mesh, etc) So you would just need to change the Handle’s Transparency. »
> — [Roblox DevForum](https://devforum.roblox.com/t/setting-transparency-of-an-accessory/1777283), consulté le 2026-11-23

> « When looping through the descendants of the Character model, make sure to check that the Instance on each iteration of the loop is a BasePart, as that will ensure it doesn’t try to modify the Transparency property for any objects that don’t have that property. »
> — [Roblox DevForum](https://devforum.roblox.com/t/setting-transparency-of-an-accessory/1777283), consulté le 2026-11-23

> « An accessory itself, does not have neither a “visible” nor a “transparency” property. »
> — [Roblox DevForum](https://devforum.roblox.com/t/setting-transparency-of-an-accessory/1777283), consulté le 2026-11-23

> « Other classes I know that have transparency property are UI’s stuff. »
> — [Roblox DevForum](https://devforum.roblox.com/t/setting-transparency-of-an-accessory/1777283), consulté le 2026-11-23

> « Changing the transparency of the handle causes some strange clipping issues but I guess that’s the only current option. »
> — [Roblox DevForum](https://devforum.roblox.com/t/setting-transparency-of-an-accessory/1777283), consulté le 2026-11-23


## Problèmes connus

À compléter.

## Alternatives

À compléter.

## Tests dans Roblox Studio

- Testé : **non**
- Conditions : —
- Résultat : —

## Questions ouvertes

- Quels réglages exacts (valeurs, propriétés) pour « Decal Transparency settings » ?
- Le résultat tient-il de nuit, à la lampe torche, sur mobile ?

## Scores (diagnostic, pas une preuve)

- Pertinence sujet : 0.583 · Contenu technique : 0.76 · Lien Roblox : oui
- Termes techniques repérés : transparency
