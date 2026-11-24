# Benchmark VDN

_2026-11-24T13:59:06+00:00 · jeux de test 5af458231264_

| Indicateur | Valeur |
|---|---:|
| relevance_f1 | 0.762 |
| relevance_precision | 0.667 |
| rag_hit_at_3 | 0.9 |
| rag_mrr | 0.9 |
| negatives_clean | 1.0 |
| planner_ok | 1.0 |

Filtre de pertinence sur 54 cas réels étiquetés à la main : VP 8, FP 4, FN 1, VN 41.

- faux négatif : Feature Request: Bone Scaling & Deformation Support (limite : demande de fonctionnalité, utile pour os/vent)
- faux positif : Colosseum build 
- faux positif : leonisbel/night-hunt (limite : jeu d'horreur nocturne, code non ciblé)
- faux positif : Feedback on this horror house interior (limite : retours d'apparence, peu technique)
- faux positif : nightcycle/quick-part 

RAG : 10 questions (FR/EN), réussite@1 0.9, réussite@3 0.9, MRR 0.9, tokens moyens 1113 (max 1499), questions négatives propres 1.0.

- manqué : « importer un squelette personnalisé, os qui buguent » (rang None)

## ⚠ Régressions

- rag_hit_at_3 : 0.9 (meilleur 1.0)

Limites : étiquettes posées par une seule personne (Claude) ; petit échantillon ; mesure le tri et la récupération, PAS la justesse des techniques ni leur rendu dans Roblox.
