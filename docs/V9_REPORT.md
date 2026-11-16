# Éponge V9 — rapport de livraison, 16 novembre 2026

Base V8 : `8d83868`, PR #2 au-dessus de V7 #1. Branche V9 :
`codex/knowledge-factory-v9`. Aucun déploiement, aucune fusion, aucun scheduler ajouté.

## Ce qui est construit

- `agent/obsidian.py` : export incrémental d'un bundle dont `knowledge/` s'ouvre
  comme coffre Obsidian ; simulation, manifeste, conflits, sauvegardes, reprise
  et rollback avec archives conservées. Les originaux ne sont jamais migrés.
- `agent/gaps.py` : inventaire par neuf dimensions et sept besoins de production.
  Les P0 sauvegardes/sécurité/collisions précèdent poursuite, rigging et finition.
- `agent/factory.py` : collecte ponctuelle explicite, robots.txt, transport et
  budgets existants, cache, tentatives bornées, arrêt sur erreur/stagnation et
  fiches candidates sourcées. Les textes ne sont jamais exécutés.
- `agent/operational.py` : briefing compact/détaillé, reformulation technique par
  problème, sources, contraintes, validation proposée, alternatives et échecs
  rapportés séparés. Aucune expérience rapportée n'est promue en preuve.
- `agent.v9` et MCP `--v9` : commandes explicites et nouvel outil de lecture
  `get_task_brief`, sans casser les outils V8. Réparation SQLite explicite avec
  archivage du cache précédent. Script PowerShell ponctuel, sans création de tâche.
- Profils réutilisant le planificateur : poursuite, diagnostic de rig et
  accessoires, en plus des profils sapin/forêt.

## Tests et autocorrection

**251 tests réussissent** via `python -m tests.offline`, dont les **218 historiques**
et 33 nouveaux tests. Les sous-processus sont également privés de connexions. Les octets CRLF Windows sont
conservés lors de la copie, de la sauvegarde et du retour arrière. Les requêtes
recopiées dans les notes ne comptent pas comme contenu de source pour les lacunes.
Tests de synchronisation : copie idempotente, conflits, notes personnelles,
symlinks, chemins, sauvegardes, corruption de transaction, interruptions et rollback.
Tests de collecte : budgets, robots, erreurs réseau simulées, données invalides,
volume, injection, secrets et doublons. Test de cache SQLite corrompu puis lecture.

La première suite complète a trouvé une régression : l'ajout de profils rendait
le contrôle d'un profil invalide dépendant du profil sélectionné. La validation
est maintenant globale et les tests historiques passent sans modification.
Un autre test protège les protocoles contenant une phrase de prudence : « aucun
seuil universel » ne doit pas faire disparaître le protocole proposé.

## Connaissances ajoutées

**4 fiches candidates**, issues de **5 pages officielles Roblox réellement lues**,
après contrôle de robots.txt, avec **6 requêtes HTTP au total**. Sauvegardes,
sécurité client/serveur, pathfinding et accessoires rigides. Cinq courtes citations
sont contrôlées littéralement contre les pages lues ; pas de copie intégrale publiée.
Les méthodes éditoriales et tests proposés sont étiquetés comme candidats :
**aucune technique n'est reproduite ou validée dans Studio**.
Voir [le rapport des recherches](V9_RESEARCH_REPORT.md).

## Résultat Obsidian observable

La démonstration exporte **110 Markdown sources**, plus **2 pages de navigation**,
dans un coffre temporaire : **112 Markdown**, **98 fiches indexables**. Trois
petits fichiers de configuration autorisés sont aussi copiés hors du coffre,
pour conserver les profils et limites du bundle de lecture.

Premier passage appliqué ; second passage **unchanged**, sans doublon.
Les empreintes des 110 Markdown copiés sont identiques aux sources.
Les liens des deux pages générées sont valides. Les six scénarios sont relus
dans un vrai sous-processus MCP stdio, avec réponses égales à celles de l'API.

