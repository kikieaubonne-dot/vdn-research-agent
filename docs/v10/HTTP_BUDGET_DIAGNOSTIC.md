# V10 — arrêt HTTP Windows et reprise bornée

Base auditée : `5809168158bb1bf6a8599eafec875403ae081fa8`, branche
`codex/research-lab-v10`. Correctif distinct : `codex/fix-v10-budget-stops`, PR
à destination de V10. Aucun changement de quota ou de configuration permanente.

## Conclusion

Avec `http_per_tick=6` et `max_http_calls=12`, un tick peut s’arrêter après **six**
appels alors que la session conserve **six** appels disponibles. Ce comportement
est normal : aucune erreur arithmétique entre ces deux plafonds n’est démontrée.
Le texte historique `budget HTTP atteint` ne permettait pas de les distinguer.

Anomalies reproduites et corrigées : une unité restait `running` après un arrêt
contrôlé ; un arrêt ultérieur pouvait encore afficher un ancien motif/une ancienne
erreur ; les erreurs et progrès partiels retournés par la collecte n’étaient pas
exposés dans la session ; un plafond déjà épuisé pouvait consommer une tentative
supplémentaire sans pouvoir envoyer de requête. Une collecte retournant à la fois
un arrêt de budget et des erreurs perdait la distinction entre ces événements.

Le dossier Windows réel `lab/research/4f817a22-a945-4f6d-8b49-ec8f2d9d8aa2`
n’est pas disponible dans cet environnement. Les chiffres fournis sont des
observations utilisateur ; les URL effectivement appelées et l’historique des
deux premiers ticks ne peuvent pas être reconstruits à partir de ces seuls
agrégats. La reproduction ci-dessous utilise uniquement des réponses simulées.
**Aucune collecte Internet réelle V10 n’a été effectuée pour ce diagnostic.**

## Parcours du code

1. `agent.v10.main` transmet `research-run --apply --allow-network` à
   `ResearchSessions.run`. La configuration doit aussi avoir `network_enabled=true`.
2. `run` prend le verrou, recharge la session, applique les limites effectives
   (minimum des limites conservées et de la configuration), puis charge la file
   isolée et les quotas quotidiens partagés. Un ancien `running` est récupéré au
   chargement ; la simulation n’effectue pas cette récupération.
3. Un tick réserve son temps, incrémente `ticks` et installe un unique `Budget`
   dans le contexte courant. Son plafond HTTP est :

   `min(http_per_tick, max(0, max_http_calls - session.http_calls))`.

   Par exemple, `min(6, 12 - 0) = 6`. Les compteurs cumulés ne sont pas remis à zéro.
4. Une unité est réservée et marquée `running`, puis le RAG local est consulté.
   En l’absence de procédure couvrant les concepts, `agent.run.research` est appelé
   avec `finalize=False` et `touch_existing=False` : pas de réécriture des notes
   existantes ni de leurs index Markdown.
5. Sans caches, `active_providers` peut initialiser l’index officiel Roblox et
   les sitemaps DevForum. Les recherches, lectures et reprises passent ensuite
   par `providers.http_get` (ou le chemin local SearXNG explicitement configuré).
6. Avant chaque tentative HTTP, `Budget.request` vérifie le temps et le compteur
   du tick. Le checkpoint réserve ensuite les compteurs de session et du jour
   sur disque **avant** l’appel au transport. Le compteur du garde est incrémenté,
   puis `urlopen` est appelé.
7. La septième tentative avec un plafond de six est refusée **avant** checkpoint
   et avant `urlopen` : elle ne porte pas les compteurs à sept. L’exception
   `BudgetExhausted` remonte directement ou est retournée par `research` sous
   `stop_reason` et désormais `stop_details`, y compris lors de l’initialisation.
8. V10 enregistre `BUDGET_STOP`. Avant le correctif, cette sortie précédait
   `mark_done` et aucun nettoyage de l’unité n’était fait. Le `finally` sauvegardait
   donc sa valeur `running`. Ce statut persistait jusqu’au prochain chargement,
   alors qu’aucun processus de collecte ne continuait en arrière-plan.

Avec les limites rapportées et le message issu de ce garde, **6 cumulés ne
signifient pas 12 épuisés**. `ticks=3` n’implique pas six appels dans chacun des
trois ticks. Sans journal par tentative, aucun scénario précis de fournisseurs
ne doit être présenté comme celui réellement rencontré sur Windows.

## Sens des compteurs et robots

