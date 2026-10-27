"""Final figure styling from saved numerical arrays; no new evolution."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from run_paper_support import *
d=np.load(OUT/'curves.npz');times=d['times']
for ci,p in enumerate([(5.,),(1.1,1.25)]):
 ref=Soliton(p);fig,ax=plt.subplots(2,2,figsize=(9,5.6),layout='constrained')
 left=min(d[f'spatial_{ci}_{mi}_u_x'][0] for mi in range(3));right=max(d[f'spatial_{ci}_{mi}_u_x'][-1] for mi in range(3));xx=np.linspace(left,right,1201)
 for j,q in enumerate(['u','rho']):
  ax[0,j].plot(xx,ref.continuous_x(xx,.25)[j],'k-',label='Continuous exact',lw=1.2)
  for mi in range(3):
   xe=d[f'spatial_{ci}_{mi}_{q}_x'];val=d[f'spatial_{ci}_{mi}_{q}'];nodes=d[f'spatial_{ci}_{mi}_u_x']
   ex=ref.continuous_density_cell_mean(nodes[:-1],nodes[1:],.25) if q=='rho' and mi<2 else ref.continuous_x(xe,.25)[j]
   ax[0,j].plot(xe[::12],val[::12],linestyle='none',marker=['o','s','^'][mi],ms=3,mfc='none',color=colors[mi],label=['Integrable SD','Moving FD','Fixed FD'][mi])
   ax[1,j].semilogy(xe,abs(val-ex),color=colors[mi],ls=['-','--','-.'][mi])
  ax[0,j].set(xlabel='$x$',ylabel='$u$' if j==0 else r'$\rho$',title=f'({chr(97+j)}) Field at $T=0.25$')
  ax[1,j].set(xlabel='$x$',ylabel='Absolute error',title=f'({chr(99+j)}) Error distribution')
 ax[0,0].legend(fontsize=8);save(fig,f'spatial_{ci}')
 fig,ax=plt.subplots(1,2,figsize=(9,3.1),layout='constrained')
 for mi in range(3):
  vals=d[f'response_{ci}_{mi}']
  for j in range(2):ax[j].plot(times,vals[:,j],color=colors[mi],ls=['-','--','-.'][mi],label=['Integrable SD','Moving FD','Fixed FD'][mi]);ax[j].set(xlabel='$t$',ylabel='$R_u$' if j==0 else r'$R_\rho$')
 ax[0].legend();save(fig,f'response_{ci}')
 fig,ax=plt.subplots(1,2,figsize=(9,3.3),layout='constrained')
 for mi,method in enumerate(['euler','rk4','trapezoid']):
  vals=d[f'time_{ci}_{method}']
  for j in range(2):ax[j].semilogy(times[1:],np.maximum(vals[1:,j],1e-16),color=[colors[1],colors[0],colors[2]][mi],label=['Euler','RK4','Crank–Nicolson'][mi]);ax[j].set(xlabel='$t$',ylabel='$E_u$' if j==0 else r'$E_\rho$')
 handles,labels=ax[0].get_legend_handles_labels();fig.legend(handles,labels,loc='outside upper center',ncol=3,frameon=False)
 save(fig,f'time_{ci}')
print('Final styles saved')
