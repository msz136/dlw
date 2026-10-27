"""Three conservation-coordinate meshes: reproducible nodal comparison."""
import json, shutil
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from natural_density_search import ROOT, ale, reference, monitor_flux

OUT=ROOT/'samm_three_20261027'; OUT.mkdir(exist_ok=True)
kinds=['fixed','rho','rm','hierarchy2']
names=['Fixed FD',r'$R_\rho$',r'$R_m$',r'$R_2$']
colors=['#343434','#3976ac','#d58232','#438b68']
styles=['-', '--','-.',':']

def run(p,kind,dt):
 sol=ale.Soliton(p); n=2000
 dense=np.linspace(-4,4,100001)
 u,r,m,_=reference(sol,dense,0); X=sol.continuous_x(dense,0)[2]
 wt,o,b=sol._weights(X,0); o=o-np.sum(wt*o,axis=0);b=b-np.sum(wt*b,axis=0)
 w=np.sum(wt*o*o*b,axis=0)*r;rx=np.sum(wt*o*b*b,axis=0)*r**3
 R,_=monitor_flux(kind,m,r,u,w,rx)
 mass=np.r_[0,np.cumsum((R[1:]+R[:-1])*np.diff(dense)/2)]
 x=np.interp(np.linspace(0,mass[-1],n),mass,dense) if kind!='fixed' else np.linspace(-4,4,n)
 u,r,_,_=reference(sol,x,0);z=(x,ale.second_derivative(u,x)+2,r[1:-1])
 lows=[float(min(np.diff(x))),float(min(r)),float(min(R))]
 for step in range(round(.25/dt)):
  z=ale.rk4(z,sol,step*dt,dt,kind,-4,4)
  m,r,u,_=ale.unpack(z,sol,(step+1)*dt,-4,4)
  R,_=monitor_flux(kind,m,r,u,np.r_[0,ale.first_derivative(u,z[0]),0],np.r_[0,ale.first_derivative(r,z[0]),0])
  # Monitor extrema are measured at interior nodes; endpoint derivatives are prescribed by the boundary closure.
  lows=np.minimum(lows,[min(np.diff(z[0])),min(r),min(R[1:-1])]).tolist()
 x=z[0]; ue,re,_,_=reference(sol,x,.25);mask=abs(x)<=2.5
 return dict(x=x,u=u,rho=r,eu=abs(u-ue),er=abs(r-re)),dict(p=list(p),kind=kind,nodes=n,dt=dt,u=float(max(abs(u[mask]-ue[mask]))),rho=float(max(abs(r[mask]-re[mask]))),min_h=lows[0],min_rho=lows[1],min_R=lows[2])

if __name__=='__main__':
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.grid':True,'grid.alpha':.16})
 rows=[]; saved={}
 for ci,p in enumerate([(5.,),(1.1,1.25)]):
  fig,axes=plt.subplots(3,1,figsize=(7.1,7.1),layout='constrained',sharex=True)
  for ki,kind in enumerate(kinds):
   data,row=run(p,kind,.0005); half,_=run(p,kind,.00025)
   row['halving_change']=max(float(max(abs(data[q]-half[q]))) for q in ['x','u','rho'])
   rows.append(row); print(json.dumps(row),flush=True)
   for q,v in data.items():saved[f'{ci}_{kind}_{q}']=v
   x=data['x']; h=np.diff(x); mid=(x[:-1]+x[1:])/2
   axes[0].plot(mid[1:-1],h[1:-1],color=colors[ki],ls=styles[ki],lw=1.5,label=names[ki])
   for ax,key in zip(axes[1:],['eu','er']):
    mask=(abs(x)<=2.5)&(data[key]>0)
    ax.semilogy(x[mask],data[key][mask],color=colors[ki],ls=styles[ki],lw=1.4)
  axes[0].set_ylabel('Cell width');axes[0].ticklabel_format(axis='y',style='sci',scilimits=(0,0))
  axes[1].set_ylabel(r'$|u-u_*|$'); axes[2].set_ylabel(r'$|\rho-\rho_*|$');axes[2].set_xlabel('$x$')
  axes[0].legend(ncol=4,loc='upper center',fontsize=9)
  axes[0].set_xlim(-2.5,2.5)
  for ext in ['png','pdf']:fig.savefig(OUT/f'samm_case_{ci}.{ext}',dpi=210)
  plt.close(fig)
  (OUT/'results.json').write_text(json.dumps(rows,indent=2))
 np.savez_compressed(OUT/'trajectories.npz',**saved)
