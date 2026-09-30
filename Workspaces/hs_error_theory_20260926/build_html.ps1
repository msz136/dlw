$ErrorActionPreference = 'Stop'
$reportRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
python (Join-Path $reportRoot 'make_report.py')
if ($LASTEXITCODE -ne 0) { throw 'Report source generation failed' }
& (Join-Path $reportRoot '..\gsg_project\dlw_report\build_html.ps1') -SourceFile '..\..\hs_error_theory_20260926\_src\index.src.html' -OutputFile 'Workspaces\hs_error_theory_20260926\index.html'
