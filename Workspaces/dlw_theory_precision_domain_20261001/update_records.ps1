$ErrorActionPreference = 'Stop'
$recordsRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$progressBlock = @'
> **2026-10-01（T04：DLW 高阶精度的数据空间与可信时间）：** 完成本题独立线性研究，根报告[DLW：高阶精度的数据空间与可信时间](Workspaces/dlw_theory_precision_domain_20261001/report.html)。固定周期边界、零背景、非零η和精确y导数；从已有增长谱证明中心Gaussian半径损失的尖锐条件Δr≥T，对称Gaussian端点另需一次权余量；给Sobolev/普通解析权不连续性与固定解析初态非分布反例。当前四阶x差分在严格Gaussian余量下统一O(k⁴)，余量μ趋零时充分界为Ck⁴μ⁻³；临界虽逐数据收敛，整个单位球不统一收敛。整数未加权带宽的绝对联合极限为k⁴K⁶exp[T(K²+2K/|η|+O(1))]→0，K∼c√log(1/k)的严格阈值Tc²<4；η=1的指定floor临界路径失败。独立核推空间/Euler/RK4尺度、真实内部符号峰与Nyquist消去、十倍种子仅延长log10/γ。两代理证明复核；预测冻结后仅420位二维模态核验，Gaussian末级误差比15.968，无新PDE、无参数扫描、未改共用求解器。正文24公式/4表/222数学渲染，1280/390检查通过。专属目录Workspaces/dlw_theory_precision_domain_20261001/保存证明、冻结预测、核验与源；冻结P4临界宽泛措辞的逻辑限定保存在THEORY_AUDIT.md。未声称孤子背景/非线性适定性或当前开链谱结论，外部文献原创性未核查。
'@
$indexBlock = @'
**T04：DLW 高阶精度的数据空间与可信时间（2026-10-01）：**

- [DLW：高阶精度的数据空间与可信时间](Workspaces/dlw_theory_precision_domain_20261001/report.html)（Gaussian尖锐半径、Sobolev/解析线性反例、严格余量统一四阶与临界单位球反例、整数带宽联合极限；24公式、4表）
- Workspaces/dlw_theory_precision_domain_20261001/report.src.html、build_report.py、manifest.json（本题专属正文源、自包含页面生成与SHA256）
- Workspaces/dlw_theory_precision_domain_20261001/data_space_review.md、symbol_review.md、THEORY_AUDIT.md（独立证明复核、精度阈值与端点、既有事实/新证明/限制及冻结措辞限定）
- Workspaces/dlw_theory_precision_domain_20261001/PREDICTIONS.json、verify_predictions.py、verification.json（数值前冻结；420位直接二维模态核验，无新PDE或调参）
- Workspaces/dlw_theory_precision_domain_20261001/check_report.cjs、html_validation.json、report_1280.png、report_390.png、report_uniform.png（222数学渲染、公式/本地链接/宽窄屏核验）
- Workspaces/dlw_theory_precision_domain_20261001/update_records.ps1（重读并独占短时写入本题共享进度/索引条目）
'@
function Edit-LatestRecord([string]$name, [string]$block, [string]$marker, [bool]$isIndex) {
    $recordPath = Join-Path $recordsRoot $name
    $stream = [System.IO.FileStream]::new($recordPath,[System.IO.FileMode]::Open,[System.IO.FileAccess]::ReadWrite,[System.IO.FileShare]::None)
    try {
        $reader = [System.IO.StreamReader]::new($stream,[System.Text.Encoding]::UTF8,$true,1024,$true)
        $latest = $reader.ReadToEnd()
        $reader.Dispose()
        $lf = [string][char]10
        $crlf = [string][char]13+$lf
        $newline = if ($latest.Contains($crlf)) { $crlf } else { $lf }
        $normalizedBlock = $block.Replace($crlf,$lf).Replace($lf,$newline).TrimEnd()
        if ($latest.Contains($marker)) {
            if ($isIndex) {
                $pattern = '(?ms)^\*\*T04：DLW 高阶精度的数据空间与可信时间.*?(?=^\*\*|\z)'
            } else {
                $pattern = '(?m)^> \*\*2026-10-01（T04：DLW 高阶精度的数据空间与可信时间）.*(?:\r?\n){0,2}'
            }
            $updated = [regex]::Replace($latest,$pattern,[System.Text.RegularExpressions.MatchEvaluator]{param($match) $normalizedBlock+$newline+$newline})
        } elseif ($isIndex) {
            $headerEnd = $latest.IndexOf($newline+$newline)
            if ($headerEnd -lt 0) { throw 'Missing file index header' }
            $updated = $latest.Substring(0,$headerEnd+2*$newline.Length)+$normalizedBlock+$newline+$newline+$latest.Substring($headerEnd+2*$newline.Length)
        } else {
            $updated = $normalizedBlock+$newline+$newline+$latest
        }
        $bytes = [System.Text.UTF8Encoding]::new($false).GetBytes($updated)
        $stream.Position = 0
        $stream.Write($bytes,0,$bytes.Length)
        $stream.SetLength($bytes.Length)
        $stream.Flush()
        Write-Output ($name+': updated dedicated T04 entry; latest content preserved')
    } finally { $stream.Dispose() }
}
Edit-LatestRecord 'PROGRESS_LOG.md' $progressBlock '（T04：DLW 高阶精度的数据空间与可信时间）' $false
Edit-LatestRecord 'FILE_INDEX.md' $indexBlock '**T04：DLW 高阶精度的数据空间与可信时间' $true
