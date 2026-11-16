# Obsidian : exporter une bibliothèque, conserver le laboratoire privé

Le clone est la bibliothèque active ; `C:\Users\kikie\Documents\VDN-Obsidian`
est une destination séparée. Le code réutilise l'export V9 : manifeste,
transactions, sauvegardes, conflits et rollback. Aucune écriture n'a été faite
dans le coffre personnel pendant cette livraison ; la validation utilise des
destinations temporaires.

```powershell
$vault = "C:\Users\kikie\Documents\VDN-Obsidian"
& $python -m agent.v11 sync --destination $vault --dry-run
# Lire les différences et conflits avant l'application :
& $python -m agent.v11 sync --destination $vault --apply
```

Ouvrir le sous-dossier `knowledge` de cette destination dans Obsidian, comme en
V9. Les fiches Ocean sont dans `knowledge/ocean`. Pages `_ocean_*` : tableau de
bord, découvertes, lacunes, sources, contradictions, obsolescence et recherches.
Les pages réservées et résumés ne deviennent pas des sources indépendantes dans
le RAG. Une source supporte une affirmation ; un lien vers une autre synthèse
n'est pas une nouvelle preuve.

Le laboratoire privé n'est pas exporté par défaut. Pour inclure explicitement
ses pages de résultats/échecs et les hubs historiques :

```powershell
& $python -m agent.v11 sync --destination $vault --include-lab --dry-run
& $python -m agent.v11 sync --destination $vault --include-lab --apply
```

Inspecter les contenus avant de partager un coffre. Les rapports personnels
peuvent contenir des détails du projet. L'export ne publie aucun service et ne
lit pas les secrets `.env`.

Si une note exportée a été modifiée manuellement, l'export retourne un conflit
et conserve la modification. Résoudre explicitement dans Obsidian, puis
resimuler ; aucune option de force nouvelle n'est ajoutée. Conserver le champ
`transaction` de chaque résultat de synchronisation :

```powershell
& $python -m agent.v11 sync --destination $vault --rollback TRANSACTION_ID --dry-run
& $python -m agent.v11 sync --destination $vault --rollback TRANSACTION_ID --apply
```

Le rollback vérifie les empreintes avant restauration et archive les créations
au lieu de supprimer des notes. Les conflits, export incrémental et reprise
sont testés. Les 115 fichiers de la synchronisation personnelle antérieure
ne sont pas un résultat reproduit ici.
