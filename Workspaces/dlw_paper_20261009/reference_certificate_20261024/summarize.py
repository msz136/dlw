from pathlib import Path
import json, html
import numpy as np
import sympy as sp
import mpmath as mp
from certificate import upper_bound

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
mp.mp.dps=100
x,h,a,lam=sp.symbols('xi h a lam',nonzero=True,real=True)
B=sp.Matrix([[-2*a*sp.I*x,h*x*x],[x*x/h-lam*sp.I*x,-(2*a+lam*h)*sp.I*x]])
vp=sp.Matrix([1,1/h-sp.I*lam/x]); sig=x*x-sp.I*(2*a+lam*h)*x
assert all(sp.simplify(v)==0 for v in B*vp-sig*vp)
sm=-x*x-2*a*sp.I*x
assert sp.simplify((B-sm*sp.eye(2)).det())==0
growth=[]
for dx in ['.1','.05','.025']:
    N=int(mp.mpf(192)/mp.mpf(dx)); xi=2*mp.pi*(N//2-1)/192
    log=xi**2*mp.mpf('.01')/mp.log(10)
    growth.append(dict(dx=float(dx),log10_amplification=float(log),amplification=mp.nstr(10**log,12),
        note='Endpoint linear first-site lower bound; not a nonlinear certificate'))
records=[json.loads(p.read_text()) for p in sorted(HERE.glob('*_dx*_dt*.json'))]
comparisons={}
for case in ['Gaussian','Sinusoidal']:
    base=np.load(HERE/f'{case}_dx0.1_dt0.0001.npz')['z']
    fine=np.load(HERE/f'{case}_dx0.05_dt0.0001.npz')['z']
    half=np.load(HERE/f'{case}_dx0.05_dt5e-05.npz')['z']
    comparisons[case]=dict(x_refinement_native=[float(abs(fine[j,:,::2]-base[j]).max()) for j in range(2)],
                          half_time_step=[float(abs(fine[j]-half[j]).max()) for j in range(2)])
precision={}
control=json.loads((HERE/'fundamental_float64_control.json').read_text()) if (HERE/'fundamental_float64_control.json').exists() else {}
p50=HERE/'Sinusoidal_precision50_dx0.05_dt0.0001.txt'
p80=HERE/'Sinusoidal_precision80_dx0.05_dt0.0001.txt'
if p50.exists() and p80.exists():
    l50=p50.read_text().splitlines();l80=p80.read_text().splitlines()
    assert len(l50)==len(l80)==2*41*480
    err=max(abs(mp.mpf(s)-mp.mpf(t)) for s,t in zip(l50,l80))
    z=np.load(p80.with_suffix('.npz'))['z']
    full=np.load(HERE/'Sinusoidal_dx0.05_dt0.0001.npz')['z']
    precision=dict(decimal_precision_difference=mp.nstr(err,15),
        full_double_vs_high_precision=[float(abs(full[j]-np.tile(z[j],(1,8))).max()) for j in range(2)],
        amplitude=[float(abs(z[j]).max()) for j in range(2)], certified=False)
v=dict(endpoint_eigenpair_symbolic=True,endpoint_minus_eigenvalue_symbolic=True,
       gaussian_periodic_derivative_jump=mp.nstr(mp.mpf(32)/3*mp.exp(-256),20),
       growth=growth,comparisons=comparisons,precision=precision,fundamental_float64_control=control,
       continuum_certificate=False,eta=None,
       missing=['nonlinear continuum existence/stability in a specified space',
                'unresolved x mode bounds','validated full-time residual/boundary enclosures'],
       conditional_arithmetic_test=upper_bound(initial='1e-14',residual='1e-12',linear='1',quadratic='1',radius='1e-10',T='.01',discrepancy='1e-8'))
for key,name in [('boundary_certificate','boundary_certificate.json'),('periodic_gaussian_certificate','periodic_gaussian_certificate.json')]:
    if (HERE/name).exists(): v[key]=json.loads((HERE/name).read_text())
(HERE/'validation.json').write_text(json.dumps(v,indent=2),encoding='utf8')
rows=''
for case in ['Gaussian','Sinusoidal']:
    for dx in [.1,.05,.025]:
        r=next(r for r in records if r.get('case')==case and r.get('dx')==dx and r.get('dt')==.0001 and 'dps' not in r)
        vals=r.get('amplitude')
        value=' / '.join(f'{x:.7g}' for x in vals) if vals else f"停止于 t={r['stopped_at']:.4f}"
        rows+=f'<tr><td>{case}</td><td>{dx}</td><td>{value}</td></tr>'
prows=''.join(f"<tr><td>{g['dx']}</td><td>{g['log10_amplification']:.3f}</td><td>{g['amplification']}</td></tr>" for g in growth)
prec='<p>高精度复核尚未完成。</p>'
if precision:
    prec=f'''<p>正弦算例在相同 Δx=0.05、h=0.1、Δt=10⁻⁴ 下，以 50 位和 80 位精度推进同一非线性 FD 方程。利用其周期 24 的不变子空间进行计算，再重复到原周期 192；未修改微分方程或滤除基本周期内的频率。两者终态最大差为 {precision['decimal_precision_difference']}。80 位计算的最大幅值为 u={precision['amplitude'][0]:.10g}、v={precision['amplitude'][1]:.10g}。</p>
<p>与完整区间双精度计算的终态差为 u={precision['full_double_vs_high_precision'][0]:.6g}、v={precision['full_double_vs_high_precision'][1]:.6g}。高精度与对称性保持共同抑制了舍入扰动的影响；两种精度之间的接近仍不是连续解误差上界。粗网格 Δx=0.5 的独立实现对照差为 9.72×10⁻¹⁷。</p>'''
    if control:
        prec+=f"<p>额外保持同一周期 24、同一网格与时间步，只使用双精度计算，最大幅值为 u={control['amplitude'][0]:.8g}、v={control['amplitude'][1]:.8g}；与 80 位结果的差为 {control['difference_to_80digit'][0]:.6g}、{control['difference_to_80digit'][1]:.6g}。这项对照进一步确认了精度敏感性，不能将原来的大幅增长直接解释为物理解的增长。</p>"
doc=f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DLW 非孤子参考解的误差认证</title>
<style>body{{max-width:940px;margin:44px auto;padding:0 24px;font:17px/1.85 Georgia,"Microsoft YaHei",serif;color:#242424}}h1{{font-size:29px}}h2{{font-size:23px;margin-top:34px}}table{{width:100%;border-collapse:collapse;margin:22px 0;border-top:2px solid;border-bottom:2px solid}}th,td{{text-align:left;padding:8px 12px}}thead{{border-bottom:1px solid}}.eq{{padding:14px 20px;background:#f5f5f3;overflow:auto}}a{{color:#245c7b}}.status{{color:#555}}</style></head><body>
<h1>DLW 高斯与正弦初值：参考解能否得到误差认证？</h1><p class="status">2026-10-24 · 理论证明稿、区间核验与数值诊断。已取得边界迹采样值的误差上界，尚未取得连续非线性解的全区域误差证书。</p>
<p>目标是证明参考解误差不超过可计算的 η，并验证 η ≤ 0.01‖q<sub>num</sub>−q<sub>ref</sub>‖。本轮完成了残差证书的条件化推导、标量上界计算器、八组双精度复核以及任意精度复核。当前的空间加密结果不能直接作为已认证参考。</p>
<h2>共同的非线性问题</h2><p>e(y)=sin[π(y+2)/4]；原高斯为 (u,v)=(0.05,0.03)e(y)exp[−(x/6)²]，正弦为 u=0.03e(y)cos(πx/12)、v=0.02e(y)sin(πx/12)。a=2，λ=−2，x∈[−96,96) 周期，y∈[−2,2]，左端 u=0。发现原高斯的边界障碍后，用户已选择将高斯改为严格的周期求和 G<sub>per</sub>(x)=Σ<sub>m∈ℤ</sub>exp[−((x+192m)/6)²]。下面旧高斯复核仍明确对应原初值，新周期高斯当前只完成边界认证。</p>
<p>令 w=v−u<sub>y</sub>，I 为从 −2 到 y 的积分，可将连续方程精确写成</p><div class="eq">u<sub>t</sub> = −u<sub>xx</sub> − ∂<sub>x</sub>(u²/2+4u) − Iw<sub>xx</sub>,<br>w<sub>t</sub> = w<sub>xx</sub> − ∂<sub>x</sub>[(u+4)w−4u],　v=u<sub>y</sub>+w.</div>
<p>这个表示不需要右端幽灵点，给出了一条保持原初值的参考方程路线。左端 w 由初值与热传导平流方程确定。它尚未提供存在性或稳定性证明。要认证 v，范数还必须控制 u 的 y 导数。</p>
<h2>双精度加密复核</h2><p>以下均为旧非线性 FD 候选参考的复核，h=0.1，Δt=10⁻⁴，目标 T=0.01。表中是场的最大幅值，不是误差；停止指首次出现非有限数或幅值超过 10⁶，不是解析爆破时间。</p><table><thead><tr><th>初值</th><th>Δx</th><th>最大幅值 u / v 或状态</th></tr></thead><tbody>{rows}</tbody></table>
<p>Δx=0.05 时将时间步减半，高斯两分量终态差为 {comparisons['Gaussian']['half_time_step'][0]:.3g}、{comparisons['Gaussian']['half_time_step'][1]:.3g}；正弦为 {comparisons['Sinusoidal']['half_time_step'][0]:.3g}、{comparisons['Sinusoidal']['half_time_step'][1]:.3g}。旧有固定 Δx=0.1 的 y 加密结果不能代替这一方向的控制。</p>
<h2>提高精度后的复核</h2>{prec}
<h2>误差上界需要证明什么</h2><p>若在具有局部存在与延拓性质的解空间中，能证明误差满足 D⁺E ≤ ρ+LE+BE²，初始误差不超过 e₀，则对给定 R，只要</p><div class="eq">η = (e₀+Tρ) exp[(L+BR)T] &lt; R,</div><p>就可通过首次离开误差管道的反证与 Gronwall 估计得到 E(T)≤η。程序已实现这一充分条件的向上舍入计算。但 ρ 必须是整段时间、完整连续方程的残差上界；当前采样的离散 ODE 残差不满足这一要求。</p>
<p>对 Endpoint-SD 的零解开链线性化，第一格点的 Fourier 块有精确增长特征值 σ₊=ξ²−i(2a+λh)ξ。因此其传播算子范数至少为 exp(ξ²T)。相应非 Nyquist 最高频率给出：</p><table><thead><tr><th>Δx</th><th>log₁₀ 放大因子</th><th>放大因子</th></tr></thead><tbody>{prows}</tbody></table><p>这是线性最坏方向的放大下界，不是非线性误差上界，也不证明指定初值不存在解。它排除了直接假设普通范数中稳定性常数与 x 分辨率无关的做法。</p>
<p>高斯初值还有一个需明确的细节：当前截断周期延拓的导数跳跃为 (32/3)e⁻²⁵⁶≈{v['gaussian_periodic_derivative_jump']}。它虽很小，却不能在解析空间的证明中当成零。换成周期高斯求和会改变初值，本轮没有作这种替换。</p>
<h2>结论与下一步</h2><p>本轮没有产生满足 η≤0.01D 的证书，η 仍未确定。高精度轨道只是候选参考，不能写入论文作为已知精确解。剩余关键问题是原始非线性初边值问题的解空间与稳定性、未解析 x 模态的控制，以及带边界处理的完整残差包络。有限维时间误差证书不能替代这三项。</p>
<p><a href="../Workspaces/dlw_paper_20261009/reference_certificate_20261024/THEORY.md">完整推导与适用条件</a> · <a href="../Workspaces/dlw_paper_20261009/reference_certificate_20261024/validation.json">核验与数据汇总</a> · <a href="../Workspaces/dlw_paper_20261009/reference_certificate_20261024/README.md">复现入口</a></p></body></html>'''
out=ROOT/'report/dlw_reference_certificate_20261024.html'
if 'boundary_certificate' in v:
    block='''<h2>已经取得的严格边界结果</h2>
<p>在下边界令 p=u<sub>y</sub>、b=v。完整非线性 PDE 在 u=0 的边界精确给出 p<sub>t</sub>=−b<sub>xx</sub>−4p<sub>x</sub>、b<sub>t</sub>=−p<sub>xx</sub>−4b<sub>x</sub>。所以 r=p+b 满足反向热方程，s=p−b 满足前向热方程。这不是对内部方程的线性近似。</p>
<p>正弦初值对应的精确边界值为</p><div class="eq">b(x,t)=(0.03π/4) cos[(π/12)(x−4t)] sinh[(π/12)²t].</div>
<p>100 位 Arb 区间运算逐点核验：旧 h=0.0125 FD 参考解的下边界最大采样误差满足 <strong>4.2267×10⁻⁸ &lt; E &lt; 4.2269×10⁻⁸</strong>。因此它不可能获得包含该边界的全区域 10⁻¹⁰ 误差证书。旧评价区域排除了边界，这个下界不能直接当成内部区域的误差下界。冻结的下端幽灵点使边界导数逼近 [p(t)+p(0)]/2，而不是 p(t)，解释了加密后仍有偏差。</p>
<p>另行按上述精确公式生成的 480 个边界值，在 T=0.01 的表示误差已逐点认证为 <strong>小于 10⁻⁷²</strong>。这只是边界公式求值的上界，不是内部参考解的上界。</p>
<p>原截断周期高斯的 Fourier 系数具有非零 n⁻² 首项，反向热边界迹将其乘以 exp(ξ²t)。任意正时间都会超出周期分布允许的多项式增长。因此，在能取上述边界迹的经典解正则性下，原初边值问题不存在所需连续解。此结论不针对实线高斯或所有弱解概念。</p>
<h2>已选定的周期高斯与上界</h2><p>用户已确认采用周期高斯求和。它与原剖面在原区间上的最大差小于 1.324×10⁻¹¹¹，但光滑性不同。周期高斯的热演化具有显式高斯求和表达，反向部分在 t&lt;9 有效。</p>
<p>在 T=0.01，保留 m=−1,0,1 并用几何级数界定余项，边界 v 的遗漏求和尾部统一小于 10⁻⁹⁹⁸；对 1921 个指定 x 点，80 位输出数值到精确边界值的误差已认证为 <strong>小于 10⁻⁸⁰</strong>。两项都不是全区域误差证书。内部非线性解的存在性、稳定性和未解析频率控制尚未完成。</p>
<p><a href="../Workspaces/dlw_paper_20261009/reference_certificate_20261024/BOUNDARY_THEOREM.md">边界推导、原高斯障碍及适用条件</a> · <a href="../Workspaces/dlw_paper_20261009/reference_certificate_20261024/boundary_certificate.json">正弦区间核验</a> · <a href="../Workspaces/dlw_paper_20261009/reference_certificate_20261024/periodic_gaussian_certificate.json">周期高斯区间核验</a></p>'''
    doc=doc.replace('<h2>结论与下一步</h2>',block+'<h2>结论与下一步</h2>')
    doc=doc.replace('换成周期高斯求和会改变初值，本轮没有作这种替换。','这个障碍已通过下面精确边界方程得到进一步确认；用户随后已明确选择周期高斯求和。')
out.write_text(doc,encoding='utf8')
print(json.dumps(v,indent=2))
print(out)
