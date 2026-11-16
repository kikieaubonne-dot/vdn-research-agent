# Audit V9 indépendant — 16 novembre 2026

Base : `8d83868f461840869c91f2649387b0dbc8652f9e` (V8). PR #1 ouverte
vers main ; PR #2 ouverte vers V7 ; aucune fusion. Branche V9 créée depuis V8.
218 tests reproduits via `python -m tests.offline`, réseau interdit jusque dans
les sous-processus. Benchmark historique V8 : hit@1/@3/@5 et MRR 1,0 sur 10
questions ; développement : hit@3 1,0, MRR 0,847 sur 12 questions. Petit échantillon.

106 fichiers historiques inventoriés par SHA-256 avant modification. Les fichiers
Markdown et les liens Obsidian existent déjà sous `knowledge/`. Le dossier peut
être ouvert directement comme coffre : aucune migration de ces fichiers nécessaire.
Le PC Windows et un coffre Obsidian réel ne sont pas montés dans cet environnement.

| Capacité | Existe | Testée | Limites | Action nécessaire |
|---|---|---|---|---|
| Collecte docs/forum/GitHub | oui | fixtures, garde-fous | quotas manuels partiellement unifiés | réutiliser le transport borné |
| File, reprise, profondeur, stagnation | oui | V7/V8 | pas de lancement depuis plan MCP | conserver, pas de second scheduler |
| Markdown, IDs, sources, index Obsidian | oui | tests V7 | index existants, pas de sync sûre démontrée | exporter sans modifier les originaux |
| Export incrémental et conflits de coffre | non | non | blocage de livraison V9 | manifeste, simulation, sauvegardes, reprise, rollback |
| Évaluation structurelle | oui | V7/V8 | pas d'inventaire relié aux besoins de production | neuf dimensions séparées, tâches et priorités |
| RAG SQLite FR/EN | oui | benchmark reproduit | petit corpus, hors-corpus peu évalué | jeu indépendant figé, pas d'embeddings par principe |
| MCP/CLI/API | oui | processus stdio | pas de Claude Desktop réel | ajouter un briefing compact sans casser les outils |
| Expériences isolées | oui | reprise/idempotence | pas de revue externe, pas de vérité prouvée | conserver échecs/observations et leur incertitude |
| Sûreté des lectures | oui | chemins/symlinks/notes corrompues | cache SQLite corrompu échoue explicitement | reconstruction explicite avec archive sous verrou |
| Boucle complète vers Obsidian puis MCP | non | non | jamais démontrée | démonstration sur coffre temporaire |
| Procédures reproduites dans Studio | non | non | logiciel et PC absents | signaler, ne pas simuler une validation réelle |

## Risques et décisions

- **Bloquant** : un export naïf écraserait des notes modifiées par l'utilisateur.
  Tester les conflits et interruptions avant d'appliquer une synchronisation.
- **Important** : les priorités de sujets privilégient encore le décor ; il faut
  distinguer priorités de production P0–P4 et priorités d'ingénierie.
- **Important** : les retours RAG sont des candidats même sur une question hors
  corpus. Ajouter abstention et compatibilité explicites dans le briefing.
- **Utile** : enrichir quelques lacunes avec des sources officielles réellement
  lues, sans collecte massive ni promotion automatique de preuves.
- **Reportable** : intégration graphique, Windows/Obsidian réels, embeddings,
  nouveaux services et orchestration V10. Ne pas les activer ici.

Le workflow existant est préservé : cron horaire et refresh quotidien, timeout
25 minutes, sérialisation et droits contents:write. Aucun nouveau cron, secret,
coffre réel ou service payant ne sera activé automatiquement.
