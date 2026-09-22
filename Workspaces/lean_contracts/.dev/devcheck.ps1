# Fast development loop: compile PkgNonlinear.lean against a pre-built Contracts.olean.
# Not the accepted verification command; used only to iterate quickly.
[CmdletBinding()]
param(
    [string]$File = 'C:\Users\msz\aca\Workspaces\lean_contracts\proofs\PkgNonlinear.lean',
    [int]$TimeoutSeconds = 900
)
$ErrorActionPreference = 'Continue'
$cfg = Get-Content 'C:\Users\msz\aca\_lean_shared\runtime.json' -Raw | ConvertFrom-Json
$devLib = 'C:\Users\msz\aca\Workspaces\lean_contracts\.dev\lib\lean'
New-Item -ItemType Directory -Force -Path $devLib | Out-Null
$srcLib = 'C:\Users\msz\aca\Workspaces\lean_contracts\proofs\.lean-runs\20260922_114510_a1288240\lib\lean'
Copy-Item -Force (Join-Path $srcLib 'Contracts.olean') (Join-Path $devLib 'Contracts.olean')
if (Test-Path (Join-Path $srcLib 'Contracts.ilean')) {
    Copy-Item -Force (Join-Path $srcLib 'Contracts.ilean') (Join-Path $devLib 'Contracts.ilean')
}
$env:LEAN_PATH = ($devLib, ($cfg.lean_paths -join ';')) -join ';'
$root = 'C:\Users\msz\aca\Workspaces\lean_contracts\proofs'
$out = Join-Path $devLib 'PkgNonlinear.olean'
$sw = [System.Diagnostics.Stopwatch]::StartNew()
$p = Start-Process -FilePath $cfg.lean_exe -ArgumentList @('-R', $root, '-o', $out, $File) `
    -WorkingDirectory $root -NoNewWindow -PassThru -RedirectStandardOutput "$env:TEMP\devcheck.out" `
    -RedirectStandardError "$env:TEMP\devcheck.err"
if (-not $p.WaitForExit($TimeoutSeconds * 1000)) { $p.Kill(); Write-Host 'TIMEOUT' }
$sw.Stop()
Get-Content "$env:TEMP\devcheck.out" -Raw
Get-Content "$env:TEMP\devcheck.err" -Raw
Write-Host "ELAPSED: $($sw.Elapsed.TotalSeconds)s"
