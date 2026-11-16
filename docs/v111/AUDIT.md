# Audit et reprise V11.1

Base vérifiée : `04a3c4c874934bbf670e84923c9411448cfa0dae`, PR #6,
branche de travail `codex/eponge-intelligence-v11-1`. À la reprise après les
erreurs de connexion signalées, les sept nouveaux modules/CLI, benchmark,
configuration et tests étaient présents sur disque, sans commit V11.1.
Aucune reconstruction n'a été nécessaire. La cause du dysfonctionnement de
l'interaction distante n'est pas établie par les journaux du dépôt.

Les preuves déjà conservées montraient : baseline 335 tests, suite intermédiaire
365 tests et 34 nouveaux tests ciblés réussis. Les versions intermédiaires,
sources et journaux privés restent dans `work/` ; ils ne sont ni effacés ni
présentés comme résultats de la version finale.

Réutilisé : corpus protégé, ResearchQueue/Budget/verrou racine, transport V11,
adaptateur d'embeddings, comptabilité modèles/coûts, registre LabStore,
MCP stdio, exports et rollback V9/V11. Les 335 tests ne sont pas modifiés.

Lacunes V11 : preuve réduite à une citation courte, modèle facultatif peu
structuré, critique limitée, pas de registre d'affirmations avec offsets ;
qualité des modèles/embeddings testée uniquement par fixtures. La V11.1 ajoute
les étapes manquantes dans un pipeline unique, sans essaim d'agents.

Diagnostic matériel réel : service Ollama inaccessible, aucun GPU détecté.
Aucun modèle téléchargé ni exécuté. Les catalogues Qwen3 et Gemma 3 ont été
consultés pour vérifier les tags et licences ; leur disponibilité dans un
catalogue ne prouve pas leur installation ni leur qualité sur ce PC.

Un diagnostic local initial a consommé une réservation HTTP. Le fichier runtime
`output/queue.json` a effectué le changement de jour normal de V10 et conserve
ce compteur ; il est laissé local, **exclu du commit**, sans restauration de
compteurs anciens. La démonstration suivante utilise un laboratoire isolé,
copiant les compteurs réels antérieurs puis les incrémentant. Aucun runtime
Windows personnel, historique ou coffre utilisateur n'a été modifié.
