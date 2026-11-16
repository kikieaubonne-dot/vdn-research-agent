# Mesure RAG sur le même corpus

Le RAG historique SQLite/BM25 et ses équivalences FR/EN filtraient déjà les notes
rejetées. Le pipeline Intelligence relisait pourtant leurs citations. Le défaut
a été reproduit avant correction. Sur le corpus inchangé : **369 →285 documents
secondaires actifs**, dont **84 →0 issus de notes rejetées**. Les 99 notes et leurs
raisons sont conservées ; ce changement ne supprime aucun original.

Benchmark : `bench.evaluate_lab_retrieval`, 22 questions annotées préexistantes
(rag_queries et rag_development_v8), mêmes sources et empreinte de corpus. Aucun
nouveau label inventé à partir du classement obtenu. Les labels sont un petit jeu
de développement, non exhaustif et non aveugle ; « précision » signifie présence
parmi les seuls IDs attendus listés, pas jugement sémantique complet.

| Stratégie | Précision vs IDs listés @5 | Rappel @5 | MRR | nDCG @5 |
|---|---:|---:|---:|---:|
| BM25 texte | 0,2303 | 0,9773 | 0,9129 | 0,9270 |
| Couverture bilingue existante | 0,2303 | 0,9773 | 0,9167 | 0,9290 |
| Intelligence lexical | 0,1583 | 0,6364 | 0,4015 | 0,4627 |

Ces métriques restent identiques avant/après sur ce jeu ; le nombre moyen de
résultats rejetés d'Intelligence passe de 0,0909 à 0. Aucun gain de rappel ou MRR
n'est revendiqué. Les latences brutes figurent dans les JSON ; caches/charge varient,
aucun gain causal de vitesse n'en est déduit. Le RAG historique demeure plus
performant sur ces annotations ; il est conservé, pas remplacé par un modèle.

Les requêtes par tâche/chapitre réutilisent les ancres du projet et livrent des
références candidates avec leur portée. Elles ne transforment pas leur méthode
proposée en fait. Une requête de chapitre donne une décomposition et des renvois
vers le détail plutôt qu'un long assemblage de documents complets.

Hybride, reranking neural et embeddings : NON EXÉCUTÉS, aucun modèle installé et
sélectionné. La comparaison logicielle historique reste disponible, sans annoncer
un bénéfice neural. Citation correcte, réponse avec preuve, applicabilité moteur
et utilité humaine restent des métriques différentes ; le classement d'IDs ne
les mesure pas. Les tests de citations sont des contrôles mécaniques distincts.

```powershell
& $python -m bench.evaluate_lab_retrieval --output C:\lab\retrieval.json
```

[Avant](proofs/retrieval-before.json) · [Après](proofs/retrieval-after.json).
Aucun appel Claude, aucune économie de quota mesurée. Le précédent benchmark de
briefings plus courts reste une mesure de caractères, pas de quota.
