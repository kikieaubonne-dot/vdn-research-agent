# MISSION CODEX — L'ÉPONGE : LABORATOIRE AUTONOME, INTELLIGENCE TECHNIQUE ET RECHERCHE ANTICIPÉE POUR ROBLOX

## 0. MISSION FONDAMENTALE

Tu es l'ingénieur principal chargé de faire évoluer « L'Éponge », notre agent de recherche technique autonome pour la création du jeu Roblox « Le Voisin de Noël [Horreur] ».

**Objectif : transformer L'Éponge en une infrastructure de recherche, de sélection, d'expérimentation, de diagnostic et de mémoire technique qui permet à Claude Desktop de construire le jeu beaucoup plus rapidement, avec moins d'essais inutiles et moins de consommation de son quota.**

L'Éponge doit devenir le cerveau technique permanent du projet.

Claude doit rester principalement l'exécutant : programmation Roblox/Luau, Blender, construction des environnements, animation, intégration et correction.

L'Éponge doit :
1. Anticiper les besoins du chapitre en cours.
2. Rechercher des techniques pertinentes sur un grand nombre de sources.
3. Sélectionner les meilleures méthodes réellement applicables.
4. Vérifier les sources et les versions.
5. Éliminer les doublons et les connaissances obsolètes.
6. Organiser la mémoire technique.
7. Préparer des expériences reproductibles.
8. Exécuter elle-même les tests lorsque les outils et permissions le permettent.
9. Analyser les résultats visuels et techniques.
10. Diagnostiquer les échecs.
11. Relancer des recherches plus précises après un échec.
12. Comparer les variantes.
13. Conserver les réussites et les échecs.
14. Transmettre à Claude des briefings courts, fiables et immédiatement exploitables.
15. Continuer à améliorer la bibliothèque pendant que Claude développe le jeu.

**Le critère de réussite n'est pas le nombre de lignes de code, d'agents, de fiches ou de recherches. C'est la capacité réelle à fournir rapidement à Claude une solution techniquement pertinente, documentée et, si possible, préalablement testée.**

---

## 1. BASE EXISTANTE — À PRÉSERVER ABSOLUMENT

Dépôt :
https://github.com/kikieaubonne-dot/vdn-research-agent

PR existante :
https://github.com/kikieaubonne-dot/vdn-research-agent/pull/8

Branche :
`codex/project-intelligence-v11-2`

Dernier commit de référence vérifié :
`89c53238ae2cea9765a95f064eb5b8a54704a89d`

Commencer par relire le code, les tests, la PR et les rapports :

- `docs/v112/continuity/CONTINUITY_AUDIT.md`
- `docs/v112/continuity/INVENTORY.md`
- `docs/v112/continuity/VALIDATION_V112.md`
- `docs/v112/continuity/DISCOVERIES.md`
- `docs/v112/continuity/CLAUDE_HANDOFF.md`
- `docs/v112/continuity/ROBLOX_TEST_PROTOCOL.md`
- `docs/v112/continuity/NEXT_ACTIONS.md`
- `project/BIBLE.md`
- `project/bible.json`
- Les modules RAG, Ocean, MCP, LabStore, Obsidian, intelligence et tests associés.

État de référence :

- 27 outils MCP.
- 99 fiches techniques : 25 candidates, 32 documentées, 42 rejetées.
- 111 Markdown historiques.
- 10 cartes de préparation : 4 PARTIAL, 6 BLOCKED.
- Aucune technique du jeu déclarée READY.
- 420 tests par scénario sur Ubuntu et Windows CI.
- Mémoire des échecs vérifiée sur des cas synthétiques.
- Export Obsidian isolé testé.
- RAG lexical opérationnel ; hybride/sémantique partiellement validé.
- Recherche Web bornée existante.
- Aucun pilotage réel de Roblox Studio confirmé.
- Aucun test Blender 5.2 confirmé.
- Aucune analyse visuelle multimodale réelle confirmée.
- Aucune connexion Claude Desktop sur le PC utilisateur confirmée.
- Aucun service permanent confirmé.

**Interdictions :**
- Ne pas repartir de zéro.
- Ne pas détruire ou remplacer les anciennes données.
- Ne pas effacer les échecs.
- Ne pas fusionner les PR sans autorisation.
- Ne pas publier ni modifier le jeu de production.
- Ne pas modifier silencieusement les budgets, configurations ou fichiers privés.
- Ne pas annoncer comme fonctionnel ce qui n'a été testé que par simulation.
- Ne pas installer de modèles volumineux sans autorisation.
- Ne pas multiplier les frameworks et les agents sans nécessité.
- Préserver les 27 contrats MCP existants ; toute extension doit être rétrocompatible.

