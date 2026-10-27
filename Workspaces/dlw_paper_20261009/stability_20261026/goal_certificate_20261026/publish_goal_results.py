"""Publish precise certification results without changing the manuscript."""
from pathlib import Path
from datetime import datetime
import hashlib
import html
import json
import re
import subprocess
from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PAPER = ROOT / 'dlw-paper.html'
REPORT = ROOT / 'report/dlw_reference_goal_20261026.html'
paper_hash = hashlib.sha256(PAPER.read_bytes()).hexdigest()
maths = []
def m(tex, display=False):
    i = len(maths)
    maths.append(dict(tex=tex, display=display))
    return f'GOALMATH{i}END'
def prose(text):
    parts = text.split('$')
    assert len(parts) % 2 == 1
    return ''.join(m(x) if i%2 else x for i,x in enumerate(parts))
def p(text): return '<p>'+prose(text)+'</p>'
def eq(tex): return '<div class="equation">'+m(tex, True)+'</div>'
def heading(id_, title): return '<h2 id="'+id_+'">'+title+'</h2>'
def link(filename, label):
    return '<a href="../Workspaces/dlw_paper_20261009/stability_20261026/goal_certificate_20261026/'+filename+'">'+label+'</a>'

body = '<header><p class="date">DLW · 2026年10月26日</p><h1>高频增长与连续参考解的误差保证</h1>'
body += p(r'目标是在当前独立扰动初始 $u,v$ 的问题中，给出连续参考解及可核验误差界，或者证明高频增长阻碍了哪一类误差保证。精度可以放宽；初值、边界、解类和保证范围必须明确。')
body += p(r'已有全非线性残差认证与初值邻域的不可能性定理。最新结果进一步针对实际高斯背景和实际单频独立扰动方向：连续物理场的最大范数响应不能具有统一的 $O(\varepsilon^\gamma)$ 保证，若 $\gamma>1/2$。固定的非零扰动是否仍能获得专门参考和更弱误差保证，继续作为目标推进。')
body += '</header><nav><a href="#problem">问题</a><a href="#residual">残差认证</a><a href="#parameters">明确参数</a><a href="#initial">初值邻域</a><a href="#remaining">固定初值</a><a href="#carrier">实际单频方向</a><a href="#construction">构造路线</a><a href="#positive">正向归约</a><a href="#evidence">核验</a></nav>'

body += heading('problem', '1. 连续问题与要求')
body += p(r'现行实验包括一孤子、双孤子、高斯和正弦四个背景，分别独立扰动 $u_0$ 或 $v_0$。原实验使用 $\varepsilon=10^{-6}$、$\kappa=\pi/2$，考察 $0\le t\le T=0.01$。此处讨论连续方程的物理场误差。')
body += p(r'用随动坐标 $X=x-4t$ 和横向变量 $z$，完整非线性物理方程的残差为')
body += eq(r'\mathcal R_1=u_{zt}+v_{XX}+\partial_X(uu_z),\qquad \mathcal R_2=v_t+u_{XXz}+\partial_X(uv-4u).')
body += p(r'目标误差是连续观测区域上的最大值。高斯、正弦当前取 $X$ 周期192、$z\in[0,4]$、下边界 $u(X,0,t)=0$。一般背景定理允许孤子的非零下边界迹。')

