$ErrorActionPreference = 'Stop'
$ReportStatePath = Join-Path $PSScriptRoot 'server-state.json'
try {
    if (-not (Test-Path -LiteralPath $ReportStatePath -PathType Leaf)) {
        Write-Host 'The report service is already stopped.'
        exit 0
    }
    $ReportState = Get-Content -LiteralPath $ReportStatePath -Raw | ConvertFrom-Json
    if ($ReportState.status -ne 'running') {
        Write-Host 'The report service is already stopped.'
        exit 0
    }
    $ReportServiceUrl = "http://127.0.0.1:$($ReportState.port)"
    $ReportHealth = Invoke-RestMethod -Uri "$ReportServiceUrl/api/health" -TimeoutSec 3
    if ($ReportHealth.service -ne 'aca-report-notebook' -or $ReportHealth.pid -ne $ReportState.pid) {
        throw 'The saved process does not match the running report service.'
    }
    $ReportStopBody = @{token = $ReportState.token} | ConvertTo-Json -Compress
    Invoke-RestMethod -Uri "$ReportServiceUrl/api/stop" -Method Post -ContentType 'application/json' -Headers @{Origin = $ReportServiceUrl} -Body $ReportStopBody -TimeoutSec 25 | Out-Null
    for ($ReportWaitAttempt = 0; $ReportWaitAttempt -lt 100; $ReportWaitAttempt++) {
        Start-Sleep -Milliseconds 100
        try { $ReportRemainingHealth = Invoke-RestMethod -Uri "$ReportServiceUrl/api/health" -TimeoutSec 1 }
        catch { $ReportRemainingHealth = $null }
        if ($null -eq $ReportRemainingHealth -or $ReportRemainingHealth.pid -ne $ReportState.pid) { break }
    }
    if ($null -ne $ReportRemainingHealth -and $ReportRemainingHealth.pid -eq $ReportState.pid) {
        throw 'The report service is still finishing cancellation. Wait a moment and retry.'
    }
    Write-Host 'Report service stopped; active Lean runs were cancelled.'
    exit 0
}
catch {
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}
