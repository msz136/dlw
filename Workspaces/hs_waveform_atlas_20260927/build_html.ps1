$ErrorActionPreference = 'Stop'
$reportRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
python (Join-Path $reportRoot 'build_report.py')
if ($LASTEXITCODE -ne 0) { throw 'Atlas report source generation failed' }
& (Join-Path $reportRoot '..\gsg_project\dlw_report\build_html.ps1') -SourceFile '..\..\hs_waveform_atlas_20260927\_src\index.src.html' -OutputFile 'Workspaces\hs_waveform_atlas_20260927\index.html'
