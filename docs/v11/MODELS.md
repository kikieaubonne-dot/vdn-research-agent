# Modèles facultatifs, coûts et matériel

Par défaut `model_backend=none`, recherche et mémoire fonctionnent sans Claude
ni abonnement. La synthèse déterministe extrait des preuves et applique des
protocoles de domaine ; elle ne remplace pas une compréhension générale.

Exécuter `python -m agent.v11 hardware` avant de choisir un modèle. Pour une
RTX 4060 Ti 8 Go, considérer poids quantifiés, contexte/KV, runtime et autres
applications. Commencer avec un petit modèle instruction compatible JSON que
l'opérateur a choisi, mesurer RAM/VRAM et latence, puis décider. Aucune garantie
de taille/contexte n'est déduite du nom du GPU. Ici : GPU non détecté, pas
d'Ollama disponible ; aucun modèle ni embedding réel n'a été évalué.

## Ollama local

Installer Ollama séparément et choisir/télécharger explicitement un modèle
selon sa licence et sa capacité matérielle. Le projet ne télécharge aucun poids.
Dans `config/v10.json`, renseigner `models.local.enabled=true`,
`endpoint="http://127.0.0.1:11434"`, `model="NOM_INSTALLE"`, `vision=false`.
Dans `config/ocean.json`, choisir `model_backend="local"`. Préparer ensuite
un nouvel objectif avec ce contrat : la configuration du modèle est figée dans
son enveloppe et les restrictions actuelles restent prises en compte.

Une seule analyse est permise par objectif **et par jour UTC** par défaut.
Le transport JSON `/api/generate` est borné ; l'échec revient au candidat
déterministe déjà écrit. Le modèle sélectionne des preuves littérales et propose
questions/étapes attribuées dans un sidecar privé. Il n'ajoute pas de vérité.

## Embeddings facultatifs

Configurer `ocean.json.semantic` avec `enabled=true`, endpoint loopback littéral
`http://127.0.0.1:11434` et un modèle d'embedding réellement installé prenant
en charge `/api/embed`.

```powershell
& $python -m agent.v11 semantic-index --max-items 4 --dry-run
& $python -m agent.v11 semantic-index --max-items 4 --apply
& $python -m agent.v11 search "personnage coincé près des épicéas" --semantic
```

Index borné, empreintes/model associés, compteur HTTP journalier partagé. Une
recherche sémantique demandée peut appeler le service local ; le mode lexical
reste disponible sans socket. Indisponibilité, index corrompu ou verrou : retour
lexical explicite. Les tests de vecteurs utilisent des fixtures ; aucun gain
sémantique avec modèle réel n'est revendiqué.

## API distante compatible OpenAI

Configurer explicitement `models.remote` dans `v10.json` : enabled, endpoint
HTTPS, nom, `key_env="VDN_REMOTE_MODEL_KEY"`. Placer la clé dans l'environnement
du processus, jamais dans le dépôt, les fiches ou un JSON commité. Aucun accès
API distant activé ici. `ocean.model_backend="remote"` nécessite un plafond
`max_cost_usd` positif et une `remote_reservation_usd` positive qui couvre le
coût maximal conservateur de **chaque** appel pour ce fournisseur/contexte.
Vérifier son tarif et sa politique de données avant activation.

Le système réserve appels/coût **avant** l'effet, sur l'objectif et le jour.
C'est une estimation conservatrice, pas une facture ni un contrôle du compte
fournisseur ; choisir une réserve trop faible ne borne pas sa facturation.
Le transport hérité limite la réponse JSON, 1 024 tokens générés et le temps.
Les sources de l'objectif envoyées au modèle restent des données non fiables.
Les appels modèles consomment aussi le budget HTTP V10 et ne sont jamais une
preuve indépendante.
