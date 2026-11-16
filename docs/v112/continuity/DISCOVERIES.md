# Techniques candidates et nouveauté réelle

Aucune nouvelle recherche Internet, aucun modèle et aucun résultat moteur dans
cette mission. Réutilisation des 99 notes et des captures antérieures accessibles.
KNOWN = déjà présent dans ce corpus ; NEW_TO_PROJECT exige une recherche de
précédent et une source ; EXPERIMENTAL = adaptation proposée, non validée.
Ces labels ne prétendent pas connaître les conversations inaccessibles.

| Candidat | Catégorie | Lacune et source | Application / mesure / risque |
|---|---|---|---|
| Inspecter CollisionFidelity et visualiser les volumes | KNOWN | Doc officielle Roblox collisions, section Mesh and solid model collisions ; original complet et SHA/offsets vérifiés | Comparer volumes et blocages sur B3/C1. Une fidélité supérieure n'est pas automatiquement préférable ; coût et géométrie réels inconnus |
| Tester une autre représentation physique sur copie | KNOWN pour la proposition ; EXPERIMENTAL sur B3/C1 | Alternatives déjà dans la recette collisions et la mémoire historique | Garder le visuel, changer un facteur, même parcours ; risque de collisions manquantes ou nouvelles zones bloquantes |
| Distinguer CanCollide et événements de contact | KNOWN | Même documentation officielle, section Collision events | Inventorier les valeurs réelles et le contrôleur ; ne pas diagnostiquer un blocage à partir de Touched seul |
| Géométrie/foliage cards et silhouette irrégulière | KNOWN ; adaptation EXPERIMENTAL | Notes végétation et protocole V10 existants ; sources de notes secondaires | Comparaison de silhouette et ombres sur copies ; aucune supériorité, licence d'assets ou compatibilité B3/C1 démontrée |
| SurfaceAppearance pour les cartes PBR réellement disponibles | KNOWN | Capture officielle surface-appearance déjà présente ; références dans fiche trees | Inventorier cartes/UV avant un changement ; coût et effet nocturne restent à mesurer |
| Isoler un facteur de lumière de la lampe | KNOWN ; réglage EXPERIMENTAL | Capture officielle light-sources, section SpotLight ; recette V11.2 lighting | Même trajet/caméra/exposition ; avis humain séparé des mesures de trame ; pas de valeur optimale Range/intensité/couleur inventée |

**NEW_TO_PROJECT démontré : aucun.** Ne pas fabriquer une découverte pour satisfaire
un compteur. Le bénéfice actuel est la mise en relation d'une lacune concrète,
d'une référence vérifiable et d'un essai réversible.

## Preuve principale disponible

URL : https://create.roblox.com/docs/workspace/collisions
Document : `doc-5f3a3ec51a5ae0f501ba508e`
SHA256 : `747a2e5da95efc80c71bc388431ac02f38a90e1b04db31170928212f1903a9d3`
Section : Mesh and solid model collisions.
Passage contrôlé : offsets caractères **21379:21982**, identifiant
`pass-a74cb8fc1f2efb214b5ef087`. Le contrôle compare le texte du passage au
snapshot, son SHA et ses offsets ; voir `field-software.json`.

Ce passage documente le rôle de CollisionFidelity dans l'alignement des limites
physiques avec la représentation visuelle. La section suivante énumère Box,
Hull, Default et PreciseConvexDecomposition et leurs compromis. Ces noms sont
observés dans l'original, pas inventés ni recommandés comme valeurs idéales.
Version Studio et applicabilité aux assets utilisateur : UNKNOWN.
Date du snapshot antérieur : 16 novembre 2026 ; pas de nouvelle visite ici.

Les originaux complets restent dans le laboratoire privé. Le clone distribue des
reçus et références secondaires. Un clone sans originaux doit s'abstenir sur les
faits actuels ; il peut encore préparer un essai d'ingénierie signalé comme tel.

## Comparaison selon cinq dimensions

| Dimension | Verdict | Motif |
|---|---|---|
| Exactitude | PARTIEL | Attribution SHA/offsets correcte pour l'original ; version/compatibilité moteur non attestées |
| Pertinence | PARTIEL | Fidélité des collisions répond à une hypothèse du problème, diagnostic B3/C1 non reproduit |
| Nouveauté | KNOWN | Déjà présent dans le corpus ; aucune découverte nouvelle prouvée |
| Applicabilité | PARTIEL | Brief/protocole disponibles ; inspection des assets et contrôleur nécessaire |
| Résultat réel | NON TESTÉ | Aucun accès Studio ni comparaison B3/C1 |

Comparaison V11.1/V11.2 : le benchmark antérieur à sept tâches est conservé dans
`../benchmark.json` et `../BENCHMARK.md`, avec le même corpus pour A/B. Il mesure
identité/structure/taille, pas une amélioration de jeu ou un quota Claude. Aucun
nouveau benchmark modèle artificiel n'est ajouté pour cette mission.
