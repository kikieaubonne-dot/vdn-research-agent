# Préservation et retour arrière

V11.2 est additive, basée sur PR #7 d23aafa. Aucun compteur ni fichier historique
n'est migré. Le contrôle [preservation.json](preservation.json) compare les 142
fichiers de connaissances/configuration/runtime présents au début : zéro manquant,
zéro changé, y compris le compteur local déjà modifié avant la mission. Ce fichier
runtime n'est pas inclus dans les commits. Les 110 anciennes notes et la note V11
restent présentes ; les rapports sources/expériences des versions précédentes
restent inchangés.

Avant installation : arrêter proprement les processus de collecte/MCP, copier
hors du dépôt `knowledge/`, `config/`, `lab/`, `output/`, `experiments/` s'il existe,
ainsi que `project/` et le coffre Obsidian. Conserver `git status`, le commit et
les fichiers non suivis dans une sauvegarde privée. Les secrets ne vont pas dans
une PR. Suivre aussi la [sauvegarde V11](../v11/BACKUP_MIGRATION.md).

Nouveaux fichiers personnels : `project/bible.json`, archive facultative
`project/prepared.json` et runtime privé `lab/ocean/project/` (cartes immuables,
index latest, enveloppes de sessions, références visuelles). `lab/` reste ignoré
par Git. Les analyses utilisent le registre Intelligence existant ; les sessions
et budgets restent ceux de V10/V11. Aucun ordonnanceur supplémentaire.

Les empreintes de source/configuration/Bible/vérificateur/expérience/visuel et des
clés de dépendances rendent les anciens résultats périmés sans les effacer.
Une clé historique peut être consultée mais ne déclenche pas de répétition d'une
procédure périmée dans un briefing. Les lectures réévaluent hors ligne si nécessaire,
sans réécrire l'index ni consommer un modèle. Pas d'invalidation globale entraînant
une nouvelle collecte automatique.

Retour fonctionnel immédiat : arrêter le serveur `--v112`, employer
`python vdn_mcp.py --v111` et `python -m agent.v111 ...` sur le même code. Leurs
outils restent disponibles. Pour revenir à un ancien checkout, employer un clone
séparé ou un worktree, en conservant intégralement les données nouvelles et les
compteurs courants. Ne pas utiliser reset --hard, clean ou une copie d'anciens
budgets. Ne pas effacer les preuves pour éliminer un échec.

Rollback Obsidian : utiliser l'identifiant de transaction avec `agent.v112 sync
--destination ... --rollback ID`, d'abord sans `--apply`. Les notes réservées
appartiennent à l'export transactionnel ; les fichiers personnels en conflit sont
conservés. Le coffre personnel n'a pas été ouvert dans cette livraison.
