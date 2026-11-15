# VDN V4.1 — Diagnostic des récompenses nulles

**Patch non destructif** : copier uniquement les dossiers `agent/`, `tests/`, `.github/` de ce ZIP à la racine du dépôt. Conserver `knowledge/`, `output/`, `config/` et les autres fichiers. Ne pas supprimer `output/meta_state.json` : les sessions précédentes restent consultables (les nouvelles colonnes afficheront `?` pour l'historique non instrumenté).

## Modifications
- Différencie `results=0` (aucun résultat), `accepted=0` (filtrage), `new=0` (déjà connu).
- Affiche les sessions vides et les résultats retournés par stratégie.
- Ajoute les diagnostics de la dernière exécution au rapport `output/meta_report.md`.
- Préserve les récompenses existantes : **ce patch ne prétend pas améliorer la pertinence**, il rend les causes de zéro observables.
- Tests de régression sur les diagnostics.

## Vérification
1. `python -m unittest discover -s tests -v`
2. GitHub Actions > VDN Research Agent > Run workflow.
3. Lire `output/last_run.json` et `output/meta_report.md`.
4. Si toutes les lignes ont `Retournés = 0`, vérifier les requêtes et les réponses des moteurs; si `Retournés > 0` mais `Acceptés = 0`, vérifier le filtre; si `Acceptés > 0` mais `Nouveaux = 0`, déduplication ou saturation.

**Étape suivante** : benchmark annoté de pertinence, puis RAG SQLite FTS5 pour Claude. Ne pas confondre réussite du workflow et qualité des résultats.
