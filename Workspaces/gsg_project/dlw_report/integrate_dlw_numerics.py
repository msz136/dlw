"""Read frozen DLW fields, verify displayed errors and draw report figures."""
from pathlib import Path
import sys,json,hashlib
import numpy as np
from scipy.signal import resample
from scipy.interpolate import CubicSpline
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parents[2]/'Workspaces/dlw_branch_mesh_euler_20260926'
OUT=HERE/'dlw_numerical_update';OUT.mkdir(exist_ok=True)
sys.path.insert(0,str(SOURCE))
from model import BranchProblem,evaluate
from run import CASES

METHODS=[('sd','fixed','D1: SD fixed','#994455'),('fd','fixed','D2: FD fixed','#276ba5'),('sd','minus','D3: SD moving','#b36521'),('fd','minus','D4: FD moving','#228855')]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    docs={phase:json.loads((SOURCE/'out'/f'{phase}.json').read_text()) for phase in ('main','time_half','space_x')}
    checked=0;worst=0.;cache={}
    for phase,d in docs.items():
        for path,h in d['source_hashes'].items():assert sha(path)==h
        for case in CASES:
            for route,branch,_,_ in METHODS:
                row=d['rows'][f'{case}_{route}_{branch}_{phase}']
                if row['status']!='completed':continue
                path=SOURCE/'out'/row['profile'];assert sha(path)==row['profile_sha256']
                spec=row['spec'];p=BranchProblem(CASES[case],**{k:spec[k] for k in ('route','branch','h','nx','L','yhalf')})
                with np.load(path) as a:
                    for t in (.005,.01):
                        e=evaluate(p,a[f't{t}_z'],a[f't{t}_s'],t)
                        for f in ('u','v'):
                            diff=abs(e[f]-row['snapshots'][str(t)]['errors'][f]);worst=max(worst,diff);assert diff<1e-12;checked+=1
                cache[case,route,branch,phase]=row
    def table(phase):
        lines=['| 参数 (a,p,q) | D1：SD 固定 | D2：FD 固定 | D3：SD 负支动格 | D4：FD 负支动格 |','|---|---:|---:|---:|---:|']
        for case,pars in CASES.items():
            vals=[]
            for route,branch,_,_ in METHODS:
                r=cache.get((case,route,branch,phase))
                e=r['snapshots']['0.01']['errors'] if r else None
                vals.append(f'{e["u"]:.3e} / {e["v"]:.3e}' if e else '未完成')
            lines.append(f'| {case} ({pars.a:g},{pars.p:g},{pars.q:g}) | '+' | '.join(vals)+' |')
        return '\n'.join(lines)
    plt.rcParams.update({'font.family':'DejaVu Serif','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fig,axes=plt.subplots(4,3,figsize=(13,11),layout='constrained');heat=plt.figure(figsize=(12,10),layout='constrained');ha=heat.subplots(4,2)
    samples={};mesh=[]
    for j,case in enumerate(('P6','P2','P10')):
        for k,(route,branch,label,color) in enumerate(METHODS):
            r=cache[case,route,branch,'main'];sp=r['spec'];p=BranchProblem(CASES[case],**{key:sp[key] for key in ('route','branch','h','nx','L','yhalf')})
            with np.load(SOURCE/'out'/r['profile']) as a:
                t=.01;p.X.set_s(a['t0.01_s']);uv=p.m.fields(a['t0.01_z'],t)
                my=abs(p.m.y)<1.5;nup=p.X.n*16
                xi=-20+np.arange(nup)*40/nup;xup=xi+resample(a['t0.01_s'],nup)
                xx=-20+np.arange(p.X.n*4)*40/(p.X.n*4);xx=xx[(xx>=-10)&(xx<10)]
                ref=p.m.G.uv(p.m.js[my],xx,t);y=p.m.y[my];iy=int(np.argmin(abs(y)))
                for fidx,field in enumerate(('u','v')):
                    values=CubicSpline(xup,resample(uv[fidx][my],nup,axis=-1),axis=-1)(xx)
                    err=abs(values-ref[fidx]);assert abs(err.max()-r['snapshots']['0.01']['errors'][field])<1e-12
                    ax=axes[fidx,j]
                    if k==0:ax.plot(xx,ref[fidx][iy],color='black',lw=2,label='Exact')
                    ax.plot(xx,values[iy],color=color,lw=1,ls=['--',':','-.','-'][k],label=label)
                    ax.set(title=f'{case}, y={y[iy]:g}',ylabel=field,xlabel='physical x',xlim=(-4,4))
                    ea=axes[fidx+2,j];ea.semilogy(xx,np.maximum(err.max(axis=0),1e-16),color=color,label=label,lw=1)
                    ea.set(xlim=(-10,10),ylim=(1e-12,None),xlabel='physical x',ylabel=f'max over y: |{field} error|')
                    samples[f'{case}_{route}_{branch}_{field}']=values
                    if case=='P6':
                        im=ha[k,fidx].pcolormesh(xx,y,np.log10(np.maximum(err,1e-12)),vmin=-10,vmax=-3,cmap='viridis',shading='auto')
                        ha[k,fidx].set(xlim=(-4,4),xlabel='physical x',ylabel='y',title=f'{label}: {field} error')
        for ax in axes[:,j]:ax.grid(alpha=.15)
    handles,labels=axes[0,0].get_legend_handles_labels();fig.legend(handles,labels,loc='outside lower center',ncol=5)
    fig.suptitle('DLW | Euler | Nx=512, h=1/8, dt=1.25e-5, T=0.01')
    heat.suptitle('P6 | pointwise error in (x,y) | T=0.01');heat.colorbar(im,ax=ha,label='log10 absolute error; values below 1e-10 share lowest color',shrink=.8)
    for name,f in [('waveforms_errors',fig),('p6_error_maps',heat)]:
        for ext in ('png','pdf'):f.savefig(OUT/f'{name}.{ext}',dpi=170)
        plt.close(f)
    fig,axes=plt.subplots(2,2,figsize=(11,7),layout='constrained')
    for j,phase in enumerate(('main','space_x')):
        for i,field in enumerate(('u','v')):
            ax=axes[i,j]
            for route,color,label in [('sd','#b36521','D3/D1: SD moving/fixed'),('fd','#276ba5','D4/D2: FD moving/fixed')]:
                ratios=[]
                for case in CASES:
                    a=cache.get((case,route,'minus',phase));b=cache[case,route,'fixed',phase]
                    ratios.append(a['snapshots']['0.01']['errors'][field]/b['snapshots']['0.01']['errors'][field] if a else np.nan)
                ax.semilogy(list(CASES),ratios,'o-',color=color,label=label)
            ax.axhline(1,color='black',lw=1);ax.set(title=f'Nx={512 if phase=="main" else 1024}',ylabel=f'{field} error ratio');ax.grid(alpha=.2);ax.legend(fontsize=8)
            if phase=='space_x':ax.text(.98,.95,'P10 moving: unfinished',transform=ax.transAxes,ha='right',va='top',fontsize=9)
    for ext in ('png','pdf'):fig.savefig(OUT/f'mesh_refinement.{ext}',dpi=170)
    plt.close(fig)
    result=dict(main_table=table('main'),fine_table=table('space_x'),half_table=table('time_half'),checked_metrics=checked,max_readback_difference=worst,source_hashes={k:sha(SOURCE/'out'/f'{k}.json') for k in docs},figures=3)
    (OUT/'integration.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    np.savez_compressed(OUT/'plotted_fields.npz',x=xx,y=y,**samples)
    print(f'DLW checked {checked} saved metrics; 3 PNG/PDF figures generated; max difference {worst}.')
if __name__=='__main__':main()
