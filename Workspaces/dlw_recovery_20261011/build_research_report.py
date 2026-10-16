"""Build the concise research report from the audited 2026-10-11 results."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "report" / "dlw_liouville_recovery_20261011.html"
HTML = '''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>半离散 DLW：一般场可积性的研究进展</title>
<style>
:root{color-scheme:light}*{box-sizing:border-box}body{margin:0;background:#faf9f6;color:#202326;font:18px/1.85 Cambria,"Noto Serif CJK SC","Songti SC",serif}main{max-width:880px;margin:55px auto;padding:0 30px 65px}h1{font-size:31px;line-height:1.45;font-weight:600;margin:0 0 12px}h2{font-size:23px;font-weight:600;margin:36px 0 12px}p{margin:13px 0}a{color:#315b70;text-decoration:none;border-bottom:1px solid #c8d7df}small,.date{color:#666;font-size:15px}.equation{text-align:center;font-size:20px;line-height:1.9;margin:21px 0;padding:6px 8px;overflow-x:auto;white-space:nowrap}.result{border-left:3px solid #7295a2;padding-left:18px}table{width:100%;border-collapse:collapse;font-size:16px;line-height:1.7;margin:22px 0}th,td{padding:11px 10px;text-align:left;vertical-align:top;border-bottom:1px solid #d9ddd9}th{font-weight:600;border-top:1px solid #939b98}footer{margin-top:40px;padding-top:17px;border-top:1px solid #d9ddd9;font-size:15px;color:#666}@media(max-width:600px){main{margin:28px auto;padding:0 20px 40px}body{font-size:17px}h1{font-size:26px}h2{font-size:21px}table{font-size:15px}.equation{font-size:18px}}@media print{body{background:white;font-size:11pt}main{margin:0;padding:0;max-width:none}h2{break-after:avoid}.equation,table{break-inside:avoid}a{color:inherit}}
</style></head><body><main>
<h1>半离散 DLW：一般场可积性的研究进展</h1>
<div class="date">2026 年 10 月 11 日 · 有限周期格点，连续周期空间</div>
<p class="result">已建立任意平均通量下的中心化守恒层级、任意有限奇前缀的真实共同解，以及明确权重下的全频线性稠密性。一般物理场上的完整无限维刘维尔定理仍未证成。</p>
<p>原方程以 U、w 表示。Π 是 M 个周期格点的平均，c=Πw 是原方程强制守恒的量；q=Π(Uw)=Γ(t) 是空间常数。以下始终保留实际平均兼容，不以二格点特例代替全 M 场。</p>

<h2>1. 任意 Γ(t) 的守恒层级</h2>
<p>当 c≠0，令 p=U−ΠU、s=w−c，P 为空间平移动量。物理 Hamiltonian 的准确分解为</p>
<div class="equation">K<sub>Γ</sub> = K<sub>0</sub> + (Γ/c)P − hMLΓ²/(2c).</div>
<p>若 a′(t)=Γ(t)/c，则零通量规范下的真实解经 x↦x−a(t)、U↦U+a′(t) 得到所需物理解；此对应可逆。因此无需先固定 Γ。瞬时标量 Lax 算子应中心化为</p>
<div class="equation">Ĉ<sub>n</sub> = (1/n) Tr (L<sub>Γ</sub>−Γ/(2c))<sup>n</sup> = C<sub>n</sub><sup>0</sup>.</div>
<p>这些泛函沿任意 Γ(t) 的实际解守恒，并继承零通量规范下的形式对合。未中心化谱迹一般随 Γ 漂移。实际 Floquet 数据还须同时中心化谱参数和连续空间乘子；形式留数迹不直接给出固定周期边界下的实际等谱。<a href="../刘维尔可积性/research/unfixed_flux_hierarchy_20261011.md">全 M 推导</a>。</p>

<h2>2. 真实共同解与辛结构</h2>
<p>剪切坐标 v=p+Rs/2 中，全阶奇谱 Hamiltonian 场具有常系数最高部。若 G=hMc/4，</p>
<div class="equation">X<sub>Cₙ</sub>(v,s) = (D<sup>n+1</sup>v, (−1)<sup>n</sup>D<sup>n+1</sup>s)/(8G) + R<sub>n</sub>,</div>
<p>其中余项微分阶至多 n。对每个奇 n，可在辅助时间规定相反方向的混合端点，用高阶热半群的可积平滑核构造真实解；窄复时间菱形中的解析收缩给出中心唯一性。逐层构造得到 K、P、C₃、…、C₂N₋₁ 的真实共同局部流，其输入仍是一般光滑函数。</p>
<p>原二阶混合域的拉回形式已证弱非退化；新增高阶共同域目前具有闭的兼容拉回形式和 Hamilton 身份。其弱非退化性仍需端点唯一性或另一种证明。每个有限前缀上的积分块可独立，但全部无限层级共用的非平凡函数域尚未建立。<a href="../刘维尔可积性/research/mixed_independent_review_20261011.md">证明与适用条件</a>。</p>

<h2>3. 零平均分支的约束层</h2>
<p>当 c=0，原方程进一步强制 Γ′=0；Γ 随初值改变，是动量而非 Casimir。写 U=b+p、w=s，q=Π(ps)，则</p>
<div class="equation">q<sub>t</sub> = −bq<sub>x</sub> − 2qb<sub>x</sub> + Dχ, &nbsp; χ = −2e + q<sub>x</sub>.</div>
<table><thead><tr><th>分支</th><th>已建立的结构</th><th>仍需推进</th></tr></thead><tbody>
<tr><td>Γ≠0</td><td>非恒定 q 模的 Dirac 约束；平方根形式谱迹的对合与守恒；每个 M、每个有限积分块在正负 Γ 扇区均有相对开独立区。</td><td>一般非线性真实共同流；任意固定均值叶上的泛性与完备性。</td></tr>
<tr><td>Γ=0，χ=κ≠0</td><td>主、次约束交叉块 −3κD 可逆；一致性强制 κ′=0，并给出二阶有限 jet 的 b 闭合；三次根形式谱迹可在相应约束层定义。</td><td>该层的真实时间流、弱辛商与谱完备性；κ=0 的更深层另需约束分析。</td></tr>
</tbody></table>
<p>Γ≠0 的独立性见证只用于检验完整场中的协向量，不把见证族作为替代动力系统。κ≠0 层在 M≥3 有非恒定函数点；零动量约束的空间平移方向必须约去。<a href="../刘维尔可积性/research/c0_independent_review_20261011.md">Γ≠0 分支</a>；<a href="../刘维尔可积性/research/singular_branch_review_20261011.md">零通量约束层</a>。</p>

<h2>4. 完整 Floquet 数据的线性可恢复性</h2>
<p>有限个标量 Lax 系数在实际物理像上已有非线性局部状态逆。完整、固定基点的 Floquet 单值矩阵变分进一步恢复全部非零 Fourier 物理方向；只保留谱特征值会在均匀态丢失一阶信息。</p>
<p>设 δ=hc/8、空间周期为 L。在明确的小背景条件</p>
<div class="equation">0 &lt; |δ| &lt; (π/L) tan(π/(2M))</div>
<p>下，共振通道的端点可分离；用正的指数衰减权重，谱层级的多项式频率差在全频通道空间中稠密。证明通过指数矩、解析 Fourier 唯一性和端点无重叠完成。这是全频线性闭包，仍需将实际谱通道与物理辛形式匹配，并建立非线性逆谱及最大各向同性。<a href="../刘维尔可积性/research/spectral_independent_review_20261011.md">全频证明</a>。</p>

<h2>5. 当前接续方向</h2>
<p>主线是把真实共同解域、完整 Floquet 局部逆和物理辛结构接起来：首先证明新增共同域的弱非退化及无限层级一致域，然后构造非线性谱坐标，在同一实际相空间内证明守恒族最大各向同性。零平均约束分支与非周期平均场继续分别推进。</p>
<footer>完整证据入口：<a href="../刘维尔可积性/research/STATE.md">研究状态</a> · <a href="../刘维尔可积性/research_checkpoint.md">研究检查点</a> · <a href="../刘维尔可积性/GOAL.md">持续目标</a>。有限符号检查支持系数与恒等式；全 M、全阶结论以对应证明为依据。</footer>
</main></body></html>'''

def latest_html(html):
    html = html.replace("任意有限奇前缀的真实共同解，以及明确权重下的全频线性稠密性", "全部谱迹任意有限前缀的真实共同弱辛域、无限相容共同解，以及全频线性辛匹配与最大性")
    html = html.replace("逐层构造得到 K、P、C₃、…、C₂N₋₁ 的真实共同局部流，其输入仍是一般光滑函数。", "偶谱迹通过虚时间 Fourier 混合构造与复反射得到真实实时间轨道；奇、偶构造可交错迭代，建立全部谱迹任意有限前缀的真实共同局部流，输入仍是一般光滑函数。")
    html = html.replace("原二阶混合域的拉回形式已证弱非退化；新增高阶共同域目前具有闭的兼容拉回形式和 Hamilton 身份。其弱非退化性仍需端点唯一性或另一种证明。每个有限前缀上的积分块可独立，但全部无限层级共用的非平凡函数域尚未建立。", "所有可缩窗口合并后的有限共同 germ 域已证弱辛非退化：共同缩窗排除内部切向的虚假核，实际切向密度与原形式连续性给出非退化。进一步逐层选择短窗，控制已固定有限复合的全部放大，得到非平凡的无限相容共同解；这些状态在每个有限前缀像中稠密，共享各时间坐标的正宽。无限域的统一辛切向结构仍待证。")
    html = html.replace("<h2>4. 完整 Floquet 数据的线性可恢复性</h2>", "<h2>4. 全频谱坐标与线性最大性</h2>")
    html = html.replace("证明通过指数矩、解析 Fourier 唯一性和端点无重叠完成。这是全频线性闭包，仍需将实际谱通道与物理辛形式匹配，并建立非线性逆谱及最大各向同性。", "证明通过指数矩、解析 Fourier 唯一性和端点无重叠完成。完整共振坐标可准确拉回原物理辛形式，给出 Hˢ 与规范序列空间 hˢ⁺½ 的有界线性对应；全部谱迹在线性/二次模型中生成最大各向同性闭包，并可放在共同真实线性流域上。仅奇谱迹加一个动量会漏掉独立相位方向，偶谱迹因此不可省略。原非线性场的逆谱与最大各向同性仍未建立。")
    html = html.replace("主线是把真实共同解域、完整 Floquet 局部逆和物理辛结构接起来：首先证明新增共同域的弱非退化及无限层级一致域，然后构造非线性谱坐标，在同一实际相空间内证明守恒族最大各向同性。", "主线是把已有真实无限相容解域与谱坐标接起来：先建立该无限域的统一弱辛切向结构，再构造非线性谱坐标，在同一实际相空间内证明守恒族最大各向同性。有限域弱辛性、无限域点态密度和线性谱最大性分别已得到，它们之间的非线性连接仍需证明。")
    html = html.replace("Γ≠0 的独立性见证只用于检验", "次约束层的独立二审核对通过，并补出 χ 三次根密度的显式 Diff 平坦化；自由平移层上的静态弱辛商因此可具体构造。Γ≠0 的独立性见证只用于检验")
    html = html.replace("全阶奇谱 Hamiltonian 场", "全阶谱 Hamiltonian 场")
    html = html.replace("该层的真实时间流、弱辛商与谱完备性；κ=0 的更深层另需约束分析。", "全 M 真实共同流与谱完备性；κ=0 的更深层另需约束分析。")
    m3 = '''<p>零通量 M=3 分支已有原物理双向光滑局部流：在 r*&gt;0、d=hr*/8、a*&gt;2d、a*≠6d 的实非共振背景附近，最小三阶分母精确化为</p>
<div class="equation">u<sub>t</sub>=−2z<sub>x</sub>, &nbsp; z<sub>t</sub>=u<sub>xxx</sub>/6+2uu<sub>x</sub>/3.</div>
<p>以 Ψ=z+iu<sub>x</sub>/(2√3) 改写为无导数损失的半线性 Schrödinger 方程，得到所有光滑阶共用的非零时间窗。实标号 Floquet 旗标、一般六因子逆交换及原 PDE 的直接 Lax 微分将其回拉为原方程；任意平均共同场 B(t) 通过空间平移和 U 加量恢复。初值可为图内一般兼容函数，不要求留在两幅值族中。这个图尚不覆盖其他 M 或全部组件平均叶。<a href="../刘维尔可积性/research/singular_m3_actual_flow_20261011.md">实际流证明</a>。</p>
<p>全 M 非恒定正则 κ 层的完整主约束消元进一步给出主符号特征多项式 (λ²+1/3)(λ²−1)<sup>M−3</sup>。因此 M=3 留下一对振荡通道，M&gt;3 还保留成对热型通道；此主符号结果本身不代替一般非线性流存在性。</p>'''
    html = html.replace("<h2>4. 全频谱坐标与线性最大性</h2>", m3 + "\n<h2>4. 全频谱坐标与线性最大性</h2>")
    html = html.replace("原非线性场的逆谱与最大各向同性仍未建立。", "固定背景原始采样还有可检验的非线性尾项：解析有限 Fourier 场也可产生 k<sup>−5/2</sup> 的规范谱坐标，使高正则同阶逆映射失败。后续须跟踪真实 holonomy、移动谱框架或减去渐近项。原非线性场的逆谱与最大各向同性仍未建立。")
    html = html.replace("无限域的统一辛切向结构仍待证。", "全部有限守恒块的独立见证已提升为可数相容的光滑参数族。无限域的统一辛切向结构仍待证。")
    html = html.replace("无限域的统一辛切向结构仍待证。", "强混合复参数域进一步取得真正的无限弱辛结构：相对延拓精确保留既有基点，同基点真实切向稠密，坐标轴与抛物线延拓排除内部虚假核。全部谱迹在该域上具有真实逐坐标共同 Hamiltonian 时间局部流。")
    html = html.replace("先建立该无限域的统一弱辛切向结构，再构造非线性谱坐标", "在已证强无限弱辛域上构造非线性谱坐标")
    html = html.replace("有限域弱辛性、无限域点态密度和线性谱最大性分别已得到，它们之间的非线性连接仍需证明。", "强无限域的合法弱辛结构与线性谱最大性已得到，完整非线性谱逆及守恒族极大性仍需证明。")
    html = html.replace("固定背景原始采样还有可检验的非线性尾项：解析有限 Fourier 场也可产生 k<sup>−5/2</sup> 的规范谱坐标，使高正则同阶逆映射失败。后续须跟踪真实 holonomy、移动谱框架或减去渐近项。", "固定背景采样有非线性尾项：companion 框架的 k<sup>−5/2</sup> 尾阻断 s≥3/2 的同阶映射，未校准原始框架的 k<sup>−3/2</sup> 尾更阻断 s≥1/2。已证明开放 C<sup>R</sup> 状态域上的首项重整化解析引理，序列正则性提高一阶；同阶 Sobolev 逆仍需统一余项估计。")
    phase = '''<p>该无限域采用 diffeology。环境空间是固定组件 Casimir 叶上的周期 C<sup>∞</sup> Fréchet 空间；以 Q=s、P=D<sup>−1</sup>(p+Rs/2) 的固定均值版本表示其切向。一个有限维参数图由同一实际中心链 E<sub>j</sub> 和光滑源映射 ψ<sub>j</sub>(a) 定义：</p>
<div class="equation">p(a)=E<sub>0</sub>ψ<sub>0</sub>(a), &nbsp; ψ<sub>j−1</sub>(a)=E<sub>j</sub>ψ<sub>j</sub>(a).</div>
<p>每个时间坐标具有随全部后续前缀保留的正复内窗口。参数图生成其 D 拓扑；没有证明它等于环境子空间拓扑，也没有把此域称为 Banach 或 Fréchet 流形。内部切空间取所有参数速度及其链式关系的代数余极限。相对延拓证明这个内部切空间单射到物理速度空间，且在同一基点的像稠密。连续物理形式 Ω=h∫ΣdQ∧dP 因而拉回为闭、弱非退化的图上二形式。</p>
<p>逐坐标实际时间流在同一类图中光滑，故其内部速度满足 ι<sub>Xₙ</sub>Ω=dC<sub>n</sub>，并由弱非退化唯一确定。所有守恒量的共同水平集可取子空间 diffeology，有限共同 Hamiltonian 轨道保持其中；尚未证明水平集是正则流形、其切空间等于全部 dC<sub>n</sub> 的共同核，或等于这些轨道。这个差别正是非线性 Liouville 完备性还需解决的部分。</p>'''
    html = html.replace("<h2>3. 零平均分支的约束层</h2>", phase + "\n<h2>3. 零平均分支的约束层</h2>")
    return html


if __name__ == "__main__":
    HTML = latest_html(HTML)
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(HTML, encoding="utf-8")
    print(f"Saved {TARGET.relative_to(ROOT)} ({len(HTML)} characters)")
