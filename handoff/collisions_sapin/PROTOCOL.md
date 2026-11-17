# Collisions sapin — H001/H002, essai minimal A/B1/B2/B3

**NON CERTIFIÉ — procédure préparée, aucun résultat Studio produit par Codex.**
Code de référence : `9a7b0b05e04ad3c6feed6886fc5e2c676e7d254f` ; compatibilité contractuelle à vérifier aussi sur `c93fe9bc944a7255752a7eded590ad039f568145`. Les relevés ci-dessous sont fournis par Claude depuis Windows le17novembre2026, pas des mesures effectuées par Codex. Les trois fichiers locaux agent/intelligence.py, config/v10.json et tests/test_markdown_filtering.py sont intouchables par cette livraison.

## 1. Problème et corrigé de référence

Scene_Validation_C2B est la forêt jouable du prologue, pas une scène jetable. Selon Claude, tous les arbres ont CanCollide=false : JeunesEpiceas48/48, GrandsTroncs45/45, CoucheMoyenne57/57, Densite_V1158/158, Extension_T61203/1203, FondSilhouettes132/132, PremierPlan8/8. Ne pas additionner ces relevés sans vérifier les périmètres et doublons. Les144volumes de guidage/obstacles/palissades/manoir sont déjà collidables. Le défaut testé est la traversée des troncs ; retirer les collisions du feuillage serait un essai sans effet, hypothèse abandonnée avant exécution.

H002 fournie par Claude : Pin_Pale_D a un tronc stable, rayon d'environ0,7stud ; les jeunes Epicea_C2 ont un rayon de tronc d'environ0,35–1,05stud et se confondent avec le feuillage dès0,5–1m. Le mesh Ecorce inclut de grosses branches. Des semis sont enterrés d'environ3studs ; le y=4,02 rapporté pour la neige n'est pas une hauteur de terrain valable partout. Rayons sondés dans8directions à1,8/3,6/7,1studs au-dessus du terrain. Les données brutes restent à joindre.

**INTERDIT : dimensionner un proxy à partir de MeshPart.Size, de la boîte2–8studs ou d'une hauteur globale de neige.** Les raycasts mesurent aussi une représentation de collision du mesh, pas nécessairement sa surface visuelle exacte. Conserver leurs positions/hits et corroborer la silhouette de l'écorce/jupe en vue rapprochée. Les valeurs approximatives de Claude ne sont pas des paramètres universels.

## 2. Copie et sécurité avant l'essai

Référence principale rapportée : Chantier VDN, PlaceId100459254442770, version655. Copie indépendante rapportée ouverte dans une seconde instance : Documents/vdn-backups/ChantierVDN_v655_1711.rbxl,10392Ko,17-11à12h35 ; contenu rapporté identique (Workspace46102descendants, ServerStorage69148, ReplicatedStorage1915, scripts34/75, Lighting6, MaterialService38, mêmes drapeaux). **SHA256 encore UNKNOWN dans les éléments reçus.** Claude calcule Get-FileHash sur ce fichier et l'inscrit dans son retour.

Identifier la vraie instance MCP reliée à cette fenêtre/fichier local. IsStudio, PlaceId et contenus identiques ne distinguent PAS les deux fenêtres. Si l'instance ciblée n'est pas certaine, aucune écriture. Conserver la copie de référence intacte. Créer quatre nouveaux fichiers locaux A, B1, B2, B3 à partir de cette même référence, sans écrasement. A reste témoin intact. N'insérer aucun dispositif dans la place principale. Aucun Publish, SaveToRoblox, package partagé ou changement de DataStore.

## 3. Sélection figée : 4pins + les mêmes4épicéas

Dans la copie, choisir exactement4pins et4épicéas accessibles depuis le parcours autorisé, près des zones où l'on peut atteindre le tronc sans être déjà arrêté par un mur invisible. Ne déplacer aucun arbre, mur, obstacle, portail ou déclencheur. Exclure les semis enterrés et toute instance sans axe/rayon mesurable ; s'il manque4cibles dans une famille, marquer cette variante BLOCKED plutôt que compléter par des centaines de proxies.

