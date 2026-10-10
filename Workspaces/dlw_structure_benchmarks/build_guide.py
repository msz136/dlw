from pathlib import Path
import json, hashlib, re

ROOT = Path('C:/Users/msz/aca')
W = ROOT / 'Workspaces/dlw_structure_benchmarks'
R = ROOT / 'Paper/refs/dlw_structure_benchmarks'
papers = [
 ('02_Conservative_BBM_SISC','Mitsotakis, Ranocha, Ketcheson & Süli','A Conservative Fully Discrete Numerical Method for the Regularized Shallow Water Wave Equations','SIAM Journal on Scientific Computing 43 (2021), B508–B537','https://doi.org/10.1137/20M1364606','https://arxiv.org/abs/2009.09641','先读：§4.3、图6、§6；下载版第15–16、22、25页。','研究问题是长时间传播中能否保住孤子的形状。作者把空间混合有限元与时间 relaxation Runge–Kutta 联合构造，验证守恒、收敛，并分别测量振幅、相位、平移对齐后的形状误差。图6显示其测试条件下，守恒方法的振幅和形状误差保持较小，相位误差增长较缓。','我们应借鉴误差的分解和随时间展示。时间算法在这里有明确职责：延续空间半离散的能量守恒；这不同于单纯排列 Euler、RK4、CN 的误差。文中的能量、边界条件和稳定性结论不能直接搬给 DLW。'),
 ('07_Linearly_implicit_SISC','Eidnes & Li','Linearly Implicit Local and Global Energy-Preserving Methods for PDEs with a Cubic Hamiltonian','SIAM Journal on Scientific Computing 42 (2020)','https://doi.org/10.1137/19M1272688','https://arxiv.org/abs/1907.02122','先读：§5、表1与表3、图7–8、§6。','研究问题是降低保能量方法每一步的求解成本。文章提出局部与全局两类线性隐式方法，并与全隐式方法比较。在一维 KdV 与二维 Zakharov–Kuznetsov 上考察收敛、能量、波形、空间振荡和耗时。二维实验尤其说明：相同点数下的波形质量与达到相同质量所需的成本，要一起看。','这是最适合参考二维结果组织的一篇。PE/PF/FD 可以比较精度—成本和空间分辨能力，而非寻找三者各自获胜的参数。该文的二维模型不是可积系统；借鉴的是评价逻辑，不是声称它与我们的理论相同。'),
 ('03_Error_growth','Ranocha, Quezada de Luna & Ketcheson','On the Rate of Error Growth in Time for Numerical Solutions of Nonlinear Dispersive Wave Equations','Partial Differential Equations and Applications (2021)','https://doi.org/10.1007/s42985-021-00126-3','https://arxiv.org/abs/2102.07376','先读：§1–2、§5、§7–8；代码链接见下。','研究问题是守恒是否改变孤子数值误差的时间增长规律。多个非线性色散模型实验呈现守恒方法近线性、非守恒方法近二次的增长；线性方程对照和质量不守恒的试验用于检验机制。二维浅水实验仍有收益，但正文明确其增长规律不完全符合前述线性/二次模式。','这是问题设计参考，不列作顶刊代表。DLW 是否有同样规律尚未验证；可积、保能量、保辛是不同性质。应先明确我们的全离散程序实际保留哪条结构，再决定是否做这类长时间实验。'),
 ('05_CH_integrable','Ohta, Maruno & Feng','An integrable semi-discretization of the Camassa–Holm equation and its determinant solution','Journal of Physics A: Mathematical and Theoretical 41 (2008), 355205','https://doi.org/10.1088/1751-8113/41/35/355205','https://arxiv.org/abs/0805.2843','先读：引言、数值部分、§6。','构造可积半离散方程、行列式解和连续极限，并把离散结构用于自适应网格计算。数值部分还展示一般初值演化产生孤子的过程。','它与我们的理论—数值路线很接近。可积半离散本身是理论结果，精确离散解也可以充当求解器的独立检验基准；不必通过短时误差全面压过普通差分来证明其存在价值。'),
 ('04_SP_integrable','Feng, Maruno & Ohta','Integrable discretizations of the short pulse equation','Journal of Physics A: Mathematical and Theoretical 43 (2010), 085203','https://doi.org/10.1088/1751-8113/43/8/085203','https://arxiv.org/abs/0912.1914','先读：§3与§5。','以双线性和行列式结构构造半离散、全离散系统及多孤子解，说明连续极限，并由半离散系统构造自适应移动网格。环孤子提供了与普通单值图像不同的测试对象。','适合参考理论到算法的衔接，不宜把其示例性实验当作充分的优越性证明。DLW 当前算例若无相应几何困难，就不能借用环孤子计算的优势作为自己的动机。'),
 ('06_Coupled_SP','Feng, Chen, Chen, Maruno & Ohta','Integrable discretizations and self-adaptive moving mesh method for a coupled short pulse equation','Journal of Physics A: Mathematical and Theoretical (2015)','https://waseda.elsevierpure.com/en/publications/integrable-discretizations-and-self-adaptive-moving-mesh-method-f/','https://arxiv.org/abs/1508.00243','先读：§4–5、图2–6。','给出耦合系统的可积离散与行列式解，通过 hodograph 变换把均匀计算网格变成随时间运动的物理网格。数值图同时展示波形、网格和误差。','适合学习如何把两个场与网格运动解释清楚。它仍以解析解符合度为主要展示，不能替代精度—成本或稳定性验证。'),
]

