# Essai manuel de laboratoire — NON EXÉCUTÉ dans Studio

1. Dans une copie de place explicitement identifiée, créer les trois ModuleScripts proposés dans ServerStorage/EpongePrologueLabModules_PROPOSED. Copier les trois fichiers Luau correspondants.
2. Créer un Script temporaire de test dans cette copie, avec le code ci-dessous. Renseigner le PlaceId réellement observé et approuver la copie. **Ne pas employer ce script dans la place principale ou publiée.**

```lua
local modules = game:GetService("ServerStorage"):WaitForChild("EpongePrologueLabModules_PROPOSED")
local Progression = require(modules:WaitForChild("Progression"))
local Builder = require(modules:WaitForChild("StarterLab"))
local Driver = require(modules:WaitForChild("LabDriver"))
local approval = {
    copied_scene = false, -- mettre true seulement après vérification de la copie
    expected_place_id = -1, -- remplacer par le PlaceId réel de cette copie
}
assert(approval.copied_scene and approval.expected_place_id == game.PlaceId, "Copie non approuvee")
local root = Builder.build()
assert(root.Parent == nil)
root.Parent = workspace -- seul geste d'insertion explicite, sur la copie
local disconnect = Driver.bind(root, Progression, approval)
script.Destroying:Connect(function()
    disconnect()
    root:Destroy() -- uniquement le modèle généré possédé par cet essai
end)
```

3. Play sur la copie. Le spawn/contrôleur n'est pas modifié par le builder ; placer manuellement un SpawnLocation de laboratoire si nécessaire. Aller vers les marqueurs dans l'ordre POSTIT_READ → MAELLE_LEAVES → MAELLE_LOST → SILHOUETTE_ENCOUNTERED → SAFE_PLACE_REACHED → REPORT_MADE → INVESTIGATION_INTRO_COMPLETE. Lire PreviewState et PreviewSequence sur le modèle.
4. Vérifier les événements hors ordre, absence de transition F et arrêt propre. Le modèle atteint ending-decision-required ; aucun choix de fin ni avatar d'enquêteur n'est créé automatiquement.
5. Conserver logs/captures et build. Stop, retirer uniquement le Script temporaire et le modèle généré ; comparer au témoin. Les modules peuvent être archivés comme candidats.

Ce test n'a pas été exécuté ici. Il faut ensuite remplacer les marqueurs par une vraie Maëlle, des observations de disparition, une menace, une fuite et une transition de rôle. Le succès du harnais ne suffit pas à valider le prologue.
