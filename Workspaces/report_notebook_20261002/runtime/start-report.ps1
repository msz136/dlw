param([switch]$NoOpenBrowser)

$ErrorActionPreference = 'Stop'
$ReportRuntimeDirectory = $PSScriptRoot
$ReportServiceUrl = 'http://127.0.0.1:8766'
$ReportPythonExecutable = 'C:\Users\msz\AppData\Local\Programs\Python\Python313\python.exe'
$ReportServerScript = Join-Path $ReportRuntimeDirectory 'report_server.py'
$ReportExpectedVersion = [regex]::Match([System.IO.File]::ReadAllText($ReportServerScript), '(?m)^VERSION\s*=\s*"([^"]+)"').Groups[1].Value
if (-not $ReportExpectedVersion) { throw 'The report service version is unavailable.' }

function Get-ReportHealth {
    try { return Invoke-RestMethod -Uri "$ReportServiceUrl/api/health" -TimeoutSec 2 }
    catch { return $null }
}

try {
    $ReportHealth = Get-ReportHealth
    for ($ReportStopAttempt = 0; $null -ne $ReportHealth -and $ReportHealth.status -eq 'stopping' -and $ReportStopAttempt -lt 100; $ReportStopAttempt++) {
        Start-Sleep -Milliseconds 100
        $ReportHealth = Get-ReportHealth
    }
    if ($null -ne $ReportHealth) {
        if ($ReportHealth.service -ne 'aca-report-notebook' -or $ReportHealth.version -ne $ReportExpectedVersion) {
            throw 'Port 8766 belongs to a different report service. Stop it before starting this version.'
        }
        if (-not $NoOpenBrowser) { Start-Process "$ReportServiceUrl/Report.html" }
        exit 0
    }
    if (-not (Test-Path -LiteralPath $ReportPythonExecutable -PathType Leaf)) {
        throw 'The existing Python interpreter is unavailable. No environment was installed.'
    }
    $ReportStartTag = Get-Date -Format 'yyyyMMdd_HHmmss_fff'
    $ReportOutputLog = Join-Path $ReportRuntimeDirectory "server_$ReportStartTag.log"
    $ReportErrorLog = Join-Path $ReportRuntimeDirectory "server_$ReportStartTag.err.log"
    $ReportProcess = Start-Process -FilePath $ReportPythonExecutable -ArgumentList @('-u', ('"' + $ReportServerScript + '"'), '--port', '8766') -WorkingDirectory $ReportRuntimeDirectory -WindowStyle Hidden -PassThru -RedirectStandardOutput $ReportOutputLog -RedirectStandardError $ReportErrorLog
    for ($ReportAttempt = 0; $ReportAttempt -lt 60; $ReportAttempt++) {
        Start-Sleep -Milliseconds 250
        $ReportHealth = Get-ReportHealth
        if ($null -ne $ReportHealth -and $ReportHealth.service -eq 'aca-report-notebook' -and $ReportHealth.version -eq $ReportExpectedVersion) {
            if (-not $NoOpenBrowser) { Start-Process "$ReportServiceUrl/Report.html" }
            exit 0
        }
        $ReportProcess.Refresh()
        if ($ReportProcess.HasExited) {
            throw "The report service could not start. See $ReportErrorLog"
        }
    }
    throw "The report service did not become ready. See $ReportOutputLog"
}
catch {
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}
