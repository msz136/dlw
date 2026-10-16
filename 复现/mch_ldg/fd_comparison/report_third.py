"""FD3-specific analysis, figure and concise HTML from immutable trajectories."""
import json,html
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from analyze_comparison import HERE,ROOT,records,label,evaluator
from mch.exact import profile

data=json.loads((HERE/'analysis/comparison.json').read_text());allrows=data['rows'];rr=records()
third=[r for r in rr if r['kind']=='FD' and r['config']['order']==3]
def select(case,t,method,dt=None):
    z=[r for r in allrows if r['case']==case and r['t']==t and r['method']==method and (dt is None or r['dt']==dt)]
    return sorted(z,key=lambda r:r['dof'])

smooth=select('5.1',.5,'FD3 aligned',.0005)
orders=[float(np.log2(a['l2_u']/b['l2_u'])) for a,b in zip(smooth[:-1],smooth[1:])]
timecontrols=[]
for offset in [0.,.5]:
    subset=[r for r in third if r['config']['case']=='5.4' and r['config']['n']==2560 and r['config']['offset']==offset]
    a=next(r for r in subset if r['config']['dt']==.00025);b=next(r for r in subset if r['config']['dt']==.000125)
    if a['summary']['completed'] and b['summary']['completed']:
        ua=np.load(Path(a['path'])/'trajectory.npz')['u'][-1];ub=np.load(Path(b['path'])/'trajectory.npz')['u'][-1]
        timecontrols.append(dict(case='5.4',offset=offset,native_l2_distance=float(np.sqrt(40/2560*np.sum((ua-ub)**2))),linf_distance=float(max(abs(ua-ub)))))
subset=[r for r in third if r['config']['case']=='5.1' and r['config']['n']==1280]
a=next(r for r in subset if r['config']['dt']==.0005);b=next(r for r in subset if r['config']['dt']==.00025)
ua=np.load(Path(a['path'])/'trajectory.npz')['u'][-1];ub=np.load(Path(b['path'])/'trajectory.npz')['u'][-1]
timecontrols.append(dict(case='5.1',offset=0.,native_l2_distance=float(np.sqrt(80/1280*np.sum((ua-ub)**2))),linf_distance=float(max(abs(ua-ub)))))
verification=json.loads((HERE/'verification_third.json').read_text())
ss=[r for r in allrows if r['case']=='5.1' and r['t']==.5 and r['dt']==.0005 and r['dof']==1280 and r['method'] in ['LDG-c','LDG-d','FD3 aligned','FD4 aligned']]
pp=[r for r in allrows if r['case']=='5.4' and r['t']==5 and r['dt']==.00025 and r['dof']==2560 and r['method'] in ['LDG-c','LDG-d','FD3 aligned','FD3 half-cell']]
ldg=next(r for r in ss if r['method']=='LDG-c');fd=next(r for r in ss if r['method']=='FD3 aligned')
result=dict(fd3_run_count=len(third),completed=sum(r['summary']['completed'] for r in third),smooth_orders=orders,
            smooth_fd3_over_ldgc=fd['l2_u']/ldg['l2_u'],smooth_equal_dof=ss,peak_equal_dof=pp,time_controls=timecontrols,
            verification=verification,failures=[r['summary'] for r in third if not r['summary']['completed']])
(HERE/'analysis/third_summary.json').write_text(json.dumps(result,indent=2),encoding='utf-8')

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'savefig.bbox':'tight'})
colors={'LDG-c':'#2166ac','LDG-d':'#d6604d','FD3 aligned':'#762a83','FD3 half-cell':'#238b45','FD4 aligned':'#777777'}
fig,axes=plt.subplots(2,2,figsize=(12,8),layout='constrained')
for method in ['LDG-c','LDG-d','FD3 aligned','FD4 aligned']:
    rows=select('5.1',.5,method,.0005)
    axes[0,0].loglog([r['dof'] for r in rows],[r['l2_u'] for r in rows],marker='o',ms=4,color=colors[method],ls='--' if method in ['LDG-d','FD4 aligned'] else '-',label=method)
