from pathlib import Path
import json,sys
HERE=Path(__file__).resolve().parent
CAN=HERE/'canonical_reference'
ROOT=HERE.parents[2]
sys.path.insert(0,str(CAN))
from evaluate import evaluate
validation=json.loads((CAN/'validation.json').read_text())
selected={'Sinusoidal':'Sinusoidal_M32_Y24_dt5.0e-05','Gaussian':'Gaussian_M128_Y24_dt5.0e-05'}
rows=''
for case,name in selected.items():
    r=json.loads((CAN/(name+'.json')).read_text())
    uv=evaluate(case,0,0,.01).ravel()
    rows+=f'<tr><td>{case}</td><td>{uv[0]:.15g}</td><td>{uv[1]:.15g}</td><td>{r["maximum_u"]:.15g}</td><td>{r["maximum_v"]:.15g}</td></tr>'
refs=''
for r in validation['refinements']:
    refs+=f'<tr><td>{r["fine"].split("_")[0]}</td><td>{r["axis"]}</td><td>{r["coarse"].split("_",1)[1]} → {r["fine"].split("_",1)[1]}</td><td>{r["max_difference_u_v"][0]:.3e}</td><td>{r["max_difference_u_v"][1]:.3e}</td></tr>'
eligibility=dict(target='full nonlinear continuous DLW at T=.01',
    domain='periodic x in [-96,96), y in [-2,2]',
    initial_data='approved periodic Gaussian sum and original sinusoidal fields',
    candidate_full_fields_available=True,candidate_time_interval=[0,.01],
    eta_u=None,eta_v=None,certified=False,
    reason='No continuum certificate; positive all-mode test R2 is proved unable to close for nonzero-frequency uncertainty',
    independently_verified=['canonical integral equations and boundary reconstruction',
       'dealiased Fourier product vs direct convolution', 'y integration on polynomials',
       'x/y/time refinement observations', 'independent DOP853 comparison',
       'exact internal forward/backward parabolic decomposition'],
    excluded_routes=['summable nonnegative R2 envelopes with nonzero-frequency error/residual seeds',
       'uniform finite-order Gevrey-y regularity for the actual sine data, conditional on smooth existence'],
    not_established=['data-specific nonlinear continuum existence and uniqueness class',
       'alternative structure-based full-domain error estimate','finite numeric eta_u and eta_v','eta<=.01D'],
    nonexistence_of_requested_data_claimed=False,
    candidate_files={case:str(CAN/(name+'.npz')) for case,name in selected.items()})
