# VDN Research Agent V7 — rapport de validation

Date : **16 novembre 2026**. Base auditée :
`728235577c27deeb274195fc3534feffa8537afe`. Branche : `codex/autonomy-v7`.
Voir [l'audit initial](AUTONOMY_AUDIT.md) et les
[mesures brutes avant/après](AUTONOMY_V7_METRICS.json).

## Résultat concret

La boucle existante est conservée et renforcée, sans nouveau service ni dépendance.
**177 tests passent**, dont **43 nouveaux**. Les connexions socket sont interdites
pendant la dernière exécution : aucun test ne déclenche de recherche réseau payante
ou gratuite. Les **100 fichiers de `knowledge/`** présents au départ sont identiques
octet par octet après travaux, par comparaison SHA-256 de chaque fichier.
Aucune migration, recherche réelle ou réindexation n'a été lancée dans cette
bibliothèque de travail ; les benchmarks utilisent une copie temporaire.

## Phase A — audit et baseline

`docs/AUTONOMY_AUDIT.md` était absent ; il a été créé à partir du code.
134 tests existants passaient. Les fonctionnalités de file, récursion, déduplication,
extraction de procédures, stratégie UCB et index RAG existaient déjà : elles ont
été réutilisées. Le modèle Ollama facultatif n'a pas été activé.

Sept régressions ont été reproduites avec les nouveaux tests sur la base V6,
avant correction : **7 échecs sur 7**, puis **7 succès sur 7** après correction.

| Défaut reproduit | Avant | Après |
|---|---|---|
| Une seule lecture quotidienne disponible | 8 lectures autorisées au moteur | 1 lecture autorisée |
| Échecs de lecture, plafond par recherche = 1 | 4 tentatives | 1 tentative |
| Interruption juste après lancement | 0 recherche imputée | 1 recherche imputée avant exécution |
| Verrou JSON partiellement écrit | second lancement autorisé | second lancement refusé |
| Inspection de file pendant un cycle | `running` transformé et historique écrit | lecture seule, état conservé |
| Note enregistrée avant le registre | source absente du registre | source retrouvée depuis la note |
| Deux corruptions successives de file | première archive écrasée | les deux archives conservées |

## Phase B — fiabilité

- `agent/budget.py` partage une échéance monotone et un plafond d'appels HTTP
  entre les fournisseurs. Chaque tentative, retry, fallback et redirection du
  transport intégré est imputé avant le réseau. Les compteurs sont persistés
  avant les effets et survivent aux interruptions.
- `cycle` transmet le reliquat quotidien de lectures au moteur et borne aussi
  les échecs de lecture. Une option CLI ne peut pas augmenter le plafond configuré
  du cycle. Les limites négatives, non finies et non numériques sont refusées.
- `refresh`, utilisé par le cron quotidien existant, partage le quota HTTP de la
  file et utilise le même verrou et le même budget de durée.
- Le verrou combine création exclusive, identité du propriétaire et verrou
  système. Le verrou système empêche deux reprises simultanées d'un vieux fichier
  et sa libération par le mauvais propriétaire. Une métadonnée partielle récente
  reste occupée. Le résumé et le rapport sont enregistrés sous verrou.
- `agent/storage.py` utilise fichier temporaire unique, flush, fsync et remplacement
  atomique. La création d'une fiche utilise un lien exclusif qui refuse d'écraser
  un nom existant. Les écritures de notes, registres, JSON et caches modifiées
  utilisent ce mécanisme. Les index Markdown générés sont également atomiques.
- Le registre dérivé est complété à partir des notes et extraits existants à
  chaque ouverture. Les références à des fichiers absents ou hors bibliothèque
  ne servent plus à déclarer une source déjà disponible.
- Les URL de nouvelles fiches sont contrôlées. Une redirection est vérifiée avant
  contact ; l'en-tête Authorization est retiré entre hôtes. Le volume décompressé
  gzip est borné. Aucun secret n'a été consulté, ajouté ou modifié.

## Phase C — recherche et évaluation

### Décomposition et prérequis

`python -m agent.run plan --topic spruce "Comment créer un sapin enneigé réaliste et performant dans Roblox ?"`
construit un plan de **11 branches** : tronc, branches, aiguilles, cartes alpha,
UV, PBR, neige, LOD, vent, éclairage et export Blender/Roblox.
Le profil est explicite dans `config/research_domains.json`, avec graphe de
prérequis validé avant sauvegarde. Une question simple reste une recherche de file.
Le parent complexe est marqué décomposé (`skipped`), pas réussi ; seuls ses
enfants réalisent les recherches. Un plan répété ne recrée pas ces recherches.

Les recherches dépendantes attendent des extraits attribués contenant des actions
exploitables. Un prérequis sans résultat reste bloquant et apparaît dans `queue`.
Une source déjà connue peut fournir cette information sans réécriture de sa fiche.
Un test avec sources locales distinctes réalise les 11 branches en trois cycles
de quatre recherches au plus, avec 11 recherches imputées. Ce résultat vérifie
l'orchestration et les budgets, pas les méthodes techniques simulées.

### Relances, stagnation et mémoire

Les relances de sources rejetées font désormais quatre termes au plus, avec la
facette utile conservée : `tutorial`, `compatibility` ou `settings`.
Le plafond de six enfants s'applique au parent, à travers toutes ses nouvelles
fiches et sources rejetées ; les plans ont un plafond séparé de douze nœuds.
Deux recherches consécutives sans nouvelle fiche arrêtent l'expansion d'une
branche, même si la profondeur maximale n'est pas encore atteinte.
Une recherche réellement vide ne crée ni fiche ni sous-question artificielle.

Les anciennes fiches candidates/documentées sont évaluées à chaque cycle.
Leurs lacunes peuvent ajouter au plus six recherches ciblées par cycle, avec
raison et identifiant de fiche. La déduplication inter-sujets est conservée,
et les facettes autrefois effacées comme stopwords restent distinctes.
Les anciennes clés de file restent reconnues ; aucune réécriture globale de mémoire.
Cette comparaison reste lexicale : elle ne résout pas toutes les paraphrases.

### Classement explicable

La file classe par ordre lexicographique, sans somme de poids ajustée arbitrairement :
utilité projet → nombre de dépendants débloqués → importance des lacunes → nouveauté
attendue → indice de source → incertitude → coût → risque de duplication.
La diversité des sujets départage ensuite les sélections d'un cycle.
Chaque critère, l'ordre de comparaison, les notes correspondantes et les entrées
inconnues sont visibles dans `queue`. Les coûts observés utilisent la moyenne
des tentatives HTTP du sujet ; sans observation, le prior neutre est signalé.
Les notes et priorités sont réévaluées après chaque recherche.

Cette politique est une décision d'ingénierie testée (préférence aux prérequis,
coût, changement après nouvelles preuves), pas un optimum appris sur un corpus.
Les priorités d'ingénierie P0/P1/P2/P3 ne sont jamais utilisées comme scores de recherche.
L'adaptation UCB des formulations et son retour arrière existants sont préservés.

