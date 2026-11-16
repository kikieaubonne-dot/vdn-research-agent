# Exécution Windows V9, sans Claude

Python 3.12 et Git ; aucune dépendance pip. Les commandes sont documentées pour
Windows mais testées ici sous Linux. Le script PowerShell n'a pas été exécuté
sur Windows. Ne pas remplacer un dossier de travail ou un coffre existant.

```powershell
git clone --branch codex/knowledge-factory-v9 https://github.com/kikieaubonne-dot/vdn-research-agent.git C:\VDN\vdn-research-agent
Set-Location C:\VDN\vdn-research-agent
py -3.12 -m venv .venv
$env:PYTHONUTF8 = "1"
.\.venv\Scripts\python.exe -m tests.offline
.\.venv\Scripts\python.exe -m agent.v9 gaps
.\.venv\Scripts\python.exe -m agent.v9 brief "Comment poursuivre un joueur parmi des obstacles Roblox ?"
.\.venv\Scripts\python.exe -m agent.v9 brief "Diagnostiquer un squelette personnalisé Roblox" --mode detailed --token-budget 4000
```

Suivre ensuite [le guide Obsidian](V9_OBSIDIAN.md). Pour préparer une collecte
ponctuelle :

```powershell
.\.venv\Scripts\python.exe -m agent.v9 research --max-items 1
# Simulation ; aucun acces reseau.
.\.venv\Scripts\python.exe -m agent.v9 research --max-items 1 --apply
```

La collecte privilégie P0/P1 et s'arrête sur erreur, budget, doublons stagnants ou
limite de tentatives. Les notes connues restent inchangées. Un refus réseau ou
robots n'est pas contourné. Aucun service payant n'est ajouté.

Pour enchaîner manuellement recherche et synchronisation, après revue des chemins :

```powershell
.\scripts\run_v9_cycle.ps1 -ProjectRoot C:\VDN\vdn-research-agent -Bundle C:\VDN-Obsidian -Python C:\VDN\vdn-research-agent\.venv\Scripts\python.exe
# Simulation par defaut ; ajouter -Acquire et/ou -ApplySync pour agir explicitement.
```

**Aucune tâche récurrente n'est installée.** Le workflow GitHub Actions existant
reste inchangé ; il utilise déjà des quotas et un verrou. Avant une éventuelle
planification Windows, autoriser explicitement la récurrence, éviter deux clones
écrivant le même coffre et observer plusieurs cycles manuels. Ce n'est pas requis
pour V9 et cela n'a pas été activé.

Si le cache SQLite est corrompu, arrêter d'abord les clients MCP qui l'utilisent :

```powershell
.\.venv\Scripts\python.exe -m agent.v9 repair-index
.\.venv\Scripts\python.exe -m agent.v9 repair-index --apply
```

L'ancien cache est archivé, les fiches ne sont pas modifiées. Pour Claude Desktop,
reprendre `CLAUDE_DESKTOP_V8.md` et ajouter `--v9` dans les arguments ; `--root`
peut pointer sur le bundle. Aucun quota Claude n'est utilisé pour ces opérations.