axes[0,0].set(xlabel='Evolved scalar degrees of freedom',ylabel=r'$L^2$ error of $u$',title='Smooth soliton, t = 0.5')
axes[0,0].legend(frameon=False,fontsize=8)
axes[0,1].plot([r['n'] for r in smooth[1:]],orders,marker='o',color=colors['FD3 aligned'],label='Observed FD3 order')
axes[0,1].axhline(3,color='black',ls=':',lw=1,label='Order 3');axes[0,1].set(xlabel='Fine-grid node count',ylabel='Observed order',title='FD3 spatial refinement',ylim=(2.7,3.3));axes[0,1].legend(frameon=False,fontsize=8)
xx=np.linspace(-1.5,7.5,5001);axes[1,0].plot(xx,profile('5.4',xx,5)[0],color='black',label='Exact')
for method in ['LDG-c','LDG-d','FD3 aligned','FD3 half-cell']:
    candidates=[r for r in rr if r['config']['case']=='5.4' and label(r)==method and r['config']['n']==(640 if r['kind']=='LDG' else 2560) and r['config']['dt']==.00025 and r['summary']['completed']]
    if candidates:
        r=candidates[0];a=np.load(Path(r['path'])/'trajectory.npz');axes[1,0].plot(xx,evaluator(r,a['u'][-1])(xx),color=colors[method],ls='--' if method in ['LDG-d','FD3 half-cell'] else '-',lw=1.1,label=method)
    rows=select('5.4',5,method,.00025)
    if rows:axes[1,1].loglog([r['dof'] for r in rows],[r['l2_u'] for r in rows],marker='o',ms=4,color=colors[method],ls='--' if method in ['LDG-d','FD3 half-cell'] else '-',label=method)
axes[1,0].set(xlabel='x',ylabel='u',title='Peakon, t = 5 | 2560 evolved degrees of freedom');axes[1,0].legend(frameon=False,fontsize=8,loc='upper left')
axes[1,1].set(xlabel='Evolved scalar degrees of freedom',ylabel=r'$L^2$ error of $u$',title='Peakon refinement, completed runs');axes[1,1].legend(frameon=False,fontsize=8)
for ax in axes.ravel():ax.grid(alpha=.15)
fig.suptitle('Third-order direct difference vs P3 LDG | RK4 and common physical-field evaluation',fontsize=13)
out=HERE/'figures';out.mkdir(exist_ok=True)
for ext in ['png','pdf']:fig.savefig(out/f'third_fd_ldg.{ext}',dpi=300)
plt.close(fig)

fmt=lambda x:f'{x:.6g}'
def table(head,rows):
    return '<div class="scroll"><table><thead><tr>'+''.join('<th>'+html.escape(str(x))+'</th>' for x in head)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+html.escape(str(x))+'</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table></div>'
