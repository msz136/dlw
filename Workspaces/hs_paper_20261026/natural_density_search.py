"""Untuned, structurally motivated density candidates for the c=1 branch."""
import json
import numpy as np
from conserved_mesh import ROOT,ale,reference
OUT=ROOT/'data/natural_density_search';OUT.mkdir(exist_ok=True)

def monitor_flux(kind,m,r,u,w,rx=None):
 if kind=='fixed':return np.ones_like(r),np.zeros_like(r)
 if kind=='rho':return r,-u*r
 if kind=='deficit':return 2-r,u*r
 if kind=='momentum':return m/2,-(u*(m-2)+w*w/2+4*u+(r*r-1)/2)/2
 if kind=='curvature_deficit':return 2-m/2,(u*(m-2)+w*w/2+4*u+(r*r-1)/2)/2
 if kind=='energy':
  E=w*w-(r*r-1)
  return 1+E,-u*E-4*u*u+2*u
 if kind=='rm':return m/(2*r),-u*m/(2*r)-(r-1)/2
 if kind=='hierarchy2':
  R=(m*m-rx*rx)/(4*r**3)
  return R,-u*R+(1/r-1)
 if kind in ['spectral_plus','spectral_minus']:
  sign=1 if kind=='spectral_plus' else -1
  R=(m+sign*rx)/(2*r)
  return R,-u*R-(r-1)/2-sign*w/2
 raise ValueError(kind)

def rhs(state,sol,t,kind,left,right):
 x=state[0];m,r,u,_=ale.unpack(state,sol,t,left,right)
 ux=ale.first_derivative(u,x);w=np.r_[0,ux,0]
 rx=ale.first_derivative(r,x)
 R,Q=monitor_flux(kind,m,r,u,w,np.r_[0,rx,0])
 if min(R)<=0:raise ValueError('nonpositive monitor')
 V=Q[1:-1]/R[1:-1];mx=ale.first_derivative(m,x);rx=ale.first_derivative(r,x)
 return np.r_[0,V,0],(u[1:-1]+V)*mx+2*ux*m[1:-1]+r[1:-1]*rx,(u[1:-1]+V)*rx+r[1:-1]*ux
ale.rhs=rhs

def experiment(p,nodes,kind,dt=.0005):
 sol=ale.Soliton(p);dense=np.linspace(-4,4,max(20001,50*nodes+1))
 u,r,m,_=reference(sol,dense,0);X=sol.continuous_x(dense,0)[2];wt,o,b=sol._weights(X,0)
 o=o-np.sum(wt*o,axis=0);b=b-np.sum(wt*b,axis=0);w=np.sum(wt*o*o*b,axis=0)*r
 rX=np.sum(wt*o*b*b,axis=0)*r*r
 rx=rX*r
 R,_=monitor_flux(kind,m,r,u,w,rx)
 if min(R)<=0:raise ValueError('nonpositive initial monitor')
 mass=np.r_[0,np.cumsum((R[1:]+R[:-1])*np.diff(dense)/2)]
 x=np.interp(np.linspace(0,mass[-1],nodes),mass,dense) if kind!='fixed' else np.linspace(-4,4,nodes)
 u,r,_,_=reference(sol,x,0);z=(x,ale.second_derivative(u,x)+2,r[1:-1])
 for step in range(round(.25/dt)):z=ale.rk4(z,sol,step*dt,dt,kind,-4,4)
 m,r,u,_=ale.unpack(z,sol,.25,-4,4);x=z[0];ue,re,_,_=reference(sol,x,.25);mask=abs(x)<=2.5
 R,_=monitor_flux(kind,m,r,u,np.r_[0,ale.first_derivative(u,x),0],np.r_[0,ale.first_derivative(r,x),0])
 return dict(p=list(p),nodes=nodes,kind=kind,dt=dt,u=float(max(abs(u[mask]-ue[mask]))),rho=float(max(abs(r[mask]-re[mask]))),min_h=float(min(np.diff(x))),min_R=float(min(R)))

if __name__=='__main__':
 rows=[]
 for nodes in [200,1000,2000]:
  for p in [(5.,),(1.1,1.25)]:
   for kind in ['fixed','rho','deficit','momentum','energy','rm']:
    try:row=experiment(p,nodes,kind)
    except Exception as exc:row=dict(p=list(p),nodes=nodes,kind=kind,error=str(exc))
    rows.append(row);print(json.dumps(row),flush=True)
    (OUT/'results.json').write_text(json.dumps(rows,indent=2))
