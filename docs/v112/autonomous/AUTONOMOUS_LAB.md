# Laboratoire local supervisé

Le nouveau `LocalLab` est un exécuteur de **mesure géométrique Blender**. Il ne
constitue pas un shell, un accès au jeu publié ou un pont Studio prétendument actif.
Il réutilise LabStore, l'import Blender existant, les verrous, les écritures
atomiques et les réservations de calcul persistantes.

## Transport, autorisation et frontières

Transport : fichiers JSON sous `lab/runner/<UUID>/`, rapports sous
`lab/inbox/jobs/<UUID>/`, droits du système de fichiers du même utilisateur.
Aucun port, listener, secret distant ou API payante. L'authentification est celle
du compte OS ; le hash contrôle l'intégrité, pas une signature contre ce même
utilisateur. Un modèle ou document ne reçoit aucun outil d'exécution.

L'exécution demande **l'opérateur CLI et --allow-blender**. Aucun des 27 outils
MCP ne peut appeler le runner. L'exécutable est choisi par l'opérateur, jamais
par une source. Le script est fixe (`scripts/blender_ocean_measure.py`) et son SHA
est lié au job. Aucun chemin de script arbitraire ou commande shell accepté.

Capacités : primitives de démonstration A/B, ou mesure d'une copie `.blend`
autorisée sous `lab/inbox`, avec hash et échelle explicitement enregistrés.
Chemins externes/parents/symlinks refusés. Blender démarre en background, réglages
factory, autoexec désactivé, un thread demandé. Cela ne remplace pas un bac à sable
OS : ne charger que des copies de confiance, sous un compte à droits limités.
Rendu, édition libre, export arbitraire et publication ne sont pas exposés.

Les IDs d'expériences dérivent du job et des méthodes ; une redirection du reçu
vers une autre expérience est refusée. Les unités/versions doivent correspondre
exactement au rapport. Le résultat importé reste PARTIAL_SUCCESS/non vérifié.
La vérification humaine du résultat de jeu est un mécanisme séparé.

## Budgets et reprise

20 jobs maximum, deux tentatives par job, réservations de calcul V10/Intelligence
existantes (maximum 20 s par opération et plafond quotidien partagé), timeout
processus au plus 18 s. Aucun quota existant augmenté. Le stockage du runner et
des rapports est contrôlé avec le plafond Ocean configuré ; les logs sont bornés
à l'admission et conservés. Ce n'est pas une isolation mémoire/VRAM formelle.

PENDING → RUNNING → SUCCEEDED/FAILED/BLOCKED. Les rapports sont create-only.
Après un checkpoint, des rapports complets et correctement liés sont importables
sans relancer le script ; des sorties partielles sont conservées et exigent une
inspection. Un job FAILED/BLOCKED n'est pas relancé aveuglément : nouveau design
explicite, anciens reçus et budgets conservés. SUCCEEDED signifie fin de collecte
logicielle, pas succès visuel ou technique du jeu.

## Preuve réelle disponible

Blender installé ici : **4.3.2**. Un job visant **5.2** a été bloqué avant mesure,
VersionMismatch. Un second design explicitement ciblé 4.3.2 a exécuté le vrai
script sur primitives générées : A **42 triangles**, B **58**, chacun **2 objets**,
**1 matériau**, dimensions mesurées **2 ×2 ×4 m**. Rapports et log sous
[proofs](proofs/blender-job.json). Aucun gain de qualité ou performance n'en est
inféré, aucun asset B3/C1 n'est impliqué, aucun rendu GPU n'a été mesuré.

## Studio : architecture proposée, non implémentée

Aucun Studio/plugin disponible dans cet environnement. Le CLI capabilities le
signale **NOT_IMPLEMENTED**. Les anciens collecteur Luau et import de rapports
restent disponibles, sans annoncer qu'ils ont été exécutés ici.

Un futur adaptateur doit : vérifier IsStudio et une scène de laboratoire explicitement
identifiée, utiliser une capacité locale authentifiée/nonce et permissions OS,
exposer une liste fermée d'opérations, lier job/asset/build, refuser publication et
jeu de production, capturer reçus/erreurs et restaurer le témoin. Aucun eval Luau,
commande système ou changement de permissions reçu d'Internet. Le transport
(file queue locale ou plugin officiel) et sa compatibilité réelle restent à
valider sur le PC avant activation. Une CI distante ne contrôle pas Studio local.
