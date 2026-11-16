# Trois démonstrations reproductibles

Ces sorties proviennent des **94 notes réelles** du corpus `9abf775`, sur copie
temporaire. `corpus.json` conserve les empreintes des 106 fichiers. Aucune fiche
n'a été inventée pour compléter les lacunes, aucun logiciel graphique exécuté.

| Scénario | Entrée et sortie | Résultat observé |
|---|---|---|
| Sapin enneigé | [snowy_tree.json](snowy_tree.json) | Références Roblox SurfaceAppearance, LOD et atlas ; plan de 11 branches, lacunes conservées |
| Squelette personnalisé | [custom_skeleton.json](custom_skeleton.json) | Fiche des glitches/RootPart première ; limites et absence de validation visibles |
| Forêt complète | [snowy_forest.json](snowy_forest.json) | 11 sous-problèmes, ordre topologique, sources par branche et prérequis non vérifiés |

Pour le sapin, les branches recherchent géométrie, feuillage, UV, matériaux,
neige, export et performances. L'existence de références candidates ne signifie
pas qu'une procédure complète existe ; `gaps`, `query_not_fully_matched`,
`validated_procedure: false` et les limites de compatibilité le signalent.
Une ressource Babylon.js est classée `other_engine`, pas prête pour Roblox.
Les premières références du scénario forêt sont des ressources Roblox.

```sh
python -m bench.demonstrate_v8 --root . --output-dir work/demos-v8
```

Un test exécute deux fois la démonstration et compare les quatre sorties octet
par octet. Les résultats pourraient évoluer après ajout de fiches : conserver
le manifeste et la révision du corpus lors des comparaisons.