Attribuer P1–P4 et E1–E4 dans un inventaire EXTERNE, avec chemin complet réel, position, inclinaison, photos et observations. Ce sont des étiquettes de protocole, pas des noms d'instances inventés. Les quatre E sont strictement identiques pour B2 et B3. Figer avant la comparaison : parcours, contrôleur, avatar, caméra, lampe, interactions,4obstacles, appareils, réglages et huit cibles. Ne pas changer les scripts du gameplay ou leurs filtres de raycast pendant cet essai.

## 4. Mesure du rayon, du sol et de l'axe

Pour chaque cible, relever le terrain local et deux centres de sections du tronc réellement exposé, P0 à la base accessible et P1 plus haut. Déduire l'axe U=(P1−P0)/|P1−P0| ; ne pas supposer que le UpVector du MeshPart suit le tronc, surtout s'il est incliné. Si l'axe courbe ne peut pas être raisonnablement représenté par un cylindre droit, choisir une autre cible ou déclarer la limite, sans approximation silencieuse.

Reprendre les8directions et hauteurs H002 avec le terrain propre à cette instance. Séparer les hits du tronc de ceux des grosses branches/jupe. Photographier les sections basses, médianes et hautes retenues, avec positions et unités. Pour une mesure manuelle, utiliser des repères temporaires dans une copie de mesure : points opposés sur l'écorce, coordonnées monde lues dans Properties, distances calculées entre ces points, dans deux directions perpendiculaires à U. Retirer les repères avant tous les essais. Noter l'incertitude et les points ; une largeur de boîte n'est jamais une mesure d'écorce.

Consigner r_tronc pour chaque cible (convention conservative : plus petit demi-diamètre visuel aux sections couvertes), r_jupe séparément pour E1–E4, et hauteur utilisable H. Les sondes de rayon doivent indiquer leur filtre, CanQuery et ce qu'elles rencontrent ; un hit de collision approchée n'établit pas seul un rayon visuel. Si l'écorce ne peut pas être isolée de la jupe, r_tronc reste UNKNOWN et B2 est bloquée pour cette cible.

La documentation des unités donne1stud=28cm ;3m correspondent à10,7142857studs à cette échelle. Figer H≤min(hauteur réellement retenue,10,7142857studs). Pour B2/B3, garder exactement le même axe, centre et H, bornés au tronc bas réellement exposé ; ne pas prolonger arbitrairement le cylindre dans la jupe. Confirmer l'échelle du projet si elle diffère de cette convention. Aucune hauteur optimale n'est présumée.

## 5. Variantes, facteur modifié et propriétés exactes

| Variante | Objets ajoutés depuis A | Rayon figé avant essai | Ce qui reste identique |
|---|---|---|---|
| A | Aucun | Sans objet | État actuel, arbres non collidables |
| B1 | 4cylindres, P1–P4 seulement |0,90×r_tronc, coefficient choisi dans85–95% | Tous les épicéas et volumes existants |
| B2 | 4cylindres étroits, E1–E4 seulement |0,90×r_tronc, choix expérimental explicite, pas une recommandation validée | Pins, feuillage, neige, guidage |
| B3 | 4cylindres, mêmes E1–E4 |0,60×r_jupe, choix dans55–70% | Même centre/axe/H que B2 ; seul rayon diffère entre B2/B3 |

B1/B2/B3 sont indépendantes, jamais cumulées. Ne pas équiper8arbres dans chacune, et surtout pas546. Si un coefficient est ajusté après lecture des résultats, conserver l'essai et préparer un nouvel ID ; ne pas réécrire son protocole. La variable A→B est l'ajout des4volumes avec paramètres figés ; B2→B3 isole le rayon. Aucun gagnant présumé, notamment pour la jupe plus large.

Pour chaque volume dans un dossier propre à la variante, créer un **Part**, Shape=Enum.PartType.Cylinder, Anchored=true, CanCollide=true, CanTouch=false, CanQuery=false, Transparency=1, CastShadow=false. Copier un CollisionGroup EXISTANT dont l'interaction avec le groupe réel du personnage est vérifiée ; ne modifier aucune matrice globale. Sans groupe existant adapté, BLOCKED. Pas de weld au personnage ni de script embarqué.

Le cylindre standard est dimensionné selon son axe localX : Size=(H,2r,2r). Aligner son axeX avec U et son centre avec P0+U×H/2 ; contrôler visuellement son orientation dans Studio avant Play. Exemple mathématique Luau à renseigner avec MESURES, pas exécuté ici :

