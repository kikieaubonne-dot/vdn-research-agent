# V10 — installation Windows et autonomie locale

Python **3.11+**, Git et un disque local NTFS ; aucune dépendance pip. Le cœur
emploie seulement la bibliothèque standard. Les commandes ci-dessous sont à
exécuter dans PowerShell, à la racine du dépôt. Elles ne sont pas installées sur
le PC utilisateur par cette livraison. Les tests locaux ont lieu sous Linux ;
le workflow `V10 offline compatibility` prévoit aussi Windows.

```powershell
git clone https://github.com/kikieaubonne-dot/vdn-research-agent.git
cd vdn-research-agent
git switch codex/research-lab-v10
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m tests.offline
.\.venv\Scripts\python.exe -m agent.v10 status
.\.venv\Scripts\python.exe -m agent.v10 spruce --dry-run
```

Les écritures atomiques de création utilisent des liens physiques : NTFS local
convient, FAT et certains lecteurs réseau ne conviennent pas. Préférer un clone
local et un export Obsidian séparé. Ne pas exécuter depuis une archive ZIP.

## Recherche manuelle et reprise

```powershell
.\.venv\Scripts\python.exe -m agent.v10 research-prepare "Comment reproduire un sapin enneigé photoréaliste dans Roblox ?" --apply
# Recopier le champ id retourné dans SESSION_UUID.
.\.venv\Scripts\python.exe -m agent.v10 research-run SESSION_UUID --dry-run
.\.venv\Scripts\python.exe -m agent.v10 research-run SESSION_UUID --apply
```

Un appel traite au plus deux unités. Relancer le même identifiant pour continuer.
`COMPLETE` signifie parcours terminé, pas réponse prouvée. `BLOCKED` signifie que
des prérequis manquent : inspecter les décisions et préparer une nouvelle session
après apport de sources. `ERROR` peut être repris après correction, dans la limite
des tentatives. Un arrêt forcé garde les réservations de budget ; aucune remise à
zéro automatique pour contourner une limite. Conserver le même `--session-id`
UUID rend la préparation répétée idempotente.

Le plan des domaines V7/V8 et ses dépendances sont réutilisés. Les relances sont
des règles lexicales explicites, sans raisonnement LLM simulé. Toute instruction
extraite demeure candidate. Aucun index Markdown historique n’est régénéré.
L’index SQLite est dérivé et actualisé par le moteur de lecture existant.

## Configuration et réseau

`config/v10.json` est le contrat local. Valeurs initiales :

| Limite | Valeur |
|---|---:|
| Profondeur | 2 |
| Branches totales, racine comprise | 24 |
| Unités par tick / tentatives par unité | 2 / 2 |
| Ticks par session | 12 |
| Appels HTTP par session / tick | 12 / 6 |
| Temps coopératif cumulé / tick | 60 s / 20 s |
| Stagnation sans nouvelle fiche | 2 niveaux |

Les plafonds globaux `config/autonomy.json` s’appliquent aussi : unités, tentatives,
profondeur, taille, HTTP et fetch quotidiens. Les nouvelles sessions gardent un
budget fixe ; réduire la configuration réduit aussi les budgets en cours.
Les unités locales consomment le quota quotidien de travail, même sans réseau.
Le compteur HTTP inclut tentatives, robots et reprises du transport existant.
Un socket déjà engagé peut terminer après le délai : budget coopératif.

Pour collecter réellement, définir `network_enabled=true`, puis ajouter
`--allow-network` à `research-run --apply`. Les deux conditions sont requises.
Les fournisseurs autorisés, robots, déduplication et classement sont ceux de V9.
La collecte peut créer des candidates sourcées, jamais promouvoir une note.
Des erreurs d’intégration arrêtent le tick et restent dans son état persistant.

## Modes limité et planifié

`tick --apply` choisit un objectif de `allowed_goals` selon les priorités V9,
reprend sa session et prépare une hypothèse d’expérience. Il ne lance pas Studio.
Il faut auparavant définir `autonomous_enabled=true`. Sans ce changement,
la commande retourne `disabled` sans créer de données.

Pour le mode planifié, activer aussi `schedule.enabled`, choisir `interval_s`
(minimum 60 s), puis configurer **manuellement** le Planificateur de tâches Windows :

- Programme : chemin absolu vers `.venv\Scripts\python.exe`.
- Arguments : `-m agent.v10 --root "C:\chemin\vdn-research-agent" tick --mode scheduled --apply`.
- Démarrer dans : racine absolue du clone ; fréquence choisie par l’utilisateur.
- Refuser les instances parallèles ; le verrou local reste une seconde protection.

Le timestamp est réservé avant le travail ; une coupure ne déclenche pas une
rafale de rattrapage. Ajouter `--allow-network` seulement pour autoriser la collecte
et avec `network_enabled=true`. Sans ce drapeau, le tick reste local. Aucun service,
daemon ou tâche récurrente n’a été installé ou activé ici. Une session terminale
n’est pas relancée sans fin : les objectifs achevés/bloqués sont à réexaminer avant
un nouveau lot. Désactiver les deux flags arrête les futurs ticks V10.

Le workflow historique de collecte V5.5 est conservé séparément ; les flags V10
ne le pilotent pas. Sa pause existante est la variable GitHub `VDN_PAUSE=1`.
Cette PR ne change ni son calendrier ni l’état des automatisations du compte.

## Modèles et matériel

Sans IA : collecte autorisée, lacunes, RAG, journal, protocoles, annotations,
comparaison manuelle et export fonctionnent. Le corpus actuel est petit ; les
tests tournent sur CPU. Aucun minimum RAM mesuré sur Windows n’est revendiqué.
Prévoir l’espace pour le clone, les sauvegardes et les preuves (8 Mo par fichier).

Adaptateur local : Ollama sur loopback HTTP, `/api/generate`, JSON, modèle
explicitement nommé. Adaptateur distant : endpoint HTTPS compatible chat completions,
par exemple base se terminant par `/v1`, clé dans `VDN_REMOTE_MODEL_KEY`, jamais
dans le JSON. `enabled=false` initialement pour les deux ; vision séparément
déclarée par `vision=true`. Vérifier soi-même que le modèle accepte les images.
Un nom configuré ne prouve pas cette capacité. Le modèle, sa RAM/VRAM et son GPU
dépendent du fournisseur et de la quantification ; consulter sa fiche avant achat.
V10 n’installe ni ne télécharge de modèle, n’a appelé aucun service IA réel et ne
garantit aucune vitesse de génération. Les contrats HTTP sont testés par fixtures.

Les appels sont bornés (10 s coopératives, une requête, 256 Ko de réponse,
1024 tokens demandés). Pas de redirection ni proxy implicite. Sans service, clé,
vision ou JSON valide, retour `manual_required`, `disabled` ou `unavailable`.
Les images ne partent à un fournisseur distant qu’après sélection explicite du
backend et activation du réseau/modèle. Les sorties restent des affirmations
non vérifiées ; aucun outil, shell ou script proposé par un modèle n’est exécuté.
