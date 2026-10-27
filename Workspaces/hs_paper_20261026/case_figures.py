"""Case-based midpoint figures and time-integrator error maps."""
from run_paper_support import *
from hs_fixed import FixedSystem
names=['Integrable SD','Moving FD','Fixed FD'];methods=['euler','rk4','trapezoid']
raw={};checks={}
for ci,p in enumerate([(5.,),(1.1,1.25)]):
 ref=Soliton(p);k=np.arange(-200,201);a=.02;midtime=.125
 X=np.linspace(-4,4,1201);u,x,r=ref.continuous_X(X,midtime)
 fig,ax=plt.subplots(1,2,figsize=(9,2.8),layout='constrained')
 for j,vals in enumerate([u,r]):ax[j].plot(x,vals,color=colors[0]);ax[j].set(xlabel='$x$',ylabel=['$u$',r'$\rho$'][j],title=['(a) Velocity','(b) Density'][j])
 save(fig,f'profile_mid_{ci}')
 fig,ax=plt.subplots(2,2,figsize=(9,5.4),layout='constrained')
 for mi,kind in enumerate(['sd','fd','fixed']):
  if kind=='fixed':s=FixedSystem(np.linspace(-4,4,401),1,ref);z=s.initial(0)
  else:
   s=MovingSystem(a,1,400,lambda t:float(ref.continuous_X(np.array([-4.]),t)[0][0]),kind)
   uu,xx,_=ref.continuous_X(k*a,0);z=s.pack(np.diff(uu),np.diff(xx),xx[0])
  sol=solve(s,z,0,midtime,.0005,'rk4');f=s.fields(midtime,sol.states[-1])
  for j,q in enumerate(['u','rho']):
   xx=f['x'] if j==0 or kind=='fixed' else (f['x'][1:]+f['x'][:-1])/2
   ee=ref.continuous_density_cell_mean(f['x'][:-1],f['x'][1:],midtime) if j==1 and kind!='fixed' else ref.continuous_x(xx,midtime)[j]
   ax[0,j].plot(xx[::12],f[q][::12],ls='none',marker=['o','s','^'][mi],mfc='none',ms=3,color=colors[mi],label=names[mi])
   ax[1,j].semilogy(xx,abs(f[q]-ee),ls=['-','--','-.'][mi],color=colors[mi])
   raw[f'{ci}_{kind}_{q}']=f[q];raw[f'{ci}_{kind}_{q}_x']=xx;raw[f'{ci}_{kind}_{q}_error']=f[q]-ee
   checks[f'{ci}_{kind}_{q}_max']=float(max(abs(f[q]-ee)))
 for j in range(2):
  ax[0,j].plot(x,[u,r][j],color='black',lw=1,label='Continuous exact',zorder=0)
  ax[0,j].set(xlabel='$x$',ylabel=['$u$',r'$\rho$'][j],title=['(a) Velocity','(b) Density'][j]);ax[1,j].set(xlabel='$x$',ylabel='Absolute error',title=['(c) Velocity error','(d) Density error'][j])
 ax[0,0].legend(fontsize=8);save(fig,f'spatial_mid_{ci}')
 # Temporal error at matching exact lattice labels, displayed at exact lattice x.
 times=np.linspace(0,.25,51);grid=np.linspace(-3.5,3.5,351)
 s=MovingSystem(a,1,400,lambda t:float(ref.lattice(k[:1],a,t)[0][0]))
 z=s.exact_initial(ref,k[0],0)
 fig,ax=plt.subplots(3,2,figsize=(9,7),layout='constrained')
 for mi,method in enumerate(methods):
  rr=solve(s,z,0,.25,.0025,method,outputs=times,tol=2e-13);curves=[[],[]]
  for t,zz in zip(times,rr.states):
   f=s.fields(t,zz);ex=ref.lattice_state(k,a,t)
   for j,q in enumerate(['u','rho']):
    xx=ex['x'] if j==0 else (ex['x'][1:]+ex['x'][:-1])/2
    curves[j].append(np.interp(grid,xx,abs(f[q]-ex[q])))
  for j in range(2):
   vals=np.array(curves[j]);raw[f'temporal_map_{ci}_{method}_{j}']=vals
   im=ax[mi,j].pcolormesh(grid,times,vals,shading='auto',cmap='magma');ax[mi,j].grid(False);cb=fig.colorbar(im,ax=ax[mi,j]);cb.formatter.set_powerlimits((0,0));cb.update_ticks()
   ax[mi,j].set(xlabel='$x_a^*$',ylabel='$t$',title=['Euler','RK4','Crank–Nicolson'][mi]+[' : $|e_u|$',r' : $|e_\rho|$'][j])
 save(fig,f'temporal_maps_{ci}')
 print('Finished case',ci,flush=True)
np.savez_compressed(OUT/'case_figures.npz',**raw)
(OUT/'midpoint_errors.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
