"""Derive and check local 2HS conserved densities; analytic profiles only."""
import json
from pathlib import Path
import sympy as sy
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE=Path(__file__).resolve().parent
OUT=HERE/'out'/'new_density'
OUT.mkdir(parents=True,exist_ok=True)
x,t,c=sy.symbols('x t c',real=True)
u,rho,m=[sy.Function(z)(x,t) for z in ('u','rho','m')]
dx=lambda f:sy.diff(f,x)
evol={sy.diff(rho,t):dx(u*rho),
      sy.diff(m,t):u*dx(m)+2*dx(u)*m+c*c*rho*dx(rho)}
R=m/(2*rho)
Q=-u*R-c*c*(rho-1)/2
res=sy.simplify((sy.diff(R,t)+dx(Q)).subs(evol))
assert res==0
s,z=sy.symbols('s z',real=True)
r=(1-s*s)/(1-s*s*z*z)
ux=-s**3*z*(1-z*z)/(1-s*s*z*z)
uxx=sy.diff(ux,z)*2*s*(1-z*z)/(1-s*s*z*z)
RR=sy.factor((uxx+2)/(2*r))
positive_add=s*s*(1-z*z)*(1+s*s*z*z)/(1-s*s*z*z)**2
assert sy.factor(RR-1-positive_add)==0

fig,ax=plt.subplots(1,2,figsize=(10,4),constrained_layout=True)
rows=[]
for p in (3,5,12,20):
    s0=1-2/p;beta=p-p/(p-1)
    theta=np.linspace(-25,25,20001); zz=np.tanh(theta/2)
    xx=theta/beta+s0*zz/2
    rr=(1-s0*s0)/(1-s0*s0*zz*zz)
    new=1+s0*s0*(1-zz*zz)*(1+s0*s0*zz*zz)/(1-s0*s0*zz*zz)**2
    ax[0].plot(xx,rr,label=f'p={p}')
    ax[1].plot(xx,new,label=f'p={p}')
    rows.append(dict(p=p,rho_min=1-s0*s0,R_center=1+s0*s0,
                     R_sampled_max=float(max(new))))
ax[0].set(title='Original mass density rho',ylabel='density')
ax[1].set(title='Conserved density (u_xx + 2) / (2 rho)')
for a in ax:
    a.set(xlim=(-3,3),xlabel='physical x, initial peak at zero')
    a.grid(alpha=.2);a.legend(fontsize=8)
fig.savefig(OUT/'density_comparison.png',dpi=180)
plt.close(fig)
(OUT/'identities.json').write_text(json.dumps(dict(
    status='continuous identities and exact-family positivity only; not a discretization or convergence result',
    conservation_residual=str(res),density_expression=str(RR),
    positivity_remainder=str(positive_add),profiles=rows),indent=2)+'\n')
print('PASSED: local conservation identity and exact-family positive-density formula.')
print(json.dumps(rows,indent=2))