### Diagnostics des fiches

`python -m agent.run evaluate` produit `output/knowledge_evaluation.json` :
attribution d'extraits, étapes, paramètres, contraintes, prérequis, alternatives,
protocole de reproduction et avertissements. La longueur ne rapporte aucun point.
Une analyse IA ou une validation déclarée n'est pas transformée en preuve.
Les états `probable`, `hypothetique`, `non_resolu` sont séparés ; `verifie` est
réservé à une validation externe et n'est jamais attribué automatiquement ici.
`truth_verified` reste faux et `technical_accuracy` reste `non_verifiee`.
Une contradiction explicitement signalée maintient l'état non résolu.

Sur les 89 notes actuelles : 25 `probable`, 10 `hypothetique`, 54 `non_resolu`.
Les diagnostics trouvent notamment 89 notes sans prérequis et 89 sans protocole
de reproduction explicite. Ce sont des constats structurels conservateurs,
pas une expertise technique des sources ni une mesure de vérité.

## Phases D et E — mesures, non-régression et autocorrection

| Mesure | Baseline | V7 |
|---|---:|---:|
| Tests existants | 134/134 | 134/134 |
| Ensemble final | — | 177/177 |
| Régressions P0 reproduites | 0/7 corrigées | 7/7 corrigées |
| Facette ciblée conservée après raccourcissement, 3 cas synthétiques | 1/3 | 3/3 |
| Précision pertinence, 54 cas existants | 0,667 | 0,667 |
| Rappel pertinence | 0,889 | 0,889 |
| F1 pertinence | 0,762 | 0,762 |
| RAG hit@1, 10 requêtes | 0,9 | 0,9 |
| RAG hit@3 | 1,0 | 1,0 |
| RAG MRR | 0,933 | 0,933 |
| Négatifs propres | 1,0 | 1,0 |
| Fichiers historiques conservés intégralement | 100 | 100 |

Les quatre faux positifs et le faux négatif du filtre de pertinence existaient
avant la mission et subsistent. Aucune amélioration de vérité, de pertinence
sémantique ou de performance réseau n'est revendiquée.

