# Trois protocoles de laboratoire — NON EXÉCUTÉS

Statut commun : ENGINEERING_PROPOSAL. Aucun résultat Studio, Blender 5.2, B3/C1
ou lampe V2 n'a été mesuré ici. Les noms de composants/scènes ci-dessous sont
PROPOSED, pas des fichiers existants. Le contrôleur, la hiérarchie des assets,
les réglages actuels, l'appareil et le build Studio sont UNKNOWN.

Préparation humaine : copier la scène et les assets dans un fichier local distinct,
conserver les originaux, désactiver toute publication automatique et vérifier que
les scripts insérés sont ceux du laboratoire. Les sources décrivent les propriétés,
pas le résultat attendu sur ces assets. Aucune référence visuelle n'est une garantie
technique. Ne pas lancer un essai dont la variable et les contrôles sont inconnus.

## 1. Collisions B3/C1

**Hypothèse.** La représentation physique pourrait contribuer aux blocages près
des troncs/branches. Un défaut du contrôleur reste une autre hypothèse.

**Entrées.** Copies identifiées B3/C1 ; contrôleur réel ; build Studio ;
configuration/appareil ; état des propriétés et du sol. Relever chaque composant
et son rôle sans le déduire du seul nom. Documenter l'état actuel des propriétés
consultées, dont CollisionFidelity si le type de pièce l'expose.

**Sources.** Doc collisions et reçu SHA/offsets dans [DISCOVERIES](DISCOVERIES.md).
Voir aussi l'affichage des volumes documenté dans cette section, si disponible
sur le build utilisé. Les options Box/Hull/Default/PreciseConvexDecomposition
sont des alternatives documentées, aucune n'est choisie comme optimum ici.

**Témoin A.** Arbre/contrôleur/sol inchangés, propriétés sauvegardées et captures.
Marquer départ/arrivée et segments : approche du tronc, passage latéral sous une
branche, demi-tour et pente si elle reproduit le problème. Consigner action et
position pour chaque arrêt. Si le problème ne se reproduit pas, suspendre le choix
de variante, conserver ce résultat et préciser le scénario.

**Variante B.** Changer seulement la représentation physique d'un composant
identifié ; garder visuel, position, échelle, ancrage et contrôleur identiques.
La variante exacte doit être justifiée après inspection : autre fidélité autorisée
ou volume séparé préparé dans la copie. Ne pas désactiver tous les troncs pour
obtenir artificiellement zéro blocage. Garder un seul ensemble A ou B actif à la
fois pour ne pas changer la densité de la scène.

**Contrôles.** Même asset, contrôleur, appareil, résolution, qualité graphique,
caméra, éclairage, sol, trajet et actions hors variable. Noter les autres scripts
actifs et les changements involontaires. Faire plusieurs passages A/B en alternance ;
le nombre de répétitions est un choix de protocole à consigner, pas une limite moteur.

**Mesures.** Nombre de blocages définis avant l'essai, positions et actions,
composant suspect, traversées indésirables, fin de parcours possible et observations
brutes. Temps de parcours seulement sous actions comparables. Coût physique/trame
via outils Studio documentés, si disponibles ; conserver données brutes et conditions.
Un intervalle Heartbeat n'est ni FPS rendu ni coût GPU.

**Critères proposés à approuver avant essai.** Réduction des blocages reproduits,
aucune nouvelle traversée du tronc, aucune transition du contrôleur cassée. Définir
le compromis physique/performance avec l'appareil réel ; aucun seuil FPS arbitraire.
Aucune amélioration annoncée si les conditions diffèrent ou le témoin ne bloque pas.

**Risques/arrêt.** Arrêter si le joueur traverse le tronc, si le contrôleur diverge
ou si le visuel/sol a changé. Conserver les cas d'échec, ne pas les effacer.

**Rollback.** Restaurer les propriétés/copies témoins, désactiver le candidat dans
le laboratoire, conserver captures et fichiers A/B. Ne pas remplacer le jeu publié.

## 2. Sapins enneigés réalistes

**Hypothèse.** Une variation de silhouette OU de feuillage OU de répartition de
neige pourrait améliorer le rendu perçu. Pas de méthode gagnante présumée.
Sources : notes de végétation et anciennes recettes V10, références PBR officielles
SurfaceAppearance déjà acquises. Les détails artistiques non documentés restent
EXPERIMENTAL. Aucune transcription vidéo ni shader Unreal transféré implicitement.

1. Inventorier B3/C1 réels : géométrie, cartes/UV, matériaux, dimensions et options
   d'export. Relever Blender 5.2/build réel si Blender intervient ; ne pas substituer
   la capture de manuel Blender 5.3 à une preuve 5.2.
2. Capturer A avec les mêmes vues de près, de loin et silhouettes à la lampe.
3. Choisir une seule variable, conserver le reste : irrégularité de distribution,
   représentation du feuillage ou répartition de neige, jamais les trois ensemble.
4. Préparer B sur copie. Garder transformation, textures/lumière/caméra, échelle,
   collisions et densité fixes hors variable. Conserver l'export A.
5. Comparer mêmes images/trajectoires. Faire annoter humainement répétition,
   silhouette, platitude, ombres et neige. L'avis esthétique est séparé du profilage.
6. Mesurer triangles dans l'outil adapté, nombre d'objets et coût de trame si
   réellement accessibles ; conserver l'outil, ses versions et les données brutes.

