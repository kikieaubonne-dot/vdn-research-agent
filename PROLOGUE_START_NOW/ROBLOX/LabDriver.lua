-- PROPOSED manual test harness, NOT executed in Studio.
-- NOT a production event source: pressing a prompt does not prove a story event.
-- Caller inserts approved model into a COPIED Studio place and calls bind explicitly.
local LabDriver = {}
function LabDriver.bind(root, Progression, approval)
    assert(game:GetService("RunService"):IsStudio(), "Studio laboratory only")
    assert(approval and approval.copied_scene == true and approval.expected_place_id == game.PlaceId, "Explicit copied-place approval and exact PlaceId required")
    assert(root and root:GetAttribute("EpongeLab") == true, "Explicit lab root required")
    local players = game:GetService("Players")
    assert(#players:GetPlayers() <= 1, "This preview is a single-player laboratory")
    local states = {}
    local connections = {}
    for _, object in ipairs(root:GetDescendants()) do
        if object:IsA("ProximityPrompt") then
            local marker = object.Parent
            local event = marker:GetAttribute("ProgressionEvent")
            if type(event) == "string" then
                table.insert(connections, object.Triggered:Connect(function(player)
                    if not marker:IsDescendantOf(root) then return end
                    if #players:GetPlayers() > 1 then return end
                    local character = player.Character
                    local pivot = character and character:FindFirstChild("HumanoidRootPart")
                    local humanoid = character and character:FindFirstChildOfClass("Humanoid")
                    if not pivot or not humanoid or humanoid.Health <= 0 then return end
                    if (pivot.Position-marker.Position).Magnitude > 10 then return end
                    local state = states[player.UserId] or Progression.new()
                    local eventId = tostring(player.UserId).."-"..tostring(state.sequence).."-"..event
                    local ok, nextState = pcall(Progression.advance, state, event, eventId)
                    if ok then
                        states[player.UserId] = nextState
                        root:SetAttribute("PreviewState", nextState.state)
                        root:SetAttribute("PreviewSequence", nextState.sequence)
                    else
                        root:SetAttribute("PreviewError", "Evenement hors ordre ou fin non approuvee")
                    end
                end))
            end
        end
    end
    return function()
        for _, connection in ipairs(connections) do connection:Disconnect() end
        states = {}
    end
end
return LabDriver
