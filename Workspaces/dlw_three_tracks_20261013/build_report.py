"""Build the offline integrated 1A–1C report from the saved results."""
from pathlib import Path
import csv
import hashlib
import html
import json
import os
import re
import subprocess
from urllib.parse import urlsplit, unquote
import markdown

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / 'report/dlw_three_tracks_20261013.html'
CON = HERE / 'conservation'
SPEC = HERE / 'spectrum/out'
POI = HERE / 'poisson'
MATH = []


def link(path):
    return os.path.relpath(path, OUT.parent).replace('\\', '/')


def rows(path):
    with path.open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))


def fmt(value):
    return f'{float(value):.5e}'


def md(text, source=None, detail=False):
    def protect(match):
        display = match.group(1) is not None
        tex = next(g for g in match.groups() if g is not None)
        index = len(MATH)
        MATH.append({'tex': tex, 'display': display})
        return f'MATHPLACEHOLDER{index:05d}END'
    text = re.sub(r'\\\[(.*?)\\\]|\\\((.*?)\\\)|(?<!\\)\$(?!\$)(.*?)(?<!\\)\$', protect, text, flags=re.S)
    result = markdown.markdown(text, extensions=['tables', 'fenced_code'])
    if detail:
        result = re.sub(r'<(/?)h([1-6])>', lambda m: f'<{m[1]}h{min(int(m[2])+2,6)}>', result)
    if source:
        def rewrite(match):
            attr, raw = match[1], html.unescape(match[2])
            parsed = urlsplit(raw)
            if parsed.scheme or not parsed.path:
                return match[0]
            target = (source.parent / unquote(parsed.path)).resolve()
            return f'{attr}="{html.escape(link(target) + ("#" + parsed.fragment if parsed.fragment else ""), quote=True)}"'
        result = re.sub(r'(href|src)="([^"]+)"', rewrite, result)
    result = re.sub(r'<table>', '<div class="table-wrap"><table>', result)
    result = result.replace('</table>', '</table></div>')
    return result


def figure(path, caption):
    return f'<figure><a href="{link(path)}"><img loading="lazy" src="{link(path)}" alt="{html.escape(caption)}"></a><figcaption>{html.escape(caption)}</figcaption></figure>'


def detail_file(path, title):
    return '<details><summary>'+title+'</summary>'+md(path.read_text(encoding='utf-8'), path, True)+'</details>'


