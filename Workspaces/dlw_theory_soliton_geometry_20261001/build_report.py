"""Build the standalone paper-style report from the frozen theory and checks."""
from pathlib import Path
import base64
import hashlib
import html
import json
import re
from fractions import Fraction

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
ASSETS = ROOT/'Workspaces/gsg_project/dlw_report/_assets/package/dist'


def main():
    validation = json.loads((HERE/'geometry_validation.json').read_text(encoding='utf-8'))
    quant = json.loads((HERE/'quantitative_bound.json').read_text(encoding='utf-8'))
    projection = validation['projection_integrals'][-1]
    rows = '\n'.join(
        f'<tr><td>{r["h"]:g}</td><td>{r["D"]:.8e}</td><td>{r["D_over_h2"]:.9f}</td>'
        f'<td>{r["remainder_over_h4"]:.9f}</td></tr>'
        for r in validation['finite_h_validation'])
    # The certificate supplies the public conservative lower bound as a decimal string.
    assert Fraction(quant['reported_strict_lower_bound']) > Fraction('0.00003166')
    lower = r'3.166\times10^{-5}'
    d = projection['pair']['d']
    du, dv = projection['u']['d'], projection['v']['d']
    source = r"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>DLW：精确孤子结构与二阶物理形变</title>
<meta name="description" content="单孤子完整谱与相位重标记后的不可去二阶形变：自然解析插值、局部距离定理、定量下界及共同初值的传播条件。">
<style>@@KATEX_CSS@@</style>
<style>
:root{color-scheme:light;--ink:#252a2f;--muted:#666c73;--line:#d7dce0;--accent:#244d66}
*{box-sizing:border-box}body{margin:0;background:#faf9f6;color:var(--ink);font-family:"Noto Serif SC","Source Han Serif SC","Songti SC","SimSun",serif;line-height:1.85}
main{max-width:930px;margin:58px auto 84px;padding:0 36px}header{padding-bottom:27px;border-bottom:1px solid var(--line)}
.eyebrow{font-family:system-ui,sans-serif;letter-spacing:.1em;color:var(--muted);font-size:12px;margin:0 0 15px}h1{font-weight:600;font-size:31px;line-height:1.45;margin:0 0 13px;letter-spacing:.01em}.subtitle{margin:0;color:var(--muted);font-size:15px}
h2{font-size:21px;font-weight:600;margin:38px 0 15px;line-height:1.5}p{margin:12px 0}a{color:var(--accent);text-decoration-thickness:1px;text-underline-offset:3px}
.abstract{margin-top:25px;font-size:16px}.eq{display:flex;align-items:center;gap:10px;margin:18px 0;padding:5px 0;min-width:0}.math{flex:1;min-width:0;overflow-x:auto;overflow-y:hidden;padding:3px 2px}.num{font-size:13px;color:var(--muted);flex:none;width:27px;text-align:right}.katex{font-size:1.05em}.katex-display{margin:.3em 0}
.theorem{border-left:3px solid #7b91a0;padding:2px 0 2px 19px;margin:20px 0}.label{font-weight:600}.small{font-size:14px;color:var(--muted)}.tablewrap{overflow-x:auto;margin:19px 0}table{border-collapse:collapse;width:100%;font-family:system-ui,sans-serif;font-size:13px;font-variant-numeric:tabular-nums}th,td{text-align:right;padding:10px 12px;border-bottom:1px solid var(--line);white-space:nowrap}th:first-child,td:first-child{text-align:left}th{font-weight:500;color:#464e55;border-top:1px solid #9ca5ae;background:#f0f1ef}
.references{font-size:14px;padding-left:22px}.references li{margin:8px 0}footer{border-top:1px solid var(--line);margin-top:34px;padding-top:14px;font-size:13px;color:var(--muted)}
@media(max-width:600px){main{margin:29px auto 45px;padding:0 20px}h1{font-size:25px}h2{font-size:19px}.abstract{font-size:15px}.eq{gap:4px}.num{width:23px}.katex{font-size:.98em}th,td{padding:9px 10px}}
@media print{body{background:white}main{margin:0;max-width:none}.math{overflow:visible}a{color:inherit}}
</style></head><body><main>
<header><p class="eyebrow">DLW · 理论问题 T03 · 2026年10月1日</p>
<h1>精确孤子结构仍留下二阶物理形变</h1>
<p class="subtitle">固定一孤子、物理重构与观测窗口；允许完整谱和相位重标记。</p></header>
<p class="abstract"><span class="label">摘要。</span>原 SD 精确保留的有限格距 Gram 孤子族，与连续物理孤子族具有不同的嵌入几何。本文证明：对任意固定正则单孤子，在任何有内点的有限矩形上，离散物理场到局部连续族的距离为 \(h^2d_\theta+O(h^4)\)，且 \(d_\theta&gt;0\)。完整谱、相位重标记仍不能吸收该二阶形变。证明来自复极点阶数，与有限采样拟合无关；另给显式积分下界和一个冻结定点验证。静态族距离与共同初值的演化误差须分别解释。</p>

<section id="objects"><h2>1　比较对象</h2>
<p>固定 \(a\in\mathbb R\)、\(N=1\)、\(\theta=(p,q,\varphi)\)，定义</p>
<div class="eq"><div class="math">\[P=p-a,\quad Q=q+a,\quad K=p+q&gt;0,\quad \Gamma=-P/Q&gt;0,\quad \ell=P^{-1}+Q^{-1}.\]</div><span class="num">(1)</span></div>
<p>这强制 \(PQ&lt;0\)、\(\ell=K/(PQ)&lt;0\)、\(\Gamma\ne1\)。取 \(0&lt;h&lt;2\min(|P|,|Q|)\)，并令 \(g=\log\Gamma\)、\(\omega=q^2-p^2\)、\(s(z)=(1+e^{-z})^{-1}\)、\(f(z)=s(z+g)\)。连续物理场为</p>
<div class="eq"><div class="math">\[z=Kx+\ell y+\omega t+\varphi,\qquad U_0=\binom{2K(f-s)}{2K\ell(f'+s')}.\]</div><span class="num">(2)</span></div>
<p>固定时刻和矩形 \(\Omega\)，采用等权物理双场 RMS：</p>
<div class="eq"><div class="math">\[\|U\|_H^2=\frac1{|\Omega|}\int_\Omega(u^2+v^2)\,dx\,dy.\]</div><span class="num">(3)</span></div>
<p>该窗口在拟合时保持不动。参数重标记只用于定义族距离，不表示更换共同物理初值。已有 Gram 精确性与中点重构见文末来源；下述完整参数障碍是本题的新证明。</p></section>

<section id="interpolation"><h2>2　精确有限格距族的自然插值</h2>
<p>物理位置为 \(y=(j+\tfrac12)h\)。直接延拓 Gram 指数，把离散与连续族放入同一函数空间：</p>
<div class="eq"><div class="math">\[\chi_h=\frac{P+h/2}{P-h/2}\frac{Q+h/2}{Q-h/2},\qquad \lambda_h=\frac{\log\chi_h}{h},\qquad \delta_h=\frac{h\lambda_h}{2}.\]</div><span class="num">(4)</span></div>
<div class="eq"><div class="math">\[\varepsilon_h=\frac12\log\frac{1-h^2/(4P^2)}{1-h^2/(4Q^2)},\qquad Z_h=Kx+\lambda_hy+\omega t+\varphi.\]</div><span class="num">(5)</span></div>
<div class="eq"><div class="math">\[\begin{aligned}u_h(y)&=K\{2s(Z_h+g+\varepsilon_h)-s(Z_h-\delta_h)-s(Z_h+\delta_h)\},\\v_h(y)&=\frac{4K}{h}\{s(Z_h+\delta_h)-s(Z_h-\delta_h)\}+\frac{u_h(y+h)-u_h(y-h)}{2h}.\end{aligned}\]</div><span class="num">(6)</span></div>
<p>这严格还原 \(u_j=\partial_x\log[F_j^2/(G_jG_{j+1})]\)、\(v_j=(4/h)\partial_x\log(G_{j+1}/G_j)+\delta_0u_j\)。三个实 \(\tau\) 都正。式 (6) 是函数公式，不是有限点的匹配结果。</p>
<p>精确公式对 \(h\) 为偶解析函数。在固定窗口和正则参数紧邻域中，</p>
<div class="eq"><div class="math">\[U_h=U_0+h^2B+O_H(h^4),\qquad c_3=\frac{P^{-3}+Q^{-3}}{12},\quad \gamma_2=\frac{Q^{-2}-P^{-2}}8.\]</div><span class="num">(7)</span></div>
<div class="eq"><div class="math">\[\begin{aligned}B_u&=2Kyc_3(f'-s')+2K\gamma_2f'-\frac{K\ell^2}{4}s'',\\B_v&=2Kc_3(f'+s')+2K\ell yc_3(f''+s'')+2K\ell\gamma_2f''\\&\hspace{1em}+\frac{K\ell^3}{12}(4f'''-5s''').\end{aligned}\]</div><span class="num">(8)</span></div>
</section>

<section id="obstruction"><h2>3　完整谱、相位切空间的障碍</h2>
<p>记 \(T_i=\partial_{\theta_i}U_0\)。连续 \(u\) 的三个参数切向仅含 \(f-s,f',s'\) 及线性坐标系数，因而复极点阶数至多为二。在 \(s\) 的极点 \(z_*=i\pi(2n+1)\) 处，\(f\) 正则，且</p>
<div class="eq"><div class="math">\[s(z_*+\zeta)=\zeta^{-1}+\tfrac12+\tfrac1{12}\zeta+O(\zeta^3),\qquad B_u=-\frac{K\ell^2}{2}\zeta^{-3}+O(\zeta^{-2}).\]</div><span class="num">(9)</span></div>
<p>三阶系数非零。若 \(B_u\) 在实窗口中是完整参数切向的线性组合，连续性和解析恒等定理将给出亚纯恒等式，与极点阶数矛盾。故 \(B\notin\operatorname{ran}T\)。</p>
<p>\(v\) 须独立计阶：\(v_0\) 自身已有二阶极点，参数切向可到三阶；\(B_v\) 在上述极点具有非零四阶系数 \((5/2)K\ell^3\)。因此两个物理分量分别也有不可吸收的形变。</p>
<p>切空间确实具有秩三。若 \(\delta u_0=0\)，两个不同 \(s\) 极点的二阶系数先迫使 \(\delta K=0\)；\(f\) 极点再迫使 \(\delta g=0\)。而 \(\delta K=0\) 时 \(\delta g=\ell\delta p\)，于是 \(\delta p=\delta q=\delta\varphi=0\)。</p>
<p>更强地，每个允许的 \(h&gt;0\) 下，\(u_h\) 有三组不同的复极点，留数为 \(+2,-1,-1\)；任意正则连续单孤子只有两组，留数为 \(+2,-2\)。因此有限格距场也不可能与任何正则连续单孤子函数恒等。</p></section>

<section id="distance"><h2>4　严格局部距离与定量系数</h2>
<div class="theorem"><p><span class="label">定理。</span>固定上述正则参数、时刻与有内点的有限矩形。对充分小而固定的参数球，定义</p>
<div class="eq"><div class="math">\[D_h(\theta)=\min_{|\theta'-\theta|\le r}\|U_h(\theta)-U_0(\theta')\|_H.\]</div><span class="num">(10)</span></div>
<p>则最近点在小 \(h\) 下唯一，并满足</p>
<div class="eq"><div class="math">\[\boxed{D_h(\theta)=h^2d_\theta+O(h^4),\qquad d_\theta&gt;0.}\]</div><span class="num">(11)</span></div></div>
<p>令 \(G_{ij}=\langle T_i,T_j\rangle_H\)、\(b_i=\langle T_i,B\rangle_H\)，则</p>
<div class="eq"><div class="math">\[d_\theta^2=\|B\|_H^2-b^{\mathsf T}G^{-1}b=\frac{\det\operatorname{Gram}(T_p,T_q,T_\varphi,B)}{\det G},\qquad \theta'_h=\theta+h^2G^{-1}b+O(h^4).\]</div><span class="num">(12)</span></div>
<p>满秩使 \(G\) 正定。与同参数连续场比较已给出 \(O(h^2)\) 上界，局部嵌入性因而迫使任一最近点偏移为 \(O(h^2)\)。最近点方程的隐函数定理给出式 (12)，极点障碍保证剩余系数严格为正。这也排除了任何趋近原参数的重标记将静态差异降为 \(o(h^2)\)。</p>
<p><span class="label">距离的范围。</span>式 (11) 是固定点到局部族的结论。对完整两族取集合间最小距离，在有限窗口中反而得到零：让 \(\varphi\to\pm\infty\)，两个场都趋零。在固定正则参数紧集上，\(d_\theta\) 连续并具有正最小值。</p>
<p>对关于孤子中心对称的窗口，令 \(w=z+g/2\)、\(A=f'-s'\)、\(C'=f''+s''\)。三个 \(u\) 切向的奇部都只有 \(A\) 一个方向，而 \(B_u\) 的奇部还含 \(-K\ell^2C'/8\)。因此得到显式下界：</p>
<div class="eq"><div class="math">\[d_\theta\ge d_u\ge\frac{K\ell^2}{8}\sqrt{\langle C',C'\rangle-\frac{\langle C',A\rangle^2}{\langle A,A\rangle}}&gt;0.\]</div><span class="num">(13)</span></div>
<p>单场内积也除以 \(|\Omega|\)。同一中心的对称子域可给保守下界；严格性仍来自三阶与二阶极点之别。</p></section>

<section id="validation"><h2>5　冻结定点的量化与验证</h2>
<p>理论命题、窗口和以下参数先冻结，再评价精确公式：</p>
<div class="eq"><div class="math">\[a=0,\quad p=2,\quad q=-1,\quad \varphi=-\tfrac12\log2,\quad t=0,\quad \Omega=[-8,8]\times[-1,1].\]</div><span class="num">(14)</span></div>
<p>此时 \(K=1\)、\(\ell=-1/2\)、\(\Gamma=2\)。式 (12) 的窗口积分给出</p>
<div class="eq"><div class="math">\[d_\theta\approx @@D@@,\qquad d_u\approx @@DU@@,\qquad d_v\approx @@DV@@.\]</div><span class="num">(15)</span></div>
<p>这些小数是求积值。独立的精确积分及有理区间包围给出更保守的认证结论：</p>
<div class="eq"><div class="math">\[\boxed{d_\theta\ge d_u&gt;@@LOWER@@.}\]</div><span class="num">(16)</span></div>
<p>认证取中心对称子域的正半部 \(z\in[0,\log4],\ y\in[-1,1]\)，其余半部由中心反射得到。令 \(r=e^z\)，三个积分的被积函数为 \(A(r)^2/r,C'(r)^2/r,A(r)C'(r)/r\)，其中</p>
<div class="eq"><div class="math">\[A(r)=\frac{2r}{(1+2r)^2}-\frac r{(1+r)^2},\qquad C'(r)=\frac{2r(1-2r)}{(1+2r)^3}+\frac{r(1-r)}{(1+r)^3}.\]</div><span class="num">(17)</span></div>
<p>其在 \([1,4]\) 上的精确定积分分别记为 \(I_A,I_C,I_{AC}\)。镜像映射为 \(r\mapsto1/(2r)\)，三种积不变；式 (16) 来自 \(\tfrac1{32}\sqrt{(I_C-I_{AC}^2/I_A)/8}\) 的认证下端。</p>
<p>下表只验证式 (7)、(11)，没有推进 PDE。全参数局部拟合使用同一个观测窗口：</p>
<div class="tablewrap"><table><thead><tr><th>\(h\)</th><th>\(D_h\)</th><th>\(D_h/h^2\)</th><th>\(\|U_h-U_0-h^2B\|/h^4\)</th></tr></thead><tbody>@@ROWS@@</tbody></table></div>
<p class="small">80、120、180阶张量 Gauss 积分交叉核对；最近参数偏移除以 \(h^2\) 同样趋向 \(G^{-1}b\)。拟合与求积支持渐近预测，函数非恒等性及正距离来自前述证明。</p></section>

<section id="evolution"><h2>6　共同初值为何需要另一条误差公式</h2>
<p>假设在明确的演化空间中，共同物理初值解具有 \(U_h^{\mathrm{evol}}=U_0+h^2a+O(h^4)\)，且连续线性化传播 \(\Phi(t,s)\) 存在。全空间或无需附加边界纠正的相容问题中，精确族偏移 \(B\) 与共同初值误差满足同一个受迫线性化方程，初态不同，故</p>
<div class="eq"><div class="math">\[\boxed{a(t)=B(t)-\Phi(t,0)B(0),\qquad a(0)=0.}\]</div><span class="num">(18)</span></div>
<p>如果参数切向也满足同一齐次线性化边界，则 \(T(t)=\Phi(t,0)T(0)\)。固定重标记 \(B\mapsto B-Tc\) 在式 (18) 中完全抵消；它不能单独改善共同初值的真实领先误差。</p>
<p>实际有限边界与 Gram 族不匹配时，须再加入边界响应，其数据是实际误差边界首项减去 Gram 族边界首项。固定解析边界通常随谱参数变化，不能直接假定切向满足齐次边界。每个时刻重新拟合参数也不是固定重标记。</p>
<p>因此静态 \(d_\theta&gt;0\) 不给总演化误差下界：在 \(t=0\) 已有 \(a=0\)。本文没有证明一般扰动的适定性、统一传播界或有限时间总误差下界；观测窗口的 \(L^2\) 范数不能代替这些条件。</p></section>

<section id="meaning"><h2>7　结构究竟保护什么</h2>
<p>精确 Gram 结构保护有限格距孤子族的解析存在与半离散演化相容性。它保留下来的物理波形含有无法由连续谱和相位坐标变化吸收的二阶形变：中点重构分裂的极点在 \(h\to0\) 时合并，却留下非零法向系数。</p>
<p>这是关于离散族物理几何的限制定理。它既不要求产生数值收益，也不把精确族保真升级为共同初值的长期准确性。共同初值的问题仍由初态纠正、传播与边界共同决定。</p></section>

<section id="sources"><h2>来源与证明材料</h2><ol class="references">
<li><a href="Workspaces/dlw_semidiscrete/NONLINEAR_CLOSURE.md">非线性闭合</a>，§1、4：中点物理变量与二阶重构。</li>
<li><a href="Workspaces/dlw_semidiscrete/ALTERNATIVE_DISCRETIZATIONS.md">Gram 半离散化</a>，§2、3：精确双壁族与谱乘子。</li>
<li><a href="Workspaces/dlw_semidiscrete/numerics/MANIFOLD_SCATTERING_REPORT.md">已有流形研究</a>，§1、5：固定谱相位投影的范围。</li>
<li><a href="Workspaces/dlw_factor_model_20260930/REPORT.md">物理误差映射</a>，§4、6、9；<a href="Workspaces/dlw_h2_bounds_20260930/REPORT.md">共同初值纠正</a>，§4。</li>
<li><a href="Workspaces/dlw_theory_soliton_geometry_20261001/THEORY.md">本题完整证明与冻结预测</a>；<a href="Workspaces/dlw_theory_soliton_geometry_20261001/quantitative_bound.json">下界认证</a>；<a href="Workspaces/dlw_theory_soliton_geometry_20261001/geometry_validation.json">定点验证</a>；<a href="Workspaces/dlw_theory_soliton_geometry_20261001/symbolic_validation.json">符号核对</a>。</li>
</ol></section>
<footer>本文的“新证明”指相对于项目既有工作新增的结论；外部文献原创性尚未核查。</footer>
</main><script>@@KATEX_JS@@</script><script>
document.addEventListener('DOMContentLoaded',()=>renderMathInElement(document.body,{delimiters:[{left:'\\[',right:'\\]',display:true},{left:'\\(',right:'\\)',display:false}],throwOnError:true}));
</script></body></html>"""
    source = source.replace('@@D@@', f'{d:.11f}').replace('@@DU@@', f'{du:.11f}').replace('@@DV@@', f'{dv:.11f}')
    source = source.replace('@@LOWER@@', lower).replace('@@ROWS@@', rows)
    srcpath = HERE/'dlw_soliton_geometry.src.html'
    srcpath.write_text(source, encoding='utf-8')
    css = (ASSETS/'katex.min.css').read_text(encoding='utf-8')

    def font(match):
        path = ASSETS/'fonts'/match.group(1)
        suffix = path.suffix.lstrip('.')
        mime = {'woff2': 'font/woff2', 'woff': 'font/woff', 'ttf': 'font/ttf'}[suffix]
        return 'url(data:'+mime+';base64,'+base64.b64encode(path.read_bytes()).decode()+')'

    css = re.sub(r'url\("?fonts/([A-Za-z0-9_\-.]+)"?\)', font, css)
    js = '\n'.join((ASSETS/name).read_text(encoding='utf-8') for name in ['katex.min.js', 'contrib/auto-render.min.js'])
    output = source.replace('@@KATEX_CSS@@', css).replace('@@KATEX_JS@@', js)
    output = output.replace('href="Workspaces/', 'href="../../Workspaces/')
    outpath = HERE/'report.html'
    outpath.write_text(output, encoding='utf-8')
    manifest = {'report': str(outpath), 'sha256': hashlib.sha256(outpath.read_bytes()).hexdigest(),
                'bytes': outpath.stat().st_size, 'source_sha256': hashlib.sha256(srcpath.read_bytes()).hexdigest(),
                'theory_current_sha256': hashlib.sha256((HERE/'THEORY.md').read_bytes()).hexdigest(),
                'frozen_prediction_sha256': validation['theory_sha256_before_verification'],
                'new_pde_runs': 0}
    (HERE/'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()
