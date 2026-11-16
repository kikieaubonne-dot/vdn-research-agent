# V10 — mémoire, Obsidian et MCP

## Registre local

Les nouvelles données privées sont dans `lab/`, ignoré par Git. Chaque expérience
a un UUID, une spécification initiale hachée et un journal numéroté d’événements
JSON. Chaque événement contient l’état complet, l’empreinte du précédent, une
révision et un identifiant de requête. Créer le même UUID avec la même spécification
est idempotent ; un contenu différent est refusé. Pour les résultats CLI/MCP,
fournir un `request_id` UUID stable permet de rejouer après interruption.

Cycle : `HYPOTHESIS → PLANNED → RUNNING → FAILED | PARTIAL_SUCCESS | SUCCESS`.
Un résultat peut repartir vers `PLANNED` pour un nouvel essai ; l’historique des
erreurs et conditions reste présent. `SUCCESS → VERIFIED` exige une revue opérateur
explicite. `OBSOLETE` termine une expérience hors exécution. Pas de promotion
directe vers un état de résultat ou de vérification.

```sh
python -m agent.v10 create --input examples/v10/experiment.json --dry-run
python -m agent.v10 create --input examples/v10/experiment.json --apply
python -m agent.v10 find "foliage" --status FAILED
python -m agent.v10 get EXPERIMENT_UUID --detailed
```

Le contexte recherche aussi les échecs d’essais précédents, même après une réussite.
Les résultats de recherche sont bornés et lexicaux, pas exhaustifs. Une candidate
revue est toujours accompagnée de conditions ; aucune technique « meilleure en
toutes circonstances » n’est déduite.

Les preuves sont déposées dans `lab/inbox/`, puis copiées telles quelles sous
un nom contenant leur SHA256. Types autorisés : JSON, CSV, TXT, PNG, JPG/JPEG,
WEBP, OBJ ; maximum 8 Mo. L’analyse visuelle V10 accepte seulement PNG.
Une preuve `self_generated` ne suffit pas à vérifier une expérience. Les types
`external_measurement` et `external_capture` déclarent une provenance opérateur,
ils ne prouvent pas cryptographiquement qu’un logiciel externe a tourné.

Après inspection des mesures/captures réelles et documentation des versions,
l’opérateur peut utiliser :

```sh
python -m agent.v10 review EXPERIMENT_UUID --reviewer "Nom" --condition "Appareil, version et limites réellement testés" --attest-human-inspection --apply
```

L’attestation est une décision humaine sous conditions, pas une certification
indépendante du moteur. Les tests de ce chemin emploient des preuves synthétiques
étiquetées fixtures : **zéro procédure Roblox vérifiée** dans cette livraison.
Le MCP et les tâches automatiques ne disposent pas de cette commande de revue.

## Obsidian

L’export V9 est conservé avec conflits utilisateur, sauvegardes, journal, reprise
et rollback. Choisir un dossier **séparé** du clone ; ouvrir son sous-dossier
`knowledge` comme coffre. `--include-lab` ajoute explicitement les fiches.

```sh
python -m agent.v10 sync --destination "C:\VDN-Export" --include-lab --dry-run
python -m agent.v10 sync --destination "C:\VDN-Export" --include-lab --apply
# Utiliser le champ transaction de la réponse pour un retour arrière :
python -m agent.v10 sync --destination "C:\VDN-Export" --rollback TRANSACTION_UUID --apply
```

Les fiches `_VDN-Experience-UUID.md` possèdent YAML, statut, révision, empreinte,
provenance, conditions et lien vers `_VDN-Experiences`. Le hub est la section
logique `07 — Expériences` ; la structure recommandée 00–99 peut être créée par
l’utilisateur sans déplacement des 110 notes existantes. Les pages générées
sont exclues du RAG de sources : une réponse ou une expérience locale ne devient
pas une source indépendante par son export. Le JSON contient dates des événements
dans le journal local ; la fiche expose sa révision et son empreinte courantes.

Le bundle transporte les notes et les configs autorisées V9, **pas** `lab/inbox`,
les captures, le registre ou les clés. Le MCP V10 doit viser le clone pour accéder
à la mémoire active. Un MCP V9 peut continuer à lire le bundle. Aucune synchronisation
du coffre personnel ni ouverture de l’application Obsidian n’a été effectuée.
Les tests utilisent uniquement des destinations temporaires.

Sauvegarder régulièrement `lab/` complet (journal et preuves) vers un emplacement
privé ; conserver aussi les sauvegardes d’export. Aucun upload implicite. Ne pas
modifier à la main les événements pour « réparer » un résultat. Une corruption
arrête la lecture ou apparaît en diagnostic ; restaurer une copie connue et
inspectée. Les fichiers temporaires laissés avant commit ne deviennent pas des
événements valides. Un verrou fichier résiduel peut rester 7200 s après un arrêt
forcé ; le verrou système protège les cycles actifs.

## MCP et Claude

Le serveur reste stdio. Le mode par défaut garde les sept outils V8 ; `--v9` en
garde huit. `--v10` garde ces outils et en ajoute cinq : `get_experiment_context`,
`get_experiment`, `prepare_experiment`, `start_experiment`,
`record_experiment_result`. Réponses compactes par défaut ; `detailed=true` pour
les deux outils de lecture. Le briefing V10 inclut une mémoire bornée des échecs
et candidates revues, en respectant le budget de réponse.

Configuration Claude Desktop, adapter les chemins absolus :

```json
{
  "mcpServers": {
    "vdn-v10": {
      "command": "C:\\VDN\\vdn-research-agent\\.venv\\Scripts\\python.exe",
      "args": ["C:\\VDN\\vdn-research-agent\\vdn_mcp.py", "--root", "C:\\VDN\\vdn-research-agent", "--v10"]
    }
  }
}
```

Ajouter `--allow-experiments` seulement pour autoriser les écritures demandées
par Claude. Sans lui, préparation, démarrage et résultats sont refusés. Les outils
ne collectent pas sur Internet, ne changent pas le code et ne lancent pas Studio.
Ils n’importent pas de chemin arbitraire ; un résultat référence des IDs de preuves
déjà importées par l’opérateur. Aucun outil `review` n’est exposé. Les sorties
conservent erreurs, limites, sources et incertitudes. Contrat stdio réellement
testé dans un sous-processus lancé depuis un autre dossier ; Claude Desktop réel
et sa configuration sur le PC utilisateur restent à tester.