body += heading('residual', '2. 全非线性定理：任意小残差仍容许任意大误差')
body += p(r'<strong>定理。</strong> 固定一个满足所列正则性条件的连续精确目标 $(U,V)$，给定任意有限批采样、任意残差预算 $r>0$ 和任意数 $M>0$。若不额外限制近似场的幅值、导数或无限频率尾部，就能构造近似场 $(u_a,v_a)$，完全保持目标的初值、边界与指定采样值，同时满足')
body += eq(r'\max_{i=1,2}\|\mathcal R_i(u_a,v_a)\|_{L^\infty(\text{全时空柱})}<r,\qquad \|v_a(T)-V(T)\|_{L^\infty(\text{内部观测区})}=M.')
body += p(r'因此，仅以精确初边值、普通残差预算和有限采样作为依据，容许的最大误差上确界为无穷大。若已知候选幅值有统一上限，仍可证明误差不能随残差趋零；此时不能排除平凡的有限界。')
body += p(r'反例也可以使用在所有变量中均为整函数的近似场，并精确保持任意指定有限阶的节点与初始导数检查。逐个候选解析仍不够；能够排除反例的是已经证明的统一解析范数或无限尾界。'+link('ANALYTIC_CANDIDATE_EXTENSION.md', '解析候选扩展'))
body += p(r'一般背景证明只要求相关背景量有界，以及固定横向切片上的标量正向抛物问题有通常的正时间平滑核。一个充分条件是背景在 $X,t$ 方向光滑，$U_z,U_{Xz},V,V_X$ 在闭时空柱上有界。对当前四个受扰目标，此结论适用于满足这些条件的解，若它存在。')
body += '<details><summary>证明的主要步骤与量词</summary>'
body += p(r'在避开所有采样横向坐标的内部窄条中，取 $\delta v=\partial_z\delta u$。令高频终端余弦沿冻结横向层的背景输运反向演化。反向时间中的标量方程是普通正向抛物方程，因此它在早期时段的幅值 $\alpha_n$ 趋于零。时间截断保持完整初值；窄条宽度 $\delta$ 控制背景差异及全部二次项。')
body += eq(r'\max_i\|\Delta\mathcal R_i\|_\infty\le MH\alpha_n+\frac{M\delta}{2}K_n(M).')
body += p(r'先选有限高频 $n$ 使第一项小于 $r/2$，再选正宽度 $\delta<\min\{d_J,r/[M(1+K_n(M))]\}$，第二项也小于 $r/2$。这一步保留完整二次非线性项。条带支撑避开所有有限采样点，终态高度则精确等于 $M$。')
body += p(link('INDEPENDENT_NO_GO_AUDIT.md', '完整证明与独立审计'))+'</details>'

body += heading('parameters', '3. 无需未知解假设的明确参数例子')
body += p(r'取连续精确目标 $(U,V)=(0,4)$，$T=0.01$、周期192。这个实例直接验证完整非线性机制。一般背景定理再将同一机制推广到当前受扰目标。')
body += eq(r'F(s)=\frac{25\sqrt5}{3}s^3(1-s)^3,\quad f=F^{\prime},\quad \|f\|_\infty=1,\quad C=\|Ff\|_\infty=\frac{9765625\sqrt{11}}{170069856}<0.190445.')
body += p(r'将 $F,f$ 在 $[0,1]$ 外置零。取 $k=\pi n/96$、$q=e^{-k^2T}$、$\delta=q$，并把横向条带放入内部观测区。定义')
body += eq(r'h(t)=\frac{e^{k^2t}-1}{e^{k^2T}-1},\qquad u_a=M\delta F\!\left(\frac{z-z_*}{\delta}\right)h(t)\cos(kX),\qquad v_a=4+\partial_z u_a.')
body += p(r'初值严格为 $(0,4)$，终态 $v$ 误差严格为 $M$。完整物理残差满足显式界')
body += eq(r'\max_i\|\mathcal R_i\|_\infty\le e^{-k^2T}\left[\frac{Mk^2}{1-e^{-k^2T}}+M^2kC\right].')
body += '<div class="table-wrap"><table><caption>256-bit区间算术核验；显示的残差数值均向上放宽</caption><thead><tr><th>终态误差 '+m('M')+'</th><th>周期指标 '+m('n')+'</th><th>波数 '+m('k')+'</th><th>条带宽度 '+m(r'\delta')+'</th><th>全域残差上界</th></tr></thead><tbody>'
records = json.loads((HERE/'quantitative_constant_background.json').read_text(encoding='utf-8'))
display = [('10^{-6}',1417,'46.3712',r'4.586\times10^{-10}',r'9.861\times10^{-13}'),
           ('10^{-6}',2446,'80.0452',r'1.492\times10^{-28}',r'9.560\times10^{-31}'),
           ('1',1829,'59.8539',r'2.764\times10^{-16}',r'9.932\times10^{-13}'),
           ('1',2700,'88.3573',r'1.244\times10^{-34}',r'9.728\times10^{-31}')]
