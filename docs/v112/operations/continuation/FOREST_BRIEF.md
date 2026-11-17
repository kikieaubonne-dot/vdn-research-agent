# Forêt enneigée — briefing de continuation

**État PARTIEL — propositions d’ingénierie, pas de validation Roblox.**

Contexte confirmé : Le Voisin de Noël, forêt enneigée nocturne, lampe centrale ; B3/C1 et V2 signalés comme prototypes, fichiers absents ici. Léo et le policier ont des gabarits à mesurer, pas à inventer.

## Priorité pour Claude

Commencer par un témoin B3/C1 sur scène COPIÉE identifiée. Isoler les collisions gênantes avant densité/rendu ; garder le témoin et le même contrôleur. Les tests suivants doivent conserver caméra, lumière, route, appareil et build Studio. Les critères de confort et performance restent à approuver.

| Sujet | État | Méthode proposée | Sources | Limites / prochain test |
|---|---|---|---|---|
| Sapins B3/C1 | PARTIAL | Comparer une courbure de branches sur copie, conserver la silhouette générale et le budget de triangles. L’essai procédural A/B est réel mais ne valide pas B3/C1. | R1 | Copies et réglages B3/C1, aiguilles détaillées, revue visuelle humaine et transfert Studio manquants. |
| Densité végétale | PARTIAL | Fixer un témoin de scène et varier seulement la densité ; profiler le même trajet avant de recommander un espacement. Le streaming est une option documentée, pas un remède garanti. | R2 | Aucun espacement, nombre d’arbres ou seuil FPS confirmé ; mesure sur appareils cibles nécessaire. |
| Collisions B3/C1 | PARTIAL | Conserver A intact. Dans B, séparer les surfaces visuelles du volume physique du tronc ; relever les collisions avant toute modification. Tester contournement, contact diagonal et blocage sous les branches avec le même contrôleur. | R3 | Géométrie, build Studio, contrôleur et règles de CanTouch/CanQuery inconnus. Ne pas désactiver les raycasts/interactions par généralisation. |
| Neige tassée et relief | PARTIAL | Conserver le matériau Terrain témoin ; comparer une modification locale de relief et de matériau sur un échantillon copié sous caméra/lumière constantes. | R4 | La documentation des matériaux ne prouve ni tassement réaliste ni traces de pas dynamiques. |
| Empreintes adulte/enfant | BLOCKED | Préparer deux protocoles correspondant à Léo et au policier, avec origine et taille tirées des personnages réels ; aucune dimension ou cadence inventée. | R4 | Pas de source procédurale suffisante ni de mesures de chaussures/contacts. Le lien R4 apporte seulement le contexte Terrain. |
| Lampe torche V2 | PARTIAL | Comparer une seule propriété documentée à la fois ; SpotLight est décrit comme une lumière directionnelle adaptée aux lampes torches. Vérifier l’attachement réel, la portée, l’angle et les ombres sans supposer de valeur optimale. | R5 | Aucun test de V2 ni de cartes alpha sous cette lampe ; l’essai Blender n’utilise pas les unités photométriques Roblox. |
| Brouillard nocturne | PARTIAL | Évaluer séparément Atmosphere et éclairage local. La source décrit notamment la diffusion de lumière solaire : elle ne démontre pas un faisceau volumétrique de lampe torche. | R6 | Interactions Atmosphere/SpotLight à vérifier dans Studio ; ne pas transférer directement le modèle volumétrique Blender/Unreal. |
| Caméra et performances | PARTIAL | Conserver le contrôleur de caméra témoin. Relever son mode et profiler un trajet répété avec les mêmes appareils et réglages avant de proposer un mouvement supplémentaire. | R7, R8 | Aucune amplitude de head-bob, seuil de confort, FPS mobile ou économie de contexte Claude mesurés. |

## Expérience réelle disponible

Épicéa et buisson procéduraux, Blender 4.3.2 CPU : branches planes A / courbées B, même seed, caméra, lumière et nombre de triangles. Épicéa 812/812 triangles ; buisson 684/684. Étendue verticale moyenne des branches 0 → 0,253125 m et 0 → 0,21225 m. Ces valeurs décrivent ces deux prototypes, sans dimension optimale Roblox.

Quatre captures, quatre scènes .blend et quatre OBJ conservés ; réouverture et réimport dans un second processus avec mêmes nombres de triangles. Critère géométrique PASS ; esthétique INCONCLUSIVE ; Roblox BLOCKED. La génération initiale a échoué sur un débruiteur absent : échec conservé, version corrigée différente et retestée. Aucun VERIFIED/HUMAN_APPROVED.

## Références attribuables

Les captures originales locales sont conservées. Licences de réutilisation des documents et versions moteur UNKNOWN : pas d’autorisation d’extraire des assets. Aucune archive éditoriale ne constitue une source indépendante.

