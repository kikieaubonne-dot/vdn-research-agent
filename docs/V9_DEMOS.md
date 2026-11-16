# Six démonstrations observables V9

Commande :

```sh
python -m bench.demonstrate_v9 --root . --output-dir work/demos-v9
```

Le test exécute deux fois les six scénarios, compare les JSON octet par octet et
vérifie la copie, les liens, le second sync et les lectures MCP en sous-processus.

| Scénario | Sortie | Ce qu'elle montre |
|---|---|---|
| A — sapin | [A_sapin.json](demos/v9/A_sapin.json) | sources existantes, candidates graphiques et plan en 11 branches ; validation requise |
| B — rigging | [B_rigging.json](demos/v9/B_rigging.json) | diagnostic en 5 branches, sources RootPart/bones/attachments ; cause non conclue |
| C — forêt | [C_foret.json](demos/v9/C_foret.json) | 11 sous-problèmes, prérequis, références et lacunes |
| D — poursuite | [D_poursuite.json](demos/v9/D_poursuite.json) | nouvelle candidate Pathfinding, architecture proposée, contraintes, protocole non exécuté |
| E — accessoires | [E_accessoires.json](demos/v9/E_accessoires.json) | nouvelle candidate rigide/layered, rig personnalisé et multijoueur restant à tester |
| F — insuffisant | [F_insuffisant.json](demos/v9/F_insuffisant.json) | abstention explicite, aucune procédure inventée |

[Validation du coffre](demos/v9/vault_validation.json) : 112 Markdown, empreintes
conformes, aucun lien généré cassé, seconde synchronisation inchangée. Les objets
`vault_notes`, `mcp_stdio_tested` et `api_mcp_equal` distinguent une lecture réelle
du serveur d'une simple description de test.

Aucun objet graphique, personnage, forêt ou comportement d'IA n'a été exécuté dans
Roblox/Blender. Les sources et propositions ne sont pas des procédures validées.
