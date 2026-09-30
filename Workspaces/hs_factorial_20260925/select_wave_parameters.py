"""Analytic 2HS waveform selection only; no numerical time evolution."""
import json
import sys
from pathlib import Path
import numpy as np
from scipy.optimize import minimize_scalar
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'hs_numerics_plan'))
from hs_exact import Soliton
OUT=HERE/'out'/'wave_selection'
OUT.mkdir(parents=True,exist_ok=True)

def fields(p,theta):
    q=p/(p-1)
    beta=p-q
    omega=1/p-1/q
    z=np.tanh(np.asarray(theta)/2)
    sech2=1-z*z
    J=1-omega*beta*sech2/4
    return (np.asarray(theta)/beta-omega*z/2,
            omega**2*sech2/4,1/J,J)

def row(p):
    q=p/(p-1); r=1-2/p; beta=p-q
    A=r*r/4; m=1-r*r
    th=2*np.arccosh(np.sqrt(2))
    fwhm=2*th/beta+r/np.sqrt(2)
    def slope(z):
        return A*(1-z*z)*z/(1/beta+r*(1-z*z)/4)
    opt=minimize_scalar(lambda z:-slope(z),bounds=(0,1),method='bounded',
                        options={'xatol':1e-14})
    d=dict(p=p,q=q,r=r,u_peak=A,rho_min=m,
           physical_speed=m/4,u_fwhm=fwhm,
           peak_slope=float(-opt.fun),
           wave_time=fwhm/(m/4),initial_shift=-r/2,
           initial_phase=0,
           exact_positive_multiplier_requires_a_less_than=1/p,
           resolution={})
    for a in (.04,.02,.01):
        d['resolution'][str(a)]=dict(
            finite_a_exact_positive_margin=1-a*p,
            positive_multiplier_admissible=bool(a*p<1),
            continuum_peak_spacing_estimate=a/m,
            mass_intervals_per_u_fwhm=2*th/(beta*a),
            fixed_intervals_per_u_fwhm=fwhm/a)
    return d

selected=[row(p) for p in (3.,5.,12.,20.)]
optional=row(40.)
scan=[row(float(p)) for p in 2+np.geomspace(.05,78,241)]
checks=[]
theta=np.linspace(-12,12,4001)
for d in selected+[optional]:
    p=d['p']; q=d['q']
    x,u,rho,J=fields(p,theta)
    ref=Soliton((p,),shift=d['initial_shift'])
    un,xn,rn=ref.continuous_X(theta/(p-q),0)
    direct=max(np.max(abs(x-xn)),np.max(abs(u-un)),np.max(abs(rho-rn)))
    assert direct<1e-12
    swapped=Soliton((q,),shift=-d['initial_shift'])
    us,xs,rs=swapped.continuous_X(theta/(p-q),0)
    symmetry=max(np.max(abs(x-xs)),np.max(abs(u-us)),np.max(abs(rho-rs)))
    assert symmetry<1e-11
    assert np.min(J)>=1-1e-12
    checks.append(dict(p=p,exact_implementation_difference=float(direct),
                       swapped_p_q_centered_difference=float(symmetry)))

fig,axes=plt.subplots(2,2,figsize=(11,7.5),constrained_layout=True)
for d in selected:
    x,u,rho,J=fields(d['p'],np.linspace(-24,24,12001))
    label=f"p={d['p']:g}, q={d['q']:.4g}"
    axes[0,0].plot(x,u,label=label)
    axes[0,1].plot(x,rho,label=label)
    axes[1,0].plot(x,J,label=label)
    axes[1,1].plot(x/d['u_fwhm'],u/d['u_peak'],label=label)
axes[0,0].set(xlim=(-3,3),title='Physical field u: peaks aligned at x=0',xlabel='x',ylabel='u')
axes[0,1].set(xlim=(-3,3),title='Density: rho > 0 in all selected cases',xlabel='x',ylabel='rho')
axes[1,0].set(xlim=(-3,3),title='Natural mass mesh stretching: dx/dX = 1/rho',xlabel='x',ylabel='dx/dX')
axes[1,1].set(xlim=(-1.5,1.5),title='Amplitude / FWHM normalized shapes',xlabel='x / FWHM',ylabel='u / peak')
for ax in axes.flat:
    ax.grid(alpha=.2)
axes[0,0].legend(fontsize=8)
fig.savefig(OUT/'smooth_waveforms.png',dpi=180)
plt.close(fig)

# Separate singular branch, which is not admissible for the current positive-rho solver.
p=.5; q=-1.; beta=p-q; omega=1/p-1/q
turn=2*np.arccosh(np.sqrt(omega*beta/4))
th=np.linspace(-8,8,4001)
x,u,_,J=fields(p,th)
fig,ax=plt.subplots(figsize=(6,4),constrained_layout=True)
ax.plot(x,u,label='p=0.5, q=-1: parameter curve')
for sign in (-1,1):
    xt,ut,_,_=fields(p,np.array([sign*turn+1e-12]))
    ax.scatter(xt,ut,color='crimson',zorder=3)
ax.set(xlim=(-2.5,2.5),xlabel='x',ylabel='u',title='Separate loop branch: rho diverges at turning points')
ax.grid(alpha=.2);ax.legend(fontsize=8)
fig.savefig(OUT/'singular_loop_diagnostic.png',dpi=180)
plt.close(fig)

data=dict(scope='analytic profiles and geometry; no PDE trajectories',c=1,
          selected=selected,optional_pressure=optional,scan=scan,checks=checks,
          loop=dict(p=.5,q=-1,theta_turns=[-float(turn),float(turn)],
                    accepted_for_positive_density_solver=False),
          notes=['p and q exchanged give the same centered single-soliton profile',
                 'rho_min tending to zero is distinct from loop singularity where x_X=0 and rho diverges',
                 'natural-mesh interval counts describe continuous mass coordinate, not an evolved numerical mesh'])
(OUT/'parameters.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(selected=selected,checks=checks,loop=data['loop']),indent=2))
