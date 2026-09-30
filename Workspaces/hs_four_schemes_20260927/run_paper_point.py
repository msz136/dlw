"""Paper Fig.1/3 point p5,c1,zero phases,a=.005; no centering gauge change."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import run_study as base
from run_parameter_calibration import AuditedMovingSystem
from hs_exact import Soliton
eng,ale=base.eng,base.ale
OUT=base.HERE/'paper_point';OUT.mkdir(exist_ok=True)
P=5.;C=1.;A=.005;N=1600
SOL=Soliton((P,),c=C,phase=(0.,),shift=-.8)
X=np.linspace(-4,4,N+1)
UE,XINIT,_=SOL.continuous_X(X,0.)
TIMES=(0.,.25,.5)
GRID=np.linspace(-2.5,1.5,32001)

def initialize(scheme):
    if scheme in ('S1','S2'):
        cc=C if scheme=='S1' else A+np.hypot(C,A)
        sys=AuditedMovingSystem(A,cc,N,lambda t:float(SOL.continuous_X(np.array([-4.]),t)[0][0]),'sd')
        return sys,sys.pack(np.diff(UE),np.diff(XINIT),XINIT[0])
    x=XINIT.copy() if scheme=='S3' else np.linspace(XINIT[0],XINIT[-1],N+1)
    u,r,_,_=eng.safe_reference(SOL,x,0.)
    return None,(x,ale.second_derivative(u,x)+2,r[1:-1])

def fields(sys,state,t):
    if sys is not None:return eng.fields(SOL,sys,state,t)
    x=state[0];_,r,u,_=ale.unpack(state,SOL,t,x[0],x[-1])
    return x,u,x,r

def measure(data,t,size):
    grid=np.linspace(-2.5,1.5,size);ue,re,_,res=eng.safe_reference(SOL,grid,t)
    x,u,rx,r=data
    assert min(x[-1],rx[-1])>=grid[-1] and max(x[0],rx[0])<=grid[0]
    return dict(u=float(max(abs(np.interp(grid,x,u)-ue))),rho=float(max(abs(np.interp(grid,rx,r)-re))),reference_residual=res)

def run(scheme,method,dt):
    sys,state=initialize(scheme);arrays={};metrics={};min_h=min_rho=np.inf
    def save(t):
        data=fields(sys,state,t)
        for name,v in zip(('x','u','rho_x','rho'),data):arrays[f't{t}_{name}']=v.copy()
        metrics[str(t)]={str(size):measure(data,t,size) for size in (16001,32001)}
    save(0.)
    aa,cc,bb=base.butcher(method)
    for j in range(round(.5/dt)):
        t=j*dt
        if sys is not None:state,_,_=eng.original_advance(sys,t,state,dt,method)
        elif scheme=='S4':state=eng.ale_step(state,SOL,t,dt,'fixed',XINIT[0],XINIT[-1],method)
        else:
            ks=[]
            for i in range(len(bb)):
                trial=tuple(v+dt*sum(aa[i,k]*ks[k][part] for k in range(i) if aa[i,k]!=0) for part,v in enumerate(state))
                ks.append(base.paper_ale_rhs(trial,SOL,t+cc[i]*dt))
            state=tuple(v+dt*sum(bb[k]*ks[k][part] for k in range(len(bb)) if bb[k]!=0) for part,v in enumerate(state))
        data=fields(sys,state,(j+1)*dt)
        min_h=min(min_h,float(np.min(np.diff(data[0]))));min_rho=min(min_rho,float(np.min(data[3])))
        for sample in TIMES[1:]:
            if j+1==round(sample/dt):save(sample)
    assert min_h>0 and min_rho>0
    path=OUT/f'{scheme}_{method}_{dt:g}.npz';np.savez_compressed(path,**arrays)
    return dict(scheme=scheme,method=method,dt=dt,metrics=metrics,min_h=min_h,min_rho=min_rho,profile=str(path.resolve()),sha256=base.sha(path))

def main():
    config=dict(p=P,c_phys=C,q=1.25,xi0=0.,eta0=0.,coordinate_shift=-.8,a=A,n=N,X_bounds=[-4,4],initial_physical_bounds=[float(XINIT[0]),float(XINIT[-1])],evaluation_bounds=[-2.5,1.5],methods=base.METHODS,dts=[.003125,.0015625],times=TIMES,source_hashes=eng.source_hashes(),driver_sha256=base.sha(__file__),four_scheme_driver_sha256=base.sha(base.__file__),html_sha256=base.sha(base.ROOT/'numerical_analysis.html'))
    dest=OUT/'results.json';saved=json.loads(dest.read_text()) if dest.exists() else dict(configuration=config,rows={})
    assert json.loads(json.dumps(config))==saved['configuration'] if dest.exists() else True
    for scheme in base.SCHEMES:
        for method in base.METHODS:
            for dt in config['dts']:
                key=f'{scheme}_{method}_{dt:g}'
                if key not in saved['rows']:
                    saved['rows'][key]=run(scheme,method,dt);eng.dump(dest,saved)
                    print(key,'completed',flush=True)
    rows=[]
    for r in saved['rows'].values():
        assert base.sha(r['profile'])==r['sha256']
        with np.load(r['profile']) as z:
            for t in TIMES:
                data=tuple(z[f't{t}_{s}'] for s in ('x','u','rho_x','rho'))
                for size in (16001,32001):assert measure(data,t,size)==r['metrics'][str(t)][str(size)]
                e=r['metrics'][str(t)]['32001']
                rows.append(dict(scheme=r['scheme'],method=r['method'],dt=r['dt'],t=t,u_error=e['u'],rho_error=e['rho'],display=f"{e['u']:.3e} / {e['rho']:.3e}"))
    base.writecsv(OUT/'errors.csv',rows)
    # Direct paper tau identities including its unnormalized coordinate gauge.
    testX=np.linspace(-3,3,101);theta=3.75*testX
    up=.09/np.cosh(theta/2)**2;rp=1/(1+.5625/np.cosh(theta/2)**2)
    xp=testX-(1+np.tanh(theta/2))/(5*(1+np.tanh((theta-np.log(4))/2)))
    uu,xx,rr=SOL.continuous_X(testX,0.)
    formula_error=max(float(max(abs(uu-up))),float(max(abs(rr-rp))),float(max(abs(xx-xp))))
    assert formula_error<1e-8
    # The paper figure itself is an exact lattice profile, not a time-stepping test.
    k=np.arange(-800,801);exact={}
    lattice_defect={}
    for t in TIMES:
        f=SOL.lattice_state(k,A,t)
        data=(f['x'],f['u'],(f['x'][1:]+f['x'][:-1])/2,f['rho'])
        lattice_defect[str(t)]=measure(data,t,32001)
        for name,v in zip(('x','u','rho_x','rho'),data):exact[f't{t}_{name}']=v
    np.savez_compressed(OUT/'paper_exact_lattice.npz',**exact)
    fig,axes=plt.subplots(2,2,figsize=(11,6.5),layout='constrained')
    ue,re,_,_=eng.safe_reference(SOL,GRID,.5)
    for i,(field,target) in enumerate((('u',ue),('rho',re))):
        axes[0,i].plot(GRID,target,'k',lw=2,label='Continuous exact')
        for scheme in base.SCHEMES:
            r=saved['rows'][f'{scheme}_rk4_0.003125']
            with np.load(r['profile']) as z:
                xp=z['t0.5_x' if field=='u' else 't0.5_rho_x'];v=z[f't0.5_{field}']
                interp=np.interp(GRID,xp,v)
                axes[0,i].plot(GRID,interp,lw=1,label=scheme)
                axes[1,i].semilogy(GRID,np.maximum(abs(interp-target),1e-14),label=scheme)
        axes[0,i].set_title(field+' at t=0.5, RK4');axes[1,i].set_title('Absolute error: '+field)
        for ax in axes[:,i]:ax.set_xlabel('physical x');ax.grid(alpha=.2);ax.legend(fontsize=8)
    fig.savefig(OUT/'waveforms.png',dpi=180);fig.savefig(OUT/'waveforms.pdf');plt.close(fig)
    table=[]
    for scheme in base.SCHEMES:
        cells=[next(r['display'] for r in rows if r['scheme']==scheme and r['method']==m and r['dt']==.003125 and r['t']==.5) for m in base.METHODS]
        table.append('| '+scheme+' | '+' | '.join(cells)+' |')
    max_eval=max(abs(r['metrics'][str(t)]['32001'][f]/r['metrics'][str(t)]['16001'][f]-1) for r in saved['rows'].values() for t in TIMES for f in ('u','rho'))
    eng.dump(OUT/'validation.json',dict(formula_error=formula_error,profiles_verified=32,max_eval_relative_change=max_eval,exact_lattice_vs_continuous=lattice_defect,html_unchanged=base.sha(base.ROOT/'numerical_analysis.html')==config['html_sha256']))
    text=f'''# 原文单孤子参数点：四方案结果

采用原文图1/3的p=5、c=1、q=1.25、xi0=eta0=0，原生步长a=.005。N=1600，辅助区间X∈[-4,4]。原文未指定本次时间推进的dt和终止时刻；我们选dt=.003125及其一半，t=.25/.5，四时间算法，共32条轨道全部完成。

原文未归一化tau的坐标为x=X-1/q-omega*sigmoid(theta)，因此代码shift=-.8，t=0波峰x=-.5。没有再将波形平移到0。已与原文(59)–(61)独立公式核对，最大差{formula_error:.3g}。

rho是满足rho_t=(u rho)_x的第二个密度场，远场为1；论文格距满足rho_k*d_k=a。此例连续解u峰值=.09，rho谷值=.64；这些是场值，不是误差。

四方案同上一级HANDOFF.md：S1原可积、S2校准可积、S3普通ALE＋论文网格、S4普通固定格。S1/S2/S3共享连续解析初始节点；S4均匀覆盖相同初始物理端点[{XINIT[0]:.9f},{XINIT[-1]:.9f}]。因此S4物理格距约.005375，不能称为物理dx=.005。初始场来自同一连续解；S1/S2胞元rho=a/d，S3/S4节点rho直接采样，S1/S2与ALE边界闭合差异仍在。

主指标为公共物理区间[-2.5,1.5]、32001点线性重构后的连续总误差。以下t=.5、dt=.003125，每格u/rho：

| 方案 | Euler | Heun | RK4 | RK8 |
|---|---|---|---|---|
{chr(10).join(table)}

errors.csv含t=0/.25/.5及半步结果；results.json含16001/32001点结果、正性与轨道哈希。全部32个轨道读回核对通过，评价加密最大相对变化{max_eval*100:.4f}%。waveforms.png/pdf为RK4、t=.5的双场与绝对误差图。

注意：原文图3展示半离散精确孤子，不是从连续初值做时间推进的误差比较。本次另保存paper_exact_lattice.npz，其直接精确公式对连续解的差值在validation.json中；不将该差值称为时间求解误差。本次四方法表是使用原文参数的数值扩展，并非原文已发表的精度表。
'''
    (OUT/'REPORT.md').write_text(text,encoding='utf-8')
    print('\n'.join(table),flush=True)

if __name__=='__main__':main()
