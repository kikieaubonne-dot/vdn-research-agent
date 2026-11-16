# Recherche spécialisée, règles et frontières

`Question → contexte Bible/contraintes → branche → lacunes/preuves → bibliothèque
lexicale → préparation bornée → reçus → briefing → détail → expérience humaine
→ mémoire → recherche ciblée`.

Les responsabilités existantes d’analyse, citations, critique, modèles, mémoire,
MCP et quotas sont réutilisées. Il n’y a pas de nouveau système multi-agent.

## Arbre et lacunes

Catalogue validé, IDs slash stables, parents et dépendances acycliques. Chaque
nœud a objectif/question, tâche, importance, concepts requis, query, aliases,
kind visuel/technique/gameplay et statut PROPOSED. Le contexte de chaque tâche
provient de la Bible ; une proposition technique ne devient pas une décision
narrative. Les versions utilisateur contradictoires provoquent CONSTRAINT_CONFLICT.
Les nombres fournis par l’utilisateur restent des contraintes proposées, pas des
paramètres établis par les sources.

Le plan descend depuis une branche choisie et explique chaque arrêt : limite de
profondeur/nœuds, faible importance en veille, contexte documentaire disponible,
portée permise épuisée, revue humaine sous conditions. Une référence sur un parent
ne couvre pas automatiquement ses descendants. Les dépendances peuvent apparaître
hors du sous-arbre sélectionné ; elles restent identifiées et ordonnées avant
leur consommateur dans les six unités maximum. Profondeur conceptuelle ≤8 ; les
unités de la file V10 gardent profondeur1 et les quotas configurés existants.

Priorité explicable : importance×10, +15 pour échec lié, +10 sans contexte original.
Ce nombre sert à ordonner ; ce n’est pas une probabilité de réussite. Deux critères
additionnels ne sont pas modélisés quantitativement : utilité sémantique et
nouveauté d’une technique. Aucun score de confiance du modèle n’est une preuve.

La lacune compare les concepts requis à des passages du moteur cible, en conservant
hash/offset/section/date/version/provenance/incomplétude. Les sources Blender de
version différente sont exclues, les versions inconnues sont explicites. Les
passages hostiles sont exclus ; les sources ne peuvent demander aucune commande,
permission, clé, téléchargement ou activation. La correspondance lexicale seule
ne ferme jamais une lacune. Une revue explicitement liée à branche/assets/build
peut clore le besoin sous ces conditions, sans déduire une réussite universelle.

## Bibliothèque

MAIN : note documentée/reproduite/validée, URL et citation. RESERVE : autres
candidates non rejetées. ARCHIVE : rejet/obsolescence. Ces niveaux de curation ne
modifient ni les statuts historiques ni les preuves des sources. Aucun déplacement
ou effacement, aucune multiplication de notes par scène.

La recherche par branche fusionne la requête utilisateur et la requête spécialisée
via rangs réciproques. Le moteur léger historique demeure accessible séparément.
La fusion a été conservée uniquement dans ce parcours après la comparaison publiée,
avec le premier essai régressif archivé et son coût de latence. Les candidats ne disparaissent pas
parce que MAIN est vide. Les techniques d’un autre moteur sont isolées comme
incompatibles, pas proposées comme fonctions Roblox.

Identité de technique : ID stable du problème/branche partagé entre scènes.
Identité d’évidence : corps complet de note exactement normalisé +version+conditions+niveau. Un aperçu tronqué ne sert jamais d’identité.
Plusieurs alias/sources peuvent pointer vers le même extrait. Des paraphrases ou
sources citant une origine commune ne deviennent pas des preuves indépendantes ;
leur équivalence nécessite encore examen humain. Les liens de sources sont des
références de notes ; le détail distingue les captures originales réellement locales.

## Reçus, collecte et échecs

Sessions V10 existantes +enveloppe `lab/ocean/roots/sessions/<id>.json`, contrôles
pause/reprise/stop avec locks existants, aucune remise à zéro. Les changements
Bible/catalogue bloquent l’exécution d’un plan périmé ; compteurs et fichiers restent.
L’exécution nécessite configuration réseau existante et `--allow-network` explicite.

Les snapshots ont une provenance primaire locale ; les notes et rapports publiés
restent secondaires. Le collecteur suit les sources autorisées par tâche et des
liens bornés via OceanWeb : robots, TLS/DNS, permissions, retry et quotas conservés.
Aucun collecteur général YouTube/Reddit ni accès payant ajouté. Les providers
facultatifs non configurés sont signalés ; un refus réseau n’est pas contourné.

Un reçu d’évaluation est écrit avant une collecte ; les mises à jour survivent aux
erreurs suivantes. Une collecte accessible mais insuffisante produit un reçu de
portée partielle, conservant la lacune. La même empreinte évite de refaire les mêmes
lectures/requêtes ; changement de contenu, version, condition, expiration, configuration,
Bible, catalogue ou expérience invalide le reçu. Les anciennes révisions restent.
Une réponse inaccessible reste une erreur détaillée, avec queue reprise sans unité
abandonnée running. Les compteurs HTTP et fetch gardent leurs sens historiques :
HTTP = tentatives transport, dont robots/reprises ; fetch = tentative documentaire,
y compris cache. Les niveaux tick/session/jour sont ceux du moteur V10.

Un résultat FAILED lié à branche ou tâche reste consultable. Hypothèses diagnostiques
explicites, sous-arbres ciblés, alternatives non déclarées gagnantes. La procédure
répétée est suspendue dans le briefing/détail tant qu’une nouvelle justification ou
condition n’est pas apportée. `guard_repeat` historique protège aussi l’écriture.
Aucun essai n’est exécuté automatiquement et aucun client MCP ne peut promouvoir
VERIFIED/HUMAN_APPROVED. Les essais synthétiques restent dans des copies isolées.

## Contrats et exports

27 outils MCP inchangés : `plan_ocean(goal="tree:forest/…")`,
`get_intelligence_brief(question="tree:forest/…")`, puis
`synthesize_technical(question=detail_question)` pour approfondir. Les outils de
chapitre et les questions classiques conservent leurs routes. `ocean_status` expose
séparément `root_research`, sans changer les sessions historiques.

Le briefing court a omissions et accès au détail ; ne pas appeler un résultat tronqué
un protocole complet. Détail : sources/conditions/paramètres attribués/protocole/alternatives/
échecs/rollback. Sans preuves suffisantes, faits vides et candidates séparées.
Des pages `_VDN-*` réservées relient bibliothèque, scènes et mémoire ; elles sont
exclues du RAG primaire. L’index SQLite est un cache dérivé et peut être reconstruit
lors de la lecture. Aucun original personnel n’est déplacé.
