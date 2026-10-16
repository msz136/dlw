from pathlib import Path
import hashlib
import html
import json

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
inventory = json.loads((OUT/'inventory.json').read_text(encoding='utf-8'))
dlw = json.loads((OUT/'dlw'/'numerical_checks.json').read_text(encoding='utf-8'))
theory = json.loads((OUT/'theory'/'evidence.json').read_text(encoding='utf-8'))
wide = json.loads((OUT/'wide_field_evidence.json').read_text(encoding='utf-8'))
cache = json.loads((OUT/'plot_cache_evidence.json').read_text(encoding='utf-8'))
cn = json.loads((OUT/'dlw'/'cn_revision'/'cn_evidence.json').read_text(encoding='utf-8'))
cn_tolerance = json.loads((OUT/'dlw'/'cn_revision'/'cn_tolerance_pure_evidence.json').read_text(encoding='utf-8'))
unchanged = {}
current_reviewed = {}
versions = {}
for key, info in inventory.items():
    current = hashlib.sha256(Path(info['path']).read_bytes()).hexdigest()
    unchanged[key] = current == info['sha256']
    reviewed_hash = cn['sha256'] if key == 'dlw' else info['sha256']
    current_reviewed[key] = current == reviewed_hash
    versions[key] = {'initial_sha256':info['sha256'], 'final_reviewed_sha256':reviewed_hash,
                     'current_sha256':current}
assert all(current_reviewed.values()), 'A notebook changed since its final reviewed snapshot.'
assert all(r['completed'] for r in dlw['main_27_runs'])
assert len(dlw['main_27_runs']) == 27
assert not any(r['mismatches'] for r in dlw['saved_tables_against_recomputed'])
assert all(c['passed'] for c in theory['symbolic_checks'])
assert all(r['completed'] for r in wide)
assert len(cn['cn_default_9_runs'])==9 and all(r['completed'] for r in cn['cn_default_9_runs'])
assert cn['saved_new_time_table']['numeric_entries']==54 and not cn['saved_new_time_table']['mismatches']
assert cn['euler_rk4_step_bodies_unchanged']

