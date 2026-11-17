# PROLOGUE_START_NOW — commencer A → E

**Livraison de démarrage PARTIELLE.** Le cœur fourni est la continuation locale de17937ba ; le SHA exact figure dans DELIVERY_SUMMARY.json. Les gestes sont validés sous Blender4.3.2/GLB ; Windows, Claude Desktop, Studio, FBX et les nouveaux scripts Luau n'ont pas été exécutés ici. Aucun fichier de ton jeu n'est inclus ni modifié. Extraire ce dossier dans un NOUVEL emplacement, sans écraser le dépôt ou le coffre Obsidian.

## Première action : donner ce dossier à Claude

Copier le message de `CLAUDE_FIRST_MESSAGE.md`. Claude doit lire la Bible, l'inventaire et les limites avant de modifier **une copie de scène explicitement approuvée**. Si Claude n'a pas d'accès fichiers local, les fichiers et extraits restent à transmettre explicitement ; ce paquet ne crée aucun accès PC ou Studio à lui seul.

## Ordre de construction immédiat

1. **Vérifier l'environnement local.** Double-cliquer `WINDOWS/DIAGNOSTIC.cmd` ou lancer `py -3.11 WINDOWS/setup.py doctor`. Attendu : chemins existants, Python mesuré, état PARTIAL avec Desktop/Studio NOT_TESTED. Une absence de Python3.11 est un blocage explicite ; aucun logiciel n'est installé automatiquement.
2. **Brancher L'Éponge en lecture seule.** Depuis PowerShell : `py -3.11 WINDOWS/setup.py config-candidate`. Cette commande fournit le chemin Python Windows réel et un fragment MCP. Sauvegarder puis fusionner manuellement dans la configuration Desktop existante, sans remplacer ses autres serveurs. Voir `MCP_CONNECT.md`.
3. **Tester le transport.** `py -3.11 WINDOWS/setup.py test-mcp` doit trouver27 contrats identiques, lire les ressources et les deux preuves d'animation, et refuser l'écriture. Cela valide stdio, pas l'interface Desktop. Depuis Desktop, demander ensuite `get_intelligence_brief(question="prologue:resources", token_budget=500)` et une preuve d'animation.
4. **Ouvrir une copie Studio ou une nouvelle place locale.** Noter son PlaceId/build et le contrôleur présent ; noms et identifiants actuels restent UNKNOWN. Ne pas publier. Le laboratoire proposé utilise seulement de nouveaux objets et des noms PROPOSED.
5. **Monter le témoin J0.** Suivre `ROBLOX_ARCHITECTURE.md` puis `ROBLOX/README.md` : modules Progression, StarterLab et LabDriver. Le builder retourne un modèle non parenté ; son insertion reste un geste explicite sur la copie. Les marqueurs manuels simulent les événements : pas encore d'IA de Maëlle, de changement d'avatar, de voix ou de cinématique.
6. **Construire A→E**, avec les proxies disponibles et des placeholders pour les assets absents. Maison/post-it → départ de Maëlle → disparition → recherche/confrontation → appel → enquêteur. Première poursuite : seulement Shift pour sprinter si nécessaire. Fin F inconnue, jamais sélectionnée automatiquement.
7. **Tester puis remplacer les placeholders.** Parcours complet, événements hors ordre/doublons, collisions, caméra, reprise et changement de rôle. Les gestes réparés doivent d'abord être testés sur copie du rig cible ; ne pas supposer que GLB est le format d'import Studio accepté. Voir `IMPORT_RETARGET.md` et les36 ressources.

## Fichiers prioritaires

| Besoin | Fichier |
|---|---|
| Bible officielle, source humaine | `Eponge/source/project/BIBLE.md` et `bible.json`, révision3 |
| Scènes et contraintes | `SCENES_A_E.md`, `Eponge/source/project/chapters.json` |
|36 ressources/statuts/dépendances | `RESOURCES_36.json`, `RESOURCES_36.md`, `DEPENDENCIES.json` |
| Planning du prologue entier | `Eponge/source/docs/v112/prologue/J0_J3.md` |
| Architecture et scripts candidats | `ROBLOX_ARCHITECTURE.md`, `ROBLOX/` |
| Gestes réels, preuves et rejets | `ASSETS/`, `PROOFS/`, runtime conservé |
| Connexion et validation | `MCP_CONNECT.md`, `ACCEPTANCE.md`, `WINDOWS/` |
| Blocages et rollback | `BLOCKERS.md`, `Eponge/source/docs/v112/prologue/BLACK_BOX.md` |

Le nom historique `father_proxy-IK` désigne un gabarit technique ; il ne confirme pas la présence du père de famille, déjà absent. Aucun personnage réaliste terminé, animation de marche/course, retargeting Roblox ou scène finale n'est fourni comme validé.

L'index SQLite de recherche est un cache dérivé : une relocalisation peut provoquer sa reconstruction lors d'une lecture. Le vérificateur distingue ce cache des codes, sources, notes et compteurs immuables ; un changement de cache doit être signalé, et son contrôle structurel ne le transforme pas en preuve fiable.

## Critères de réussite de la première séance

Pouvoir parcourir A→E sur une copie, sans imposer d'escalade/glissade/accroupissement/enjambement en B, identifier Maëlle/sa disparition et le prochain objectif, déclencher l'appel puis une vraie transition vers l'enquêteur, et s'arrêter avant F. Les marqueurs de laboratoire ne valident pas ces comportements réels : les remplacer progressivement par des observations du jeu.

Hypothèses à mesurer, pas normes : contrôle<10s, interaction<30s, mystère<60s, éviter les séquences non interactives>20s, durée7–9min. Aucun test joueur ni gain de rétention démontré.

**Budgets préservés :** ledger103,752s dans cette copie cumulative (V10 conservée séparément à77,058s), mission forêt ponctuelle clôturée, politique60s rétablie ; aucun calcul Blender restant aujourd'hui. Ne pas réinitialiser les compteurs ou installer/activer un modèle/service. L’autorisation forêt120s/8HTTP a été consommée puis refermée ; elle n’est pas récurrente. Une future mission exige une nouvelle autorisation. Les lectures MCP et diagnostics n'engagent pas de nouvelle expérience.

## Résultat forêt livré ensuite

`FOREST_LAB/README.md` distingue le cycle automatique initial et les diagnostics dirigés par Codex. Les nouveaux proxies sont des candidats de laboratoire, pas des sapins réalistes terminés. `Eponge/runtime` contient la mémoire cumulative clôturée et ses échecs ; `OBSIDIAN_LAB` est le coffre isolé exporté. Pour le sapin, demander directement `tree:forest/spruce/snow`, puis `get_experiment_context(problem="Snowy spruce", limit=10, detailed=true)` afin de voir aussi les variantes rejetées. Aucun réseau, modèle ou Blender n’est lancé par ces consultations.
