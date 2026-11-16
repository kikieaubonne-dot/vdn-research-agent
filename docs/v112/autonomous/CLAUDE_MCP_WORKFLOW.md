# Utilisation quotidienne depuis Claude

Le mode `--v112` conserve exactement les **27 noms, schémas d'entrée et annotations**.
Les autres modes restent disponibles. Les requêtes de chapitre empruntent désormais
le plan de scènes, les requêtes de tâche le pipeline Intelligence existant.

1. Consulter le contexte confirmé et ses inconnues.
2. Demander le chapitre ou une tâche précise ; inspecter les références et conditions.
3. Récupérer le détail à la demande, sans envoyer tous les documents.
4. Préparer une expérience isolée ou une recherche de lacune sous permissions explicites.
5. Après exécution réelle, signaler résultat/preuves et relire le diagnostic.

| Besoin | Outil / exemple |
|---|---|
| Bible et rôles | get_intelligence_brief : `{"question":"Bible du jeu","token_budget":1800}` |
| Chapitre 2 | get_intelligence_brief : `{"question":"Nous commençons le chapitre 2 : grenier, lumière, poussière, cadenas et énigmes","token_budget":1800}` |
| Toutes scènes/dépendances/horizons | plan_ocean : `{"goal":"chapitre 2"}` |
| Préparer sans lancer | prepare_ocean : `{"goal":"chapitre 2","apply":false}` |
| Préparer une session persistante | prepare_ocean : `{"goal":"chapitre 2","apply":true}` avec --allow-research |
| Un tick de recherche | run_ocean avec goal_id retourné, apply et allow_network explicites ; configuration réseau nécessaire |
| Pause/reprise/arrêt | control_ocean, mêmes IDs et compteurs |
| Détail d'une tâche | synthesize_technical : `{"question":"collisions","apply":false,"allow_model":false}` |
| Analyse sauvegardée | get_intelligence_analysis avec clé conservée ; respecter detail_tool pour les prévisualisations non persistées |
| Échecs et hypothèses | get_experiment_context : `{"problem":"collision","status":"FAILED","detailed":true}` |
| Rapport réel | record_experiment_result, schéma existant ; --allow-experiments, preuves et conditions requises |

Le briefing de chapitre livre une méthode candidate par tâche, références
**candidates**, dépendances, échecs et prochaine action. Les sources de moteur
étranger ou de version Blender incompatible sont exclues de ce briefing. Le
nombre retiré est visible. `facts=[]` ne devient pas une preuve parce qu'une URL
est présente. La meilleure méthode mesurée reste inconnue sans comparaison réelle.

Un petit budget peut omettre des tâches : `omitted_tasks` l'indique, le détail
reste disponible via plan_ocean. Aucun rollback/avertissement n'est supprimé pour
faire croire à une procédure complète. Le chapitre 2 reste PROPOSED ; le plan
n'approuve pas une énigme ou une solution narrative non décidée.

Les capacités hôte sont séparées : --allow-research, --allow-experiments,
--allow-intelligence. Les modèles exigent aussi configuration et demande explicites.
Le runner Blender n'est **pas** exposé comme outil MCP et ne s'active pas à partir
d'un rapport d'échec. Claude peut préparer le design, l'opérateur autorise la CLI.

## Brief immédiat forêt/collisions

Objectif : réduire les blocages B3/C1 dans une copie de forêt. Hypothèses : volumes
physiques et contrôleur à inspecter. Source : doc collisions officielle, reçus et
protocole déjà disponibles dans `../continuity/`. Aucune valeur CollisionFidelity
optimale inventée. Inventorier A, reproduire le trajet, modifier un facteur dans B,
mesurer blocages/traversées/coût sous mêmes conditions, conserver preuves et restaurer
le témoin si régression. Assets/contrôleur/build sur le PC : encore inconnus ici.

## Brief immédiat grenier proposé

Objectif : préparer blockout et progression d'évasion. D'abord architecture,
matériaux, lumière documentée, interactions/cadenas, guidage/puzzles et audio.
Poussière P2 ensuite. Recettes : copier la scène, inventorier les entrées, isoler
un facteur, définir mesures et rollback. Aucun cadenas/rig/scène existant inventé.
Les réglages de lumière ou particules ne sont pas des valeurs optimales sourcées.

Le processus MCP stdio est testé réellement. **Claude Desktop sur le PC utilisateur
reste non validé**. Le protocole et le guide Windows permettent de le vérifier sans
modifier les autres serveurs ou le jeu.
