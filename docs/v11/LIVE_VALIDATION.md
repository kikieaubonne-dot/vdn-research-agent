# Validation réelle, séparée des fixtures

## Internet : collecte effectivement exécutée

16 novembre 2026, laboratoire privé isolé du clone et des données Windows.
La connexion directe épinglée n'était pas disponible dans l'environnement Cloud.
Le test a explicitement autorisé son proxy système et son autorité de certificat,
sans désactiver TLS. La configuration livrée reste en connexion directe.

La session `ae390b30-b9c5-403d-b9ad-e8d7c20371d0` a conservé ses quatre ticks et
**10 réservations HTTP**, y compris erreurs initiales. Trois documents Roblox
ont été réellement lus et mis en cache : collisions, SurfaceAppearance et
`https://create.roblox.com/docs/performance-optimization/improve.md`, découvert
par lien, hors des deux seeds. Robots a été demandé. Cela a produit une candidate
collisions avec un extrait exact de la page performance et un protocole de
comparaison troncs/branches/proxies/controller non exécuté dans le jeu.

Le probe de développement a rencontré une incompatibilité Python 3.12 du
transport, des refus de connexion directe et trois images 404 avant correction.
Les réservations et échecs sont conservés. Pendant ce développement, les liens
d'images ont été retirés des métadonnées du cache privé et des alternatives
approuvées ajoutées à l'unité épuisée ; aucun texte source, SHA ou compteur
n'a été réinitialisé. Le code livré filtre les assets et ajoute ces alternatives
sous verrou. Il ne s'agit donc pas d'un parcours vierge parfait avec les
réglages réseau par défaut.

[Bilan brut](live-research.json), [trace de métadonnées](live-web-trace.jsonl).
La trace garde l'ID du prototype initial `536271fc132120ff7ee2` ; la recette
d'identité finale inclut l'empreinte de source :
[`vdn-ocean-54fe16e8e5a3e6ea5304`](../../knowledge/ocean/vdn-ocean-54fe16e8e5a3e6ea5304.md).
La même preuve a été rendue avec le schéma final ; aucune affirmation n'est
devenue vérifiée. Le document performance était tronqué à 32 Ko ; version et
date de publication restent inconnues.

## Deuxième objectif et mémoire

Objectif `5b2db71c-5920-4492-b1f5-415081a6872a`, même laboratoire, aucune remise
à zéro : une unité collisions réutilisée, une acquisition logique évitée.
Le compteur journalier passe de **10 à 11 HTTP**. La collecte produit réellement
une [candidate feuillage/transparence](memory-candidate.md) sur SurfaceAppearance,
puis une unité géométrie ne trouve pas de passage pertinent parmi les deux
documents tentés. État final **ERROR**, dix unités en attente, zéro `running`.

Le bilan de la dernière unité indique zéro création ; la reconstruction en
lecture seule du tick complet donne **1 création, 3 documents obtenus dont
2 rejetés, 1 accepté, 1 erreur**. La nouvelle sortie `last_summary.collection`
évite cette ambiguïté ; son test reproduit création puis erreur. Ni ERROR ni
une tentative HTTP ne sont qualifiés de réussite. La fiche de cette seconde
recherche est livrée comme preuve dans `docs`, sans enrichir artificiellement
le corpus du benchmark. [Résultat complet](memory-live.json).

## Expériences et intégrations

Blender 4.3.2 réellement exécuté en processus background et profil temporaire :
deux géométries, **42 et 58 triangles**, rapports importés et comparaison sous
conditions identiques. [Rapport](blender-isolated/comparison.json).

MCP stdio réellement lancé par les tests ; conflits/rollback Obsidian vérifiés
dans des destinations temporaires avec données contrôlées. En complément,
l'export du corpus actif réel de 111 notes vers un coffre isolé a écrit
**125 fichiers**, sans conflit ; une seconde simulation constate **125 inchangés**.
[Bilan de cet export](obsidian-real.json), laboratoire privé exclu.
Le coffre Windows personnel,
Claude Desktop, Roblox Studio, B3/C1 et Blender 5.2 étaient indisponibles.
Ollama indisponible : aucune analyse IA ni embedding réel. Aucune dépense API.
