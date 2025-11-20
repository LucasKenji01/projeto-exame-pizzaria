param([int]$Port = 8001)

$root = Split-Path -Parent $MyInvocation.MyCommand.Definition
$venv = Join-Path $root "pizzaria_api_pkg\.venv\Scripts\python.exe"
$wd = Join-Path $root "pizzaria_api_pkg"
$args = "-m uvicorn pizzaria_api_pkg.main:app --host 0.0.0.0 --port $Port --reload"

Write-Host "Starting: $venv $args"
$p = Start-Process -FilePath $venv -ArgumentList $args -WorkingDirectory $wd -PassThru
Start-Sleep -Seconds 1
Write-Host ("Started PID: {0}" -f $p.Id)
Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue | Format-Table LocalAddress,LocalPort,State,OwningProcess -AutoSize
