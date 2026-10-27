param([ValidateSet('all','dlw','2hs')][string]$Paper = 'all')
$ErrorActionPreference = 'Stop'
$projects = if ($Paper -eq 'all') { @('dlw','2hs') } else { @($Paper) }
foreach ($project in $projects) {
    Push-Location (Join-Path $PSScriptRoot $project)
    try {
        New-Item -ItemType Directory -Path build -Force | Out-Null
        for ($pass = 1; $pass -le 2; $pass++) {
            & xelatex '-synctex=1' '-interaction=nonstopmode' '-halt-on-error' '-aux-directory=build' 'main.tex'
            if ($LASTEXITCODE -ne 0) { throw "XeLaTeX failed for $project on pass $pass" }
        }
        Write-Host "Built: $project/main.pdf"
    } finally { Pop-Location }
}
