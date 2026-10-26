"""One-time initialization of the integrated manuscript; refuses overwrite."""
from pathlib import Path
import html,json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sections=[
('1','Introduction','引言',[
 ('','', '从连续 DLW 的可积结构与数值逼近需求引出问题；说明格点来源、对称物理场、非线性表示与计算之间的联系。贡献声明在推导核验后定稿。')]),
('2','Bilinear lattice construction and exact solutions','双线性格点构造与精确解',[
 ('2.1','The continuous DLW system and its bilinear representation','固定连续方程、参数与 τ 变换，解释为什么从双线性系统出发。保留一般 λ 作为背景，主构造明确采用 λ=−2。'),
 ('2.2','An unreduced bilinear lattice from the Hirota–Miwa equation','吸收并核验并行线的 Miwa 展开和辅助方向重组，给出单侧格点来源；DLW 不施加通向 2-HS 的伪二约化。文献来源仍需明确引用。'),
 ('2.3','A symmetric staggered formulation','由 B_b f_k·g_k=0、B_(b−h) f_k·g_(k−1)=0，令 b=a+h/2、F_j=f_(j+1)、G_j=g_j，精确得到 B_(a−h/2)F_j·G_j=0、B_(a+h/2)F_j·G_(j+1)=0。固定的是连续目标 a；b 随 h 变化。说明交错位置和对称构造的动机。'),
 ('2.4','Gram determinant solutions and regularity','以一套 Gram 记号给出任意 N 的行列式解、证明及正则适用条件；核验两条探索线解族的参数和规范对应，不能只验证方程对应就宣称解族自动等同。Casoratian 作为替代表达按需要置于附录。')]),
('3','Nonlinear formulations and integrable structure','非线性表示与可积结构',[
 ('3.1','The endpoint-based semi-discretization (ESD)','将并行稿方案命名为 ESD（endpoint-based semi-discretization，端点型半离散化）。定义其 U、V 物理场，从同点及跨点双线性式完整推导两场闭合方程，说明 V 的边位置及连续比较约定。ESD 为正式比较方法，不再仅作补充对照。'),
 ('3.2','The centered semi-discretization (CSD): potential elimination','定义对称 u、辅助 ω 及 v=4ω/h+δ₀u，在 CSD 构造下从对数势关系消元得到 PE（potential-elimination formulation，消势形式）。给出 W=4ω/h、P=δ₋u 的计算形式、下侧重构条件，以及 ESD/CSD 的参数与物理场转换；区分共同 τ 解上的精确对应与任意非线性解可逆性。'),
 ('3.3','The potential formulation of CSD','在 CSD 构造下保留势变量得到 PF，明确 Q、R、M 的方程、格点约束和场重构，核查与 PE 的关系及逆向重构自由度。PF 保留为理论辅助表示，不纳入主数值方法比较。'),
 ('3.4','Darboux–Lax representations','为最终选定的格点形式给出相容性推导，核对并行线标量算子形式与我们 Darboux 表示的变量、参数和规范关系。区分局部开链与周期零模条件；不预先宣称两种 Lax 形式已规范等价。'),
 ('3.5','The continuum limit and second-order field approximation','分别证明方程的一致性和匹配精确解族的物理场二阶逼近；说明位置、固定参数、正性及导数界。保留模型误差首项作为理论结果，长推导放附录；不恢复旧的中心 x 差分误差抵消叙事。')]),
('4','Numerical formulation and linear stability','数值实现与线性稳定性',[
 ('4.1','Fourier differentiation and spatial formulations','均匀 x 网格统一采用 Fourier 配点微分，明确乘积与去混叠约定。主对照为 ESD（端点型半离散化）、CSD（中心型半离散化，数值采用其 PE 表示）与 FD（连续 DLW 的直接 y 差分）；FD 的 x 导数也用 FFT。两种半离散格式的共同格点来源、参数配置和物理场重构差别须明确，不能当作无关系统。'),
 ('4.2','Boundary closure and time integration','分别给出 ESD、CSD、FD 的下侧闭合和 x 周期处理，并统一说明 RK4、Euler 和 C–N。时间法比较以两种半离散方法为对象；保留 C–N 的前提是隐式求解已核验。PF 非周期势的处理只在需要其辅助数值验证时讨论。'),
 ('4.3','A conservation-based moving mesh','从最终非线性形式的守恒律构造共享 x 动网格，推导计算坐标变换和 ALE 项。在均匀计算坐标上用 FFT，再借助 Jacobian 转成物理导数；不在非均匀物理节点上直接套普通 FFT。'),
 ('4.4','Linearized evolution under the numerical closure','针对最终方法及实际边界闭合重新推导线性增长分支；区分格点系统增长、空间离散影响和时间算法稳定域。并行线的 ξ² 分支用作对照，不能未经转换直接归属于我们的所有表示。')]),
('5','Numerical experiments','数值实验',[
 ('5.1','Test problems and error measures','采用一个单孤子、一个双孤子、Gaussian 和正弦两类非精确初值。后两者不是随机噪声；若另加随机扰动，明确种子和谱。区分连续解误差、半离散解误差及无精确解时的加密差异。原四组孤子结果作历史证据，不直接冒充新 FFT 实验。'),
 ('5.2','Comparison of spatial formulations','同一 Fourier x 微分及时间推进下，正式比较 ESD、CSD、FD 三种空间形式。统一连续目标参数、初边值、评价位置和误差参照；分别声明 ESD/CSD 的场重构，不能无说明地混用点与边中点数据。以误差表及加密结果为主，不展开旧中心 x 差分的误差构成与抵消分析。'),
 ('5.3','Time integration and exact-lattice benchmarks','对 ESD、CSD 分别使用各自相容的半离散精确初边值验证求解器和时间阶；控制空间误差或明确误差平台，再比较 Euler/RK4/C–N 的误差及成本。不同精确场的误差不直接当作同一连续场误差比较。'),
 ('5.4','Fixed and adaptive meshes','围绕 CSD 的 PE 表示比较固定/动网格的精度、计算成本及最小间距，使用相同节点数和误差评价口径。'),
 ('5.5','Nonexact initial data and stability diagnostics','展示 Gaussian、正弦数据的真实时间演化，通过扰动与分辨率敏感性联系4.4的增长分析。将时间步敏感性与空间可靠性分开，不把有限时间波形当作长期稳定或波破裂证明。')]),
('6','Conclusions','结论',[
 ('','', '回到格点来源、对称物理场、表示与计算之间的联系，概括已证明结果及实验支持的结论；按实际稳定性结果界定适用范围。')])]
