# Sauvegarde, migration additive et rollback

La V11 ajoute `config/ocean.json`, `agent/ocean*`, une enveloppe d'objectif et
des fiches `vdn.knowledge/11`. Elle n'altère pas le schéma des sessions V10 ni
les 110 Markdown historiques. Le manifeste [preservation.json](preservation.json)
compare leurs octets à `4e2624f`. Les deux fiches créées sur le PC Windows sont
absentes de cette base : les sauvegarder dans le clone personnel.

Avant changement de branche, fermer les processus de collecte/MCP et faire
une copie locale privée. Exemple PowerShell, depuis le clone actuel :

```powershell
$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$backup = Join-Path (Split-Path $PWD -Parent) ("vdn-backup-" + $stamp)
robocopy $PWD.Path $backup /E /XJ /XD .git .venv __pycache__ /R:1 /W:1
if ($LASTEXITCODE -ge 8) { throw "Sauvegarde incomplète : inspecter robocopy" }
git status --short
git rev-parse HEAD
```

La copie inclut `lab`, `output`, `config`, `knowledge` et les secrets locaux
éventuels : la garder privée, jamais dans une PR. Copier séparément le coffre
Obsidian si nécessaire. La base SQLite dérivée peut être reconstruite, mais les
sessions, journaux, reçus et compteurs sont des données à préserver.

`python -m agent.v11 legacy-view` expose une correspondance en lecture seule
des statuts historiques. Aucune migration massive ni réécriture pour ajouter
un nouveau statut. `adopt UUID --apply` crée uniquement l'enveloppe et garde
les octets de session ; l'état source ne gagne aucun budget.

Rollback d'une adoption : arrêter les processus, archiver l'enveloppe
`lab/ocean/goals/UUID.json` dans la sauvegarde privée, puis utiliser le CLI V10
sur la même session. Conserver les nouvelles fiches comme candidates séparées.
Rollback du code : après sauvegarde et examen de `git status`, revenir à la
branche V10 souhaitée ; ne pas effacer les runtime ignorés par Git. Les données
Océan peuvent rester archivées pour retour ultérieur. Ne pas restaurer une
ancienne copie de compteurs pour obtenir artificiellement du budget.

Le rollback Obsidian est transactionnel et distinct, voir [guide](OBSIDIAN.md).
La reprise après interruption et l'adoption sans modification de session sont
testées ; un rollback complet sur le PC personnel n'a pas été exécuté ici.
