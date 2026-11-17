---
id: "vdn-c2b-trunk-colliders-h001-h002"
title: "Collisions sapin C2B H001 H002 — cylindres de tronc A B1 B2 B3"
domain: "forest"
subdomain: "collisions"
status: "candidat"
tested_in_studio: "non"
confidence: "faible"
confidence_reason: "Procédure et seuils expérimentaux ; observations initiales rapportées par Claude, essais A/B à exécuter."
engine_version: "Roblox Studio build UNKNOWN ; place de référence v655 rapportée par Claude"
source_tier: 1
official: false
sources:
  - "https://create.roblox.com/docs/reference/engine/classes/BasePart"
  - "https://create.roblox.com/docs/reference/engine/classes/Part"
  - "https://create.roblox.com/docs/reference/engine/enums/CollisionFidelity"
  - "https://create.roblox.com/docs/physics/units"
accessed: "2026-11-17"
created: "2026-11-17"
updated: "2026-11-17"
procedure_origin: "source_based_editorial_candidate"
editorial_steps:
  - "Sur la COPIE locale identifiée (pas seulement IsStudio/PlaceId), conserver A intacte et créer B1/B2/B3 indépendantes. Aucune publication ou modification de la place principale."
  - "Figer4pins P1-P4 et4épicéas E1-E4 accessibles ; exclure semis enterrés et cibles non mesurables. Préserver les144volumes, contrôleur, caméra, lampe, feuillage et neige."
  - "Mesurer terrain local, axe, rayon visuel du tronc et rayon distinct de jupe ; garder positions/hits/incertitude. INTERDIT : déduire le rayon de MeshPart.Size ou de la boîte de branches. Les raycasts approchent aussi la collision, corroborer la silhouette."
  - "B1 :4pins, r=0.90*r_tronc. B2 :4épicéas, proxy étroit r=0.90*r_tronc (choix expérimental). B3 : les mêmes4épicéas, r=0.60*r_jupe dans55-70%. Centre, axe et hauteur B2/B3 identiques. Ne jamais cumuler les variantes."
  - "Créer seulement4Part Shape=Cylinder par variante ; Anchored/CanCollide=true, CanTouch/CanQuery=false, Transparency=1, CastShadow=false. CollisionGroup existant vérifié avec le personnage, matrice inchangée. Ne pas modifier CollisionFidelity=Default des MeshParts."
  - "Aligner axe localX du cylindre sur le tronc, Size=(H,2r,2r), centre=P0+U*H/2 ; H limité au tronc bas exposé et3m maximum (10.714studs à28cm/stud). Contrôler la forme/inclinaison dans la copie."
  - "CanQuery=false ne garantit PAS exclusion des raycasts si CanCollide=true. Comparer mêmes origines/directions de lampe/interactions et résultats A/B ; ne pas ajouter un filtre pour masquer un échec pendant le test."
  - "Effectuer>=5circuits A/B1/B2/B3 : marche, sprint, glissade et4obstacles ; filmer traversées, passages tangents, blocages et caméra contre écorce. Ne pas compter un contact volontaire contre le tronc comme blocage indésirable."
  - "Critères expérimentaux :0traversée des4troncs équipés ;0nouveau blocage>0.5s ;0régression obstacles/glissade/raycasts ;0nouvelle erreur ; surcoût médian physique<0.2ms et frame p95<0.5ms. Bruit/donnée absente=INDÉTERMINÉ."
  - "Garder CSV bruts et unités, rouvrir chaque fichier B puis refaire le contrôle ; mobile=émulateur Studio seulement. Pathfinding PNJ séparé obligatoire avant V6. Aucun résultat Blender/Python ne valide ces critères."
  - "Préparer/démarrer/enregistrer3expériences séparées B1/B2/B3, preuves importées via reçus LabStore, statuts rapportés uniquement, puis relire get_experiment_context. Ne pas envoyer le modèle de résultat non rempli."
  - "Reposer la question à L'Éponge avant/après, conserver réponses et lacunes face au corrigé H001/H002 ; revue contradictoire ChatGPT PENDING. Aucun VERIFIED ou déploiement automatique ; rollback par réouverture du témoin A."
tags:
  - "vdn"
  - "C2B"
  - "H001"
  - "H002"
  - "sapin"
  - "collisions"
  - "engineering_proposal"
---

# Collisions sapin — procédure candidate H001/H002

**NON CERTIFIÉE ; aucune variante exécutée par Codex.** Source humaine : dernières observations de Claude/Kylian. Les arbres sont rapportés non collidables ; retirer une collision de feuillage déjà désactivée est sans effet. L'Ecorce inclut des branches : Size ne mesure pas le tronc.

