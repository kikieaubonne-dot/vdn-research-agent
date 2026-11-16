# Choisir et comparer les modèles

**Aucun modèle recommandé par défaut** : aucun service ni poids disponibles
dans l'environnement de livraison, donc aucune supériorité IA démontrée.
Les réponses des tests de transport sont des fixtures identifiées.

Tags vérifiés dans le catalogue officiel le 16 novembre 2026 ; ces informations
ne prouvent ni installation locale ni capacité mémoire effective :

| Tag exact | Quantification affichée | Taille catalogue | Licence indiquée |
|---|---|---:|---|
| [qwen3:1.7b](https://ollama.com/library/qwen3:1.7b) | Q4_K_M | 1,4 GB | Apache 2.0 |
| [qwen3:4b](https://ollama.com/library/qwen3:4b) | Q4_K_M | 2,5 GB | Apache 2.0 |
| [qwen3:4b-q8_0](https://ollama.com/library/qwen3:4b-q8_0) | Q8_0 | 4,4 GB | Apache 2.0 |
| [gemma3:1b](https://ollama.com/library/gemma3:1b) | Q4_K_M | 806 MB | Gemma Terms of Use |
| [gemma3:4b](https://ollama.com/library/gemma3:4b) | Q4_K_M | 3,4 GB | Gemma Terms of Use |
| [gemma3:4b-it-qat](https://ollama.com/library/gemma3:4b-it-qat) | Q4_0 (QAT) | 4,0 GB | vérifier les termes Gemma et métadonnées installées |

Lire la licence effective du tag retenu et la conserver avec `/api/show`.
Les alias peuvent évoluer : le diagnostic enregistre le digest réellement
installé et les paramètres. Qwen3 peut consacrer des tokens au raisonnement ;
si le JSON final n'arrive pas sous la limite, l'analyse est rejetée proprement.
Les modèles vision ne sont pas évalués comme vision par ce pipeline textuel.
Un autre instruct local peut être testé par son nom exact s'il produit le JSON
attendu ; aucune liste d'achat ni service payant imposé.

Pour la RTX 4060 Ti 8 Go : la taille catalogue n'est pas la VRAM totale requise.
Ajouter KV cache, contexte, runtime, éventuel projecteur et autres applications.
Comparer d'abord un seul candidat compact sous mode économie ; relever VRAM
libre, RAM, modèles chargés, latence, tokens réellement rapportés et échecs.
Ne pas charger tous les candidats, ni fermer des processus automatiquement.

Le routeur choisit le compact en économie ou pression GPU élevée ; un objectif
plus complexe peut utiliser `capable_model` si configuré et installé. Il ne
déduit pas la qualité du nombre de paramètres. Le budget temps est conservateur ;
il n'apprend pas encore automatiquement un profil de latence par matériel.

Les huit tâches annotées sont identiques pour chaque candidat : intention,
paramètres absents, synthèse, contradiction, procédure, refus d'inventer,
JSON et source anglaise/réponse française. Comparer les résultats bruts et la
grille, puis demander une revue humaine des procédures. Le plafond modèle
commun peut ne permettre qu'une tâche par jour : conserver les rapports
partiels et poursuivre ultérieurement, sans réinitialiser le registre.

## Distant facultatif

Niveau 3 seulement si aucun local n'est sélectionné ET :
`intelligence.remote_allowed=true`, `sensitivity=public` choisie par l'opérateur,
`v10.network_enabled=true`, `models.remote.enabled=true` avec endpoint/modèle/clé
en environnement, `ocean.model_backend=remote`, réserve positive et plafond
de coût suffisant. L'appel réutilise l'adaptateur V11 et son registre commun.
`public` est une déclaration de l'opérateur, pas une détection automatique des
données privées. Vérifier les textes envoyés avant activation. Aucune clé dans
Git, aucun appel payant exécuté ici ; coût réel inconnu, réserve séparée.
