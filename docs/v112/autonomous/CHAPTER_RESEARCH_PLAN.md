# Recherche anticipée par scène

`agent.chapters.Chapters` relie acte → chapitre → scène → tâches partagées →
dépendances → préparation de session → protocoles. Sept scènes et vingt tâches
techniques, sans dupliquer une fiche par scène. Le focus opérationnel proposé
est la forêt du chapitre 1 ; il ne décide pas du périmètre de bêta.

Horizon A : chapitre sélectionné. B : dépendances du chapitre suivant. C : veille
seulement. Les tâches B/C ne sont pas lancées automatiquement. Les priorités P0/P1
recherchées sont distinctes des tâches P2 de réalisme et P3 reportées. Un prérequis
technique peut hériter de l'urgence sans changer sa priorité de gameplay.

| Scène | Préparation principale |
|---|---|
| prologue-home | post-it rapporté, guidage, audio, interactions |
| prologue-forest | sapins, sol, collisions, lampe, sprint, poursuite, audio |
| lobby-hub | groupes/transitions, sauvegarde, guidage, décor |
| chapter1-arrival | mains/viewmodel, caméra, audio, guidage, lampe |
| chapter1-forest | végétation/sol, collisions, caméra/mouvements, interactions, performance |
| chapter1-house | architecture, clé/fenêtre/interactions, progression, attaque/audio |
| chapter2-attic | blockout, matériaux, lumière, poussière P2, cadenas/interactions, énigmes, audio |

```powershell
& $python -m agent.v112 chapters chapter1
& $python -m agent.v112 chapters chapter2
& $python -m agent.v112 brief "Nous commençons le chapitre 2 : grenier, poussière, cadenas et énigmes"
& $python -m agent.v112 chapter-prepare chapter2
$goal = (& $python -m agent.v112 chapter-prepare chapter2 --apply | ConvertFrom-Json)
```

Le chapitre 2 propose sept tâches P0/P1 dans la session : interactions, guidage,
matériaux, lumière, architecture, audio, puzzles. La poussière reste P2, visible
au plan et dans le détail ; elle n'est pas lancée avant les prérequis. Maximum
12 tâches par plan, deux tentatives de contenu par unité, mêmes budgets V10.

La préparation ne collecte rien. Le tick appliqué exige configuration réseau et
`--allow-network`, conserve robots, quotas, erreurs et checkpoints. Une modification
de la Bible ou du catalogue arrête la reprise avec PROJECT_CHANGED, sans changer
les anciens compteurs. Pause/reprise/arrêt passent par les commandes et outils
existants. La complétude de file n'est pas la validation d'une scène.

Les tâches possèdent identifiants, objectifs, requêtes/ancres, priorité, sources
candidates, dépendances, conditions, coût borné et prochaine action. Les scènes
conservent leurs actions joueur, éléments existants rapportés et statut narratif.
Les expériences restent dans LabStore ; leur absence n'est pas une réussite.
