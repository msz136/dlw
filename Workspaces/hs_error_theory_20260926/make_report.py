"""Generate tables and figures from saved results, then fill the paper template."""
import json
import re
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from run_designed_cases import HERE, OUT, PS, TIMES, ROUTES

data=json.loads((OUT/'results.json').read_text(encoding='utf-8'))
summary=json.loads((OUT/'summary.json').read_text(encoding='utf-8'))
theory=json.loads((HERE/'theory_checks.json').read_text(encoding='utf-8'))
rows=list(data['rows'].values())
def get(p,route,purpose='main'):
    return next(r for r in rows if r['spec']['p']==p and r['spec']['route']==route and r['spec']['purpose']==purpose)
def err(p,route,t,region='core',purpose='main'):
    return get(p,route,purpose)['snapshots'][str(t)]['errors'][region]
def pair(e,ratio=False):
    return ' / '.join(f'{e[f]:.3f}' if ratio else f'{e[f]:.3e}' for f in ('u','rho'))
def table(headers,body,caption):
    return '<div class="table-wrap"><table class="numeric"><caption>'+caption+'</caption><thead><tr>'+''.join('<th scope="col">'+h+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr><th scope="row">'+str(r[0])+'</th>'+''.join('<td class="num">'+str(c)+'</td>' for c in r[1:])+'</tr>' for r in body)+'</tbody></table></div>'
def absolute_table(purpose):
    labels=['$p$','原可积','校准可积','普通差分<br>同变量','普通差分<br>固定格','普通差分<br>$R_m$ 网格']
    return table(labels,[[int(p)]+[pair(err(p,r,.5,purpose=purpose)) for r in ROUTES] for p in PS],
                 '共同物理核心 [−2, 2]；t = 0.5；每格为 u / ρ 的最大绝对误差。')
def ratio(p,t,region,purpose='main'):
    a,b=err(p,'integrable_calibrated',t,region,purpose),err(p,'difference_matched',t,region,purpose)
    return {k:a[k]/b[k] for k in ('u','rho')}

coef=[]
for p in PS:
    s=1-2/p;rho0=1-s*s
    bd=s**4*(s**4-4)/6;bc=2/3*s**4*(1-s*s)*(2-s*s)
    coef.append([int(p),f'{rho0:.4f}',f'{bd:.5f}',f'{bc:.5f}',f'{abs(bc/bd):.4f}',f'{bc/rho0**2:.4f}'])
coeff_table=table(['$p$','$\\rho_0$','$B_{D,0}$','$B_{C,0}$','$\\Gamma$','$B_{C,0}/\\rho_0^2$'],coef,
                 '同一波峰、同一连续解。最后一列是固定质量步长下的校准残差系数。')
late_table=table(['$p$','RK4 波峰','RK4 全域','Euler 波峰','Euler 全域'],
     [[int(p)]+[pair(ratio(p,.5,g,purpose),True) for purpose in ('main','euler') for g in ('peak','core')] for p in PS],
     't = 0.5；每格为校准式 / 同变量普通差分的 u / ρ 误差比。')
all_tables=''.join(table(['$p$']+[f't = {t:g}' for t in TIMES[1:]],
     [[int(p)]+[pair(ratio(p,t,g),True) for t in TIMES[1:]] for p in PS],
     ('RK4 · 波峰区域' if g=='peak' else 'RK4 · 共同全域')+'；每格为 u / ρ 误差比。') for g in ('peak','core'))
initial=table(['$p$','共同全域','波峰区域'],[[int(p)]+[pair(err(p,'difference_matched',0.,g)) for g in ('core','peak')] for p in PS],
              't = 0；三条同变量路线共有的重构误差，u / ρ 同格。')

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,
                     'axes.spines.right':False,'axes.labelcolor':'#282722','text.color':'#282722',
                     'axes.edgecolor':'#706b61','xtick.color':'#706b61','ytick.color':'#706b61',
                     'figure.facecolor':'#fffdf9','axes.facecolor':'#fffdf9','svg.fonttype':'path'})