for row in display:
    body += '<tr>'+''.join('<td>'+m(str(x))+'</td>' for x in row)+'</tr>'
body += '</tbody></table></div>'
body += p(r'高频使反向热演化的强迫残差指数缩小；横向窄条使二次非线性残差也缩小。最大范数仍能看到窄条的完整高度。上述两个作用共同产生了表中的差距。')
body += p(link('QUANTITATIVE_CONSTANT_BACKGROUND.md', '显式构造与推导')+' · '+link('quantitative_constant_background.json', '区间参数证书'))

body += heading('initial', '4. 保留当前包络的初值邻域也存在障碍')
body += p(r'这一结论直接涉及当前高斯、正弦及其独立扰动初值。保持 $\phi(z)=\sin^2(\alpha z)$、$\alpha=\pi/4$，只把一个物理场的初值再改变任意小的 $-\eta\phi(z)H_\rho(X)$，另一场保持原样，其中')
body += eq(r'H_\rho(X)=\sum_{n\ge1}e^{-\rho n}\cos(ndX),\qquad d=\pi/96,\quad\rho>0.')
body += p(r'这个初始函数是解析的。减小 $|\eta|$，可以使它在任意固定有限阶光滑范数中任意小；对任何给定有限解析条带宽度 $s$，选择 $\rho>ds$，它在该解析范数中也任意小。横向包络和初始端点值保持不变。')
body += p(r'令 $A=u_z+v-4$、$B=v-u_z-4$，记归一化边界导数 $a_j=\partial_z^jA(X,0,t)/j!$。两个假设解的低阶边界方程逐层相减，所有背景非线性强迫精确抵消。首次变化的边界导数满足反向热方程：')
body += eq(r'[\delta a_1(t)]_{nd}=-\eta\alpha^2e^{td^2n^2-\rho n}\quad(u\text{ 独立改变}),\qquad [\delta a_2(t)]_{nd}=-\frac{\eta\alpha^2}{2}e^{td^2n^2-\rho n}\quad(v\text{ 独立改变}).')
body += p(r'任意正时间，上述系数增长快于所有多项式，不能成为周期分布的 Fourier 系数。因此，一个容许此类初值不确定性的正半径邻域，无法统一保证具有这些有限阶经典边界导数的解存在，也就无法统一保证到该解的误差。$u$ 独立改变只需涉及 $u$ 的二阶、$v$ 的一阶横向导数；$v$ 独立改变涉及三阶和二阶导数，并需所列时间与 $X$ 正则性。')
body += p(r'还可以把 $H_\rho$ 乘以在所有给定初始 $X$ 采样点为零的三角多项式，得到完全相同有限网格初值的邻近函数。其高频尾部仍为非零常数乘 $e^{-\rho n}$，上述矛盾保持成立。从已知未扰动高斯、正弦连续解出发，这就给出了明确的同包络独立扰动无解例子；所排除的仍是这里明确列出的有限边界正则性解类。')
body += p(r'这个定理并未把当前精确单频初值换成别的参考问题。它说明：即使初始函数在普通光滑或解析条带范数中已知得任意准确，只要无限高频尾部仍有这种不确定性，就不能保证整个不确定性集合都有光滑连续参考。对精确指定的单频函数，仍需单独判断。')
body += p(link('ROBUST_SAME_ENVELOPE.md', '同包络有限阶边界证明')+' · '+link('robust_same_envelope_check.json', '精确符号核验'))