| Événement | HTTP | `fetch_attempts` |
|---|---:|---:|
| Initialisation d’un index/sitemap | chaque tentative | 0 |
| Recherche GitHub, y compris variantes de secours | chaque tentative | 0 |
| Lecture d’une source | chaque tentative réseau | 1 avant `reader.fetch` |
| Retry HTTP 429/502/503/504, URLError ou timeout | +1 par tentative autorisée | pas de nouvelle tentative logique de source |
| Redirection autorisée | +1 avant suivi | pas de nouvelle tentative logique de source |
| URL/redirection interdite | refus avant réservation de cet appel | une tentative de source peut déjà avoir été réservée |
| Requête refusée par le garde HTTP | 0 appel supplémentaire | une tentative de source peut déjà avoir été réservée |
| Source connue dédupliquée | pas de lecture réseau supplémentaire | 0 |

Une lecture GitHub peut demander métadonnées **et** README ; une source logique
n’équivaut donc pas à un appel HTTP. `fetch_attempts=5` ne signifie pas cinq pages
lues avec succès. Le compteur est réservé avant la lecture et peut précéder une
requête refusée. Les quotas ne sont pas remboursés après un arrêt.

Le chemin V10 `research-run → run.research → active_providers` **ne télécharge pas
automatiquement robots.txt**. Il réutilise notamment la politique statique de
chemins DevForum et la liste d’hôtes autorisés. La collecte `factory.collect` V9,
qui lit robots.txt, est un autre chemin. Si `http_get` reçoit explicitement une
URL robots.txt autorisée, cette requête est comptée normalement ; le test de
transport le vérifie. L’écart 6 HTTP / 5 fetch ne prouve donc pas un appel robots.

Le comptage est une réservation conservatrice avant effet : une interruption
entre réservation et transport peut surcompter. Les délais restent coopératifs ;
un socket déjà engagé peut terminer après l’échéance. Aucun quota n’est élargi
pour cacher ces coûts.

## Correction et nouveaux diagnostics

- `stop_reason` conserve le message humain. `stop_details` ajoute `kind`, `scope`
  (`tick`, `session`, `daily`), `resource`, `limit`, `used` et une politique de
  reprise. Pour un plafond de session, `used` et `limit` sont **cumulés** : 12/12,
  et non le garde résiduel de six appels.
- `last_tick` contient les HTTP/fetch du dernier tick exécuté, le plafond effectif,
  le reste HTTP de session et les compteurs quotidiens globaux. Le champ `daily`
  de l’ancienne file isolée n’est pas le compteur global de collecte.
- `last_collection` conserve les comptes retournés, IDs de notes créées, nombre
  d’erreurs et jusqu’à cinq messages bornés. Ces données restent non vérifiées.
  Les données sont validées avant leur écriture dans la session et la file.
- En cas de budget **et** d’erreurs de collecte, `BUDGET_STOP` décrit l’arrêt et
  `last_collection.errors` conserve les erreurs. Sans arrêt de budget, une collecte
  en erreur donne `ERROR` et incrémente `integration_failures`. Ce compteur mesure
  les ticks `ERROR`, pas toutes les erreurs de toutes les sources.
- Une unité interrompue de façon contrôlée passe à `pending` si elle dispose
  encore d’une tentative, sinon à `failed`. Les tentatives déjà réservées restent
  consommées ; une pause de budget n’est pas une preuve d’échec technique dans
  Roblox. Le journal reçoit `controlled_stop` et l’unité garde son dernier bilan.
- Un plafond HTTP déjà atteint est signalé avant une nouvelle réservation de
  tick/unité quand le réseau est demandé. Pour continuer uniquement en local,
  omettre `--allow-network`. Les autres plafonds restent applicables.
- Une interruption brutale (`KeyboardInterrupt`, processus tué) conserve le
  mécanisme existant de récupération au prochain `--apply`. La simulation ne
  modifie ni file, ni compteurs. Une reprise efface les diagnostics périmés.

Les signatures et messages existants du budget restent compatibles. Les nouveaux
attributs de l’exception sont propagés sans modifier le transport, les retries,
les robots, les redirections ou les règles d’autorisation.

## Validation reproductible

```sh
python -m unittest tests.test_v10_budget_stops -v
python -m tests.offline
```

Baseline reproduite : **288 tests**. Nouvelle suite : **305 tests**, dont
**17 régressions/contrôles supplémentaires**.
[Journal final](../validation/v10-budget/final-tests.log).

Le cas principal prépare dix unités synthétiques et fixe `ticks=2`. Des réponses
HTTP simulées autorisent six appels et cinq réservations de lecture ; le septième
appel est bloqué. Résultat : tick 3, six HTTP cumulés, cinq fetch, aucun appel
supplémentaire au transport, dix unités en attente et zéro `running`. Un tick
supplémentaire porte la session à douze appels et signale le plafond **session**.
Un nouvel appel à la commande ne consomme ensuite ni tick, ni tentative HTTP.
Les réservations sur disque sont vérifiées avant chacun des appels simulés.

