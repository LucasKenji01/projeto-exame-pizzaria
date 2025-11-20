param(
    [int]$Port = 8000
)

Write-Host "Stopping processes on port $Port..."
$conns = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
if ($conns) {
    foreach ($c in $conns) {
        $procId = $c.OwningProcess
        Write-Host "Stopping PID $procId"
        try {
            Stop-Process -Id $procId -Force -ErrorAction Stop
            Write-Host "Stopped $procId"
        } catch {
            Write-Host ("Failed to stop {0}" -f $procId)
            Write-Host $_
        }
    }
} else {
    Write-Host "No connections found on port $Port"
}

Write-Host "Final check:"
Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue | Format-Table LocalAddress,LocalPort,State,OwningProcess -AutoSize
