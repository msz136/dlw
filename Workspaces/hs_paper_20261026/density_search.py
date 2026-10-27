"""Conserved-monitor search with all trials retained, same nodal metric."""
import json,time
import numpy as np
from conserved_mesh import ROOT,ale,reference
OUT=ROOT/'data/density_search';OUT.mkdir(exist_ok=True)

def rhs(state,sol,t,mode,left,right):
 alpha,motion,*extra=mode
 beta=extra[0] if extra else 0
 x=state[0];m,r,u,R=ale.unpack(state,sol,t,left,right)
 ux=ale.first_derivative(u,x)
 w=np.r_[0,ux,0]
 E=w*w-(r*r-1)
 monitor=1+alpha*(R-1)+beta*E
 if min(monitor)<=0:raise ValueError('monitor nonpositive')
 V=(alpha*(-u*R-(r-1)/2)+beta*(-u*E-4*u*u+2*u))/monitor if motion else np.zeros_like(x)
 mx=ale.first_derivative(m,x);rx=ale.first_derivative(r,x)
 return np.r_[0,V[1:-1],0],(u[1:-1]+V[1:-1])*mx+2*ux*m[1:-1]+r[1:-1]*rx,(u[1:-1]+V[1:-1])*rx+r[1:-1]*ux
ale.rhs=rhs

def experiment(p,nodes,alpha,motion=True,dt=.0005,beta=0,quadrature_factor=1):
 sol=ale.Soliton(p)
 dense=np.linspace(-4,4,quadrature_factor*(max(20001,50*nodes+1)-1)+1)
 u,r,_,R=reference(sol,dense,0)
 X=sol.continuous_x(dense,0)[2];wt,o,b=sol._weights(X,0)
 o=o-np.sum(wt*o,axis=0);b=b-np.sum(wt*b,axis=0)
 ux=np.sum(wt*o*o*b,axis=0)*r
 E=ux*ux-(r*r-1)
 monitor=1+alpha*(R-1)+beta*E
 if min(monitor)<=0:raise ValueError('initial monitor nonpositive')
 mass=np.r_[0,np.cumsum((monitor[1:]+monitor[:-1])*np.diff(dense)/2)]
 x=np.interp(np.linspace(0,mass[-1],nodes),mass,dense) if alpha or beta else np.linspace(-4,4,nodes)
 u,r,_,_=reference(sol,x,0);z=(x,ale.second_derivative(u,x)+2,r[1:-1])
 for step in range(round(.25/dt)):z=ale.rk4(z,sol,step*dt,dt,(alpha,motion,beta),-4,4)
 m,r,u,R=ale.unpack(z,sol,.25,-4,4);x=z[0];ue,re,_,_=reference(sol,x,.25)
 mask=abs(x)<=2.5
 w=np.r_[0,ale.first_derivative(u,x),0]
 return dict(p=list(p),nodes=nodes,alpha=alpha,beta=beta,motion=motion,dt=dt,u=float(max(abs(u[mask]-ue[mask]))),rho=float(max(abs(r[mask]-re[mask]))),min_h=float(min(np.diff(x))),min_monitor=float(min(1+alpha*(R-1)+beta*(w*w-(r*r-1))))),dict(x=x,u=u,rho=r)

if __name__=='__main__':
 rows=[]
 for nodes in [200,1000,2000]:
  for p in [(5.,),(1.1,1.25)]:
   for alpha,motion in [(0,True),(.1,True),(.25,True),(.5,True),(.75,True),(1,True),(1,False)]:
    row,arr=experiment(p,nodes,alpha,motion);rows.append(row)
    (OUT/'scan.json').write_text(json.dumps(rows,indent=2))
    np.savez_compressed(OUT/f'n{nodes}_p{p[0]}_a{alpha}_motion{motion}.npz',**arr)
    print(json.dumps(row),flush=True)
