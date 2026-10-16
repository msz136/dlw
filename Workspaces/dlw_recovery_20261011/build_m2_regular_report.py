"""Write the concise coupled original M=2 local Liouville report."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "report/dlw_m2_regular_liouville_20261011.html"
HTML = '''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>原半离散 DLW：M=2 耦合函数相域上的局部刘维尔定理</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#faf9f6;color:#22272b;font:18px/1.85 Cambria,"Noto Serif CJK SC","Songti SC",serif}main{max-width:880px;margin:50px auto;padding:0 30px 60px}h1{font-size:29px;line-height:1.45;font-weight:600;margin:0 0 14px}h2{font-size:22px;font-weight:600;margin:34px 0 12px}p{margin:14px 0}a{color:#315b70;text-decoration:none;border-bottom:1px solid #c8d7df}.date,footer{color:#666;font-size:15px}.result{border-left:3px solid #7195a2;padding-left:18px}.eq{text-align:center;font-size:19px;margin:19px 0;line-height:1.9;overflow-x:auto;white-space:nowrap}footer{margin-top:35px;padding-top:15px;border-top:1px solid #d9ddd9}table{width:100%;border-collapse:collapse;font-size:16px;line-height:1.7;margin:20px 0}td,th{padding:10px;text-align:left;vertical-align:top;border-bottom:1px solid #d9ddd9}th{font-weight:600;border-top:1px solid #9aa09d}@media(max-width:600px){main{margin:25px auto;padding:0 18px 35px}body{font-size:17px}h1{font-size:25px}.eq{font-size:17px}}@media print{body{background:white;font-size:11pt}main{max-width:none;margin:0;padding:0}h2{break-after:avoid}.eq{break-inside:avoid}a{color:inherit}}
</style></head><body><main>
<h1>原半离散 DLW：M=2 耦合函数相域上的局部刘维尔定理</h1>
<div class="date">2026 年 10 月 11 日 · 两个周期格点，连续周期空间 x∈ℝ/Lℤ</div>
<p class="result">在充分小的非零均匀背景附近，可构造一个明确的实 Banach 函数相域：原 DLW 有真实局部解流，原弱辛形式非退化，实际谱积分对合且每个有限块独立；共同水平集是正则 Lagrangian 子流形，并由真实 Hamilton 流覆盖。这个相域保留两组独立的无限函数参数，两个原物理场均可非零且独立变化。</p>

<h2>1. 原物理场与耦合方程</h2>
<p>取 S=hc/4≠0、δ=S/2、2B(t)=Γ(t)/c。固定源空间均值后，以 u,v 为自由场，原变量准确恢复为</p>
<div class="eq">U₀=2B+(1−2v/S)u，&nbsp; U₁=2B−(1+2v/S)u，<br>w₀=8(δ+v)/h，&nbsp; w₁=8(δ−v)/h.</div>
<p>于是 Πw=c、Π(Uw)=Γ(t)。原方程在这些坐标中为</p>
<div class="eq">u<sub>t</sub>=−u<sub>xx</sub>−2Sv<sub>x</sub>+(2/S)∂<sub>x</sub>(u²v)−2Bu<sub>x</sub>，<br>v<sub>t</sub>=v<sub>xx</sub>−(S/2)u<sub>x</sub>+(2/S)∂<sub>x</sub>(uv²)−2Bv<sub>x</sub>.</div>
<p>证明先处理 B=0 的自治流，任意 Γ(t) 经共同空间平移和 U 的共同加量恢复。c 是辛叶标签，可在允许的小非零背景区间改变。取 ‖v‖∞&lt;|S|/4，可进一步选择普通开放子域使 u(x₀)≠0、v<sub>x</sub>(x₁)≠0；两个 U 分量都不是零函数。其点态变分行列式为 −4u/S≠0。线性交叉项和非线性耦合项均保留。<a href="../Workspaces/dlw_recovery_20261011/root_m2_unfrozen_physical_coupling_audit_20261011.md">原方程与解除冻结的复核</a>。</p>

<h2>2. 实际逆谱坐标与原 Hamilton 场</h2>
<p>实际约化状态图 ℛ 在同一低阶源域给出 H<sup>r</sup><sub>0</sub>×H<sup>r+1</sup><sub>0</sub> 与两组 h<sup>r</sup>(ℤ∖{0}) 序列的双解析对应，r≥0。中央动作由原物理约束唯一消除，中央角由真实规范截面消除。记其非中央 Cartesian 坐标为 wₙ,zₙ，实际动作 Jₙ=wₙzₙ；物理实结构准确为</p>
<div class="eq">w<sub>−n</sub>=−w̅ₙ，&nbsp; z<sub>−n</sub>=−z̅ₙ.</div>
<p>在真实谱动作积分中加入原 Poisson 权重 ω<sub>λ</sub>=(S²−λ²)/(16S) 的倒数，定义谱积分 𝒜ₙ。随场变化的谱中心项在微分中精确抵消，得到原 Hamilton 场</p>
<div class="eq">Dℛ X<sub>𝒜ₙ</sub>=L(−wₙeₙ,zₙeₙ).</div>
<p>𝒜: h⁰×h⁰→ℓ¹ 是解析映射。对任意有界序列 d，H<sub>d</sub>=Σdₙ𝒜ₙ 是实际解析 Hamiltonian，其流为 wₙ↦e<sup>−Ldₙτ</sup>wₙ、zₙ↦e<sup>Ldₙτ</sup>zₙ。实流取 d<sub>−n</sub>=d̅ₙ。谱动作、这些积分、原 Hamiltonian H 与平移 Hamiltonian P<sub>T</sub> 全部对合，X<sub>P<sub>T</sub></sub>=∂<sub>x</sub>。<a href="../Workspaces/dlw_recovery_20261011/m2_reciprocal_spectral_actions_and_dlw_frequencies_20261011.md">谱积分及原时间归一化证明</a>。</p>

<h2>3. 明确的普通函数相域</h2>
<p>取真实强解域中所有 Jₙ*≠0 的小实基点。其双向原时间窗保证 w*,z* 有 Gaussian 下降。令 kₙ=2πn/L，以两组有界反射共轭序列 a,q 和两个实参数 t,s 定义</p>
<div class="eq">wₙ=wₙ* exp(aₙ/2+qₙ−tkₙ²+iskₙ)，<br>zₙ=zₙ* exp(aₙ/2−qₙ+tkₙ²−iskₙ).</div>
<p>在足够小的普通参数盒中，此映射单射且导数单射，解析映入每一级光滑场空间。相域采用这组坐标给定的 Banach 拓扑。两组序列均可独立无限变化，不限有限模态。</p>
<p>必要的小背景条件包括 L|S|&lt;π/4，以及原势位于复近零逆谱域和 NLS 频率定理域；后者须另缩半径。实基点的中央动作一般为负，引用使用复解析域，不将原实场改成 NLS 的实相空间。各高阶状态逆共用低域，允许所有 Jₙ 同时趋零；不要求 gap 的统一正下界。</p>

<h2>4. 正则水平集、原弱辛形式与完备性</h2>
<p>原物理 Poisson 张量及其逆形式仍为</p>
<div class="eq">J=−offdiag(∂<sub>x</sub>)/16，<br>Ω(ξ,ζ)=−16∫[(∂<sub>x,0</sub><sup>−1</sup>ξ<sub>u</sub>)ζ<sub>v</sub>+(∂<sub>x,0</sub><sup>−1</sup>ξ<sub>v</sub>)ζ<sub>u</sub>]dx.</div>
<p>其回拉光滑、闭且弱非退化。有限 Cartesian 切向在各级状态空间稠密，保证没有物理零切向的隐藏方向。相对动作 aₙ=log(Jₙ/Jₙ*) 是分裂满射；共同水平集就是 a=a₀ 的普通 Banach 子流形。</p>
<div class="eq">T Y=∩ker d(Re Jₙ)∩ker d(Im Jₙ)，&nbsp; (T Y)<sup>⊥Ω</sup>=T Y.</div>
<p>每个有限实动作块独立。角方向由真实 H<sub>d</sub> 场逐点检验；共同水平集的切空间既是实际微分核，也是原形式下的 Lagrangian 空间。<a href="../Workspaces/dlw_recovery_20261011/m2_regular_variable_action_original_symplectic_phase_20261011.md">完整定理 §§1–10</a>；<a href="../Workspaces/dlw_recovery_20261011/m2_regular_core_akns_bridge_independent_audit_20261011.md">独立几何复核</a>。</p>

<h2>5. 实际轨道与积分求解</h2>
<p>原时间频率已准确归一化为 Ω<sub>H,n</sub>=−kₙ²−2iη(J)kₙ+rₙ(J)，r(J)∈ℓ∞ 解析。因此在上述相域，原 H、平移 P<sub>T</sub> 与有界组合 H<sub>d</sub> 的真实流为</p>
<table><thead><tr><th>Hamiltonian</th><th>参数变化</th></tr></thead><tbody>
<tr><td>原 H</td><td>a′=0，t′=1，s′=−2η(J)，q′=r(J)</td></tr>
<tr><td>空间平移 P<sub>T</sub></td><td>s′=1，其余为零</td></tr>
<tr><td>H<sub>d</sub></td><td>q′=−Ld，其余为零</td></tr></tbody></table>
<p>同一共同水平集的两近点，取 τ=Δt、σ=Δs+2ητ、d=−(Δq−rτ)/L，依次沿 H、P<sub>T</sub>、H<sub>d</sub> 流动时间 τ、σ、1，准确到达目标点。因此小共同水平集是实际 Hamilton 轨道；任意无限有界角方向都有真实流。原解由这些线性参数变化和实际状态逆恢复。无限活跃模态的 −kₙ² 主频也排除了静态与刚性平移。</p>
<p>这是指定函数相域上的局部弱刘维尔定理。时间取使轨道留在参数盒内的非零窗口；尚未覆盖任意光滑初态，也未证明整个变量动作相域同时容纳所有更高辅助层级的双向真实流。一般 M 的 invariant action 逆与全谱 Hamilton 完备性仍需建立。<a href="../Workspaces/dlw_recovery_20261011/root_m2_regular_original_liouville_phase_audit_20261011.md">根复核及准确范围</a>。</p>
<footer><a href="dlw_liouville_recovery_20261011.html">全专题报告</a> · <a href="../刘维尔可积性/research/STATE.md">研究状态</a> · <a href="../刘维尔可积性/GOAL.md">持续目标</a></footer>
</main></body></html>'''

if __name__ == "__main__":
    TARGET.write_text(HTML, encoding="utf-8")
    print(f"Saved {TARGET.relative_to(ROOT)} ({len(HTML)} characters).")