Tu peux proposer une évolution majeure, mais privilégie les améliorations incrémentales sur l'architecture actuelle.

---

## 2. BIBLE DU JEU — ORGANISATION NARRATIVE EXACTE

Nom : **Le Voisin de Noël [Horreur]**.

Genre : jeu d'horreur narratif Roblox à la première personne, environnement de Noël enneigé, réalisme visuel maximal compatible avec les contraintes du moteur et les performances ciblées.

Inspirations artistiques : Alan Wake 2, The Last of Us, Resident Evil Village et jeux AAA narratifs.

L'acte 1 correspond au jeu actuellement développé. Il comporte un prologue et plusieurs chapitres.

### PROLOGUE — Léo et Maëlle

Le joueur incarne Léo, un petit garçon, la veille de Noël.

Élément déjà créé dans le jeu : un post-it animé des parents, indiquant qu'ils sont partis chercher Mamie et demandant à Léo de surveiller sa petite sœur Maëlle.

Pendant le post-it, une voix anglaise du Père Noël retentit, dans l'esprit de « Ho, ho, ho! Merry Christmas, everyone! ».

Maëlle entend cette voix, croit avoir découvert le Père Noël, puis part dans la forêt enneigée.

La transition doit être crédible : regard par la fenêtre, clochettes ou lumière lointaine, dialogue avec Léo, puis départ de Maëlle.

Léo la suit. Elle disparaît au loin. On entend son cri, un rire inquiétant, puis le silence.

La lampe torche commence à dysfonctionner.

Le Père Noël poursuit Léo. Le joueur apprend à sprinter.

Une chute et une attaque manquée sont envisagées. Léo s'échappe vers les habitations, voit le Père Noël retourner dans la forêt, puis appelle la police.

Le prologue se termine.

### LOBBY / MENU PRINCIPAL

Après le prologue, changement vers une place/instance de lobby.

Accueil cinématographique inspiré des menus de jeux comme Call of Duty, avec un policier réaliste et un décor enneigé.

Groupes de 1 à 4 joueurs :
- Solo.
- Duo.
- Trio.
- Escouade de quatre.

Difficultés :
- Facile.
- Normal.
- Difficile.
- Cauchemar, débloqué après réussite en difficile.

Le mode Cauchemar doit contenir des indices narratifs concernant l'acte 2 futur.

Le lobby contient :
- Mode histoire.
- Progression et chapitres.
- Souvenirs permettant notamment de rejouer le prologue.
- Invitations de joueurs.
- Difficultés.
- Paramètres.
- Mode multijoueur asymétrique futur où un joueur incarne le Père Noël, verrouillé « Bientôt disponible ».

Ce mode asymétrique est prévu après la sortie initiale. Ne pas le développer maintenant.

### CHAPITRE 1 — Le policier

Le joueur incarne un policier équipé de gants, d'une lampe torche et d'une tenue tactique.

Arrivée près de véhicules de police, gyrophares et ambiance sonore.

Un marqueur discret en forme de losange guide vers la forêt.

Le joueur découvre progressivement :
- Sprint.
- Enjambement.
- Escalade.
- Saut.
- Accroupissement.
- Glissade.
- Interactions.

Le parcours forestier contient sapins enneigés, sentier non linéaire, relief, rochers, troncs, ravin ou rivière, pente et obstacles.

Le policier rejoint la maison du Père Noël, trouve une clé, tente d'entrer, puis passe par une fenêtre.

Le Père Noël l'attaque. Le policier perd connaissance et se réveille dans le grenier.

### CHAPITRE 2 — Début envisagé

Le policier se réveille prisonnier dans le grenier.

Objectif : s'échapper.

Décor souhaité :
- Grenier photoréaliste.
- Poussière visible dans la lumière.
- Rayons lunaires par la fenêtre.
- Prison ou cage crédible.
- Cadenas réaliste.
- Indices et interactions soignés.
- Ambiance sonore et lumière horrifiques.
- Énigmes compréhensibles et progression contrôlée.

Les détails non confirmés restent PROPOSED, pas CONFIRMED.

### UX ET RÉTENTION

Le jeu doit être immersif, compréhensible même pour un jeune joueur, et conserver une histoire mystérieuse et captivante.

La première bêta présentait un problème : trop de liberté dans la maison, indices disponibles simultanément, joueurs perdus et objectifs peu compréhensibles.

