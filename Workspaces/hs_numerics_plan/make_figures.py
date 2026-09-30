"""Render publication-style diagnostic figures from run_study.py outputs."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from hs_exact import Soliton

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'out'; FIG=OUT/'figures'

def style():
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,
                         'axes.spines.right':False,'figure.dpi':140,
                         'savefig.dpi':180,'axes.grid':True,
                         'grid.alpha':.22})

def main():
    style(); FIG.mkdir(parents=True,exist_ok=True)
    data=json.loads((OUT/'results.json').read_text(encoding='utf-8'))
    snap=np.load(OUT/'snapshots.npz')
    ref=Soliton((5.,))

    # Single wave: propagated points and independent continuous curve.
    fig,axs=plt.subplots(2,2,figsize=(10,6),sharex=True)
    for i,t in enumerate(snap['single_times']):
        if i not in (0,len(snap['single_times'])//2,len(snap['single_times'])-1): continue
        x=snap['single_x'][i]; u=snap['single_u'][i]; rho=snap['single_rho'][i]
        xx=np.linspace(x.min(),x.max(),1000)
        uc,rc,_=ref.continuous_x(xx,t)
        color=plt.cm.viridis(i/(len(snap['single_times'])-1))
        axs[0,0].plot(x,u,color=color,lw=1.3,label=f't={t:g} SD')
        axs[0,0].plot(xx,uc,color=color,lw=.8,ls='--')
        axs[0,1].plot((x[1:]+x[:-1])/2,rho,color=color,lw=1.3,label=f't={t:g} SD')
        axs[0,1].plot(xx,rc,color=color,lw=.8,ls='--')
        axs[1,0].plot(x,u-snap['single_exact_u'][i],color=color,lw=1)
        axs[1,1].plot((x[1:]+x[:-1])/2,np.diff(x),color=color,lw=1)
    axs[0,0].set(ylabel='u',title='Single soliton: solid propagated / dashed continuous')
    axs[0,1].set(ylabel='rho (edge)',title='Density')
    axs[1,0].set(xlabel='physical x',ylabel='u - exact finite-a u',title='Solver error')
    axs[1,1].set(xlabel='physical x',ylabel='edge length d',title='Moving mesh intervals')
    axs[0,0].legend(fontsize=8);fig.tight_layout();fig.savefig(FIG/'fig1_single.png');plt.close(fig)

    fig,axs=plt.subplots(1,2,figsize=(10,3.6))
    for method in ('euler','rk4','trapezoid'):
        rows=sorted([r for r in data['E1_time_methods'] if r['method']==method],key=lambda r:r['dt'])
        axs[0].loglog([r['dt'] for r in rows],
                      [r['metrics']['solver_u']['linf'] for r in rows],'-o',label=method)
    axs[0].set(xlabel='time step',ylabel='max |u - exact SD u|',title='Time-method error')
    axs[0].legend()
    aa=[r['a'] for r in data['E2_E3_continuum']]
    axs[1].loglog(aa,[r['metrics']['model_u_linf'] for r in data['E2_E3_continuum']],'-o',label='u model')
    axs[1].loglog(aa,[r['metrics']['model_rho_cell_linf'] for r in data['E2_E3_continuum']],'-s',label='rho model')
    axs[1].loglog(aa,np.array(aa)*data['E2_E3_continuum'][0]['metrics']['model_u_linf']/aa[0],
                  ':',color='.4',label='O(a) guide')
    axs[1].set(xlabel='lattice a',ylabel='max model error',title='Continuum limit')
    axs[1].legend();fig.tight_layout();fig.savefig(FIG/'fig2_convergence.png');plt.close(fig)

    fig,axs=plt.subplots(2,1,figsize=(9,6),sharex=True)
    for i,t in enumerate(snap['double_times']):
        x=snap['double_x'][i]
        color=plt.cm.plasma(i/(len(snap['double_times'])-1))
        axs[0].plot(x,snap['double_u'][i],color=color,lw=1.3,label=f't={t:g}')
        axs[1].plot((x[1:]+x[:-1])/2,snap['double_rho'][i],color=color,lw=1.3)
    axs[0].set(ylabel='u',title='Two-soliton interaction: actual RK4 trajectories')
    axs[1].set(xlabel='physical x',ylabel='rho on edges')
    axs[0].legend(ncol=5,fontsize=8);fig.tight_layout();fig.savefig(FIG/'fig3_collision.png');plt.close(fig)

    fig,axs=plt.subplots(1,2,figsize=(10,3.8))
    t=float(snap['compare_t']); xx=np.linspace(-4,4,1200)
    ue,_,_=ref.continuous_x(xx,t)
    axs[0].plot(xx,ue,'k-',lw=1.6,label='continuous exact')
    for key,label in (('sd','SD + RK4'),('fd','ordinary mesh + RK4'),('fixed','fixed + CN')):
        axs[0].plot(snap[f'compare_{key}_x'],snap[f'compare_{key}_u'],
                    lw=1,alpha=.85,label=label)
    axs[0].set(xlim=(-2,2),xlabel='physical x',ylabel='u',title=f'Common continuous initial data, t={t:g}')
    axs[0].legend(fontsize=7)
    for row in data['E5_comparison']:
        metric=row['metrics']['physical_u']['linf']
        axs[1].scatter(row['seconds'],metric,s=55,label=row['kind'])
    axs[1].set(xlabel='elapsed seconds',ylabel='max physical u error',yscale='log',title='Measured cost / accuracy')
    axs[1].legend();fig.tight_layout();fig.savefig(FIG/'fig4_methods.png');plt.close(fig)
    print('Figures in',FIG)

if __name__=='__main__': main()
