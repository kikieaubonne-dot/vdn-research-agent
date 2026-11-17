-- Original PROPOSED lab builder. NOT EXECUTED in Roblox Studio.
-- Returns an UNPARENTED model. Caller must approve a COPIED scene before insertion.
-- No downloaded assets, player/controller edits, publication, audio or global lighting.
local StarterLab = {}
local function part(parent, name, size, position, color)
    local object = Instance.new("Part")
    object.Name = name
    object.Anchored = true
    object.Size = size
    object.Position = position
    object.Color = color
    object.Parent = parent
    return object
end
function StarterLab.build()
    assert(game:GetService("RunService"):IsStudio(), "Studio laboratory only")
    local root = Instance.new("Model")
    root.Name = "EpongePrologueLab_PROPOSED"
    root:SetAttribute("EpongeLab", true)
    root:SetAttribute("EndingApproved", false)
    local names = {"A_Maison", "B_Poursuite", "C_Confrontation", "D_Appel", "E_Enqueteur"}
    local labels = {"Maison : post-it et Maelle", "Suivre Maelle : Shift si necessaire", "Retrouve Maelle", "Signaler la disparition", "Enqueteur : indices"}
    local events = {
        {"POSTIT_READ", "MAELLE_LEAVES"}, {"MAELLE_LOST"},
        {"SILHOUETTE_ENCOUNTERED", "SAFE_PLACE_REACHED"}, {"REPORT_MADE"}, {"INVESTIGATION_INTRO_COMPLETE"}
    }
    for i, name in ipairs(names) do
        local zone = Instance.new("Model")
        zone.Name = name
        zone.Parent = root
        local x = (i-1)*48
        part(zone, "SolTemoin", Vector3.new(48, 1, 24), Vector3.new(x, 0, 0), Color3.fromRGB(220, 225, 230))
        local board = part(zone, "RepereScene", Vector3.new(12, 5, 1), Vector3.new(x, 4, -10), Color3.fromRGB(45, 50, 65))
        local surface = Instance.new("SurfaceGui")
        surface.Face = Enum.NormalId.Front
        surface.Parent = board
        local text = Instance.new("TextLabel")
        text.Size = UDim2.fromScale(1, 1)
        text.BackgroundTransparency = 1
        text.TextColor3 = Color3.fromRGB(255, 255, 255)
        text.TextScaled = true
        text.Text = labels[i]
        text.Parent = surface
        for j, event in ipairs(events[i]) do
            local marker = part(zone, event, Vector3.new(3, 3, 3), Vector3.new(x-8+j*5, 2, 3), Color3.fromRGB(70, 120, 160))
            marker:SetAttribute("ProgressionEvent", event)
            local prompt = Instance.new("ProximityPrompt")
            prompt.ActionText = "Essai narratif"
            prompt.ObjectText = event
            prompt.MaxActivationDistance = 8
            prompt.RequiresLineOfSight = true
            prompt.Parent = marker
        end
        if i==1 then
            part(zone, "Maelle_PROXY_NON_RIGGE", Vector3.new(2, 4, 2), Vector3.new(x+8, 2.5, 0), Color3.fromRGB(190, 80, 80))
        elseif i==3 then
            part(zone, "Menace_PROXY_NON_RIGGE", Vector3.new(3, 6, 2), Vector3.new(x+8, 3.5, 0), Color3.fromRGB(110, 25, 25))
        elseif i==5 then
            part(zone, "Enqueteur_PROXY_NON_RIGGE", Vector3.new(2, 5, 2), Vector3.new(x+8, 3, 0), Color3.fromRGB(25, 35, 65))
        end
    end
    assert(root.Parent == nil, "Builder must not modify Workspace")
    return root
end
return StarterLab
