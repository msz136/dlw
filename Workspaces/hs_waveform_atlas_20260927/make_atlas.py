"""Five figure families, physical errors and parameter scan, all explicit Euler."""
import csv
import json
import base64
import re
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from run_experiments import HERE,OUT,PREVIOUS,PS,REPRESENTATIVES,ROUTES,TIMES,SOURCE,engine,sha

FIG=HERE/'figures';FIG.mkdir(exist_ok=True)
saved=json.loads((OUT/'results.json').read_text(encoding='utf-8'))
rows=list(saved['rows'].values())
assert len(rows)==405 and all(r['status']=='completed' for r in rows)
assert sha(SOURCE)==saved['source_results_sha256']
for name,h in engine.source_hashes().items():assert saved['source_hashes'][name]==h
for file in ('run_designed_cases.py',):assert sha(PREVIOUS/file)==saved['source_hashes'][file]
assert sha(HERE/'run_experiments.py')==saved['source_hashes']['run_experiments.py']
for r in rows:
    assert sha(r['profile'])==r['profile_sha256']
    assert r['min_h']>0 and r['min_rho']>0
def get(p,route,purpose='main'):
    return next(r for r in rows if r['spec']['p']==p and r['spec']['route']==route and r['spec']['purpose']==purpose)
def err(p,route,t,field,region='core',purpose='main',fine=False):
    return get(p,route,purpose)['snapshots'][str(t)]['eval_32001' if fine else 'errors'][region][field]
def fields(p,route,t,purpose='main'):
    with np.load(get(p,route,purpose)['profile']) as a:
        return tuple(a[f't{t}_{k}'] for k in ('x','u','rho_x','rho'))
def soliton(p):return engine.initialize(p,'difference_matched',400)[0]

flat=[]
for r in rows:
    for t in TIMES:
        for region in ('core','peak'):
            flat.append({**r['spec'],'time':t,'region':region,**r['snapshots'][str(t)]['errors'][region],
                         'provenance':r['provenance']})
with (OUT/'errors.csv').open('w',newline='',encoding='utf-8-sig') as f:
    writer=csv.DictWriter(f,fieldnames=list(flat[0]));writer.writeheader();writer.writerows(flat)

pairs=[('difference_rm','difference_fixed'),('integrable_calibrated','difference_matched')]
ratios=[];timeflips=[];spaceflips=[];evalflips=[]
for a,b in pairs:
    for p in PS:
        for t in TIMES:
            for region in ('core','peak'):
                r=dict(p=p,time=t,region=region,numerator=a,denominator=b)
                for field in ('u','rho'):
                    r[field]=err(p,a,t,field,region)/err(p,b,t,field,region)
                    r[field+'_half']=err(p,a,t,field,region,'time_half')/err(p,b,t,field,region,'time_half')
                    if (r[field]<1)!=(r[field+'_half']<1):timeflips.append({**r,'field':field})
                    fine=err(p,a,t,field,region,fine=True)/err(p,b,t,field,region,fine=True)
                    if (r[field]<1)!=(fine<1):evalflips.append({**r,'field':field})
                    if p in REPRESENTATIVES:
                        refined=err(p,a,t,field,region,'space_time_half')/err(p,b,t,field,region,'space_time_half')
                        if (r[field+'_half']<1)!=(refined<1):spaceflips.append({**r,'field':field,'refined_ratio':refined})
                ratios.append(r)
max_eval=max(abs(r['snapshots'][str(t)]['eval_32001'][region][f]/r['snapshots'][str(t)]['errors'][region][f]-1)
             for r in rows for t in TIMES for region in ('core','peak') for f in ('u','rho'))
summary=dict(completed=405,new=sum(r['provenance']=='new' for r in rows),reused=sum(r['provenance']=='reused' for r in rows),
             ratios=ratios,time_ranking_changes=timeflips,space_ranking_changes=spaceflips,
             evaluation_ranking_changes=evalflips,max_evaluation_relative_change=max_eval,
             min_h=min(r['min_h'] for r in rows),min_rho=min(r['min_rho'] for r in rows))

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,
                     'axes.spines.right':False,'figure.facecolor':'white','axes.facecolor':'white',
                     'axes.grid':True,'grid.alpha':.15,'pdf.fonttype':42})
colors={'integrable_original':'#929292','integrable_calibrated':'#267548','difference_matched':'#8855a1',
        'difference_rm':'#b36521','difference_fixed':'#276ba5'}
labels={'integrable_original':'Original integrable','integrable_calibrated':'Calibrated integrable',
        'difference_matched':'Matched FD','difference_rm':'FD + Rm mesh','difference_fixed':'FD + fixed mesh'}
styles={'integrable_original':':','integrable_calibrated':'--','difference_matched':'-.','difference_rm':'--','difference_fixed':':'}
FIGURES=[]
def save(fig,name,title,caption):
    fig.savefig(FIG/(name+'.png'),dpi=165,bbox_inches='tight')
    fig.savefig(FIG/(name+'.pdf'),bbox_inches='tight')
    plt.close(fig)
    FIGURES.append(dict(name=name,title=title,caption=caption))

