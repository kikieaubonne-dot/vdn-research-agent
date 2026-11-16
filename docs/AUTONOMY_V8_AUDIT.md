# Audit indépendant V7 → V8 — 16 novembre 2026

Base V7 : `f5cb699`, PR #1 ouverte, non fusionnée. Les quatre commits de la PR
(`0f13b9a`, `63ade6f`, `5b14025`, `f5cb699`) sont inspectés ; le merge ne contient
que les données collectées par le robot. Rapport et roadmap V7 lus intégralement.
Aucun AGENTS.md supplémentaire. Branche de travail : `codex/knowledge-engine-v8`.

## Vérifications avant modification du code

- **177 tests passent**, `socket.socket.connect` interdit. Log de baseline conservé.
- 106 fichiers de connaissances inventoriés par SHA-256. Arbre `knowledge/`
  identique au corpus de `9abf775` : `e46fb73b3efc4284acdf5a2a1863ab13e9d5c06b`.
- Baseline RAG reproduite sur copie : hit@1 0,9, hit@3 0,9, MRR 0,925.
  La fiche `vdn-1290b940c378` est quatrième pour la requête de squelette FR.
- Aucun appel de recherche réseau, aucune fusion de PR ni modification de données.

## Architecture réelle

Acquisition : `run`, `providers`, `meta`, `autonomy`, `research_queue`.
Mémoire Markdown et registre : `knowledge`, écritures atomiques `storage`.
Index dérivé : SQLite FTS5 dans `rag`, fallback LIKE. Extraction : `procedure`,
`structure`, `procedure_analysis`. Diagnostics : `evaluation`. Décomposition :
`decomposition` + profils configurables. Interface existante : `mcp_server`,
JSON-RPC stdio avec search_knowledge/read_knowledge/get_topic_index.
`agent.run` constitue l'interface CLI historique et reste compatible.

Les budgets de cycle/refresh, reprise et verrou système sont testés et conservés.
La collecte manuelle hors cycle reste hors comptabilité persistante (limite V7).
Le planificateur persistant ne peut pas être directement exposé comme prévision
en lecture seule : il écrit dans la file. Il faut partager sa décomposition pure.

## Défauts et limites observables

- **MCP** : les schémas annoncés ne sont pas validés ; conversions bool/int
  permissives. Un message JSON valide mais non objet fait tomber `.get`.
  Protection nécessaire avant d'étendre l'interface.
- **Chemins** : `get_topic_index` ne résout pas le chemin général avant lecture ;
  un `_index.md` symlink peut sortir de la bibliothèque. `load_notes` suit aussi
  des fichiers symlink et ne signale pas les notes corrompues individuellement.
- **Indexation** : une seule note illisible ou un tier invalide peut bloquer
  tout l'index. Fermeture/rollback après interruption à renforcer.
- **Budget de contexte** : le premier passage conserve un minimum de 60 caractères,
  même si son en-tête dépasse le budget. Un budget minuscule peut être dépassé.
- **RAG** : l'expansion est limitée globalement aux douze premiers synonymes,
  pas équilibrée par terme ; des notions différentes sont confondues (os/vent),
  et la pertinence est multipliée par des statuts déclarés, pas des preuves.
  La diversité est gérée par passage avant d'assurer la couverture des fiches.
- **Capacités absentes** : procédures multi-sources prudentes, prévision de plan
  sans effet, retour d'expérience séparé, interface structurée validée et démos.

## Architecture minimale retenue

Réutiliser le même SQLite/FTS et les mêmes Markdown. Ajouter une façade locale
validée pour cinq opérations : recherche, lecture complète, procédures,
prévision de recherche et rapport d'expérience explicite. Conserver le serveur
MCP historique et fournir un mode V8 avec les outils supplémentaires ; aucun
port réseau. Les écritures d'expérience nécessitent une activation explicite.
Séparer scores textuels et diagnostics de preuve ; aucun statut déclaré par
Claude ou par une fiche n'entraîne une validation automatique.

Comparer plusieurs corrections du RAG sur un jeu de développement FR/EN distinct
avant le benchmark historique. Mesurer aussi latence, index initial/incrémental
et résultats négatifs. Les protocoles Studio/Blender et Claude Desktop réel ne
sont pas exécutables ici et ne seront pas annoncés comme testés.
