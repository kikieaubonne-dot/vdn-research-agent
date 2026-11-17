# Bible — Le Voisin de Noël [Horreur]

Source : contexte utilisateur V11.2. CONFIRMED décrit une intention rapportée, pas un test moteur.
Révision : 3 ; empreinte : `1bf923d5e88d05b74358f71338e14f817906c9a87d452bfdb12e814ffed25348`.

## vision

- **CONFIRMED** — Le Voisin de Noël [Horreur], jeu Roblox d’horreur cinématographique, infiltration et exploration à la première personne.

## art

- **CONFIRMED** — Nuit de Noël enneigée, tension, obscurité et réalisme cinématographique dans les limites réelles de Roblox.
- **CONFIRMED** — Lampe torche centrale, éclairage nocturne, neige tassée et traces de pas crédibles comme cibles visuelles.

## environments

- **CONFIRMED** — Forêt nordique d’épicéas, silhouettes naturelles, sentier forestier et brouillard léger comme cible artistique.
- **CONFIRMED** — Rue enneigée, maisons, manoir, maison de Noël et intérieurs font partie du contexte fourni ; leur disponibilité dans le dépôt est inconnue.

## visual_references

- **CONFIRMED** — Références étudiées : Alan Wake 2, The Last of Us Part II, Resident Evil Village et promenades nocturnes en forêt nordique. Aucune équivalence technique Roblox garantie.

## gameplay

- **PROPOSED** — Marche, sprint, accroupissement, glissade, enjambement et escalade sont étudiés ; aucune liste de fonctionnalités de bêta confirmée.
- **PROPOSED** — Cachettes, interactions, indices, énigmes, poursuites et événements scénarisés sont étudiés, pas tous obligatoires.
- **CONFIRMED** — Lobby souhaité avec groupes de 1 à 4, difficultés Facile/Normal/Difficile/Cauchemar ; Cauchemar déverrouillé après Difficile, indices futurs acte 2.

## development

- **PROTOTYPE** — Sapin B3 et jeune sapin C1 signalés par l’utilisateur ; fichiers et état de validation non inspectés.
- **PROTOTYPE** — Lampe torche V2 signalée ; comportement, fichiers et mesures non disponibles dans ce dépôt.
- **PROTOTYPE** — Caméra immersive à améliorer, d’après le contexte utilisateur ; aucun défaut Studio reproduit ici.
- **PROTOTYPE** — Sol enneigé et traces de pas signalés ; mesures et assets non inspectés.
- **PROTOTYPE** — Pipeline Blender vers Roblox étudié ; compatibilité des exports réels à vérifier.
- **PROTOTYPE** — Post-it animé des parents déjà créé selon l’utilisateur ; fichier et exécution non inspectés.
- **CONFIRMED** — Problème de première bêta rapporté : joueurs perdus, trop de liberté et indices simultanés ; aucune télémétrie fournie.

## characters

- **DEFERRED** — Sonia, personnage réaliste, est un chantier secondaire ; sa présence dans la bêta n’est pas confirmée.
- **CONFIRMED** — Maëlle est la petite sœur de Léo ; dans le prologue elle croit entendre le Père Noël et part vers la forêt.
- **CONFIRMED** — Le Père Noël est une menace du prologue et attaque le policier au chapitre 1, selon le récit fourni.
- **CONFIRMED** — Léo, petit garçon, est le personnage jouable du prologue.
- **CONFIRMED** — Le policier devient jouable pendant la phase E du prologue ; le chapitre 1 déjà prévu reste à articuler avec cette transition. Gants, lampe et tenue tactique restent des objectifs de présentation.

## story

- **CONFIRMED** — Prologue : Léo à la maison, départ de Maëlle, poursuite, disparition, confrontation, appel à la police puis enquêteur jouable. Fin exacte UNKNOWN ; lobby et chapitre 1 conservés, articulation finale à confirmer.
- **UNKNOWN** — Fin exacte du prologue non approuvée. Mystère vers manoir, apparition ou indice anormal sont des propositions séparées.

## chronology

- **CONFIRMED** — Ordre humain confirmé A maison → B poursuite → C recherche/confrontation → D appel → E enquêteur. Fin F non choisie ; aucune date narrative inventée.

## controls