appendices=[
 ('A','Determinant identities and alternative solution representations','任意 N 行列式恒等式、相邻层关系，以及确有需要的 Casoratian/Gram 对应。'),
 ('B','Field transformations and reconstruction conditions','ESD/CSD、CSD 的 PE/PF 转换的详细代数；积分函数、边界和周期相容条件。'),
 ('C','Operator compatibility and continuum expansions','Lax 算子系数计算、连续极限及精确物理场首项展开。'),
 ('D','Numerical implementation and supplementary experiments','FFT 周期化/去混叠、势变量处理、动坐标导数和隐式求解细节；补充参数、复现信息和必要的额外算例。')]
title='Integrable semi-discretization and numerical approximation of the (2+1)-dimensional dispersive long-wave system'
out=ROOT/'dlw-paper.html'
if out.exists():raise FileExistsError('Refusing to overwrite an existing manuscript')
parts=['''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Integrable semi-discretization and numerical approximation of the DLW system</title>
<style>body{max-width:1020px;margin:48px auto;padding:0 26px;color:#222;background:#fff;font:17px/1.8 Georgia,"Times New Roman","Microsoft YaHei",serif}h1{font-size:30px;line-height:1.35}h2{font-size:24px;margin-top:42px}h3{font-size:19px;margin-top:26px}a{color:#245c7b}nav{border-block:1px solid #ddd;padding:16px 0}nav a{display:block;text-decoration:none}.guide{border-top:2px solid #aaa;margin-top:60px}.guide p{margin:10px 0 22px}.status{font-size:15px;color:#555}@media print{body{max-width:none;margin:0;padding:0}nav{display:none}}</style></head><body><article>''',f'<h1>{html.escape(title)}</h1>',
 '<!-- Integration initialized 2026-10-22. Main text is a manuscript skeleton, not a completed proof. Editorial guidance is isolated in Appendix G. -->',
 '<section id="abstract"><h2>Abstract</h2><!-- Write after the mathematical statements and numerical evidence are settled. --></section>',
 '<nav aria-label="Contents">'+''.join(f'<a href="#section-{n}">{n}. {html.escape(en)}</a>' for n,en,zh,subs in sections)+'</nav>']
