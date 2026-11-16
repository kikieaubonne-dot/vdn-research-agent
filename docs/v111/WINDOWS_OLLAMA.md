# Windows, diagnostic et synthèse

Sauvegarder un clone existant selon [migration](MIGRATION.md). Installation
neuve : Python 3.11+, Git, disque local NTFS ; aucune dépendance pip ajoutée.

```powershell
git clone --branch codex/eponge-intelligence-v11-1 https://github.com/kikieaubonne-dot/vdn-research-agent.git
Set-Location vdn-research-agent
$env:PYTHONUTF8 = "1"
py -3.11 -m venv .venv
$python = Join-Path $PWD ".venv\Scripts\python.exe"
& $python -m tests.offline
& $python -m tests.personal_config
& $python -m agent.v111 diagnose
& $python -m agent.v111 synthesize "Mes sapins Roblox sont artificiels, leurs collisions gênent le joueur et le rendu de nuit manque de réalisme"
```

Sans `--apply` : analyse déterministe en lecture, aucun modèle ni écriture.
Pour conserver l'analyse et ses preuves dans la mémoire privée :

```powershell
$question = "Mes sapins Roblox sont artificiels, leurs collisions gênent le joueur et le rendu de nuit manque de réalisme"
$result = (& $python -m agent.v111 synthesize $question --apply | ConvertFrom-Json)
$key = $result.key
& $python -m agent.v111 get $key
& $python -m agent.v111 search "collisions et réalisme des sapins"
& $python -m agent.v111 brief $question --key $key --token-budget 1800
```

Le clone doit disposer de snapshots V11 pour contrôler une source originale.
Les notes seules restent secondaires. L'analyse ne télécharge pas elle-même
les sources manquantes : utiliser les objectifs de collecte V11 autorisés.

## Installer/configurer Ollama, facultatif

Installer manuellement depuis [Ollama Windows](https://ollama.com/download/windows).
Choisir le modèle et vérifier sa licence avec le [guide de sélection](MODELS.md).
Le dépôt ne télécharge aucun poids. Les commandes suivantes ne lancent pas un pull :

```powershell
ollama --version
ollama list
ollama ps
$model = Read-Host "Nom exact d'un modèle déjà installé, tag compris"
ollama show $model
& $python -m agent.v111 diagnose --probe --model $model
```

`--probe` interroge le service et consomme des réservations HTTP locales dans
le compteur commun. Le diagnostic affiche RAM totale/disponible, GPU/VRAM libre
si nvidia-smi existe, working sets/RSS Ollama si observables, modèles chargés et
VRAM déclarée par Ollama. Il ne tue aucun processus. Taille des poids, KV cache,
contexte et applications Studio/Blender/Unreal doivent tous être considérés.

Activer uniquement le **nouveau** contrat, sans réécrire v10.json/ocean.json :

```powershell
$env:VDN_SELECTED_MODEL = $model
$configure = @'
import json, os
from pathlib import Path
p = Path("config/intelligence.json")
c = json.loads(p.read_text(encoding="utf-8"))
c.update(enabled=True, compact_model=os.environ["VDN_SELECTED_MODEL"], economy=True)
p.write_text(json.dumps(c, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
'@
$configure | & $python -
& $python -m agent.v111 synthesize $question --apply --allow-model
```

Le nom doit figurer exactement dans `ollama list` : aucune résolution de tag
par téléchargement. Modèle absent, mémoire/temps insuffisants, contexte trop
court, sortie invalide ou quota atteint : candidat déterministe conservé et
critique consultable. Les quotas V11 restent en vigueur, notamment une
génération par jour par défaut. Ne pas modifier les compteurs pour réessayer.
Ctrl+C annule coopérativement et conserve les preuves/réservations acquises.

Le contexte livré est 2 048 tokens estimés, sortie au plus 512 tokens,
timeout 15 s dans le plafond d'opération. Une analyse complexe peut exiger un
contexte configuré plus grand après mesures ; le code limite à 8 192 et ne
promet pas que cela tient en VRAM. Le mode économie conserve le modèle compact.

## Embeddings et comparaison

Configurer explicitement `ocean.json.semantic` comme en V11, avec un modèle
d'embedding déjà installé prenant `/api/embed` et un endpoint loopback littéral.

```powershell
& $python -m agent.v111 embed-index
& $python -m agent.v111 embed-index --apply --max-items 10
& $python -m agent.v111 synthesize $question --apply --allow-model --retrieval semantic
& $python -m agent.v111 synthesize $question --apply --allow-model --retrieval hybrid
& $python -m bench.evaluate_intelligence --output work\quality.json
& $python -m bench.evaluate_intelligence --models $model --allow-model --max-cases 1 --output work\model-quality.json
& $python -m bench.evaluate_intelligence --with-embeddings --allow-model --output work\retrieval-quality.json
```

L'index dérivé est lié au digest installé, aux passages et à leur contenu.
Un changement de modèle exige d'archiver explicitement cet index avant de le
reconstruire. Service/index indisponible : retour lexical diagnostiqué.
Les benchmarks réels restent soumis aux mêmes limites : un rapport peut donc
être partiel et contenir un arrêt de budget. Aucun gain IA n'a été mesuré ici.
