# Inventaire typé — état de référence V11.2

Lecture du dépôt au commit de référence 72f1b9c, des modifications locales
préservées et du précédent laboratoire explicitement accessible. Les données
complètes et les chemins/pointeurs des occurrences sont dans [inventory.json](inventory.json).
Ne pas additionner définitions, références, empreintes et index comme des fiches.

| Catégorie dans le dépôt | Nombre unique | Nature |
|---|---:|---|
| Fiches admises avec ID | **99** | 25 candidat, 32 documente, 42 rejete |
| Markdown knowledge | **111** | 99 fiches +12 pages d'index/structure |
| URL citées par les notes | 99 | 100 occurrences ; pas 99 visites vérifiées |
| Références de fiches du registre URL | 94 | Sous-ensemble des notes, pas 94 notes supplémentaires |
| Empreintes du registre historique | 393 | Empreintes de contenu, pas sources indépendantes |
| Documents de citations secondaires | 369 | Dérivés des notes |
| Passages secondaires | 369 | IDs propres aux passages dérivés |
| Snapshots originaux dans le runtime du dépôt | **0** | Absents d'un clone normal |
| Cartes de préparation publiques | 10 | Archives secondaires, 4 PARTIAL et 6 BLOCKED |
| Analyses privées référencées par ces cartes | 10 | Fichiers non distribués dans le dépôt |
| Documents originaux référencés dans l'archive | 8 | 11 références au total, métadonnées uniquement |
| Passages référencés par les sources des cartes | 11 | Pas des originaux embarqués |
| IDs de claims archivés | 47 | 50 occurrences, réutilisation entre tâches possible |
| Tâches du projet | 13 | 10 thèmes initiaux + export, matériaux, animation |
| Éléments de Bible | 25 | Namespace items |
| Questions de Bible | 6 | Toutes sans réponse confirmée |
| Groupes de Bible | 5 | Namespace groups |
| Référence visuelle déclarative de Bible | 1 | Aucune image réelle jointe |
| Élément reporté de Bible | 1 | Namespace deferred |
| Outils MCP V11.2 | **27** | Définitions de contrats, pas connaissances |
| Unités de file globale | 93 | IDs de recherches persistantes, pas sessions |
| Entrées seen V5 | 54 | Registre historique séparé |
| Sessions privées présentes dans le dépôt | 0 | Runtime non distribué |
| Expériences privées présentes dans le dépôt | 0 | Ne pas confondre exemples JSON et expériences |
| Modules agent analysés | 67 | Définitions, imports et SHA dans le JSON |

## Anciennes valeurs « 99 fiches » et « environ 150 IDs »

**99 fiches est vérifié** pour V11, V11.1 et V11.2. Ce total inclut les notes
rejetées ; il ne désigne pas 99 techniques validées dans Roblox.

| Référence Git locale accessible | Markdown | IDs de fiches uniques |
|---|---:|---:|
| main | 100 | 89 |
| V7 | 106 | 94 |
| V8 | 106 | 94 |
| V9 | 110 | 98 |
| V10 | 110 | 98 |
| V11 | 111 | 99 |
| V11.1 d23aafa | 111 | 99 |
| V11.2 72f1b9c | 111 | 99 |

Les SHA exacts, IDs ajoutés/retirés entre références listées et doublons sont
publiés dans le JSON. Il s'agit de références Git locales inspectées, pas d'une
assertion de fusion sur main. Les PR #7/#8 restent ouvertes.

La discussion évoquant 150 IDs n'est pas accessible. Aucun registre vérifié de
« 150 fiches » n'a été trouvé. Il existe de nombreuses catégories d'IDs ; une
somme accidentelle de catégories ne prouverait pas ce que désignait la discussion.
Ce point reste **NON ÉTABLI**.

## Doublons, intégrité et références manquantes

- Aucun ID de fiche défini deux fois ; aucun contrat MCP dupliqué.
- 94 références registry → note/path résolues ; aucun lien wiki non résolu dans
  le périmètre du dépôt inspecté.
- Répétition de claims/documents dans les préparations : références partagées,
  pas nouvelles preuves indépendantes.
- Les dix références d'analyse et les reçus sources de l'archive ne sont pas
  livrés comme runtime primaire : absence attendue, explicitement signalée.
- Les URL distantes ne sont pas revérifiées par cet inventaire hors ligne.
- Les occurrences génériques de clés JSON sont classées par fichier/pointeur.
  Les fixtures et rapports ne deviennent pas des définitions de production.

## Ancien laboratoire isolé — périmètre distinct

Le laboratoire de la collecte précédente contient **11 fichiers cache**,
**10 documents originaux uniques**, **664 passages originaux**,
**1 session** (`52974000-e519-42d0-a653-01fc97e89a60`), **30 révisions de cartes**,
**20 analyses** et **0 expérience**. Le cache canonique identique en double est
conservé physiquement et dédupliqué à la lecture. Ce laboratoire n'est pas le
runtime du clone ni celui du PC Windows. Les expériences synthétiques créées
pour cette mission vivent dans une nouvelle copie, hors de ces deux périmètres.

## Reproduction

```powershell
& $python -m bench.inventory_v112 --output C:\lab\inventory.json
# Facultatif : lecture d'un ancien laboratoire explicitement choisi
& $python -m bench.inventory_v112 --runtime C:\lab\ancien-laboratoire --output C:\lab\inventory-with-runtime.json
```

Exécuter depuis la racine du dépôt avec Git installé. Aucun socket, modèle ou
compteur modifié. Les résultats de la présente mission sous docs/v112/continuity
sont exclus des entrées pour éviter qu'un inventaire réinventorie ses propres
occurrences. Le JSON inclut le SHA de référence et ceux des modules analysés.
