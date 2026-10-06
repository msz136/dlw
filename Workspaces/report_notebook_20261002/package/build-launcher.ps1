$ErrorActionPreference = 'Stop'
$ReportPackageDirectory = $PSScriptRoot
$ReportCompiler = Join-Path $env:WINDIR 'Microsoft.NET\Framework64\v4.0.30319\csc.exe'
$ReportSource = Join-Path $ReportPackageDirectory 'ReportLauncher.cs'
$ReportOutput = Join-Path $ReportPackageDirectory 'Report.exe'

if (-not (Test-Path -LiteralPath $ReportCompiler -PathType Leaf)) {
    throw 'The existing .NET Framework compiler is unavailable.'
}
& $ReportCompiler /nologo /target:winexe /optimize+ /platform:anycpu /utf8output /codepage:65001 /reference:System.dll /reference:System.Core.dll /reference:System.Windows.Forms.dll /reference:System.Web.Extensions.dll ("/out:" + $ReportOutput) $ReportSource
if ($LASTEXITCODE -ne 0) { throw 'Report.exe compilation failed.' }
$ReportBuild = [ordered]@{
    builtAtUtc = (Get-Date).ToUniversalTime().ToString('o')
    compiler = $ReportCompiler
    target = 'Windows GUI (PE subsystem 2)'
    artifact = $ReportOutput
    sha256 = (Get-FileHash -LiteralPath $ReportOutput -Algorithm SHA256).Hash.ToLowerInvariant()
    bytes = (Get-Item -LiteralPath $ReportOutput).Length
    externalRuntime = 'Existing workspace Python + Lean/Mathlib; no installer, no bundled toolchain'
}
$ReportBuild | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $ReportPackageDirectory 'build.json') -Encoding UTF8
$ReportBuild | ConvertTo-Json