body += heading('remaining', '5. 精确单频初值的参考目前做到哪里')
body += p(r'未扰动的孤子与当前高斯、正弦基准已有连续精确表示和相应求值依据。独立扰动之后，已经证明一个小数据混合时间问题可解：一个变换分量在初时给定，另一个在终时给定。在 $T=0.01$ 的既定小球条件下，收缩常数小于 $0.113138$。')
body += p(r'原问题同时指定两个初始物理场，还必须解出完整的初值匹配方程。其非零背景导数、首个修正和部分尾项已有推导；无限尾部与全部高阶余项尚未闭合。放宽所需误差精度，并不会自动补上存在性和尾部控制。')
body += p(r'针对当前精确受扰正弦数据，还能得到定量必要条件。若解具有所有所列边界导数，记 $M_j(t)$ 为两个物理场第 $j$ 阶横向边界导数的最大值，则')
body += eq(r'\limsup_{j\to\infty}\frac{\log(1+M_j(t))}{j^2}\ge\begin{cases}\kappa^2t/4,&u\text{ 独立扰动},\\\kappa^2t/9,&v\text{ 独立扰动}.\end{cases}')
body += p(r'所以全部有限阶横向 Gevrey 类均被排除。任意光滑函数仍可能具有更快增长的导数；该必要条件没有证明一般光滑解不存在。')
body += p(r'当前目标继续保持进行中：需要为精确给定的独立扰动初值，构造带完整尾界的参考，或者在明确、足够适用的解类中证明其不可认证或不存在。现阶段已严格关闭普通残差与有限采样认证路线，以及普通初值不确定性球上的统一光滑认证路线。')
body += p(link('ACTUAL_IVP_CLASS_BOUNDARY.md', '实际单频初值的正则性界与剩余解类'))

body += heading('carrier', '6. 实际高斯单频扰动：最大范数中的稳定性障碍')
body += p(r'这一结果保持当前高斯背景及实验扰动，不加入额外高频噪声。周期为192，$z\in[0,4]$、下边界 $u=0$，背景初值为 $u_b=0.05\sin(\pi z/4)F_0(X)$、$v_b=4-3u_{b,z}$，$F_0$ 是当前周期高斯。分别只给 $u_0$ 或 $v_0$ 加上 $\varepsilon\sin^2(\pi z/4)\cos(\pi X/2)$。')
body += p(r'<strong>最大范数定理。</strong> 任取共同正时间区间 $[0,T]$。不存在覆盖所有充分小振幅的经典连续解族，能对某个固定 $\gamma>1/2$ 满足')
body += eq(r'\|u^\varepsilon-u^b\|_{L^\infty(\mathbb T_{192}\times[0,4]\times[0,T])}+\|v^\varepsilon-v^b\|_{L^\infty(\mathbb T_{192}\times[0,4]\times[0,T])}\le C|\varepsilon|^\gamma,')
body += p(r'其中常数 $C$ 与振幅无关。特别地，沿任何趋零振幅序列也不可能有统一的 $O(\varepsilon)$ 最大响应界。这个结论只对未求导的物理场最大范数提出假设，不需要预先控制受扰解的高阶横向导数。')
body += p(r'证明把所选方向的变分经精确缺陷恒等式、规范变换和 Bloch 提升，转成自由后向热方程。正时间分布解要求初始提升具有 Gaussian Fourier 尾。然而实际高斯初值给出')
body += eq(r'F_0h_0^{\prime}-F_0^{\prime}h_0=e^{s(z)J_0(X)}\bigl[a(z)F_0^2\cos(\kappa X)-b(z)(F_0(\cos\kappa X)^{\prime}-F_0^{\prime}\cos\kappa X)\bigr],\qquad s(z)=0.025\sin(\pi z/4).')
body += p(r'右端的复变量增长超过该热方程容许的二阶整函数增长。对 $O(\varepsilon^\gamma)$ 假设，归一化后的二次余项为 $O(\varepsilon^{2\gamma-1})$；逐模选择振幅，仍迫使同一个初值具有 Gaussian 尾，从而矛盾。')
body += p(r'这说明不能把当前有限网格下近似线性的响应，直接解释为一个对分辨率一致有效的连续线性稳定性估计。对精确 Fourier–Galerkin 的一阶变分，还能证明物理场响应随频率截断不可能一致有界。该 Galerkin 推论保持 $z$ 连续，并使用精确背景；对具体 Centered-SD 全离散格式需要另外的相容性论证。')
body += p(r'本定理尚未排除 $\gamma\le1/2$ 的响应，也未证明孤立振幅 $\varepsilon=10^{-6}$ 的解不存在。因此固定初值的参考误差 $\eta_u,\eta_v$ 仍未取得。')
body += p(link('fixed_data_continuation/GAUSSIAN_LINF_HOLDER_OBSTRUCTION.md', '最大范数与 Hölder 障碍证明')+' · '+link('fixed_data_continuation/GAUSSIAN_COMPLEX_GROWTH_LEMMA.md', '实际高斯复增长引理')+' · '+link('fixed_data_continuation/GAUSSIAN_LINEARIZED_AUDIT.md', '独立变换审计'))

