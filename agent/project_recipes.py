"""Actionable laboratory proposals. Names are proposed components, not existing files."""

RECIPES={
'animation':('AnimationRoundTripHarness','validation d’un mouvement et de son import sur un rig témoin',[
 ('rig de laboratoire et pose de repos','Consigner hiérarchie, unités, os et pose de référence ; le personnage de bêta reste à confirmer.','Rig et pose de référence inspectables.'),
 ('animation courte sur une copie','Exporter une copie avec options documentées ; comparer pose de repos, mouvement et déformations après import.','Différences localisées entre rig, animation et import.'),
 ('mêmes rig, version et séquence','Tester lecture, interruption et retour à la pose sûre ; garder les exports et les captures d’échec.','Aucun gain ou compatibilité attribué à Sonia sans mesure sur son asset.')],['animation témoin','un réglage d’export documenté modifié']),
'trees':('TreeVariantsLab','comparaison silhouette/géométrie et feuillage',[
 ('copies B3/C1 et vues de référence','Aligner les copies sur la même échelle ; capturer silhouette proche et lointaine.','Silhouettes annotées et dimensions consignées.'),
 ('copies de même silhouette','Modifier un seul facteur : géométrie ou représentation du feuillage ; conserver matériaux, caméra et lumière.','Variantes A/B différant seulement par le facteur choisi.'),
 ('parcours et captures identiques','Comparer répétition, contours, ombres et coût mesuré ; conserver les défauts signalés par un humain.','Revue visuelle et mesures jointes, sans gagnant présumé.')],['géométrie','cartes de feuillage']),
'collisions':('TreeCollisionHarness','comparaison du collider actuel et d’une variante simplifiée',[
 ('copie de l’arbre et contrôleur réel','Inventorier séparément troncs, branches, géométrie visible et volumes physiques ; relever uniquement les propriétés sourcées.','État témoin enregistré pour restauration.'),
 ('trajet marqué entre arbres, sous branches et sur pente','Exécuter le trajet témoin et journaliser chaque blocage avec position, action et composant touché.','Liste reproductible des blocages.'),
 ('copie A témoin et copie B','Changer uniquement la représentation physique autorisée par les sources ; rejouer le même contrôleur et parcours.','Comparaison des blocages et du coût physique ; rollback si régression.')],['collider du mesh','volumes physiques séparés, à valider']),
'ground':('SnowGroundHarness','comparaison de deux représentations de sol et d’empreintes',[
 ('zone témoin avec pente et repères','Consigner relief, matériau et trajectoire ; capturer les contacts du joueur avant toute empreinte.','Baseline de déplacement et de raccords.'),
 ('représentation terrain ou mesh autorisée','Ajouter la représentation d’empreintes candidate dans une copie ; conserver un sol témoin.','Effet isolé, durée et nettoyage observables.'),
 ('mêmes pas, pente et éclairage','Rejouer arrêts, virages et passages répétés ; relever flottement, intersections, persistance et coût.','Défauts annotés et mesures, sans durée optimale inventée.')],['terrain','surface mesh et effet d’empreinte documenté']),
'lighting':('FlashlightNightHarness','isolation du faisceau et de l’ambiance nocturne',[
 ('lampe V2 et scène témoin','Consigner propriétés réellement disponibles et valeurs actuelles ; fixer caméra, exposition et appareil.','Baseline restaurable et versions enregistrées.'),
 ('copies A/B, mêmes arbres et sol','Changer un seul facteur documenté de lumière, ombre ou brouillard ; conserver le reste.','Cause isolée des différences de lisibilité.'),
 ('même trajet et mêmes positions','Capturer bord du faisceau, contact avec le sol, branches et silhouettes ; joindre coût de trame et avis humain.','Compromis visibilité/ambiance mesuré, aucune portée optimale présumée.')],['lumière témoin','variante d’ombre ou d’atmosphère documentée']),
'camera':('FirstPersonCameraHarness','séparation du suivi, du mouvement et de l’obstruction',[
 ('caméra et avatar copiés','Consigner état caméra et contrôleur ; désactiver les effets candidats dans la copie témoin, pas dans le jeu principal.','Reproduction du problème avec contrôles connus.'),
 ('module logique de suivi et journal de trajectoire','Séparer cible de suivi, contribution du mouvement et gestion d’obstruction ; tracer chaque contribution sans valeur de lissage inventée.','Origine de clipping ou mouvement parasite identifiée.'),
 ('trajet près des murs, branches et pentes','Comparer arrêt, virage, sprint et accroupissement ; vérifier retour de contrôle et confort humain.','Aucune traversée de décor et aucun état caméra bloqué dans le scénario de test.')],['suivi témoin','effet de mouvement candidat isolé']),
'movement':('MovementStateHarness','machine d’états explicite et validation des transitions',[
 ('schéma de contrôles et avatar à confirmer','Écrire une table état/entrée/condition de sortie pour marche, sprint, accroupissement, glissade et enjambement ; marquer les actions non validées.','Transitions et exclusions inspectables avant programmation.'),
 ('détecteur d’obstacles et contrôleur dans la copie','Séparer détection, autorisation de transition et mouvement ; journaliser les refus au lieu de forcer un franchissement.','Reproduction des collisions et transitions impossibles.'),
 ('parcours témoin avec obstacles','Tester interruption, changement de direction, plafond bas et perte de contrôle ; consigner chaque retour à l’état sûr.','Aucun état coincé ; comportement validé seulement sur les contrôles testés.')],['locomotion témoin','actions avancées activées séparément']),
'interactions':('InteractionDoorHarness','contrat d’interaction avec validation de l’état',[
 ('porte et cachette témoins, mode réseau à confirmer','Définir action, portée autorisée, préconditions et état avant/après ; les valeurs restent à choisir à partir des sources et tests.','Contrat d’interaction et erreurs explicites.'),
 ('composants logique de demande et d’autorisation','Séparer présentation, requête et décision ; rejeter les demandes répétées ou incompatibles avec l’état courant.','Aucun double déclenchement ni changement d’état impossible.'),
 ('même scénario d’ouverture et de sortie','Tester annulation, obstacle, entrée déjà occupée et reconnexion si le mode retenu le requiert.','Résultats et limites réseau consignés avant réutilisation.')],['interaction minimale','variante de cachette conditionnée au scénario']),
'performance':('ForestProfileHarness','baseline par appareil et modification d’un facteur',[
 ('scène témoin et appareils confirmés','Consigner géométrie, matériaux, instances, résolution et trajet ; les objectifs de FPS restent inconnus tant que non validés.','Rapport de baseline avec conditions.'),
 ('même caméra et même trajet','Mesurer les segments coûteux avec les outils officiellement documentés ; séparer rendu, physique et logique.','Coût attribué à un segment et non à un FPS supposé.'),
 ('variante ne changeant qu’un facteur','Comparer densité, géométrie ou gestion de distance séparément ; garder les mesures brutes et les défauts visuels.','Décision conditionnelle par appareil, pas de gain général inventé.')],['baseline','une optimisation documentée à la fois']),
'architecture':('HouseBlockoutHarness','blockout conditionné à la séquence jouable',[
 ('objectif bêta et plan provisoire','Marquer entrée, sortie, visibilité et espaces nécessaires à la séquence ; laisser les choix narratifs non confirmés visibles.','Plan de circulation et inconnues explicites.'),
 ('copies de volumes simples','Parcourir le blockout avec le contrôleur témoin avant détails ; mesurer encombrement et blocages.','Circulation et lignes de vue annotées.'),
 ('mêmes portes, lampe et objectifs','Comparer variantes de parcours ; ne figer une pièce scénarisée qu’après décision humaine.','Blockout réversible avec décision et alternatives consignées.')],['blockout minimal','détails artistiques différés']),
'pursuit':('PursuitDetectionHarness','séparation détection, décision et déplacement',[
 ('NPC générique et mode réseau confirmé','Définir observations visibles, états de détection et sorties ; ne pas attribuer le rôle au Père Noël sans décision.','Table de transitions et conditions de perte de cible.'),
 ('module de détection et module de trajet distincts','Journaliser observation, décision et demande de déplacement ; tester les obstacles sans supposer une visibilité traversante.','Erreur localisée entre détection et navigation.'),
 ('même trajet joueur et obstacles','Comparer apparition, perte de vue, chemin indisponible et cible immobile ; conserver les échecs et conditions.','Poursuite bornée et sortie d’état sûre, sans résultat inventé.')],['détection témoin','navigation candidate sourcée']),
'export':('ExportRoundTripHarness','comparaison avant/après export',[
 ('copies Blender 5.2','Consigner unités, transformations, normales et options réellement utilisées sans modifier les originaux.','Rapport des paramètres choisis et des versions.'),
 ('export séparé et copie du laboratoire Roblox','Importer la copie et comparer dimensions, orientation, matériaux et pose à la référence.','Différences attribuées à l’étape du pipeline.'),
 ('mêmes assets B3/C1','Rejouer l’export avec une seule option modifiée ; garder l’export précédent pour rollback.','Compatibilité limitée aux assets et versions réellement testés.')],['export témoin','une option d’export modifiée']),
'materials':('MaterialNormalHarness','comparaison des cartes réellement fournies',[
 ('textures et UV disponibles','Inventorier les cartes, leurs sources et les éléments manquants ; ne pas fabriquer une carte absente.','Liste d’entrées complète ou lacunes explicites.'),
 ('même arbre et lumière témoin','Comparer matériau témoin et cartes candidates en isolant couleur, normales ou transparence.','Cause des coutures ou contours isolée.'),
 ('mêmes vues proches et lointaines','Examiner raccords, orientation des normales, ombres et coût ; ne pas transposer un shader Unreal.','Avis humain et limites moteur liés aux sources.')],['matériau témoin','cartes candidates documentées'])}


