# Conservation des données V9

Base `8d83868` : **106 fichiers historiques**, tous toujours présents et identiques
par SHA-256. Aucun ancien fichier de connaissances, index Obsidian historique ou
réglage personnel n'est modifié. `docs/v9/preservation.json` conserve l'inventaire.

Ajouts dans `knowledge/` : **4 fiches candidates** ; total **110 Markdown**, dont
**98 fiches indexables**. Les données historiques suivies sous `output/` et les
workflows ne sont pas réécrits par la livraison. L'index SQLite local est un cache
ignoré par Git, reconstruit uniquement pour les lectures et tests.

Sur le coffre temporaire, les 110 copies correspondent aux sources ; 2 pages
générées s'ajoutent sans changer les originaux. Les fichiers source retirés ne
sont jamais supprimés du coffre. Les conflits, backups et archives de rollback
restent dans le bundle. Les réglages `.obsidian/` sont préservés par test.

Les caches de sources et rapports d'expérience privés ne sont pas publiés.
La réparation SQLite archive les anciens fichiers ; les notes ne sont pas touchées.
Arrêter les clients avant cette réparation explicite : ce n'est pas une migration
transactionnelle de clients actifs sur plusieurs machines.