Rechercher des solutions de game design :
- Guidage contextuel discret.
- Objectifs simples et explicites.
- Déblocage progressif des zones.
- Indices introduits au bon moment.
- Interactions lisibles.
- Tutoriels intégrés au récit.
- Progression narrative cohérente.
- Récompenses de découverte.
- Suspense et révélations.
- Accessibilité des commandes et de l'interface.
- Mesure des points d'abandon, de confusion et de réussite.

Ne pas utiliser de mécanismes manipulateurs pour retenir artificiellement les joueurs. Privilégier la qualité de l'expérience et une rétention saine.

---

## 3. NOUVEAU SYSTÈME DE RECHERCHE ANTICIPÉE PAR CHAPITRE

Implémenter une planification hiérarchique :

ACTE → PROLOGUE / CHAPITRE → SCÈNE → FONCTIONNALITÉ → DÉPENDANCES → RECHERCHE → TEST.

Chaque scène possède :
- Objectif narratif.
- Actions du joueur.
- Éléments existants.
- P0 indispensable.
- P1 essentiel.
- P2 réalisme avancé.
- P3 finitions.
- Dépendances.
- État de développement.
- État de validation.
- Recherches nécessaires.
- Techniques disponibles.
- Résultats expérimentaux.
- Prochaines actions.

L'Éponge doit anticiper les besoins.

Horizon A : chapitre actuel, recherches approfondies.

Horizon B : chapitre suivant, préparation des dépendances.

Horizon C : chapitres futurs, veille légère.

Priorité immédiate :
1. Forêt enneigée actuellement construite.
2. Sapins B3/C1, sol, neige, collisions.
3. Lampe V2, caméra, mains, viewmodel.
4. Déplacements, animations, interactions.
5. Prologue, Maëlle, poursuite.
6. Lobby, sauvegardes, groupes.
7. Chapitre 1 et progression.
8. Préparation du chapitre 2.

Ne pas réécrire les éléments déjà créés sans diagnostic préalable.

---

## 4. OCÉAN V2 — RECHERCHE MULTISOURCE APPROFONDIE

Améliorer le système Ocean existant, pas le remplacer aveuglément.

Sources potentielles, dans le respect des accès autorisés :

### Officielles
- Roblox Creator Hub.
- Roblox DevForum.
- Documentation API Roblox.
- Roblox release notes.
- Blender Manual et documentation Python.
- Unreal Engine documentation.
- Documentation des formats FBX, glTF, PBR et outils pertinents.

### Communautés
- GitHub.
- Reddit, notamment les communautés Roblox, développement de jeux, Blender, graphisme et optimisation.
- YouTube : tutoriels, démonstrations et making-of.
- Forums techniques.
- Blogs de développeurs.
- ArtStation et portfolios avec explications techniques.
- Discussions publiques pertinentes sur les réseaux sociaux.
- Issues, pull requests et discussions de projets open source.
- Publications de créateurs et études de cas.

Ne pas considérer une plateforme comme une preuve de qualité.

### Vidéos YouTube

Lorsque l'accès est autorisé et techniquement possible :
- Chercher les vidéos pertinentes.
- Exploiter les sous-titres ou transcriptions disponibles légalement.
- Identifier les étapes techniques, paramètres et versions.
- Conserver les timestamps.
- Distinguer ce que la vidéo démontre de ce que l'auteur affirme.
- Éviter de confondre une démonstration Unreal avec une méthode directement compatible Roblox.

Ne pas contourner les restrictions d'accès, robots.txt, protections ou conditions des plateformes.

### Recherche récursive

Une recherche doit pouvoir être décomposée.

Exemple :
« Sapin enneigé réaliste Roblox »

Sous-problèmes :
- Géométrie.
- Silhouette.
- Feuillage.
- Répartition de neige.
- UV.
- Textures.
- Normal maps.
- Roughness.
- Transparence.
- Ombres.
- LOD.
- Export Blender.
- Import Roblox.
- Collisions.
- Performances.
- Animation du vent.
- Réalisme sous lampe torche.

Pour chaque sous-problème, identifier les meilleures sources et les lacunes.

Autoriser l'approfondissement récursif uniquement lorsqu'une nouvelle branche apporte une valeur mesurable.

Arrêter une branche si :
- Elle répète les mêmes résultats.
- Elle ne concerne pas Roblox.
- Elle dépasse le budget.
- Elle n'apporte aucune nouvelle information.
- Elle nécessite des ressources indisponibles.
- Sa pertinence est trop faible.

Prévoir des checkpoints, la reprise après interruption et des budgets persistants.

---

## 5. TRI, DÉDUPLICATION ET QUALITÉ DES FICHES

C'est une priorité majeure.

Améliorer le classement à plusieurs niveaux :