[Rejeu avant/après](budget-reproduction.json) : le même scénario a aussi été
exécuté dans une copie isolée du commit V10 d’origine. Il reproduit **9 pending,
1 running**, tick 3, six HTTP et cinq fetch. Le correctif donne **10 pending,
0 running** avec exactement les mêmes compteurs, et ajoute `scope=tick`.

Les autres tests couvrent initialisation, résultat renvoyé par le vrai moteur de
collecte, progrès partiels avec création de note fixture non vérifiée, quotas
quotidiens, temps/ticks, reprises, plafond de tentatives, diagnostics de `status`,
secrets reconnaissables, robots explicitement demandé, retries réseau/HTTP et
redirections. Aucun test n’ouvre un socket vers les sites de collecte.
Les résultats GitHub Actions Linux/Windows sont à lire sur la PR de correction.

## Fichiers modifiés

| Fichier | Rôle |
|---|---|
| `agent/budget.py` | métadonnées d’exception, sans changement des plafonds ni messages existants |
| `agent/run.py` | propagation des diagnostics d’arrêt, initialisation comprise |
| `agent/research_session.py` | attribution des limites, nettoyage contrôlé, reprise et bilans partiels |
| `agent/v10.py` | diagnostics visibles dans `status` |
| `tests/test_v10_budget_stops.py` | 17 tests hors ligne |
| ce rapport, rapport V10, manifeste et journal de validation | preuves, limites et procédure |

[Conservation](http-budget-preservation.json) : les 110 Markdown et les fichiers
de tests V10 déjà présents restent inchangés. Aucun changement de configuration,
de calendrier ou de tâche permanente ; aucun déploiement ni fusion.

## Reprise de la session Windows

1. Arrêter les autres exécutions VDN. Faire une copie privée du dossier complet
   `lab/research/4f817a22-a945-4f6d-8b49-ec8f2d9d8aa2` et de `output/queue.json`
   (quotas globaux). Conserver aussi `output/last_run.json` et les caches si présents,
   avant qu’une nouvelle collecte ne remplace ce dernier bilan. Ne pas publier
   de clé ou capture personnelle avec ces fichiers.
2. Récupérer le correctif, sans écraser le `config/v10.json` local. Vérifier les
   modifications locales avec `git status --short` :

```powershell
git fetch origin
git switch codex/fix-v10-budget-stops
$env:PYTHONUTF8 = "1"
python -m tests.offline
python -m agent.v10 research-run 4f817a22-a945-4f6d-8b49-ec8f2d9d8aa2 --dry-run
```

3. Inspecter limites, `attempts`, temps cumulé et `ticks`. Le vieux `running`
   peut encore apparaître dans la simulation : elle ne le répare pas sur disque.
   Au prochain `--apply`, le mécanisme existant le récupère. Les anciennes
   tentatives, y compris les éventuels échecs périmés, ne sont pas effacées.
4. Si les limites et autorisations locales le permettent, déclencher **un** nouveau
   tick avec la même session :

```powershell
python -m agent.v10 research-run 4f817a22-a945-4f6d-8b49-ec8f2d9d8aa2 --apply --allow-network
python -m agent.v10 status
```

Avec les chiffres fournis, il reste au plus six appels de session, sous réserve
du temps, des tentatives et des quotas du jour. Un nouveau tick ne garantit pas
une fiche : bootstrap, retries, rejets ou absence de sources peuvent le consommer.
Si `scope=tick`, une reprise reste possible dans les limites restantes ; si
`scope=session`, pas de remise à zéro automatique ; si `scope=daily`, attendre
le jour UTC suivant selon la ressource. Une unité ayant atteint sa limite peut
être `failed` : inspecter son historique, sans falsifier ses compteurs.

Pour un passage strictement local, utiliser la même commande `--apply` **sans**
`--allow-network`. Ne pas remettre HTTP/fetch/tentatives à zéro, ne pas augmenter
arbitrairement les plafonds et ne pas automatiser une boucle de nouveaux ticks
ou sessions pour contourner un arrêt. Toute révision du plan/budget exige un
examen explicite. Aucun processus récurrent n’est nécessaire à cette reprise.

## Limites restantes

La session Windows personnelle et son Internet réel n’ont pas été exécutés ici.
Les tests prouvent les transitions et réservations avec transport simulé, pas la
disponibilité ou la pertinence des sites. Les anciens fichiers ne contiennent
pas un journal de chaque URL/retry/redirection ; leurs séquences exactes restent
inconnues. Un arrêt brutal ou une panne disque reste distinct d’un arrêt contrôlé.
Les limites de temps sont coopératives, le stockage est local et aucune collecte
ne valide automatiquement une connaissance dans Studio ou Blender.