Critères proposés : défaut visuel ciblé réduit selon revue humaine sous mêmes vues,
pas de régression de déplacement et coût compatible avec l'objectif préalablement
choisi. Risques : transparence, ombres, export, coût et répétition toujours visible.
Rollback : remettre la copie et l'export A, garder les échecs. Sans assets/images,
ce protocole reste non exécuté et aucune analyse visuelle n'est revendiquée.

## 3. Lampe torche V2

**Hypothèse.** Un facteur du faisceau ou de la lumière pourrait améliorer la
lisibilité nocturne, indépendamment d'un défaut du matériau ou de la caméra.
Source : documentation light-sources, section SpotLight, capture antérieure ;
version Studio inconnue. Les propriétés réellement présentes sont à inventorier.

1. Copier V2 et son code, identifier composants de lumière et mouvement de caméra.
   Sauvegarder les valeurs actuelles. Aucun composant interne n'est supposé ici.
2. Fixer arbres, sol, caméra, exposition, appareil, trajet et qualité. Capturer A
   au bord du faisceau, sur les branches et le sentier, immobile puis en mouvement.
3. Choisir un seul facteur documenté réellement exposé : bord du faisceau,
   intensité, portée, couleur ou ombre. Consigner valeur A et valeur B proposées,
   sans présenter une valeur comme optimale. Laisser brouillard et autres facteurs
   fixes ; un essai brouillard serait une comparaison séparée.
4. Rejouer les vues et mouvements identiques. Recueillir séparément lisibilité,
   continuité du faisceau, stabilité, défauts et coût de trame si mesurable.
5. Comparer avec les critères visuels/performance approuvés avant essai. Ne pas
   déclarer un gain global si une meilleure image coûte davantage sans compromis validé.

Risques : visibilité dégradée, ombres instables, coût ou confusion effet caméra/
lumière. Rollback : remettre V2 témoin et ses paramètres, sans édition du jeu réel.

## Registre de résultats commun

Conserver pour chaque A/B : question, source, méthode, versions/builds, appareil,
asset et version de fichier, contrôleur, variable, contrôles, parcours, répétition,
mesures brutes, observation humaine, erreur, décision et justification. Les valeurs
inconnues restent null/UNKNOWN. Enregistrer un résultat seulement après exécution.

Les CLI existants `agent.v10 create/configure/transition/artifact/result` et les
outils MCP prepare/start/record_experiment_result permettent de lier la tâche via
`parameters.project_task` ou `environment.project_task`. Un rapport envoyé par
client demeure non indépendamment vérifié ; la revue opérateur est distincte.
Le hash de la recette, les assets et le build doivent être liés pour une revue
READY ; ne pas déclarer équivalents deux protocoles différents.

Les échecs ne sont pas supprimés. Une nouvelle expérience peut être planifiée
avec conditions différentes et justification explicite, sans effacer la première.
Le briefing conserve un blocage conservateur jusqu'à réévaluation ; aucune
réussite nouvelle ne devient automatiquement VERIFIED.

`roblox/VDNLabCollector.client.luau` est un collecteur historique **non validé dans
Studio ici**. Il exige Studio et Workspace.VDNLab=true, ne mesure pas les blocages
et ne fournit pas les FPS rendus. Ne pas l'utiliser comme substitut du parcours
manuel ni le déployer au jeu publié. Aucun nouveau script Studio n'a été exécuté.

## Enregistrer une observation réelle avec les commandes existantes

Créer le design JSON privé sous `lab/inbox/` après avoir rempli les conditions
réelles. Champs attendus par `agent.v10 create` : problem, technique, hypothesis,
parameters, environment, references (liste d'URL), protocol. Lier explicitement
`parameters.project_task="collisions"`, l'asset réellement testé, sa version,
le build et la variable A/B. Conserver le design A séparé du design B. Aucun
fichier prérempli n'est fourni comme si ces conditions avaient été observées.

```powershell
$record = (& $python -m agent.v10 create --input .\lab\inbox\collision-design.json --apply | ConvertFrom-Json)
$planned = (& $python -m agent.v10 transition $record.id PLANNED --revision $record.revision --apply | ConvertFrom-Json)
$running = (& $python -m agent.v10 transition $record.id RUNNING --revision $planned.revision --apply | ConvertFrom-Json)
# Exécuter réellement le protocole dans Studio avant les commandes suivantes.
$proof = (& $python -m agent.v10 artifact "lab/inbox/collision-observations.json" --kind external_measurement --apply | ConvertFrom-Json)
# Ajouter l'identifiant retourné à artifacts dans collision-result.json.
& $python -m agent.v10 result $record.id --input .\lab\inbox\collision-result.json
& $python -m agent.v10 result $record.id --input .\lab\inbox\collision-result.json --apply
& $python -m agent.v112 brief "collisions"
```

Le fichier résultat attend status (FAILED/PARTIAL_SUCCESS/SUCCESS selon l'observation),
metrics (mesures numériques réelles ou null), observations non vides, errors,
artifacts et limits. Un FAILED doit conserver son erreur ; aucune donnée fictive
pour remplir un champ. La première commande result simule. Le résultat appliqué
reste `not_verified`. La revue opérateur CLI est séparée et ne doit pas être
exécutée automatiquement. Consulter aussi get_experiment_context/get_experiment
pour les conditions et preuves détaillées.
