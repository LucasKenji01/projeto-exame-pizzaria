param(
    [int]$Port = 8001,
    [string]$LogFile = "$PSScriptRoot\\uvicorn.log"
)

$root = Split-Path -Parent $MyInvocation.MyCommand.Definition
$venv = Join-Path $root "pizzaria_api_pkg\\.venv\\Scripts\\python.exe"
$wd = Join-Path $root "pizzaria_api_pkg"
$args = "-m uvicorn pizzaria_api_pkg.main:app --host 0.0.0.0 --port $Port --reload"

Write-Host "Starting backend (logs -> $LogFile)"
if (Test-Path $LogFile) { Remove-Item $LogFile -Force }

$p = Start-Process -FilePath $venv -ArgumentList $args -WorkingDirectory $wd -RedirectStandardOutput $LogFile -RedirectStandardError $LogFile -PassThru
Start-Sleep -Seconds 2
Write-Host ("Started PID: {0}" -f $p.Id)
Write-Host "--- Last 30 lines of log ---"
if (Test-Path $LogFile) { Get-Content $LogFile -Tail 30 } else { Write-Host "Log file not found yet." }
Write-Host "You can follow logs with: Get-Content -Path $LogFile -Wait"
