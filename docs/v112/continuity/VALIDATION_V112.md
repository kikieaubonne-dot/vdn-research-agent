# Validation opérationnelle V11.2 — résultat PARTIEL

Référence retrouvée : 72f1b9c, PR #8 ouverte vers V11.1. L'ancien run
[43865177113](https://github.com/kikieaubonne-dot/vdn-research-agent/actions/runs/43865177113)
a été relu : succès Ubuntu/Windows, 416 tests par scénario. Aucun besoin de
rejouer la base avant les quatre régressions nouvelles.

## Résultats de la présente mission

| Catégorie | Résultat | Ce que cela prouve / ne prouve pas |
|---|---|---|
| Tests ciblés | **51 OK** | 47 V11.2 précédents +4 régressions nouvelles |
| Suite hors ligne Linux Python 3.12.14 | **420 OK**, 58,389 s | Compatibilité logicielle ; sockets interdites |
| Configuration personnelle isolée Linux | **420 OK**, 67,383 s | Aucun effet sur configurations/budgets originaux |
| CI Python 3.11 Ubuntu et Windows | Voir les checks du commit publié dans PR #8 | Résultats distants vérifiés et consignés dans la description PR, distincts du Windows utilisateur |
| Processus MCP stdio | **7 processus réels**, 27 outils | Initialisation et appels Bible/brief/détail/expériences fonctionnent |
| Originaux | SHA et offsets du snapshot collisions contrôlés | Attribution au snapshot, pas compatibilité Studio/B3/C1 |
| Clone sans originaux | Abstention vraie, faits et paramètres documentés vides | Archive explicitement secondaire ; candidats conservés à part |
| Boucle échec → mémoire → nouveau briefing | Échec synthétique propagé, état BLOCKED, étapes non répétées | Aucune expérience moteur ; aucune promotion VERIFIED |
| Nouvelle condition après échec | Nouvelle expérience synthétique PLANNED | Pas d'interdiction globale de planifier ; échec initial conservé |
| Export Obsidian isolé | simulation → committed → unchanged → rolled_back | Transaction réelle et pas de doublons ; coffre personnel non accessible |
| RAG après export | Ensemble des 99 IDs techniques inchangé | Pages générées/expériences exclues du corpus primaire |
| Préservation | **146 fichiers, zéro changé/manquant** | SHA avant/après, y compris le compteur déjà modifié avant mission |
| HTTP, modèles, coûts API de la validation | **0, 0, 0** | Pas de nouvelle collecte ni modèle ; sockets des enfants bloquées |
| PC Windows utilisateur | NON ACCESSIBLE | CI Windows n'est pas ce PC |
| Claude Desktop | NON TESTÉ | Un client stdio ne valide pas l'interface Desktop |
| Roblox/Blender 5.2, B3/C1, V2 | NON EXÉCUTÉ | Fichiers/applications absents ; aucun FPS ni résultat visuel |

Données reproductibles : [field-software.json](field-software.json),
[inventory.json](inventory.json), [preservation.json](preservation.json),
journaux `offline-linux.log`, `personal-linux.log`, `targeted.log`.
Les nouveaux enregistrements d'expériences sont uniquement des fixtures
étiquetées dans une copie isolée ; aucun résultat réel n'est ajouté au dépôt.

## Méthode du parcours contrôlé

`bench.validate_v112_field` crée une nouvelle copie séparée, conserve les compteurs
copiés et bloque socket/create_connection/getaddrinfo dans les serveurs enfants.
Il teste d'abord l'archive sans originaux ; puis relit des copies des snapshots
acquis auparavant. Aucune nouvelle visite Internet. Il conserve une fiche privée,
vérifie son détail via MCP, prépare/démarre/enregistre un FAILED synthétique par
les outils autorisés, puis consulte le briefing et la synthèse actualisés. La
révision précédente reste byte pour byte identique.

Un nouvel essai avec conditions différentes peut être préparé, sans faire oublier
l'échec. Les données sont exportées explicitement avec les pages privées de lab
vers un coffre isolé, puis restaurées transactionnellement. Le journal quotidien
copié reste identique, les originaux du dépôt et du précédent laboratoire restent
inchangés. Les traces complètes, incluant passages sources, restent privées.
Le JSON public contient métadonnées, assertions, durée des appels et hash du code
produit testé ; le SHA Git de base seul ne décrit pas les modifications en cours.

Deux premières tentatives du harnais de travail ont échoué avant les appels MCP :
import agent depuis un autre répertoire, puis patch socket avant l'import SSL.
Ce sont des défauts du harnais provisoire, corrigés avant sa publication ; aucun
résultat produit ni moteur n'en a été déduit. Le parcours publié a été exécuté
avec succès dans un nouveau répertoire. Les anciens répertoires d'essai sont conservés.

## Défauts corrigés

Les quatre tests nouveaux échouaient avant changement, preuve conservée dans
`regressions-before.log`. Causes et corrections :

1. L'abstention dépendait de la présence de métadonnées source, pas des faits
   actuellement attribués. Le briefing expose maintenant la disponibilité réelle
   de l'attribution ; sans faits il s'abstient.
2. Le chargement d'archive retirait les faits mais conservait les paramètres
   documentés. Ils sont désormais des `archived_parameter_candidates` ; les
   paramètres actuels restent vides tant que l'original n'est pas revalidé.
3. La fraîcheur d'une archive ignorait les expériences locales. Les révisions
   liées sont comparées ; un échec nouveau exige une réévaluation.
4. Une prévisualisation recalculée exposait une clé non sauvegardée comme si le
   détail était conservé. Son `detail_tool` indique maintenant
   `synthesize_technical` avec la même question, en lecture seule.

Seul `agent/project_work.py` change dans le produit. `tests/test_v112_continuity.py`
ajoute quatre tests ; les deux scripts bench rendent inventaire/parcours
reproductibles. Les 27 contrats MCP et permissions sont inchangés. Aucun fichier
historique, archive de carte, source, budget ou configuration n'est réécrit.

## Valeur utile et limites de l'évaluation

Une méthode candidate pour le problème collisions est sourcée et accompagnée
[d'instructions Claude](CLAUDE_HANDOFF.md) et d'un [test reproductible](ROBLOX_TEST_PROTOCOL.md).
Exactitude : attribution contrôlée, compatibilité partielle. Pertinence : hypothèse
adaptée au symptôme, non diagnostiquée sur assets. Nouveauté : KNOWN, aucune nouvelle
technique prouvée. Applicabilité : partielle jusqu'à inspection de la scène.
Résultat de jeu : NON TESTÉ.

La comparaison V11.1/V11.2 antérieure reste publiée, sans annoncer de gain de
Claude à partir des caractères JSON. Aucun nouveau benchmark IA ou jugement humain
aveugle n'est inventé. Contradictions, pertinence, liens distants et licences
ne font pas l'objet d'une preuve sémantique ou d'une certification exhaustive.

## Frontière humaine et reprise

Question utile unique : fournir l'emplacement autorisé d'une copie de scène
contenant B3/C1 et le contrôleur réel, ou confirmer qu'elle reste uniquement sur
le PC Windows. Cette question n'a pas interrompu inventaire, corrections, tests,
MCP ou préparation. Ensuite appliquer le protocole collisions, conserver les
observations réelles, puis consulter la mémoire. Le scénario bêta reste inconnu.

Retour arrière : [NEXT_ACTIONS](NEXT_ACTIONS.md) et [migration](../MIGRATION.md).
Aucune fusion, installation de modèle, tâche permanente ou publication Roblox.
