param([int]$ReportVerificationPort = 8767, [int]$ReportIdleSeconds = 6)

$ErrorActionPreference = 'Stop'
$ReportPackageDirectory = $PSScriptRoot
$ReportExecutable = Join-Path $ReportPackageDirectory 'Report.exe'
$ReportServiceUrl = "http://127.0.0.1:$ReportVerificationPort"
$ReportVerificationStarted = (Get-Date).ToUniversalTime()
$ReportVerificationStamp = Get-Date -Format 'yyyyMMdd_HHmmss_fff'

function Test-ReportPort {
    $ReportSocket = New-Object System.Net.Sockets.TcpClient
    try {
        $ReportSocket.Connect('127.0.0.1', $ReportVerificationPort)
        return $true
    }
    catch { return $false }
    finally { $ReportSocket.Dispose() }
}

if (Test-ReportPort) { throw "Verification requires unused port $ReportVerificationPort." }
$ReportExecutableBytes = [System.IO.File]::ReadAllBytes($ReportExecutable)
$ReportPeOffset = [BitConverter]::ToInt32($ReportExecutableBytes, 0x3c)
$ReportSubsystem = [BitConverter]::ToUInt16($ReportExecutableBytes, $ReportPeOffset + 24 + 68)
if ($ReportSubsystem -ne 2) { throw 'Launcher is not a Windows GUI executable.' }

$ReportArguments = @('--no-open', '--port', [string]$ReportVerificationPort, '--idle-seconds', [string]$ReportIdleSeconds)
$ReportFirstLauncher = Start-Process -FilePath $ReportExecutable -ArgumentList $ReportArguments -WindowStyle Hidden -PassThru
$ReportSecondLauncher = Start-Process -FilePath $ReportExecutable -ArgumentList $ReportArguments -WindowStyle Hidden -PassThru
$ReportFirstLauncher.WaitForExit(60000) | Out-Null
$ReportSecondLauncher.WaitForExit(60000) | Out-Null
$ReportFirstLauncher.Refresh()
$ReportSecondLauncher.Refresh()
if (-not $ReportFirstLauncher.HasExited -or -not $ReportSecondLauncher.HasExited) { throw 'Launcher did not exit.' }
if ($ReportFirstLauncher.ExitCode -ne 0 -or $ReportSecondLauncher.ExitCode -ne 0) { throw 'Launcher failed. See package/logs/.' }
$ReportOutcomes = @(Get-ChildItem -LiteralPath (Join-Path $ReportPackageDirectory 'logs') -Filter 'launcher_*.json' |
    Where-Object { $_.LastWriteTimeUtc -ge $ReportVerificationStarted } |
    ForEach-Object { Get-Content -LiteralPath $_.FullName -Raw | ConvertFrom-Json })
if ($ReportOutcomes.Count -ne 2) { throw 'Expected exactly two launcher outcomes.' }
if (@($ReportOutcomes | Where-Object { $_.started }).Count -ne 1) { throw 'Two simultaneous opens should start exactly one service.' }
if (@($ReportOutcomes.pid | Select-Object -Unique).Count -ne 1) { throw 'Second launcher did not reuse the first service.' }
$ReportHealth = Invoke-RestMethod -Uri "$ReportServiceUrl/api/health" -TimeoutSec 3
$ReportServiceProcess = Get-Process -Id $ReportHealth.pid
$ReportServiceWindow = $ReportServiceProcess.MainWindowHandle.ToInt64()
if ($ReportServiceWindow -ne 0) { throw 'Service has a visible main window.' }
$ReportProcessDetails = Get-CimInstance -ClassName Win32_Process -Filter "ProcessId=$($ReportHealth.pid)"
$ReportChildren = @(Get-CimInstance -ClassName Win32_Process -Filter "ParentProcessId=$($ReportHealth.pid)" | ForEach-Object {
    $ReportChildWindow = (Get-Process -Id $_.ProcessId -ErrorAction SilentlyContinue).MainWindowHandle
    [pscustomobject]@{ ProcessId=$_.ProcessId; Name=$_.Name; CommandLine=$_.CommandLine; MainWindowHandle=[int64]$ReportChildWindow }
})
if (@($ReportChildren | Where-Object { $_.Name -in @('cmd.exe', 'powershell.exe', 'pwsh.exe') }).Count -ne 0) {
    throw 'Unexpected terminal process below report service.'
}
if (@($ReportChildren | Where-Object { $_.MainWindowHandle -ne 0 }).Count -ne 0) { throw 'Service child has a visible window.' }
$ReportServicePid = [int]$ReportHealth.pid
$ReportShutdownDeadline = (Get-Date).AddSeconds($ReportIdleSeconds + 15)
while ((Get-Date) -lt $ReportShutdownDeadline -and (Test-ReportPort)) { Start-Sleep -Milliseconds 250 }
$ReportStopped = -not (Test-ReportPort)
if (-not $ReportStopped) { throw 'Unopened report service did not automatically exit after the idle deadline.' }

$ReportVerification = [ordered]@{
    verifiedAtUtc = (Get-Date).ToUniversalTime().ToString('o')
    passed = $true
    artifact = $ReportExecutable
    peSubsystem = $ReportSubsystem
    simultaneousOpens = 2
    freshServices = @($ReportOutcomes | Where-Object { $_.started }).Count
    sharedServicePid = $ReportServicePid
    mainWindowHandle = $ReportServiceWindow
    browserOpened = $false
    commandLine = $ReportProcessDetails.CommandLine
    childProcesses = $ReportChildren
    health = $ReportHealth
    autoIdleExit = $ReportStopped
    idleSeconds = $ReportIdleSeconds
    outcomes = $ReportOutcomes
}
$ReportVerificationPath = Join-Path $ReportPackageDirectory "verification_$ReportVerificationStamp.json"
$ReportVerification | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $ReportVerificationPath -Encoding UTF8
$ReportVerification | ConvertTo-Json -Depth 10