```lua
-- P0, P1, H, radius sont mesurés et figés ; collider est le NOUVEAU Part de copie.
local U = (P1 - P0).Unit
local ref = math.abs(U.Y) < 0.95 and Vector3.yAxis or Vector3.zAxis
local V = ref:Cross(U).Unit
collider.Shape = Enum.PartType.Cylinder
collider.Size = Vector3.new(H, 2 * radius, 2 * radius)
collider.CFrame = CFrame.fromMatrix(P0 + U * H / 2, U, V, U:Cross(V))
```

Ce fragment n'est ni un exécuteur automatique ni un test Luau validé. L'orientation/forme réellement affichées restent à contrôler sur la build cible. Les MeshParts d'écorce, cartes, dessous et neige gardent CanCollide=false et CollisionFidelity=Default. **CollisionFidelity concerne les MeshParts/PartOperations, pas ce Part primitif.** Default, Hull, Box, PreciseConvexDecomposition sont des options documentées, pas une garantie de correspondance polygonale. Aucun changement de fidélité dans cet essai.

**Q001 — limite documentaire importante :** CanQuery ne prend pas effet comme exclusion lorsque CanCollide=true. Garder la valeur false demandée ne garantit donc pas que les nouveaux cylindres seront ignorés des raycasts. Vérifier réellement lampe et interactions, depuis les mêmes positions/directions, debout et accroupi/glissade si ces états existent. Comparer les instances touchées et distances aux témoins. Un nouveau hit du proxy ou un résultat fonctionnel perturbé est une régression. Ne pas ajouter de filtre ni changer le code de lampe pour masquer cet échec ; cela relèverait d'un autre essai après revue.

## 6. Parcours et mesures réelles

Réaliser au moins5circuits par variante, même parcours et mêmes phases : marche, sprint, glissade et les4obstacles. A contrôle les8arbres ; B1 impose les critères de protection seulement aux4pins équipés, B2/B3 aux4épicéas équipés. Les4autres restent des contrôles non équipés. Filmer les tentatives de traversée centrale et les passages tangents, avec identifiant de cible, horodatage, commande et mode. Les contacts intentionnels où le joueur pousse contre un tronc ne sont pas des blocages indésirables ; chronométrer le délai pour se dégager quand le joueur demande une trajectoire libre.

Relever : traversées complètes/partielles, durée des nouveaux blocages, régressions des4obstacles et de la glissade, distances/écarts visuels-physiques, caméra1repersonne contre l'écorce, collisions éventuelles des branches/neige et journal des erreurs. Capturer aussi les raycasts de lampe/interactions avec origines/directions et réponses A/B. Conserver les erreurs préexistantes au lieu de vider les logs pour obtenir zéro.

Performances : mêmes résolution/qualité, apps ouvertes, appareil, tracé, population et durée mesurée. Proposition d'acquisition à figer avant :30s d'échauffement puis au moins30s de capture par passage, mêmes fenêtres pour A/B. Exporter les échantillons horodatés. Stats.FrameTime est documenté en secondes côté client (×1000 pour ms), sous réserve de disponibilité sur la build. Pour la physique, préférer une piste MicroProfiler avec unité et périmètre explicites ; Stats.PhysicsStepTimeMs est documenté en ms mais déprécié, à utiliser seulement si disponible et étiqueté. Ne pas attribuer une unité à Stats.PhysicsStepTime sans la vérifier, ni convertir des FPS moyens en p95. Séparer client/serveur si les deux sont mesurés.

Convention d'analyse avant essai : pour chaque variante, mêmes fenêtres, médiane de tous les temps physiques et p95 des temps de frame (rang ceil(0,95×N) sur série triée), plus résultats par passage. Comparer à A, conserver A brut et appariement des circuits. Comparer la dispersion des répétitions A/A à0,2ms et0,5ms : si l'incertitude recouvre le seuil ou que la mesure est trop bruitée, **INDÉTERMINÉ**, pas PASS. Pas de significativité statistique revendiquée avec cinq circuits.

Sauvegarder B1/B2/B3 uniquement en fichiers locaux distincts, fermer/réouvrir la copie concernée puis refaire au moins un circuit complet et les contrôles d'objets/propriétés/hits. Vérifier les SHA256 des fichiers de référence et la permanence des réglages. Émulateur mobile Studio : mêmes vérifications avec profil et contrôles déclarés ; pas une preuve de performance sur téléphone réel. Pathfinding du futur PNJ : NON TESTÉ, essai séparé obligatoire avant V6.