### R1 — Transparency
https://create.roblox.com/docs/art/modeling/surface-appearance

Document `doc-a6cc7c1e3387a8cc46168e3d`, passage `pass-7e898b552533941fd729e7a7`, caractères 13179–13552, SHA256 `cf02d3f01584a51f0622086732d89ae69a27a1902abe321bf0008c3adc014ca4` ; accès 2026-11-16, version unknown, contexte incomplet=False.

```text
You can use the `Enum.AlphaMode.Transparency` mode to create complex or extremely fine objects, such as lace or netting, […]
```

### R2 — Instance streaming
https://create.roblox.com/docs/workspace/streaming

Document `doc-7f6e3b754b544c0e8c949408`, passage `pass-d840fa44a1ea98ef656c3a1c`, caractères 1403–1586, SHA256 `e188ea4d8d88f777c38d5c800350d943c05d1b6d0ba15ba16f34189b0c940622` ; accès 2026-11-17, version unknown, contexte incomplet=False.

```text
Instance streaming is controlled through the `Class.Workspace.StreamingEnabled` property, enabled by default for new pla […]
```

### R3 — Physics memory usage
https://create.roblox.com/docs/performance-optimization/improve

Document `doc-0dce45f2b67681fcb25582db`, passage `pass-031664fd983c49a7c253798b`, caractères 9911–10135, SHA256 `3517d9d6e0db2f5a3febf2023c9828687af332427af9cea618ce5edb1716a99e` ; accès 2026-11-16, version unknown, contexte incomplet=True.

```text
Physics movement and collision detection consumes memory. Mesh parts have a `Class.MeshPart.CollisionFidelity|CollisionF […]
```

### R4 — Terrain materials
https://create.roblox.com/docs/parts/terrain

Document `doc-ae07cc946d4b006af7a0d167`, passage `pass-7e7f9fd09806f3bf68030796`, caractères 1210–1777, SHA256 `fc67e10e2b4290b5a34368ae640a855f4ed195d8716fc162c901093f0ef4e575` ; accès 2026-11-16, version unknown, contexte incomplet=False.

```text
The following default materials are available for terrain. You can also paint [custom terrain materials](/docs/en-us/par […]
```

### R5 — Description
https://create.roblox.com/docs/reference/engine/classes/SpotLight

Document `doc-f03de1f548339691fe69ffb8`, passage `pass-449eb39576eea0c0c87f3dd1`, caractères 379–662, SHA256 `04899531919b80337d3759004656ea6683ebfd81e0d9ca4d70ac3fc647d10640` ; accès 2026-11-17, version unknown, contexte incomplet=False.

```text
A **Spotlight** emits light of a specified [Color](/docs/reference/engine/classes/Light.md) and
[Brightness](/docs/refer […]
```

### R6 — Atmospheric effects
https://create.roblox.com/docs/environment/atmosphere

Document `doc-11e0d70b781ffead8e8beec4`, passage `pass-8db65ce0171a0d1b9bf26574`, caractères 242–429, SHA256 `64afeee1537c84c935c10c574f41f6eae3ed90b6d5e960d2a0cb15ce190e7bb0` ; accès 2026-11-16, version unknown, contexte incomplet=False.

```text
**Atmospheric effects** simulate realistic environments by scattering sunlight in unique ways based on properties that c […]
```

### R7 — Camera mode
https://create.roblox.com/docs/workspace/camera

Document `doc-e54362f11eb31cf3c6cf5281`, passage `pass-b32a99cc34d66d818b676098`, caractères 2015–2447, SHA256 `17d579798b54d7347acd74b3bb8a823ca4cd377b5b4280d5fef175a0b76a5429` ; accès 2026-11-16, version unknown, contexte incomplet=False.

```text
| Setting | Description |
| --- | --- |
| **Classic** | The classic Roblox third-person camera which can be zoomed into  […]
```

### R8 — MicroProfiler scopes
https://create.roblox.com/docs/performance-optimization/improve

Document `doc-0dce45f2b67681fcb25582db`, passage `pass-a7834f4918f9846dd9802944`, caractères 2636–3015, SHA256 `3517d9d6e0db2f5a3febf2023c9828687af332427af9cea618ce5edb1716a99e` ; accès 2026-11-16, version unknown, contexte incomplet=True.

```text
For more information on debugging scripts using the MicroProfiler, see the `Library.debug` library, which includes funct […]
```

## Rollback et décision suivante

Annuler uniquement les modifications des copies de laboratoire, restaurer leur témoin et conserver sources/mesures/échecs. Ne pas toucher au jeu principal ni publier. Une seule action humaine bloquante : ouvrir le dossier autorisé dans une session Codex locale Windows ; l’accès cloud ne donne pas accès à Studio ni à B3/C1.
