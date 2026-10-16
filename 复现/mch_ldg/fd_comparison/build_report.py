import json,html
from pathlib import Path
from analyze_comparison import HERE

data=json.loads((HERE/'analysis/comparison.json').read_text());rows=data['rows']
f=lambda x:f'{x:.6g}'
def tab(head,rr):
    return '<div class="scroll"><table><thead><tr>'+''.join('<th>'+html.escape(str(v))+'</th>' for v in head)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+html.escape(str(v))+'</td>' for v in row)+'</tr>' for row in rr)+'</tbody></table></div>'
smooth=[r for r in rows if r['case']=='5.1' and r['t']==.5 and r['dof']==1280]
st=tab(['方法','单元／节点数','演化自由度','物理场 L² 误差','采样 L∞ 误差'],[[r['method'],r['n'],r['dof'],f(r['l2_u']),f(r['sampled_linf_u'])] for r in smooth])
peak=[r for r in rows if r['case']=='5.4' and r['t']==5 and r['dt']==.00025 and r['dof']==2560]
pt=tab(['方法','物理场 L² 误差','采样 L∞ 误差','峰位误差','峰高'],[[r['method'],f(r['l2_u']),f(r['sampled_linf_u']),f(r['peak_position_error']),f(r['peak_height'])] for r in peak])
mesh=[r for r in rows if r['case']=='5.4' and r['t']==5 and r['dt']==.00025 and r['method'] in ['LDG-c','FD2 half-cell','FD4 half-cell'] and r['dof'] in [640,1280,2560]]
mt=tab(['演化自由度','方法','L² 误差','峰位误差'],[[r['dof'],r['method'],f(r['l2_u']),f(r['peak_position_error'])] for r in sorted(mesh,key=lambda r:(r['dof'],r['method']))])
fail=tab(['方法','节点数','时间步长','停止时刻','最后诊断时刻'],[[r['method'],r['n'],r['dt'],f(r['reached']),f(r['last_diagnostic_time'])] for r in data['failures']])
early=[r for r in rows if r['case']=='5.4' and r['t']==.5 and r['dt']==.00025 and r['dof']==2560]
et=tab(['方法','t=0.5 的 L² 误差','t=0.5 的采样 L∞ 误差'],[[r['method'],f(r['l2_u']),f(r['sampled_linf_u'])] for r in early])
image=lambda name,alt:f'<figure><img src="../复现/mch_ldg/fd_comparison/figures/{name}.png" alt="{alt}"></figure>'
body=f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>mCH：LDG与直接差分</title>
<style>body{{max-width:1050px;margin:44px auto;padding:0 24px;color:#20252b;font:17px/1.8 "Microsoft YaHei",sans-serif}}h1{{font-size:30px}}h2{{font-size:23px;margin-top:34px}}p{{margin:14px 0}}small,.caption{{font-size:14px;color:#555}}img{{width:100%;height:auto}}figure{{margin:24px 0}}.scroll{{overflow:auto}}table{{border-collapse:collapse;width:100%;font-size:14px}}th,td{{padding:8px 10px;border-bottom:1px solid #ddd;text-align:right;white-space:nowrap}}thead{{border-top:2px solid #333;border-bottom:1px solid #333}}td:first-child,th:first-child{{text-align:left}}a{{color:#2166ac}}.eq{{text-align:center;font-family:Georgia,serif;font-size:20px;padding:16px}}@media(max-width:600px){{body{{padding:0 14px;margin:24px auto;font-size:16px}}h1{{font-size:25px}}}}@media print{{body{{font-size:11pt}}figure,table{{break-inside:avoid}}}}</style>
<main><h1>mCH 方程：LDG 与直接有限差分的比较</h1><p class="caption">2026年10月15日 · 同一物理初值、周期截断、RK4；两类解分别作分辨率检验</p>
<p>光滑单孤子上，四阶直接差分与 P³ LDG 在相同演化自由度下精度接近。尖峰上，中心差分对初始网格位置高度敏感，守恒 LDG 在本次加密序列中更稳定地降低误差；但粗网格上的半格差分也有优于 LDG 的结果。当前比较不能推出 LDG 对所有有限差分方法都更优。</p>
<h2>1　直接差分与比较口径</h2><p>直接离散原方程，取 r=D₁u、m=(I−D₂)u，并计算</p>
<div class="eq">(I−D₂)u<sub>t</sub>=−D₁[2κ²u+(u²−r²)m]。</div>
<p>FD2和FD4分别采用二阶、四阶中心模板，D₂独立离散二阶导数。循环Helmholtz方程用FFT对角化求解，空间导数仍是有限差分。另增原动量通量的局部Rusanov耗散版本：界面通量为相邻物理通量均值减去 max|u²−r²| 乘动量跳跃的一半。该版本为一致的低阶耗散基线，尚无本项目中的非线性能量稳定证明。</p>
<p>P³ LDG每单元有4个演化系数，故640单元对应2560个差分节点。主表按相同演化自由度比较；格距控制另见原始数据。所有方法使用相同连续物理初值，但LDG作Radau投影、FD在节点采样，初始表示误差分别保存。FD由周期三次样条重构，LDG使用其原生分片多项式，在共同物理积分点评价 u 的误差。两者各自的离散能量定义不同，不把能量漂移当作跨方法精度排名。</p>
<p>共比较{data['run_count']}条轨迹（含2条复用的LDG轨迹），{data['completed']}条到达目标终点。FD的算子符号、Helmholtz逆、守恒和光滑右端一致性等15项检查通过。评价网格再次加密后，已检查终态L²误差的最大相对变化为 {f(max(r['l2_relative_difference'] for r in data['evaluation_controls']))}，采样L∞最大绝对变化为 {f(max(r['linf_absolute_difference'] for r in data['evaluation_controls']))}。</p>
<h2>2　光滑单孤子</h2><p>例5.1取α=0.5，区间(−40,40)，T=0.5，dt=0.0005。扩域用于避免前轮已发现的截断边界污染。在1280个演化自由度下：</p>{st}
{image('smooth_fd_ldg','光滑解的误差随演化自由度的变化')}
<p>FD2表现为二阶，FD4表现为四阶；本次最细网格上FD4的物理场L²误差略低于两种LDG，属于相近量级。Rusanov基线的低阶耗散显著增加光滑解误差。这里没有同一计算预算下的性能基准，故不按Python运行时间评价效率。</p>
<h2>3　尖峰：完成终点不等于网格收敛</h2><p>例5.4取c=1、κ=0、区间(−20,20)、T=5，默认dt=0.00025。对于节点采样FD，尖顶位于节点与位于半格位置是两种独立控制；LDG沿用已有单元划分。下表为2560个演化自由度、已完成共同终点的结果。精确峰高为√(3/2)，峰位为5。</p>{pt}
{image('peak_fd_ldg','尖峰剖面、误差和峰位随自由度的变化')}
<p>细网格上守恒LDG的L²误差约0.0822，小于半格FD2的0.2673和FD4的0.2500。耗散LDG误差约0.4771，反而大于这两种半格差分。Rusanov版能完成计算，但峰明显变低并落后，L²误差约1.169。稳定推进与精确保持峰子是两个不同指标。</p>
<p>完整加密序列揭示排名反转：</p>{mt}
<p>在640个自由度下半格差分比守恒LDG更准；在1280和2560个自由度下排名反转。半格FD的误差随加密先降后升，不能据其中一个低误差点宣称尖峰收敛。守恒LDG的误差在这三层上持续下降，但这些数据不构成尖峰的一般收敛定理，也不支持三阶尖峰精度。</p>
<h2>4　网格相位与时间步控制</h2><p>尖顶初始恰好落在节点时，所测试的8条中心差分基线均未到T=5。N=2560减半时间步后的两条对齐运行仍未到终点。将节点整体偏移半格后，所测试中心差分运行均完成。两种初始化都直接采样同一个精确函数；差异说明尖角与测度动量的离散表示高度敏感。</p>
<p>在共同可用时刻t=0.5、2560个自由度下：</p>{et}
<p>半格FD2/FD4在N=2560下减半时间步，终态物理误差变化低于10⁻⁸，支持其主要偏差并非当前时间步造成。Rusanov同分辨率也做了半步长控制。对节点对齐且失稳的FD4，减半步长仍改变失稳前轨迹，因此目前不把失稳严格归因于某一个机制。</p>
<details><summary>未完成运行的停止记录</summary>{fail}</details>
<h2>5　结论范围</h2><p>本次结果支持：光滑波形可以用常规高阶差分获得与LDG相近的精度；本文守恒LDG在本次尖峰加密序列中更稳定地降低误差，而中心差分对网格相位敏感。本轮没有对LDG开展完整的网格相位扫描。耗散LDG没有在所有指标上优于直接差分。后续若研究尖峰弱解选择、相容差分通量或高阶无振荡重构，需要作为新的算法分别验证，不能由当前中心差分和低阶Rusanov的结果代替。</p>
<p class="caption"><a href="../复现/mch_ldg/fd_comparison/README.md">实现与复现入口</a> · <a href="../复现/mch_ldg/fd_comparison/analysis/physical_errors.csv">共同物理场误差表</a> · <a href="mch_ldg_reproduction_20261015.html">原LDG复现报告</a></p></main></html>'''
target=HERE.parents[2]/'report/mch_ldg_fd_comparison_20261015.html';target.write_text(body,encoding='utf-8')
print(str(target))
