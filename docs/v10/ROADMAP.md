# Après validation des fondations V10

## V11 — laboratoire connecté

Conditions d’entrée : revue de la PR V10, tests Windows réellement passés,
premier protocole sapin exécuté manuellement et preuves inspectées. Priorités :

1. Valider puis instrumenter le collecteur dans la version Studio installée,
   avec refus explicite de tout place de production et identifiant de laboratoire.
2. Relier les runs à versions/assets/appareils, captures contrôlées et répétitions ;
   mesurer rendu et GPU avec les outils Roblox adaptés, pas par Heartbeat.
3. Ajouter un connecteur local avec authentification, journal et consentement
   par expérience ; conserver une voie d’import manuelle de secours.
4. Importer des mesures Blender réelles, notamment triangles et exports, puis
   comparer A/B sur des conditions identiques et des objectifs fixés d’avance.
5. Évaluer un modèle multimodal réel sur des images annotées et un budget matériel
   connu avant de recommander une configuration ou de prétendre comprendre une scène.

V10 ne développe ni n’active ces connecteurs. Le premier résultat utile peut être
un échec documenté et réutilisable, sans promotion de statut automatique.

## V12 — production assistée

Après preuves V11 : assistants spécialisés assets, vêtements, rigging, animation
et optimisation, chacun évalué sur cas reproductibles. Propositions d’édition
de code/assets dans des copies isolées, validation humaine avant application,
comparaison avec l’état initial et rollback. Les sous-agents n’auront pas de droit
de déploiement implicite. Mesurer taux de reprise correcte, réutilisation de
solutions sous mêmes conditions et temps humain par tâche avec protocole explicite.
Les gains de production ne seront déclarés qu’après ces mesures.
