# Lacunes prioritaires et utilité pour la sortie du jeu

Inventaires complets : `v9/gaps_before.json` et `v9/gaps_after.json`. Chaque fiche
a neuf dimensions séparées : pertinence à la tâche, qualité des sources, fraîcheur,
compatibilité, couverture, reproductibilité, vérifiabilité, utilité et incertitude.
La fraîcheur distingue l'âge de collecte d'une version logicielle réellement vérifiée.
Aucune probabilité ni score de vérité n'est inventé.

| Production | Besoin | Constat et action |
|---|---|---|
| P0 | Sauvegardes / progression | Aucune référence spécifique avant V9 ; nouvelle candidate DataStore avec prérequis, annulation, gestion d'erreur et protocole proposé |
| P0 | Frontière client/serveur | Références initiales trop générales ; nouvelle candidate de validation serveur, entrées malformées et nombres non finis |
| P0 | Collisions / performance | Références présentes, mais protocole de parcours, collisions réelles et budget appareil non établis ; reste prioritaire |
| P1 | Poursuite du Père Noël | Nouvelle candidate de navigation ; perception, états et limites de recomputation restent des décisions à tester |
| P2 | Rigging / animation | Glitches RootPart/bones documentés mais cause et correction non prouvées dans le projet |
| P3 | Forêt / neige / éclairage | Corpus déjà plus riche ; pas de raison de multiplier les recherches avant de stabiliser le gameplay |
| P4 | Bonnet / sacoche | Une candidate officielle clarifie rigide/layered et attachments ; multijoueur et rig personnalisé restent non vérifiés |

Les priorités **de production** ne remplacent pas les P0/P1 d'ingénierie du logiciel.
Le classement est explicable : ordre de production, puis nombre de dimensions
manquantes, sans estimation chiffrée de probabilité d'utilité. Les protocoles
éditoriaux proposés sont distingués de tests exécutés et des extraits littéraux.

L'inventaire continue à signaler versions et reproduction dans le projet pour
chaque tâche. Il ne conclut pas qu'une lacune est résolue parce qu'une fiche vient
d'être ajoutée. Certaines contraintes françaises proposées ne sont pas reconnues
comme contraintes littérales par l'ancien extracteur V7 ; ce diagnostic reste
conservateur, distinct de l'affichage de la procédure candidate complète.
