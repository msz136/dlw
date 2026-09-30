"""Build the readable cream atlas from generated scientific figures and records."""
import json
import base64
import re
from pathlib import Path
from PIL import Image
HERE=Path(__file__).resolve().parent
data=json.loads((HERE/'out/summary.json').read_text(encoding='utf-8'))
figs=data['figures']
def figure(f):
    path=HERE/'figures'/(f['name']+'.png')
    w,h=Image.open(path).size
    image=base64.b64encode(path.read_bytes()).decode()
    return f'<figure id="{f["name"]}"><h3>{f["title"]}</h3><a href="figures/{f["name"]}.png" title="查看原尺寸图"><img src="data:image/png;base64,{image}" width="{w}" height="{h}" alt="{f["title"]}"></a><figcaption>{f["caption"]} <a href="figures/{f["name"]}.pdf">下载 PDF</a> · <a href="figures/{f["name"]}.png">原尺寸 PNG</a></figcaption></figure>'
def group(prefix,time):return ''.join(figure(f) for f in figs if f['name'].startswith(prefix) and f['name'].endswith(time))
theme=(HERE.parent/'gsg_project/dlw_report/_src/miura_dlw.src.html').read_text(encoding='utf-8')
theme=re.findall(r'<style>([\s\S]*?)</style>',theme)[1]
extra='''.page{max-width:1160px;padding-inline:50px}figure{margin:32px 0 44px}figure img{width:100%;height:auto;display:block;border:1px solid var(--rule)}figcaption{font-size:.86rem;color:var(--muted);margin-top:10px}table{font-variant-numeric:tabular-nums}.table-wrap:focus-visible{outline:2px solid var(--accent)}.figure-guide{font-size:.92rem}.download{font-size:.87rem}@media(max-width:700px){.page{padding-inline:22px}figure{margin-inline:-12px}figure h3,figure figcaption{padding-inline:12px}th,td{min-width:100px}}'''
body=r'''
<header id="top"><div class="eyebrow">2HS 数值图集 · 对照 GSG §4 的作图思路</div><h1>固定时刻，看波形、误差与参数</h1><p class="subtitle">Euler · 39 个孤子参数 · 两组明确的方案对照</p><p class="date">2026 年 9 月 27 日 · 主图 t = 0.5，补充 t = 0.25</p></header>
<p class="lede">本图集把之前的误差大表展开成曲线：先固定一个波形参数看解析解与数值解是否重合，再看误差集中在哪些位置，最后扫描参数，看优势在哪些波形中出现。</p>
<div class="key"><p><strong>横轴需要分清：</strong>GSG 原文中的 $y$ 是辅助空间坐标，$p_1$ 才是孤子参数。我们用 $x$ 表示物理位置，用 $y=X$ 表示连续质量坐标，用 $p$ 表示改变波形的参数。本页同时提供沿 $x$、沿 $y$ 的误差图，以及沿 $p$ 的参数扫描。</p><p>如果把某个系统参数叫作 $y$，它当然也能作横轴，但画出的将是“不同问题之间的参数响应曲线”。这里保留 $p$ 的名称，以便与单个解的空间波形区分。</p></div>
<nav class="toc" aria-label="图集目录"><p>建议先看前三项</p><ol><li><a href="#wave">一 · 波形叠加</a><small>固定 p、固定 t，沿空间取样</small></li><li><a href="#error">二 · 空间误差分布</a><small>差异小到肉眼看不清时，看这里</small></li><li><a href="#scan">三 · 参数扫描</a><small>固定 t，沿 p 判断有利与不利场景</small></li><li><a href="#extra">四 · y 坐标与二维误差图</a><small>辅助坐标版本及 x–p 分布</small></li><li><a href="#checks">五 · 实验与核查</a><small>步长减半、加密与原始数据</small></li></ol></nav>
<section class="part" id="setup"><h2>本轮具体做了哪些实验</h2>
<p>主配置为显式 Euler、$N=400$、$\Delta t=0.003125$、连续物理参数 $c=1$；从同一光滑单孤子族中取 $p=3,3.5,\ldots,22$，共 39 点。每条轨道输出 $t=0.25,0.5$。主图代表参数为 $p=5,14,22$，用于同时展示双场收益、局部收益与较大参数下的取舍。</p>
<div class="table-wrap" tabindex="0"><table><thead><tr><th>对照</th><th>方案一</th><th>方案二</th><th>回答的问题</th></tr></thead><tbody>
<tr><td>网格选择</td><td>普通差分＋持续 Rₘ 动网格</td><td>普通差分＋固定网格</td><td>相同 ALE 场求解框架下，完整网格方案是否改善精度</td></tr>
<tr><td>空间格式</td><td>校准可积半离散</td><td>同变量普通差分</td><td>相同初态、变量及开链边界下，校准式能否降低总误差</td></tr>
<tr><td>背景参照</td><td>未校准原可积半离散</td><td>放在误差图中作为参照</td><td>校准前后差异有多大</td></tr>
</tbody></table></div>
<p>这里有五条真实可执行的方案，不是任意“可积／普通 × Rₘ／固定”的四组合。原可积与校准式的格距方程属于其模型本身；它们保留原生运动规则。普通密度动网格不再作为候选方案加入，Rₘ 与固定网格也没有拆成“仅初始布点”和“持续移动”两组。</p>
<p>连续密度场仍记为 $\rho$；它是要评估的求解量。所有动网格都在时间推进中持续更新。只比较同节点预算的精度，未把运行时间或 CPU 成本作为等价约束。</p></section>
<section class="part" id="wave"><h2>一 · 固定 p、t，画出波形</h2>
<p class="figure-guide">每列是一个参数，每行是一种物理场。主图只放一组对照，避免五条重合曲线看不清。黑色解析曲线与彩色数值曲线接近重合，说明整体波形正确；它本身不足以判断哪一种数值方法更精确。</p>
@@WAVE@@
</section>
<section class="part" id="error"><h2>二 · 看误差到底出在哪里</h2>
<div class="mathblock">$$e_u(x;p,t)=|u_h(x;p,t)-u_{\rm exact}(x;p,t)|,\qquad
e_\rho(x;p,t)=|\rho_h(x;p,t)-\rho_{\rm exact}(x;p,t)|.$$</div>
<p>不同方案在同一个物理位置 $x$ 上比较。动网格上的数值解先分段线性重构到公共位置，再减连续解析解；没有相位拟合，没有用各自离散精确解替代连续参照，也没有扣掉重构误差。</p>
@@ERROR@@
<p>曲线上的细小锯齿来自节点间的线性重构误差及与演化误差的叠加，不能仅凭锯齿就认定解出现不稳定振荡。图中也能看到：局部误差较小，不一定意味着整个区间的最大误差较小；开链累加恢复 $u$ 的误差可以延伸到波峰之外。</p>
</section>
<section class="part" id="scan"><h2>三 · 固定 t，扫描孤子参数 p</h2>
<p>这一组回答你说的“移动另一个系统参数去采样”。每一个 $p$ 都对应一次独立数值演化，再把整个共同区间 $[-2,2]$ 内的最大误差记下来。它不是对一个解沿空间取值。</p>
<div class="mathblock">$$E_u(p;t)=\max_{x\in[-2,2]}e_u(x;p,t),\qquad
E_\rho(p;t)=\max_{x\in[-2,2]}e_\rho(x;p,t).$$</div>
@@SCAN@@
<div class="key"><p><strong>主 Euler 配置下的新扫描结果：</strong>在 $t=0.5$，Rₘ 相对固定网格的 $u$ 优势出现在已测的 $p=3,3.5,\ldots,8$；$\rho$ 则在全部 39 个点更好。校准可积相对同变量普通差分的全域 $u$ 优势出现在已测的 $p=15.5,16,\ldots,22$；$\rho$ 没有对应优势。</p><p>到 $t=0.25$，两组全域 $u$ 的有利采样点分别为 $p=4,4.5,\ldots,10$ 和 $p=10.5,11,\ldots,22$。这些是固定分辨率的采样结果，不是已证明的连续参数门槛；图中的步长减半曲线显示临界位置会变化。</p></div>
</section>
<section class="part" id="extra"><h2>四 · 补齐 y 坐标与 x–p 分布图</h2>
<details><summary>沿 y=X 的误差图：对应辅助空间坐标的读法</summary>
<p>在 2HS 中取 $y=X$ 为连续质量坐标，用解析映射 $x_{\rm exact}(y,t)$ 找到同一个物理位置。画的是</p>
<div class="mathblock">$$\widetilde e_u(y;p,t)=|u_h(x_{\rm exact}(y,t);p,t)-u_{\rm exact}(x_{\rm exact}(y,t);p,t)|.$$</div>
<p>密度同理。这样不会因为网格编号相同但实际位置不同，误把不同位置的场值相减。本图是公共物理场误差的重参数化；若要单独研究原生网格坐标误差 $|x_k-x_{\rm exact}(X_k,t)|$，那是另一个指标，不与场误差混用。</p>
@@Y@@
</details>
<details><summary>空间 x × 参数 p 的误差分布：哪种波形、哪个位置更难</summary>
<p>每条横行对应一个参数实验，横向是物理位置。同一物理场使用共同色标；可以直接比较误差集中在峰、两侧还是尾部。</p>@@MAP@@</details>
<details><summary>展开 t=0.25 的整套对照图</summary>@@EARLY@@</details>
</section>
<section class="part" id="checks"><h2>五 · 核查与当前结论的范围</h2>
<p>共完成 <strong>405 条记录</strong>：39 参数 × 五方案 × 两档 Euler 步长为 390 条；另对 $p=5,14,22$ 的五方案使用 $N=800$、$\Delta t=0.0015625$ 加密，增加 15 条。130 条完全匹配的旧轨道直接复用，本次新演化 275 条；所有旧求解器源码哈希保持不变。</p>
<p>最大误差在 16001 个公共物理点评价，并用 32001 点复核；两组对照的优势方向没有因评价点加密改变，所有记录误差的最大相对变化为 @@EVAL@@。图中的连续线在 4001 点取样，数值标记来自原生配点；PDF 与 PNG 都可下载，图线采样数据另存 NPZ。</p>
<p><strong>不能忽略的敏感性：</strong>Euler 步长减半使 18 个单场／区域比较翻转，全部是 $u$。三代表参数的空间加密又有一项翻转：$p=14,t=0.25$ 的峰区 Rₘ／固定 $u$ 比，在相同半步长下由 0.926 变为 1.302。固定时间步的空间加密会改变空间误差与时间误差的相对大小，所以不能把这些临界收益称为与分辨率无关。</p>
<p>所有轨道的网格和密度保持正值。独立读回保存的数值场，在公共物理点重新计算最大误差，与记录差异为 @@READBACK@@；解析反演最大残差为 @@INVERSION@@。本批没有增加长时间、多孤子或随机总体试验，没有作新的统计显著性声明。</p>
<p class="download"><a href="out/errors.csv">全部误差 CSV</a> · <a href="out/summary.json">比值及敏感性</a> · <a href="out/plan.json">冻结实验清单</a> · <a href="out/results.json">原始轨道索引</a> · <a href="out/waveform_samples_t0.5.npz">t=0.5 图线数据</a> · <a href="out/y_samples_t0.5.npz">y 坐标图线数据</a></p>
<p class="aside">导出的代表图已直接查看。公式编译、图片嵌入、文件链接与锚点通过<a href="out/static_validation.json">静态检查</a>；内置浏览器安全策略拒绝打开 file://，本次没有确认 HTML 的浏览器渲染效果。</p>
<p class="source">来源：<a href="../../numerical_analysis.html">主目录数值报告 §1.3</a>、<a href="../../Paper/sources/gsg.txt">GSG 原文 §4</a>、<a href="../hs_error_theory_20260926/DYNAMIC_MESH_REPORT.html">此前六方案大表</a>、<a href="../hs_error_theory_20260926/index.html">校准误差系数推导</a>。</p>
<details><summary>复现顺序</summary><p>依次运行 <a href="run_experiments.py">run_experiments.py</a>、<a href="make_atlas.py">make_atlas.py</a> 与 <a href="build_html.ps1">build_html.ps1</a>。既有结果会按冻结清单读回；新图集正文来自 <a href="build_report.py">build_report.py</a>，生成到 <a href="_src/index.src.html">HTML 源</a> 后嵌入字体与公式渲染资源。</p></details>
</section><footer>图集固定使用 Euler；曲线、误差、参数维度分别标注。<a href="#top">回到顶部</a></footer>
'''
replacements={'WAVE':group('01','t0p5'),'ERROR':group('02','t0p5'),'SCAN':group('04','t0p5'),
              'Y':group('03','t0p5'),'MAP':group('05','t0p5'),'EARLY':''.join(figure(f) for f in figs if f['name'].endswith('t0p25')),
              'EVAL':f"{100*data['max_evaluation_relative_change']:.3f}%",
              'READBACK':f"{data['pointwise_metric_readback_max']:.2e}",'INVERSION':f"{data['reference_inversion_max']:.2e}"}
