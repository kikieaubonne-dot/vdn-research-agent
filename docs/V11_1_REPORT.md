# V11.1 « Éponge Intelligence » — rapport de livraison

Base vérifiée : `04a3c4c874934bbf670e84923c9411448cfa0dae`, PR #6.
Branche dédiée : `codex/eponge-intelligence-v11-1`, PR vers
`codex/eponge-ocean-v11`. Les PR historiques ne sont ni fusionnées ni modifiées.

## Résultat réellement implémenté

La nouvelle chaîne réalise : question → analyse d'intention → passages V11
localisés → sélection des preuves → synthèse déterministe ou JSON modèle
facultatif → registre d'affirmations → critique mécanique → protocole
expérimental → mémoire persistante → briefing MCP. Il ne s'agit pas d'une
modification des poids du modèle ni d'un agent autorisé à éditer le jeu.

Les trois problèmes de la démonstration sont identifiés : apparence,
collisions et éclairage/rendu nocturne. Le pipeline récupère des références
Roblox et un contexte Blender, distingue citations originales et notes
secondaires, conserve les hypothèses et propose trois comparaisons contrôlées.
Il signale les versions inconnues, le contexte incomplet, la nécessité
d'adapter Blender à Roblox et l'absence de tests dans le projet utilisateur.

## Architecture et fichiers

| Fichiers | Responsabilité |
|---|---|
| `agent/intelligence_evidence.py` | intention, documents/passages, classement, citations, versions et contradictions explicites |
| `agent/intelligence_models.py` | diagnostic, Ollama installé/digest, streaming borné, annulation, routage et réservations communes |
| `agent/intelligence.py` | synthèse, critique, protocoles, paramètres documentés, cache et journal consultable |
| `agent/intelligence_semantic.py` | index de passages lié au digest, lexical/sémantique/RRF et fallback |
| `agent/intelligence_api.py`, `agent/v111.py` | cinq outils MCP et CLI, permissions explicites, export privé facultatif |
| `agent/ocean.py`, `agent/mcp_v8.py` | intégration opt-in V11, contrat historique préservé |
| `config/intelligence.json` | nouveau contrat désactivé par défaut |
| `bench/evaluate_intelligence.py`, `bench/intelligence_cases.json` | 36 références annotées, huit tâches et mesures A/B facultatives réelles |
| `tests/test_intelligence.py` | 34 tests supplémentaires, y compris processus MCP et intégration collecteur |
| `docs/v111/`, `docs/validation/v111/`, README | guides, preuves, benchmark et résultats |

[Architecture détaillée](v111/ARCHITECTURE.md), [audit et reprise](v111/AUDIT.md).

## Validation exécutée

- Baseline **335 tests réussis**, inchangés.
- Suite finale locale : **369 tests hors ligne réussis**, connexions socket
  interdites, puis les **369** dans une copie avec configuration personnelle
  réseau/autonomie/schedule autorisée ; configuration source et copiée conservées.
- 36/36 contrats de qualité annotés ; comparaison déterministe sur mêmes
  documents/questions, sans vérité terrain moteur ni revue humaine inventée.
- Processus MCP stdio réel depuis un autre cwd : 27 outils en mode V11.1,
  initialize/list/call/structuredContent ; `--v11` conserve ses 22 outils.
- Corpus réel du laboratoire isolé : analyse finale, preuves/critique/protocoles
  enregistrés puis réutilisés ; collecte supplémentaire d'une page Blender
  officielle, sans réinitialisation des compteurs copiés.
- Contrôles de corruption, version/digest changé, nombres absents ou préfixes
  numériques trompeurs, injections, panne modèle, reprise après checkpoint,
  annulation, quota partagé, absence de doublon d'appel V11, export RAG sûr.

Les logs sont dans [validation/v111](validation/v111/). Les résultats Windows
et Linux du **commit final** doivent être lus dans les checks de la PR dédiée,
dont le lien et le SHA sont fournis à la livraison. La CI exécute les deux
scénarios de configuration sous Python 3.11 ; elle n'exécute pas de modèle réel.