- **CONFIRMED** — Première poursuite : seulement sprint Shift si nécessaire ; aucun apprentissage imposé de glissade, accroupissement, escalade ou enjambement. Apprentissage approfondi dans la phase enquêteur. Manette/tactile UNKNOWN.

## performance

- **UNKNOWN** — Appareils Roblox cibles, résolution, budgets de trame et FPS cible ne sont pas confirmés.

## technical

- **CONFIRMED** — Outils du projet : Roblox Studio, Blender 5.2, Unreal comme référence/atelier artistique, Claude Desktop/MCP, Obsidian ; Ollama facultatif.
- **CONFIRMED** — PC utilisateur annoncé : RTX 4060 Ti 8 Go. Aucune disponibilité de ce GPU dans l’environnement CI n’est supposée.

## priorities

- **PROPOSED** — P0 fonctionnement indispensable ; P1 horreur essentielle ; P2 amélioration non bloquante ; P3 reportable. Classement des tâches proposé et révisable après validation du scénario.
- **PROPOSED** — Hypothèses de design à tester : contrôle <10s, interaction <30s, mystère <60s, pas de cinématique non interactive >20s, durée cible 7–9min. Aucun résultat joueur mesuré.

## dependencies

- **PROPOSED** — Rechercher les prérequis techniques qui débloquent P0/P1 sans bloquer les recherches indépendantes sur des décisions narratives.

## deferred

- **DEFERRED** — Extension à un assistant universel, installation de modèles et automatisations permanentes hors de cette préparation.
- **DEFERRED** — Mode où un joueur incarne le Père Noël après la sortie initiale ; afficher Bientôt disponible, ne pas développer maintenant.

## Questions non résolues

- **CONFIRMED** — Quel personnage est jouable dans la première version ? Réponse : Léo dans les phases A–D du prologue ; policier enquêteur jouable dès la phase E du prologue, puis chapitre 1 déjà prévu. Autres rôles et portée de bêta à confirmer.
- **CONFIRMED** — Quelle est la motivation et l’objectif immédiat du joueur ? Réponse : Léo surveille Maëlle, la suit, recherche sa sœur disparue, échappe à la menace puis signale sa disparition. Phase E : le policier enquête dans la forêt ; suite et fin F non approuvées.
- **UNKNOWN** — Quelle séquence jouable doit être terminée pour la bêta ?
- **UNKNOWN** — La première version est-elle solo ou coopérative ?
- **UNKNOWN** — Quels appareils et budgets de performance doivent être validés pour la bêta ?
- **UNKNOWN** — Quels personnages doivent réellement apparaître dans la bêta ?

## Priorités et dépendances — proposées

- trees : P1 (PROPOSED) ; prérequis : export, materials
- collisions : P0 (PROPOSED) ; prérequis : aucun lien de dépendance imposé
- ground : P1 (PROPOSED) ; prérequis : aucun lien de dépendance imposé
- lighting : P1 (PROPOSED) ; prérequis : aucun lien de dépendance imposé
- camera : P0 (PROPOSED) ; prérequis : aucun lien de dépendance imposé
- movement : P0 (PROPOSED) ; prérequis : aucun lien de dépendance imposé
- interactions : P0 (PROPOSED) ; prérequis : aucun lien de dépendance imposé
- performance : P1 (PROPOSED) ; prérequis : aucun lien de dépendance imposé
- architecture : P1 (PROPOSED) ; prérequis : aucun lien de dépendance imposé
- pursuit : P1 (PROPOSED) ; prérequis : aucun lien de dépendance imposé
- export : P2 (PROPOSED) ; prérequis : aucun lien de dépendance imposé
- materials : P2 (PROPOSED) ; prérequis : aucun lien de dépendance imposé
- animation : P2 (PROPOSED) ; prérequis : export
- viewmodel : P1 (PROPOSED) ; prérequis : camera
- audio : P1 (PROPOSED) ; prérequis : aucun lien de dépendance imposé
- guidance : P0 (PROPOSED) ; prérequis : aucun lien de dépendance imposé
- saves : P0 (PROPOSED) ; prérequis : aucun lien de dépendance imposé
- groups : P1 (PROPOSED) ; prérequis : saves
- puzzles : P1 (PROPOSED) ; prérequis : interactions, guidance
- dust : P2 (PROPOSED) ; prérequis : lighting