for k,v in replacements.items():body=body.replace('@@'+k+'@@',v)
html='''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light"><meta name="description" content="2HS Euler 波形和空间误差图集，包含39参数扫描、R_m与固定网格及校准可积与普通差分的比较。"><title>2HS Euler 波形与误差图集</title><style>@@KATEX_CSS@@</style><style>'''+theme+extra+'''</style></head><body><a class="skip" href="#main">跳到正文</a><main class="page" id="main">'''+body+'''</main><script>@@KATEX_JS@@</script><script>document.addEventListener('DOMContentLoaded',function(){renderMathInElement(document.querySelector('main'),{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],ignoredTags:['script','noscript','style','textarea','pre','code','option'],throwOnError:false});});</script></body></html>'''
(HERE/'_src').mkdir(exist_ok=True)
(HERE/'_src/index.src.html').write_text(html,encoding='utf-8')
md=['# 2HS Euler 波形与误差图集','',
    '主图 t=0.5，补充 t=0.25；N400，dt=.003125。39个p=3,.3.5,…,22（步长0.5）。',
    '坐标：x=物理位置，y=X=辅助质量坐标，p=孤子参数。',
    '两组比较：普通Rm网格/固定网格；校准可积/同变量普通差分。原可积作背景误差参照。',
    '',
    '405条记录全部完成（275新增、130复用）；含全部参数Euler减步和3代表参数网格加密。',
    '评价点加密无方向翻转；Euler减步18个u比较翻转，加密又有1个峰区u比较翻转，见summary.json。',
    '','[完整离线HTML](index.html)','']
for f in figs:
    md += [f'## {f["title"]}','',f'![{f["title"]}](figures/{f["name"]}.png)','',f['caption'],'']
(HERE/'REPORT.md').write_text('\n'.join(md).replace('3,.3.5','3,3.5'),encoding='utf-8')
print(HERE/'_src/index.src.html')
