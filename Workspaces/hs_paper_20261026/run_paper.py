"""Reproducible numerical data and figures for the 2HS manuscript.
Uses the existing, attributed 2HS soliton evaluator and spatial solvers.
"""
from pathlib import Path
import sys,json,hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.integrate import cumulative_trapezoid
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/'hs_numerics_plan'
sys.path.insert(0,str(BASE))
from hs_exact import Soliton
from hs_solver import MovingSystem,solve
from hs_fixed import FixedSystem
OUT=ROOT/'data'; FIG=ROOT/'figures'
OUT.mkdir(exist_ok=True);FIG.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.grid':True,'grid.alpha':.18,'lines.linewidth':1.6,'savefig.dpi':300})
colors=['#2878B5','#E47C25','#27946B']; names=['Integrable SD','Moving FD','Fixed FD']
refs={'One soliton':Soliton((5.,)),'Two solitons':Soliton((1.1,1.25))}
T=.25; results={'parameters':{'T':T,'c':1,'label_domain':[-4,4],'spatial_a':[.04,.02,.01],'spatial_dt':.0005},'model':[],'spatial':[],'time':[],'mesh':[],'response':[],'checks':{}}
arrays={}
def save(fig,name):
 fig.savefig(FIG/(name+'.png'),bbox_inches='tight');fig.savefig(FIG/(name+'.pdf'),bbox_inches='tight');plt.close(fig)
def setup(ref,a,kind='sd',lattice=False):
 k=np.arange(-round(4/a),round(4/a)+1);X=k*a
 b=(lambda t:float(ref.lattice(k[:1],a,t)[0][0])) if lattice else (lambda t:float(ref.continuous_X(X[:1],t)[0][0]))
 s=MovingSystem(a,1,len(k)-1,b,kind)
 if lattice:z=s.exact_initial(ref,k[0],0)
 else:
  u,x,r=ref.continuous_X(X,0);z=s.pack(np.diff(u),np.diff(x),x[0])
 return s,z,k
def errors(ref,s,t,z,lattice=False,k=None):
 f=s.fields(t,z)
 if lattice:
  e=ref.lattice_state(k,s.a,t);return np.array([max(abs(f[q]-e[q])) for q in ('u','rho')])
 ue,re,_=ref.continuous_x(f['x'],t)
 if isinstance(s,MovingSystem):re=ref.continuous_density_cell_mean(f['x'][:-1],f['x'][1:],t)
 return np.array([max(abs(f['u']-ue)),max(abs(f['rho']-re))])
def integrate(s,z,dt,method='rk4',outputs=None):
 r=solve(s,z,0,T,dt,method,outputs=outputs,tol=2e-13)
 assert r.status=='completed' and r.rejected==0
 return r