st=table(['方法','单元／节点数','自由度','L²误差','采样L∞误差'],[[r['method'],r['n'],r['dof'],fmt(r['l2_u']),fmt(r['sampled_linf_u'])] for r in ss])
pt=table(['方法','L²误差','采样L∞误差','峰位误差','峰高'],[[r['method'],fmt(r['l2_u']),fmt(r['sampled_linf_u']),fmt(r['peak_position_error']),fmt(r['peak_height'])] for r in pp])
ref=table(['节点数','格距','L²误差','观测阶'],[[r['n'],fmt(80/r['n']),fmt(r['l2_u']),('—' if i==0 else f'{orders[i-1]:.4f}')] for i,r in enumerate(smooth)])
tc=table(['算例','节点偏移','半步长末态L²差','最大节点差'],[[r['case'],r['offset'],fmt(r['native_l2_distance']),fmt(r['linf_distance'])] for r in timecontrols])
body=f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>三阶直接差分与P³ LDG</title><style>
body{{max-width:1040px;margin:44px auto;padding:0 24px;font:17px/1.8 "Microsoft YaHei",sans-serif;color:#20252b}}h1{{font-size:29px}}h2{{font-size:23px;margin-top:32px}}img{{width:100%;height:auto}}.scroll{{overflow:auto}}table{{border-collapse:collapse;width:100%;font-size:14px}}th,td{{padding:8px 10px;text-align:right;border-bottom:1px solid #ddd;white-space:nowrap}}thead{{border-top:2px solid #333;border-bottom:1px solid #333}}th:first-child,td:first-child{{text-align:left}}a{{color:#2166ac}}.caption{{font-size:14px;color:#555}}.eq{{padding:16px;text-align:center;font-family:Georgia,serif;font-size:19px}}@media(max-width:600px){{body{{padding:0 14px;font-size:16px}}h1{{font-size:25px}}}}@media print{{figure,table{{break-inside:avoid}}}}</style><main>
<h1>三阶直接差分与 P³ LDG 的比较</h1><p class="caption">2026年10月15日 · 原mCH方程、同一物理初值、RK4、共同物理场评价</p>
<p>新增三阶迎风直接差分FD3，完成{len(third)}条运行中的{result['completed']}条。光滑孤子的整体误差按约三阶下降；相同1280个演化自由度下，FD3的物理场L²误差约为守恒P³ LDG的{result['smooth_fd3_over_ldgc']:.2f}倍。这比较的是两套具体格式的物理场表现，不能将论文联合范数的三阶保证等同于单独u场的三阶精度。</p>
<h2>1　三阶格式的定义</h2><p>对称中心模板通常给偶数精度阶。本次采用三阶迎风通量差分，辅助导数保持四阶，以避免低阶辅助模板掩盖整体三阶：</p>
<div class="eq">r=D₁⁽⁴⁾u，m=(I−D₂⁽⁴⁾)u，F=2κ²u+(u²−r²)m。</div>
<div class="eq">m<sub>t</sub>=−D₃⁻[(F+αm)/2]−D₃⁺[(F−αm)/2]，α=maxᵢ|uᵢ²−rᵢ²|。</div>
<p>每个RK阶段冻结空间常数α。D₃⁻f=(fᵢ₋₂−6fᵢ₋₁+3fᵢ+2fᵢ₊₁)/(6h)，D₃⁺为其镜像。该分裂等价于四阶中心通量导数加一个h³阶的高频耗散项，因此整体空间精度为三阶。未使用限制器、滤波或精确解强迫；α由当前数值状态决定。这里没有新的非线性能量稳定定理。</p>
<p>14项模板矩、离散符号关系、守恒及完整右端检查通过，独立右端一致性观测阶为{verification['rhs_observed_order']:.4f}。</p>
<h2>2　光滑孤子的三阶验证</h2><p>沿用例5.1，α=0.5，区间(−40,40)，T=0.5，dt=0.0005。此处α为解析解幅度参数，与通量分裂速度α不是同一个量。下表给出FD3的完整加密序列：</p>{ref}
<p>同1280个演化自由度的对照为：</p>{st}
<p>P³ LDG在单独u场上的误差呈现接近四阶，而FD3的整体空间精度为三阶；因此随加密两者差距扩大是允许的。四阶差分作为已有参照并列，表明常规差分本身并非只能达到当前FD3误差。</p>
<figure><img src="../复现/mch_ldg/fd_comparison/figures/third_fd_ldg.png" alt="三阶差分与LDG的光滑加密和尖峰传播比较"></figure>
<h2>3　尖峰结果</h2><p>例5.4采用(−20,20)、c=1、T=5，dt=0.00025。FD3覆盖N=320、640、1280、2560及节点对齐／半格两种相位。相同2560个演化自由度下：</p>{pt}
<p>峰子不满足光滑解的三阶误差估计条件。高阶通量中的数值耗散会影响峰高和传播位置，因此应同时查看峰位、峰高与误差，而不能只凭能量或是否到终点评价方法。</p>
<p>本次FD3的两种网格相位均能到达终点，但峰高降至约0.92、峰位落后约0.86—0.90，误差高于两套LDG。四层网格上的FD3尖峰误差下降缓慢，不能认定已进入逼近指定尖峰弱解的收敛区间；光滑解三阶检验也不能替代这一判断。</p>
<h2>4　时间与评价控制</h2><p>最细网格减半时间步的离散状态差如下：</p>{tc}
<p>物理u继续使用相同积分点和密集采样集评价：FD为周期三次样条重构，LDG为原生分片多项式。初态表示误差另存，评价规则再次加密。比较按演化自由度进行，不等于计算时间相同，也不宣称所有三阶有限差分都有相同行为。</p>
<p class="caption"><a href="../复现/mch_ldg/fd_comparison/PROTOCOL_THIRD.md">三阶协议</a> · <a href="../复现/mch_ldg/fd_comparison/analysis/third_summary.json">数值摘要</a> · <a href="mch_ldg_fd_comparison_20261015.html">此前FD2／FD4对照</a></p></main></html>'''
target=HERE.parents[2]/'report/mch_ldg_fd3_comparison_20261015.html';target.write_text(body,encoding='utf-8')
print(json.dumps(dict(fd3_runs=len(third),completed=result['completed'],smooth_orders=orders,smooth_ratio=result['smooth_fd3_over_ldgc'],time_controls=timecontrols),indent=2))
print(str(target))