Un premier test de plan complet a été bloqué par la déduplication des extraits :
le fournisseur factice générique répétait les mêmes instructions SpotLight pour
tous les prérequis. La fixture a été corrigée pour fournir des preuves distinctes,
sans affaiblir le filtre du logiciel. Le test de prérequis infructueux reste bloquant.
Les tests ciblés ont ensuite été rejoués, puis la suite complète sans réseau.

Commandes reproductibles :

```sh
python -m unittest discover -s tests -v
python -m unittest tests.test_v7_safety tests.test_v7_intelligence -v
python bench/evaluate_v7.py --repo .
python -m agent.run bench
```

Les traces des tests avant/après sont dans `docs/validation/`. Le dernier lancement
a ajouté un mock de `socket.socket.connect` levant une erreur pour toute tentative
réseau. Les tests de retries, redirections et gzip utilisent des réponses locales.

## Configuration et exploitation

| Limite | Valeur |
|---|---:|
| Recherches par cycle / jour | 4 / 40 |
| Durée coopérative du cycle ou refresh | 1 200 s |
| Lectures tentées par recherche / jour | 8 / 300 |
| Tentatives HTTP par cycle ou refresh / jour partagé | 100 / 600 |
| Profondeur maximale | 2 |
| Enfants par fiche / parent de recherche | 3 / 6 |
| Nœuds d'un plan | 12 |
| Stagnation sans nouvelle fiche | 2 recherches |
| Échecs avant abandon | 3 |
| File en attente | 400 |
| Rafraîchissement d'une recherche terminée | après 14 jours |
| Expiration des métadonnées de verrou | 7 200 s |

`max_size` borne les éléments en attente, pas l'historique de toute la vie du projet.
`max_fetch` et `daily.fetch` comptent désormais les tentatives, tandis que
`fetched` dans les rapports compte encore les lectures réussies. Les requêtes
logiques, lectures et tentatives HTTP sont des unités différentes.
Les plafonds HTTP sont prudents et configurables ; ils ne représentent pas un
engagement d'acceptation des services externes.

Le workflow GitHub Actions est inchangé : tests avant recherche, cron horaire,
refresh quotidien, sérialisation, timeout 25 minutes et contrôle anti-secret.
Ni code auto-généré, ni déploiement automatique, ni fusion dans `main` n'ont été ajoutés.

## Limites et critères partiellement atteints

- Le profil de décomposition couvre pour l'instant le cas sapin/arbres, avec
  déclencheurs FR/EN. Les autres sujets utilisent la file et les relances générales.
- L'évaluateur contrôle la structure des preuves et les contradictions déjà
  signalées ; il ne détecte pas toutes les contradictions sémantiques, ne vérifie
  pas la disponibilité des liens, et ne reproduit rien dans Studio/Blender/Unreal.
- Les diagnostics de sources et de nouveauté sont heuristiques. Aucun embedding,
  service payant ou modèle de jugement n'a été ajouté.
- Les deadlines sont coopératives : un appel socket engagé peut finir après
  l'échéance. Les timeouts sont réduits au temps restant, sans prétention de limite
  temps réel absolue ; indexation et sauvegarde finale restent nécessaires.
- La persistance est atomique fichier par fichier, sans transaction globale entre
  notes, JSON et journaux ni garantie contre toute panne matérielle. Un registre
  JSON déjà corrompu échoue explicitement ; les notes restent conservées.
- Les chemins Windows sont pris en charge dans le code du verrou, mais les tests
  de cette mission tournent sous Linux/Python 3.12. La panne disque est simulée,
  pas provoquée sur un disque réel.
- `cycle` et `refresh` appliquent les quotas persistants. La commande historique
  manuelle `research`, Ollama et les appels directs aux fournisseurs ne partagent
  pas automatiquement la comptabilité de file ; ils ne sont pas lancés par le
  workflow autonome. Leur unification est inscrite en roadmap.
- Aucun auto-changement de code n'est exécuté. Toute future proposition doit
  passer par une branche, les tests et une revue humaine avant déploiement.

Les critères locaux P0/P1 sont validés dans le périmètre décrit. L'autonomie
générale, la validation technique et la calibration large restent partielles.
La publication de la branche et de la pull request dépend de l'accès GitHub
en écriture ; l'authentification disponible au début de mission était invalide.
L'état final de publication est indiqué dans la livraison, sans prétendre qu'une
PR existe si sa création n'a pas abouti.

### État de publication constaté

Le commit d'implémentation est `0f13b9a`. Le push de `codex/autonomy-v7` a été
tenté et a échoué : Git n'a pas d'identité HTTPS utilisable pour github.com.
`gh auth status` signalait également un jeton invalide. La branche n'est donc
pas publiée et **aucune pull request n'a été créée**. La connexion GitHub est
nécessaire pour terminer ce livrable ; aucune fusion dans `main` n'a eu lieu.
