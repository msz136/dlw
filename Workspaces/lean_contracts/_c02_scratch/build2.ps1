param()
$ErrorActionPreference = 'Stop'
$scratch = 'C:\Users\msz\aca\Workspaces\lean_contracts\_c02_scratch'
$real = 'C:\Users\msz\aca\Workspaces\lean_contracts\proofs\PkgC02.lean'
$lines = [System.IO.File]::ReadAllLines($real)
$idx = ($lines | Select-String -Pattern '^end DLWContract' | Select-Object -Last 1).LineNumber
$prefix = $lines[0..($idx - 2)]
$appendix = [System.IO.File]::ReadAllLines((Join-Path $scratch 'appendix.lean'))
$out = @($prefix) + @($appendix) + @('end DLWContract')
[System.IO.File]::WriteAllLines((Join-Path $scratch 'PkgC02.lean'), $out)
$cfg = Get-Content 'C:\Users\msz\aca\_lean_shared\runtime.json' -Raw | ConvertFrom-Json
$olean = Join-Path $scratch 'olean'
New-Item -ItemType Directory -Force -Path $olean | Out-Null
$env:LEAN_PATH = (@($olean) + $cfg.lean_paths) -join ';'
$sw = [System.Diagnostics.Stopwatch]::StartNew()
& $cfg.lean_exe -R $scratch -o (Join-Path $olean 'PkgC02.olean') (Join-Path $scratch 'PkgC02.lean')
$code = $LASTEXITCODE
$sw.Stop()
Write-Output ("[{0:N1}s] exit={1}" -f $sw.Elapsed.TotalSeconds, $code)
exit $code