for ci,(case,ref) in enumerate(refs.items()):
 print('case',case,flush=True)
 # Exact continuous profiles and space-time maps.
 X=np.linspace(-4,4,1001);u,x,rho=ref.continuous_X(X,0)
 xx=np.linspace(-3.5,3.5,501);tt=np.linspace(0,T,81)
 U=[];R=[]
 for t in tt:
  v,r,_=ref.continuous_x(xx,t);U.append(v);R.append(r)
 fig,ax=plt.subplots(2,2,figsize=(9,5.6),layout='constrained')
 for j,(field,values,heat) in enumerate([('$u$',u,U),(r'$\rho$',rho,R)]):
  ax[0,j].plot(x,values,color=colors[0]);ax[0,j].set(xlabel='$x$',ylabel=field,title=f'({chr(97+j)}) Initial field')
  im=ax[1,j].pcolormesh(xx,tt,heat,shading='auto',cmap='viridis');ax[1,j].grid(False);fig.colorbar(im,ax=ax[1,j]);ax[1,j].set(xlabel='$x$',ylabel='$t$',title=f'({chr(99+j)}) Exact evolution')
 save(fig,f'profiles_{ci}')
 # Finite-lattice exact solutions vs continuous fields at physical sites.
 for a in [.04,.02,.01]:
  s,z,k=setup(ref,a,lattice=True);e=ref.lattice_state(k,a,T);ze=s.pack(e['v'],e['d'],e['x'][0])
  er=errors(ref,s,T,ze)
  results['model'].append({'case':case,'a':a,'u':er[0],'rho':er[1]})
  # independent analytic-time-derivative check via central time difference
  eps=1e-5; ep=ref.lattice_state(k,a,eps);em=ref.lattice_state(k,a,-eps)
  derivative=(s.pack(ep['v'],ep['d'],ep['x'][0])-s.pack(em['v'],em['d'],em['x'][0]))/(2*eps)
  results['checks'][f'rhs_{ci}_{a}']=float(max(abs(derivative-s.rhs(0,z))))
 # Spatial methods from continuous initial fields.
 snapshots=[]
 for a in [.04,.02,.01]:
  for mi,kind in enumerate(['sd','fd','fixed']):
   if kind=='fixed':s=FixedSystem(np.linspace(-4,4,round(8/a)+1),1,ref);z=s.initial(0)
   else:s,z,k=setup(ref,a,kind)
   r=integrate(s,z,.0005);er=errors(ref,s,T,r.states[-1]);f=s.fields(T,r.states[-1])
   results['spatial'].append({'case':case,'method':names[mi],'spacing':a,'u':er[0],'rho':er[1],'min_rho':float(min(f['rho']))})
   if a==.02:
    rh=integrate(s,z,.00025);results['checks'][f'spatial_dt_half_{ci}_{mi}']=float(max(abs(r.states[-1]-rh.states[-1])))
    snapshots.append((mi,f))
 fig,ax=plt.subplots(2,2,figsize=(9,5.6),layout='constrained')
 for j,q in enumerate(['u','rho']):
  ex=ref.continuous_x(xx,T)[j];ax[0,j].plot(xx,ex,'k-',label='Continuous exact',lw=1.2)
  for mi,f in snapshots:
   xe=f['x'] if len(f[q])==len(f['x']) else (f['x'][1:]+f['x'][:-1])/2
   if q=='rho' and mi<2:exs=ref.continuous_density_cell_mean(f['x'][:-1],f['x'][1:],T)
   else:exs=ref.continuous_x(xe,T)[j]
   ax[0,j].plot(xe[::12],f[q][::12],linestyle='none',marker=['o','s','^'][mi],ms=3,mfc='none',color=colors[mi],label=names[mi])
   ax[1,j].plot(xe,abs(f[q]-exs),color=colors[mi],ls=['-','--',':'][mi]);ax[1,j].set_yscale('log')
   arrays[f'spatial_{ci}_{mi}_{q}']=f[q];arrays[f'spatial_{ci}_{mi}_{q}_x']=xe
  ax[0,j].set(xlabel='$x$',ylabel='$u$' if j==0 else r'$\rho$',title=f'({chr(97+j)}) Field at $T=0.25$')
  ax[1,j].set(xlabel='$x$',ylabel='Absolute error',title=f'({chr(99+j)}) Error distribution')
 ax[0,0].legend(fontsize=8);save(fig,f'spatial_{ci}')
 # Time methods on one and the same exact finite lattice.
 s,z,k=setup(ref,.02,lattice=True)
 for method in ['euler','rk4','trapezoid']:
  for dt in [.025,.0125,.00625]:
   rr=integrate(s,z,dt,method);er=errors(ref,s,T,rr.states[-1],True,k)
   results['time'].append({'case':case,'method':method,'dt':dt,'u':er[0],'rho':er[1],'residual':rr.max_residual})
 times=np.linspace(0,T,101)
 fig,ax=plt.subplots(1,2,figsize=(9,3.1),layout='constrained')
 for mi,method in enumerate(['euler','rk4','trapezoid']):
  rr=integrate(s,z,.0025,method,times)
  ee=np.array([errors(ref,s,t,zz,True,k) for t,zz in zip(rr.t,rr.states)])
  arrays[f'time_{ci}_{method}']=ee
  for j in range(2):ax[j].semilogy(times[1:],np.maximum(ee[1:,j],1e-16),color=colors[mi],label=['Euler','RK4','Crank–Nicolson'][mi]);ax[j].set(xlabel='$t$',ylabel='$E_u$' if j==0 else r'$E_\rho$')
 ax[0].legend();save(fig,f'time_{ci}')
 # Perturbations in nodal u, at unchanged initial positions and density.
 fig,ax=plt.subplots(1,2,figsize=(9,3.1),layout='constrained')
 for mi,kind in enumerate(['sd','fd','fixed']):
  if kind=='fixed':s=FixedSystem(np.linspace(-4,4,401),1,ref);z=s.initial(0)
  else:s,z,k=setup(ref,.02,kind)
  f=s.fields(0,z);xn=f['x'];eta=(xn-xn[0])/(xn[-1]-xn[0]);phi=np.sin(np.pi*eta)**2*np.cos(2*np.pi*eta);phi/=max(abs(phi))
  def perturb(eps):
   zp=z.copy()
   if kind=='fixed':zp[:s.n]+=eps*np.diff(phi,2)/s.dx**2
   else:zp[:s.edges]+=eps*np.diff(phi)
   return zp
  clean=integrate(s,z,.0005,outputs=times)
  histories=[]
  for eps,dt in [(1e-6,.0005),(5e-7,.0005),(1e-6,.00025)]:
   pp=integrate(s,perturb(eps),dt,outputs=times)
   cc=clean if dt==.0005 else integrate(s,z,dt,outputs=times)
   response=np.array([[max(abs(s.fields(t,p)[q]-s.fields(t,b)[q]))/eps for q in ['u','rho']] for t,p,b in zip(times,pp.states,cc.states)])
   histories.append(response)
  response=histories[0];arrays[f'response_{ci}_{mi}']=response
  results['response'].append({'case':case,'method':names[mi],'u':float(response[-1,0]),'rho':float(response[-1,1]),'epsilon_halving_change':float(max(abs(histories[1]-response).flat)),'dt_halving_change':float(max(abs(histories[2]-response).flat))})
  for j in range(2):ax[j].plot(times,response[:,j],color=colors[mi],ls=['-','--',':'][mi],label=names[mi]);ax[j].set(xlabel='$t$',ylabel='$R_u$' if j==0 else r'$R_\rho$')
 ax[0].legend();save(fig,f'response_{ci}')
 print('completed',case,flush=True)
