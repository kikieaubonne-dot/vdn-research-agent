# Modèle de sécurité et limites V6.4

Le périmètre autorisé est le dépôt cloud, ses copies de laboratoire et les chemins
explicitement fournis. Le PC Windows, les fichiers personnels, le jeu publié et
les assets réels B3/C1 ne sont pas accessibles. Aucun push, publication, installation
ou service permanent n’est effectué dans cette mission.

Le superviseur et le validateur n’importent pas le cœur. Le superviseur crée son
enfant/groupe, vérifie son identité/heartbeat/progrès, borne le temps et les reprises,
puis termine seulement ce groupe. Les essais de panne utilisent des sous-processus
créés pour le test. Les outils MCP gardent leurs 27 schémas et permissions.

Code/tests/config/benchmarks sont épinglés. L’agent ne possède aucun chemin de
promotion de code ; le gate rejette code, tests, permissions et mémoire fiable.
Les seules propositions acceptées restent sous `lab/candidates/*.json|md`, en
STAGED_REVIEW_REQUIRED, jamais exécutées ni rendues fiables automatiquement.
Les données Internet ne deviennent jamais des commandes de l’exécuteur.

Les états critiques sont écrits atomiquement et les checkpoints sont versionnés
avec SHA256. Les incidents nouveaux utilisent une chaîne d’empreintes ; les anciens
journaux version1 restent lisibles comme héritage non scellé, sans garantie
rétroactive. Une altération JSON sans mise à jour des empreintes est refusée. Ce
mécanisme détecte les corruptions éprouvées ; il n’authentifie pas un utilisateur
malveillant du même compte OS capable de réécrire à la fois code et manifeste.
Aucun bac à sable OS formel pour du code arbitraire n’est revendiqué.

Les réparations AUTO_SAFE sont limitées à des opérations connues. L’index dérivé
est copié en quarantaine, reconstruit séparément et retesté. Les Markdown, configs,
Bible et données fiables doivent rester identiques. Les incidents CRITICAL ou
HUMAN_REQUIRED ne sont jamais auto-résolus. Une panne du rapporteur produit une
sortie indépendante ou une erreur visible ; aucune santé universelle n’est déduite
de l’absence d’incident enregistré.

Les journaux expurgent les formes de secrets et chemins privés testées, bornent
les lignes et leur taille. Cette expurgation n’est pas un détecteur universel de
secrets. Les logs privés restent dans le workspace et ne sont pas poussés. Aucun
secret ni environnement complet n’est demandé à l’utilisateur ou publié.

Ressources : plafonds V10 conservés, mission ≤6 HTTP, calcul coopératif borné,
Blender --threads1, aucun modèle/GPU lourd lancé, contrôle disque et watchdog.
La coordination globale de plusieurs workspaces et la pause automatique sous
charge de l’utilisateur restent PARTIELLES : conserver une mission à la fois.
Le crash de l’OS ou du superviseur n’a pas de service externe de reprise installé.

Aucune métrique Python, citation exacte, primitive Blender ou test vert ne devient
une preuve de rendu Roblox ou de préférence artistique. Aucun poids de modèle
n’a été entraîné ; aucun quota Claude économisé n’est estimé à partir des tokens.
