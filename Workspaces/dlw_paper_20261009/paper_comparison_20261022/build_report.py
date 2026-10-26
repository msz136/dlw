from pathlib import Path
import json,hashlib,re
import numpy as np
from scipy.interpolate import CubicSpline
H=Path(__file__).resolve().parent; R=H.parents[2]
records={(c,m):json.loads((H/f'{c}_{m}.json').read_text()) for c in 'ABCD' for m in ('FD','PE','paper_endpoint','paper_midpoint')}
expected={'A':{'FD':[4.715088e-4,1.201923e-3],'PE':[6.406395e-4,1.339511e-3]},'B':{'FD':[1.718043e-5,2.605300e-5],'PE':[1.419616e-5,2.745967e-5]},'C':{'FD':[3.989986e-5,5.173628e-5],'PE':[3.552455e-5,5.359645e-5]},'D':{'FD':[4.782980e-4,1.350627e-3],'PE':[6.329588e-4,1.511271e-3]}}
val={'baseline_reproduction':{},'time_halving':{},'snapshot_sha256':hashlib.sha256((H/'solver_snapshot.py').read_bytes()).hexdigest()}
for c in 'ABCD':
 for m in ('FD','PE'):
  e=float(np.max(abs(np.array(records[c,m]['errors'])/expected[c][m]-1)));assert e<2e-6
  val['baseline_reproduction'][f'{c}_{m}']=e
 for m in ('paper_endpoint','paper_midpoint'):
  fine=json.loads((H/f'{c}_{m}_halfdt.json').read_text())
  a=np.load(H/f'{c}_{m}.npz');b=np.load(H/f'{c}_{m}_halfdt.npz');half=records[c,m]['config']['eval_half'];mask=abs(a['y'])<half
  dif=[]
  for field in ('u','v'):
   spl=CubicSpline(a['x'],(a[field]-b[field])[mask],axis=-1,extrapolate=False)
   dif.append(max(float(abs(spl(x)).max()) for x in np.array_split(a['eval_x'],30)))
  val['time_halving'][f'{c}_{m}']={'field_differences':dif,'fine_errors':fine['errors']}
assert max(v['initial_max_error'] for v in records.values())<1e-10
(H/'summary_validation.json').write_text(json.dumps(val,indent=2))
def pair(a):return ' / '.join(f'{x:.6e}' for x in a)
def table(head,rows):return '<div class="scroll"><table><tr>'+''.join('<th>'+s+'</th>' for s in head)+'</tr>'+''.join('<tr>'+''.join('<td>'+str(v)+'</td>' for v in row)+'</tr>' for row in rows)+'</table></div>'
labels={'A':'A: (1,2)','B':'B: (4,-3)','C':'C: (6,-5;4,-3)','D':'D: (1,2;4,-3)'}
main=[];mid=[];times=[];gaps=[];checks=json.loads((H/'independent_checks.json').read_text())
for c in 'ABCD':
 fd=np.array(records[c,'FD']['errors']);ep=np.array(records[c,'paper_endpoint']['errors']);mp=np.array(records[c,'paper_midpoint']['errors'])
 assert np.all(ep>fd) and np.all(mp>fd)
 main.append([labels[c],pair(fd),pair(records[c,'PE']['errors']),pair(ep),' / '.join(f'{x:.2f}' for x in ep/fd)])
 mid.append([labels[c],pair(mp),' / '.join(f'{x:.2f}' for x in mp/fd)])
 times.append([labels[c],pair(val['time_halving'][f'{c}_paper_endpoint']['field_differences']),pair(val['time_halving'][f'{c}_paper_midpoint']['field_differences'])])
 gaps.append([labels[c],pair(records[c,'paper_endpoint']['paper_exact_gap']),pair(records[c,'paper_endpoint']['distance_to_paper_exact']),' / '.join(f'{x:.3f}' for x in checks[c]['model_gap_refinement']['orders'][-1])])
