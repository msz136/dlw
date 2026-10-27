"""Publish audited linear/discrete stability results; retain PDE certificate status."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime
from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PAPER = ROOT / 'dlw-paper.html'
REPORT = ROOT / 'report/dlw_independent_stability_20261026.html'
FIG = 'Workspaces/dlw_paper_20261009/stability_20261026/perturbation_pilot/figures/physical_perturbation_responses.png'
DATA = json.loads((HERE / 'perturbation_pilot/figures/perturbation_endpoint_table.json').read_text())
AUDIT = json.loads((HERE / 'audit_four_case.json').read_text())
MATH = []


def m(tex, display=False):
    token = f'STMATH{len(MATH)}END'
    MATH.append(dict(tex=tex, display=display))
    return token


def inline(text):
    parts = text.split('$')
    assert len(parts) % 2 == 1
    return ''.join(m(t) if i % 2 else t for i, t in enumerate(parts))


def p(text):
    return '<p>' + inline(text) + '</p>\n'


def eq(text):
    return '<div class="equation">' + m(text, True) + '</div>\n'


def render_all(texts):
    js = ("const fs=require('fs'),k=require(process.argv[1]);"
          "process.stdout.write(JSON.stringify(JSON.parse(fs.readFileSync(0,'utf8'))"
          ".map(f=>k.renderToString(f.tex,{displayMode:f.display,throwOnError:true,strict:'error'}))));")
    katex = ROOT / 'Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.js'
    out = subprocess.run(['node', '-e', js, str(katex)], input=json.dumps(MATH),
                         text=True, encoding='utf-8', capture_output=True, check=True)
    formulas = json.loads(out.stdout)
    return [re.sub(r'STMATH(\d+)END', lambda z: formulas[int(z[1])], t) for t in texts]


def table(caption, ident):
    result = '<div class="table-wrap"><table id="' + ident + '"><caption>' + inline(caption) + '</caption>'
    result += '<thead><tr><th>Background</th><th>Input</th><th>' + m(r'\|\delta u_h(T)\|_\infty/\varepsilon') + '</th><th>' + m(r'\|\delta v_h(T)\|_\infty/\varepsilon') + '</th><th>' + m(r'G_2(T)') + '</th></tr></thead><tbody>'
    for i, row in enumerate(DATA['records']):
        result += '<tr>'
        if i % 2 == 0:
            result += f'<th scope="rowgroup" rowspan="2">{row["case_label"]}</th>'
        result += '<td>' + m(row['input_field'] + '_0') + ' only</td>'
        result += ''.join(f'<td>{row[k]:.5f}</td>' for k in ['native_max_delta_u_over_epsilon', 'native_max_delta_v_over_epsilon', 'L2_pair_gain'])
        result += '</tr>'
    return result + '</tbody></table></div>\n'


S44 = '<section id="section-4.4"><h3>4.4 Linearized evolution under the numerical closure</h3>\n'
S44 += p(r'We examine how the fixed-grid Centered-SD evolution responds to a perturbation of the physical fields. The lower boundary fixes the integration constant in the first field equation, so it enters the linearized evolution together with the spatial operators. For this calculation, set $w_k=4\omega_k/h$ and write $\Delta_h^-r_k=(r_k-r_{k-1})/h$, $M_h^-s_k=(s_k+s_{k-1})/2$. Perturbations $r_k$ and $s_k$ of $u_k$ and $w_k$ then give the physical perturbation $q_k=\Delta_h^-r_k+M_h^-s_k$ of $v_k$. The prescribed lower trace is held fixed, hence $r_0=0$.')
S44 += p(r'At a constant state $(u,w)=(U,V)$, put $c=U+4$ and $d=V-4$. For a non-Nyquist Fourier mode $e^{i\xi x}$, ordering the unknowns as $(s_0,r_1,s_1,r_2,s_2,\ldots)$ gives a block lower-triangular evolution matrix. The lower-boundary block is $-\xi^2-ic\xi$, and each interior diagonal block is')
S44 += eq(r'B(\xi)=\begin{pmatrix}\xi^2-ic\xi & \tfrac h2\xi^2-\tfrac{i h^2d}{16}\xi\\-id\xi&-\xi^2-ic\xi\end{pmatrix},\qquad \lambda_\pm=-ic\xi\pm\left(\xi^2-\frac{ihd\xi}{4}\right).')
S44 += p(r'The diagonal entry $h/2$ in the transverse trapezoidal primitive produces the upper-right entry of this block. Its characteristic polynomial follows from $(\lambda+ic\xi)^2=(\xi^2-ihd\xi/4)^2$. Thus the real parts of the two branches are $\pm\xi^2$. At the Nyquist mode, the zero first-derivative multiplier used in Section 4.1 removes the imaginary terms and leaves the same real branches. The positive branch identifies increasing sensitivity to short wavelengths in $x$. Coupling between transverse layers also affects finite-time amplification, which can be calculated explicitly when $V=4$.')
S44 += p(r'For $V=4$, set $p_k=\Delta_h^-r_k$. The linearized physical variables satisfy $p_t=-c p_x-q_{xx}$ and $q_t=-c q_x-p_{xx}$. For a non-Nyquist Fourier mode, with amplitudes denoted by hats, the solution is')
S44 += eq(r'\begin{pmatrix}\widehat p(t)\\\widehat q(t)\end{pmatrix}=e^{-ic\xi t}\begin{pmatrix}\cosh(\xi^2t)&\sinh(\xi^2t)\\\sinh(\xi^2t)&\cosh(\xi^2t)\end{pmatrix}\begin{pmatrix}\widehat p(0)\\\widehat q(0)\end{pmatrix},\qquad \widehat r_k(t)=h\sum_{j=1}^{k}\widehat p_j(t).')
S44 += p(r'This formula separates the response within each field from transfer between the fields. A perturbation initially confined to $v$ produces an $u$ response proportional to its transverse primitive, while an initial $u$ perturbation produces a $v$ response proportional to its transverse difference. Consequently, the transverse domain and the observation region contribute to the measured response even when the $x$ wavenumber is fixed. The continuous constant-background linearization has the same formula, with the difference and sum replaced by a derivative and an integral.')
S44 += p(r'Time integration acts on these spatial branches through its amplification function. At $U=0$, $V=4$, the growing branch for a non-Nyquist mode is $\lambda_+=\xi^2-4i\xi$. At Nyquist, the advection factor is one and the growing eigenvalue is $\xi^2$. Forward Euler, RK4, and Crank–Nicolson use $R(z)=1+z$, $R(z)=1+z+z^2/2+z^3/6+z^4/24$, and $R(z)=(1+z/2)/(1-z/2)$, respectively. Decreasing the time step makes $R(\Delta t\lambda_+)^{T/\Delta t}$ approach $e^{T\lambda_+}$. It resolves the growth of the spatial system more accurately; the growth rate itself is already present before time discretization.')
S44 += '</section>'

S55 = '<section id="section-5.5"><h3>5.5 Independent physical-field perturbations</h3>\n'
S55 += p(r'We measure the response of the fully discrete Centered-SD evolution to independent perturbations of the initial physical fields. Each of the four backgrounds in Section 5.1 is evolved with $h=\Delta x=0.1$, RK4, $\Delta t=10^{-4}$, and $T=0.01$. Two experiments add $\varepsilon\Phi$ to $u_0$ or to $v_0$, respectively, where')
S55 += eq(r'\Phi(x,y)=\sin^2\!\left(\frac{\pi(y-y_L)}{y_R-y_L}\right)\cos(\kappa x),\qquad \kappa=\frac\pi2,\qquad \varepsilon=10^{-6}.')
S55 += p(r'The carrier has the same physical wavelength in all four cases. The envelope and its first derivative vanish at the transverse endpoints. We impose each perturbation at the native physical-field locations and recover the auxiliary values through the Centered-SD recurrence, starting with zero lower auxiliary perturbation. The perturbed and unperturbed trajectories share the prescribed lower $u$ trace. The transverse node intervals are $[-9.95,9.95]$ for the one-soliton case, $[-39.95,39.95]$ for the two-soliton case, and $[-2,2]$ for the Gaussian and sinusoidal cases.')
S55 += p(r'Let $\delta u_h$ and $\delta v_h$ denote the differences between the perturbed and unperturbed numerical trajectories. We evolve their algebraically subtracted nonlinear equations together with the background at every RK4 stage. Figure 29 follows the native-node maxima divided by $\varepsilon$, using the observation regions of Section 5.1. Table 6 also records the pair gain')
S55 += eq(r'G_2(t)=\frac{\bigl(\|\delta u_h(t)\|_{2,h}^2+\|\delta v_h(t)\|_{2,h}^2\bigr)^{1/2}}{\bigl(\|\delta u_h(0)\|_{2,h}^2+\|\delta v_h(0)\|_{2,h}^2\bigr)^{1/2}},\qquad \|f\|_{2,h}^2=h\Delta x\sum_{j,k}|f_{j,k}|^2.')
S55 += p(r'The sum covers the full periodic $x$ interval and the same interior $y$ region, separately at each field’s native sites. These quantities measure the sensitivity of the computed trajectories. An error relative to the independently perturbed continuous solution additionally requires a reference bound for that initial-value problem; such a bound remains open here.')
S55 += table(r'Table 6. Independent perturbation responses at $T=0.01$. Maximum responses are divided by the prescribed amplitude $\varepsilon=10^{-6}$; the pair gain uses its measured initial norm.', 'table-perturbation')
S55 += '<figure id="figure-29"><img src="' + FIG + '" alt="Time histories of two physical-field responses for four independently perturbed backgrounds" loading="lazy"><figcaption><strong>Figure 29.</strong> ' + inline(r'Normalized native-node perturbation maxima under Centered-SD and RK4. Rows show the one-soliton, two-soliton, Gaussian, and sinusoidal backgrounds; columns show the $u$ and $v$ responses. Solid blue curves perturb $u_0$ only, and dashed orange curves perturb $v_0$ only. All curves use $\varepsilon=10^{-6}$ and the same physical carrier $\kappa=\pi/2$.') + '</figcaption></figure>\n'
S55 += p(r'The initially perturbed component remains close to its initial magnitude over this interval, while coupling generates a response in the other field. The larger $v$-to-$u$ response in the two-soliton case is closely related to the transverse primitive in Section 4.4. Applying the constant-background formula on the actual grids and observation regions gives normalized responses $0.22248$ and $0.97158$ for the one- and two-soliton domains, compared with the measured values $0.22453$ and $0.97382$. The respective differences are about $0.92\%$ and $0.23\%$. Thus the domain and boundary closure explain most of this contrast. The reverse transfer shows a stronger background dependence: the measured $u$-to-$v$ responses are $0.09186$ and $0.10278$, compared with constant-background values $0.00389$ and $0.00097$.')
S55 += p(r'For the Gaussian and sinusoidal backgrounds, the pair gains are approximately $1.00055$ for a perturbation of $u_0$ and $1.00147$ for a perturbation of $v_0$. Their native-node maxima also reflect translation relative to the sampling grid. Evaluating the saved Fourier interpolants on eight times as many $x$ points gives same-component peak ratios of $1.00036$–$1.00038$ relative to their initial peaks. This resolves the slight decrease seen at the original nodes and shows why the maximum curves and the pair norm provide complementary information about these small responses.')
S55 += '</section>'

R = '<header><p class="eyebrow">DLW · 独立扰动 · 2026-10-26</p><h1>独立物理场扰动：响应、线性机制与连续误差界</h1></header>'
R += p(r'四个背景分别独立扰动 $u$、$v$，八条数值轨道均达到 $T=0.01$。当前结果包含完整的扰动响应表图，以及与现行 Centered-SD 闭合一致的常背景线性公式。独立扰动后的非线性连续参考解尚未获得误差证书，$\eta_u$、$\eta_v$ 仍未给出。')
R += '<nav><a href="#results">扰动结果</a><a href="#mechanism">响应从哪里来</a><a href="#certificate">连续误差界的进展</a><a href="#sources">证明与数据</a></nav>'
R += '<section id="results"><h2>1. 扰动结果</h2>'
R += p(r'使用当前论文的单孤子 A、双孤子 D、高斯和正弦四个背景。统一 $h=\Delta x=0.1$、RK4、$\Delta t=10^{-4}$。分别指定 $(\delta u_0,\delta v_0)=(\varepsilon\Phi,0)$ 和 $(0,\varepsilon\Phi)$，其中')
R += eq(r'\Phi(x,y)=\sin^2\!\left(\frac{\pi(y-y_L)}{y_R-y_L}\right)\cos\frac{\pi x}{2},\qquad\varepsilon=10^{-6}.')
R += p(r'扰动由物理场给定，辅助变量通过原有重构关系恢复；两条轨道采用相同的下边界数据。表中前两列是各场扰动的原生格点最大值除以 $\varepsilon$，最后一列是两场离散 $L^2$ 合范数相对初值的比值。最大值沿用论文的观察区间；$L^2$ 使用全周期 $x$ 区间和相同的内部 $y$ 层。')
R += table(r'表 1. $T=0.01$ 的独立扰动响应。', 'report-perturbation')
R += '<figure><img src="../' + FIG + '" alt="四个背景的独立扰动响应时间曲线"><figcaption>图 1. 左列为 u，右列为 v；蓝实线只扰动初始 u，橙虚线只扰动初始 v。纵轴均除以 ε，曲线使用全部 101 个时间层。</figcaption></figure>'
R += p(r'四条未扰动背景轨道逐元素复现既有 RK4 结果，初始物理场重构的最大偏差为 $1.06\times10^{-22}$。这里比较的是同一离散系统中两条轨道的差。')
R += '</section><section id="mechanism"><h2>2. 响应从哪里来</h2>'
R += p(r'在常背景 $(u,v)=(0,4)$，令 $p=\delta u_y$、$q=\delta v$，进入随动坐标 $X=x-4t$ 后有 $p_t=-q_{XX}$、$q_t=-p_{XX}$。每个波数 $\kappa$ 的两条分支分别以 $e^{\kappa^2t}$ 和 $e^{-\kappa^2t}$ 演化。对只扰动 $v$ 的初值，精确线性响应为')
R += eq(r'\delta u=\varepsilon J(y)\cos(\kappa X)\sinh(\kappa^2t),\quad\delta v=\varepsilon\phi(y)\cos(\kappa X)\cosh(\kappa^2t),\qquad J(y)=\int_{y_L}^y\phi(s)\,ds.')
R += p(r'其中 $\phi(y)=\sin^2(\pi(y-y_L)/L)$、$L=y_R-y_L$。设 $r=(y-y_L)/L$，则 $J(y)=L[r/2-\sin(2\pi r)/(4\pi)]$。现行 Centered-SD 在同一常背景下也有精确的双曲函数公式，只需把积分换为离散累加 $J_hq_k=h\sum_{j=1}^kq_j$。')
R += '<div class="table-wrap"><table><caption>表 2. 只扰动 v 时的 u 响应：现行网格的常背景线性公式与非线性实验，均除以 ε。</caption><thead><tr><th>背景</th><th>y 区间长度</th><th>常背景线性值</th><th>实际响应</th><th>相对差</th></tr></thead><tbody>'
labels = {'A':'单孤子 A','D':'双孤子 D','Gaussian':'高斯','Sinusoidal':'正弦'}
for row in AUDIT['records']:
    mode = row['modes'][1]
    ctrl = mode['constant_semidiscrete_native_max'][0] / 1e-6
    obs = mode['numerical_final_native_max'][0] / 1e-6
    length = row['y_interval'][1] - row['y_interval'][0]
    R += f'<tr><th>{labels[row["case"]]}</th><td>{length:.1f}</td><td>{ctrl:.6f}</td><td>{obs:.6f}</td><td>{100*(obs/ctrl-1):.3f}%</td></tr>'
R += '</tbody></table></div>'
R += p(r'双孤子算例的横向积分区间更长，因此相同幅度的 $v$ 扰动会产生更大的 $u$ 响应。这一几何因素已解释表中大部分差异。另一方向的传递更依赖背景：孤子中的 $u\!\to v$ 响应显著高于常背景公式。')
R += p(r'高斯和正弦的原生最大值略有下降，主要来自峰值相对格点的移动。速度 $4$ 在 $T=0.01$ 内带来 $0.04$ 的位移；对当前载波，原峰值格点处的因子为 $\cos(\pi\,0.04/2)\simeq0.99803$。对保存的有限 Fourier 插值加密求值后，同一分量的峰值比约为 $1.00036$–$1.00038$，与轻微增长的 $L^2$ 指标一致。')
R += '</section><section id="certificate"><h2>3. 连续参考误差界的进展</h2>'
R += p(r'对于非孤子背景，取 $A=u_y+v-4$、$B=v-u_y-4$，在 $X=x-4t$ 中完整非线性方程恰为')
R += eq(r'A_t=-A_{XX}-(uA)_X,\qquad B_t=B_{XX}-(uB)_X,\qquad u=\frac12\int_0^z(A-B)\,ds,\quad z=y+2\in[0,4].')
R += p(r'本轮得到一个带显式常数的混合问题存在性证明稿，并完成独立推导复核。在解析 Fourier 范数 $\|f\|_\rho=\sum_n e^{\rho|\xi_n|}\sup_{z,t}|f_n(z,t)|$ 中，指定 $G=A(T)$ 与 $H=B(0)$。若 $\|G\|_\rho+\|H\|_\rho\le0.3$，则 $T=0.01$ 时映射将半径 $0.4$ 的球映入半径 $0.322628$ 的球，压缩因子小于 $0.113138$。这给出了该初末值混合问题的唯一小解。')
R += p(r'要得到我们指定的独立初值，还必须找到终端函数 $G$，使混合解满足 $F_H(G)=A_G(0)=A_0^\varepsilon$。这就是当前尚未闭合的匹配方程。实际非零背景的导数包含速度变化项 $\delta u\,\bar A$、$\delta u\,\bar B$；本轮已完整保留这些项，推导出条件性的解析平滑估计，并计算了当前正弦背景的首阶侧频耦合。它们表明逆算子必须处理不同 Fourier 模态之间的耦合。')
R += p(r'进一步地，已经算出独立初值对应的第一个背景匹配修正。对于当前高斯振幅 $0.05$、扰动振幅 $10^{-6}$，在 $\rho=0.1$ 的解析范数中，将这一项截断至 $|n|\le128$ 后，独立 $u$、$v$ 扰动的 Fourier 尾界分别小于 $7.563\times10^{-79}$、$1.183\times10^{-78}$。公式、振幅因子及尾部求和已独立复核。这两个数只控制首次修正的截断误差；全部高阶修正的总界仍是下一步需要证明的部分。')
R += p(r'常背景可以直接量化匹配所需的精度。若只看一条不稳定 $A$ 模态，终态容差取 $10^{-10}$，则初始系数误差必须不超过 $10^{-10}e^{-TK^2}$。下面采用 $T=0.01$、$K=\pi/\Delta x$。这些是常背景线性公式的数值尺度。')
R += '<div class="table-wrap"><table><caption>表 3. 常背景线性匹配的精度尺度。</caption><thead><tr><th>Δx</th><th>终态放大 e<sup>TK²</sup></th><th>允许的初始 A 模态误差</th></tr></thead><tbody><tr><td>0.1</td><td>1.9334 × 10⁴</td><td>5.1723 × 10⁻¹⁵</td></tr><tr><td>0.05</td><td>1.3972 × 10¹⁷</td><td>7.1572 × 10⁻²⁸</td></tr><tr><td>0.025</td><td>3.8110 × 10⁶⁸</td><td>2.6240 × 10⁻⁷⁹</td></tr></tbody></table></div>'
R += p(r'因此，参考解的下一步需要对非零背景匹配算子的逆及无限 Fourier 尾部给出共同界，验证一个包含完整初值的误差球。当前尚无满足条件的误差球，也没有四组独立扰动的 $\eta_u,\eta_v$。孤子还需要同时控制全直线初值与有限计算区间之间的误差。')
R += p(r'加密诊断也反映了这一困难：此前单孤子试验取 $\Delta x=0.05$、$\Delta t=2.5\times10^{-5}$，在 $t=0.007525$ 停止，未扰动背景相对已知精确解的内部最大误差已约为 $(20.15,5.11)$。这条记录说明该次双精度加密计算已失准；其初始载波为 $2\pi/5$，与上面的统一实验分开保存。')
R += '</section><section id="sources"><h2>4. 证明与数据</h2><ul>'
for label, path in [
    ('常背景与现行闭合的独立核验', 'AUDIT_DESIGN.md'),
    ('混合问题与独立初值匹配', 'certificate_design/INDEPENDENT_PERTURBATIONS.md'),
    ('非零背景匹配导数与尾部条件', 'certificate_design/NONZERO_MATCHING_DERIVATIVE.md'),
    ('四个算例的协议与数据入口', 'perturbation_pilot/README.md'),
    ('独立核验数据', 'audit_four_case.json')]:
    R += '<li><a href="../Workspaces/dlw_paper_20261009/stability_20261026/' + path + '">' + label + '</a></li>'
R += '</ul><p><a href="../dlw-paper.html#section-6.1">主论文 §6.1</a> · <a href="../dlw-paper.html#section-6.2">主论文 §6.2</a></p></section>'
R = '''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DLW 独立扰动与连续误差认证</title><link rel="stylesheet" href="../Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.min.css"><style>
body{max-width:1000px;margin:48px auto;padding:0 26px;color:#222;background:#fff;font:17px/1.85 Georgia,"Times New Roman","Microsoft YaHei",serif}h1{font-size:30px;line-height:1.4}h2{font-size:24px;margin-top:42px}a{color:#245c7b}nav{border-block:1px solid #ccc;padding:12px 0;display:flex;gap:24px;flex-wrap:wrap}.eyebrow{font-size:14px;color:#666}.equation,.table-wrap{overflow-x:auto;margin:24px 0}table{border-collapse:collapse;width:100%;border-top:2px solid #222;border-bottom:2px solid #222;font-size:15px;line-height:1.6;font-variant-numeric:tabular-nums}caption{text-align:left;padding-bottom:12px}thead{border-bottom:1px solid #222}th,td{padding:10px;text-align:right}th:first-child{text-align:left}figure{margin:32px 0}figure img{display:block;width:100%;max-width:850px;margin:auto}figcaption{font-size:14px;line-height:1.65;color:#444;margin-top:16px}@media(max-width:650px){body{margin-top:24px;padding:0 16px;font-size:16px}h1{font-size:25px}table{font-size:13px}th,td{padding:8px 6px}}@media print{nav{display:none}body{max-width:none;margin:0}tr{break-inside:avoid}}
</style></head><body>''' + R + '</body></html>'

S44, S55, R = render_all([S44, S55, R])
(HERE / 'section44.html').write_text(S44, encoding='utf-8')
(HERE / 'section55.html').write_text(S55, encoding='utf-8')
REPORT.write_text(R, encoding='utf-8')

if '--report-only' in sys.argv:
    print('Report and section source fragments refreshed; main paper unchanged.')
    raise SystemExit(0)

before = PAPER.read_bytes()
source = before.decode('utf-8')
for ident in ('section-4.4', 'section-5.5'):
    old = re.search(r'<section id="' + re.escape(ident) + r'">.*?</section>', source, re.S)
    assert old and 'Editorial guide:' in old[0], 'Target already edited; review before republishing.'
backup = HERE / ('before_' + datetime.now().strftime('%Y%m%d_%H%M%S'))
backup.mkdir()
(backup / 'dlw-paper.html').write_bytes(before)
source = re.sub(r'<section id="section-4\.4">.*?</section>', lambda _: S44, source, count=1, flags=re.S)
source = re.sub(r'<section id="section-5\.5">.*?</section>', lambda _: S55, source, count=1, flags=re.S)
source = source.replace('5.5 Nonexact initial data and stability diagnostics', '5.5 Independent physical-field perturbations')
source = source.replace('Table 6. Control runs for Section 5.', 'Table 7. Control runs for Section 5.')
source = source.replace('couples its node motion to the field evolution.</p>',
                        'couples its node motion to the field evolution. Section 4.4 derives the constant-background linear response under the fixed-grid boundary closure.</p>', 1)
source = source.replace('Finally, Section 5.4 examines', 'Section 5.4 examines', 1)
# Add to the direct Section 5 overview without replacing any existing mathematical markup.
old5 = re.search(r'(<section[^>]*id="section-5"[^>]*>.*?<p>)(.*?)(</p>)', source, re.S)
assert old5
newp = old5[0][:-4] + ' Section 5.5 measures the response to independent perturbations of the initial physical fields and relates the results to the linearized closure.</p>'
source = source[:old5.start()] + newp + source[old5.end():]
source = source.replace('and the conservation-based moving mesh. Section 5 presents',
                        'the conservation-based moving mesh, and the constant-background linearized evolution. Section 5 presents', 1)
assert PAPER.read_bytes() == before, 'Paper changed concurrently; do not overwrite.'
PAPER.write_text(source, encoding='utf-8')

old_soup, new_soup = BeautifulSoup(before, 'html.parser'), BeautifulSoup(source, 'html.parser')
changed = [s.get('id') for s in new_soup.find_all('section') if str(s) != str(old_soup.find('section', id=s.get('id')))]
allowed = {'section-1','section-4','section-4.4','section-5','section-5.5','appendix-D'}
assert set(changed) <= allowed, changed
assert len(new_soup.find_all('figure')) == len(old_soup.find_all('figure')) + 1 == 29
assert len(new_soup.find_all('table')) == len(old_soup.find_all('table')) + 1 == 7
assert not new_soup.select('.katex-error')
for ident in ('abstract','section-4.2','section-4.3','section-5.2','section-5.3','section-5.4','section-6'):
    assert str(old_soup.find('section',id=ident)) == str(new_soup.find('section',id=ident)), ident
for fig in old_soup.find_all('figure'):
    assert str(fig) == str(new_soup.find('figure',id=fig.get('id')))
manifest = dict(date='2026-10-26', before_sha256=hashlib.sha256(before).hexdigest(),
                after_sha256=hashlib.sha256(PAPER.read_bytes()).hexdigest(), backup=str(backup),
                changed_sections=changed, figures=29, tables=7, rendered_formulas=len(MATH),
                continuous_perturbed_reference_certified=False, eta_u=None, eta_v=None,
                report=str(REPORT), numerical_cases=[x['case'] for x in AUDIT['records']])
(HERE / 'publication_validation.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
print(json.dumps(manifest, indent=2))
