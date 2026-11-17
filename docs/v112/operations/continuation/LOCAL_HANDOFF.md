# Reprise Windows et rollback

**Une action humaine indispensable : ouvrir `C:\Users\kikie\Documents\Eponge-V11.2` dans une session Codex locale Windows, avec le paquet de livraison.** Cette session cloud n’a pas accès au dossier Windows. Ne pas remplacer ce diagnostic par une chaîne de commandes PowerShell à recopier.

Le Codex local doit lire CODEX_HANDOFF et le manifeste, inspecter HEAD/diff/worktrees, préserver configurations, notes, sessions, budgets et fichiers non suivis. Les patchs n’incluent aucune file runtime. Vérifier leur base avant application ; une branche locale différente se traite sans reset. Les images Linux et les anciennes CI ne dispensent pas des tests locaux Windows/Python3.11.

Lanceur existant : `Eponge.cmd` / `eponge.py`. `.cmd` est maintenant épinglé et emballé dans l’image, mais son exécution Windows reste NON TESTÉE. Ne pas installer service, tâche récurrente, modèle, API payante ou réglage système. Le bilan11 h est une tâche ponctuelle cloud, pas un démarrage du PC.

Avant activation locale : vérifier Python réellement utilisé, UTF-8, droits des chemins choisis, disque libre, modèles éventuellement installés, serveur MCP stdio27 puis interface Desktop en lecture seule. Sauvegarder toute configuration Desktop avant une modification explicitement autorisée. Obsidian : destination de laboratoire choisie, jamais le coffre personnel par défaut. Studio : pont autorisé et copies identifiées B3/C1 nécessaires ; aucun accès ni publication au jeu principal.

## Commandes existantes, exécutées ou préparées

Entrée actuelle de diagnostic : `python eponge.py --workspace <laboratoire> doctor` (JSON,0 réservé prêt,1 dégradé,2 bloqué). Le chemin doit désigner un laboratoire existant explicitement préparé. Ne pas réinitialiser une copie pour contourner un compteur ou un conflit de date.

Essai facultatif de végétation générée : `python -m agent.forest_lab --root <runtime-laboratoire> --allow-blender`. Le programme utilise la version installée, un script local fixe, les budgets existants et des fichiers générés dans lab/inbox/forest. Exécuté ici sur Blender4.3.2 seulement. Le budget épuisé interdit le recalcul ; ne pas augmenter les quotas. Les variantes enregistrées dans cette livraison peuvent être inspectées directement sans nouveau run.

Images : `python scripts/eponge_recovery.py --help`. `seal` exige source, manifeste indépendant, résultat/log PASS, destination nouvelle et `--approve-image`. `recover` exige workspace, image, son SHA256 approuvé, destination nouvelle et `--apply`. Les deux fonctions ont été exercées ; la restauration reste **désactivée** jusqu’à diagnostic et démarrage explicitement autorisés. Les images d’essais antérieures ne doivent pas être substituées à celle du manifeste final.

## Rollback

Aucune migration destructive. La branche de départ et les snapshots restent conservés. Un rollback de code s’effectue dans une nouvelle copie depuis une image validée et approuvée, jamais par écrasement du dépôt sale. Runtime/quotas/checkpoint sont copiés et vérifiés, pas remis à zéro. Si les données protégées sont corrompues, le changement d’exécutable est refusé : conserver la preuve et diagnostiquer les données.

Obsidian : rollback uniquement de la dernière transaction générée et non modifiée ; les conflits doivent être conservés, jamais écrasés. L’essai livré a réellement conservé123 fichiers knowledge et archivé la note de probe ajoutée. B3/C1 : restaurer uniquement le témoin du laboratoire ; aucun asset réel n’a été modifié ici.

Les preuves et fichiers sources privés ne sont pas publiés. La distribution comporte les patchs, scènes procédurales et rapports nécessaires ; elle ne recopie pas les caches Web complets ni les configurations personnelles.
