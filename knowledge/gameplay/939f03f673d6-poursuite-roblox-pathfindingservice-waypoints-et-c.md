---
id: "vdn-939f03f673d6"
title: "Poursuite Roblox — PathfindingService, waypoints et chemins bloqués"
domain: "gameplay"
subdomain: "pursuit"
status: "candidat"
source_tier: 1
sources:
  - "https://create.roblox.com/docs/characters/pathfinding"
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
  - "4ac36ed92a5fad3f626bf1ee3a8840fb71b9f7a8cca4e46512e1c9fe02563eb0"
queries:
  - "pursuit ComputeAsync Blocked"
editorial_steps:
  - "Créer un Path avec les paramètres du gabarit du PNJ, puis calculer le chemin avec ComputeAsync sous gestion d’erreur."
  - "Vérifier PathStatus.Success avant de parcourir les waypoints retournés dans leur ordre."
  - "Sur un blocage pertinent signalé par Path.Blocked, recalculer un chemin ; borner les recomputations comme politique de projet à mesurer."
procedure_origin: "source_based_editorial_candidate"
production_priority: 1
tags:
  - "vdn"
  - "v9"
  - "pursuit"
  - "a-verifier"
---

# Poursuite Roblox — PathfindingService, waypoints et chemins bloqués

> Procédure éditoriale candidate issue des sources listées ; aucun test Studio ni revue externe.

## Problème

pursuit

## Contexte

Roblox ; version du projet et appareils à vérifier.

## Sources

- [1] https://create.roblox.com/docs/characters/pathfinding — consulté le 2026-11-16

## Prérequis

- PNJ mobile avec Humanoid et point de départ/destination ; scène d’obstacles de test. [source 1]

## Méthode candidate

- Créer un Path avec les paramètres du gabarit du PNJ, puis calculer le chemin avec ComputeAsync sous gestion d’erreur. [source 1]
- Vérifier PathStatus.Success avant de parcourir les waypoints retournés dans leur ordre. [source 1]
- Sur un blocage pertinent signalé par Path.Blocked, recalculer un chemin ; borner les recomputations comme politique de projet à mesurer. [source 1]

## Limites connues de Roblox

- AgentRadius et AgentHeight doivent correspondre aux passages possibles ; des paramètres incompatibles empêchent le calcul. [source 1]
- La documentation décrit le chemin, pas une IA complète de perception, poursuite ou coopération. [source 1]

## Alternatives

- Hypothèse de conception à tester : séparer patrouille, détection, poursuite et recherche du joueur dans une machine à états. [proposition de conception non validée]

## Paramètres (sourcés)

- La page donne AgentRadius = 2 studs et AgentHeight = 5 studs comme valeurs par défaut, pas comme réglages recommandés pour le Père Noël. [source 1]

## Protocole de reproduction proposé, non exécuté

Tester obstacle mobile, destination inaccessible et cible déplacée ; mesurer blocages, recomputations et coût serveur. Aucun seuil universel de performance n’est déduit.

## Diagnostic

Conserver erreurs, environnement, paramètres et observations. Les causes proposées restent des hypothèses.

## Retour arrière

Revenir à un PNJ immobile ou à une patrouille sûre si la poursuite se bloque ; garder les paramètres et observations de l’échec.

## Extraits justificatifs

> « Then, in the [Properties](/docs/en-us/studio/properties.md) window, set both `Class.StarterPlayer.DevComputerMovementMode|DevComputerMovementMode` and `Class.StarterPlayer.DevTouchMovementMode|DevTouchMovementMode` to `Scriptable`. »
> — [source](https://create.roblox.com/docs/characters/pathfinding)

## Niveau de preuve

Documentation officielle consultée ; exactitude de la procédure proposée et fonctionnement dans le jeu non vérifiés.
