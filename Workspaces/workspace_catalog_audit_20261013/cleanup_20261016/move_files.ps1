$ErrorActionPreference = 'Stop'
$planPath = Join-Path $PSScriptRoot 'move_plan.json'
$plan = Get-Content -LiteralPath $planPath -Raw -Encoding utf8 | ConvertFrom-Json
$rootPath = [IO.Path]::GetFullPath($plan.root).TrimEnd('\')
$trashPath = [IO.Path]::GetFullPath($plan.trash).TrimEnd('\')
$rootPrefix = $rootPath + '\'
$trashPrefix = $trashPath + '\'
if (-not $trashPath.StartsWith(($rootPath + '\Trash\'), [StringComparison]::OrdinalIgnoreCase)) { throw 'Trash path outside workspace Trash' }
New-Item -ItemType Directory -Path $trashPath -Force | Out-Null
$journalPath = Join-Path $PSScriptRoot 'move_journal.jsonl'
$journal = [IO.StreamWriter]::new($journalPath, $true, [Text.UTF8Encoding]::new($false))
$count = 0
try {
    foreach ($unit in $plan.move_units) {
        $sourcePath = [IO.Path]::GetFullPath((Join-Path $rootPath $unit.path))
        $destinationPath = [IO.Path]::GetFullPath((Join-Path $trashPath $unit.path))
        if (-not $sourcePath.StartsWith($rootPrefix, [StringComparison]::OrdinalIgnoreCase)) { throw "Source outside workspace: $sourcePath" }
        if ($sourcePath.StartsWith(($rootPath + '\Trash\'), [StringComparison]::OrdinalIgnoreCase)) { throw 'Cannot move existing Trash' }
        if (-not $destinationPath.StartsWith($trashPrefix, [StringComparison]::OrdinalIgnoreCase)) { throw "Destination outside cleanup Trash: $destinationPath" }
        if (-not (Test-Path -LiteralPath $sourcePath)) {
            if (Test-Path -LiteralPath $destinationPath) { continue }
            throw "Missing both source and destination: $sourcePath"
        }
        if (Test-Path -LiteralPath $destinationPath) { throw "Destination already exists: $destinationPath" }
        New-Item -ItemType Directory -Path ([IO.Path]::GetDirectoryName($destinationPath)) -Force | Out-Null
        $journal.WriteLine((@{event='planned';source=$sourcePath;destination=$destinationPath} | ConvertTo-Json -Compress))
        $journal.Flush()
        Move-Item -LiteralPath $sourcePath -Destination $destinationPath
        $journal.WriteLine((@{event='moved';source=$sourcePath;destination=$destinationPath} | ConvertTo-Json -Compress))
        $journal.Flush()
        $count++
        if (($count % 100) -eq 0) { Write-Output "Moved $count units" }
    }
} finally { $journal.Dispose() }
Write-Output "Completed: $count move units"
