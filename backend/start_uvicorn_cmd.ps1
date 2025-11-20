param(
    [int]$Port = 8000
)

$venv = 'D:\\Lucas\\FACULDADE EXAME\\3º Semestre\\Projeto Integrador\\projeto\\backend\\pizzaria_api_pkg\\.venv\\Scripts\\python.exe'
$wd = 'D:\\Lucas\\FACULDADE EXAME\\3º Semestre\\Projeto Integrador\\projeto\\backend\\pizzaria_api_pkg'
$log = 'D:\\Lucas\\FACULDADE EXAME\\3º Semestre\\Projeto Integrador\\projeto\\backend\\uvicorn.log'

$cmd = '"' + $venv + '" -m uvicorn pizzaria_api_pkg.main:app --host 0.0.0.0 --port ' + $Port + ' --reload > "' + $log + '" 2>&1'
Write-Host "Running: cmd.exe /c $cmd"
$p = Start-Process -FilePath cmd.exe -ArgumentList '/c', $cmd -PassThru
Start-Sleep -Seconds 2
Write-Host 'Started PID:' $p.Id
if (Test-Path $log) { Get-Content $log -Tail 60 } else { Write-Host 'Log file not created yet.' }
