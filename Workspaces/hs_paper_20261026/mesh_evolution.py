from run_paper_support import *

class WeightedMoving(MovingSystem):
 def __init__(self,mass,b):
  self.mass=mass
  super().__init__(float(np.mean(mass)),1,len(mass),b,'fd')
 def fields(self,t,z):
  f=super().fields(t,z);f['rho']=self.mass/f['d'];return f
 def rhs(self,t,z):
  f=self.fields(t,z);v,d,u,r=f['v'],f['d'],f['u'],f['rho'];w=v/d
  return self.pack(d*(.5*w*w+2*(u[1:]+u[:-1])+.5*(r*r-1))-w*v,-v,-float(self.left_u(t)))

rows=[]
for ci,(name,p) in enumerate([('One soliton',(5.,)),('Two solitons',(1.1,1.25))]):
 ref=Soliton(p);Xd=np.linspace(-4,4,8001);u,x,r=ref.continuous_X(Xd,0)
 cu=abs(np.gradient(np.gradient(u,x),x));cr=abs(np.gradient(np.gradient(r,x),x))
 fig,ax=plt.subplots(1,3,figsize=(11,3.1),layout='constrained')
 for gi,gamma in enumerate([0,2]):
  M=1+gamma/2*(cu/max(cu)+cr/max(cr));integ=np.r_[0,cumulative_trapezoid(M,Xd)]
  X=np.interp(np.linspace(0,integ[-1],201),integ,Xd);u0,x0,_=ref.continuous_X(X,0)
  s=WeightedMoving(np.diff(X),lambda t:float(ref.continuous_X(X[:1],t)[0][0]));z=s.pack(np.diff(u0),np.diff(x0),x0[0])
  rr=solve(s,z,0,.25,.0005,'rk4');f=s.fields(.25,rr.states[-1]);rh=solve(s,z,0,.25,.00025,'rk4')
  ue,_,_=ref.continuous_x(f['x'],.25);re=ref.continuous_density_cell_mean(f['x'][:-1],f['x'][1:],.25)
  eu=abs(f['u']-ue);er=abs(f['rho']-re);mid=(f['x'][1:]+f['x'][:-1])/2
  common=np.linspace(-2.5,2.5,2001);uc,rc,_=ref.continuous_x(common,.25)
  rows.append({'case':name,'gamma':gamma,'nodes':201,'u':float(max(eu)),'rho':float(max(er)),'common_u':float(max(abs(np.interp(common,f['x'],f['u'])-uc))),'common_rho':float(max(abs(np.interp(common,mid,f['rho'])-rc))),'min_d':float(min(f['d'])),'dt_half_state_change':float(max(abs(rr.states[-1]-rh.states[-1])))})
  label='Uniform labels' if gamma==0 else 'Curvature-adapted labels'
  ax[0].plot(mid,f['d'],color=colors[gi],ls=['-','--'][gi],label=label)
  ax[1].plot(f['x'],eu,color=colors[gi],ls=['-','--'][gi]);ax[2].plot(mid,er,color=colors[gi],ls=['-','--'][gi])
 for j in range(3):ax[j].set(xlabel='$x$',ylabel=['Cell width','Absolute error in $u$',r'Absolute error in $\rho$'][j])
 ax[0].legend(fontsize=7);save(fig,f'moving_mesh_{ci}')
(OUT/'mesh_evolution.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
print('Moving mesh experiments completed')
