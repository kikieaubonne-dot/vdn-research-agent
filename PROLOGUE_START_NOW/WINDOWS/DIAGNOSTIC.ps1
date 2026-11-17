$ErrorActionPreference = 'Stop'
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONDONTWRITEBYTECODE = '1'
Get-Location
Get-Command py.exe -ErrorAction Stop | Select-Object Source
& py.exe -3.11 (Join-Path $PSScriptRoot 'setup.py') doctor
exit $LASTEXITCODE
