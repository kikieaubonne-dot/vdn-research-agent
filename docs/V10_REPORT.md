# Livraison V10 — Éponge, recherche et expérimentation contrôlées

Base vérifiée : `codex/knowledge-factory-v9`, commit `71d8087`. Nouvelle branche
`codex/research-lab-v10`, destinée à une PR vers V9. PR #1 → V7, #2 → V8 et #3 → V9
restent ouvertes dans leur chaîne de dépendances ; aucune ancienne PR n’est
modifiée, fusionnée ou déployée. [Audit préalable](V10_AUDIT.md).

## 1. Ce qui est implémenté

Le moteur local réutilise file, profils, classement des sources, acquisition,
budgets, RAG et export V9. Il ajoute des sessions persistantes avec profondeur,
branches, tentatives, ticks, temps, quotas réseau et stagnation bornés. Trois modes :
manuel, tick autonome sur objectifs autorisés, tick planifié à fréquence configurable.
Les deux derniers sont désactivés par défaut ; le Planificateur Windows reste
à configurer par l’utilisateur. Réseau également désactivé.

Le registre d’expériences conserve huit états, conditions par essai, échecs,
limites, artefacts hachés, révisions et événements atomiques. `SUCCESS` demeure
un rapport ; `VERIFIED` nécessite une revue opérateur explicite et une preuve
déclarée externe. Une revue n’altère aucune note historique et ne transforme
pas une réussite locale en solution universelle. Les échecs restent consultables,
y compris après une réussite ultérieure. Aucun moteur d’édition de code autonome.

Autres livraisons : cinq outils MCP optionnels, briefing V10 avec mémoire des
échecs, fiches Obsidian, annotations visuelles manuelles, adaptateurs IA optionnels,
comparaison cible/résultat sans score inventé, neuf zones de laboratoire, protocole
sapin A/B, collecteur candidat, schéma et import externe lié au bon essai.

## 2. Ce qui est réellement testé

**288 tests hors ligne réussis**, dont les **251 historiques** conservés et
37 nouveaux. Les connexions socket sont interdites, sous-processus compris.
Tests d’intégrité/corruption, budgets avant effet, quotas, reprise, erreurs disque,
secrets, chemins/symlinks, idempotence, permissions MCP, transport IA par fixtures,
collecte réelle avec fournisseur fixture, annotations et import de mesures.
L’export Obsidian est testé en dossier temporaire avec deuxième sync et rollback.
MCP stdio est testé depuis un dossier externe au dépôt.

La démonstration réelle sur copie du corpus atteint profondeur 2 et 13 branches,
puis s’arrête sur des prérequis manquants. Elle ne comble pas artificiellement
la lacune. Les **110 Markdown** restent inchangés, dont les 106 historiques.
Le holdout gelé V9 conserve hit@3=1 et MRR=0,958 sur le même corpus. Aucun gain
de pertinence ou productivité V10 n’est revendiqué.

[Logs, mesures et protocole](v10/BENCHMARK.md). Les tests locaux tournent sous
Linux ; la [CI de la PR #4](https://github.com/kikieaubonne-dot/vdn-research-agent/pull/4/checks)
exécute également la suite complète sous Windows avec Python 3.11 et UTF-8.
Le lecteur de corpus valide les chemins fournis avant leur conversion native,
en conservant le refus des chemins dangereux et symlinks. Seul le lanceur des
tests historiques impose UTF-8 à ses sous-processus ; les 251 cas sont inchangés.
Ces vérifications ne valident pas le PC utilisateur, Claude Desktop, les modèles
réels ou les applications graphiques.

## 3. Ce qui fonctionne sans IA externe

CLI autonome en Python standard : lacunes et neuf dimensions de qualité,
recherche dans le corpus, collecte déterministe depuis les fournisseurs autorisés
si explicitement activée, décomposition/relances lexicales, journal d’expériences,
plans reproductibles, annotations/comparaisons manuelles, métriques et export.
Ces fonctions ne consomment aucun quota Claude/Codex et n’exigent pas de clé.
Les sources Internet exigent Internet ; leur contenu et disponibilité ne sont
pas garantis. La collecte V10 en ligne n’a pas été exercée dans cette livraison.

## 4. Ce qui nécessite un modèle

Interprétation automatique d’une image ou comparaison visuelle automatique :
modèle compatible et backend explicitement activé. Local Ollama ou distant HTTPS
compatible chat completions ; aucun fournisseur payant imposé. Sans modèle, le
système demande des annotations ; il ne simule pas une compréhension visuelle.
Aucune forêt n’a été reconnue par un modèle ici. Ressources RAM/VRAM dépendantes
du modèle, non benchmarkées ; [configuration](v10/WINDOWS.md).

## 5. Ce qui nécessite Roblox ou Blender

Construire/importer les prototypes, compter les triangles réels, vérifier les
matériaux/transparences, capturer le rendu et mesurer les performances sur appareil
cible exigent les outils réels. **Studio et Blender n’ont pas été exécutés.**
Le [laboratoire](v10/LAB.md) est une spécification installable, sans place publié.
Le [rapport sapin](v10/SPRUCE_COMPARISON.md) conserve toutes les mesures inconnues
et aucun gagnant. Zéro procédure de jeu vérifiée dans cette livraison.

## 6. Ce qui reste expérimental

Collecteur Luau non compilé/non exécuté dans Studio ; contrats de modèles testés
seulement par fixtures ; adaptateurs distants variables selon fournisseur ;
classement et analyse de contradictions principalement lexicaux. La revue humaine
repose sur l’attestation de l’opérateur, pas sur une preuve cryptographique
d’exécution. Délais coopératifs, quotas conservateurs après crash, stockage local
à sauvegarder et surveiller. Pas d’authentification d’un logiciel externe, de
production d’assets, de multi-agent ni de modification automatique du jeu.
[Frontières de sécurité](v10/SECURITY.md).

## 7. Installation

Suivre le [guide Windows](v10/WINDOWS.md) : cloner, sélectionner la branche,
Python 3.11+, lancer `python -m tests.offline`, puis `python -m agent.v10 status`
et `python -m agent.v10 spruce --dry-run`. Aucun pip requis. Utiliser `--apply`
pour les écritures ; `--allow-network` et flag de configuration pour collecter.
Pour Claude : `python vdn_mcp.py --v10`, écritures désactivées sauf
`--allow-experiments`. [MCP/Obsidian](v10/INTEGRATIONS.md).

## 8. Prochaines actions

Relire la PR et exécuter le guide sur Windows ; configurer un export Obsidian
séparé ; créer le place privé du laboratoire ; remplir les contrôles du sapin et
exécuter A/B ; importer les preuves et consigner même les échecs ; effectuer une
revue humaine conditionnelle. Activer une planification seulement après validation
des budgets et objectifs locaux. [V11/V12](v10/ROADMAP.md) restent une feuille de
route, sans développement ou activation anticipés.
