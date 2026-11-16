# Audit V10 — 16 novembre 2026

Base réelle : `71d8087`, V9 #3 ouverte vers V8. Les branches distantes et les
relations d'ascendance V7 → V8 → V9 sont vérifiées. Nouvelle branche :
`codex/research-lab-v10`. Aucun changement, fusion ou déploiement des PR existantes.

Baseline reproduite : **251 tests** avec `python -m tests.offline`, connexions
interdites jusque dans les sous-processus. Inventaire initial : **110 Markdown**,
dont les 106 fichiers historiques et les quatre candidates V9.

| Interface existante | Réutilisation V10 | Limite vérifiée |
|---|---|---|
| ResearchQueue / décomposition / relances | sessions isolées dans lab/, mêmes clés et règles | le cycle historique réécrit les index Markdown : ne pas l'utiliser tel quel pour V10 |
| Transport HTTP / Budget / quotas quotidiens | garde-fous existants et pré-imputation persistante | temps coopératif, pas de préemption absolue d'une requête engagée |
| RAG / qualité / briefing V9 | contexte local et lacunes sans nouvelle IA obligatoire | scores lexicaux, aucune preuve Studio automatique |
| Rapports d'expérience V8 | conservés ; nouveau cycle de vie séparé | pas de transitions, vérification opérateur ou preuves hachées |
| Obsidian V9 | export supplémentaire explicite des expériences | coffre personnel inaccessible ; fichier temporaire seulement |
| MCP / CLI | nouveaux outils optionnels, signatures anciennes préservées | clients réels Claude/Windows non testés |
| Collecte V9 | intacte, aucun nouveau service requis | sources et révisions encore bornées au périmètre autorisé |

Les limitations V9 sont confirmées : pas de Roblox Studio/Blender/Obsidian Windows,
pas de modèle multimodal connecté, pas de preuve graphique réelle ni de gain de
productivité mesuré. Aucun code de production ne sera exécuté ou modifié.

Architecture minimale : journal d'événements immuables par expérience, preuves
importées dans un espace autorisé, sessions de recherche bornées réutilisant la
file, un tick local non activé par défaut, adaptateurs IA optionnels, protocole
de laboratoire séparé et analyse visuelle manuelle explicite en repli.
