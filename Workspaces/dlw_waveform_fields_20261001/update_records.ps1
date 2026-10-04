$ErrorActionPreference = 'Stop'
$workspace = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$utf8 = [System.Text.UTF8Encoding]::new($false)
$newProgress = @'
> **2026-10-01（DLW 波形分布、误差系数与因素映射）：** 已按Report.html的解析曲线/实际数值节点叠加画法，为主报告A/B单孤子和C二孤子生成T=.01的u/v波形剖面、逐点绝对误差及x–y波形/误差分布。覆盖SD/SD2/FD×Euler/RK4×fixed/moving全部36组，新增[index第6节](index.html#section-6)的12幅剖面及`report/` 下的[完整图集](report/dlw_waveform_fields.html)的36幅图；36张PNG/PDF与12张SVG在`Workspaces/dlw_waveform_fields_20261001/figures/`。只读既有物理场，无新PDE；4001×24评价点、原三次样条、初始误差保留，剖面取真实y=−1/16层。误差图采用同case/field共用色标与平方根颜色映射、原值刻度，并标出全场峰。独立有理tau重算72项误差与原CSV/记录最大差8.882e−16、36源哈希通过；图生成读回差≤6.662e−16。A/SD2/fixed原空间控制未通过的†保留；表4 C/SD2/u显示末位1.189修正为1.190。两根HTML图片自包含，1440/390px数学、全部图片、折叠、链接及页面溢出核验通过；5张原表仅该末位变化、16公式完整保留。绘图/构建/独立审查、图数据NPZ、72项误差CSV、核验记录及修改前副本在本题目录。
'@
$indexLines = @'
- [DLW 孤子波形与误差分布](report/dlw_waveform_fields.html)（T=.01，36实验组合；u/v二维波形、全场绝对误差与原层剖面，36张自包含图；index第6节含12张剖面）
- `Workspaces/dlw_waveform_fields_20261001/plot_fields.py`、`build_reports.py`、`waveform_fields.src.html`、`README.md`（保存场作图、自包含两报告生成与复现）
- `Workspaces/dlw_waveform_fields_20261001/field_errors.csv`、`plotted_fields.npz`、`plot_validation.json`、`delivery_manifest.json`（72全场误差/峰位、全部绘图场、原始场/图数据核对与交付哈希）
- `Workspaces/dlw_waveform_fields_20261001/audit_saved_fields.py`、`data_audit.json`（36源哈希、独立tau参照、72原表误差与48比值复核）
- `Workspaces/dlw_waveform_fields_20261001/check_report.cjs`、`html_validation.json`、`html_preview/`（双页1440/390px数学、36/12图解码、折叠与链接核对）
- `Workspaces/dlw_waveform_fields_20261001/figures/*_profiles.png/.pdf/.svg`、`*_wavefields.png/.pdf`、`*_errorfields.png/.pdf`（A/B/C×RK4/Euler×fixed/moving；36PNG、36PDF、12SVG）；`before/`、`update_records.ps1`、`registration.json`（修改前副本与共享记录的合并登记）
'@

function Update-Record([string]$name) {
    $path = Join-Path $workspace $name
    $stream = [System.IO.FileStream]::new($path, [System.IO.FileMode]::Open, [System.IO.FileAccess]::ReadWrite, [System.IO.FileShare]::None)
    try {
        $bytes = [byte[]]::new([int]$stream.Length)
        $offset = 0
        while ($offset -lt $bytes.Length) {
            $read = $stream.Read($bytes, $offset, $bytes.Length-$offset)
            if ($read -eq 0) { throw 'Unexpected EOF' }
            $offset += $read
        }
        $current = $utf8.GetString($bytes)
        $nl = if ($current.Contains("`r`n")) { "`r`n" } else { "`n" }
        if ($name -eq 'PROGRESS_LOG.md') {
            if ($current.Contains('（DLW 波形分布、误差系数与因素映射）')) { return }
            $pattern = '(?m)^> \*\*2026-09-30（固定网格误差系数与因素映射）：\*\*[^\r\n]*'
            $match = [regex]::Match($current, $pattern)
            if (-not $match.Success) { throw 'Existing same-topic progress entry not found' }
            $old = $match.Value -replace '^> \*\*2026-09-30（固定网格误差系数与因素映射）：\*\*\s*', ''
            $merged = $newProgress.TrimEnd()+ ' **此前固定网格误差系数与因素映射（2026-09-30）：** '+$old
            $rest = $current.Remove($match.Index, $match.Length).TrimStart("`r", "`n")
            $updated = $merged+$nl+$nl+$rest
        } else {
            if ($current.Contains('[DLW 孤子波形与误差分布](report/dlw_waveform_fields.html)')) { return }
            $oldTitle = '**DLW 固定网格二阶系数与三路线误差（2026-09-30／29）：**'
            if (-not $current.Contains($oldTitle)) { throw 'Existing index section not found' }
            $updated = $current.Replace($oldTitle, '**DLW 波形分布、固定网格二阶系数与三路线误差（2026-10-01／09-30／29）：**')
            $line = [regex]::Match($updated, '(?m)^- \[index\.html\]\(index\.html\)[^\r\n]*')
            if (-not $line.Success) { throw 'Index root report line not found' }
            $local = $indexLines.TrimEnd().Replace("`r`n", "`n").Replace("`n", $nl)
            $updated = $updated.Insert($line.Index+$line.Length, $nl+$local)
        }
        $outBytes = $utf8.GetBytes($updated)
        $stream.Position = 0
        $stream.Write($outBytes, 0, $outBytes.Length)
        $stream.SetLength($outBytes.Length)
        $stream.Flush($true)
        Write-Output "$name merged with existing topic."
    } finally { $stream.Dispose() }
}
Update-Record 'PROGRESS_LOG.md'
Update-Record 'FILE_INDEX.md'
@{status='registered'; progress='merged existing DLW topic and moved to top'; index='extended existing DLW section'} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'registration.json') -Encoding utf8
