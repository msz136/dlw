param(
    [string]$Python = 'C:\Users\msz\AppData\Local\Programs\Python\Python313\python.exe'
)
$ErrorActionPreference = 'Stop'
$reportDir = Split-Path -Parent $MyInvocation.MyCommand.Path
& $Python (Join-Path $reportDir 'generate_error_theory.py')
if ($LASTEXITCODE -ne 0) { throw 'Document generation failed' }
$sharedBuild = Join-Path $reportDir '..\gsg_project\dlw_report\build_html.ps1'
New-Item -ItemType Directory -Force -Path (Join-Path $reportDir '..\..\report') | Out-Null
& $sharedBuild -SourceFile '..\..\dlw_factor_model_20260930\_src\dlw_error_theory.src.html' -OutputFile 'report\dlw_error_theory.html'
