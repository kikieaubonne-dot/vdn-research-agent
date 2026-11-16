# Première préparation P0/P1 — exécution réelle, résultat PARTIEL

Session isolée `52974000-e519-42d0-a653-01fc97e89a60`, le 16 novembre 2026.
La [trace HTTP](live-web-trace.jsonl) contient les requêtes réelles et statuts,
le [rapport brut](research-session.json) conserve les erreurs, budgets, anciennes
clés de cartes et recalcul hors ligne. Aucun fichier de connaissances principal
n'est ajouté par cette session. Dix préparations canoniques, pas une masse de notes.

**8 ticks, 10 HTTP /12, 13 tentatives logiques de collecte**. Sur les 10 HTTP :
1 robots réussi, 6 documents réussis, 3 réponses 404. Quatre hits cache sont
également tracés. Les robots déjà en cache ne produisent pas une nouvelle requête.
Une tentative peut lire le cache ou échouer ; ce compteur n'est pas le nombre de
HTTP. Les reprises de transport éventuelles consomment leur propre réservation.
Ici le traceur ne montre pas de retry réseau additionnel. Réseau via proxy système
explicitement reconnu et autorisé dans cette copie, TLS vérifié, aucun contournement
robots ou certificat. Ce n'est pas un essai Internet Windows.

Compteurs de la copie conservés : HTTP quotidien 14 →24, fetch 8 →21, items 7 →20.
Le budget session reste 6 HTTP/tick, 12/session, 60 secondes calcul et 12 ticks
maximum ; calcul réservé mesuré 31,17 secondes. Aucun compteur remis à zéro.
La file finale est done=8, failed=2, pending=0, running=0, skipped=1.
Le compteur historique `integration_failures=5` est conservé : deux tentatives
sans passage suffisant (défaut de classement ensuite reproduit/corrigé), puis
404 aux ticks 4, 6, 7. Le succès du dernier tick n'efface pas ces erreurs.
COMPLETE désigne l'acquisition terminale ; l'état projet reste PARTIAL.

Les caches originaux complets et les notes déjà présentes sont réutilisés avant
la collecte. Le corpus inclut une ancienne capture Blender **5.3**, tronquée,
rejetée pour la cible **5.2**. Aucune visite Blender 5.2 ni exécution Blender n'est
revendiquée. Après la correction de classement/déduplication, les dix fiches ont
été recalculées hors ligne ; le compteur HTTP reste 24 et les appels modèle 0.
Les échecs et anciennes cartes de la session n'ont pas été réécrits.

| Thème, fiche consultable | Préparation | Sources originales attribuées après recalcul | Lacune principale |
|---|---|---:|---|
| [Sapins](preparation/trees.md) | PARTIAL | 1 | B3/C1, silhouette/neige/optimisation non testées |
| [Collisions](preparation/collisions.md) | PARTIAL | 1 | Parcours contrôlé sur copies B3/C1 à exécuter |
| [Sol et empreintes](preparation/ground.md) | PARTIAL | 2 | Relief/empreintes et coût réel non validés |
| [Éclairage et lampe](preparation/lighting.md) | PARTIAL | 1 | Mesures et comparaison de la lampe V2 |
| [Caméra](preparation/camera.md) | BLOCKED | 1 | Personnage/objectif de bêta et comportement cible |
| [Mouvements](preparation/movement.md) | BLOCKED | 1 | Contrôleur, mode solo/coop et scénario à décider |
| [Interactions](preparation/interactions.md) | BLOCKED | 1 | Parcours de bêta et mode de jeu |
| [Performance](preparation/performance.md) | BLOCKED | 0 | Appareils/budgets inconnus, original tronqué |
| [Architecture](preparation/architecture.md) | BLOCKED | 2 | Séquence/scénario/layout non confirmés |
| [Poursuite](preparation/pursuit.md) | BLOCKED | 1 | Scénario, motivation, mode de jeu |

Une source peut être réutilisée pour deux tâches ; ces nombres ne sont pas un
nombre de preuves indépendantes nouvelles. L'attribution concerne un passage,
pas la validation de l'ensemble de la recette. Tous les protocoles sont
ENGINEERING_PROPOSAL, sans résultat inventé. Les versions Studio demeurent
inconnues et empêchent une compatibilité READY. Les priorités sont proposées,
les P2 export/matériaux restent des prérequis, pas une nouvelle fonctionnalité
obligatoire. Animation P2 n'a pas consommé cette session.

L'[archive](../../project/prepared.json) est disponible dans un clone propre,
via CLI, MCP ou export Obsidian. Elle contient les procédures rédigées et reçus
(URL, SHA, offsets, section, version), pas les corps originaux ni les résultats
privés d'expériences. Elle est **secondaire** : ses anciens faits ne sont pas
réaffirmés et ses sources doivent être récupérées/vérifiées avant application.
Les dix Markdown ci-dessus sont les vues de cette archive, pas des sources
indépendantes.

Prochaine action utile : fournir des copies B3/C1 et l'état du contrôleur pour
le protocole collisions ; tester la lampe V2 en scène témoin. En parallèle,
confirmer la séquence de bêta et les appareils visés pour lever plusieurs blocages.
Ne pas relancer automatiquement la session entière ni relever ses quotas.
