$ErrorActionPreference = 'Stop'
$workspace = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$utf8 = [System.Text.UTF8Encoding]::new($false)
$lead = @'
> **2026-10-02（DLW Euler误差分布、误差系数与因素映射）：** 按用户修订，主报告[index第6节](index.html#section-6)与[误差图集](report/dlw_waveform_fields.html)撤下波形/剖面对照及RK4图，只保留Euler在T=.01、x∈[-1,1]的绝对误差分布；A/B单孤子与C二孤子、SD/SD2/FD、fixed/moving、u/v分别绘成36张单面板图，按算例/网格/场折叠、各方案纵向逐张显示。当前窗口使用原4001点中的401点及原24层y，window max和青色十字均重新按窗口计算；同case/field共用Euler裁窗色标、平方根颜色映射，刻度为绝对误差。18份Euler原场哈希通过，36局部误差与独立有理tau重算最大差1.332e−15、所有峰位一致；原裁窗误差数组读回差0。5原表与16公式保留，A/SD2/fixed†保留；原全域表指标不改。两根HTML各36独立误差图，桌面/390px公式、图片、折叠、链接与溢出核验通过。当前绘图/构建、36PNG/PDF、局部CSV/NPZ、独立核验与修改前页面位于`Workspaces/dlw_waveform_fields_20261001/revision_euler_crop/`，正常构建入口已转为此Euler版；旧图与初版证据保留。
'@
$newIndex = @'
- [DLW：Euler 局部误差分布](report/dlw_waveform_fields.html)（T=.01、x∈[-1,1]；18Euler组合，u/v、三方案、两网格分别绘成36张单图；index第6节同步）
- `Workspaces/dlw_waveform_fields_20261001/revision_euler_crop/plot_euler_errors.py`、`build_euler_reports.py`、`euler_errors.src.html`（当前单面板绘图与两根HTML生成，build_reports.py入口转发）
- `Workspaces/dlw_waveform_fields_20261001/revision_euler_crop/euler_cropped_errors.csv`、`euler_cropped_errors.npz`、`euler_plot_validation.json`、`euler_delivery_manifest.json`、`euler_figure_manifest.json`（401×24裁窗误差、36峰位/色限与交付哈希）
- `Workspaces/dlw_waveform_fields_20261001/revision_euler_crop/euler_crop_audit.py`、`euler_crop_audit.json`（18源哈希与36独立有理tau误差/峰位复核）
- `Workspaces/dlw_waveform_fields_20261001/check_euler_report.cjs`、`euler_html_validation.json`、`euler_preview/`（两页各36独立Euler图、宽窄屏与折叠核对）
- `Workspaces/dlw_waveform_fields_20261001/revision_euler_crop/figures/*.png/.pdf`、`before/`、`update_euler_records.ps1`、`euler_registration.json`（36单图PNG/PDF、修订前备份与合并登记）
'@

function Update-Record([string]$name) {
    $path = Join-Path $workspace $name
    $stream = [System.IO.FileStream]::new($path, [System.IO.FileMode]::Open, [System.IO.FileAccess]::ReadWrite, [System.IO.FileShare]::None)
    try {
        $bytes=[byte[]]::new([int]$stream.Length);$offset=0
        while ($offset -lt $bytes.Length) {
            $read=$stream.Read($bytes,$offset,$bytes.Length-$offset)
            if ($read -eq 0) { throw 'Unexpected EOF' };$offset+=$read
        }
        $current=$utf8.GetString($bytes)
        $nl=if($current.Contains("`r`n")){"`r`n"}else{"`n"}
        if ($name -eq 'PROGRESS_LOG.md') {
            if ($current.Contains('（DLW Euler误差分布、误差系数与因素映射）')) { return }
            $match=[regex]::Match($current,'(?m)^> \*\*2026-10-01（DLW 波形分布、误差系数与因素映射）：\*\*[^\r\n]*')
            if (-not $match.Success) { throw 'Existing DLW topic not found' }
            $old=$match.Value -replace '^> \*\*2026-10-01（DLW 波形分布、误差系数与因素映射）：\*\*\s*',''
            $rest=$current.Remove($match.Index,$match.Length).TrimStart("`r","`n")
            $updated=$lead.TrimEnd()+' **此前2026-10-01图集（已被上述Euler单图版替代）：** '+$old+$nl+$nl+$rest
        } else {
            if ($current.Contains('revision_euler_crop/plot_euler_errors.py')) { return }
            $match=[regex]::Match($current,'(?m)^- \[DLW 孤子波形与误差分布\]\(dlw_waveform_fields\.html\)[^\r\n]*')
            if (-not $match.Success) { throw 'Old plot index entry not found' }
            $local=$newIndex.TrimEnd().Replace("`r`n","`n").Replace("`n",$nl)
            $updated=$current.Remove($match.Index,$match.Length).Insert($match.Index,$local)
            $updated=$updated.Replace('（2026-10-01／09-30／29）：**','（2026-10-02／01／09-30／29）：**')
        }
        $out=$utf8.GetBytes($updated);$stream.Position=0
        $stream.Write($out,0,$out.Length);$stream.SetLength($out.Length);$stream.Flush($true)
        Write-Output "$name updated in existing topic."
    } finally {$stream.Dispose()}
}
Update-Record 'PROGRESS_LOG.md'
Update-Record 'FILE_INDEX.md'
@{status='registered';scope='Euler errors only; x=[-1,1]; 36 separate figures';date='2026-10-02'} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'euler_registration.json') -Encoding utf8
