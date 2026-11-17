# Inventaire du prologue —36 ressources

Source structurée : project/prologue.json. Disponible signifie fichier présent dans le runtime ou le dépôt de code, pas validation Studio. Coûts et compatibilités inconnus restent inconnus.

| ID | Scènes | Priorité | Fonction | Validation | Dépendances |
|---|---|---|---|---|---|
| progression | A,B,C,D,E | P0 | Deterministic narrative progression, event ordering and resume | TESTED_IN_ISOLATION | aucune imposée |
| scene-state | A,B,C,D,E | P0 | Scene ownership, safe copied environment and explicit engine build | NOT_TESTED | progression |
| camera-controller | A,B,C,D,E | P0 | First person, immediate player control, proposed interruption limits | NOT_TESTED | scene-state |
| interaction-contract | A,D,E | P0 | Post-it, phone and clue events; unknown component names | NOT_TESTED | progression |
| boy-proxy | A,B,C,D | P0 | Léo playable proxy, no invented height or final appearance | NOT_TESTED | camera-controller |
| maelle-proxy | A,B | P0 | Sister visible, leaves house and disappears from line of sight | NOT_TESTED | scene-state |
| antagonist-proxy | C | P0 | Brief silhouette and encounter; no family-father presence added | NOT_TESTED | scene-state |
| investigator-proxy | E | P0 | Playable police investigator after reported disappearance | NOT_TESTED | camera-controller |
| rig-export | A,B,C,E | P0 | Visual bake trial and independently measured animation export | TESTED_IN_ISOLATION | aucune imposée |
| reach-proxy | A,D,E | P1 | Reusable original lab gesture; not a final character or approved game animation | TESTED_IN_BLENDER | rig-export |
| walk-sprint | B,C,E | P0 | Character movement and chase readability | NOT_TESTED | rig-export, camera-controller |
| investigation-movements | E | P1 | Crouch/vault/climb/slide are candidates introduced during investigation, not B | NOT_TESTED | walk-sprint |
| house-blockout | A | P0 | Family house, Christmas contrast and clear exit | NOT_TESTED | scene-state |
| furniture | A | P2 | Readable domestic silhouettes and navigation | NOT_TESTED | house-blockout |
| postit | A | P0 | Parents already absent, ask Léo to watch Maëlle | NOT_TESTED | interaction-contract |
| forest-path | B,C,E | P0 | Continuous snowy route and line-of-sight events | NOT_TESTED | scene-state |
| snowy-spruce | B,C,E | P1 | Reuse B3/C1 knowledge, actual assets unavailable | NOT_TESTED | forest-path |
| tree-collision | B,C,E | P0 | Player passes branches on a copied route | NOT_TESTED | forest-path, camera-controller |
| snow-ground | B,C,E | P1 | Terrain readability and snow material | NOT_TESTED | forest-path |
| footprints | C,E | P1 | Adult/child footprint candidates without premature narrative decision | NOT_TESTED | snow-ground |
| night-light | B,C,E | P1 | Flashlight/night visibility under matched test conditions | NOT_TESTED | forest-path |
| flashlight-v2 | B,C,E | P1 | Inspect reported V2 before selecting changes | NOT_TESTED | night-light |
| fog | B,C,E | P2 | Light fog; no assumed Roblox parameters | NOT_TESTED | night-light |
| red-eyes | C | P1 | Eyes linger in darkness after silhouette disappearance | NOT_TESTED | antagonist-proxy, night-light |
| chase-ai | B,C | P0 | Bounded line-of-sight/chase triggers; no untested pathfinding guarantee | NOT_TESTED | forest-path, maelle-proxy, antagonist-proxy |
| christmas-room-tone | A | P1 | Warm atmosphere; originals or licensed content | NOT_TESTED | house-blockout |
| forest-sound | B,C,E | P1 | Tension escalation, spatial clues and silence | NOT_TESTED | forest-path |
| licensed-music | A,B,C | P2 | Optional authorized music, no copied AAA content | NOT_TESTED | aucune imposée |
| dialogue | A,B,C,D | P1 | Authorized voice for Maëlle cry, Ho ho ho and police report; no voice cloning | NOT_TESTED | forest-sound |
| subtitles-objectives | A,B,C,D,E | P0 | Short text, Retrouve Maëlle, optional Shift prompt | NOT_TESTED | progression |
| phone | D | P0 | Safe place and report interaction | NOT_TESTED | interaction-contract |
| role-transition | D,E | P0 | Switch player role without inventing a confirmed ending | NOT_TESTED | progression, boy-proxy, investigator-proxy |
| clue-props | E | P1 | Inspectable clues; exact evidence and puzzles proposed | NOT_TESTED | interaction-contract, forest-path |
| clothes-hair | A,B,C,E | P2 | Character clothing/hair/beard pipeline, actual references UNKNOWN | NOT_TESTED | rig-export |
| materials-pbr | A,B,C,E | P2 | Documented PBR authoring; no unverified optimal values | NOT_TESTED | rig-export |
| performance-protocol | A,B,C,D,E | P0 | Device/build, continuous route and measured frame times | TESTED_IN_ISOLATION | camera-controller, forest-path |

Les formats, méthodes, licences, coûts, fichiers disponibles, tests et problèmes connus sont présents pour chaque ressource dans le JSON, consultable via `synthesize_technical(question="prologue:resources")`. Fichiers connus :

- progression : `agent/prologue.py`
- progression : `roblox/prologue/Progression.lua`
- rig-export : `agent/animation_roundtrip.py`
- rig-export : `scripts/blender_animation_trial.py`
- reach-proxy : `docs/v112/prologue/artifacts/gesture-primary.blend`
- reach-proxy : `docs/v112/prologue/artifacts/gesture-primary.glb`
- reach-proxy : `docs/v112/prologue/artifacts/gesture-transfer.blend`
- reach-proxy : `docs/v112/prologue/artifacts/gesture-transfer.glb`
- performance-protocol : `project/prologue.json`