### Déduplication

Détecter :
- URL identiques.
- Contenus identiques.
- Paraphrases proches.
- Tutoriels reproduisant la même méthode.
- Versions successives d'une même technique.
- Résultats dérivés d'une seule source.
- Sources indépendantes apportant réellement une confirmation supplémentaire.

Ne pas supprimer une information simplement parce qu'elle ressemble à une autre : conserver les différences techniques utiles.

### Classement de pertinence

Évaluer :
- Correspondance avec la tâche.
- Compatibilité Roblox.
- Version du moteur.
- Qualité de la source.
- Preuves.
- Reproductibilité.
- Coût de mise en œuvre.
- Performances.
- Niveau de réalisme.
- Contraintes de licence.
- Date de mise à jour.
- Résultats des expériences précédentes.
- Pertinence pour le chapitre actuel.

Ne pas transformer ces scores en fausse certitude.

### Fraîcheur

Pour chaque technique importante :
- Conserver la date de publication.
- Conserver la date de dernière vérification.
- Vérifier les mises à jour officielles.
- Détecter les API dépréciées.
- Détecter les nouvelles méthodes.
- Signaler les incompatibilités de version.
- Réexaminer les techniques après changement de moteur.

### Conservation

Ne garder dans le corpus actif que les fiches utiles et traçables.

Archiver les versions obsolètes sans supprimer les preuves historiques.

Les fiches rejetées doivent être exclues du RAG par défaut, mais leurs raisons de rejet doivent rester consultables pour éviter de refaire les mêmes erreurs.

Créer des rapports :
- Fiches utiles.
- Doublons fusionnés.
- Fiches obsolètes.
- Lacunes.
- Contradictions.
- Sources non vérifiables.
- Techniques candidates.
- Techniques validées.

Ne jamais inventer une source, un test ou une compatibilité.

---

## 6. RAG — DEVENIR LA SOURCE TECHNIQUE PRINCIPALE DE CLAUDE

Claude doit consulter l'Éponge directement par MCP.

Il ne doit pas être obligé d'ouvrir manuellement des centaines de fichiers Obsidian.

Améliorer le RAG existant :

1. Analyse de l'intention.
2. Reformulation de la requête.
3. Recherche lexicale.
4. Recherche sémantique si un modèle est réellement disponible.
5. Fusion et reranking.
6. Filtrage par moteur/version.
7. Filtrage par statut de preuve.
8. Déduplication des passages.
9. Sélection diversifiée des méthodes.
10. Compression du contexte.
11. Citations précises.
12. Accès au détail à la demande.

Comparer plusieurs stratégies sur un benchmark reproductible :
- BM25 existant.
- Hybride.
- Reranking.
- Recherche hiérarchique par tâche.
- Filtrage des fiches rejetées.

Mesurer :
- Precision@k.
- Recall@k sur un jeu de questions annotées.
- MRR ou nDCG.
- Taux de citations correctes.
- Taux de réponses sans preuve.
- Latence.
- Taille des briefings.
- Coût de calcul.

Ne pas prétendre réduire le quota Claude à partir du seul nombre de caractères JSON.

### Format de briefing Claude

Retourner par défaut :
- Objectif.
- Meilleure méthode candidate.
- Pourquoi elle est pertinente.
- Sources.
- Prérequis.
- Paramètres.
- Étapes d'implémentation.
- Tests.
- Risques.
- Alternatives.
- Échecs connus.
- Niveau de confiance.
- Statut de validation.

Prévoir un briefing compact, puis un approfondissement à la demande.

---

## 7. ANALYSE VISUELLE D'IMAGES DE RÉFÉRENCE

Objectif : permettre à l'utilisateur de fournir une image photoréaliste ou une capture de jeu et d'obtenir un plan technique Roblox.

Pipeline :

IMAGE → ANALYSE → DÉCOMPOSITION → RECHERCHE → RECETTES → LABORATOIRE → BRIEFING CLAUDE.

Pour une forêt, analyser :
- Composition.
- Types d'arbres.
- Densité.
- Silhouettes.
- Branches.
- Neige.
- Rochers.
- Sol.
- Brouillard.
- Ciel.
- Nuages.
- Éclairage.
- Ombres.
- Palette de couleurs.
- Distance de visibilité.
- Éléments animés.
- Contraintes de performances.

Créer une description structurée.

Distinguer :
- Ce qui est visible dans l'image.
- Ce qui est inféré.
- Ce qui doit être vérifié.
- Ce qui n'est pas reproductible directement dans Roblox.

Étudier les options de modèles visuels locaux compatibles avec le matériel utilisateur, sans installation automatique.