def main():
    cr = rows(CON / 'invariant_summary.csv')
    sr = [r for r in rows(SPEC / 'spectral_metrics.csv') if int(r['frame']) == 20 and 'halfdt' not in r['dataset']]
    refinements = rows(SPEC / 'dt_refinement.csv')
    pc = json.loads((POI / 'exact_checks.json').read_text())
    sm = json.loads((SPEC / 'manifest.json').read_text())
    cv = json.loads((CON / 'validation.json').read_text())
    parts = [md(r'''# DLW：守恒量漂移、误差频谱与离散 Poisson 结构

2026年10月13日

三项研究给出一致的认识：在连续时间的 Hamilton 空间离散中，保持 Poisson 结构与 Hamiltonian 仍不足以保持其余谱积分。周期实验中，中心差分引入的前三个谱量漂移随空间加密约二阶缩小；物理括号的精确 Jacobi 验证与动量非守恒反例揭示了这种缺陷的来源。论文孤子算例的 Fourier 与小波分析则显示，误差包含条带和脊线，频谱对加窗处理明显敏感，尚无新增孤子的谱证据。

1A 与 1C 使用周期平均约束流形。1B 沿用论文的缓冲计算域及孤子边界。两类试验分别回答守恒结构与实际误差形态问题。

[1A 守恒量误差](#track-a) · [1B 误差频谱与动画](#track-b) · [1C Poisson 括号](#track-c) · [数据与验证](#validation)
''')]
    parts.append('<section id="track-a">'+md(r'''## 1A　前三个谱守恒量的数值漂移

采用原周期逆单值化谱积分

\[
I_n=\int_0^{L_x}\operatorname{res}_D\mathscr L^n\,dx,
\qquad I_{n,\Delta x}=\Delta x\sum_i\rho_n[U,w;D_{\Delta x}]_i,
\qquad\Delta I_n(t)=I_{n,\Delta x}(t)-I_{n,\Delta x}(0).
\]

固定同一密度代表元进行离散评估。周期算例为 $M=3,h_y=4,c=2,\gamma=4,L_x=2\pi,T=0.02$；它沿用已有精确 Fourier 见证的规范，区别于论文的 $h_y=0.1$ 孤子试验。时间积分采用 RK4，主比较 $\Delta t=2.5\times10^{-4}$，每条轨迹保存 81 个时刻。

下表列出时间窗内最大绝对漂移。中心差分三个网格的观测阶约为 1.93–1.99。Fourier 结果在本短时低频算例中接近浮点计算误差，不据此宣称全离散可积。
'''))
    table = r'| x 算子 | $N_x$ | $\max\lvert\Delta I_1\rvert$ | $\max\lvert\Delta I_2\rvert$ | $\max\lvert\Delta I_3\rvert$ |' + '\n|---|---:|---:|---:|---:|\n'
    for r in cr:
        table += f'| {"中心差分" if "centered" in r["run"] else "Fourier"} | {r["nx"]} | {fmt(r["I1_max_abs_drift"])} | {fmt(r["I2_max_abs_drift"])} | {fmt(r["I3_max_abs_drift"])} |\n'
    parts.append(md(table))
    parts.append(figure(CON/'invariant_drift_absolute.png', '图1　指定周期算例的前三个谱积分有符号漂移（未归一化）；同一时间步，分别加密空间。'))
    parts.append(md(r'''本例的漂移可由实际缺陷率 $\mathcal D_n=DI_{n,\Delta x}[F_{\Delta x}]$ 追踪。中心差分三条轨迹中，直接方向微分后的时间积分与实测漂移相差小于 $7.5\times10^{-13}$。对第一积分还有精确关系

\[
\boxed{\Delta I_1=-\frac{\Delta K_{\Delta x}}{48}
+\frac{\Delta P_{\mathrm{mom},\Delta x}}{24}.}
\]

整条轨迹上的关系残差小于 $7\times10^{-15}$。此时数值 Hamiltonian 漂移仅约 $10^{-13}$，$I_1$ 的空间漂移来自平移动量缺陷。其根源是有限差分不满足连续乘积法则。1C 给出相应非零缺陷的精确有理数见证。

单独减小时间步得到 RK4 场误差约四阶下降；谱积分的时间误差很快进入舍入区间。空间与时间精化分别进行。
'''))
    parts.append(figure(CON/'error_separation.png', '图2　分别控制时间场误差与空间谱量漂移，避免将时间精化误认为空间精化。'))
    parts.append(detail_file(CON/'DERIVATION_AND_RESULTS.md', '展开：I₁、I₂、I₃ 的完整递推、密度、初值及数值分析'))
    parts.append('</section><section id="track-b">'+md(r'''## 1B　论文孤子误差的 Fourier、小波与局域峰分析

采用论文单孤子 $(p,q)=(1,2)$ 与二孤子 $(p_1,q_1;p_2,q_2)=(6,-5;4,-3)$。每例计算 PE（文件中记 SD）、FD 和 PE 时间步减半对照，共六条轨迹，均有 21 个真实时刻。四条基准的最终完整状态与既有论文存档逐值一致。

固定 $\Delta x=h_y=0.1,T=0.01$；主步长 $10^{-4}$，对照 $5\times10^{-5}$。误差定义为同坐标下的物理数值场减去连续精确场，不滤波、不插值。下列最大误差位于原生网格，因此与论文加密插值评价表略有不同。
'''))
    table = '| 算例 | 方法 | 场 | RMS 误差 | 最大绝对误差 |\n|---|---|---|---:|---:|\n'
    for r in sr:
        table += f'| {"单孤子" if r["dataset"].startswith("A") else "二孤子"} | {"PE" if "_SD_" in r["dataset"] else "FD"} | {r["field"]} | {fmt(r["rms_error"])} | {fmt(r["linf_error"])} |\n'
    parts.append(md(table))
    parts.append(figure(SPEC/'A_SD_RK4_fourier.png', '图3　单孤子 PE：精确场、带正负格点极值标记的误差场、二维 Fourier 功率。误差包含斜向脊线及其他条带。'))
    parts.append(md(r'''二维 FFT 使用物理角波数、加权去均值与可分离 Hann 窗，并以窗能量修正功率。窗口后的 Parseval 等式经过核验。另保留矩形截断谱作对照；窗函数改变后高频占比的显著变化，说明窗口处理不可与物理辐射混淆。这里的高频区定义为 $|k_x|\ge\pi/(2\Delta x)$ 或 $|k_y|\ge\pi/(2h_y)$。

小波采用 PyWavelets 的复 Morlet `cmor1.5-1.0`，分析最接近 $y=0$ 的共同原生截面；浅色区域标出可能的边缘影响。色谱是局域尺度诊断，不作为独立的守恒能量谱。
'''))
    table = '| 算例 | 方法 | 场 | 矩形截断高频占比 | Hann 高频占比 |\n|---|---|---|---:|---:|\n'
    for r in sr:
        table += f'| {r["dataset"][0]} | {"PE" if "_SD_" in r["dataset"] else "FD"} | {r["field"]} | {fmt(r["raw_high_k_fraction"])} | {fmt(r["high_k_fraction"])} |\n'
    parts.append(md(table))
    parts.append(figure(SPEC/'C_SD_RK4_wavelet.png', '图4　二孤子 PE：共同截面的精确／数值场、误差与 Morlet 小波图。'))
    parts.append(md(r'''局域极值以 $5\times5$ 邻域和当前误差峰值的 25% 阈值提取，排除边缘两层格点。另分析 $|e|$ 超过峰值 50% 的连通分量，并比较 35%、50%、65% 三种阈值。细长分量与沿脊线的多个格点极值，不计作多个孤子。

PE 时间步减半后，四个场的主频与最强峰位置均保持；这只说明当前时间步对这些诊断的影响很小，尚不构成空间收敛或新孤子谱证据。
'''))
    table = '| 算例 | 场 | 减半时间步的误差场相对差 | 最强峰位移 |\n|---|---|---:|---:|\n'
    for r in refinements:
        table += f'| {r["case"]} | {r["field"]} | {fmt(r["relative_field_difference"])} | {float(r["abs_peak_distance"]):.3g} |\n'
    parts.append(md(table))
    for case, label in [('A','单孤子'),('C','二孤子')]:
        parts.append('<details><summary>'+label+' PE：误差场与频谱动画（全时段固定色阶）</summary>'+figure(SPEC/f'{case}_SD_RK4_error_evolution.gif', f'{label} PE，21个真实时刻，播放为慢放。')+'</details>')
    spectrum_report = HERE/'spectrum/FINDINGS.md'
    if spectrum_report.exists():
        parts.append(detail_file(spectrum_report, '展开：频谱定义、峰检测、边缘效应及完整结果'))
    gallery = '| 算例 | 方法 | Fourier | 小波 | 动画 |\n|---|---|---|---|---|\n'
    for case in ['A', 'C']:
        for method in ['SD', 'FD']:
            stem = f'{case}_{method}_RK4'
            gallery += f'| {case} | {"PE" if method == "SD" else "FD"} | [PNG]({link(SPEC/(stem+"_fourier.png"))}) / [PDF]({link(SPEC/(stem+"_fourier.pdf"))}) | [PNG]({link(SPEC/(stem+"_wavelet.png"))}) / [PDF]({link(SPEC/(stem+"_wavelet.pdf"))}) | [GIF]({link(SPEC/(stem+"_error_evolution.gif"))}) |\n'
    parts.append('<details><summary>全部频谱图、小波图与动画</summary>'+md(gallery)+figure(SPEC/'error_diagnostics_summary.png', '四条基准轨迹的误差与频谱时序；低于舍入阈值的初始点不作对数绘图。')+'</details>')
    parts.append('</section><section id="track-c">'+md(r'''## 1C　物理变量的 Poisson 括号与 Jacobi 恒等式

令 $j,k$ 为周期 $y$ 格点，$i,\ell$ 为周期 $x$ 节点，固定 $c\ne0$ 与常数 $\gamma$。记 $P_{jk}=\delta_{jk}-1/M$，$q=Pu,r=Pv$，$\rho=-1/c$，$\omega=h_y\Delta x$。本节 $a$ 是原方程参数，出现在平移 $U=u+2a$ 中。原约束流形上的物理坐标为

\[
u_{j,i}=q_{j,i}+b_0+\rho S_i,\quad
v_{j,i}=r_{j,i}+c+4,\qquad
S_i=\frac1M\sum_aq_{a,i}r_{a,i},\quad b_0=\gamma/c-2a.
\]

对任意固定斜对称空间矩阵 $D$，自由坐标括号为

\[
\{q_{j,i},r_{k,\ell}\}_{\Delta x}=-\frac{P_{jk}D_{i\ell}}{\omega},
\qquad\{q,q\}_{\Delta x}=\{r,r\}_{\Delta x}=0.
\]

由原结构的物理坐标推前，用户要求的自括号是

\[
\boxed{\{u_{j,i},u_{k,\ell}\}_{\Delta x}
=-\frac{D_{i\ell}}{\omega}\left[
\frac\rho M(q_{j,\ell}+q_{k,i})
+\frac{\rho^2}{M^2}\sum_a(r_{a,i}q_{a,\ell}+q_{a,i}r_{a,\ell})\right].}
\]

交叉块与第二场自括号为

\[
\{u_{j,i},v_{k,\ell}\}_{\Delta x}
=-\frac{D_{i\ell}}{\omega}\left(P_{jk}+\frac\rho M r_{k,i}\right),
\qquad\{v_{j,i},v_{k,\ell}\}_{\Delta x}=0.
\]

**Jacobi 的一般证明。** 给自由常括号增加均值 Casimir 坐标后，上述物理映射可逆，逆映射包含 $q=Pu,r=Pv$。因此物理括号是常 Poisson 矩阵在光滑坐标变换下的推前，Jacobi 对任意网格成立。这里只使用有限维坐标链式法则，不使用错误的空间差分乘积法则。

对中心差分 $D_{i\ell}=(\delta_{\ell,i+1}-\delta_{\ell,i-1})/(2\Delta x)$，约束流形上的秩为 $2(M-1)(N_x-\kappa)$，奇数网格 $\kappa=1$，偶数网格 $\kappa=2$；后者额外含 Nyquist Casimir。显式物理点括号的 1596 个全符号 Jacobi 三元组及 66 项精确检查全部通过。

一个完全有理的反例进一步给出

\[
\boxed{\dot K_{\Delta x}=0,\qquad \dot P_{\mathrm{mom},\Delta x}=\frac{169}{12936}\ne0.}
\]

这是连续时间 Hamilton 空间离散的性质，已经先于时间积分误差出现。它说明 Jacobi 与能量保持本身不足以保证完整可积性。该反例与 1A 使用同一构造，参数不同；完整有理状态与全部括号块如下。
'''))
    parts.append(detail_file(POI/'report.md', '展开：完整手算推导、全部括号、Casimir、秩与有理反例'))
    parts.append('</section><section id="validation">'+md(f'''## 数据与验证

- [1A Python 脚本]({link(CON/'conservation_experiment.py')}) · [数值汇总 CSV]({link(CON/'invariant_summary.csv')}) · [逐时 CSV]({link(CON/'invariant_timeseries.csv')}) · [精化表]({link(CON/'space_refinement.csv')})。
- [1B Python 脚本]({link(HERE/'spectrum/analyze_error_fields.py')}) · [完整方法说明]({link(HERE/'spectrum/README.md')}) · [频谱与误差表]({link(SPEC/'spectral_metrics.csv')}) · [局域极值表]({link(SPEC/'local_extrema.csv')}) · [连通分量表]({link(SPEC/'excursion_components.csv')}) · [阈值敏感性]({link(SPEC/'threshold_sensitivity.csv')})。
- [1C SymPy 脚本]({link(POI/'verify_poisson.py')}) · [精确检查]({link(POI/'exact_checks.json')})。
- [完整复现说明]({link(HERE/'README.md')}) · [时序生成脚本]({link(HERE/'generate_shared.py')})。静态图均有同名 PDF；四条主轨迹均有 GIF 动画。

当前结果支持进一步区分三类误差来源：空间离散的守恒缺陷、时间积分缺陷，以及有限观测窗口造成的频谱变化。新增离散本征值、非线性长期稳定性和完整有限维 Liouville 可积性仍需独立证明。
''')+'</section>')
    raw = '\n'.join(parts)
    (HERE/'report_math.json').write_text(json.dumps(MATH, ensure_ascii=False), encoding='utf-8')
    node = """const fs=require('fs'),path=require('path');const k=require(path.resolve(process.argv[1],'../gsg_project/dlw_report/_assets/package/dist/katex.js')); const src=JSON.parse(fs.readFileSync(path.join(process.argv[1],'report_math.json'),'utf8'));const out=src.map(x=>k.renderToString(x.tex,{displayMode:x.display,throwOnError:true,strict:'error',output:'htmlAndMathml'}));fs.writeFileSync(path.join(process.argv[1],'report_math_rendered.json'),JSON.stringify(out));"""
    subprocess.run(['node', '-e', node, str(HERE)], check=True)
    rendered = json.loads((HERE/'report_math_rendered.json').read_text(encoding='utf-8'))
    for i, result in enumerate(rendered):
        raw = raw.replace(f'MATHPLACEHOLDER{i:05d}END', result)
    style = '''*{box-sizing:border-box}body{margin:0;background:#f3f2ef;color:#1b1b1b;font:17px/1.9 Georgia,"Times New Roman","SimSun",serif}main{max-width:1160px;margin:28px auto;padding:44px 54px;background:white}h1{font-size:29px;line-height:1.55;text-align:center;margin:0 0 22px}h2{font-size:23px;margin-top:40px}h3{font-size:21px}h4{font-size:18px}p{overflow-wrap:anywhere}a{color:#28556d;text-underline-offset:3px}a:focus-visible,summary:focus-visible{outline:2px solid #28556d;outline-offset:4px}figure{margin:26px 0}img{max-width:100%;height:auto;display:block;margin:auto}figcaption{font-size:14px;color:#555;margin-top:8px;text-align:center}.table-wrap{overflow-x:auto;margin:22px 0}table{border-collapse:collapse;width:100%;font-size:14px}th,td{padding:9px 10px;text-align:left;border-bottom:1px solid #ddd}th{border-block:1px solid #777}details{margin:24px 0;border-top:1px solid #bbb;padding:14px 0}summary{cursor:pointer;font-weight:600;color:#28556d}details>h3{margin-top:28px}.katex-display{overflow-x:auto;overflow-y:hidden;padding:7px 0;font-size:.92em}pre{overflow:auto;background:#f7f7f5;padding:14px;font-size:13px}code{font-size:.88em}li{margin:8px 0}@media(max-width:700px){main{margin:0;padding:24px 18px}body{font-size:16px}h1{font-size:24px}h2{font-size:21px}.katex-display{font-size:.85em}th,td{padding:7px}table{min-width:600px}}@media print{body{background:white;font-size:10.5pt}main{margin:0;padding:0;max-width:none}h1{font-size:20pt}h2{font-size:15pt}figure{break-inside:avoid}summary{color:#222}a{color:inherit}table{font-size:9pt;min-width:0}.table-wrap{overflow:visible}}'''
    output = '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="DLW三项并行研究：前三谱积分漂移、误差场Fourier及小波分析、物理Poisson括号和Jacobi证明。"><title>DLW：守恒量、频谱与Poisson结构</title><link rel="stylesheet" href="../Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.min.css"><style>'+style+'</style></head><body><main>'+raw+'</main></body></html>'
    OUT.write_text(output, encoding='utf-8')
    print(json.dumps({'report': str(OUT), 'math_count': len(MATH), 'bytes': OUT.stat().st_size}, ensure_ascii=False))


if __name__ == '__main__':
    main()