findings = [
    dict(id='D1', priority='P2', category='implementation', notebook='dlw',
         locations=[{'cell':20,'lines':[25,69,71]}, {'cell':33,'lines':[11,13]}],
         title='修改参数后仍可能使用旧结果',
         cause='主结果缓存不含 CONFIG/CASES；solve 的默认 CONFIG 对象在定义时绑定；宽域缓存不含 CASES。'),
    dict(id='H1', priority='P2', category='implementation', notebook='2hs',
         locations=[{'cell':24,'lines':[3,7]}, {'cell':17,'lines':[1,2]}, {'cell':20,'lines':[19,20]}],
         title='局部重运行会把二孤子标成单孤子',
         cause='二孤子覆盖共享解析函数及网格，单孤子求解单元没有重建案例上下文。'),
    dict(id='D2', priority='P2', category='implementation', notebook='dlw',
         locations=[{'cell':14,'lines':[11,12]}, {'cell':20,'lines':[43,52]}],
         title='SD2 最后一步缺少 Q 正性验收',
         cause='stage 检查输入 Q，candidate 只验有限性、幅值和网格；最后一步无需再调用 stage。'),
    dict(id='C1', priority='P2', category='solver_accuracy', notebook='dlw',
         locations=[{'cell':20,'lines':[6,15]}],
         title='CN 固定残差容差干扰时间阶验证',
         cause='默认细化在3次与2次Picard残差评价之间切换；仅将容差缩紧1000倍，六场观测阶恢复约2。当前dt/4不是直接接受Euler。'),
    dict(id='T1', priority='P3', category='wording', notebook='theory',
         locations=[{'cell':18,'lines':[1]}], title='实对数局部定义应写严格为正'),
    dict(id='T2', priority='P3', category='proof_coverage', notebook='theory',
         locations=[{'cell':7,'lines':[22]}, {'cell':8,'lines':[5,7]}],
         title='辅助层正文范围稍宽于 Lean LayerOK'),
    dict(id='G1', priority='P3', category='figure_wording', notebook='dlw',
         locations=[{'cell':32,'lines':[3]}, {'cell':35,'lines':[11]}],
         title='颜色叙述仍是旧版，实际为 jet 等高线'),
    dict(id='G2', priority='P3', category='figure_wording', notebook='2hs',
         locations=[{'cell':18,'lines':[8]}, {'cell':34,'lines':[9,28]}],
         title='100 段最大误差的叙述未对应当前绘图'),
    dict(id='H2', priority='P3', category='edge_case', notebook='2hs',
         locations=[{'cell':4,'lines':[17,18]}, {'cell':34,'lines':[3]}],
         title='配置接受 T=0，但时间曲面绘图失败'),
    dict(id='S1', priority='P3', category='saved_output', notebook='dlw',
         locations=[{'cell':30,'lines':[8,9]}],
         title='新增 CN 后，保存的总试验数仍为27，应为36'),
]
summary = {
    'review_dates': ['2026-10-08','2026-10-09'],
    'scope': list(inventory[k]['path'] for k in inventory),
    'excluded': 'DLW刘维尔可积性report.ipynb',
    'cells_reviewed': sum(len(v['cells']) for v in inventory.values()),
    'code_cells_reviewed': sum(c['type']=='code' for v in inventory.values() for c in v['cells']),
    'notebooks_unchanged_since_start': unchanged,
    'current_matches_final_reviewed_version': current_reviewed,
    'reviewed_versions': versions,
    'external_dlw_revision': {'changed_cells':cn['source_changed_cells'],
                              'new_algorithm':'Crank–Nicolson','reviewed':True},
    'findings': findings,
    'default_dlw_runs_completed': 36,
    'baseline_dlw_runs_completed': 27,
    'additional_cn_runs_completed': 9,
    'saved_dlw_table_entries_matched': sum(r['numeric_entries'] for r in dlw['saved_tables_against_recomputed'])-36+54,
    'wide_field_runs_completed': len(wide),
    'theory_exact_checks_passed': len(theory['symbolic_checks']),
    'lean_recompiled': False,
    'plot_cache_checks': cache,
    'cn_tolerance_check': cn_tolerance,
    'limitations': ['No long-time or all-parameter scan.',
                    'Finite-N independent checks supplement the existing general-N Lean proof audit.',
                    'No full Lean recompilation in this review.'],
}
(OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
wide_rows = '\n'.join('<tr><td>'+r['case']+'</td><td>'+f"{r['fields']['u']['max_error']:.6g}"+
                     '</td><td>'+f"{r['fields']['v']['max_error']:.6g}"+'</td></tr>' for r in wide)
template = '''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Notebook 审查：2HS 与 DLW</title>
<style>
:root{color-scheme:light;--ink:#202326;--muted:#58616a;--line:#d7dde2;--accent:#244a67}
*{box-sizing:border-box}body{margin:0;background:#fff;color:var(--ink);font-family:"Noto Serif CJK SC","Source Han Serif SC","Microsoft YaHei",serif;line-height:1.8}
main{max-width:1040px;margin:42px auto 72px;padding:0 30px}h1{font-size:30px;line-height:1.4;font-weight:600;margin:0 0 8px}h2{font-size:22px;font-weight:600;margin:36px 0 14px;border-bottom:1px solid var(--line);padding-bottom:7px}h3{font-size:18px;margin:22px 0 8px;font-weight:600}p{margin:9px 0}a{color:var(--accent);text-decoration-thickness:1px;text-underline-offset:3px}code{font-family:Consolas,monospace;font-size:.92em;background:#f4f6f8;padding:1px 4px;border-radius:3px}.meta,.location,figcaption{color:var(--muted);font-size:14px}.lead{font-size:17px;margin-top:22px}.priority{font-size:13px;color:var(--accent);border:1px solid #bacbd8;padding:1px 5px;margin-right:8px;white-space:nowrap}.table-wrap{overflow-x:auto}table{border-collapse:collapse;width:100%;margin:16px 0;font-size:15px}th,td{text-align:left;vertical-align:top;padding:9px 12px;border-bottom:1px solid var(--line)}th{border-top:2px solid #697680;border-bottom:1px solid #697680;font-weight:600}tr:last-child td{border-bottom:2px solid #697680}.number{font-variant-numeric:tabular-nums}.note{border-left:3px solid #b3c7d6;padding:3px 16px;margin:18px 0}figure{margin:20px 0}figure img{display:block;width:100%;height:auto;border:1px solid #e5e8eb}figcaption{margin-top:8px}details{margin:18px 0}summary{cursor:pointer;color:var(--accent)}.source-links{font-size:14px}.nowrap{white-space:nowrap}
@media(max-width:650px){main{margin:22px auto 40px;padding:0 17px}h1{font-size:25px}h2{font-size:20px}table{font-size:13px;min-width:530px}th,td{padding:7px 8px}}
@media print{main{max-width:none;margin:0;padding:0}body{font-size:10.5pt}h1{font-size:21pt}h2{font-size:15pt;break-after:avoid}h3{break-after:avoid}table,figure{break-inside:avoid}a{color:inherit}.table-wrap{overflow:visible}details{display:none}@page{size:A4;margin:18mm}}
</style></head><body><main>
<h1>Notebook 审查：2HS 与 DLW</h1>
<p class="meta">2026 年 10 月 8—9 日 · 理论、算法实现与图表</p>
<p class="source-links">对象：<a href="../notebook/2HS数值分析report.ipynb">2HS 数值分析</a>、<a href="../notebook/DLW数值分析report.ipynb">DLW 数值分析</a>、<a href="../notebook/DLW理论.ipynb">DLW 理论</a>。刘维尔可积性不在本次范围内。</p>
<p class="lead">默认顺序执行的主要数值结果得到复现；理论主结论未发现实质错误。确证四项 P2 问题，涉及参数修改后的缓存、局部重运行的案例状态、SD2 最后一步的正性验收，以及 C–N 的迭代精度。当前保存的默认误差表得到复现，尚未发现方法排序因此翻转。</p>

<h2>1　需要修正的实现</h2>
<h3><span class="priority">P2 · D1</span>DLW 修改参数后可能继续使用旧结果</h3>
<p class="location">数值本：单元 20，第 25、69—71 行；单元 33，第 11—13 行。单元与行号均从 1 开始。</p>
<p>主试验以算例、空间方案、时间算法和网格策略作为缓存键，遗漏 <code>CONFIG</code> 和孤子参数。复现中将终点从 0.01 改为 0.02 后重跑比较，未再次求解，仍返回终点为 0.01 的结果。宽域场图的缓存包含计算配置，但遗漏 <code>CASES</code>；改变同名算例的谱参数也会沿用旧图数据。</p>
<p><code>solve(..., config=CONFIG)</code> 还在定义时绑定配置对象；重跑配置单元创建新字典后，旧函数仍可能使用原字典。应显式传递当前配置，并使两个缓存键覆盖实际配置与孤子参数；改变算法实现后重建缓存。</p>

<h3><span class="priority">P2 · H1</span>2HS 局部重运行可能误标案例</h3>
<p class="location">单元 24，第 3—7 行；单元 17，第 1—2 行；单元 20，第 19—20 行。</p>
<p>二孤子段永久替换解析函数、初值和网格。完整运行后仅重跑单孤子求解单元，实际求解二孤子，却保存为 <code>hs_histories['one']</code>；继续计算误差还会覆盖单孤子摘要。小规模复现中，该“单孤子”参照与二孤子完全相同，与真实单孤子的最大场差为 0.03823。</p>
<p>应将每个案例的解析函数、网格、初值和边界封装为独立上下文，由求解单元显式选取案例。正常从头顺序执行的现有单／二孤子结果对应正确。</p>

<h3><span class="priority">P2 · D2</span>SD2 未验收最后一步的 Q 正性</h3>
<p class="location">DLW 数值本：单元 14，第 11—12 行；单元 20，第 43—52 行。</p>
<p>计算右端时检查输入 Q&gt;0，但接受候选状态时只检查有限性、幅值和网格。若最后一步首次产生非正 Q，程序仍可报告完成，并以 2D₁Q/Q 恢复物理场。</p>
<p>非默认复现取 A、Euler、固定网格、Δt=T=2：最终 min Q=−0.53696，原状态幅值仅 7.217，仍返回 <code>completed=True</code>。该步长远大于原实验；这一反例说明验收遗漏，不否定当前短时表格。应在候选时刻检查 Q 正性、动网格监测密度及恢复场的有限性，再接受该步。</p>
<p>新增 C–N 在评估隐式残差时会调用候选终点的右端，因此会触发其 Q 正性检查；不能将上述 Euler 反例直接推广到 C–N。</p>

<h3><span class="priority">P2 · C1</span>C–N 固定残差容差干扰时间阶验证</h3>
<p class="location">DLW 数值本：单元 20，第 6—15 行；审查期间新增的算法已补审。</p>
<p>端点平均的梯形公式正确，默认九组 C–N 主试验全部完成，720 个时间步的隐式残差均在设定容差内。但停止容差 10⁻¹²+10⁻¹¹max(1,‖z‖∞) 不随 Δt 缩放。</p>
<p>算例 C 按原步长及两次减半做自收敛：SD/FD 的观测阶约 1.01—1.04，SD2 约 3.22—3.65。这里细步至少完成一次 Picard 校正，并非直接接受 Euler；残差评价次数在 3 与 2 之间切换，使不同步长混合了充分求解的梯形法与一次校正的 Heun 近似，污染阶数估计。仅将容差缩紧 1000 倍、不改变其他设置，六个场的观测阶恢复到 1.9986—2.0001。</p>
<p>另在更小步长的标量方程 z′=z 中，预测子残差已低于固定容差，确会直接接受 Euler。应使隐式求解误差随时间步控制到局部 O(Δt³) 的量级，并做容差敏感性核验。默认误差表的空间误差远大于该迭代误差；本发现不否定其已复现数值，也不说明 C–N 公式是一阶。</p>

<h2>2　数值精度与适用范围</h2>
<h3>2HS：局部误差不能代表完整波形</h3>
<p>Integrable 的右尾偏差已在原图保留，独立计算也复现。默认 N=2400、a=0.005、T=0.5，各区间分别取 32001 个等距评价点：</p>
<div class="table-wrap"><table class="number"><thead><tr><th>案例</th><th>Eᵤ，[-1,1]</th><th>Eᵤ，[-5,5]</th><th>Eρ，[-1,1]</th><th>Eρ，[-5,5]</th></tr></thead><tbody>
<tr><td>单孤子</td><td>0.0100128</td><td>0.0935635</td><td>0.00114968</td><td>0.00438729</td></tr>
<tr><td>二孤子</td><td>0.0345089</td><td>0.279438</td><td>0.00399324</td><td>0.0121404</td></tr></tbody></table></div>
<p>N 从 300 逐次加倍至 4800，宽域 Eᵤ 约以一阶衰减：单孤子由 0.77080 降至 0.046686，二孤子由 2.41588 降至 0.13899。默认步长两次减半，重构 u 的变化不足 9×10⁻¹⁰，尾误差由空间截断主导。</p>
<p>RHS 与正文式（3）逐项一致，常背景也是精确平衡。对连续孤子采样初值，单胞 b 方程残差的主导项为 a²(J²−1)/J，累计恢复 u 后成为 O(a)。因此应补充宽域误差与空间细化；若要检验半离散系统自身的精确性，应另用其精确半离散孤子作为基准。FD 默认 Eᵤ 约为 9×10⁻⁷、Eρ 约为 3×10⁻⁶，局部与宽域均保持这一量级。</p>
<details><summary>查看原 Notebook 保存的尾部对照图</summary><figure><img src="../Workspaces/notebook_audit_20261008/extracted/2hs/cell_34_output_03.png" alt="2HS 单孤子 Integrable 在 t=0.5 的数值、解析及绝对误差对照"><figcaption>原单元 34 的保存输出：单孤子右尾的数值 u 明显偏离解析场；误差图未将该偏差隐藏。</figcaption></figure></details>

<h3>DLW：短时与时间自收敛不保证细化稳定性</h3>
<p>SD 零背景上取 x 棋盘格 Pᵢ=(−1)ⁱ、W=0，实际右端给出正增长率 λ=4/Δx²。固定 L=40、T=0.01，nₓ=256、512、1024 时，半离散放大因子约为 5.15、702、2.43×10¹¹。减小时间步只会更准确地积分这一增长分支。</p>
<p>这与正文方程一致，不能判作扩散符号写反。现有光滑孤子的短时比较有效；Euler 一阶自收敛也得到复核，但不能据此声称空间细化时一致稳定或长时间可靠。应将空间截断阶、时间阶和稳定性分开陈述。</p>

<h2>3　理论与边界假设</h2>
<p>任意有限 N 的 Gram 双线性精确性、正则性和紧集二阶连续极限，都由现有 Lean 终点覆盖。审查核对了实际参数条件及前提消除链，未发现把待证结论作为结构输入的情形。N7/N8、QRM 的起点与物理重构相符，残差消元和 Taylor 系数通过独立精确核验。</p>
<p>一般 N 的子集系数公式 T7 由正文 Cauchy 行列式推导；Notebook 直接展示的显式系数 Lean 终点为 N=2。任意 N 解的精确性、正性及连续极限并不依赖把该 N=2 终点当成一般 N 证明。</p>
<p>第一方程含 δ₋uₜ，须用边界或均值固定 y 常数模态。数值本以每个时刻的下侧解析值固定该模态，上侧采用解析背景加扰动外推。x 方向的 SD/FD 使用周期延拓，SD2 使用 Q/R 加性跳量；此闭合依赖孤子尾部进入常数及互逆背景。在 T=0.01 时，主表计算域的解析 u/v 在 x 两端的幅值不超过 1.264×10⁻⁸，宽域计算域不超过 3.766×10⁻¹¹；这是解析尾部检查，未给出数值场或全时段的边界误差上界。变更域或参数后需重新检查尾部。</p>
<p><code>Exact</code> 的稳定求值还要求所有谱分母非零、γ 与各 τ 项系数为正。A/B/C 均满足；若允许修改谱参数，应在入口显式检查这些条件。仅有 f/g 总和值为正，尚不足以适用当前逐项取对数的实现。</p>

<h2>4　图表与低优先修订</h2>
<p>18 张保存图均已检查。数值、解析和绝对误差的数据流对应正确；同一物理场的数值／解析面板共享色标和等高线高度，误差由同点作差产生。DLW 宽域 A/B/C 也全部独立回算，在当前绘图窗口内的最大误差如下；这些图使用独立宽域数据，不能与前面的原域误差表直接等同。</p>
<div class="table-wrap"><table class="number"><thead><tr><th>算例</th><th>图窗口内 Eᵤ</th><th>图窗口内 Eᵥ</th></tr></thead><tbody>__WIDE_ROWS__</tbody></table></div>
<div class="table-wrap"><table><thead><tr><th>P3 项</th><th>位置</th><th>修订建议</th></tr></thead><tbody>
<tr><td>实对数定义域</td><td>理论单元 18，行 1</td><td>将“非零区域”改为“严格为正的区域”，与后文及实际 Lean 条件一致。</td></tr>
<tr><td>辅助层形式化范围</td><td>理论单元 7—9</td><td>说明 C07 的 LayerOK 对所有整数层要求 pᵢ−s≠0；正文 n≥0 的退化层范围稍宽。主 F/G 条件已满足，不影响主结论。</td></tr>
<tr><td>颜色叙述陈旧</td><td>DLW 单元 32、35</td><td>当前为 jet 等高线，零误差映为深蓝；白底来自未填充区域。将“零白、负蓝、正红”改为当前实际色标说明。</td></tr>
<tr><td>误差图分箱叙述陈旧</td><td>2HS 单元 18，行 8；单元 34</td><td>当前按 xpoints=601 直接重构作图，并未取 100 段内最大值；删改该句及已失效的 plot_xlim 名称。</td></tr>
<tr><td>零时长配置</td><td>2HS 单元 4、34</td><td>T=0 被接受，但时间窗口 (0,0) 必报错；支持初值切片，或入口明确 T&gt;0。</td></tr>
<tr><td>保存试验数未同步</td><td>DLW 单元 30 的输出</td><td>新增九组 C–N 后，完整运行有 36 组主试验；保存输出仍写 27。源码动态使用 len(results)，应更新保存输出而非改统计公式。</td></tr>
</tbody></table></div>
<p class="meta">DLW 的 y 数据位于胞元中心：宽域实际样点为 [−29.9375,29.9375]；图轴标至 ±30，端部半格没有额外节点样本。2HS 图中的第二坐标是时间 t，DLW 则是空间 y，当前标签正确。</p>

<h2>5　核验覆盖</h2>
<div class="table-wrap"><table><thead><tr><th>Notebook</th><th>完整阅读</th><th>独立核验</th></tr></thead><tbody>
<tr><td>2HS 数值</td><td>34 单元／19 代码单元</td><td>两案例、两方案的默认误差表；解析 PDE 与链式导数；Poisson 解、RK4；Integrable 的空间／时间细化和重运行误标。</td></tr>
<tr><td>DLW 数值</td><td>37 单元／20 代码单元</td><td>原 27 组与新增 9 组 C–N 主试验；新版保存表 126 值均匹配；3 组宽域场；SD/FD 右端、SD2 提升与边界导数、ALE；Euler/C–N 时间细化与容差配对；缓存及终步反例。</td></tr>
<tr><td>DLW 理论</td><td>31 单元／14 代码单元</td><td>__SYMBOLIC_COUNT__ 项精确检查；13 个 Lean 单元的起点、终点与已有成功编译输入对应；38 个本地证明模块及其直接相关证明链。</td></tr>
</tbody></table></div>
<p>本次审查未修改 Notebook。审查期间 DLW 被并行任务新增 C–N；本报告已补审该版本，单元定位采用新版。2HS 与理论本的哈希保持，DLW 的初始及补审版本哈希均载于汇总证据。本轮没有重编译 Lean 库，也没有作长时间或全参数扫描；有限 N 的独立样例用于交叉检查，一般 N 结论仍依据审读的完整证明。</p>
<p class="source-links">详细记录：<a href="../Workspaces/notebook_audit_20261008/2hs/findings.md">2HS</a> · <a href="../Workspaces/notebook_audit_20261008/dlw/findings.md">DLW 数值</a> · <a href="../Workspaces/notebook_audit_20261008/theory/findings.md">DLW 理论</a> · <a href="../Workspaces/notebook_audit_20261008/summary.json">汇总证据</a></p>
</main></body></html>'''
report = ROOT/'report'/'notebook_review_20261009.html'
report.parent.mkdir(exist_ok=True)
report.write_text(template.replace('__WIDE_ROWS__',wide_rows).replace('__SYMBOLIC_COUNT__',str(len(theory['symbolic_checks']))),encoding='utf-8')
print(json.dumps({'report':str(report),'cells':summary['cells_reviewed'],
                  'code_cells':summary['code_cells_reviewed'],'findings':len(findings),
                  'current_matches_reviewed_version':current_reviewed},ensure_ascii=False))