body += heading('construction', '7. 有限标准 Darboux 构造的范围已明确')
body += p(r'当前四个独立受扰初值不仅不能通过既有有限 Laplace 链构造，也不能从 $P=0$ 或 $P=Q_z$ 的可分解热方程种子，经过有限个局部正则的标准两类 Darboux 变换构造出来。具有正则基本分解的有限 Wronskian 公式也在此范围内。')
body += p(r'有限变换保留一个有限阶的任意函数解族；沿合适方向的 Laplace 步逐次降低其阶数，最终必须出现零不变量，与四组实际初值的不终止性矛盾。无限 dressing、尚未分解的一般积分型 binary 变换，以及奇异或合流极限仍需分别研究。')
body += p(link('fixed_data_continuation/FINITE_DARBOUX_TERMINATION.md', '全阶证明')+' · '+link('fixed_data_continuation/FINITE_DARBOUX_AUDIT.md', '独立审计'))

body += heading('positive', '8. 正向路线：延长时间后做有界近似匹配')
body += p(r'另一个构造性归约使用 $S=0.02>T=0.01$。若能在较长区间构造精确的连续混合解序列，使稳定分量的初值始终准确、另一分量的初值误差趋零，并证明所有轨道处于同一个解析 $X$ 范数球，那么条件稳定性估计会使它们在较短区间上成为 Cauchy 序列。这样可以构造真实初值解，而无需先证明整个无限尾部匹配映射具有有界逆。')
body += p(r'取解析半宽 $\rho=0.1$、轨道球半径 $R=0.4$ 时，已算出明确的条件估计常数。它们比较的是两个已经存在且满足统一范数界的连续混合解。实际数据的统一有界匹配序列尚未验证；$v$ 的最大范数收敛还需有限横向正则性或直接一致收敛控制。')
body += p(r'不能仅由“初值依赖解析、混合映射解析、已有条件 Hölder 估计”推断解的横向依赖也属于有限 Gevrey 类。已经构造一个二次解析、Gaussian 平滑、导数单射的抽象反例，表明这条推理缺少条件。它用于检查证明逻辑，不代替 DLW 的分析。')
body += p(link('fixed_data_continuation/TIME_PADDING_MATCHING_REDUCTION.md', '有界匹配序列的正向归约')+' · '+link('fixed_data_continuation/time_padding_constants.json', '条件常数的区间核验')+' · '+link('fixed_data_continuation/QUADRATIC_PARAMETER_BRIDGE_COUNTEREXAMPLE.md', '解析参数推理的反例'))

body += heading('evidence', '9. 核验与入口')
body += p(r'全非线性相减恒等式与输运抵消经过独立符号检查；明确参数使用256-bit区间算术核验；同包络初值定理的首次边界系数与非线性强迫抵消也已符号检查。证明以解析推导及独立复核的证明稿形式保存，尚未形式化验证。')
body += p(link('INDEPENDENT_NO_GO_AUDIT.md', '独立数学审计')+' · '+link('no_go_algebra_audit.json', '残差恒等式核验')+' · '+link('quantitative_constant_background.json', '明确参数核验'))
body += '<p><a href="dlw_reference_certification_20261026.html">前轮高阶认证分析</a> · <a href="dlw_independent_stability_20261026.html">扰动响应实验</a> · <a href="../dlw-paper.html#section-6">主论文 Section 6</a></p>'

