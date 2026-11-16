---
id: "2e6c6823-da8c-5cea-9524-d1408b1a0efc"
type: "experiment"
status: "PLANNED"
verification: "not_verified"
revision: 2
event_sha256: "90e64e5f7c9e0a8f463cccd6d00a37166f72a5ec4ac4b55322d21958d5b61043"
created: "2026-11-16T02:12:08.638905+00:00"
updated: "2026-11-16T02:12:08.642548+00:00"
---

# Sapin enneigé Roblox : qualité nocturne et coût de rendu

[[_VDN-Experiences]]

Données rapportées ; les conditions de réutilisation restent obligatoires.

```json
{"created_at": "2026-11-16T02:12:08.638905+00:00", "environment": {}, "event_sha256": "90e64e5f7c9e0a8f463cccd6d00a37166f72a5ec4ac4b55322d21958d5b61043", "hypothesis": "Comparer qualité et coût sous les mêmes conditions, sans supposer une méthode gagnante.", "id": "2e6c6823-da8c-5cea-9524-d1408b1a0efc", "parameters": {"assets": [], "method": "B"}, "problem": "Sapin enneigé Roblox : qualité nocturne et coût de rendu", "protocol": {"batch": "snowy-spruce-v10", "controls": {"camera": null, "device": null, "graphics_quality": null, "lighting": null, "resolution": null, "sample_s": null, "studio_version": null, "tree_count": null, "warmup_s": null}, "metrics_template": {"artifact_count": null, "asset_bytes": null, "frame_time_ms": null, "materials": null, "night_readability_rating": null, "textures": null, "triangles": null}, "not_executed": true, "procedure": ["Créer un place privé VDN — Laboratoire et définir Workspace.VDNLab=true.", "Créer deux modèles isolés avec la même silhouette et les mêmes dimensions cibles.", "A : tronc, branches et aiguilles en géométrie simplifiée ; B : même tronc avec cartes de feuillage et atlas.", "Exporter des copies distinctes ; consigner versions Blender/Studio, options FBX et identifiants des assets.", "Fixer caméra, lumière nocturne, appareil, qualité et résolution identiques ; documenter tous les contrôles.", "Mesurer chaque méthode seule, après préchauffage, puis répéter trois fois en alternant A/B.", "Compter triangles dans Blender ; mesurer octets des exports locaux ; capturer les mêmes vues de nuit.", "Consigner textures, matériaux, artefacts, MicroProfiler et durée des trames ; conserver captures et journaux."], "rollback": "Supprimer les copies du laboratoire ; aucun changement au jeu principal.", "validation": ["Aucun paramètre comparatif inconnu ; trois répétitions documentées et données brutes jointes.", "Comparer silhouette et lisibilité par annotation humaine ; l’échelle 1–5 est subjective.", "Définir les seuils de performance et de qualité pour l’appareil cible avant le test.", "Examiner les différences et limites avant toute recommandation conditionnelle."], "zone": "Forêt et végétation"}, "references": [], "results": [], "reuse_conditions": [], "review": null, "revision": 2, "spec_sha256": "9718f4e1c8f290d896dc7e473f99532ec929e2ab05494f737868a49d15519f40", "status": "PLANNED", "technique": "Cartes de feuillage", "updated_at": "2026-11-16T02:12:08.642548+00:00", "verification": "not_verified"}
```

<!-- Exemple généré en dossier temporaire ; aucune mesure Studio. -->
