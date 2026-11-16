# Livraison V6.4 — fiabilité et démarrage productif sur le socle V11.2

**État global PARTIEL.** Exécution réelle dans le cloud Linux/Python3.12.14.
Le PC `C:\Users\kikie\Documents\Eponge-V11.2` n’est pas connecté. L’appellation
V6.4 désigne le cahier des charges ajouté ; le dépôt et les 27 contrats restent V11.2.
Aucun redémarrage du projet depuis zéro, aucune publication, fusion ou installation
permanente. Les configurations/corpus personnels et le scratch antérieur sont préservés.

## État retrouvé et priorité productive

Base `c93fe9b` retrouvée sur `codex/project-intelligence-v11-2` ; queue déjà modifiée
et `work/` non suivi conservés. Les 490 tests de cette base étaient vérifiés sur
Ubuntu/Windows dans la livraison précédente. La référence jointe «492 tests,8 ignorés»
ne correspond pas à cette copie cloud et n’a pas pu être vérifiée sur le PC utilisateur.

Un point de restauration privé de **553 fichiers suivis, avec les octets locaux
réels**, a été créé, extrait dans une copie jetable et vérifié par checksum avant
le développement. Les modifications existantes n’ont pas été réinitialisées.
Les nouvelles opérations ont leurs propres snapshots et code figé, sans perturber
la campagne en cours lors des développements.

Le noyau existant a immédiatement été exercé dans une copie isolée :

- **Campagne bornée réellement écoulée : 1800,359s.** Les cinq phases initiales
  prennent environ38,314s cumulées ; le reste est de la veille avec heartbeat,
  sans recherches identiques répétées. CPU propre du worker21,626s, incluant le
  suivi ; CPU enfants/GPU non mesurés, RSS/disque disponibles dans le rapport brut.
- **4 HTTP réels**, robots réutilisés en cache. Compteurs conservés : HTTP27→31,
  fetch25→35, items22→28. Plafond de mission6, limites existantes non augmentées.
- Sources : documentation Atmosphere, Terrain et Terrain Editor, discussion
  DevForum1193996. Les captures, dates, empreintes et limites sont conservées.
- Cinq préparations : **quatre PARTIAL, une BLOCKED**, aucune connaissance du jeu
  promue VERIFIED. Les priorités restent sapins/collisions/neige/éclairage/performance.
- Python réellement exécuté ; Blender4.3.2 réellement lancé sur primitives A/B :
  **42/58 triangles**, deux objets, un matériau, dimensions2×2×4m pour les deux.
  Comparaison contrôlée et mémoire des résultats ; aucun gagnant esthétique déduit.
- Obsidian : véritable écriture dans un coffre isolé, contenu relu et empreinté,
  second export unchanged. Coffre personnel non touché.
- Véritable processus MCP stdio : **27 outils**, Bible, briefing et détail.
  Aucune utilisation de l’interface Claude Desktop revendiquée.

Le processus de campagne est **STOPPED après sa limite**, pas «en recherche toute
la nuit». Le nouveau worker supervisé a ensuite exécuté ses six étapes et s’est
arrêté normalement ; cet essai court est distinct de la campagne de30min.
Le bilan du17 novembre à11h Europe/Paris a été programmé une seule fois dans le
cloud, avec obligation de rapporter l’état réel ou l’inaccessibilité des fichiers.

## Audit et protections des dix composants

[Matrice détaillée](CAPABILITY_MATRIX.md). Les modules stables sont réutilisés :
ResearchSessions/Roots, LabStore, Project, LocalLab, Obsidian, MCP et leurs budgets.

Nouveaux modules ciblés :

- `agent/reliability.py` : incidents versionnés/chaînés, déduplication, limites de
  réparation, restauration vérifiée, reconstruction de l’index, croyances séparées.
- `agent/mission.py` : préparation désactivée par défaut, diagnostic JSON, activation
  explicite, phases persistantes, checkpoints hashés, cache/permissions figées,
  détection d’index corrompu et réparation sûre avant les phases.
- `scripts/eponge_guard.py` : superviseur sans dépendance au cœur ; watchdog,
  circuit-breaker, groupe enfant maîtrisé, journal propre, gate de propositions.
- `scripts/eponge_validate.py` : validation hors cœur, suites fixes et inputs
  épinglés, vrais codes de sortie, timeout, aucun assouplissement de critères.
- `eponge.py`, `Eponge.cmd` : entrée unique Python et menu Windows préparé.

Le lanceur Windows est fourni mais **NON TESTÉ sur Windows**. La nouvelle suite
n’a pas été publiée sur GitHub pour obtenir une CI : la consigne interdit une
publication automatique. Les anciennes preuves Windows ne valident pas ce code nouveau.

## Défauts réellement démontrés

