from run_paper_support import *
from hs_fixed import FixedSystem
exec((ROOT/'mesh_evolution.py').read_text().split('rows=[]')[0])
rows=[];saved={}
for ci,(case,p) in enumerate([('One soliton',(5.,)),('Two solitons',(1.1,1.25))]):
 ref=Soliton(p);common=np.linspace(-2.5,2.5,2001);uc,rc,_=ref.continuous_x(common,.25)
 Xd=np.linspace(-4,4,8001);u,x,r=ref.continuous_X(Xd,0)
 cu=abs(np.gradient(np.gradient(u,x),x));cr=abs(np.gradient(np.gradient(r,x),x))
 fig,ax=plt.subplots(1,3,figsize=(11,3.2),layout='constrained')
 for mi,name in enumerate(['Fixed FD','Moving FD','Adaptive moving FD']):
  if mi==0:s=FixedSystem(np.linspace(-4,4,201),1,ref);z=s.initial(0)
  else:
   gamma=0 if mi==1 else 2;M=1+gamma/2*(cu/max(cu)+cr/max(cr));integ=np.r_[0,cumulative_trapezoid(M,Xd)]
   X=np.interp(np.linspace(0,integ[-1],201),integ,Xd);u0,x0,_=ref.continuous_X(X,0)
   s=WeightedMoving(np.diff(X),lambda t:float(ref.continuous_X(X[:1],t)[0][0]));z=s.pack(np.diff(u0),np.diff(x0),x0[0])
  rr=solve(s,z,0,.25,.0005,'rk4');hh=solve(s,z,0,.25,.00025,'rk4');f=s.fields(.25,rr.states[-1])
  xr=f['x'] if mi==0 else (f['x'][1:]+f['x'][:-1])/2
  eu=abs(np.interp(common,f['x'],f['u'])-uc);er=abs(np.interp(common,xr,f['rho'])-rc)
  rows.append({'case':case,'method':name,'u':float(max(eu)),'rho':float(max(er)),'dt_halving_change':float(max(abs(rr.states[-1]-hh.states[-1])))})
  ax[0].plot((f['x'][1:]+f['x'][:-1])/2,np.diff(f['x']),color=colors[mi],ls=['-','--','-.'][mi],label=name)
  for j,e in enumerate([eu,er],1):ax[j].plot(common,e,color=colors[mi],ls=['-','--','-.'][mi])
  saved[f'{ci}_{mi}_x']=f['x'];saved[f'{ci}_{mi}_u']=f['u'];saved[f'{ci}_{mi}_rho']=f['rho']
 for j in range(3):ax[j].set(xlabel='$x$',ylabel=['Cell width','Common-point error in $u$',r'Common-point error in $\rho$'][j])
 ax[0].legend(fontsize=7);save(fig,f'fd_mesh_{ci}')
 print(case,flush=True)
(OUT/'fd_mesh_comparison.json').write_text(json.dumps(rows,indent=2),encoding='utf-8');np.savez_compressed(OUT/'fd_mesh_comparison.npz',**saved)
# Spatial-method figures: only integrable SD and fixed FD.
d=np.load(OUT/'case_figures.npz')
for ci,p in enumerate([(5.,),(1.1,1.25)]):
 ref=Soliton(p);fig,ax=plt.subplots(2,2,figsize=(9,5.4),layout='constrained')
 for j,q in enumerate(['u','rho']):
  for mi,kind in enumerate(['sd','fixed']):
   xx=d[f'{ci}_{kind}_{q}_x'];v=d[f'{ci}_{kind}_{q}'];e=d[f'{ci}_{kind}_{q}_error']
   ax[0,j].plot(xx[::12],v[::12],ls='none',marker=['o','s'][mi],mfc='none',ms=3,color=colors[mi],label=['Integrable SD','FD'][mi]);ax[1,j].semilogy(xx,abs(e),color=colors[mi],ls=['-','--'][mi])
  xx=np.linspace(min(d[f'{ci}_sd_u_x'][0],-4),max(d[f'{ci}_sd_u_x'][-1],4),1401)
  ax[0,j].plot(xx,ref.continuous_x(xx,.125)[j],'k-',lw=1,label='Continuous exact',zorder=0)
  ax[0,j].set(xlabel='$x$',ylabel=['$u$',r'$\rho$'][j]);ax[1,j].set(xlabel='$x$',ylabel='Absolute error')
 ax[0,0].legend(fontsize=8);save(fig,f'spatial_sd_fd_{ci}')
