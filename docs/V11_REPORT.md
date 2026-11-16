# V11 « L'Éponge Océan » — livraison vérifiable

Base : PR #5 `4e2624f`, branche dédiée `codex/eponge-ocean-v11`.
Aucune PR historique modifiée, fusion, publication Roblox, déploiement ou tâche
permanente activée. Le socle V10 reste disponible.

## 1. Fonctionnement réel

Objectif général forêt → plan de douze facettes indépendantes → lacunes et
mémoire → découverte de liens autorisés → extraction/attribution → candidats
avec propositions de procédures et limites → récupération MCP/Obsidian.
Le pipeline fonctionne sans Claude ni modèle. La collecte réelle a produit une
candidate collisions exploitable pour **préparer** une comparaison, sans
prétendre que sa procédure a été validée dans le jeu. Une seconde recherche
réutilise cette mémoire et ajoute une candidate feuillage, puis s'arrête en
ERROR sur une autre lacune sans preuve pertinente.

La découverte est bornée à un registre de domaines et seeds ; le planificateur
est un profil de domaine déterministe. Ce n'est ni un explorateur universel,
ni un raisonneur général autonome. Les propositions d'ingénierie sont séparées
des affirmations directement soutenues par une source.

## 2. Vérifications exécutées

- Baseline **305 tests**, puis **335 tests hors ligne réussis**, sans socket.
- Suite complète dans une copie avec réseau/autonomie/schedule autorisés :
  **335 réussites**, configuration personnelle copiée et source inchangées.
- Vrais processus MCP stdio depuis autre cwd, 22 outils, briefing/structuredContent.
- Export incrémental Obsidian, conflit et rollback dans coffres temporaires.
- Internet réellement utilisé en laboratoire isolé via proxy explicitement
  approuvé dans sa configuration : 10 réservations sur quatre ticks, puis
  1 HTTP pour le deuxième objectif ; échecs historiques conservés.
- Blender **4.3.2 réellement exécuté**, géométries DEMO_A/DEMO_B : 42/58 triangles,
  import des rapports et comparaison identique. Pas Blender 5.2 ni assets B3/C1.
- 110 Markdown historiques comparés par SHA-256 : aucun octet modifié. Une seule
  candidate réelle ajoutée au corpus ; seconde conservée comme preuve dans docs.

Résultats CI Linux/Windows : consulter les checks de la PR V11 et leur SHA.
Le workflow exécute la suite hors ligne **et** le scénario configuration
personnelle sous Python 3.11. La validation CI n'est pas un accès Internet
réel Windows. [Logs locaux](validation/v11/),
[preuves réelles](v11/LIVE_VALIDATION.md), [préservation](v11/preservation.json).

## 3. Configuration nécessaire

Le réseau manuel nécessite `v10.network_enabled=true` et `--allow-network` ;
le `true` personnel n'est pas annulé. Les tests copient maintenant des fixtures
figées au lieu de la configuration vivante : cause du défaut Windows isolée.
Les quotas tick/session/jour V10 restent inchangés. `adopt` ajoute seulement
une enveloppe : la session Windows déjà à 12/12 HTTP ne gagne aucun budget.

Modèles et embeddings désactivés. Pour les utiliser : service installé,
matériel mesuré, endpoint/modèle configurés, activation explicite, et réserve
de coût conservatrice pour une API distante. Aucun abonnement imposé.
Le proxy de confiance n'est nécessaire que si le réseau l'impose ; sa frontière
de confiance est documentée et désactivée par défaut.

## 4. Dépendances aux applications

Claude sert de consommateur MCP ; sa fermeture ne bloque pas les ticks CLI.
Blender est nécessaire aux nouvelles mesures géométriques ; les protocoles
peuvent être préparés sans lui. Roblox Studio reste nécessaire pour déplacements,
collisions, rendu et performance réels. Aucun outil V11 ne modifie le jeu publié.
Claude Desktop et le Planificateur Windows ne sont pas pilotés dans cet environnement.

## 5. Limites et travail restant

