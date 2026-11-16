# Claude Desktop et MCP stdio

Configurer un clone local stable, puis redémarrer Claude Desktop. Exemple dans
`%APPDATA%\Claude\claude_desktop_config.json`, en remplaçant les chemins par
ceux du clone et de son environnement Python :

```json
{
  "mcpServers": {
    "eponge": {
      "command": "C:\\Users\\kikie\\Documents\\vdn-research-agent\\.venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\kikie\\Documents\\vdn-research-agent\\vdn_mcp.py",
        "--root", "C:\\Users\\kikie\\Documents\\vdn-research-agent",
        "--v11"
      ],
      "env": {"PYTHONUTF8": "1"}
    }
  }
}
```

Ce serveur de lecture fournit **22 outils** : 13 V10 conservés et neuf Océan :
`search_ocean`, `get_ocean_card`, `get_ocean_brief`, `plan_ocean`, `ocean_status`,
`compare_techniques`, `prepare_ocean`, `run_ocean`, `control_ocean`.
Les outils modifiants retournent un refus sans capacité hôte. Pour autoriser
explicitement les recherches, ajouter `--allow-research` aux arguments ; pour
le laboratoire historique, `--allow-experiments` séparément. Le réseau exige
encore `network_enabled=true`, `apply=true` et `allow_network=true`. Ces options
ne donnent aucun outil d'édition de Blender, Studio ou du jeu publié.

Parcours recommandé à ajouter aux instructions de projet Claude :

> Avant une décision technique importante pour Le Voisin de Noël, consulter
> `get_ocean_brief` avec l'objectif précis. Distinguer extraits sourcés,
> propositions d'ingénierie, versions inconnues et expériences réellement
> mesurées. Lire les fiches utiles avec `get_ocean_card(detailed=true)` ; consulter
> les échecs du laboratoire. Préparer les tests manquants et demander les
> autorisations de modification du projet dans l'outil approprié. Ne pas
> transformer un candidat ou un résultat limité en technique vérifiée.

Exemples d'arguments :

```json
{"goal":"Pourquoi mon personnage se bloque contre les sapins ?","token_budget":1800}
```

```json
{"note_id":"vdn-ocean-54fe16e8e5a3e6ea5304","detailed":true}
```

Vérifier le schéma retourné par `tools/list` pour chaque outil. Le briefing
est borné, puis les détails se chargent à la demande. Le serveur ne force pas
Claude à le consulter ; l'usage réel dans Desktop et le temps gagné n'ont pas
été mesurés. Le test d'intégration lance réellement le processus stdio depuis
un autre répertoire : initialize, notification initialized, tools/list,
tools/call, contenu JSON et structuredContent sous protocole 2025-06-18.
Claude Desktop et ses clics d'interface n'étaient pas disponibles ici.

Le fichier `vdn_mcp.py` absolu évite une dépendance au répertoire courant.
Pointer `--root` vers le clone actif, pas vers l'export Obsidian incomplet en
configuration. Les anciens modes sans `--v11` gardent leurs interfaces.