1. **Packaging figé incomplet.** Le premier lancement réel échoue sur le vocabulaire
   absent ; Python/MCP sont bloqués, les autres phases indépendantes continuent.
   Deux incidents persistants et la copie défaillante restent disponibles.
   Régression dédiée avant correction ; configuration en lecture incluse dans le
   snapshot ; nouveau lancement réel réussi. Aucun effacement pour masquer l’échec.
2. **JSON valide falsifiant une réussite.** Une modification directe de status/DONE
   était initialement acceptée. Deux régressions rouges précèdent le checkpoint
   version2 et le journal d’incidents chaîné. Altérations désormais rejetées.
3. **Légendes d’images présentées comme faits.** Observé sur les fiches réelles,
   puis reproduit sur une source de référence annotée. Les blocs Markdown commençant
   par une image restent dans les documents comme contexte, mais sortent de la
   récupération des affirmations et de la couverture de lacune. Le vérificateur les
   refuse aussi directement. Le pipeline11.2.5 invalide les anciennes analyses ;
   leurs résultats historiques ne sont pas supprimés.

Sur les cinq fiches conservées : **10 légendes parmi20 faits historiques →0 parmi14
faits nouvellement sélectionnés**. Ce contrôle porte sur le motif image balisé,
pas sur la vérité universelle des14 phrases restantes. Le témoin technique positif
reste récupéré. Les légendes sans balisage et l’inférence sémantique restent des limites.

Le benchmark22 conserve Recall@5 et MRR : moteur coverage0,977273/0,916667,
Intelligence lexical0,636364/0,401515. Aucun gain de rappel inventé ; le progrès
observé concerne le retrait de faux faits et la récupération sûre, pas un nouveau modèle.

## Tests et preuves

- **527 tests hors ligne OK**, exécutés par le validateur indépendant sur inputs
  épinglés, code de sortie0 et sources/critères inchangés.
- **527 tests OK** dans une copie à configuration personnelle activée, sockets
  interdits et paramètres sources inchangés. Les37 nouveaux tests sont distincts.
- Scénarios éprouvés : crash/import du réparateur, heartbeat absent, timeout,
  index SQLite réellement corrompu, sauvegarde falsifiée, manque de dépendance,
  permission refusée, altération de checkpoint/incident, faux patch touchant
  tests/config/permissions/mémoire fiable, panne du rapporteur et réutilisation
  de tâche sans nouvel effet. Un vrai test échoué est transmis FAIL/code1 ; une
  entrée épinglée modifiée est REJECTED/code2.
- Linux est le seul OS du nouvel essai. Python3.11 local, Windows, verrouillage de
  session GUI, Studio et Desktop restent explicitement non validés.

[Résumé machine](proofs/validation-summary.json),
[campagne réelle](proofs/campaign-summary.json),
[contrat210 exigences](ACCEPTANCE.json),
[runbook](AUTONOMY_RUNBOOK.md), [sécurité](SECURITY_MODEL.md).
Les logs bruts et les anciens incidents sont conservés dans la livraison privée,
avec leur manifeste ; ils ne sont pas poussés dans le dépôt distant.

Un essai supplémentaire a injecté un vrai fichier SQLite corrompu dans un runtime
isolé, puis lancé le processus complet : réparation automatique en une tentative,
incident RESOLVED après retest, original en quarantaine, sources protégées inchangées
après l’activation explicitement autorisée et six étapes terminées. La première
vérification du harnais incluait par erreur cette modification de configuration
d’activation ; elle est distinguée dans la preuve, sans changer les tests épinglés.
[Preuve du processus réel](proofs/auto-recovery-real-process.json).

## Limites importantes et décision

Le BLACK BOX généré contient les frontières concrètes : accès Windows/Studio/Desktop,
failover automatique de code non implémenté, contrôle GPU/charge et quotas multi-workspaces
partiels, holdout réellement aveugle absent, redaction non exhaustive, reprise après
panne du superviseur/OS non installée, modèle Ollama indisponible. Les causes inconnues
restent des hypothèses ; aucune amélioration générale de compétence n’est inférée.

Aucun candidat n’est automatiquement promu dans le code critique ou la mémoire
fiable ; aucune permission n’est élargie par une source ou un modèle. Les réparations
sont volontairement restreintes. Les modèles/embeddings réels, export/réouverture
Blender, test B3/C1, qualité artistique et généralisation nouvelle restent bloqués
ou non testés. Aucun pourcentage de fiabilité ou d’économie Claude n’est annoncé.

Le noyau est utile immédiatement dans le périmètre cloud testé. L’exploitation
Windows/nocturne permanente reste **à autoriser et vérifier**, sans masquer ce
blocage par les tests logiciels. Une seule intervention indispensable pour lever
l’accès au PC : ouvrir le dossier autorisé dans une session Codex locale Windows.