js = "const fs=require('fs'),k=require(process.argv[1]);process.stdout.write(JSON.stringify(JSON.parse(fs.readFileSync(0,'utf8')).map(x=>k.renderToString(x.tex,{displayMode:x.display,throwOnError:true,strict:'error'}))));"
rendered = subprocess.run(['node','-e',js,str(ROOT/'Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.js')], input=json.dumps(maths),text=True,encoding='utf-8',capture_output=True,check=True)
formulas=json.loads(rendered.stdout)
body=re.sub(r'GOALMATH(\d+)END',lambda match:formulas[int(match[1])],body)
style='''body{max-width:1000px;margin:48px auto;padding:0 26px;font:17px/1.85 Georgia,"Times New Roman","Microsoft YaHei",serif;color:#222;background:#fff}h1{font-size:31px;line-height:1.4}h2{font-size:24px;margin-top:44px;line-height:1.5}.date{color:#666;font-size:14px}nav{display:flex;gap:22px;flex-wrap:wrap;border-block:1px solid #ccc;padding:12px 0}a{color:#245c7b}.equation{overflow-x:auto;margin:22px 0}.table-wrap{overflow-x:auto}table{border-collapse:collapse;width:100%;margin:25px 0;border-top:2px solid #333;border-bottom:2px solid #333;font-size:15px}th,td{padding:10px 12px;text-align:center;white-space:nowrap}thead{border-bottom:1px solid #555}caption{text-align:left;margin-bottom:12px;color:#555;font-size:14px}details{border-top:1px solid #ddd;padding-top:14px;margin:28px 0}summary{cursor:pointer}@media(max-width:650px){body{padding:0 16px;margin-top:24px;font-size:16px}h1{font-size:25px}h2{font-size:21px}}@media print{nav{display:none}body{max-width:none;margin:0}}'''
document='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DLW 高频增长与参考解误差保证</title><link rel="stylesheet" href="../Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.min.css"><style>'+style+'</style></head><body>'+body+'</body></html>'
soup=BeautifulSoup(document,'html.parser')
assert not soup.select('.katex-error')
missing=[]
for tag in soup.find_all(['a','link'],href=True):
    url=tag['href']
    if url.startswith('#'):
        if soup.find(id=url[1:]) is None:missing.append(url)
    elif not re.match(r'https?://',url):
        path=url.split('#',1)[0]
        if path and not (REPORT.parent/path).resolve().exists():missing.append(url)
assert not missing, missing
if REPORT.exists():
    stamp=datetime.now().strftime('%Y%m%d_%H%M%S')
    (HERE/('report_before_'+stamp+'.html')).write_bytes(REPORT.read_bytes())
REPORT.write_bytes(document.encode('utf-8'))
assert hashlib.sha256(PAPER.read_bytes()).hexdigest()==paper_hash
status=dict(date='2026-10-26',goal_status='active',continuous_independent_reference_certified=False,eta_u=None,eta_v=None,
            attained=['full nonlinear no-finite-uniform-residual-bound theorem under explicit information model',
                      'same-envelope analytic initial-neighborhood obstruction with finite boundary jets',
                      'quantitative actual-sine transverse derivative lower bound',
                      'actual Gaussian pure-carrier no-Lipschitz and no uniform Holder response with exponent greater than 1/2 in physical L-infinity',
                      'finite regular standard Darboux construction obstruction for all four actual data',
                      'conditional constructive time-padding reduction; uniform actual-data matching sequence not verified'],
            open='exact fixed pure-carrier perturbed IVP and a structural/tail-aware certificate or stronger actual-data nonexistence theorem',
            full_unconditional_impossibility_proved=False,report=str(REPORT),main_paper_unchanged_sha256=paper_hash,
            mathematical_status='independently reasoned/reviewed proof drafts plus exact symbolic checks and interval constants; not formal verification',
            formulas=len(maths),katex_errors=0,missing_links=[])
(HERE/'STATUS.json').write_text(json.dumps(status,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(status,ensure_ascii=False,indent=2))
