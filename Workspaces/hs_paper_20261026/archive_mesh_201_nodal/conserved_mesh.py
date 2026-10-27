"""Matched fixed/Rm ALE experiments; analytic tau derivatives for both cases.
Plot layout and colors follow the approved fd_mesh figures; no data smoothing.
"""
import sys,json,importlib.util
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('ale',ROOT.parent/'hs_conserved_mesh_20260925/run_mesh_comparison.py')
ale=importlib.util.module_from_spec(spec);spec.loader.exec_module(ale)
cache={}
def reference(sol,x,t):
 x=np.asarray(x);key=(sol.p,round(t,12))
 boundary=len(x)==2 and np.array_equal(x,[-4,4])
 if boundary and key in cache:return cache[key]
 u,r,X=sol.continuous_x(x,t)
 w,o,b=sol._weights(X,t);o=o-np.sum(w*o,axis=0);b=b-np.sum(w*b,axis=0)
 cov=np.sum(w*o*b,axis=0)
 uX=np.sum(w*o*o*b,axis=0)
 uXX=np.sum(w*o*o*b*b,axis=0)-u*np.sum(w*b*b,axis=0)-2*cov**2
 xXX=-np.sum(w*o*b*b,axis=0)
 m=2+uXX*r*r-uX*xXX*r**3
 result=(u,r,m,m/(2*r))
 if boundary:cache[key]=result
 return result
ale.reference=reference
def run(sol,mode,dt,n=200):
 x=ale.initial_grid(sol,mode,n,4)
 u,r,_,_=reference(sol,x,0)
 z=(x,ale.second_derivative(u,x)+2,r[1:-1])
 low=[float(np.min(np.diff(x))),float(min(r)),float(min(z[1]/(2*z[2])))]
 for step in range(round(.25/dt)):
  z=ale.rk4(z,sol,step*dt,dt,mode,-4,4)
  low=np.minimum(low,[min(np.diff(z[0])),min(z[2]),min(z[1]/(2*z[2]))]).tolist()
 m,r,u,R=ale.unpack(z,sol,.25,-4,4)
 return z[0],u,r,low
if __name__=='__main__':
 rows=[];saved={}
 plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.grid':True,'grid.alpha':.18})
 for ci,p in enumerate([(5.,),(1.1,1.25)]):
  sol=ale.Soliton(p)
  # Independent centered-difference check of the analytic u_xx used in boundaries/monitor.
  h=1e-4;xs=np.linspace(-3,3,61)
  exact_m=reference(sol,xs,.123)[2]
  fd_m=2+(reference(sol,xs+h,.123)[0]-2*reference(sol,xs,.123)[0]+reference(sol,xs-h,.123)[0])/h**2
  assert max(abs(exact_m-fd_m))<2e-6
  fig,ax=plt.subplots(1,3,figsize=(11,3.2),layout='constrained')
  for mi,mode in enumerate(['fixed','rm']):
   x,u,r,low=run(sol,mode,.0005);xh,uh,rh,_=run(sol,mode,.00025)
   ue,re,_,_=reference(sol,x,.25)
   mask=(x>=-2.5)&(x<=2.5)
   eu=abs(u-ue);er=abs(r-re)
   change=max(max(abs(x-xh)),max(abs(u-uh)),max(abs(r-rh)))
   name=['Fixed FD','Conserved-density moving FD'][mi]
   row=dict(case=['One soliton','Two solitons'][ci],method=name,u=float(max(eu[mask])),rho=float(max(er[mask])),nodes=len(x),metric="native nodes in [-2.5,2.5]",dt_halving_change=float(change),min_h=low[0],min_rho=low[1],min_Rm=low[2],analytic_derivative_check=float(max(abs(exact_m-fd_m))))
   rows.append(row);print(row,flush=True)
   for q,a in [('x',x),('u',u),('rho',r),('eu',eu),('er',er)]:saved[f'{ci}_{mi}_{q}']=a
   color=['#2878b5','#e78123'][mi];ls=['-','--'][mi]
   ax[0].plot((x[1:]+x[:-1])/2,np.diff(x),color=color,ls=ls,label=name)
   for j,e in enumerate([eu,er],1):ax[j].plot(x[mask],e[mask],color=color,ls=ls,lw=1.5)
  for j in range(3):
   ax[j].set(xlabel='$x$',ylabel=['Cell width',r'$|u_h-u_*|$',r'$|\rho_h-\rho_*|$'][j])
   if j:ax[j].ticklabel_format(axis='y',style='sci',scilimits=(0,0))
  fig.legend(loc='outside upper center',ncol=2,frameon=False,fontsize=9)
  for ext in ['png','pdf']:fig.savefig(ROOT/f'figures/conserved_mesh_{ci}.{ext}',dpi=300)
  plt.close(fig)
 (ROOT/'data/conserved_mesh.json').write_text(json.dumps(rows,indent=2))
 np.savez_compressed(ROOT/'data/conserved_mesh.npz',**saved)