- Autres domaines : nouveaux profils et connecteurs à développer ; DevForum,
  articles, vidéos/transcriptions et moteurs de recherche externes non validés.
- Compréhension IA, embeddings réels, contradictions implicites et qualité
  subjective des procédures : non évalués. Les sources obsolètes sont signalées
  selon âge/cache, pas vérifiées continuellement.
- Le second objectif montre une collecte partielle utile, puis ERROR ; les
  douze facettes ne sont pas toutes documentées par des nouvelles fiches réelles.
- B3/C1, coffre personnel et deux fiches Windows absents. Aucune mesure Studio,
  FPS, qualité visuelle, édition autonome Blender/Roblox ou gain de temps Claude.
- Benchmark de huit questions de développement sur même corpus : cible hit@3
  0,4 → 1,0, sans preuve générale de supériorité ; V11 plus lent sur ce protocole.
- Limite disque spécifique à Océan, pas à tous les artefacts historiques.
  Les réservations de coûts ne remplacent pas les tarifs/plafonds du fournisseur.

## 6. Installation et commandes PowerShell

```powershell
git clone --branch codex/eponge-ocean-v11 https://github.com/kikieaubonne-dot/vdn-research-agent.git
Set-Location vdn-research-agent
$env:PYTHONUTF8 = "1"
py -3.11 -m venv .venv
$python = Join-Path $PWD ".venv\Scripts\python.exe"
& $python -m tests.offline
& $python -m tests.personal_config
& $python -m agent.v11 plan "Forêt d'épicéas enneigée nocturne Roblox"
& $python -m agent.v11 brief "Pourquoi mon personnage se bloque contre les sapins ?"
```

Pour un clone déjà utilisé, sauvegarder avant de changer de branche.
Le [guide Windows](v11/WINDOWS.md) donne l'activation réseau explicite,
préparation/run avec UUID, reprise, adoption de la session existante et arrêt.
Pas de commande d'activation de tâche permanente exécutée.

## 7. PR, architecture et critères d'acceptation

La PR distincte cible `codex/fix-v10-budget-stops`. Son lien et les résultats CI
du commit final sont fournis avec la livraison ; les anciennes PR restent ouvertes.

| Démonstration | Résultat vérifié |
|---|---|
| 1 — recherche autonome | Collecte réelle, lien découvert hors seeds, candidat ; profil forêt borné |
| 2 — connaissance utile | Fiche collisions : preuves, étapes/protocole ; utilité humaine à revoir |
| 3 — mémoire | Réutilisation + candidate supplémentaire réelles, erreur ultérieure explicite |
| 4 — MCP | Vrai processus stdio testé ; Desktop non disponible |
| 5 — reprise | Interruption après écriture et reprise sans doublon/reset testées |
| 6 — Obsidian | Export/conflit/rollback testés en coffre temporaire |
| 7 — laboratoire | Blender réel, rapports importés/comparés ; aucun asset utilisateur |
| 8 — Windows | Suite et configuration personnelle dans CI Windows, voir checks du commit |

Fichiers principaux : `agent/ocean.py` (orchestration), `ocean_plan.py`,
`ocean_web.py`, `ocean_knowledge.py`, `ocean_semantic.py`, `ocean_api.py`,
`ocean_lab.py`, `v11.py`, `scripts/blender_ocean_measure.py`, les deux benchs,
`config/ocean.json`, deux modules de tests Océan et fixtures/config.
Adaptations compatibles : `research_session.py` (plan/collecteur/suivis
injectables), `providers.py` (transport/statut HTTP), `mcp_v8.py` (mode V11),
`tests/test_autonomy.py` (helper isolé), lanceurs de tests et workflow.

[Architecture et sécurité](v11/ARCHITECTURE.md) · [Modèles](v11/MODELS.md) ·
[MCP Claude](v11/CLAUDE_MCP.md) · [Obsidian](v11/OBSIDIAN.md) ·
[Autonomie](v11/AUTONOMY.md) · [Laboratoire](v11/LAB.md) ·
[Migration/rollback](v11/BACKUP_MIGRATION.md) · [Benchmark](v11/BENCHMARK.md).
