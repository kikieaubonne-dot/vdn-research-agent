---
status: a_verifier
source_type: "GitHub repositories"
topic: "spruce"
score_heuristique: 35
collected_utc: "2026-11-15T12:15:20+00:00"
---

# DiyorFayz/skills

**Sujet :** Épicéa enneigé réaliste

**Source :** [GitHub repositories](https://github.com/DiyorFayz/skills)

**Question de recherche :** Roblox SurfaceAppearance transparency foliage

## Extrait de découverte (non vérifié)

Aucun extrait disponible.

## Vérification Roblox / Blender

- [ ] Ouvrir et lire la source complète
- [ ] Vérifier la version du moteur et les limites techniques
- [ ] Extraire une procédure précise, des paramètres et les prérequis
- [ ] Tester dans Blender puis Roblox Studio
- [ ] Mesurer visuel, performances et reproductibilité

## Résultat du test

À compléter après expérimentation.

## Analyse V3 — éléments techniques à vérifier

**Statut :** passages candidats extraits de la source, **non validés** dans Roblox.

**Source lue :** https://github.com/DiyorFayz/skills  
**Contenu :** GitHub README  
**Passages candidats :** 5

### Passages et paramètres repérés

- | [scenario-text-overlay](skills/scenario-text-overlay/SKILL.md) | Letter-perfect text overlays: templated transparent PNG cards (taglines, CTAs, legal supers, rich cards) to composite |
- | [scenario-sprite-animation](skills/scenario-sprite-animation/SKILL.md) | Walk cycles, idle loops, VFX sprites, and animation sheets from one prompt: GIF vs sprite sheet output, frame slicing, pixel cleanup |
- | [scenario-side-view-game-kit](skills/scenario-side-view-game-kit/SKILL.md) | Side-scroller and platformer art: side-view pixel sprite strips for a hero and enemies (run, walk, attack, hurt, poses), parallax layers, seamless wall texture, platform strip, props |
- | [scenario-blender-2d-animation](skills/scenario-blender-2d-animation/SKILL.md) | A side-scroller shot animated in Blender from Scenario pictures: a concept frame that locks the look, parallax layers, props and a hero run cycle on its reference, flat image cards with an orthographic camera, keyed jumps and rigid-body props, and a whole new look by swapping the pictures |
- | [scenario-skyboxes](skills/scenario-skyboxes/SKILL.md) | 360 equirectangular panoramas and skyboxes, seam-safe upscaling, engine export |

### Questions de recherche complémentaires

- spruce Roblox transparent implementation limitations troubleshooting
- spruce Roblox animation implementation limitations troubleshooting
- spruce Roblox texture implementation limitations troubleshooting

### Validation requise

- [ ] Vérifier chaque passage dans la source complète
- [ ] Confirmer les limitations Roblox actuelles
- [ ] Tester dans Roblox Studio ET Roblox Player
- [ ] Mesurer qualité et performance