Si aucun modèle visuel n'est disponible, accepter une description fournie par Claude ou l'utilisateur et continuer le pipeline sans prétendre avoir analysé l'image.

Prévoir un système de références multiples et de comparaison des rendus.

Ne pas copier aveuglément les assets d'une œuvre protégée. Les images servent de références artistiques et techniques.

---

## 8. LABORATOIRE AUTONOME BLENDER ET ROBLOX STUDIO

C'est la fonctionnalité stratégique principale.

Créer une architecture expérimentale séparée du jeu de production.

### Laboratoire Blender

Étudier une connexion contrôlée à Blender 5.2 permettant :
- Ouvrir un fichier de laboratoire.
- Importer un modèle.
- Exécuter un script Python approuvé.
- Générer des variantes.
- Modifier géométrie et matériaux.
- Mesurer triangles et objets.
- Exporter des modèles.
- Capturer des rendus.
- Enregistrer les erreurs.
- Restaurer un état précédent.

### Laboratoire Roblox Studio

Étudier puis implémenter, si l'environnement le permet, un pont local sécurisé permettant :
- Ouvrir une place de test isolée.
- Importer des modèles.
- Créer des scènes de comparaison.
- Modifier des propriétés autorisées.
- Exécuter des tests contrôlés.
- Capturer des images.
- Collecter des métriques réellement disponibles.
- Tester collisions et interactions.
- Conserver les logs.
- Restaurer la scène.

Ne jamais supposer qu'un MCP peut contrôler Roblox Studio sans pont/plugin réel.

Définir explicitement le transport, les permissions, l'authentification locale, les capacités exposées et les limites.

Interdire toute écriture dans le jeu publié par défaut.

### Exécution expérimentale

Chaque expérience doit contenir :
- Identifiant unique.
- Question.
- Hypothèse.
- Source.
- Technique.
- Asset.
- Version.
- Variables modifiées.
- Conditions constantes.
- Témoin A.
- Variante B.
- Critères de réussite.
- Mesures.
- Captures.
- Logs.
- Erreurs.
- Décision.
- Rollback.

Une expérience sans preuve moteur ne peut pas être déclarée validée.

Ne pas confondre Heartbeat et FPS de rendu.

Ne pas inventer des mesures GPU.

---

## 9. BOUCLE D'AUTOCORRECTION

Construire une boucle fermée :

RECHERCHE → HYPOTHÈSE → EXPÉRIENCE → OBSERVATION → DIAGNOSTIC → NOUVELLE HYPOTHÈSE.

### Exemple : sapin de Noël

Test 1 :
Le sapin est trop plat, la neige paraît artificielle.

Enregistrer :
- Technique utilisée.
- Paramètres.
- Captures.
- Symptômes.
- Conditions.
- Causes possibles.
- Échec observé.

Test 2 :
Modifier uniquement la répartition de neige.

Si amélioration partielle :
- Conserver les éléments améliorés.
- Identifier les défauts restants.
- Rechercher des méthodes ciblées.

Test 3 :
Modifier le feuillage ou la géométrie selon les résultats précédents.

Si amélioration :
- Comparer avec le témoin.
- Vérifier performances et collisions.
- Conserver les preuves.
- Proposer la meilleure variante à Claude.

### Diagnostic

Après un échec, déterminer si la cause probable relève :
- De la recherche.
- De la méthode.
- Des paramètres.
- De l'implémentation.
- De l'export.
- Du moteur.
- De l'éclairage.
- Des matériaux.
- De la caméra.
- Des performances.
- Du protocole expérimental.

Ne pas relancer automatiquement la même expérience sans nouvelle hypothèse.

Ne pas effacer les résultats négatifs.

### Amélioration du moteur de recherche

L'Éponge doit pouvoir proposer :
- Une meilleure requête.
- Une nouvelle source.
- Un approfondissement.
- Une révision du classement.
- Une mise à jour de fiche.
- Une nouvelle expérience.

Les modifications de ses propres algorithmes, permissions, critères de validation ou politiques de recherche doivent passer par des tests et une revue humaine avant activation.

Ne pas autoriser une auto-modification incontrôlée du code de production.

---

## 10. CLAUDE → ÉPONGE : REMONTÉE AUTOMATISÉE DES ÉCHECS

Concevoir un protocole MCP pour que Claude puisse signaler :

- Tâche.
- Technique appliquée.
- Résultat attendu.
- Résultat obtenu.
- Capture ou log.
- Erreur.
- Conditions de test.
- Version de l'asset.
- Paramètres.
- Hypothèse sur le problème.

