# Obsidian V9 — export sûr et preuve locale

Les notes existantes sont déjà compatibles Obsidian. **Aucune migration n'est
nécessaire** : on peut ouvrir directement `knowledge/`. Le bundle permet une
copie séparée contrôlée, avec sauvegardes, sans toucher au dépôt source.

```text
C:\VDN-Obsidian\
  knowledge\              ← ouvrir CE dossier comme coffre Obsidian
    _VDN-Accueil.md        ← navigation de production
    _VDN-Lacunes.md        ← recherches, validation proposée et liens
    forest\ ...           ← structure historique conservée
    roblox\ ...           ← nouvelles candidates
  config\                 ← 3 JSON autorisés, hors coffre
  .vdn-sync\               ← manifeste, transactions, backups et archives
  output\                 ← index dérivé et verrou, hors coffre
```

## Vérifier puis appliquer sur le PC propriétaire

Avant une écriture réelle, vérifier le chemin absolu et les droits ; conserver
une sauvegarde personnelle. Aucun coffre réel n'a été identifié ou écrit par Codex.
Le dossier destination doit être séparé du dépôt source. Depuis le dépôt :

```powershell
python -m agent.v9 sync --destination C:\VDN-Obsidian
# Examiner le JSON : creations, mises a jour, conflits et transaction en attente.
python -m agent.v9 sync --destination C:\VDN-Obsidian --apply
python -m agent.v9 sync --destination C:\VDN-Obsidian
```

Le dernier passage doit afficher `unchanged` s'il n'y a rien de nouveau. Les
réglages personnels `.obsidian/`, les fichiers utilisateur non suivis et les
notes modifiées ne sont pas écrasés. Un conflit bloque toute nouvelle transaction.
Les fichiers retirés du dépôt source restent dans le bundle ; aucune suppression.

## Reprise et retour arrière

Une interruption laisse une transaction préparée. Relancer la même commande avec
`--apply` reprend son instantané ; relancer ensuite pour les éventuelles nouveautés.
Les modifications de destination survenues entre-temps produisent un conflit.

```powershell
python -m agent.v9 sync --destination C:\VDN-Obsidian --rollback UUID-DE-LA-TRANSACTION
python -m agent.v9 sync --destination C:\VDN-Obsidian --rollback UUID-DE-LA-TRANSACTION --apply
```

Seule la dernière transaction validée peut être annulée. Les anciennes versions
sont restaurées depuis les backups ; les nouvelles copies sont déplacées dans
`.vdn-sync/archives/`, conservées plutôt que supprimées. Des changements utilisateur
après synchronisation bloquent le retour arrière et restent intacts.

## Lecture via MCP du bundle

```powershell
python C:\VDN\vdn-research-agent\vdn_mcp.py --root C:\VDN-Obsidian --v9
```

Le serveur hérite des outils V8 et ajoute `get_task_brief(task, mode, token_budget)`.
Les lectures peuvent créer/rafraîchir l'index dérivé `output/knowledge.db` ; elles
ne réécrivent pas les Markdown. Les pages `_VDN-` sont exclues de l'index des fiches.
Les expériences privées ne sont pas exportées par défaut.

## Ce qui est réellement démontré

`docs/demos/v9/vault_validation.json` constate 112 Markdown exportés, toutes les
empreintes sources conformes, aucun lien généré cassé et un second sync inchangé.
Les six fichiers de démonstration prouvent la lecture API/MCP en sous-processus.
**L'application Obsidian n'a pas été ouverte, Windows n'a pas été testé et aucun
coffre réel n'a été synchronisé.**
