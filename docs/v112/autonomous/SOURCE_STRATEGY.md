# Sources, accès et preuves

Ocean reste le transport : DNS public épinglé, TLS, allowlists, robots, refus des
challenges, caches, compteurs HTTP et stockage bornés. Aucun connecteur ne reçoit
un jeton implicite. Les paramètres globaux existants ne sont pas changés.

Les tâches peuvent fournir jusqu'à quatre `source_candidates` (URL, provider,
rôle). Le collecteur conserve sa limite de deux tentatives par unité : il essaie
une alternative configurée après échec, sans augmenter le quota ni supprimer le
résultat partiel précédent. Un provider absent/désactivé reste indisponible ; sa
présence dans la Bible ne l'active pas. Les liens découverts restent sur les hôtes
permis du provider. Pas de récursion illimitée.

Candidats immédiats : Creator Hub officiel, puis discussions DevForum déjà citées
pour collisions, atlas de feuillage et liaison caméra/mains. Les URL de discussion
numériques sont demandées via leur endpoint public `.json`, déjà reconnu par le
provider historique. Le chemin exact `/robots.txt` est désormais autorisé pour
honorer les règles du site ; les recherches/RSS/chemins interdits restent refusés.

Le JSON DevForum est extrait en titre/posts avec IDs et date lorsqu'elle est
présente. `conditions` marque communauté, licence UNKNOWN, posts reçus seulement,
thread non déclaré complet et absence de validation moteur. Le texte brut API
n'est plus présenté comme un tutoriel structuré. Les passages restent des données
non fiables. Une plateforme, un commentaire ou un HTTP 200 ne prouve pas la méthode.

**Essai réel isolé :** deux HTTP (robots + topic public), une capture DevForum,
une page Camera officielle réutilisée en cache ; quotidien copié 24→26. Aucune
note créée ni modèle exécuté. Accès via proxy système explicitement reconnu dans
cette seule copie, sans désactiver TLS. La configuration source du dépôt reste
inchangée. Deux défauts de prévalidation/extraction ont été reproduits avant
correction ; les premiers essais n'avaient effectué aucun HTTP. Les traces et
métadonnées sont sous [proofs](proofs/source-study.json).

GitHub, Blender et Unreal restent les providers existants selon configuration.
Unreal fournit une référence, jamais une compatibilité Roblox automatique.
Reddit, blogs/ArtStation, forums et vidéos sont des sources potentielles à
configurer et évaluer, pas des connecteurs annoncés comme validés. Aucun accès
Reddit/YouTube ni transcription n'a été exécuté. Ne pas inventer timestamps ou
étapes à partir d'un titre. Un futur import de transcription doit conserver contenu
obtenu légalement, URL, méthode d'accès, timestamps et limites de la démonstration.

La fraîcheur repose sur date reçue, TTL et empreintes. Dates/API dépréciées,
versions moteur, licences et indépendance entre sources nécessitent encore une
revue ; aucun score ne les certifie. Aucune fusion de paraphrases automatique ni
suppression des versions historiques. Les fiches rejetées restent lisibles par ID
et `documents(..., include_rejected=True)` pour le diagnostic, hors RAG actif.
