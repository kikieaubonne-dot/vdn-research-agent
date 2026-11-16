# Lanceur unique — campagnes bornées, pas de service installé

Entrée : `eponge.py` ; menu Windows : `Eponge.cmd`. Le menu et Python3.11 sur le PC
utilisateur restent **NON TESTÉS**. L’entrée Python a été exécutée sous Linux3.12.14.
Aucun fichier C:\Users\kikie\Documents\Eponge-V11.2 n’a été atteint/modifié ici.

## Parcours disponible

Depuis le dépôt, choisir un nouveau dossier de laboratoire explicitement autorisé :

```sh
python eponge.py --workspace /chemin/nouveau-laboratoire init
python eponge.py --workspace /chemin/nouveau-laboratoire doctor
python eponge.py --workspace /chemin/nouveau-laboratoire start --activate --allow-network --allow-blender
python eponge.py --workspace /chemin/nouveau-laboratoire status
python eponge.py --workspace /chemin/nouveau-laboratoire report
```

Ces commandes existent et les opérations ont été exercées par Codex sur les
workspaces documentés. `doctor` produit du JSON par défaut : code0 réservé à une
prêteté complète future, code1 DEGRADÉ, code2 BLOCKED. Le cœur cloud peut fonctionner
avec un diagnostic DEGRADÉ si les dépendances optionnelles/GUI manquent ; un
préflight critique bloqué interdit le démarrage. Aucun modèle n’est téléchargé.

`init` refuse tout dossier existant, les entrées protégées et les symlinks. Il
copie le code, ses configurations nécessaires en lecture et le runtime ; les
compteurs connus sont conservés. `--seed-runtime` permet de réutiliser un runtime
**explicitement autorisé** : fichiers en conflit refusés, compteurs du même jour
fusionnés par maximum, ledgers calcul/modèle et expériences conservés. Des dates
différentes nécessitent une réconciliation explicite, jamais une remise à zéro.

Le défaut initial de packaging (vocabulaire absent de la copie figée) a été
reproduit, corrigé puis vérifié par un vrai lancement. Ne pas réutiliser les
premières copies privées défaillantes ; elles restent des preuves de reproduction.

`start` exige `--activate`, l’intégrité des données préparées et un préflight du
cœur non bloqué. Réseau et Blender exigent leurs flags explicites. Le budget HTTP
reste inférieur ou égal aux limites V10 ; la mission de démonstration est plafonnée
à6, sans réinitialisation. Tous les contrôles du moteur existant restent en place.
Le code exécuté est figé : éditer le dépôt pendant une campagne ne modifie pas son
worker. Un nouveau périmètre après travail déjà réalisé doit être préparé et revu
explicitement à partir du runtime existant ; pas de réutilisation trompeuse d’un DONE.

Le superviseur démarre un processus Python, pas un service. Il suit uniquement ce
processus/groupe, lui laisse le temps borné autorisé et plafonne les redémarrages.
La campagne s’arrête lorsque le travail est achevé ou à sa limite, sans créer des
cycles vides pour gonfler un compteur. `pause`, `resume`, `stop` utilisent le même
lanceur ; stop est terminal jusqu’à une reprise explicitement diagnostiquée.
La pause est coopérative aux frontières des étapes : un appel borné en cours peut
terminer ; ce n’est pas une suspension instantanée de tout calcul. Stop termine
le groupe enfant suivi. Les processus GUI non enfants, Studio et applications
personnelles sont hors périmètre.

## Résultats et interprétation

Dans le laboratoire :

- `guard-status.json`, `guard-events.json` : état indépendant du cœur et tentatives.
- `reports/status.json`, `checkpoint.json` : activité, heartbeat, progression et tâches.
- `reports/report.json`, `report.html`, `MORNING_BRIEF.md` : bilan du worker.
- `runtime/lab/operations/reports/` : BLACK BOX et réparations.
- `vault/` : coffre Obsidian **isolé**, généré par export transactionnel.
- `restore-point/`, `restoration-check/`, `code-manifest.json` : restauration vérifiée.

RUNNING ancien sans heartbeat récent devient STALE. Un PID stocké n’établit pas
la présence de vie. Un état terminal STOPPED n’est pas présenté comme un travail
encore en cours. Un essai Python ne valide pas Roblox ; les primitives Blender ne
valident ni B3/C1 ni le réalisme de la forêt ni Blender5.2.

## Réparations et contrôle indépendant

La reconstruction automatique est limitée à l’index SQLite dérivé, après constat
qu’il est corrompu. L’original est conservé en quarantaine ; le nouvel index est
retesté et les sources protégées doivent être identiques. Deux réservations de
réparation maximum ; au-delà, dossier à revoir. Aucun changement de permission,
installation, code critique ou statut VERIFIED n’est automatique.

```sh
python scripts/eponge_validate.py prepare --source /chemin/depot --manifest /chemin/nouveau-manifeste.json --approve-baseline
python scripts/eponge_validate.py run --source /chemin/depot --manifest /chemin/nouveau-manifeste.json --output /chemin/nouveau-resultat --suite offline
```

L’épinglage est une action opérateur explicite, pas une décision du générateur.
Une suite réellement échouée rend FAIL ; une modification des entrées/tests après
épinglage rend REJECTED. Le runner ne promeut aucune proposition. Le holdout aveugle
et la promotion générale restent non démontrés.

## Rollback et autorisations

Restaurer un snapshot uniquement vers une **nouvelle copie** avec vérification
des empreintes. Ne jamais restaurer par-dessus le runtime actif ou ses compteurs.
Conserver ses ledgers et réconcilier les budgets avant une nouvelle exécution.
Le point initial complet de c93fe9b est conservé dans la livraison privée ; ce code
ancien sait exécuter les CLI V11.2 historiques mais pas le nouveau lanceur.
La bascule automatique de version vivante n’est pas implémentée.

Aucune tâche Windows, service, pare-feu ou alimentation n’a été configuré. Pour
valider le PC réel, une seule action nécessaire : ouvrir le projet dans une session
Codex locale Windows avec accès au terminal/dossier autorisé. Les validations
accessibles devront ensuite être lancées par Codex lui-même. Un lancement au boot
ou un fonctionnement permanent demandera une autorisation distincte, après test.

Le bilan du17 novembre à11h Europe/Paris est un déclenchement **unique côté cloud**,
pas un démarrage Windows. Sa lecture des artefacts dépend de leur disponibilité ;
le prompt impose de signaler BLOCKED s’ils manquent et de ne lancer aucun nouveau
travail ou publication. Aucun daemon n’est laissé actif par cette livraison.
