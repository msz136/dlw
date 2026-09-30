$ErrorActionPreference = 'Stop'
$reportRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
python (Join-Path $reportRoot 'make_dynamic_mesh_report.py')
if ($LASTEXITCODE -ne 0) { throw 'Dynamic mesh report source generation failed' }
& (Join-Path $reportRoot '..\gsg_project\dlw_report\build_html.ps1') -SourceFile '..\..\hs_error_theory_20260926\_src\dynamic_mesh.src.html' -OutputFile 'Workspaces\hs_error_theory_20260926\DYNAMIC_MESH_REPORT.html'
