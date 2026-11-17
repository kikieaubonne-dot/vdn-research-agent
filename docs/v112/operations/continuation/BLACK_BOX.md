# BLACK BOX — risques non clos

Les limites ci-dessous sont un audit opérateur, distinct des crashs. Le journal généré conserve en plus l’échec réel du débruiteur. Celui-ci reste BLOCKED pour revue, même si une variante corrigée a réussi. Aucun historique ni incident n’est effacé.

| Composant | Gravité / état | Cause ou frontière observée | Action recommandée |
|---|---|---|---|
| windows | HIGH / BLOCKED | Le seul shell disponible est Linux/Python3.12.14 ; aucun transport vers le PC Windows autorisé. | Ouvrir le dossier autorisé dans Codex local Windows, puis laisser Codex exécuter le préflight. |
| desktop | MEDIUM / BLOCKED | MCP stdio testé ; application Claude Desktop non accessible dans cette session. | Tester la découverte puis une consultation en lecture seule dans Desktop local. |
| studio | HIGH / BLOCKED | Aucune copie réelle B3/C1 ni pont Studio autorisé accessibles ici. | Fournir une copie identifiée dans le laboratoire local et vérifier le transport avant tout essai. |
| failover | MEDIUM / OPEN | Restauration explicite d’une image testée vers une copie désactivée validée ; bascule vivante automatique non implémentée. | Conserver les promotions désactivées ; approuver séparément le périmètre d’un éventuel canary/failover. |
| supervisor | MEDIUM / OPEN | La perte du superviseur arrête le worker via un compagnon transitoire ; panne OS/Python/compagnon sans service externe non couverte. | Reprendre explicitement depuis checkpoint après diagnostic ; aucun service système n’a été autorisé/installé. |
| resources | MEDIUM / OPEN | Les nouveaux superviseurs sont sérialisés ; suspension automatique sous charge CPU/GPU utilisateur et agrégation des ledgers séquentiels incomplètes. | Garder le mode nuit/concurrence non activé ; mesurer les ressources locales avant toute extension. |
| validator | MEDIUM / BLOCKED | Un utilisateur OS unique peut lire tous les jeux de tests ; aucune isolation aveugle du générateur n’est démontrée. | Validation indépendante externe et jeu réellement séparé avant toute promotion automatique. |
| evidence | MEDIUM / OPEN | Protection des légendes Markdown conservée ; légendes non balisées et entailment sémantique non résolus. | Revue des passages complets, moteur et versions ; ne pas confondre citation et vérité technique. |
| artistic | MEDIUM / BLOCKED | Critère géométrique PASS, mais quatre captures de prototypes simples ne démontrent pas un réalisme amélioré. | Comparer les images et définir les critères humains avant de conclure sur le rendu ou B3/C1. |
| ollama | LOW / NOT_TESTED | Ancienne sonde indisponible ; aucun modèle ni embedding réel exécuté ou téléchargé dans cette reprise. | Continuer déterministe ; tester seulement un modèle installé explicitement choisi lorsque l’environnement l’autorise. |
| provenance | MEDIUM / OPEN | Dates et hashes conservés ; licence des sources et build Studio du jeu UNKNOWN. | Vérifier droits et versions avant réutilisation d’assets ou recommandation validée. |
| research | LOW / OPEN | Le premier harnais conserve seulement FetchError sur deux réponses200 non capturées. Les erreurs502 Camera sont tracées ; aucun contournement. | Conserver la cause précise comme inconnue ; les reprises futures journalisent le message expurgé, sans nouvelle collecte dans cette enveloppe épuisée. |

Deux lieux de secours sur le même disque ne garantissent pas la persistance en cas de panne physique totale. Le dernier recours est stderr minimal, avec DIAGNOSTIC_UNAVAILABLE explicite. Les checksums ne constituent pas une barrière contre un propriétaire OS malveillant.