## IA réelle, matériel et benchmark

Le diagnostic réel trouve le service Ollama **inaccessible** et aucun GPU
détecté dans cet environnement. Aucun téléchargement de poids, génération,
embedding réel ou API payante exécutés. La RTX 4060 Ti 8 Go utilisateur n'est
pas présente ici. Les performances de modèles et leur JSON valide ne sont
donc **pas évalués** ; les réponses des tests de transport restent des fixtures.

Les tags Qwen3/Gemma 3, quantifications et licences ont été vérifiés dans leurs
catalogues officiels. Aucun modèle n'est recommandé par défaut. Le diagnostic
enregistre le nom/digest réellement installé ; le routeur considère complexité,
économie, mémoire et sensibilité, sans promettre qu'une taille tient en VRAM.

[Benchmark et résultats bruts](v111/BENCHMARK.md),
[diagnostic réel](v111/hardware-service.json), [démonstration réelle](v111/demo.json).
La structuration du registre est mesurable ; aucun gain général d'intelligence,
de qualité subjective, de vitesse ou de temps Claude n'est déduit.

## Préservation et limites

Les **110 Markdown historiques, la candidate V11 supplémentaire et tous les
fichiers de configuration historiques** sont inchangés, comparés à la base par
SHA-256 : [manifeste](v111/preservation.json). Les sessions et preuves privées
antérieures sont conservées. Une réservation de diagnostic dans le runtime local
est préservée et non publiée ; aucune restauration d'ancien compteur.

Les états d'affirmations ne remplacent pas les statuts historiques. Aucune
connaissance ou expérience n'est promue automatiquement VERIFIED. Les échecs
LabStore restent accessibles au briefing après import opérateur.

Limites : intention spécialisée déterministe ; pas de raisonnement général
évalué. Les citations établissent une attribution, pas une preuve de vérité.
Contradictions limitées aux assignations explicites avec conditions comparables ;
pas de démonstration sémantique ni de revue humaine des procédures. Les fenêtres
tronquées, sources périmées et versions inconnues diminuent le soutien.

Le modèle peut proposer des étapes candidates, mais aucune édition, exécution
Studio ou expérimentation Roblox/Blender n'est déclenchée par le modèle.
Blender 5.2, B3/C1, Claude Desktop et le coffre personnel étaient indisponibles.
La page Blender collectée indique 5.3 ; sa compatibilité n'est pas supposée.
Le routeur n'apprend pas encore un profil automatique de latence par matériel.
Le contrôle mémoire ne garantit pas un chargement ; le timeout/annulation reste
coopératif. Une réserve API n'est pas une facture ni le plafond du fournisseur.

## Installation, commandes, MCP et rollback

```powershell
git clone --branch codex/eponge-intelligence-v11-1 https://github.com/kikieaubonne-dot/vdn-research-agent.git
Set-Location vdn-research-agent
$env:PYTHONUTF8 = "1"
py -3.11 -m venv .venv
$python = Join-Path $PWD ".venv\Scripts\python.exe"
& $python -m agent.v111 diagnose
& $python -m agent.v111 synthesize "Mes sapins Roblox sont artificiels, leurs collisions gênent le joueur et le rendu de nuit manque de réalisme" --apply
& $python -m agent.v111 search "collisions sapins"
& $python -m agent.v111 brief "Quelles priorités pour ma forêt Roblox ?"
```

Pour la génération, installer/choisir explicitement un modèle et configurer le
nouveau contrat, puis `synthesize ... --apply --allow-model`. Aucune tâche
permanente n'est activée. Les plafonds V10/V11 restent en vigueur.

[Guide Windows/Ollama et commandes](v111/WINDOWS_OLLAMA.md) ·
[Sélection des modèles et licences](v111/MODELS.md) ·
[MCP Claude Desktop](v111/CLAUDE_MCP.md) ·
[Migration, Obsidian et rollback](v111/MIGRATION.md).