**Export créé : oui. Synchronisation locale testée : oui. Coffre temporaire
validé sur fichiers/index/MCP : oui. Application Obsidian ouverte : non.
Coffre Windows réel synchronisé : non.** Aucun accès au disque Windows n'est
présent ; [la procédure locale](V9_OBSIDIAN.md) reste à exécuter par le propriétaire.

## Comparaison V8/V9

Jeu nouveau figé : 16 questions, dont 12 avec références attendues et 4 hors corpus.

| Mesure | V8, 106 fichiers initiaux | V8, corpus enrichi | V9, corpus enrichi |
|---|---:|---:|---:|
| Hit@1 | 0,500 | 0,917 | 0,917 |
| Hit@3 / Hit@5 | 0,583 / 0,583 | 1,0 / 1,0 | 1,0 / 1,0 |
| MRR | 0,542 | 0,958 | 0,958 |

**Le gain de récupération vient des nouvelles connaissances, pas d'un nouveau
classement.** Sur le même corpus, V8 et V9 ont les mêmes résultats. Le briefing
V9 s'abstient explicitement sur les quatre questions hors corpus ; V8 n'a pas de
champ d'abstention et renvoie des candidats (comparaison à son résultat vide,
pas à un jugement de vérité). Les dix questions historiques conservent Hit@1/@3/@5
et MRR 1,0 avec la politique déployée.
Voir [le protocole et ses limites](V9_RAG_REPORT.md). Pas de gain de vitesse annoncé.

## Critères d'acceptation

| Critère | État |
|---|---|
| A — tests historiques | 218/218 passent ; 251/251 au total |
| B — conservation | 106 fichiers identiques SHA-256, aucun ancien supprimé |
| C — lacunes concrètes | inventaire relié à sept tâches de production |
| D — connaissances sourcées | 4 candidates, 5 sources, vérification technique non faite |
| E — procédures et prérequis | reliés aux sources ; tests et rollback proposés, non exécutés |
| F — coffre sans doublon/écrasement | démontré sur coffre temporaire, conflits et interruptions testés |
| G — nouvelles fiches retrouvables | API et MCP réels sur le bundle exporté |
| H — démos reproductibles | six scénarios, comparaison octet par octet dans les tests |
| I — comparaison V8 | corpus initial/enrichi et implémentations isolés |
| J — Windows sans Claude | procédure et script livrés ; Windows réel non testé |
| K — limites explicites | sections ci-dessous et rapports spécialisés |
| L — pas d'action réelle prétendue | aucun coffre Windows, app Obsidian, Studio ou déploiement exécuté |

## Limites et suite

Les classements sont lexicaux et les labels du petit holdout viennent d'un seul
ingénieur. L'identité des citations est vérifiée, pas leur vérité sémantique.
L'abstention reste une heuristique ; des questions ambiguës peuvent encore produire
des candidats faibles. Versions, multijoueur, perception de l'IA et performances
réelles restent à tester. Les autres fournisseurs (Blender/Unreal/vidéo/Reddit)
n'ont pas été activés dans ce nouvel incrément ; seules cinq pages Creator Hub
ont été consultées. Les titres de vidéos ne sont pas présentés comme des vidéos lues.

Le collecteur complet a été testé avec fixtures ; les sources réelles ont été
lues sous budget puis importées par le même générateur de candidates. Aucune
collecte périodique n'a été activée. Les quotas partagés sont ceux du clone local,
pas un verrou distribué couvrant tous les PC et GitHub Actions.

La synchronisation suppose un dossier local contrôlé par son propriétaire. Elle
refuse les symlinks et conflits, mais ne constitue pas une défense contre un autre
processus hostile remplaçant des fichiers pendant une opération. Les transactions
et sauvegardes restent disponibles pour inspection. Une révision de source déjà
publiée n'écrase jamais la fiche : les révisions versionnées restent à développer.

[Audit](V9_BASELINE_AUDIT.md) · [Lacunes](V9_GAPS_REPORT.md) ·
[Démonstrations](V9_DEMOS.md) · [Conservation](V9_DATA_PRESERVATION.md) ·
[Windows](V9_WINDOWS.md) · [Roadmap V9.1/V10](V9_ROADMAP.md).