RECIPES.update({
'viewmodel':('FirstPersonHandsLab','séparer vue, animation et logique de lampe',[
 ('copies caméra, contrôleur et mains disponibles','Relever rig, hiérarchie, animations et contraintes réelles sans inventer de fichier existant.','Baseline caméra/mains sauvegardée.'),
 ('mannequin et lampe de laboratoire','Isoler une liaison de caméra ou une animation à la fois ; garder le contrôleur témoin.','Origine du décalage ou clipping observable.'),
 ('même trajet et mêmes actions','Comparer marche, sprint, accroupissement et interaction ; conserver les défauts et le rollback.','Résultats limités au rig et contrôleur réellement testés.')],['mains témoins','variante de liaison ou animation isolée']),
'audio':('NarrativeAudioLab','déclenchement contextuel et lisibilité des indices sonores',[
 ('sons autorisés et copie de scène','Vérifier droits, provenance et déclencheurs ; les sons non disponibles restent des lacunes.','Inventaire sans audio fabriqué ni licence supposée.'),
 ('même caméra et même parcours','Comparer un signal spatial ou narratif à la fois ; conserver les autres sons.','Cause des différences de localisation ou compréhension isolée.'),
 ('mêmes actions et écoute humaine','Noter orientation perçue, compréhension, répétitions et défauts ; conserver les conditions.','Avis humain et événements enregistrés, sans mesure acoustique inventée.')],['signal témoin','indice sonore candidat']),
'guidance':('ContextualObjectivesLab','objectif progressif et indice au moment utile',[
 ('séquence utilisateur et joueurs témoins','Décrire objectif courant, zone accessible et condition de déblocage ; distinguer hypothèse de confusion et observation.','Table des états de progression inspectable.'),
 ('copie avec mêmes interactions','Comparer un indice contextuel ou une ouverture de zone à la fois, sans retirer le contrôle du joueur arbitrairement.','Effet attribuable à une seule modification UX.'),
 ('parcours observé avec consentement','Noter demandes d’aide, hésitations et réussite ; ne pas inventer taux d’abandon ni temps de résolution.','Décision humaine sur compréhension et accessibilité.')],['guidage témoin','indice progressif candidat']),
'saves':('ChapterSaveLab','persistance versionnée avec cas d’erreur',[
 ('données de test et schéma de progression','Définir clés logiques, version et droits ; aucune donnée joueur de production dans le laboratoire.','Schéma et règles de déverrouillage explicites.'),
 ('adaptateur de stockage de test','Préparer succès, erreur et reprise avec API officiellement documentée ; ne pas masquer un échec de sauvegarde.','Statuts et opérations inspectables sans perte silencieuse.'),
 ('mêmes scénarios de progression','Tester relecture, nouvelle tentative et migration sur copies ; conserver les anciennes données.','Résultats bornés au stockage et versions testés.')],['stockage témoin','version de schéma candidate']),
'groups':('LobbyPartyLab','séparer groupe, invitation et transition de scène',[
 ('règles utilisateur de groupes 1 à 4','Définir états d’invitation et départ ; ce nombre est une règle du projet, pas une limite de plateforme.','Contrat de groupe et inconnues réseau visibles.'),
 ('place de test et comptes autorisés','Préparer une transition à la fois avec validation serveur ; aucune téléportation du jeu publié.','Erreurs et autorisations liées à une scène isolée.'),
 ('mêmes règles et conditions réseau','Tester départ, refus, déconnexion et reprise ; ne pas annoncer un test multijoueur sans sessions réelles.','Rapports conditionnels, aucune réussite réseau fictive.')],['groupe minimal','transition candidate']),
'puzzles':('ProgressivePuzzleLab','indices et verrous avec transitions explicites',[
 ('plan de grenier proposé et objets copiés','Définir indice, condition de découverte et effet ; ne pas confirmer une énigme narrative non décidée.','Graphe de progression proposé et inspectable.'),
 ('même scène et mêmes interactions','Changer un seul verrou ou indice contextuel ; éviter tous les indices simultanés.','Différence de compréhension isolée.'),
 ('parcours reproductible et revue humaine','Tester ordre inattendu, interaction répétée et retour arrière ; consigner les impasses.','Aucune résolution ou compréhension présumée sans essai.')],['énigme témoin','déblocage progressif candidat']),
'dust':('MoonlightDustLab','isoler poussière et faisceau lumineux',[
 ('scène témoin et version Studio','Inventorier lumière et effet particulaire réellement disponibles ; ne pas transposer une volumétrie Unreal.','Paramètres actuels et source compatibles à vérifier.'),
 ('même caméra, exposition et géométrie','Comparer présence et représentation de poussière en changeant un facteur documenté.','Effet visuel isolé sans densité optimale inventée.'),
 ('mêmes vues et appareil cible','Recueillir avis humain et mesure de trame si disponible ; distinguer rendu perceptuel et coût.','Compromis borné aux conditions testées.')],['lumière sans poussière','particules candidates documentées'])})


def recipe(task):
    component,solution,steps,alternatives=RECIPES[task['id']]
    return {'status':'ENGINEERING_PROPOSAL','solution':solution,'component':{'name':component,'location':'emplacement à confirmer dans le projet','exists':'UNKNOWN'},
        'steps':[{'component':component,'input':i,'action':a,'expected_observation':o} for i,a,o in steps],
        'alternatives':[{'method':a,'decision':'à comparer, pas de gagnant présumé'} for a in alternatives],
        'test':{'controls':['mêmes assets, versions, appareil, caméra et trajet hors variable étudiée'],
                'changed_variable':'un seul facteur identifié avant exécution','measures':['observations brutes et coût mesuré','captures si disponibles'],
                'success_criteria':['critères et seuils à valider avant exécution','aucune régression du comportement témoin'],
                'executed':False},
        'risks':['compatibilité moteur et versions non présumée','coût de rendu/physique à mesurer sur appareil cible'],
        'rollback':'Restaurer les copies et paramètres témoins ; conserver les preuves et ne pas modifier le jeu publié.'}
