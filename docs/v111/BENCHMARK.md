# Évaluation et limites scientifiques

[Résultats bruts](benchmark.json), [jeu annoté](../../bench/intelligence_cases.json).
36 contrats explicites couvrent intention simple/complexe, proximité des
questions, français/anglais, mauvaises citations, nombres absents, source
secondaire, offsets/SHA altérés, versions, obsolescence, contradiction,
injection et document long. **Ce sont des références synthétiques rédigées
pour tester les contrats, pas une vérité terrain Roblox ou Blender.** Elles
ne sont jamais enregistrées comme connaissances réelles.

Le résultat local est **36/36**, dont 20 classifications d'affirmations conformes
aux annotations. Cela vérifie la mécanique d'attribution et d'abstention sur
ces cas ; cela ne mesure pas la vérité technique, l'implication sémantique
générale ni la robustesse à toutes les attaques.

## Comparaison sur le même corpus

Huit tâches identiques : compréhension, paramètres, synthèse, contradictions,
procédure, refus d'inventer, JSON et anglais vers français. Le runner compare
la synthèse V11 déterministe inchangée avec le pipeline V11.1 déterministe.
Les deux reçoivent le même corpus de références synthétiques. Le JSON conserve
questions, sorties du registre, abstention, documents sélectionnés, précision
et rappel par document annoté, latences et allocation mémoire Python.

| Condition | Exécution et portée |
|---|---|
| A — V11 déterministe | Exécutée, synthèses existantes sur le corpus commun |
| B déterministe — V11.1 | Exécutée, registre/offsets/critique/protocoles structurés |
| B — modèle local | Non exécutée : service Ollama inaccessible, aucun poids disponible |
| C — embeddings seuls / hybride | Non exécutée avec un modèle réel ; comparaison facultative implémentée |

Les champs supplémentaires montrent une meilleure **structuration mesurable**,
pas une meilleure décision technique démontrée. La pertinence est annotée au
niveau des documents, pas par une revue humaine complète de chaque passage.
La complétude d'un protocole ne prouve pas son utilité. Les timings portent sur
des chemins différents ; pas de pourcentage général de gain annoncé.

La VRAM, les tokens par seconde et le taux de JSON valide **d'un vrai modèle**
restent non mesurés. Les tests NDJSON/JSON, sorties fautives, annulation et
vecteurs utilisent des fixtures. Aucun modèle par défaut n'est recommandé.
Un éventuel jugement sémantique reste facultatif/non certifiant ; aucun juge
sémantique supplémentaire n'est activé dans cette livraison.

## Reproduire

```powershell
& $python -m bench.evaluate_intelligence --output work\deterministic-quality.json
& $python -m bench.evaluate_intelligence --models NOM_EXACT_INSTALLE --allow-model --max-cases 1 --output work\model-quality.json
& $python -m bench.evaluate_intelligence --with-embeddings --allow-model --output work\embedding-quality.json
```

Les exécutions réelles exigent configuration/permissions et partagent les quotas
V11, dont une génération/jour par défaut. Elles peuvent être partielles ; le
rapport conserve les erreurs/arrêts plutôt que d'élargir les budgets. Le mode
embeddings compare lexical, sémantique et RRF sur le même corpus, et précise
qu'il mesure la récupération seule, pas une génération hybride de bout en bout.

## Démonstration sur documents réels

[demo.json](demo.json) distingue cette exécution des références synthétiques.
Sources Roblox réellement capturées en V11, puis nouvelle page Blender
officielle, collectée avec robots/transport V11 sous proxy explicitement
configuré dans le laboratoire isolé. La collecte ajoute **2 HTTP**, compteur
copié **11 → 13** ; un diagnostic local ultérieur ajoute une réservation.
Sources, erreurs et anciennes analyses sont conservées.

Question finale demandée : trois problèmes identifiés, huit passages localisés,
cinq affirmations attribuées sous les règles mécaniques, trois protocoles non
exécutés. Le document Blender indique **5.3** dans son en-tête et est tronqué :
aucune compatibilité avec le Blender 5.2 utilisateur ou Roblox n'est supposée.
Une deuxième analyse identique réutilise la mémoire, sans génération ni HTTP
supplémentaire pour la synthèse. Les textes complets restent privés ; la preuve
publiée conserve offsets, SHA, décisions et protocoles, sans recopier les sources.