## Objectif
Empêcher la traversée des troncs ciblés sans régression des parcours, caméra, raycasts ou performance. Essai minimal de4pins et4épicéas, jamais546proxies.

## Étapes reproductibles — PROPOSITION D'INGÉNIERIE

1. Sur la COPIE locale identifiée (pas seulement IsStudio/PlaceId), conserver A intacte et créer B1/B2/B3 indépendantes. Aucune publication ou modification de la place principale.

2. Figer4pins P1-P4 et4épicéas E1-E4 accessibles ; exclure semis enterrés et cibles non mesurables. Préserver les144volumes, contrôleur, caméra, lampe, feuillage et neige.

3. Mesurer terrain local, axe, rayon visuel du tronc et rayon distinct de jupe ; garder positions/hits/incertitude. INTERDIT : déduire le rayon de MeshPart.Size ou de la boîte de branches. Les raycasts approchent aussi la collision, corroborer la silhouette.

4. B1 :4pins, r=0.90*r_tronc. B2 :4épicéas, proxy étroit r=0.90*r_tronc (choix expérimental). B3 : les mêmes4épicéas, r=0.60*r_jupe dans55-70%. Centre, axe et hauteur B2/B3 identiques. Ne jamais cumuler les variantes.

5. Créer seulement4Part Shape=Cylinder par variante ; Anchored/CanCollide=true, CanTouch/CanQuery=false, Transparency=1, CastShadow=false. CollisionGroup existant vérifié avec le personnage, matrice inchangée. Ne pas modifier CollisionFidelity=Default des MeshParts.

6. Aligner axe localX du cylindre sur le tronc, Size=(H,2r,2r), centre=P0+U*H/2 ; H limité au tronc bas exposé et3m maximum (10.714studs à28cm/stud). Contrôler la forme/inclinaison dans la copie.

7. CanQuery=false ne garantit PAS exclusion des raycasts si CanCollide=true. Comparer mêmes origines/directions de lampe/interactions et résultats A/B ; ne pas ajouter un filtre pour masquer un échec pendant le test.

8. Effectuer>=5circuits A/B1/B2/B3 : marche, sprint, glissade et4obstacles ; filmer traversées, passages tangents, blocages et caméra contre écorce. Ne pas compter un contact volontaire contre le tronc comme blocage indésirable.

9. Critères expérimentaux :0traversée des4troncs équipés ;0nouveau blocage>0.5s ;0régression obstacles/glissade/raycasts ;0nouvelle erreur ; surcoût médian physique<0.2ms et frame p95<0.5ms. Bruit/donnée absente=INDÉTERMINÉ.

10. Garder CSV bruts et unités, rouvrir chaque fichier B puis refaire le contrôle ; mobile=émulateur Studio seulement. Pathfinding PNJ séparé obligatoire avant V6. Aucun résultat Blender/Python ne valide ces critères.

11. Préparer/démarrer/enregistrer3expériences séparées B1/B2/B3, preuves importées via reçus LabStore, statuts rapportés uniquement, puis relire get_experiment_context. Ne pas envoyer le modèle de résultat non rempli.

12. Reposer la question à L'Éponge avant/après, conserver réponses et lacunes face au corrigé H001/H002 ; revue contradictoire ChatGPT PENDING. Aucun VERIFIED ou déploiement automatique ; rollback par réouverture du témoin A.

## Sources et limites

> « CanCollide determines whether a part will physically interact with other parts. »
> — [source](https://create.roblox.com/docs/reference/engine/classes/BasePart)

La documentation CanQuery précise que CanCollide doit être désactivé pour que CanQuery prenne effet comme exclusion. Ce point contredit une garantie de raycast fondée seulement sur CanQuery=false ; le test fonctionnel est obligatoire. Références officielles figées avec provenance dans handoff/proofs/ ; licence CC-BY4.0 Roblox/creator-docs. Les coefficients0.90/0.60,3m et budgets0.2/0.5ms sont des paramètres d'expérience, pas des réglages Roblox optimaux.

## Protocole complet, résultats et rollback

[Procédure A/B1/B2/B3 et mesures](https://github.com/kikieaubonne-dot/vdn-research-agent/blob/codex/handoff-collisions-sapin-2026-11-17/handoff/collisions_sapin/PROTOCOL.md). Le résultat réel demeure PENDING ; modèles MCP dans le même dossier, trois IDs distincts. Fermer la variante et réouvrir A pour rollback. Aucun changement du jeu principal ni promotion VERIFIED par MCP.
