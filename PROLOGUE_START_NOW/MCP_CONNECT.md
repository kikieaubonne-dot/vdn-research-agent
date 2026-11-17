# L'Éponge → Claude Desktop

Le dossier Eponge/source contient la continuation testée de17937ba (SHA exact dans DELIVERY_SUMMARY.json) ; Eponge/runtime contient la mémoire, preuves et vrais compteurs préservés. Aucun téléchargement ou service n'est nécessaire pour le serveur stdio.

Sur Windows, avec Python3.11 existant :

```powershell
py -3.11 WINDOWS/setup.py verify
py -3.11 WINDOWS/setup.py doctor
py -3.11 WINDOWS/setup.py test-mcp
py -3.11 WINDOWS/setup.py config-candidate
```

Le dernier résultat est un fragment avec le chemin Python Windows réellement mesuré. Sauvegarder le JSON Desktop actuel, vérifier les collisions de nom, puis fusionner seulement le serveur eponge_prologue. Aucun outil du paquet ne modifie ce fichier personnel. Ne pas remplacer les autres mcpServers. Si une politique Windows bloque un script, ne pas la contourner : utiliser le diagnostic Python ou demander l'autorisation appropriée.

Redémarrer Desktop et vérifier les27 outils. Faire une consultation prologue:resources, puis une clé learning:animation du dossier PROOFS. Demander le détail seulement lorsque nécessaire. Une réponse stdio valide ne prouve pas l'UI Desktop ou Studio. Les tailles de réponses ne sont pas des tokens Claude mesurés.

Erreurs : Python absent → installer uniquement après accord ; fichiers absents/hash incorrect → vérifier extraction, ne pas désactiver le contrôle ; serveur non visible → lire erreur de démarrage et chemins absolus ; outil non autorisé → conserver le refus, pas d'élargissement silencieux de permission.

Rollback Desktop : restaurer sa copie JSON et redémarrer l'application. Aucun service permanent ou planificateur n'est ajouté ; fermer un terminal de test arrête son processus stdio.
