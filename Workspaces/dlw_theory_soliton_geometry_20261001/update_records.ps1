$ErrorActionPreference = 'Stop'
$workspace = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$utf8 = [System.Text.UTF8Encoding]::new($false)
$progressEntry = @'
> **2026-10-01（DLW T03：孤子结构与二阶物理形变）：** 已完成原SD、固定a、N=1、自然解析插值下的完整谱/相位局部距离定理：`D_h(θ)=h²d_θ+O(h⁴)`、`d_θ>0`；核对物理中点y=(j+1/2)h和双场B展开，u的三阶/v的四阶复极点分别超出连续切向阶数，完整参数切空间满秩。更强地每个允许的h>0下离散u留数(+2,−1,−1)不能与连续单孤子(+2,−2)函数恒等。普通全族集合间inf距离在有界窗口为0，正结果严格限定固定点到局部族；不冒充共同初值演化下界。对称窗口奇部给显式积分下界；冻结a=0,p=2,q=−1,φ=−log2/2,t=0、Ω=[−8,8]×[−1,1]等权双场RMS后才作定点验证，求积d≈0.00758434137、du≈0.00229034330、dv≈0.00101928965；有理原函数、96项正atanh级数尾界及整数平方根严格认证d≥du>0.000031662945286865150361243802。4个预定h的局部拟合支持h²距离与h⁴余项；16组48项精确符号恒等式及2项多项式断言通过。静态与动态分开：相容传播下a=B−ΦB(0)，固定参数重标记在初态纠正中抵消；参数切向齐次边界须另行保证，实际边界不匹配另加响应。主目录[精确孤子结构与二阶物理形变](Workspaces/dlw_theory_soliton_geometry_20261001/report.html)，证明/冻结快照、认证/验证、生成源码在`Workspaces/dlw_theory_soliton_geometry_20261001/`；18公式、4表行、1280/390px无页面溢出或公式错误。未运行PDE、未扫参数、未改共用求解器或登记；一般初值传播与外部文献原创性未证明。
'@
$indexEntry = @'
**DLW T03：孤子结构与二阶物理形变（2026-10-01）：**

- [精确孤子结构与二阶物理形变](Workspaces/dlw_theory_soliton_geometry_20261001/report.html)（完整谱/相位局部距离h²d+O(h⁴)、严格正系数、有限h非恒等性、认证下界；静态与共同初值演化分开）
- `Workspaces/dlw_theory_soliton_geometry_20261001/THEORY.md`、`frozen/THEORY_v1.md`（完整证明、自然函数插值、冻结参数/窗口/范数、冻结后文字校正记录）；`audit/EXACT_FAMILY_AUDIT.md`（独立公式核对）
- `Workspaces/dlw_theory_soliton_geometry_20261001/symbolic_checks.py`、`symbolic_validation.json`（16组48项精确恒等式及2项多项式断言；展开、切向、极点与留数）
- `Workspaces/dlw_theory_soliton_geometry_20261001/quantitative_bound.py`、`quantitative_bound.json`（有理原函数、正atanh级数尾界与整数平方根；d≥du>3.166e−5的严格认证）
- `Workspaces/dlw_theory_soliton_geometry_20261001/verify_geometry.py`、`geometry_validation.json`（冻结单点4个h，80/120/180阶求积及全参数局部拟合；无PDE或扫描）
- `Workspaces/dlw_theory_soliton_geometry_20261001/build_report.py`、`dlw_soliton_geometry.src.html`、`manifest.json`（论文式自包含HTML生成与哈希）；`check_report.cjs`、`html_validation.json`、`report_1280.png`、`report_390.png`、`report_theorem.png`、`report_validation.png`（18公式、引用与宽窄屏检查）；`update_records.ps1`（共享索引的短时独占局部写入）
'@

function Update-Record([string]$name, [string]$entry, [bool]$isIndex) {
    $path = Join-Path $workspace $name
    # Re-read current bytes under an exclusive handle to preserve concurrent work.
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
        if ($current.Contains('**DLW T03：') -or $current.Contains('（DLW T03：')) {
            Write-Output "$name already contains the topic; no duplicate inserted."
            return
        }
        $nl = if ($current.Contains("`r`n")) { "`r`n" } else { "`n" }
        $localEntry = $entry.Replace("`r`n", "`n").Replace("`n", $nl).TrimEnd()
        if ($isIndex) {
            $headingEnd = $current.IndexOf($nl)
            if ($headingEnd -lt 0 -or -not $current.StartsWith('# 工作区逐文件索引')) { throw 'Unexpected index heading' }
            $head = $current.Substring(0, $headingEnd+$nl.Length)
            $tail = $current.Substring($headingEnd+$nl.Length)
            $updated = $head+$nl+$localEntry+$nl+$tail
            if (-not $updated.EndsWith($tail)) { throw 'Index preservation failed' }
        } else {
            $updated = $localEntry+$nl+$nl+$current
            if (-not $updated.EndsWith($current)) { throw 'Progress preservation failed' }
        }
        $outBytes = $utf8.GetBytes($updated)
        $stream.Position = 0
        $stream.Write($outBytes, 0, $outBytes.Length)
        $stream.SetLength($outBytes.Length)
        $stream.Flush($true)
        Write-Output "$name updated; all preceding other-topic bytes preserved."
    } finally { $stream.Dispose() }
}

Update-Record 'PROGRESS_LOG.md' $progressEntry $false
Update-Record 'FILE_INDEX.md' $indexEntry $true
