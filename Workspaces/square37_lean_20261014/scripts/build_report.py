"""Build the standalone, offline research report from the retained certificate."""
import json
from fractions import Fraction
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT.parents[1] / 'report' / 'square37_cantrell_lean_20261014.html'
cert = json.loads((ROOT/'certificates/n37_rational_sat.json').read_text(encoding='utf-8'))
L = float(Fraction(cert['L']))
parts = ['<svg viewBox="-0.16 -0.16 6.92 6.92" role="img" aria-labelledby="packing-title"><title id="packing-title">Cantrell 37块布局的已核验有理见证，按源证书编号</title>',
         f'<rect x="0" y="0" width="{L}" height="{L}" fill="#fff" stroke="#243a43" stroke-width=".025"/>']
for square in cert['squares']:
    i = square['i']+1
    cx,cy,ux,uy = (float(Fraction(square[k])) for k in ('cx','cy','ux','uy'))
    vertices = [(cx+a*ux-b*uy,L-(cy+a*uy+b*ux)) for a,b in [(-.5,-.5),(.5,-.5),(.5,.5),(-.5,.5)]]
    fill = '#eed3b4' if 10<=i<=15 else '#bbd6df' if 19<=i<=24 else '#d2bddb' if i==36 else '#edf0ee'
    p = ' '.join(f'{x:.12f},{y:.12f}' for x,y in vertices)
    parts.append(f'<polygon points="{p}" fill="{fill}" stroke="#4e5f62" stroke-width=".012"/>')
    parts.append(f'<text x="{cx:.10f}" y="{L-cy+.045:.10f}" text-anchor="middle" font-size=".14" fill="#172a30">{i}</text>')
parts.append('</svg>')
svg = ''.join(parts)
(ROOT/'analysis/cantrell37.svg').write_text(svg, encoding='utf-8')

status_path = ROOT/'STATUS.json'
status = json.loads(status_path.read_text(encoding='utf-8')) if status_path.exists() else {}
completed = status.get('conditional_minimax_lean_passed', False)
minimax_state = '已通过 Lean' if completed else '精确证书已完成，Lean 整合中'
receipt = status.get('final_receipt', '')
receipt_html = f'<a href="../Workspaces/square37_lean_20261014/{escape(receipt)}">最终编译记录</a>' if receipt else '最终编译记录待整合'

