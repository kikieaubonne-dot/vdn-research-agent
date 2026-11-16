# Migration additive, Obsidian et rollback

Les notes V11, sessions V10/V11, registre d'expériences et configurations
historiques ne sont pas migrés ni réécrits. Un nouveau contrat
`config/intelligence.json` est désactivé par défaut ; sans ce fichier, les
valeurs prudentes intégrées s'appliquent. Les analyses restent des données
privées sous `lab/ocean/intelligence`, ignorées par Git comme le laboratoire V11.

Avant changement de branche, fermer collecte/MCP et appliquer la
[sauvegarde V11](../v11/BACKUP_MIGRATION.md) incluant knowledge, config, lab et
output. Conserver la copie privée. Ne pas utiliser reset --hard, clean ou
restauration d'anciens compteurs pour obtenir davantage de budget.

Rollback fonctionnel : mettre `intelligence.enabled=false`, arrêter le
processus concerné, puis utiliser `agent.v11` et `vdn_mcp.py --v11`. Les anciennes
interfaces restent disponibles. Archiver les nouvelles analyses/configuration
avant retour au code V11 ; ne pas effacer les preuves ni remplacer ses sessions.
Les états nouveaux sont attachés aux affirmations, pas imposés aux anciens
statuts de connaissances. Une analyse périmée peut être consultée comme historique,
mais doit être réévaluée avant réutilisation.

Les index d'embeddings sont dérivés. Un changement de digest/modèle exige une
archive explicite de `lab/ocean/intelligence/embeddings.json`, puis réindexation.
Les résultats et journaux ne sont pas des sources du RAG. Une corruption est
diagnostiquée, sans écraser la révision concernée.

## Export privé explicite

L'export V11 courant reste disponible. Pour inclure la nouvelle page de mémoire :

```powershell
$vault = "C:\Users\kikie\Documents\VDN-Obsidian"
& $python -m agent.v111 sync --destination $vault --include-intelligence
& $python -m agent.v111 sync --destination $vault --include-intelligence --apply
```

La première commande simule. Les mécanismes V9 de conflits, sauvegarde et reprise
restent utilisés. La page réservée `knowledge/_VDN-Intelligence.md` ne contient
pas les corps des sources et est exclue du corpus RAG ; les analyses privées ne
sont incluses que si l'opérateur le demande. Pour rollback, conserver l'identifiant
de transaction retourné :

```powershell
& $python -m agent.v111 sync --destination $vault --rollback TRANSACTION_ID
& $python -m agent.v111 sync --destination $vault --rollback TRANSACTION_ID --apply
```

Le coffre personnel n'a pas été modifié dans cette livraison. Export, exclusion
des résumés, conflits et rollback sont vérifiés dans des destinations isolées.
