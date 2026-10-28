"""Replace the third main comparison by the energy-type conserved coordinate."""
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from samm_three import ROOT,run,colors,styles

OUT=ROOT/'samm_energy_20261028';OUT.mkdir(exist_ok=True)
if __name__=='__main__':
 oldrows=json.loads((ROOT/'samm_three_20261027/results.json').read_text())
 old=np.load(ROOT/'samm_three_20261027/trajectories.npz')
 rows=[];saved={}
 kinds=['fixed','rho','rm','energy'];names=['Fixed FD',r'$R_\rho$',r'$R_m$',r'$R_E$']
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.grid':True,'grid.alpha':.16})
 for ci,p in enumerate([(5.,),(1.1,1.25)]):
  fig,axes=plt.subplots(3,1,figsize=(7.1,7.1),layout='constrained',sharex=True)
  for ki,kind in enumerate(kinds):
   if kind=='energy':
    data,row=run(p,kind,.0005);half,_=run(p,kind,.00025)
    row['halving_change']=max(float(max(abs(data[q]-half[q]))) for q in ['x','u','rho'])
   else:
    row=next(z for z in oldrows if z['p']==list(p) and z['kind']==kind)
    data={q:old[f'{ci}_{kind}_{q}'] for q in ['x','u','rho','eu','er']}
   rows.append(row);print(json.dumps(row),flush=True)
   for q,v in data.items():saved[f'{ci}_{kind}_{q}']=v
   x=data['x'];h=np.diff(x);mid=(x[:-1]+x[1:])/2
   axes[0].plot(mid[1:-1],h[1:-1],color=colors[ki],ls=styles[ki],lw=1.5,label=names[ki])
   for ax,key in zip(axes[1:],['eu','er']):
    mask=(abs(x)<=2.5)&(data[key]>0);ax.semilogy(x[mask],data[key][mask],color=colors[ki],ls=styles[ki],lw=1.4)
  axes[0].set_ylabel('Cell width');axes[0].ticklabel_format(axis='y',style='sci',scilimits=(0,0))
  axes[1].set_ylabel(r'$|u-u_*|$');axes[2].set_ylabel(r'$|\rho-\rho_*|$');axes[2].set_xlabel('$x$')
  axes[0].legend(ncol=4,loc='upper center',fontsize=9);axes[0].set_xlim(-2.5,2.5)
  for ext in ['png','pdf']:fig.savefig(OUT/f'samm_energy_{ci}.{ext}',dpi=210)
  plt.close(fig)
  (OUT/'results.json').write_text(json.dumps(rows,indent=2))
 np.savez_compressed(OUT/'trajectories.npz',**saved)