for n,en,zh,subs in sections:
    parts.append(f'<section id="section-{n}"><h2>{n}. {html.escape(en)}</h2>')
    for sn,st,guide in subs:
        if sn:parts.append(f'<section id="section-{sn}"><h3>{sn} {html.escape(st)}</h3>')
        parts.append('<!-- Editorial guide: '+guide.replace('--','—')+' -->')
        if sn:parts.append('</section>')
    parts.append('</section>')
for letter,name,guide in appendices:
    parts.append(f'<section id="appendix-{letter}"><h2>Appendix {letter}. {html.escape(name)}</h2><!-- {guide} --></section>')
parts.append('<section id="references"><h2>References</h2><!-- Consolidate verified references from both lines; internal integration does not remove attribution to underlying published work. --></section>')
parts.append('<section class="guide" id="appendix-G" lang="zh-CN"><h2>Appendix G. Editorial guide（暂存，投稿前移除）</h2><p class="status">2026-10-22：本文件为正式成果整合入口；当前仅建立章节骨架。以下是编写计划，不代表新的推导已经完成或证明已经通过核验。</p><p>叙事主线：从连续 DLW 的双线性结构进入有明确来源的格点关系，通过对称配置定义离散物理场，再导出两种闭合表示、可积结构和连续极限，最终讨论这些选择对计算的影响。正文以研究问题和推导动机衔接，不使用“两份稿子合并”的过程叙述。</p>')
for n,en,zh,subs in sections:
    parts.append(f'<h3>{n}. {zh}</h3>')
    for sn,st,guide in subs:
        parts.append(f'<p><strong>{sn+" "+html.escape(st) if sn else html.escape(en)}</strong><br>{html.escape(guide)}</p>')
parts.append('<h3>方法命名与比较范围</h3><p><strong>ESD — endpoint-based semi-discretization：</strong>端点型半离散化。<strong>CSD — centered semi-discretization：</strong>中心型半离散化。端点/中心指双线性配对的参数基准及相应物理场重构，不表示所有物理变量都放在端点或所有差分都采用中心模板。PE/PF 分别表示 CSD 的消势/势变量形式；数值表中的 CSD 默认采用 PE 表示。<strong>FD — direct finite-difference formulation：</strong>连续 DLW 的直接 y 差分基准；三者的 x 导数均采用 FFT。名称描述构造或表示，不把有限时间观测阶作为方法名称。PF 保留为理论辅助表示。</p><h3>理论工作的推进顺序</h3><ol><li>统一符号、固定参数与格点位置，核验 ESD 到 CSD 的精确转换。</li><li>推导物理场关系和 PE/PF，明确正向、逆向及边界条件。</li><li>统一行列式解与正则性条件，检查解族的参数、相位和规范匹配。</li><li>逐项核验 Lax 相容性、不同表示间的联系及连续极限。</li><li>完成二阶一致性与精确场逼近的条件化陈述，再据此定稿摘要和贡献。</li></ol><p>本轮先规划，不启动新一轮 FFT 数值实验。Gaussian/正弦属于非精确初值，不能称为随机抽样。旧中心差分误差解释从新数值主线移出；必要的二阶理论证明继续保留。</p><p>来源入口：<a href="report/dlw_paper_draft.html">既有论文稿</a>；<a href="Paper/sources/dlw_y_lattice_20261018/DLW_y_lattice_and_2HS.pdf">并行探索稿</a>；<a href="report/dlw_paper_method_comparison_20261022.html">现有共同参数比较</a>。</p></section></article></body></html>')
out.write_text('\n'.join(parts),encoding='utf8')
(HERE/'chapter_plan.json').write_text(json.dumps(dict(title=title,sections=sections,appendices=appendices,numerical_methods={"ESD":"endpoint-based semi-discretization","CSD":"centered semi-discretization (PE realization)","FD":"direct y finite-difference formulation"},nomenclature={"PE":"potential-elimination formulation of CSD","PF":"potential formulation of CSD","qualification":"Endpoint/center refers to bilinear parameter anchoring and field reconstruction, not the location of every field or every difference stencil."}),ensure_ascii=False,indent=2),encoding='utf8')
print(out)
