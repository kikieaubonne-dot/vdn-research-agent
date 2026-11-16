# Installer et utiliser V11 sous PowerShell

Python **3.11+**, Git, clone local NTFS. Le cœur ne demande aucun `pip install`.
Les commandes ci-dessous ne créent aucune tâche Windows. Conserver le clone
actuel si ses sessions/fiches ne sont pas commitées : lire d'abord la
[sauvegarde](BACKUP_MIGRATION.md). Ne pas utiliser `git reset --hard` ni `clean`.

Pour une installation neuve :

```powershell
git clone --branch codex/eponge-ocean-v11 https://github.com/kikieaubonne-dot/vdn-research-agent.git
Set-Location vdn-research-agent
$env:PYTHONUTF8 = "1"
py -3.11 -m venv .venv
$python = Join-Path $PWD ".venv\Scripts\python.exe"
& $python -m tests.offline
& $python -m tests.personal_config
& $python -m agent.v11 hardware
& $python -m agent.v11 status
& $python -m agent.v11 plan "Créer une forêt d'épicéas enneigée nocturne dans Roblox"
```

Clone existant **après sauvegarde**, vérifier `git status`, puis `git fetch origin`
et `git switch codex/eponge-ocean-v11`. Git peut refuser une modification locale
en conflit : la conserver dans la sauvegarde, résoudre explicitement ; ne pas
la supprimer pour forcer la mise à jour.

## Recherche manuelle autorisée

Le `network_enabled=true` personnel est conservé. Pour un clone neuf, l'activer
explicitement dans `config/v10.json` ; les autres champs restent identiques :

```powershell
$enableNetwork = @'
import json
from pathlib import Path
p = Path("config/v10.json")
c = json.loads(p.read_text(encoding="utf-8"))
c["network_enabled"] = True
p.write_text(json.dumps(c, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
'@
$enableNetwork | & $python -
$goal = (& $python -m agent.v11 prepare "Créer une forêt d'épicéas enneigée nocturne dans Roblox avec collisions et lampe torche" --apply | ConvertFrom-Json)
$id = $goal.id
& $python -m agent.v11 run $id --dry-run
& $python -m agent.v11 run $id --apply --allow-network
& $python -m agent.v11 status
```

Relancer **le même `$id`** pour le tick suivant. `config/ocean.json.enabled=false`
désactive les modes automatiques seulement ; la recherche manuelle explicite
reste possible. Aucun modèle requis. Le réseau réel Windows n'a pas été testé
ici ; la CI Windows exécute des transports contrôlés sans socket.

`BUDGET_STOP` par tick autorise un tick ultérieur ; par session impose de
conserver la limite. Le quota journalier revient le jour suivant, sans effacer
le compteur historique. `ERROR` exige d'inspecter `last_collection`, trace
`lab/ocean/web-trace.jsonl` et unités avant reprise. Des pages refusées ou sans
preuve pertinente ne sont pas remplacées par des résultats inventés. Ne pas
créer en boucle des sessions pour contourner les limites.

```powershell
& $python -m agent.v11 control $id pause --apply
& $python -m agent.v11 control $id resume --apply
& $python -m agent.v11 run $id --apply --allow-network
# Arrêt terminal de cet objectif, à utiliser lorsqu'il doit être abandonné :
# & $python -m agent.v11 control $id stop --apply
& $python -m agent.v11 search "Pourquoi mon personnage se bloque contre les sapins ?"
& $python -m agent.v11 brief "Collisions des troncs et branches dans Roblox" --token-budget 1800
```

## Session Windows V10 existante

```powershell
$old = "4f817a22-a945-4f6d-8b49-ec8f2d9d8aa2"
& $python -m agent.v11 adopt $old --dry-run
& $python -m agent.v11 adopt $old --apply
& $python -m agent.v11 status
# Consultation V10 toujours disponible :
& $python -m agent.v10 research-run $old --dry-run
```

L'adoption ajoute une enveloppe ; aucun compteur ni fichier de session n'est
réécrit. Avec **12 HTTP/12** déjà consommés, l'adoption ne donne aucun appel
supplémentaire. Les deux fiches Windows signalées sont à conserver dans leur
clone : absentes de ce checkout, elles n'ont pas été inspectées ici. Un nouvel
objectif distinct peut traiter des lacunes restantes dans les plafonds normaux,
après examen des résultats existants ; pas de remise à zéro de l'ancienne session.

Voir [Claude/MCP](CLAUDE_MCP.md), [Obsidian](OBSIDIAN.md),
[modèles](MODELS.md), [autonomie](AUTONOMY.md) et [laboratoire](LAB.md).
