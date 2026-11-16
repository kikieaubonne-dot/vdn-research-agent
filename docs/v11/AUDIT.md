# Audit Océan — 16 novembre 2026

Base distante et locale : PR #5, `4e2624f`. PR #1–#5 toujours ouvertes,
chaîne V7 → V8 → V9 → V10 → correctif. Nouvelle branche V11 séparée.
Baseline : 305 tests hors ligne reproduits. Aucun compteur Windows modifié.

Réutilisation : ResearchSessions/ResearchQueue et Budget pour les réservations,
providers pour le transport borné, LabStore pour les preuves et expériences,
KnowledgeEngine/SQLite pour le corpus, Obsidian pour les conflits/rollback,
MCP stdio et adaptateurs modèles facultatifs. Les rôles seront des étapes Python,
sans multiplication obligatoire d’appels IA.

Défauts : make_root copiait la configuration personnelle ; `network_enabled=true`
supprime le refus attendu dans des tests. Reproduit dans une copie temporaire,
sans modifier le fichier utilisateur. Les fixtures de configuration deviennent
un contrat figé ; les tests qui autorisent le réseau l’activent dans leur copie.
La dépendance documentaire séquentielle V10 bloque aussi trop tôt la recherche
de sujets indépendants. La synthèse manque de contexte, preuves par affirmation
et protocoles utiles. La V11 doit conserver ses incertitudes et non inventer une
compréhension sans modèle.

110 Markdown présents à préserver. Les deux fiches Windows mentionnées dans la
mission ne sont pas présentes dans ce checkout ; aucune analyse de leur contenu
effectif n’est revendiquée. Le coffre personnel et les assets B3/C1 sont absents.
Blender disponible : **4.3.2**, différent du 5.2 utilisateur ; test réel possible
sur géométrie de démonstration. Roblox Studio et Claude Desktop indisponibles.
La roadmap V10 demandait une validation avant connexion Studio : on livre un
import local borné, sans publier ni éditer le jeu principal.