xplot=np.linspace(-2.,2.,4001)
point_readback=0.;reference_roundtrip=0.
for t in TIMES:
    arrays={'x':xplot,'p':np.array(PS)}
    truths=[]
    curves={r:[] for r in ROUTES}
    for p in PS:
        sol=soliton(p);u,rho,_,res=engine.safe_reference(sol,xplot,t);reference_roundtrip=max(reference_roundtrip,res)
        truths.append(np.stack([u,rho]))
        for route in ROUTES:
            x,nu,rx,nr=fields(p,route,t)
            assert max(x[0],rx[0])<=-2 and min(x[-1],rx[-1])>=2
            curves[route].append(np.stack([np.interp(xplot,x,nu),np.interp(xplot,rx,nr)]))
            # Independent readback on the prescribed metric grid.
            xx=np.linspace(-2,2,16001);eu,er,_,_=engine.safe_reference(sol,xx,t)
            remeasure=[np.max(abs(np.interp(xx,x,nu)-eu)),np.max(abs(np.interp(xx,rx,nr)-er))]
            for f,val in zip(('u','rho'),remeasure):point_readback=max(point_readback,abs(float(val)-err(p,route,t,f)))
    truths=np.array(truths);arrays['exact']=truths
    for route in ROUTES:
        curves[route]=np.array(curves[route]);arrays[route]=curves[route];arrays[route+'_abs_error']=abs(curves[route]-truths)
    np.savez_compressed(OUT/f'waveform_samples_t{t:g}.npz',**arrays)
    tag=str(t).replace('.','p')

    # Family 1: solution overlays, two well-defined comparisons kept readable.
    for group,selected in [('mesh',ROUTES[3:]),('calibration',ROUTES[1:3])]:
        fig,axs=plt.subplots(2,3,figsize=(12,6),layout='constrained')
        for j,p in enumerate(REPRESENTATIVES):
            idx=PS.index(p)
            for fi,f in enumerate(('u','rho')):
                ax=axs[fi,j];ax.plot(xplot,truths[idx,fi],color='#202020',lw=1.6,label='Analytic')
                for route in selected:
                    ax.plot(xplot,curves[route][idx,fi],styles[route],color=colors[route],lw=1.15,label=labels[route])
                    data=fields(p,route,t);xn,yn=(data[0],data[1]) if fi==0 else (data[2],data[3])
                    indices=np.flatnonzero((xn>=-2)&(xn<=2));indices=indices[::max(1,len(indices)//30)]
                    ax.plot(xn[indices],yn[indices],linestyle='none',marker='o' if route==selected[0] else 'x',
                            ms=3,mfc='none',color=colors[route],alpha=.75)
                ax.set(xlabel='physical x',ylabel=r'$u$' if fi==0 else r'$\rho$',title=f'p = {p:g}, t = {t:g}')
                if j==0:ax.legend(fontsize=8,frameon=False)
        save(fig,f'01_{group}_t{tag}',f'波形叠加 · {"Rₘ / 固定网格" if group=="mesh" else "校准 / 同变量差分"} · t={t:g}',
             '黑线为连续解析解，彩线为数值重构，标记取自实际数值节点（密度使用各格式本来的配点）。曲线接近重合时，应结合下方误差图判断。')
    # Family 2: pointwise physical-field errors; original included as context.
    fig,axs=plt.subplots(2,3,figsize=(12,6.3),layout='constrained')
    for j,p in enumerate(REPRESENTATIVES):
        idx=PS.index(p)
        for fi,f in enumerate(('u','rho')):
            ax=axs[fi,j]
            for route in ROUTES:
                e=arrays[route+'_abs_error'][idx,fi]
                ax.semilogy(xplot,np.where(e>0,e,np.nan),styles[route],color=colors[route],lw=1.15,label=labels[route])
            ax.set(xlabel='physical x',ylabel=f'absolute {f} error',title=f'p = {p:g}, t = {t:g}',ylim=(1e-12,.2))
            if j==0:ax.legend(fontsize=7,frameon=False)
    save(fig,f'02_error_x_t{tag}',f'逐点绝对误差 · 物理坐标 x · t={t:g}',
         '画 |数值解−连续解析解|，不扣除初始或重构误差。纵轴为对数；零值不画，低于 10⁻¹² 的值在图外，原始数据完整保留。')
    # Family 3: the same physical error sampled through a common analytic y=X map.
    fig,axs=plt.subplots(2,3,figsize=(12,6.3),layout='constrained');ysamples={}
    for j,p in enumerate(REPRESENTATIVES):
        sol=soliton(p);_,_,yb,_=engine.safe_reference(sol,np.array([-2.,2.]),t)
        yy=np.linspace(yb[0],yb[1],4001);eu,xx,er=sol.continuous_X(yy,t)
        ysamples[f'p{p:g}_y']=yy;ysamples[f'p{p:g}_x_exact']=xx
        for fi,f in enumerate(('u','rho')):
            ax=axs[fi,j];truth=eu if fi==0 else er
            for route in ROUTES:
                d=fields(p,route,t);xn,yn=(d[0],d[1]) if fi==0 else (d[2],d[3])
                e=abs(np.interp(xx,xn,yn)-truth)
                ysamples[f'p{p:g}_{route}_{f}_abs_error']=e
                ax.semilogy(yy,np.where(e>0,e,np.nan),styles[route],color=colors[route],lw=1.15,label=labels[route])
            ax.set(xlabel='y = X (mass coordinate)',ylabel=f'absolute {f} error',title=f'p = {p:g}, t = {t:g}',ylim=(1e-12,.2))
            if j==0:ax.legend(fontsize=7,frameon=False)
    np.savez_compressed(OUT/f'y_samples_t{t:g}.npz',**ysamples)
    save(fig,f'03_error_y_t{tag}',f'逐点绝对误差 · 辅助坐标 y=X · t={t:g}',
         '此处 y 是连续质量坐标，不是孤子参数。所有数值场都在同一个解析物理位置 x_exact(y,t) 上取值，避免按不同网格的编号直接相减。')
    # Family 4: parameter response and two explicit baseline ratios.
    fig,axs=plt.subplots(2,2,figsize=(11,7),layout='constrained')
    for fi,f in enumerate(('u','rho')):
        ax=axs[0,fi]
        for route in ROUTES:
            ax.semilogy(PS,[err(p,route,t,f) for p in PS],styles[route],color=colors[route],label=labels[route])
        ax.set(xlabel='soliton parameter p',ylabel=f'max |{f} error|',title=f'Core [-2,2], t = {t:g}')
        ax.legend(fontsize=8,frameon=False)
        ax=axs[1,fi]
        for (a,b),color,label in zip(pairs,['#b36521','#267548'],['Rm / fixed','Calibrated / matched']):
            for purpose,style,width in [('main','-',1.6),('time_half',':',1.)]:
                vals=[err(p,a,t,f,purpose=purpose)/err(p,b,t,f,purpose=purpose) for p in PS]
                ax.semilogy(PS,vals,style,color=color,lw=width,label=label+(' (half dt)' if purpose=='time_half' else ''))
        ax.axhline(1,color='#333333',ls='--',lw=.8)
        ax.set(xlabel='soliton parameter p',ylabel=f'{f} error ratio',title='Below 1: improvement')
        ax.legend(fontsize=8,frameon=False)
    save(fig,f'04_parameter_scan_t{tag}',f'固定时刻的参数扫描 · t={t:g}',
         '39 个 p=3,3.5,…,22；上排为共同核心最大总误差，下排为两组配对误差比。实线为主 Euler 步长，点线为步长减半。连线仅连接采样点，不代表已证明连续参数区间的门槛。')
    # Family 5: absolute error in x-p plane, shared scale within each field.
    heat_routes=('difference_fixed','difference_rm','difference_matched','integrable_calibrated')
    fig,axs=plt.subplots(2,4,figsize=(13,6.5),layout='constrained')
    for fi,f in enumerate(('u','rho')):
        vmax=max(np.max(arrays[r+'_abs_error'][:,fi]) for r in heat_routes)
        for j,route in enumerate(heat_routes):
            im=axs[fi,j].imshow(arrays[route+'_abs_error'][:,fi],origin='lower',aspect='auto',
                    extent=[-2,2,2.75,22.25],norm=LogNorm(vmin=1e-12,vmax=vmax),cmap='magma',interpolation='nearest')
            axs[fi,j].set(xlabel='physical x',ylabel='parameter p',title=labels[route]+f' / {f}');axs[fi,j].grid(False)
        fig.colorbar(im,ax=axs[fi,:],label=f'absolute {f} error',shrink=.88)
    save(fig,f'05_error_map_t{tag}',f'误差分布图 · 空间 x × 参数 p · t={t:g}',
         '每一横行是一个独立参数案例在固定时刻的空间误差。同一物理场的四图共用色标；低于 10⁻¹² 的值按色标下限显示。这里的 p 维度是实验扫描维度，不是 2HS 新增的空间维度。')

assert point_readback<1e-11
summary['pointwise_metric_readback_max']=point_readback;summary['reference_inversion_max']=reference_roundtrip
summary['figures']=FIGURES
engine.dump(OUT/'summary.json',summary)
print(json.dumps({k:v for k,v in summary.items() if k not in ('ratios','figures','time_ranking_changes','space_ranking_changes')},indent=2))
print('Time ranking changes:',len(timeflips),'Space ranking changes:',len(spaceflips))
for a,b in pairs:
    for t in TIMES:
        selected=[r for r in ratios if r['numerator']==a and r['time']==t and r['region']=='core']
        print(a,t,'u wins',[r['p'] for r in selected if r['u']<1], 'rho wins',sum(r['rho']<1 for r in selected))