html = '''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>37方块：Cantrell构造与条件下界的Lean验证</title>
<style>
:root{color-scheme:light}*{box-sizing:border-box}body{margin:0;background:#f6f5f0;color:#1d3035;font-family:Georgia,"Noto Serif SC","Microsoft YaHei",serif;line-height:1.8}main{max-width:1050px;margin:0 auto;padding:42px 28px 70px}h1{font-size:1.9rem;line-height:1.45;font-weight:600;margin:8px 0 18px}h2{font-size:1.28rem;margin:36px 0 10px;border-top:1px solid #ccd4d1;padding-top:22px}p{margin:10px 0}a{color:#215d77;text-underline-offset:3px}code{font-size:.86em;overflow-wrap:anywhere}small,.meta,figcaption{color:#52646a;font-size:.91rem}.status{border-left:4px solid #85622f;background:#eee8d9;padding:14px 18px}.eq{font-family:"Cambria Math",Georgia,serif;font-size:1.15rem;text-align:center;overflow-x:auto;padding:15px 5px;margin:12px 0}.layout{display:grid;grid-template-columns:minmax(300px,1fr) minmax(300px,1fr);gap:30px;align-items:center}figure{margin:18px 0}svg{display:block;width:100%;height:auto}table{width:100%;border-collapse:collapse;margin:18px 0;font-size:.94rem}th,td{padding:10px 12px;text-align:left;border-bottom:1px solid #ccd4d1;vertical-align:top}th{font-weight:600;background:#e8eeeb}.scroll{overflow-x:auto}.note{color:#475c61}ol{padding-left:1.5rem}footer{border-top:1px solid #ccd4d1;margin-top:32px;padding-top:16px;font-size:.9rem} @media(max-width:720px){main{padding:24px 17px}h1{font-size:1.5rem}.layout{display:block}table{min-width:570px}}
</style><main>
<div class="meta">研究记录 · 2026年10月14日 · 复用 DLW 的 Lean 4.34.0 / Mathlib 环境</div>
<h1>37方块：Cantrell构造与条件下界的Lean验证</h1>
<p class="status"><strong>全局最优性尚未证明。</strong>原始目录将37块问题标为 open，报告区间为 6.44 ≤ s(37) ≤ 6.59861960924437。本项目严格核验已知构造，并从其接触链建立可形式化的必要下界；尚未排除全部其他布局。</p>
<div class="layout"><figure>SVG_PLACEHOLDER<figcaption>从有理证书绘制，编号与源文件一致。橙、蓝两组分别对应理想构造的相反倾角，紫色为中央块36。图形用于阅读，几何真实性由精确证书核验。</figcaption></figure><div>
<h2>已核验的构造</h2><p>在边长</p><div class="eq">L<sub>rat</sub> = 659861960924437 / 10<sup>14</sup></div>
<p>的正方形内存在37个实数单位正方形。每块可独立平移和旋转；闭方块两两不相交。</p><p>Lean 逐项证明37项单位性、148条容器约束和666对严格分离。另以 Python 有理数重算666对多边形交集，全部为空。</p>
<p class="note">这是 Cantrell 已知构造的认证，不是新纪录。源证书还给出更紧的有理边长 6.598619609244360116244356658771；本次 Lean 采用目录公开上取整值。</p></div></div>
<h2>由接触链得到的两条必要下界</h2>
<p>设两组倾角为 ±θ，c = cos θ、s = sin θ，0 ≤ s ≤ c，中央块为精确45°。在明确列出的有向分离与外围轴向链条件下，得到</p>
<div class="eq">(c+s)L ≥ 3+4c+5s,<br>2(1+s(c−s))L ≥ 6+8c+10s(c−s)+√2.</div>
<p>第一条来自13条支撑与墙条件的加权求和；第二条来自左右两条支撑链及中央对角线间距。两者已在 <code>CantrellSupports.lean</code> 中证明，全部假设显式保留。右半部通过坐标反射表达所需条件，并不假定整个布局镜面对称。</p>
<p>记两个商分别为 F₁(θ)、F₂(θ)。令 q = tan(θ/2)，其交点满足</p>
<div class="eq">(4−√2)q<sup>4</sup> + (12−2√2)q<sup>2</sup> − √2 = 0.</div>
<p>交点约为 θ = 42.0866074742°。有理区间计算严格隔离该交点；正系数 Bernstein 恒等式证明相关区间内 F₂ 下降，F₁ 在交点右侧上升。因此，在 q ∈ [0,√2−1]，即 θ ∈ [0,π/4] 的支持模型内，交点是两支撑函数最大值的全局最小点。<strong>形式化状态：MINIMAX_STATE。</strong></p>
<p>最终整合定理 <a href="../Workspaces/square37_lean_20261014/lean/FinalBridge.lean"><code>conditional_branch_lower_bound</code></a> 证明：对任意满足 0 ≤ s ≤ c、c²+s²=1 的共同方向，以及满足上述明确支撑条件的坐标数组，必有 L ≥ L*。证明覆盖整个允许方向区间，未把方向固定为数值优化所得角度。</p>
<p>当前精确有理37块见证略高于理想代数端点，其中央角也只是极接近45°。因此，支撑模型的最小值与完整37块在端点处的可行性仍须区分。</p>
<h2>精确代数端点</h2>
<p>两条支撑等式消元得到 Q(L,√2)=0，其中</p>
<div class="eq">Q(L,r)=6L⁴−(208+64r)L³+(2058+850r)L²<br>−(7936+3658r)L+11163+5502r.</div>
<p>其共轭乘积是目录给出的八次多项式：</p>
<div class="eq">P(L)=36L⁸−2496L⁷+59768L⁶−733760L⁵+5289248L⁴<br>−23462672L³+63458276L²−96673872L+64068561.</div>
<p>Lean 证明 P 在下列区间内有唯一根 L*，排除了共轭因子，并证明 Q(L*,√2)=0：</p>
<div class="eq">6.59861960924436 &lt; L* &lt; 6.59861960924437.</div>
<p>在该区间内，只要共同方向满足单位性及两条支撑取等，其 L 就等于 L*。独立有理区间程序进一步定位到 6.5986196092443601161783704626783488043909 与末位增加1之间；这段更细夹逼属于精确程序记录，不冒称已在 Lean 中逐位重放。</p>
<h2>从17块证明可复用什么</h2>
<p>17块页面包含两条不同证据：T-153 是仍带义务的候选证明；T-154 的 <a href="https://github.com/ofitzharding/sq17-lean">sq17-lean</a> 声称完整证明，并明确使用13,343项 native_decide 事实。本项目审核了可获得源码的覆盖、重编号与最终装配接口；未下载约1.963 GB的全部生成证书，也未独立重建其完整证明。</p>
<p>已为任意块数重写并核验六个有限覆盖引理：完整性需要“每行有效、无重复、计数正确”共同成立；容量为一给出单射分配；占用集相等给出真实重编号置换。37块尚未实例化这些条件。</p>
<div class="scroll"><table><thead><tr><th>证明环节</th><th>当前结论</th><th>实际范围</th></tr></thead><tbody>
<tr><td>有理构造 → 实数几何</td><td>Lean 已通过</td><td>严格可行上界；闭方块不交</td></tr>
<tr><td>接触链 → 两支撑不等式</td><td>Lean 已通过</td><td>指定方向、有向分离分支</td></tr>
<tr><td>支撑等式 → 目录代数根</td><td>Lean 已通过</td><td>区间内唯一根；排除共轭根</td></tr>
<tr><td>半角交点、支撑函数 minimax</td><td>MINIMAX_STATE</td><td>两支持函数模型，不能自动覆盖其他骨架</td></tr>
<tr><td>有限覆盖与重编号</td><td>六个通用引理通过</td><td>无37块专用覆盖证书</td></tr>
<tr><td>任意37块布局的全局下界</td><td>未证明</td><td>仍需完备覆盖、排除与端点邻域归约</td></tr>
<tr><td>代数端点处的完整布局</td><td>未形式化</td><td>现有有理证书只给端点上方的可行值</td></tr>
</tbody></table></div>
<h2>全局证明尚缺的核心</h2>
<p><code>ResearchTarget.lean</code> 将目标明确写为所有实数 L 上的等价式：存在37块合法布局，当且仅当 L* ≤ L。该命题只被定义，没有被当作已证定理或公理使用。</p>
<p>一个具体的下一步是先核验容量覆盖：以 U = 6.59861960924437 为搜索上界，将中心所在的 [1/2,U−1/2]² 分为8×8格，格宽 w = (U−1)/8 满足 2w² &lt; 1。每块含半径1/2的内圆，因此每格至多一个中心。但占用集数 C(64,37) = 846636978475316672，即使按正方形的8个对称约去，仍至少有105829622309414584个轨道。这一基线的几何解释尚未接入 Lean；它表明需要更强容量单元与自适应区间剪枝，而非直接列出全部组合。</p>
<p>全局搜索还必须为每块保留独立方向，包括正、负倾角。当前支撑模型的共同倾角和第一八分区参数化，不能充当任意37块布局的方向覆盖。</p>
<ol><li>为任意小于 L* 的布局建立几何容量覆盖与完整占用分类；若用对称性缩减，需证明恢复全部原布局。</li><li>生成并形式核验各类排除证书，将剩余布局完整归约到端点附近的可分析分支。</li><li>把局部支撑结论接到该全局归约，并给出 L* 处完整37块的精确可行构造。</li></ol>
<p>因此，本轮所得是构造认证、代数识别与条件下界的证明基础。全局37块最优性的关键内容仍是对所有其他布局的完备排除。</p>
<h2>核验与复用入口</h2>
<p>新证明使用 DLW 现有 Lean 4.34.0、Mathlib 提交 <code>5ed2965256430c3649e86755f9576b54eca72435</code>。关键定理的公理依赖限于 <code>propext</code>、<code>Classical.choice</code>、<code>Quot.sound</code>；新文件没有占位证明、自定义公理或 <code>native_decide</code>。</p>
<p><a href="../Workspaces/square37_lean_20261014/lean/All.lean">Lean 总入口</a> · RECEIPT_LINK · <a href="../Workspaces/square37_lean_20261014/STATUS.json">项目状态与运行信息</a> · <a href="../Workspaces/square37_lean_20261014/analysis/n37_exact_verification.json">有理几何核验</a> · <a href="../Workspaces/square37_lean_20261014/analysis/proof17_review.json">17块证明审查</a></p>
<footer>来源：<a href="https://jlevy.github.io/squares/cases/37.html">37块目录</a>；<a href="https://jlevy.github.io/squares/cases/17.html">17块目录</a>。37块资料固定于 <code>b8c930338ee3577a43faccb52472c6975ab7eccd</code>；17块 T-154 源码固定于 <code>0a7167efa8dcae7fa73855890630fb7e2de550ed</code>。来源、代码与证书哈希保存在项目中。</footer>
</main></html>'''
html = html.replace('SVG_PLACEHOLDER',svg).replace('MINIMAX_STATE',minimax_state).replace('RECEIPT_LINK',receipt_html)
REPORT.write_text(html,encoding='utf-8')
print(REPORT)
