---
id: "9aeaea86-b2ec-5c0d-a7d7-9c8ff8ead522"
type: "experiment"
status: "PLANNED"
verification: "not_verified"
revision: 2
event_sha256: "4f078f9419c9b0af47924ed09808d0d74a504b299ead9cb8289df9015473f178"
created: "2026-11-16T02:12:08.630464+00:00"
updated: "2026-11-16T02:12:08.635322+00:00"
---

# Sapin enneigé Roblox : qualité nocturne et coût de rendu

[[_VDN-Experiences]]

Données rapportées ; les conditions de réutilisation restent obligatoires.

```json
{"created_at": "2026-11-16T02:12:08.630464+00:00", "environment": {}, "event_sha256": "4f078f9419c9b0af47924ed09808d0d74a504b299ead9cb8289df9015473f178", "hypothesis": "Comparer qualité et coût sous les mêmes conditions, sans supposer une méthode gagnante.", "id": "9aeaea86-b2ec-5c0d-a7d7-9c8ff8ead522", "parameters": {"assets": [], "method": "A"}, "problem": "Sapin enneigé Roblox : qualité nocturne et coût de rendu", "protocol": {"batch": "snowy-spruce-v10", "controls": {"camera": null, "device": null, "graphics_quality": null, "lighting": null, "resolution": null, "sample_s": null, "studio_version": null, "tree_count": null, "warmup_s": null}, "metrics_template": {"artifact_count": null, "asset_bytes": null, "frame_time_ms": null, "materials": null, "night_readability_rating": null, "textures": null, "triangles": null}, "not_executed": true, "procedure": ["Créer un place privé VDN — Laboratoire et définir Workspace.VDNLab=true.", "Créer deux modèles isolés avec la même silhouette et les mêmes dimensions cibles.", "A : tronc, branches et aiguilles en géométrie simplifiée ; B : même tronc avec cartes de feuillage et atlas.", "Exporter des copies distinctes ; consigner versions Blender/Studio, options FBX et identifiants des assets.", "Fixer caméra, lumière nocturne, appareil, qualité et résolution identiques ; documenter tous les contrôles.", "Mesurer chaque méthode seule, après préchauffage, puis répéter trois fois en alternant A/B.", "Compter triangles dans Blender ; mesurer octets des exports locaux ; capturer les mêmes vues de nuit.", "Consigner textures, matériaux, artefacts, MicroProfiler et durée des trames ; conserver captures et journaux."], "rollback": "Supprimer les copies du laboratoire ; aucun changement au jeu principal.", "validation": ["Aucun paramètre comparatif inconnu ; trois répétitions documentées et données brutes jointes.", "Comparer silhouette et lisibilité par annotation humaine ; l’échelle 1–5 est subjective.", "Définir les seuils de performance et de qualité pour l’appareil cible avant le test.", "Examiner les différences et limites avant toute recommandation conditionnelle."], "zone": "Forêt et végétation"}, "references": [], "results": [], "reuse_conditions": [], "review": null, "revision": 2, "spec_sha256": "42096f49d9c845f82f02eccf37c64912c2f6f14c92de74feda94f8ceaa9c1d76", "status": "PLANNED", "technique": "Géométrie simplifiée", "updated_at": "2026-11-16T02:12:08.635322+00:00", "verification": "not_verified"}
```

<!-- Exemple généré en dossier temporaire ; aucune mesure Studio. -->
