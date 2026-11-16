# V10 — frontières de sécurité et validation

| Risque | Contrôle livré | Preuve / limite |
|---|---|---|
| Réponse auto-promue | résultat client distinct de la revue opérateur ; `VERIFIED` absent du MCP | transitions négatives et preuve synthétique refusée ; attestation humaine reste une frontière de confiance |
| Injection dans source/modèle | données sans exécution d’outil, shell ou script | fixtures d’injection ; pas de compréhension sémantique ni d’exécution agentique du modèle |
| Traversée / symlink | chemins `lab/`, inbox imposée, UUID, refus des ancêtres symlink | tests hors dossier, liens de contrôle et preuves ; pas de défense contre un attaquant local remplaçant les chemins pendant l’opération |
| Corruption | événements séquencés et chaînés, taille bornée, contrôle du hash de chaque preuve | modification et trou internes détectés ; pas de signature externe ni détection garantie d’une suppression de fin de journal |
| Coupure / double écriture | fsync + création/remplacement atomique, verrous système/fichier, request_id, révisions | tests erreur disque, replay et reprise ; conserver une sauvegarde privée du registre |
| Boucle / coût réseau | profondeur, branches, stagnation, tentatives, ticks, délais, réservations avant effet | tests HTTP supplémentaire interdit, temps nul et quota quotidien ; un appel en vol n’est pas préempté |
| Réseau modèle implicite | modèles désactivés ; loopback local / HTTPS distant ; pas de redirection ni proxy | fixtures transport seulement ; endpoint distant configuré par l’opérateur, pas un audit de son fournisseur |
| Secrets | clé distant lue depuis l’environnement uniquement, champs credentials et motifs connus refusés | tests non-écho ; filtrage heuristique, pas détection universelle de tous secrets dans des captures ou données libres |
| Historique / production | `lab/` séparé ; collecte `touch_existing=False, finalize=False` ; aucun outil de patch/déploiement | manifeste des 110 Markdown inchangé ; aucun lancement Studio ou modification du jeu |
| Coffre personnel | export explicite séparé, simulation, conflits, sauvegarde et rollback V9 | tests sur coffre temporaire ; aucun accès au coffre personnel |

Les scripts Python importés sont le code de confiance du dépôt. Les configs et
les noms de fournisseurs doivent être modifiés par l’opérateur. Les artefacts
ne sont jamais exécutés ; OBJ et texte sont archivés, pas chargés comme code.
La lecture des dimensions PNG examine uniquement l’en-tête et n’ouvre aucun
décodeur multimédia. Les chemins de preuves sont revérifiés à l’usage.

Les quotas partagés V7/V9 et les compteurs de session sont réservés avant l’appel
HTTP. Une coupure peut donc **surcompter**, ce qui évite de sous-compter des effets
déjà lancés. Les limites de session et quotas quotidiens ne sont pas une limite
globale de stockage : archiver manuellement les anciens journaux/preuves, surveiller
le disque et conserver des sauvegardes. Limites structurelles : 1000 événements
par expérience, 1000 expériences/sessions inspectées par commande, 64 Ko par
snapshot et 8 Mo par preuve. Aucun nettoyage destructif automatique.

`lab/` est ignoré par Git et peut contenir des données privées. Les exemples et
fixtures publiés ne contiennent aucune capture personnelle ni clé. Aucune clé
d’environnement réelle n’a été utilisée pour des tests de modèle. L’ancienne
collecte GitHub Actions et ses autorisations sont héritées, non modifiées par V10 ;
le nouveau workflow de tests a uniquement `contents: read` et aucun calendrier.

Le lecteur de corpus valide la forme POSIX fournie **avant** sa conversion en
chemin natif Windows. Les antislashs fournis, chemins absolus, traversées `..`
et liens symboliques restent refusés ; la normalisation interne Windows ne
provoque plus le rejet de toutes les notes. Une régression vérifie la lecture
d’une note valide et le refus des formes dangereuses.
