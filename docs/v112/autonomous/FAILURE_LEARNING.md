# Retour d'expérience et autocorrection supervisée

La mémoire conserve les résultats et conditions dans la chaîne d'événements
LabStore. Aucun FAILED ni ancienne révision n'est effacé. Les rapports de Claude
restent `client_report_not_independently_verified` ; seule une revue opérateur
explicite peut établir VERIFIED sous conditions.

En mode --v112, les outils existants `record_experiment_result` et
`get_experiment_context` ajoutent un diagnostic : catégories candidates, requêtes
ciblées et protocole suivant proposé. Catégories actuelles : export, éclairage,
géométrie, collision, performance, protocole, matériaux, caméra. Ce sont des
**hypothèses par mots présents dans les erreurs/observations**, pas une preuve de
cause. Aucune image n'est prétendument analysée à partir d'une phrase.

Le diagnostic réutilise les conditions du résultat enregistré, pas une nouvelle
configuration qui pourrait avoir changé depuis. Il conserve ID et hash d'événement,
liens de tâche et observations. Si aucun résultat n'existe : WAITING_EVIDENCE.
La recherche et le nouvel essai sont **proposés**, pas exécutés sans les capacités
et budgets requis. Aucune auto-modification des politiques ou du code.

## Éviter la répétition aveugle

`prepare_experiment` refuse en mode projet la même technique sous les mêmes
paramètres/environnement/protocole qu'un FAILED lié à la tâche. Une répétition
justifiée demande `protocol.retry_justification` explicite et suffisamment précis.
Une modification réelle déclarée des conditions permet une nouvelle expérience,
sans effacer la première. Cela autorise un plan, pas une validation de la nouvelle
méthode. La garde est limitée aux rapports de tâche chargés par la mémoire bornée ;
elle ne constitue pas une détection sémantique de toutes les expériences historiques.

Le briefing de tâche garde un état conservateur après échec et retire les étapes
répétées sans justification. Les empreintes de révision invalident les fiches
périmées, y compris les archives publiées ; source/configuration/Bible/visuel
changé n'efface pas les anciennes preuves.

```powershell
& $python -m agent.v112 diagnose-failure EXPERIMENT_UUID
```

Exemple de boucle, sans résultats fictifs : enregistrer « neige trop uniforme »
avec vraies captures/conditions → hypothèse matériaux/géométrie → chercher les
lacunes → proposer un changement de répartition seulement → lancer un essai autorisé
→ comparer et conserver aussi les défauts restants. L'analyse visuelle réelle et
la sélection du meilleur rendu demandent encore outils/preuves et revue humaine.

Les tests utilisent des rapports **synthétiques explicitement étiquetés**, distincts
de la mesure Blender réelle sur primitives et d'un futur essai de jeu.
