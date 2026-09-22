# Build a single self-contained index.html:
#   * inline katex.min.css with every woff2 font embedded as a base64 data URI
#   * inline katex.min.js + contrib/auto-render.min.js
#   * substitute the @@KATEX_CSS@@ / @@KATEX_JS@@ placeholders of _src/index.src.html
#
# Usage:  pwsh -File build_html.ps1

param(
    [string]$SourceFile = '_src\index.src.html',
    [string]$OutputFile = 'index.html'
)

$ErrorActionPreference = 'Stop'
$root   = Split-Path -Parent $MyInvocation.MyCommand.Path
$src    = Join-Path $root $SourceFile
$dist   = Join-Path $root '_assets\package\dist'
# 输出到工作区主目录（用户直接打开的那份）；$root 是 dlw_report\ 本身
$rootOut = (Resolve-Path (Join-Path $root '..\..\..')).Path
$out    = Join-Path $rootOut $OutputFile

if (-not (Test-Path $src))  { throw "missing template: $src" }
if (-not (Test-Path $dist)) { throw "missing KaTeX dist: $dist" }

$utf8 = New-Object System.Text.UTF8Encoding($false)

function Read-Text([string]$p) { [System.IO.File]::ReadAllText($p, [System.Text.Encoding]::UTF8) }

# ---- 1. CSS with embedded fonts -------------------------------------------------------
$css = Read-Text (Join-Path $dist 'katex.min.css')
$fontDir = Join-Path $dist 'fonts'
$embedded = 0
$missing  = 0

$css = [regex]::Replace($css, 'url\((?:")?fonts/([A-Za-z0-9_\-\.]+)(?:")?\)', {
    param($m)
    $name = $m.Groups[1].Value
    $path = Join-Path $fontDir $name
    if (Test-Path $path) {
        $b64 = [Convert]::ToBase64String([System.IO.File]::ReadAllBytes($path))
        $mime = switch ([System.IO.Path]::GetExtension($name)) {
            '.woff2' { 'font/woff2' }
            '.woff'  { 'font/woff'  }
            '.ttf'   { 'font/ttf'   }
            default  { 'application/octet-stream' }
        }
        $script:embedded++
        return "url(data:$mime;base64,$b64)"
    } else {
        $script:missing++
        return 'url("data:application/octet-stream;base64,")'
    }
})

# ---- 2. JavaScript --------------------------------------------------------------------
$jsFiles = @(
    (Join-Path $dist 'katex.min.js'),
    (Join-Path $dist 'contrib\auto-render.min.js')
)
$js = ''
foreach ($f in $jsFiles) {
    if (-not (Test-Path $f)) { throw "missing KaTeX asset: $f" }
    $js += "/* ==== $(Split-Path -Leaf $f) ==== */`n" + (Read-Text $f) + "`n"
}

# ---- 3. substitute ---------------------------------------------------------------------
$html = Read-Text $src
$html = $html.Replace('@@KATEX_CSS@@', $css)
$html = $html.Replace('@@KATEX_JS@@',  $js)
[System.IO.File]::WriteAllText($out, $html, $utf8)

$info = Get-Item $out
Write-Output ("built  : {0}" -f $out)
Write-Output ("size   : {0:N0} bytes ({1:N0} KB)" -f $info.Length, ($info.Length / 1KB))
Write-Output ("fonts  : {0} embedded, {1} substituted with an empty fallback" -f $embedded, $missing)
Write-Output ("remaining placeholders: {0}" -f ([regex]::Matches($html, '@@KATEX').Count))
