---
id: "vdn-ac07d1c0fed7"
title: "Sauvegardes Roblox — DataStore, UpdateAsync et erreurs"
domain: "roblox"
subdomain: "persistence"
status: "candidat"
source_tier: 1
sources:
  - "https://create.roblox.com/docs/cloud-services/data-stores"
  - "https://create.roblox.com/docs/reference/engine/classes/DataStore"
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
  - "2026-11-14T04:04:51Z"
  - "2026-11-14T04:05:03Z"
source_sha256:
  - "48b11e1a3779490e033bc4797821d3b37cd814e02192021e95379222b5282822"
  - "4952919fa12bc2114b06fc359562f80d7a593c2fa0052e6c9b5bb19f3f122335"
queries:
  - "saves UpdateAsync pcall"
editorial_steps:
  - "Accéder au DataStore depuis un Script serveur ; protéger les opérations réseau avec pcall et traiter explicitement leur échec."
  - "Utiliser UpdateAsync avec une transformation de la valeur courante ; retourner nil pour annuler une écriture."
  - "Garder le callback sans fonction susceptible de suspendre son exécution. Définir les reprises comme une politique de projet restant à tester."
procedure_origin: "source_based_editorial_candidate"
production_priority: 0
tags:
  - "vdn"
  - "v9"
  - "saves"
  - "a-verifier"
---

# Sauvegardes Roblox — DataStore, UpdateAsync et erreurs

> Procédure éditoriale candidate issue des sources listées ; aucun test Studio ni revue externe.

## Problème

saves

## Contexte

Roblox ; version du projet et appareils à vérifier.

## Sources

- [1] https://create.roblox.com/docs/cloud-services/data-stores — consulté le 2026-11-16
- [2] https://create.roblox.com/docs/reference/engine/classes/DataStore — consulté le 2026-11-16

## Prérequis

- Lieu de test séparé des données de production ; Script côté serveur et schéma de clés défini. [source 1]

## Méthode candidate

- Accéder au DataStore depuis un Script serveur ; protéger les opérations réseau avec pcall et traiter explicitement leur échec. [source 1]
- Utiliser UpdateAsync avec une transformation de la valeur courante ; retourner nil pour annuler une écriture. [source 1]
- Garder le callback sans fonction susceptible de suspendre son exécution. Définir les reprises comme une politique de projet restant à tester. [source 1]

## Limites connues de Roblox

- L’accès depuis LocalScript n’est pas autorisé ; les appels réseau peuvent échouer. [source 1]
- Le callback UpdateAsync ne peut pas yield. Le succès d’un essai ne prouve pas l’absence de perte en concurrence. [source 1]

## Alternatives

- Comparer SetAsync et UpdateAsync selon les accès concurrents, sans leur attribuer des garanties équivalentes. [source 1]

## Paramètres (sourcés)

- Callback UpdateAsync : valeur nouvelle ou nil pour annuler ; pas de yield. Aucune stratégie de retry du projet n’est validée. [source 1]

## Protocole de reproduction proposé, non exécuté

Dans un lieu de test : écrire/lire une valeur, annuler avec nil, provoquer un échec et deux mises à jour concurrentes ; vérifier ancienne valeur et absence de perte.

## Diagnostic

Conserver erreurs, environnement, paramètres et observations. Les causes proposées restent des hypothèses.

## Retour arrière

Conserver une copie de test des anciennes valeurs et désactiver la nouvelle logique en cas d’écart ; ne pas expérimenter sur les données des joueurs.

## Extraits justificatifs

> « url: /docs/en-us/cloud-services/data-stores »
> — [source](https://create.roblox.com/docs/cloud-services/data-stores)

> « - **Property `Capabilities`** (`SecurityCapabilities`): The set of capabilities allowed to be used for scripts inside this »
> — [source](https://create.roblox.com/docs/reference/engine/classes/DataStore)

## Niveau de preuve

Documentation officielle consultée ; exactitude de la procédure proposée et fonctionnement dans le jeu non vérifiés.
