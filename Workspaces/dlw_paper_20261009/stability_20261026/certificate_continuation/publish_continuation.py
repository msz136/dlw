"""Record the new continuum-certification obstructions without assigning an eta."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import re
import subprocess
from bs4 import BeautifulSoup

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
PAPER=ROOT/'dlw-paper.html'
REPORT=ROOT/'report/dlw_reference_certification_20261026.html'
before=PAPER.read_bytes()
src=before.decode('utf-8')
old=re.search(r'<section id="section-6\.3">.*?</section>',src,re.S)
assert old and 'Transverse regularity of the perturbed sine data' not in old[0]
maths=[]
def m(t,display=False):
    token=f'CCMATH{len(maths)}END';maths.append(dict(tex=t,display=display));return token
def text(t):
    parts=t.split('$');assert len(parts)%2==1
    return ''.join(m(x) if i%2 else x for i,x in enumerate(parts))
def p(t):return '<p>'+text(t)+'</p>\n'
def eq(t):return '<div class="equation">'+m(t,True)+'</div>\n'

addition='<h4>Transverse regularity of the perturbed sine data</h4>\n'
addition+=p(r'The initial matching problem also imposes a transverse regularity constraint. For the sinusoidal benchmark, write $\alpha=\pi/4$, $q=\pi/12$, and $\kappa=6q=\pi/2$. The background is $u_0=0.03\sin(\alpha z)\cos(qX)$, $v_0=4-3u_{0,z}$, and either initial field receives the independent perturbation $\varepsilon\sin^2(\alpha z)\cos(\kappa X)$ used in Section 6.2.')
addition+=p(r'<strong>Proposition.</strong> Suppose the perturbed periodic solution exists, every transverse boundary jet is continuously differentiable in time and twice continuously differentiable in $X$, and the mixed derivatives commute so that the equations hold after differentiation at $z=0$. For either independent perturbation with $\varepsilon\ne0$, the physical pair $(u,v)$ fails every finite-order transverse Gevrey bound at $z=0$ at each positive time. In particular, the pair cannot be analytic in $z$ at that boundary.')
addition+=p(r'To see this, set $a_j=\partial_z^jA(X,0,t)/j!$, $b_j=\partial_z^jB(X,0,t)/j!$. Assign each coefficient the weight $j+1$. The background starts at weight one and frequency $q$, while the $u$ and $v$ perturbations start at weights two and three, respectively, at frequency $6q$. Products in the boundary-jet equations add their weights. Consequently, the Fourier coefficient at $(j,\xi)=(2n-1,n\kappa)$ for $u$ input, or $(3n-1,n\kappa)$ for $v$ input, contains exactly $n$ perturbation factors and no background contribution.')
addition+=p(r'Put $r=2$ for $u$ input and $r=3$ for $v$ input, and write the selected coefficients as $[a_{rn-1}]_{n\kappa}=(-i\kappa)^{n-1}\varepsilon^n C_n$ and $[b_{rn-1}]_{n\kappa}=(-i\kappa)^{n-1}\varepsilon^n D_n$. Their exact equations are')
addition+=eq(r'\begin{aligned}C_n^{\prime}&=n^2\kappa^2 C_n+n\sum_{p=1}^{n-1}\frac{C_p-D_p}{2rp}C_{n-p},\\D_n^{\prime}&=-n^2\kappa^2 D_n+n\sum_{p=1}^{n-1}\frac{C_p-D_p}{2rp}D_{n-p}.\end{aligned}')
addition+=p(r'The first coefficients start from $(C_1,D_1)=(\alpha^2,-\alpha^2)$ for $u$ input and $(\alpha^2/2,\alpha^2/2)$ for $v$ input; all higher selected coefficients initially vanish. The first case preserves $C_n\ge0\ge D_n$, and the second preserves $C_n\ge D_n\ge0$. Integrating the $p=1$ contribution over the first half of the time interval and retaining the homogeneous growth over the second half yields, for fixed $t>0$ and $\varepsilon\ne0$,')
addition+=eq(r'\log\left|[a_{rn-1}]_{n\kappa}\right|\ge\frac{\kappa^2t}{2}n^2+O(n).')
addition+=p(r'A finite-order Gevrey estimate $\|\partial_z^jA\|_\infty\le CR^j(j!)^s$, with finite $s\ge1$, permits only $O(n\log n)$ growth for the logarithm of these normalized coefficients. The quadratic lower bound gives the contradiction. A finite-order Gevrey bound for both physical fields would also give one for $A=u_z+v-4$. The argument uses actual boundary derivatives for a fixed perturbation, without assuming convergence of a perturbation-amplitude series.')
addition+=p(r'The proposition requires any sufficiently smooth reference for these sine data to include transverse behavior beyond every finite Gevrey class. The mixed problem above remains meaningful in a norm that controls continuity in $z$ without imposing such derivative bounds, but exact initial matching in that weaker class is still unresolved. A complete physical-field error certificate must establish that matching and bound the full unresolved tail. No such certificate has yet been obtained for the independently perturbed trajectories.')

last=r'<p>For the present Gaussian and sinusoidal data, the first coefficient of the matching correction.*?</p>'
matched=re.search(last,old[0],re.S);assert matched
new63=old[0][:matched.start()]+p(r'For the present Gaussian and sinusoidal data, the first coefficient of the matching correction in the background and perturbation amplitudes can be computed explicitly. Its Gaussian Fourier tail has a finite analytic bound. To extend this calculation to a complete reference, the behavior of all higher corrections must also be controlled. The following necessary condition shows why transverse regularity must be addressed in that construction.')+addition+'</section>'

R='<header><p class="eyebrow">DLW · 连续参考误差认证 · 2026-10-26</p><h1>独立扰动参考解：高阶分析与认证条件</h1></header>'
R+=p(r'<strong>当前还不能保证参考解足够精确。</strong> 独立扰动后的完整连续解尚未获得误差上界。本轮完成了高阶分析，证明两条此前考虑的构造路线存在具体障碍，并得到一条针对当前正弦初值的横向正则性结论。以下结果属于已交叉复核的证明稿；它们没有被当作完整参考解证书。')
R+='<nav><a href="#target">验收目标</a><a href="#sine">当前正弦数据</a><a href="#routes">另外两条路线</a><a href="#status">剩余问题</a></nav>'
R+='<section id="target"><h2>1. “足够好”需要一个完整的场误差界</h2>'
R+=p(r'参考对象是与扰动实验具有相同初始函数、边界数据和连续 DLW 方程的解。可操作的首轮目标取为在整个比较区域和 $0\le t\le0.01$ 上，两个物理场分别满足')
R+=eq(r'\|u_{\mathrm{ref}}-u\|_\infty\le\eta_u,\qquad\|v_{\mathrm{ref}}-v\|_\infty\le\eta_v,\qquad\eta_u,\eta_v\le10^{-10}.')
R+=p(r'该阈值约为当前最小终态跨场响应 $1.93\times10^{-8}$ 的 $0.52\%$。它是待验证的目标，不是已取得的结果。只要完整上界成立，数值误差与可计算参考误差之间的差就由同一个上界控制。首个修正的截断误差、有限网格的舍入误差以及网格间差值，都不能单独替代这个完整上界。')
R+='</section><section id="sine"><h2>2. 当前正弦初值的横向正则性约束</h2>'
R+=p(r'这里保留当前正弦背景的振幅 $0.03$、$x$ 波数 $q=\pi/12$，以及独立扰动 $\varepsilon\sin^2(\pi z/4)\cos(\pi X/2)$，其中 $z=y+2$、$\varepsilon=10^{-6}$。两个实验分别只改变初始 $u$ 或初始 $v$，下边界仍为 $u(X,0,t)=0$。')
R+=p(r'<strong>结论。</strong> 假设相应周期解存在，所有横向边界导数均可代入微分后的方程，并具有所需的时间、空间连续性。则在任何 $t>0$，物理场对 $(u,v)$ 都不满足下边界处的任何有限阶横向 Gevrey 界。这包含解析函数这一特例。')
R+=p(r'有限阶 Gevrey 界要求导数至多按 $CR^j(j!)^s$ 增长，其中 $s$ 是某个固定有限数。此处可以从原方程隔离出一列实际导数，其归一化 Fourier 系数的增长至少包含 $e^{c n^2t}$。它最终超过任何固定阶乘幂；结论对固定非零扰动成立，不依赖扰动振幅级数是否收敛。')
R+=eq(r'\left|\left[\frac{\partial_z^{rn-1}A(X,0,t)}{(rn-1)!}\right]_{n\kappa}\right|\ge K_1K_2^n n\,e^{n^2\kappa^2t/2},\quad r=2\ \text{或}\ 3,\quad\kappa=\pi/2,')
R+=p(r'这里 $A=u_z+v-4$，常数 $K_1,K_2>0$ 对固定 $t,\varepsilon$ 与 $n$ 无关。背景 Fourier 波数与横向阶数的组合，使这列系数只包含扰动因素；原来的非零正弦背景无法抵消它。')
R+=p(r'这排除了基于解析或有限阶 Gevrey 横向尾部的认证方法，但没有排除一般光滑解，也没有证明场值会在当前网格上变大。高阶导数的增长与有限时间内小幅物理场响应可以同时出现。高斯背景含有无限多个初始 Fourier 模式，不能直接套用这一频率隔离证明。')
R+='<details><summary>完整推导与复核</summary><p><a href="../Workspaces/dlw_paper_20261009/stability_20261026/certificate_continuation/audit_sine_jet_obstruction.md">实际正弦数据的边界导数证明</a>给出解类、精确递推、符号、阶乘及下界。两条独立推导一致，四个二阶递推残差均为零。</p></details></section>'
R+='<section id="routes"><h2>3. 首个修正与精确变换还缺什么</h2>'
R+=p(r'<strong>逐阶修正。</strong> 常背景下，只扰动 $u$ 或只扰动 $v$ 时，最高谐波都满足正递推。其第 $n$ 阶系数具有全阶下界 $\exp(n^2\kappa^2t-O(n\log n))$，所以对应振幅级数在任意正时间的收敛半径为零。600-bit 区间算术复算了下界；结论本身来自递推证明，而不是对几个数值系数的拟合。')
R+=p(r'这说明此前首次高斯匹配修正的尾界即使小于 $10^{-78}$，也不能证明剩余全部修正很小。该数值控制的是一个已知项的 Fourier 截断，未包含无限高阶修正。常背景级数发散本身仍不等于固定扰动初值无解。')
R+=p(r'<strong>原有热方程／Laplace 构造。</strong> 当前未扰动参考具有有限终止的 Laplace 链。独立扰动之后，初始不变量满足')
R+=eq(r'P_{j+2}=2P_{j+1}-P_j+\partial_{Xz}\log P_{j+1},\qquad P_0=\frac{v_0-4-u_{0,z}}4,\quad P_1=\frac{v_0-4+u_{0,z}}4.')
R+=p(r'扰动在复横向方向产生的主项，在每个整数指标 $j$ 上都不为零。因此，增加有限次同一种 Laplace 变换也不能回到已有热方程种子。该结论已覆盖高斯、正弦和当前 A/D 孤子初值；它限定于这条变换链，没有排除一般 dressing 或其他非终止表示。')
R+='<details><summary>构造路线的证明与计算</summary><ul><li><a href="../Workspaces/dlw_paper_20261009/stability_20261026/certificate_continuation/series_highest_harmonic.md">最高谐波与全阶增长</a></li><li><a href="../Workspaces/dlw_paper_20261009/stability_20261026/certificate_continuation/constructive_laplace_chain.md">Laplace 不变量与有限终止障碍</a></li><li><a href="../Workspaces/dlw_paper_20261009/stability_20261026/certificate_continuation/audit_soliton_laplace_extension.md">A/D 孤子扩展的独立核验</a></li></ul></details></section>'
R+='<section id="status"><h2>4. 连续参考仍需解决的部分</h2>'
R+=p(r'已有混合初末值问题的压缩定理仍然有效：它只要求横向连续性，不要求横向解析。现在需要在允许这种较弱横向正则性的空间中，证明终端数据 $G$ 能精确满足 $F_H(G)=A_0^\varepsilon$，再给出覆盖全部频率的误差界。对实际正弦数据，不能再把解析／Gevrey 横向尾部作为未验证的假设加入证明。')
R+=p(r'目前没有得到这样的匹配解或完整误差球。四组独立扰动的 $\eta_u,\eta_v$ 均保持未认证；现有八条计算轨道继续作为离散扰动响应使用。下一步的关键是较弱横向正则性下的存在性与匹配逆估计，单纯增加网格数或浮点精度不能补上这一步。')
R+=p('文献核查也没有给出可直接沿用的定理。<a href="https://fizmathim.com/pryamaya-i-obratnaya-zadachi-dlya-2-1-mernogo-nelineynogo-uravneniya-blp">Garagash 的学位论文摘要</a>在逆散射部分采用可解性假设，并讨论全平面快速衰减数据；这一框架没有直接覆盖当前周期条带初值。')
R+='<p><a href="../dlw-paper.html#section-6.3">主论文 §6.3</a> · <a href="dlw_independent_stability_20261026.html">扰动实验报告</a></p></section>'
R='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DLW 连续参考误差认证：高阶分析</title><link rel="stylesheet" href="../Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.min.css"><style>body{max-width:1000px;margin:48px auto;padding:0 26px;color:#222;background:white;font:17px/1.85 Georgia,"Times New Roman","Microsoft YaHei",serif}h1{font-size:30px;line-height:1.4}h2{font-size:24px;margin-top:40px}a{color:#245c7b}.eyebrow{font-size:14px;color:#666}nav{border-block:1px solid #ccc;padding:12px 0;display:flex;gap:24px;flex-wrap:wrap}.equation{overflow-x:auto;margin:24px 0}details{border-top:1px solid #ddd;margin:25px 0;padding-top:12px}summary{cursor:pointer}@media(max-width:650px){body{margin-top:24px;padding:0 16px;font-size:16px}h1{font-size:25px}}@media print{nav{display:none}body{max-width:none;margin:0}}</style></head><body>'''+R+'</body></html>'

js="const fs=require('fs'),k=require(process.argv[1]);process.stdout.write(JSON.stringify(JSON.parse(fs.readFileSync(0,'utf8')).map(x=>k.renderToString(x.tex,{displayMode:x.display,throwOnError:true,strict:'error'}))));"
out=subprocess.run(['node','-e',js,str(ROOT/'Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.js')],input=json.dumps(maths),text=True,encoding='utf-8',capture_output=True,check=True)
formulas=json.loads(out.stdout)
def render(t):return re.sub(r'CCMATH(\d+)END',lambda x:formulas[int(x[1])],t)
new63,R=render(new63),render(R)
REPORT.write_text(R,encoding='utf-8')
backup=HERE/('before_'+datetime.now().strftime('%Y%m%d_%H%M%S'));backup.mkdir()
(backup/'dlw-paper.html').write_bytes(before)
updated=src[:old.start()]+new63+src[old.end():]
assert PAPER.read_bytes()==before,'Concurrent manuscript edit; preserve and review.'
PAPER.write_text(updated,encoding='utf-8')
(HERE/'section63.html').write_text(new63,encoding='utf-8')
previous=HERE.parent/'section6.html'
previous.write_text(re.sub(r'<section id="section-6\.3">.*?</section>',lambda _:new63,previous.read_text(encoding='utf-8'),count=1,flags=re.S),encoding='utf-8')

soup=BeautifulSoup(updated,'html.parser');report_soup=BeautifulSoup(R,'html.parser')
assert not soup.select('.katex-error') and not report_soup.select('.katex-error')
assert updated.replace(new63,'')==src.replace(old[0],''),'Outside Section 6.3 changed.'
assert len(soup.find_all('figure'))==29 and len(soup.find_all('table'))==7
links=[]
for a in report_soup.find_all('a',href=True):
    href=a['href']
    if not href.startswith(('https:','#')):
        path=(REPORT.parent/href.split('#')[0]).resolve()
        if not path.exists():links.append(str(path))
assert not links,links
status=dict(date='2026-10-26',problem='independent u/v perturbations, full nonlinear continuous DLW',
    target_T=.01,target_field_error=1e-10,target_status='proposed acceptance threshold, not attained',
    certified=False,eta_u=None,eta_v=None,
    new_results=['actual sine: no finite-order Gevrey-y boundary estimate under explicit smooth-solution hypotheses',
                 'constant-state independent perturbation amplitude series has zero radius at positive time',
                 'specific finite heat/Laplace chain cannot terminate for all four perturbed data'],
    general_C_infinity_nonexistence_proved=False,
    open_problem='exact initial matching and full tail/inverse estimates in an admissible weaker transverse class',
    main_changed_sections=['section-6.3'],figures=29,tables=7,
    before_sha256=hashlib.sha256(before).hexdigest(),after_sha256=hashlib.sha256(PAPER.read_bytes()).hexdigest(),
    backup=str(backup),report=str(REPORT),katex_errors=0,missing_links=links)
(HERE/'STATUS.json').write_text(json.dumps(status,indent=2),encoding='utf-8')
print(json.dumps(status,indent=2))