Exemple :

« Sapin C1, essai 3 : neige trop uniforme, silhouette répétitive, ombres incorrectes sous lampe V2. »

L'Éponge doit :
1. Enregistrer le résultat.
2. Relier l'échec à la fiche utilisée.
3. Mettre à jour son niveau de validation.
4. Identifier les causes candidates.
5. Rechercher les connaissances manquantes.
6. Préparer une nouvelle expérience.
7. Renvoyer à Claude une correction priorisée.

Ne pas enregistrer une réussite déclarée par Claude comme indépendamment vérifiée sans preuve adéquate.

Utiliser les outils MCP existants de mémoire expérimentale lorsque possible ; étendre uniquement les contrats manquants.

---

## 11. ÉCONOMISER LE QUOTA CLAUDE

L'Éponge doit effectuer en local ou via des processus spécialisés les tâches qui n'exigent pas Claude :

- Collecte documentaire.
- Indexation.
- Déduplication.
- Extraction de métadonnées.
- Vérification des versions.
- Préparation des briefings.
- Analyse des logs.
- Calcul de métriques.
- Génération de plans de test.
- Tests automatisés accessibles.
- Comparaison de variantes.

Prévoir une mesure comparative :
- Nombre d'appels Claude.
- Taille des contextes.
- Temps de résolution.
- Nombre d'essais.
- Taux de réussite.
- Qualité finale.
- Coût de calcul local.
- Coûts API éventuels.

Ne pas promettre une réduction de quota sans benchmark réel.

L'objectif est de transférer vers l'Éponge le travail de recherche et de validation répétitif, pas de supprimer tout jugement de Claude ou du développeur.

---

## 12. AUTONOMIE CONTINUE ET TRAVAIL NOCTURNE

Construire une exécution supervisée et bornée.

Fonctionnalités :
- File persistante.
- Planification.
- Priorités par chapitre.
- Checkpoints.
- Reprise après interruption.
- Journal des recherches.
- Budgets.
- Détection de boucles.
- Limites de ressources.
- Arrêt automatique sur erreurs répétées.
- Rapports de fin de session.
- Mode pause.
- Mode arrêt.
- Reprise contrôlée.

Le PC éteint ne peut pas exécuter de modèles locaux.

Étudier les tâches GitHub Actions ou une infrastructure distante pour les recherches compatibles avec le cloud, sans supposer qu'elles peuvent contrôler le Roblox Studio local.

Séparer :
- Recherche documentaire distante.
- Calcul local.
- Laboratoire Blender.
- Laboratoire Roblox Studio.
- Synchronisation.
- Publication de résultats.

Ne jamais activer une boucle infinie non bornée.

Ne jamais lancer une installation ou une dépense payante sans autorisation.

---

## 13. AGENTS SPÉCIALISÉS — SEULEMENT S'ILS APPORTENT UNE VALEUR MESURABLE

Étudier une organisation logique :

- Planificateur : décompose les tâches.
- Chercheur : collecte les sources.
- Vérificateur : contrôle les preuves.
- Architecte Roblox : vérifie la compatibilité.
- Spécialiste Blender : prépare les assets.
- Analyste visuel : compare les images.
- Expérimentateur : lance les tests autorisés.
- Diagnosticien : analyse les échecs.
- Archiviste : maintient la mémoire.
- Critique : détecte contradictions et fausses conclusions.

Il ne faut pas nécessairement créer dix processus ou dix modèles.

Privilégier les modules existants et les workflows orchestrés.

N'ajouter un agent indépendant que si son coût, son rôle et sa valeur sont démontrés.

---

## 14. OPTIMISATION TECHNIQUE ROBLOX

Conserver les contraintes réelles du projet :
- Roblox Studio et éclairage moderne compatible avec le moteur.
- Blender 5.2.
- Unreal Engine comme référence artistique et outil éventuel de prototypage.
- RTX 4060 Ti 8 Go sur le PC utilisateur.
- SurfaceAppearance et textures PBR.
- MeshParts et budgets géométriques adaptés.
- Cartes de feuillage.
- Animations skinnées.
- Compatibilité avec les appareils cibles, à définir.
- Qualité de rendu nocturne sous lampe torche.

Les limites techniques exactes doivent être vérifiées dans la documentation actuelle plutôt que reprises comme vérités intemporelles.

Priorités de recherche :
- Végétation réaliste.
- Neige et accumulation.
- Relief.
- Éclairage nocturne.
- Brouillard.
- Lampe torche.
- Vent et animation végétale.
- Empreintes.
- Collisions.
- Caméra.
- Viewmodel.
- Animation des personnages.
- Poursuite.
- Audio.
- Interactions.
- IA.
- Optimisation.
- Interface et guidage.
- Sauvegarde et multijoueur.