# Equal-node spatial representation, at a fixed time.
ref=refs['One soliton'];X=np.linspace(-4,4,401);_,natural,_=ref.continuous_X(X,T)
dense=np.linspace(natural[0],natural[-1],16001);ue,re,_=ref.continuous_x(dense,T)
cu=abs(np.gradient(np.gradient(ue,dense),dense));cr=abs(np.gradient(np.gradient(re,dense),dense))
monitor=1+5*(cu/max(cu)+cr/max(cr));measure=np.r_[0,cumulative_trapezoid(monitor,dense)]
grids=[natural,np.linspace(dense[0],dense[-1],401),np.interp(np.linspace(0,measure[-1],401),measure,dense)]
fig,ax=plt.subplots(1,3,figsize=(11,3.1),layout='constrained')
for mi,(name,grid) in enumerate(zip(['Natural mass mesh','Uniform physical mesh','Two-field curvature mesh'],grids)):
 u,r,_=ref.continuous_x(grid,T);eu=abs(np.interp(dense,grid,u)-ue);er=abs(np.interp(dense,grid,r)-re)
 results['mesh'].append({'mesh':name,'nodes':401,'u':float(max(eu)),'rho':float(max(er)),'min_dx':float(min(np.diff(grid))),'max_dx':float(max(np.diff(grid)))})
 ax[0].plot((grid[1:]+grid[:-1])/2,np.diff(grid),color=colors[mi],ls=['-','--',':'][mi],label=name)
 ax[1].plot(dense,eu,color=colors[mi],ls=['-','--',':'][mi]);ax[2].plot(dense,er,color=colors[mi],ls=['-','--',':'][mi])
for j in range(3):ax[j].set(xlabel='$x$',ylabel=['Cell width','Interpolation error in $u$',r'Interpolation error in $\rho$'][j])
ax[0].legend(fontsize=7);save(fig,'mesh')
arrays['times']=times
np.savez_compressed(OUT/'curves.npz',**arrays)
results['source_hashes']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [BASE/'hs_exact.py',BASE/'hs_solver.py',BASE/'hs_fixed.py']}
(OUT/'results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print('All experiments saved',flush=True)
