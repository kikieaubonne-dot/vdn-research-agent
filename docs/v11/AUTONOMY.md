# Autonomie bornée sans Claude

Le CLI peut collecter et conserver la mémoire lorsque Claude est fermé. Le mode
manuel traite un tick d'un objectif explicitement préparé. Aucun daemon,
abonnement, tâche récurrente ou collecte en arrière-plan n'est activé ici.

`prepare --apply` autorise un objectif ; `run UUID --apply --allow-network`
exécute un tick. Pause, reprise et arrêt : voir [Windows](WINDOWS.md). Les
plafonds V10 ne sont ni relevés ni réinitialisés. Un objectif de recherche n'est
pas une autorisation de modifier les assets du jeu.

## Mode automatique facultatif

Pour l'activer ultérieurement, l'opérateur doit choisir explicitement :
`config/ocean.json.enabled=true` ET `config/v10.json.autonomous_enabled=true`.
Pour le mode scheduled, `v10.schedule.enabled=true` s'ajoute. Sans ces choix :

```powershell
& $python -m agent.v11 tick --mode autonomous --dry-run
& $python -m agent.v11 tick --mode scheduled --apply --allow-network
# La configuration livrée répond disabled, sans réseau.
```

Une invocation traite au plus un objectif READY autorisé, sans créer d'objectif
arbitraire. Les objectifs ERROR/BLOCKED/COMPLETE, pausés ou épuisés par session
sont ignorés. Le mode scheduled réserve son horodatage et respecte l'intervalle
configuré (3 600 s par défaut). Les erreurs de sources demandent une inspection
humaine, pas une boucle de retries infinie.

## Préparer une tâche Windows sans l'enregistrer

Exemple à adapter dans PowerShell ; ce bloc construit seulement un objet de
tâche. Le dossier de travail est nécessaire pour certains outils externes.

```powershell
$repo = $PWD.Path
$action = New-ScheduledTaskAction -Execute $python -Argument "-m agent.v11 --root `"$repo`" tick --mode scheduled --apply --allow-network" -WorkingDirectory $repo
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(5) -RepetitionInterval (New-TimeSpan -Hours 1)
$settings = New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Minutes 5)
$task = New-ScheduledTask -Action $action -Trigger $trigger -Settings $settings
# Aucune commande Register-ScheduledTask n'est exécutée.
```

Après examen, configuration et consentement explicite, l'opérateur peut
enregistrer cet objet dans le Planificateur sous son compte non administrateur.
Configurer la capture des sorties et la conservation des journaux localement.
Pour arrêter une planification existante : la désactiver dans le Planificateur,
mettre `ocean.enabled=false` et mettre les objectifs en pause. Le contrôle est
coopératif pour la requête courante ; vérifier le processus avant toute
intervention sur un verrou. L'intégration UI du Planificateur n'a pas été testée.
