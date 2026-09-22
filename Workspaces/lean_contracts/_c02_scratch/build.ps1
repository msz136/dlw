param([Parameter(Mandatory=$true)][string]$File)
$ErrorActionPreference = 'Stop'
$cfg = Get-Content 'C:\Users\msz\aca\_lean_shared\runtime.json' -Raw | ConvertFrom-Json
$lean = $cfg.lean_exe
$scratch = 'C:\Users\msz\aca\Workspaces\lean_contracts\_c02_scratch'
$olean = Join-Path $scratch 'olean'
New-Item -ItemType Directory -Force -Path $olean | Out-Null
$env:LEAN_PATH = (@($olean) + $cfg.lean_paths) -join ';'
$out = [System.IO.Path]::ChangeExtension($File, '.olean')
$sw = [System.Diagnostics.Stopwatch]::StartNew()
& $lean -R $scratch -o $out $File
$code = $LASTEXITCODE
$sw.Stop()
Write-Output ("[{0:N1}s] exit={1}" -f $sw.Elapsed.TotalSeconds, $code)
exit $code