Chercher les techniques permettant de reproduire l'impression visuelle AAA sans prétendre égaler les fonctionnalités natives d'Unreal dans Roblox.

---

## 15. MÉMOIRE ET OBSIDIAN

Obsidian doit être la bibliothèque humaine consultable.

Le RAG doit rester l'interface de recherche rapide pour Claude.

Prévoir une organisation :

- Projet.
- Actes.
- Prologue.
- Chapitres.
- Scènes.
- Fonctionnalités.
- Techniques.
- Sources.
- Expériences.
- Réussites.
- Échecs.
- Contradictions.
- Versions.
- Décisions.
- Questions ouvertes.

Une technique doit avoir un identifiant stable et des références vers les tâches auxquelles elle sert.

Éviter de recopier intégralement la même fiche dans chaque chapitre.

Les résultats expérimentaux doivent être liés aux connaissances sans polluer le corpus primaire par des pages générées répétitives.

Préserver les originaux et la provenance.

Les synchronisations doivent être transactionnelles, réversibles et testées.

---

## 16. VALIDATION QUALITÉ ET BENCHMARKS

Construire un jeu de tests représentatif des besoins réels.

Exemples :
1. Trouver la meilleure méthode candidate pour les collisions B3/C1.
2. Trouver les techniques de neige réaliste.
3. Préparer un viewmodel de lampe.
4. Diagnostiquer un sapin trop plat.
5. Comparer deux variantes d'éclairage.
6. Détecter une fiche obsolète.
7. Refuser une méthode incompatible.
8. Retrouver un échec précédent.
9. Éviter de répéter un essai déjà raté.
10. Produire un briefing Claude compact.
11. Préparer une expérience Roblox.
12. Importer un résultat réel.
13. Réévaluer une technique après un échec.
14. Retrouver les dépendances du chapitre actuel.
15. Préparer les besoins du chapitre suivant.
16. Décomposer une image de forêt.
17. Refuser de déclarer un test visuel sans image.
18. Vérifier que les fiches rejetées n'envahissent pas les résultats.
19. Vérifier les permissions de laboratoire.
20. Vérifier la reprise après interruption.

Pour chaque amélioration :
- Test avant.
- Modification.
- Test après.
- Mesure.
- Régression.
- Limites.

Les tests simulés doivent être explicitement étiquetés.

Aucune capture inventée.

Aucune métrique inventée.

Aucune validation Roblox sans Roblox Studio.

---

## 17. ORDRE D'EXÉCUTION — NE PAS SE DISPERSER

### PHASE A — Consolider immédiatement

1. Vérifier l'état réel du dépôt.
2. Préserver les données.
3. Vérifier le pipeline MCP.
4. Améliorer le tri et le RAG.
5. Préparer la recherche anticipée du prologue et du chapitre 1.
6. Construire les tests de pertinence et de déduplication.
7. Préparer des briefings directement utilisables par Claude.

### PHASE B — Recherche multisource

1. Auditer les connecteurs existants.
2. Ajouter les sources les plus pertinentes réellement accessibles.
3. Gérer transcriptions et timestamps quand disponibles.
4. Vérifier les mises à jour des techniques.
5. Améliorer la décomposition récursive.
6. Remplir les lacunes prioritaires du chapitre actuel.
7. Exporter les fiches vers Obsidian.
8. Mesurer la qualité du RAG.

### PHASE C — Laboratoire

1. Définir le pont Blender.
2. Définir le pont Roblox Studio.
3. Construire une place de test isolée.
4. Implémenter les tests A/B.
5. Collecter les preuves.
6. Ajouter l'analyse visuelle lorsqu'un modèle compatible est réellement disponible.
7. Connecter la mémoire des échecs.
8. Tester la boucle d'autocorrection.

### PHASE D — Autonomie

1. Planification par chapitre.
2. Recherche anticipée.
3. Sessions nocturnes bornées.
4. Rapports automatiques.
5. Reprise après interruption.
6. Contrôle des ressources.
7. Évaluation de la réduction de travail Claude.

**Ne pas retarder les livrables utiles de la phase A pour terminer les phases C ou D.**

Si une capacité dépend du PC utilisateur, fournir un pont local testable et des instructions exactes, sans annoncer son fonctionnement réel avant le test sur ce PC.

---

## 18. LIVRABLES ATTENDUS

Créer ou mettre à jour des documents de référence dans le dépôt :

