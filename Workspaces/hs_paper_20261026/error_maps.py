from run_paper_support import *
from hs_fixed import FixedSystem
for ci,p in enumerate([(5.,),(1.1,1.25)]):
 ref=Soliton(p);a=.02;k=np.arange(-200,201);times=np.linspace(0,.25,51);common=np.linspace(-3.5,3.5,401)
 fig,ax=plt.subplots(3,2,figsize=(9,7.4),layout='constrained');saved={}
 for mi,kind in enumerate(['sd','fd','fixed']):
  if kind=='fixed':s=FixedSystem(np.linspace(-4,4,401),1,ref);z=s.initial(0)
  else:
   s=MovingSystem(a,1,400,lambda t:float(ref.continuous_X(np.array([-4.]),t)[0][0]),kind)
   u,x,r=ref.continuous_X(k*a,0);z=s.pack(np.diff(u),np.diff(x),x[0])
  rr=solve(s,z,0,.25,.0005,'rk4',outputs=times)
  curves=[[],[]]
  for t,zz in zip(times,rr.states):
   f=s.fields(t,zz);u,r,_=ref.continuous_x(f['x'],t)
   if kind!='fixed':r=ref.continuous_density_cell_mean(f['x'][:-1],f['x'][1:],t)
   for j,q in enumerate(['u','rho']):
    xx=f['x'] if j==0 or kind=='fixed' else (f['x'][1:]+f['x'][:-1])/2
    curves[j].append(np.interp(common,xx,abs(f[q]-[u,r][j])))
  for j in range(2):
   vals=np.array(curves[j]);im=ax[mi,j].pcolormesh(common,times,vals,shading='auto',cmap='magma');ax[mi,j].grid(False);cb=fig.colorbar(im,ax=ax[mi,j]);cb.formatter.set_powerlimits((0,0));cb.update_ticks()
   ax[mi,j].set(xlabel='$x$',ylabel='$t$',title=['Integrable SD','Moving FD','Fixed FD'][mi]+(' : $|e_u|$' if j==0 else r' : $|e_\rho|$'));saved[f'{kind}_{j}']=vals
 save(fig,f'error_maps_{ci}');np.savez_compressed(OUT/f'error_maps_{ci}.npz',x=common,t=times,**saved)
print('Error maps completed')
