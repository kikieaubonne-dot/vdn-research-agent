# Opérations bornées, pause et reprise

Aucun service permanent, cron, tâche Windows ou recherche nocturne n'est activé.
Les configurations historiques demeurent inchangées. Le PC éteint ne peut pas
faire tourner Ollama/Blender/Studio ; une CI distante n'obtient pas ces applications.

La file et les sessions V10 restent le moteur. Les chapitres sélectionnent les
besoins, pas un nouvel ordonnanceur. Maximum 12 nœuds de préparation, limites
persistantes existantes : 6 HTTP/tick, 12/session, 12 ticks, 60 s de calcul session,
20 s/tick selon la configuration actuelle. Les plafonds effectifs restent les
plus restrictifs des budgets globaux/session/tick. Robots, retries et accès locaux
Ollama consomment leurs réservations correspondantes. Aucun compteur remis à zéro.

```powershell
& $python -m agent.v112 chapter-prepare chapter1
$session = (& $python -m agent.v112 chapter-prepare chapter1 --apply | ConvertFrom-Json)
& $python -m agent.v112 research-run $session.id --apply --allow-network
& $python -m agent.v112 control $session.id pause --apply
& $python -m agent.v112 control $session.id resume --apply
& $python -m agent.v112 research-run $session.id --apply --allow-network
& $python -m agent.v112 budget
& $python -m agent.v112 daily
```

Une commande run effectue un tick, pas une boucle infinie. Réseau configuré et
autorisation de requête restent nécessaires. STOPPED est terminal. PROJECT_CHANGED
signale un changement de Bible/catalogue et garde la session ancienne. File COMPLETE
signifie acquisition terminale ; tâche/chapitre peuvent rester PARTIAL/BLOCKED.
Les rapports gardent erreurs et résultats partiels au lieu de les effacer.

Arrêts : budget, profondeur/branches, stagnation, manque d'accès, provider désactivé,
source insuffisante, décisions/ressources manquantes. La récursion ne dépasse pas
les mécanismes existants ; aucun sous-agent autonome supplémentaire. Les diagnostics
d'échec proposent une recherche ciblée au lieu de relancer la même requête sans fin.

Une future exécution cloud manuelle peut faire recherche documentaire et tests
logiciels autorisés, avec secrets/budgets/rapports séparés. Elle ne doit pas
publier automatiquement des résultats non revus dans les données utilisateur ni
se présenter comme un laboratoire Studio local. La CI existante n'a pas été
transformée en collecteur permanent pendant cette mission.
