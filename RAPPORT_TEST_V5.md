# Rapport de test — VDN Research Agent V5 (15/11/2026)

Tout ce qui suit a été **exécuté** dans un environnement Linux isolé (Python 3, sans accès réseau aux sources). Ce qui n'a pas pu être exécuté est listé à part, sans résultat inventé.

## 1. Audit de la V4 (causes prouvées sur les fichiers du dépôt)

| Symptôme V4 | Cause démontrée |
|---|---|
| Récompenses méta toutes à 0.00 | La pertinence était calculée sur `nom du dépôt + description`, alors que GitHub trouvait le mot dans le README → 0 même pour un bon résultat |
| Requêtes inutiles qui reviennent | Le planificateur triait par « moins exécutée d'abord » : les longues requêtes V3 générées passaient toujours devant |
| 1 seul résultat sans rapport | Requêtes de 8–10 mots alors que la recherche GitHub exige *tous* les mots (reproduit : 1 dépôt hors sujet) |
| Modificateurs absurdes | `language:Python`, « workaround settings » ajoutés aux requêtes Roblox |
| DevForum vide | La recherche DevForum est interdite par son robots.txt |
| Compteurs incohérents | 8 requêtes × 2 fournisseurs = 16 essais, « 19 » = somme des résultats |
| Notes poubelle acceptées | Score V1 sans seuil |

## 2. Tests unitaires

`python -m unittest discover -s tests` → **52 tests, OK** (20 anciens + 32 nouveaux).

Couverture des nouveaux tests : normalisation du texte, fournisseurs (avec réponses enregistrées), refus de la recherche DevForum, filtrage, schéma de note, dédoublonnage, aller-retour du frontmatter, migration sans perte et idempotente, RAG (budget, français, mise à jour incrémentale, sécurité des chemins), protocole MCP, ancrage des réponses Ollama, planificateur, retour arrière méta, chaîne complète de bout en bout, erreur de fournisseur signalée.

## 3. Migration des données existantes

- 54 notes migrées, **0 supprimée**.
- Vérification ligne par ligne contre le commit d'origine : **0 ligne de contenu perdue, 0 champ perdu** (les anciens champs sont recopiés en `legacy_status`, `legacy_source_type`, `legacy_topic`, `legacy_score_heuristique`, `legacy_collected_utc`).
- Une première version de la migration perdait `source_type` et l'heure de collecte ; corrigé avant livraison, avec un test dédié.
- Reclassement : 5 `documenté`, 7 `candidat`, 42 `rejeté` (raison écrite dans chaque note). Aucune note `reproduit` ni `validé`.

## 4. Benchmark hors ligne (`python -m agent.run bench`)

| Mesure | Valeur | Base |
|---|---|---|
| Filtre : précision | 0,667 | 54 cas réels étiquetés à la main, 9 positifs |
| Filtre : rappel | 0,889 | |
| Filtre : F1 | 0,762 | 8 vrais positifs, 4 faux positifs, 1 faux négatif |
| RAG : hit@1 / hit@3 / MRR | 1,0 / 1,0 / 1,0 | 10 questions FR/EN |
| RAG : tokens par réponse | ~1 170 en moyenne, 1 474 max | budget 1 500 |
| Notes indésirables jamais remontées | 1,0 | portfolios, RNG |
| Requêtes de 2–4 mots | oui | |

Prudence :
- Le RAG à 1,0 vient d'une petite bibliothèque (12 notes non rejetées). C'est un test facile, pas une preuve de qualité à grande échelle.
- Les cas du filtre ont été étiquetés par Claude, pas par toi. Les règles n'ont pas été ajustées sur ces cas, pour éviter de tricher sur le score.
- Faux positifs restants : Colosseum build, night-hunt, retour sur un intérieur de maison d'horreur, nightcycle. Faux négatif : Bone Scaling.
- Aucune comparaison chiffrée avec la V4 sur des recherches en ligne : impossible ici. Je n'affirme donc pas que la V5 trouve mieux en ligne.

## 5. Serveur MCP (stdio réel)

- `initialize` → version 2025-06-18.
- 3 outils listés.
- « feuillage transparent de loin » → 2 bonnes notes (foliage transparent, texture atlas), 382 tokens.
- « escalade rebord » → note ledge climbing.
- `read_knowledge("../../etc/passwd")` → refusé (`isError`).

## 6. Recherche hors réseau (comportement en panne)

`python -m agent.run research` sans réseau :
- pas de plantage ;
- 0 note créée ;
- 3 erreurs écrites dans `output/last_run.json` : index officiel indisponible, sitemap DevForum indisponible, GitHub HTTP 403.

Un défaut où l'échec de l'index était effacé du rapport a été corrigé pendant ce test.

## 7. État d'avancement

| Élément | État |
|---|---|
| Audit V4 | Réalisé |
| Étude local-deep-researcher / GPT Researcher / STORM | Réalisé (méthodes reprises, pas de dépendance ajoutée) |
| Moteur multi-sources | Réalisé, **testé hors ligne** sur réponses enregistrées |
| Filtre + raisons de rejet | Réalisé, testé, benchmarké |
| Notes Obsidian + statuts + index | Réalisé, testé |
| Migration sans perte | Réalisé, vérifié ligne par ligne |
| RAG SQLite FTS5 | Réalisé, testé, benchmarké |
| Serveur MCP lecture seule | Réalisé, testé en stdio |
| Méta-recherche mesurée (UCB + retour arrière) | Réalisé, testé sur scénarios ; **pas encore observé sur de vraies recherches** |
| Ollama (analyse ancrée) | Réalisé, testé avec un faux modèle ; **non testé avec Ollama réel** |
| Workflow GitHub Actions | Écrit ; **non exécuté** (pas de push possible d'ici) |
| Recherche en ligne réelle | **Bloqué ici** (réseau du bac à sable) |
| Connexion Claude Desktop | **Non testé** (pas d'accès à ton PC Windows depuis cette session pour ça) |
| Validation des techniques dans Roblox Studio | **Non fait** : aucune note n'est marquée validée |

## 8. Limites

1. **Premières vraies recherches à surveiller.** Les 2–3 premiers lancements GitHub Actions diront si les sources répondent comme prévu. Lire `output/last_run.json` et `output/meta_report.md`.
2. **DevForum par sitemap seulement.** Le DevForum interdit sa recherche. L'agent parcourt donc son plan du site par lots : la couverture grandit nuit après nuit, elle n'est pas immédiate.
3. **GitHub = source de niveau 3.** Beaucoup de dépôts sont hors sujet ; le filtre en élimine la plupart, mais pas tous (précision 0,67).
4. **Ollama ne tourne que PC allumé.** GitHub Actions ne lance pas de modèle local. Sans Ollama, l'agent collecte et filtre, sans résumé IA.
5. **Synonymes FR/EN limités** à `config/vocabulary.json`. Un mot absent ne sera pas traduit : il suffit de l'ajouter dans ce fichier.
6. **Aucune garantie de compatibilité Roblox.** Une note `documenté` veut dire « source sérieuse trouvée », pas « ça marche dans ton jeu ». Seul ton essai dans Studio peut la passer en `reproduit` / `validé`.
7. **Économie de tokens non mesurée en conditions réelles.** Une recherche coûte ~1 200 tokens au lieu de lire des notes entières, mais aucun pourcentage n'est promis.
