param(
    [int]$Port = 8000
)

$root = Split-Path -Parent $MyInvocation.MyCommand.Definition
$venv = Join-Path $root "pizzaria_api_pkg\.venv\Scripts\python.exe"
$wd = Join-Path $root "pizzaria_api_pkg"
$args = "-m uvicorn pizzaria_api_pkg.main:app --host 0.0.0.0 --port $Port --reload"

Write-Host "Starting backend using: $venv"
Write-Host "Working directory: $wd"

# Start the process so it runs independently
Start-Process -FilePath $venv -ArgumentList $args -WorkingDirectory $wd
Write-Host "Backend start requested (check processes or logs)."
