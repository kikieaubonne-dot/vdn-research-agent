param(
    [string]$ProjectRoot,
    [string]$Bundle,
    [string]$Python = "python",
    [int]$MaxItems = 1,
    [switch]$Acquire,
    [switch]$ApplySync
)
# Manual bounded run only. This script registers no scheduled task.
$ErrorActionPreference = "Stop"
if (-not $ProjectRoot -or -not $Bundle) { throw "ProjectRoot and Bundle are required." }
$ProjectRoot = (Resolve-Path -LiteralPath $ProjectRoot).Path
$env:PYTHONUTF8 = "1"
Push-Location -LiteralPath $ProjectRoot
try {
    $researchArgs = @("-m", "agent.v9", "--root", $ProjectRoot, "research", "--max-items", "$MaxItems")
    if ($Acquire) { $researchArgs += "--apply" }
    & $Python @researchArgs
    if ($LASTEXITCODE -ne 0) { throw "Research failed; sync was not started." }
    $syncArgs = @("-m", "agent.v9", "--root", $ProjectRoot, "sync", "--destination", $Bundle)
    if ($ApplySync) { $syncArgs += "--apply" }
    & $Python @syncArgs
    if ($LASTEXITCODE -ne 0) { throw "Sync conflict or failure; inspect the JSON report." }
} finally {
    Pop-Location
}