head='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DLW：研究定位与数值论证参考</title><style>
body{max-width:960px;margin:48px auto;padding:0 24px;color:#20242b;background:#fff;font:17px/1.85 Georgia,"Noto Serif SC","Microsoft YaHei",serif}h1{font-size:30px;line-height:1.4}h2{font-size:23px;margin-top:2em}h3{font-size:19px;line-height:1.6}a{color:#145a83;overflow-wrap:anywhere}p{margin:.7em 0}.meta{font-size:14px;color:#646b73}.table{overflow:auto}table{border-collapse:collapse;width:100%;font-size:15px}th,td{text-align:left;padding:12px;border-bottom:1px solid #d8dde2;vertical-align:top}article{margin:2em 0}strong{font-weight:700}@media(max-width:600px){body{padding:0 16px;margin:24px auto;font-size:16px}h1{font-size:25px}}@media print{body{max-width:none;margin:0}article{break-inside:avoid}}</style><main>
<h1>DLW：研究定位与数值论证参考</h1><p class="meta">2026年10月10日 · 六篇公开版全文与一篇补充阅读 · 本次未修改论文或运行新实验</p>
<p><strong>当前工作属于可积系统与结构保持数值方法的交叉。</strong>理论部分研究离散后能保留怎样的方程结构；数值部分研究这些构造是否能形成可靠、有效的求解方法。短时间的终点误差表可以说明特定配置的准确程度，尚不足以解释可积离散的数值价值。</p>
<h2>期刊应按研究问题区分</h2><p>以下是值得对标的代表性高水平期刊，不是统一排名，也不是对当前稿件录用可能性的判断。数值分析与数学物理的评价重点不同。</p>
<div class="table"><table><tr><th>方向</th><th>优先关注</th><th>与我们工作的关系</th></tr>
<tr><td>严格数值分析</td><td><a href="https://epubs.siam.org/journal/sinum/editorial-policy">SIAM Journal on Numerical Analysis</a>；<a href="https://link.springer.com/journal/211/aims-and-scope">Numerische Mathematik</a></td><td>数值方法的收敛、稳定性与误差理论。局部一致性或精确孤子族的二阶极限，不等于一般初值问题求解器的收敛定理。</td></tr>
<tr><td>科学计算方法</td><td><a href="https://epubs.siam.org/journal/sisc/editorial-policy">SIAM Journal on Scientific Computing</a>；Journal of Computational Physics</td><td>有解释力的算法改进、结构性质和准确性—成本证据。当前最值得参考的实验设计来自这一支。</td></tr>
<tr><td>数学物理与非线性理论</td><td><a href="https://link.springer.com/journal/220/aims-and-scope">Communications in Mathematical Physics</a>；<a href="https://publishingsupport.iopscience.iop.org/journals/nonlinearity/about-nonlinearity/">Nonlinearity</a></td><td>可积结构及非线性问题的实质数学进展。CMP 是高标准数学物理标杆，但常规“构造＋几个算例”不是其定位。</td></tr>
<tr><td>直接相关的专业期刊</td><td>Physica D；Journal of Physics A: Mathematical and Theoretical；Journal of Scientific Computing</td><td>分别偏非线性动力学、数学物理、计算方法。下面的 J. Phys. A 文献最接近我们的技术路线；不把这些期刊一概称作顶刊。</td></tr></table></div>
<h2>先读三篇：让实验回答问题</h2>'''
body=head
for i,(slug,authors,title,journal,doi,arxiv,read,findings,transfer) in enumerate(papers):
 if i==3:body+='<h2>再读三篇：与可积半离散直接相接</h2>'
 body+=f'<article><h3>{i+1}. {title}</h3><p class="meta">{authors}<br>{journal} · <a href="{doi}">出版记录</a> · <a href="{arxiv}">arXiv记录</a> · <a href="../Paper/refs/dlw_structure_benchmarks/{slug}.pdf">已下载PDF（arXiv版）</a></p><p><strong>{read}</strong></p><p>{findings}</p><p>对 DLW 的启发：{transfer}</p></article>'
body+='''<p>误差增长论文的公开代码：<a href="https://github.com/ranocha/Dispersive-wave-error-growth-notebooks">Dispersive-wave-error-growth-notebooks</a>。Eidnes–Li 的出版页还附有方法与参照方法的实现。</p>
<h2>一篇直接追问“结构有什么用”的经典文章</h2><p>Ascher 与 McLachlan，<a href="https://link.springer.com/article/10.1007/s10915-004-4634-6">On Symplectic and Multisymplectic Schemes for the KdV Equation</a>，Journal of Scientific Computing 25 (2005), 83–104。它直接考察结构保持与长期计算质量的关系，讨论紧致 box 离散、粗网格稳定性与非物理振荡。其问题设置值得读：需要辨认具体设计带来的效果，不能只凭“保结构”标签归因。本次核读了出版页摘要与作者版可检索引言；作者PDF链接访问失败，未计入六篇下载。</p>
<h2>我们可以建立怎样的结论</h2><p>下面是据这些文献提出的研究设计建议，不是已经获得的 DLW 实验结论。建议先以“可积半离散的构造与数值实现验证”为主线；在结构收益被验证后，再提升为“具有某种计算优势的方法”。理论与数值贡献可以有不同的强度，不需要强行让 PE、PF、FD 各赢一类算例。</p>
<div class="table"><table><tr><th>要回答的问题</th><th>最直接的证据</th><th>能够支持的结论</th></tr>
<tr><td>离散解是否正确逼近连续解？</td><td>同一谱参数下，半离散精确解与连续精确解随 h 细化的差；固定物理位置并明确重构。</td><td>精确解族的连续极限及相应阶数。</td></tr>
<tr><td>程序是否正确求解半离散模型？</td><td>以半离散精确解为基准，分别缩小 Δx 与 Δt，保持边界与物理变量重构一致。</td><td>区分 y 半离散误差与后续 x、时间离散及重构误差，解释 PE/PF 的实际表现。</td></tr>
<tr><td>保留结构有没有计算收益？</td><td>先找出实际全离散方法保留的守恒式或几何性质；再考察其缺陷与波形、相位误差随时间的变化。</td><td>只有出现对应证据，才能声称结构减少某类漂移或改善长期行为。</td></tr>
<tr><td>自适应网格是否值得？</td><td>同一物理问题与误差区域下，比较达到给定误差所需的自由度、步数、耗时，并展示网格聚集的位置。</td><td>是否以更少资源解析相同孤子结构。</td></tr></table></div>
<p><strong>最近的一步应是把误差来源分清。</strong>我们已经有半离散精确解，这是非常有用的参照。总误差中可能同时包含 y 方向半离散、x 导数近似、时间推进和变量重构的影响；只更换 h=Δx 会把这些效应混在一起。若 PF 较差，先解释它差在哪里，比为它挑一个获胜参数更有论文价值。</p>
<p>已有 T=0.05 试算出现误差快速增长或中止，因此不能直接照搬文献做长时间优势图。需要先辨别连续模型的线性化增长、半离散稳定性、x 方向离散、边界处理和时间稳定性各自的作用。T 的绝对数值跨方程不能直接比较；实验长度应对应波传播距离、孤子宽度或相互作用阶段。</p>
<p>时间算法比较可以有两种明确用途：一是让时间误差足够小，从而判断空间方法；二是验证某种时间推进能否延续已证明的空间结构。若两者均不是目标，Euler/RK4/CN 的独立排行榜可以精简。CN 二阶或对称，并不自动意味着它保留我们的可积结构。</p>
<p>一篇有根据的结论可以围绕“构造了什么、证明了什么、数值实现验证了什么、在哪种成本或稳定性条件下表现如何”展开。现有证据尚未支持 PE/PF 对 FD 的普遍优势；这并不消除半离散系统、Lax 表示和精确解的理论贡献，但它们的新颖性仍需与同类 DLW 工作单独比较。</p>
</main></html>'''
(W/'guide.html').write_text(body,encoding='utf8')
(ROOT/'report/dlw_research_benchmarks.html').write_text(body,encoding='utf8')
manifest=[]
for row in papers:
 p=R/(row[0]+'.pdf'); assert p.read_bytes().startswith(b'%PDF')
 manifest.append(dict(file=p.relative_to(ROOT).as_posix(),title=row[2],journal=row[3],source=row[5],version='arXiv public version',sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
(W/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf8')
for h in re.findall(r'href="(\.\./[^"]+)"',body): assert (ROOT/'report'/h).resolve().exists(),h
print('Verified six PDFs and all local report links.')