## 7. Acceptation par variante

Budgets expérimentaux approuvés, pas limites officielles Roblox :

-0traversée de tronc équipé ;0nouveau blocage indésirable de plus de0,5s.
-0régression des obstacles et de la glissade ;0nouvelle erreur liée au changement.
-Surcoût médian physique STRICTEMENT<0,2ms et surcoût frame p95 STRICTEMENT<0,5ms ; INDÉTERMINÉ si bruit ou donnée absente.
-Caméra contre l'écorce vérifiée, aucune perturbation observée de lampe/interactions ; conditions et distances documentées.
-Réouverture et nouveau contrôle réussis sur la copie. Résultats mobile émulé distingués du PC.

SUCCESS uniquement si tous les critères applicables sont observés et soutenus ; FAILED si une régression ou un critère échoue ; PARTIAL_SUCCESS si mesures manquantes/indéterminées malgré certains contrôles réussis. Ces statuts sont des résultats rapportés, jamais VERIFIED/HUMAN_APPROVED. A est le témoin : sa traversée connue ne fait pas échouer l'instrumentation et reste dans les preuves.

## 8. Mémoire et récupération : trois enregistrements séparés

Lire `MCP_RESULTS.md`, les JSON de préparation et le modèle de retour. `prepare_experiment` ne lance pas Studio ; `start_experiment` marque RUNNING juste avant l'essai réel, avec la révision renvoyée ; `record_experiment_result` après les mesures. B1/B2/B3 ont trois UUID distincts. Réutiliser la même preuve A en la citant explicitement, sans la compter comme trois confirmations indépendantes.

Importer JSON/CSV/PNG dans lab/inbox puis via LabStore.import_artifact pour obtenir des IDs de reçus ; le MCP existant n'a pas d'outil d'import arbitraire. Ne pas mettre un chemin de fichier dans artifacts. Les .rbxl et vidéos brutes restent hors LabStore (format/taille non acceptés), avec SHA et chemins consignés dans un manifeste JSON importé. Pas de nouveau tool ni modification des garde-fous.

Après enregistrement, get_experiment puis get_experiment_context(problem="C2B H001 H002 collisions sapin", detailed=true, limit=10), retrouver les trois résultats et leurs erreurs/limites. Reposer la question initiale à L'Éponge, conserver les sorties AVANT/APRÈS et envoyer les preuves à la revue contradictoire ChatGPT. Le fait que la mémoire restitue un résultat ne valide pas la technique. Le prototype/source partagé ne sera pas promu automatiquement.

## Sources et limites

[S1] Roblox Creator Hub, BasePart.CanCollide/CanQuery/CanTouch/CollisionGroup : https://create.roblox.com/docs/reference/engine/classes/BasePart ; copie officielle avec Git blob et SHA256 dans handoff/proofs/.
[S2] Part.Shape : https://create.roblox.com/docs/reference/engine/classes/Part ; le montage/orientation proposé doit être contrôlé dans Studio.
[S3] CollisionFidelity : https://create.roblox.com/docs/reference/engine/enums/CollisionFidelity ; options approximatives, pas « polygon perfect ».
[S4] Unités : https://create.roblox.com/docs/physics/units ;1stud=28cm convention documentaire.
[S5] Stats : https://create.roblox.com/docs/reference/engine/classes/Stats ; vérifier disponibilité/build/unités des sondes.
[H001/H002] Messages de Claude validés par le propriétaire/ChatGPT selon les messages reçus le17-11 ; données Studio brutes et SHA de copie encore à joindre. Les sondes ne prouvent pas seules la géométrie visuelle.

Officiel consulté via Roblox/creator-docs, licence CC-BY4.0 ; provenance des fichiers figée par Git blob, pas promesse de compatibilité avec toute build. Anciennes affirmations DevForum « collision exacte » non retenues. Tous les coefficients/critères/durées proposés sont des paramètres d'expérience, non des valeurs optimales documentées. Rollback : fermer sans sauvegarder ou réouvrir A ; garder toutes les variantes/mesures comme preuves ; ne pas modifier la place principale.
