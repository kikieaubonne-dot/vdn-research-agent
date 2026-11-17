# Acceptation — ne pas confondre les laboratoires

| Étape | Résultat attendu | Statut actuel |
|---|---|---|
| Intégrité du paquet | Manifestes et empreintes correspondent | Vérifier via WINDOWS/setup.py verify |
| Logiciel historique et régressions nouvelles | Suites Linux hors ligne et personnelles séquentielles | Résultat exact dans PROOFS/test-summary.json ; aucun résultat Windows inféré |
| Stdio relocalisé |27 contrats identiques, lectures réussies, écriture refusée | Testable par setup.py test-mcp |
| Windows réel | Python3.11, chemins/UTF-8/processus fonctionnels | NON TESTÉ ici |
| Desktop réel | Outils visibles et consultations dans l'application | NON TESTÉ ici |
| Builder/driver Luau | Uniquement nouveau modèle de lab, contrôle de cible, événements validés | PRÉPARÉS, NON TESTÉS dans Studio |
| Geste Blender |25 poses,2gabarits,2s, critères interop-2 | VALIDÉ en environnement limité4.3.2/GLB |
| Rig/Studio | Animation sur copie du rig cible et pendant gameplay | NON TESTÉ |
| Prologue A→E | Partie jouable, objectifs lisibles, transitions réelles | NON EXÉCUTÉ |
| Fin F | Aucune fin choisie automatiquement | UNKNOWN conservé |
| Quota Claude A/B | Tokens/appels/temps et qualité issus d'observations réelles | NON MESURÉ |

Consigner build/appareil, fichiers, scénario, résultat, traces, limites et rollback. Les critères de rythme restent des hypothèses. Les26 autres outils ne doivent pas perdre leur contrat pendant le test d'un seul parcours. Ne pas promouvoir automatiquement un rapport client en VERIFIED/HUMAN_APPROVED.