fig,axes=plt.subplots(1,3,figsize=(11.2,3.5),layout='constrained')
grid=np.linspace(5,24,200);s=1-2/grid
axes[0].plot(grid,4*(1-s*s)/(2+s*s),color='#8a5a2b',lw=1.7)
sp=1-2/np.array(PS)
axes[0].scatter(PS,4*(1-sp*sp)/(2+sp*sp),color='#8a5a2b',s=28,zorder=3)
axes[0].axhline(.5,color='#706b61',ls=':',lw=1)
axes[0].set(title='Peak RHS coefficient',xlabel='p',ylabel=r'$|B_C|\,/\,|B_D|$',ylim=(0,1.2))
for ax,field in zip(axes[1:],('u','rho')):
    for g,label,style in [('peak','Peak window','-'),('core','Core [-2, 2]','--')]:
        ax.plot(PS,[ratio(p,.5,g)[field] for p in PS],style,marker='o' if g=='peak' else 's',
                color='#8a5a2b' if g=='peak' else '#706b61',label=label,lw=1.5,ms=4)
    ax.axhline(1,color='#b9ad9d',ls=':',lw=1)
    ax.set(title=('u' if field=='u' else r'$\rho$')+' error, t = 0.5',xlabel='p',ylabel='Calibrated / ordinary')
    ax.legend(frameon=False,fontsize=8,loc='best')
for ax in axes:ax.grid(axis='y',alpha=.13);ax.set_xticks([8,11,14,18,22])
fig.savefig(HERE/'coefficient_and_error_ratios.svg',bbox_inches='tight')
fig.savefig(HERE/'coefficient_and_error_ratios.pdf',bbox_inches='tight')
fig.savefig(HERE/'coefficient_and_error_ratios.png',dpi=170,bbox_inches='tight')
plt.close(fig)
svg=(HERE/'coefficient_and_error_ratios.svg').read_text(encoding='utf-8')
svg=svg[svg.index('<svg'):]
svg=svg.replace('<svg ','<svg role="img" aria-label="理论系数比与实际双场误差比" ',1)
controls=summary['controls']
validation=table(['检查','结果'],[
 ['轨道完整性','135 / 135 完成；旧求解器源码哈希不变'],
 ['代数核对',f"{len(theory['symbolic_checks'])} 条符号恒等式残差为零"],
 ['独立胞元积分',f"d = 0.0025 时系数最大相对差 {max(r['coefficient_relative_error'] for r in theory['cell_quadrature'] if r['d']==.0025):.2e}"],
 ['空间加密','N = 400 → 800；校准式观测阶 1.830–2.055，同变量差分 1.898–2.057'],
 ['RK4 时间减半',f"细格场值最大变化 {summary['rk4_half_step_field_linf']:.2e}；误差相对变化 ≤ {controls['time_control']['max_relative_error_change']:.2e}"],
 ['评价点加密',f"16001 → 32001；所有记录误差最大相对变化 {100*summary['max_evaluation_relative_change']:.3f}%"],
 ['扩域对照',f"p = 8, 22；L = 4 → 5 且 N = 400 → 500，保持 a = 0.02；跨路线最大误差变化 {100*controls['domain_control']['max_relative_error_change']:.2f}%"],
 ['主对照方向','空间加密、RK4 减步、Euler 两步长、评价加密：各 80 项方向无翻转；扩域 32 项无翻转'],
 ['独立参照往返',f"质量坐标最大差 {summary['reference_round_trip_max']:.2e}；双场最大差 {summary['reference_field_max']:.2e}"],
 ['网格与密度',f"全部记录 min d = {summary['min_h']:.6f}，min ρ = {summary['min_rho']:.6f}，均为正"]
 ],'空间观测阶覆盖所有四个时刻、两场与两个评价区域；方向项指校准式相对同变量普通差分。')

theme_source=(HERE.parent/'gsg_project/dlw_report/_src/miura_dlw.src.html').read_text(encoding='utf-8')
theme=re.findall(r'<style>([\s\S]*?)</style>',theme_source)[1]
source=(HERE/'_src/report.template.html').read_text(encoding='utf-8')
replacements={'THEME':theme,'COEFFICIENT_TABLE':coeff_table,'RK4_TABLE':absolute_table('main'),
              'EULER_TABLE':absolute_table('euler'),'RATIO_TABLE':late_table,'ALL_RATIO_TABLES':all_tables,
              'INITIAL_TABLE':initial,'FIGURE':svg,'VALIDATION':validation,
              'REFERENCE_CHANGE':f"{summary['previous_successful_reference_max_change']:.2e}"}
for k,v in replacements.items():source=source.replace('@@'+k+'@@',v)
assert set(re.findall(r'@@(\w+)@@',source))=={'KATEX_CSS','KATEX_JS'}
(HERE/'_src/index.src.html').write_text(source,encoding='utf-8')
print(HERE/'_src/index.src.html')
