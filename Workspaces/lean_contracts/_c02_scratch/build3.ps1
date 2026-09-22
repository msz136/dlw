param(
  [string]$File = 'C:\Users\msz\aca\Workspaces\lean_contracts\_c02_scratch\PkgC02_merged.lean',
  [string]$Out = 'C:\Users\msz\aca\Workspaces\lean_contracts\_c02_scratch\olean\PkgC02_merged.olean'
)
$cfg = Get-Content 'C:\Users\msz\aca\_lean_shared\runtime.json' -Raw | ConvertFrom-Json
$root = Split-Path $File
$env:LEAN_PATH = (@('C:\Users\msz\aca\Workspaces\lean_contracts\_c02_scratch\olean') + $cfg.lean_paths) -join ';'
$sw = [System.Diagnostics.Stopwatch]::StartNew()
& $cfg.lean_exe -R $root -o $Out $File 2>&1 | Select-Object -Last 40
$code = $LASTEXITCODE
$sw.Stop()
"[{0:N1}s] exit={1}" -f $sw.Elapsed.TotalSeconds, $code
exit $code
