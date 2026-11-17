# Windows — installation sans écrasement et retour arrière

Ce guide est préparé sous Linux ; aucune validation sur le PC utilisateur ni application Desktop/Studio.

Extraire l'archive dans un NOUVEAU dossier, par exemple `C:\Users\kikie\Documents\Eponge-V11-StartNow`. Ne pas superposer l'ancien Eponge-V11.2. Dans PowerShell, depuis le dossier contenant START_HERE.md :

```powershell
Get-Location
Test-Path .\Eponge\source\vdn_mcp.py
py -3.11 --version
py -3.11 .\WINDOWS\setup.py verify
py -3.11 .\WINDOWS\setup.py doctor
py -3.11 .\WINDOWS\setup.py test-mcp
py -3.11 .\WINDOWS\setup.py config-candidate
```

Attendus : chemin du nouveau dossier ; True ; Python3.11.x ; verify PASS et aucune source modifiée ; doctor PARTIAL avec chemins réels et autonomie désactivée ; test-mcp PASS/27outils/4lectures/refus d'écriture ; candidat avec l'exécutable Python Windows réel. Un cache dérivé SQLite reconstruit peut être explicitement signalé : cela ne permet pas une modification des sources ou compteurs. Une erreur d'intégrité bloque ; ne pas la contourner.

Le candidat ne touche pas Desktop. Localiser sa configuration effective dans l'application ; sauvegarder ce JSON dans un nouveau fichier avant toute fusion manuelle. Conserver les autres serveurs et permissions. Redémarrer Desktop et consulter la Bible/ressources, la preuve d'un geste puis `tree:forest/spruce/snow`. La seule validation stdio ne vaut pas validation UI.

La mémoire cumulative dans Eponge/runtime est consultable ; ses expériences/calculs sont fermés. Ne pas activer le worker, planificateur ou augmenter la politique60s depuis ce guide. Ne pas réinitialiser le compteur103,752s. L'ancien runtime V10 reste distinct à77,058s et V9 à59,596s.

Studio : nouvelle place ou copie approuvée seulement, relever son PlaceId et sa version, lire ROBLOX/README.md. Aucun asset original B3/C1 n'est requis pour le harnais proxy ; aucun de leurs réglages n'est inventé. Le harnais manuel ne crée pas un prologue complet. Un test rig/import/retargeting réel reste nécessaire avant usage en gameplay. Aucun déploiement ni publication.

Retour arrière : fermer les processus stdio de test ; restaurer uniquement la sauvegarde de configuration Desktop si elle a été modifiée ; retirer uniquement les objets et scripts possédés par le laboratoire dans la copie Studio. Conserver le dossier livré et ses journaux comme preuves. Ne pas recopier des anciens budgets sur les budgets récents, ni remplacer l'ancien projet. L'export OBSIDIAN_LAB est isolé ; ne pas le fusionner automatiquement dans un coffre personnel. Les transactions précédentes restent dans le runtime pour consultation, mais leurs anciens chemins cloud ne sont pas une autorisation de rollback sur le PC.
