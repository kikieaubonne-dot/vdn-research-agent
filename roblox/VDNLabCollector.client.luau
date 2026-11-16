-- V10 candidate collector. Install ONLY in StarterPlayerScripts of VDN — Laboratoire.
-- Not executed in Studio during V10 delivery. No network, publishing or asset edits.
local RunService = game:GetService("RunService")
local HttpService = game:GetService("HttpService")
local Workspace = game:GetService("Workspace")

if not RunService:IsStudio() or Workspace:GetAttribute("VDNLab") ~= true then
    warn("VDN collector refused: Studio and Workspace.VDNLab=true required")
    return
end

-- Fill from the Python experiment design. Never point at the production place.
local EXPERIMENT_ID = "REPLACE_WITH_EXPERIMENT_UUID"
local METHOD = "A"
local MODEL_NAME = "VDNTest_A"
local ENVIRONMENT = { studio_version = "FILL_MANUALLY", device = "FILL_MANUALLY" }
local CONTROLS = {
    studio_version = "FILL_MANUALLY", device = "FILL_MANUALLY",
    graphics_quality = "FILL_MANUALLY", resolution = "FILL_MANUALLY",
    camera = "FILL_MANUALLY", lighting = "FILL_MANUALLY", tree_count = 1,
    warmup_s = 5, sample_s = 10,
}
if not string.match(EXPERIMENT_ID, "^%x%x%x%x%x%x%x%x%-%x%x%x%x%-%x%x%x%x%-%x%x%x%x%-%x%x%x%x%x%x%x%x%x%x%x%x$") then
    warn("VDN collector refused: fill experiment UUID")
    return
end
local target = Workspace:FindFirstChild(MODEL_NAME)
if not target or not target:IsA("Model") then
    warn("VDN collector refused: isolated test Model missing")
    return
end
-- Keep traversal and sampling bounded. The model must stay unchanged during sampling.
local descendants = target:GetDescendants()
if #descendants > 10000 then
    warn("VDN collector refused: model exceeds 10000 descendants")
    return
end
local materials, textures = {}, {}
for _, instance in ipairs(descendants) do
    if instance:IsA("BasePart") then
        materials[tostring(instance.Material) .. ":" .. instance.MaterialVariant] = true
    end
    if instance:IsA("MeshPart") and instance.TextureID ~= "" then
        textures[instance.TextureID] = true
    end
    if instance:IsA("SurfaceAppearance") then
        for _, id in ipairs({instance.ColorMap, instance.NormalMap, instance.RoughnessMap, instance.MetalnessMap}) do
            if id ~= "" then textures[id] = true end
        end
    end
end
local function count(set)
    local n = 0
    for _ in pairs(set) do n += 1 end
    return n
end
task.wait(CONTROLS.warmup_s)
local elapsed, samples = 0, 0
while elapsed < CONTROLS.sample_s and samples < 10000 do
    local delta = RunService.Heartbeat:Wait()
    elapsed += delta
    samples += 1
end
-- Heartbeat intervals are reported as observations, never mislabeled rendered FPS.
-- GPU frame time, triangles, asset bytes, night quality and artifacts need other tools.
local report = {
    schema = "vdn.roblox-measurement/10", experiment_id = EXPERIMENT_ID, method = METHOD,
    metrics = { materials = count(materials), textures = count(textures) },
    observations = {
        "Client Heartbeat mean interval ms (NOT rendered FPS): " .. tostring(elapsed * 1000 / math.max(1, samples)),
        "Samples: " .. tostring(samples) .. "; elapsed seconds: " .. tostring(elapsed),
        "Material/property and texture-ID counts only; not draw calls, texture memory, complete decal inventory or GPU cost.",
    },
    errors = {}, controls = CONTROLS, environment = ENVIRONMENT,
}
print("VDN_MEASUREMENT_BEGIN")
print(HttpService:JSONEncode(report))
print("VDN_MEASUREMENT_END")