(HERE/'full_reference_status.json').write_text(json.dumps(eligibility,indent=2),encoding='utf8')
doc=f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>连续 DLW 全场候选参考与认证状态</title>
<style>body{{max-width:1080px;margin:44px auto;padding:0 24px;font:17px/1.85 Georgia,"Microsoft YaHei",serif;color:#222}}h1{{font-size:29px}}h2{{font-size:23px;margin-top:34px}}table{{width:100%;border-collapse:collapse;margin:22px 0;border-top:2px solid;border-bottom:2px solid;font-size:14px;font-variant-numeric:tabular-nums}}th,td{{text-align:left;padding:8px 10px}}thead{{border-bottom:1px solid}}.eq{{padding:14px 20px;background:#f5f5f3;overflow:auto}}a{{color:#245c7b}}.status{{color:#555}}.scroll{{overflow-x:auto}}</style></head><body>
<h1>连续 DLW 全场候选参考与误差认证状态</h1><p class="status">2026-10-24 · 已生成 0≤t≤0.01 的两组全场候选轨道；全区域误差上界 η<sub>u</sub>、η<sub>v</sub>尚未取得。</p>
<p>本轮的目标是连续方程的物理场，而不是 Endpoint-SD、Centered-SD 或旧 FD 格式的精细网格解。采用独立的 Fourier–Galerkin / Chebyshev 求解器推进完整非线性连续方程的积分表示。所有数据明确标记为候选，不能据此宣称 η≤0.01‖q<sub>num</sub>−q<sub>ref</sub>‖。</p>
<h2>连续问题与候选表示</h2><p>a=2，λ=−2，x 周期 192，−2≤y≤2，u(x,−2,t)=0。高斯使用用户批准的周期求和 G<sub>per</sub>(x)=Σ<sub>m∈ℤ</sub> exp[−((x+192m)/6)²]，两场初值为 (0.05,0.03)e(y)G<sub>per</sub>；正弦初值为 u₀=0.03e(y)cos(πx/12)、v₀=0.02e(y)sin(πx/12)，其中 e(y)=sin[π(y+2)/4]。</p>
<p>令 w=v−u<sub>y</sub>，I 为从 −2 到 y 的积分，求解精确非线性等价式</p><div class="eq">u<sub>t</sub>=−u<sub>xx</sub>−∂<sub>x</sub>(u²/2+4u)−Iw<sub>xx</sub>,<br>w<sub>t</sub>=w<sub>xx</sub>−∂<sub>x</sub>[(u+4)w−4u],　v=u<sub>y</sub>+w.</div>
<p>在 x 中作明确的 Fourier–Galerkin 投影，二次乘积去混叠；在 y 中使用 Chebyshev 多项式与积分矩阵。旧 FD 的冻结下端幽灵点和上端外推均不用于本求解器。正弦按其周期 24 的精确对称性计算，得到的候选函数在原区间重复。选用正弦 M=32、高斯 M=128 的 Fourier 截断、y 多项式次数 24、RK4 步长 5×10⁻⁵；附加更高截断与独立 DOP853 对照。</p>
<h2>T=0.01 的实际候选场值</h2><div class="scroll"><table><thead><tr><th>算例</th><th>u(0,0,T)</th><th>v(0,0,T)</th><th>采样 max|u|</th><th>采样 max|v|</th></tr></thead><tbody>{rows}</tbody></table></div><p>表中数值是计算结果，不附已证明的正确位数。最大值取公共评价采样点，不是经过区间包围的连续最大值。</p>
<p>轨道保存 11 个时刻的 Fourier/Chebyshev 系数。<a href="../Workspaces/dlw_paper_20261009/reference_certificate_20261024/canonical_reference/evaluate.py">evaluate.py</a> 可在任意 x、−2≤y≤2、0≤t≤0.01 上返回候选 u,v；保存时刻之间使用明确的三次 Hermite 插值，其误差也尚未认证。</p>
<p><a href="../Workspaces/dlw_paper_20261009/reference_certificate_20261024/canonical_reference/Sinusoidal_M32_Y24_dt5.0e-05.npz">正弦全场轨道 NPZ</a> · <a href="../Workspaces/dlw_paper_20261009/reference_certificate_20261024/canonical_reference/Gaussian_M128_Y24_dt5.0e-05.npz">周期高斯全场轨道 NPZ</a></p>
<h2>数值复核</h2><div class="scroll"><table><thead><tr><th>算例</th><th>加密方向</th><th>设置</th><th>u 最大差</th><th>v 最大差</th></tr></thead><tbody>{refs}</tbody></table></div>
<p>独立 DOP853 与选定轨道的最终场值差不超过 2.3×10⁻¹⁶。精确非线性下边界迹检查约为 10⁻¹⁵。对完整物理 PDE 的离散时空采样残差不超过 3.3×10⁻¹²。这些均是数值诊断；未通过整个时空区间的区间运算包围，也不控制全部未解析频率。</p>
<h2>为什么还不能给出全区域上界</h2><p>取 a=u<sub>y</sub>+v，b=u<sub>y</sub>−v，则连续非线性方程本身精确包含</p><div class="eq">a<sub>t</sub>=−a<sub>xx</sub>−∂<sub>x</sub>[(u+4)a−4u],<br>b<sub>t</sub>=b<sub>xx</sub>−∂<sub>x</sub>[(u+4)b+4u],　u=I(a+b)/2.</div>
<p>第一式的线性部分具有 exp(ξ²t) 的增长。独立推导确认：即使扰动完全位于内部、在下边界附近恒为零，零解线性化仍保留这一高频谱。因此边界处理正确并没有自动提供全区域稳定性。</p>
<p>通常控制二次乘积的解析 Fourier 权至多指数增长，吸收不了 exp(ξ²t)；高斯 Fourier 权能控制线性反向扩散，却不构成同一空间中的乘法代数。对当前周期高斯，G² 的频谱衰减已从 exp(−9ξ²) 降至 exp(−4.5ξ²)。对正弦，非线性立即生成二倍频。不能把初始光滑性直接当成传播到 T 的尾部上界。</p>
<p>这些结论排除了上述直接认证路线，并不证明两组指定初值的非线性解不存在。一个不同初值的精确反例还说明：一般的“解析初值保证局部经典解”在此系统中不成立，因而不能引用这种未验证前提来补足证明。</p>
<h2>本轮核查：原误差包络无法闭合</h2><p>进一步的解析证明排除了此前提出的正值 Fourier 包络 R2。只要某个非零频率 m 的误差包络在一个时间段内有正下界 δ，二次卷积便产生各次谐波；反向扩散随后迫使</p>
<div class="eq">α<sub>jm</sub>(T) ≥ jδ(cδτ)<sup>j−1</sup> exp[j²κ²(T−t₀)]，　j≥2.</div>
<p>这里 κ=|ξ<sub>m</sub>|，c=Jκ/2，τ=t₀−s₀&gt;0，且 t₀&lt;T。右端随 j 发散，因此不可能存在可求和的包络。减小残差或增加计算精度无法改变这一结论。它说明该正值估计丢失了必须利用的结构，并不证明真实 Fourier 系数也发生相同的增长。<a href="../Workspaces/dlw_paper_20261009/reference_certificate_20261024/TAIL_MAJORANT_REVIEW.md">完整证明</a>。</p>
<h2>当前正弦初值的具体正则性障碍</h2><p>对本文使用的正弦初值，还能从下边界逐阶求导得到一个精确结论。假设解光滑到足以计算所有边界导数，令 ω=π/12、c₀=0.03(π/4)/2，则每个 t&gt;0 都满足</p>
<div class="eq">sup<sub>x</sub>|∂<sub>y</sub><sup>n</sup>u(x,−2,t)| ≥ (n!/2)c₀<sup>n</sup>(ωt/2)<sup>n−1</sup> exp(n²ω²t/2)，　n≥1.</div>
<p>因此这些导数不满足任何固定有限阶的界 CB<sup>n</sup>(n!)<sup>s</sup>。在给定初边值条件下，不能假设正时间真解具有解析或有限阶 Gevrey 的 y 向正则性，也不能以相应的 Chebyshev 尾部衰减来认证它。该推导针对当前正弦数据，已独立复核；它不排除更弱正则性的解，不给出物理场误差下界，也不直接适用于周期高斯。<a href="../Workspaces/dlw_paper_20261009/reference_certificate_20261024/ACTUAL_DATA_REVIEW.md">推导与条件</a> · <a href="../Workspaces/dlw_paper_20261009/reference_certificate_20261024/ACTUAL_DATA_INDEPENDENT_REVIEW.md">独立复核</a>。</p>
<h2>全区域误差保证的当前结论</h2><p><strong>尚未得到有限数值的 η<sub>u</sub>、η<sub>v</sub>，也未证明它们小于方法间误差的 1%。</strong>此前“只需找到合适的 R2 尾部包络”的判断已由上面的证明修正。两组全场轨道仍是未经认证的候选，不能作为论文中带严格误差保证的连续参考解。</p>
<p>实际初值对应的连续解存在性及另一种全域误差估计仍未建立。这里排除的是明确的证明路线，没有据此宣称这两组连续解不存在。主论文尚未加入任何已认证精度的表述。</p>
<p><a href="../Workspaces/dlw_paper_20261009/reference_certificate_20261024/CERTIFICATE_ROUTE_REVIEW.md">完整包络条件与内部谱论证</a> · <a href="../Workspaces/dlw_paper_20261009/reference_certificate_20261024/INTERIOR_EXISTENCE_REVIEW.md">非线性变换与存在性审查</a> · <a href="../Workspaces/dlw_paper_20261009/reference_certificate_20261024/canonical_reference/README.md">复现入口</a> · <a href="../Workspaces/dlw_paper_20261009/reference_certificate_20261024/full_reference_status.json">认证状态</a></p></body></html>'''
out=ROOT/'report/dlw_continuum_reference_20261024.html'
out.write_text(doc,encoding='utf8')
print(out)