1. `MASTER_SPEC.md` — Cahier des charges complet.
2. `CAPABILITY_MATRIX.md` — Existant / testé / partiel / manquant.
3. `PROJECT_STORY.md` — Bible narrative corrigée.
4. `CHAPTER_RESEARCH_PLAN.md` — Recherche anticipée par chapitre.
5. `SOURCE_STRATEGY.md` — Recherche multisource et qualité.
6. `RAG_QUALITY.md` — Benchmark et améliorations.
7. `VISUAL_PIPELINE.md` — Analyse d'images et décomposition.
8. `AUTONOMOUS_LAB.md` — Architecture du laboratoire.
9. `FAILURE_LEARNING.md` — Boucle d'autocorrection.
10. `CLAUDE_MCP_WORKFLOW.md` — Utilisation quotidienne par Claude.
11. `AUTONOMY_OPERATIONS.md` — Travail continu, budgets et reprise.
12. `IMPLEMENTATION_REPORT.md` — Modifications et preuves.
13. `WINDOWS_SETUP.md` — Installation et validation sur le PC utilisateur.
14. `NEXT_STEPS.md` — Prochaines étapes ordonnées.

Les noms peuvent être adaptés à l'organisation existante pour éviter les doublons.

Fournir également :
- Code fonctionnel pour les améliorations réalisables.
- Tests automatisés.
- Résultats avant/après.
- Exemples de requêtes MCP.
- Briefings prêts pour Claude.
- Procédures de rollback.
- Liste précise des éléments nécessitant mon PC.

Ne pas produire uniquement des documents si des améliorations fonctionnelles sont réalisables dans l'environnement.

---

## 19. CRITÈRES D'ACCEPTATION

### Niveau 1 — Immédiatement utile

Claude peut interroger l'Éponge et recevoir un briefing pertinent pour une tâche du chapitre actuel.

Le RAG retrouve les bonnes fiches et évite les doublons.

Les échecs connus sont visibles.

Les limites et les sources sont explicites.

### Niveau 2 — Recherche anticipée

L'Éponge sait identifier les besoins du chapitre et préparer les recherches avant les demandes de Claude.

Les nouvelles connaissances sont classées et exportables.

Les recherches sont bornées et reprenables.

### Niveau 3 — Laboratoire

Une expérience isolée peut être créée, exécutée avec un pont réellement disponible, mesurée et enregistrée.

Les résultats ne modifient pas le jeu de production.

### Niveau 4 — Autocorrection

Un échec entraîne une nouvelle hypothèse justifiée, une recherche ciblée et un nouvel essai.

La mémoire évite de répéter les mêmes erreurs.

### Niveau 5 — Amélioration mesurée du workflow

Comparer une tâche avec et sans Éponge.

Mesurer le temps, les essais, les appels Claude, la qualité et les coûts.

Ne déclarer un gain que s'il est réellement observé.

---

## 20. INSTRUCTION FINALE

Je veux une Éponge qui travaille en avance sur mon développement, accumule des connaissances fiables, les teste quand elle en a réellement les moyens, apprend des échecs et fournit à Claude les méthodes les plus utiles pour créer mon jeu.

Je veux pouvoir dire :

« Nous commençons le chapitre 2. Le policier se réveille prisonnier dans un grenier. Prépare les meilleures techniques Roblox pour construire un grenier photoréaliste, la lumière lunaire, la poussière, les cadenas, les interactions et les énigmes. »

Et obtenir :
- Une décomposition technique complète.
- Les meilleures méthodes candidates.
- Des sources fiables et récentes.
- Les paramètres pertinents.
- Des tests reproductibles.
- Des résultats expérimentaux lorsqu'ils existent.
- Les risques et limites.
- Un briefing immédiatement exploitable par Claude.

**Privilégie la qualité réelle, la fiabilité, la réutilisation et l'efficacité.**

Ne confonds jamais :
- Connaissance et preuve.
- Proposition et implémentation.
- Simulation et test réel.
- Corrélation et causalité.
- Réalisme visuel et performances.
- Nombre de fiches et qualité de la bibliothèque.
- Autonomie souhaitée et autonomie effectivement opérationnelle.

Commence par inspecter le dépôt et produire un plan d'exécution court, puis implémente directement les améliorations réalisables, avec tests et preuves.

Travaille sur la PR existante sans fusionner, préserve les données et termine par un rapport précis : FAIT / PARTIEL / BLOQUÉ / NON TESTÉ.

**Objectif final : faire de l'Éponge le partenaire technique principal de Claude, capable de réduire les recherches répétitives et de transformer chaque échec en connaissance réutilisable.**