maxres=max(max(v['analytic_nonlinear_residuals']) for v in checks.values());maxdt=max(max(v['field_differences']) for v in val['time_halving'].values())
html='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>附件 DLW 半离散与 FD 比较</title><style>body{max-width:1180px;margin:40px auto;padding:0 24px;font:17px/1.8 Georgia,"Microsoft YaHei",serif;color:#222}h1{font-size:28px}h2{font-size:21px;margin-top:32px}table{border-collapse:collapse;width:100%;font-size:14px;font-variant-numeric:tabular-nums}td,th{padding:10px;border-bottom:1px solid #ddd;text-align:left;white-space:nowrap}th{background:#f2f4f5}.scroll{overflow:auto}a{color:#17638d}pre{background:#f5f6f7;padding:16px;overflow:auto;font-size:14px}</style></head><body><h1>附件 DLW 半离散方法与 FD 的统一参数比较</h1><p>2026-10-22 · 四组连续孤子初值，固定网格，终点误差。</p><p><strong>本轮四组参数、网格和边界设置下，附件半离散方法两场的终点误差均大于 FD；按自然边中点解释 v 后，仍未改变这一排序。</strong>这是指定短时间实验的数值观察，不是对所有初值或网格的普遍结论。</p><h2>1. 共同设置</h2><p>a=2，λ=−2，Δx=h=0.1，RK4，Δt=10⁻⁴，T=0.01。A/B/C/D 的计算半宽依次为 10/20/40/40，评价半宽为 5/10/30/30。ρᵢ=1，初始相位为零。全部方法从连续精确场初始化，以连续精确场提供下侧边界；x 方向统一使用周期中心二阶差分。沿 x 用三次样条评价到间距 0.01，y 保留原生层。</p><p>比较附件式 (4)–(5) 与既有 FD，同时重算我们的 PE。没有沿用附件的 Fourier 配点设置，也没有将 a 改为 a+h/2。误差为终点相对连续精确解的最大绝对误差。</p><h2>2. 共点主比较</h2><p>成对数字依次为 Eᵤ / Eᵥ。附件采用定理6.1的同点解释：U、V 在同一 y 位置取连续初值和参考值，与 FD/PE 使用相同评价点。格点原点作共同平移，与 y=kh 的写法等价。</p>'''
html+=table(['算例','FD: u / v','我们的 PE: u / v','附件半离散: u / v','附件 / FD'],main)
html+='''<h2>3. 边中点解释的补充比较</h2><p>另算一组：U 的位置不变，V 的初值及参考值取 yᵤ−h/2，符合附件的边变量解释。RHS 不变，但重新初始化并积分，并非事后换坐标。本表 v 的采样点与 FD/PE 不同，倍数仅作同区域最大误差的补充参考，不能称为共点评价。所有 v 点均在目标区域内。</p>'''
html+=table(['算例','附件边中点: u / v','相对 FD 的倍数'],mid)
html+='<p>在边中点作光滑展开，第一式局部残差为 O(h²)，第二式仍含 h∂ₓ[−2v+v²/4−uᵧ²/4] 的首项。因此仅改变 V 的位置解释不能使整个格式变为二阶。该局部展开与 u 改善明显、v 仍偏大的观察相符，但不是全局误差定理。</p>'
html+='''<h2>4. 实现与核验</h2><p>状态为 P=δ₋U 与 V，给定下侧 U 后累加恢复 U。该实现与原文对第一式沿 y 累加后直接推进 U 等价：</p><pre>Pₜ = −δ₋D₁(U²/2+2aU) − D₂V
Vₜ = −D₁[(M₋U+2a−2h)V + hV²/4 − 4M₋U + D₁P − hP²/4]</pre>'''
html+=f'<p>四组 FD/PE 重算均复现原论文公布数字，差异在表格舍入范围内。解析 τ 导数独立检查的非线性方程最大残差为 {maxres:.2e}，原生节点初值恢复误差均小于 10⁻¹⁰。Δt 减半后的最大终点场差为 {maxdt:.2e}，没有改变排名。</p>'
html+=table(['算例','共点: dt/2 场差 u / v','边中点: dt/2 场差 u / v'],times)
html+='''<h2>5. 精确格点模型差与本轮总误差</h2><p>另构造保持相同 p、q、a、系数及相位的附件格点精确解，将每个 y 相位率替换为 [log(1+h/(p−a))−log(1−h/(q+a))]/h，并按附件定义恢复 U、V。其双线性式和非线性式均已核验。下表前两项在函数层面相加为总误差，但两个最大范数不能相加。</p>'''
html+=table(['算例','格点精确解−连续解: u / v','数值解−格点精确解: u / v','模型差末级观测阶: u / v'],gaps)
html+='''<p>本轮从共同连续初值出发，故“数值解−格点精确解”包含初边值不匹配，不能称为纯积分误差。两项存在抵消，总误差可以远小于各自范数。末列来自固定物理坐标下的解析模型差加密 h=0.1、0.05、0.025，趋近一阶；不是一般初值的演化收敛试验。</p><h2>6. 结果范围</h2><p>在我们论文四组参数及共同中心 x 差分下，附件方法未取得比 FD 更小的连续场终点误差。改变 V 的位置解释显著影响结果，必须声明采样位置。附件原文的极小误差针对半离散精确解，使用 Fourier 配点与不同参数，不能直接与本表比较。</p><p>本轮未验证长期稳定性，也未证明一般初值的空间收敛；原文开链高频增长机制仍需单独研究。二阶一致性不能替代稳定性分析。</p>'''
rel='../Workspaces/dlw_paper_20261009/paper_comparison_20261022/'
html+=f'<p><a href="{rel}README.md">协议与复现说明</a> · <a href="{rel}results.json">全部运行结果</a> · <a href="{rel}summary_validation.json">核验汇总</a> · <a href="../Paper/sources/dlw_y_lattice_20261018/DLW_y_lattice_and_2HS.pdf">附件原文</a> · <a href="dlw_paper_draft.html">我们的论文</a></p></body></html>'
out=R/'report/dlw_paper_method_comparison_20261022.html';out.write_text(html,encoding='utf8')
for href in re.findall(r'href="([^"]+)"',html):assert (out.parent/href).exists(),href
print(json.dumps(dict(main=main,midpoint=mid,max_time_difference=maxdt),ensure_ascii=False,indent=2))
