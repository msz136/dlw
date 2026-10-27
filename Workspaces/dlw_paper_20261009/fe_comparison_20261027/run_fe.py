"""P1 finite-element y approximation with exact element integration.
Cell tests for the integrated first equation; continuous hat tests for second.
Consistent (not lumped) mass, full endpoint hats, no ghost extrapolation.
"""
from pathlib import Path
import sys,json,time,importlib.util
import numpy as np
from scipy.linalg import solve_banded
HERE=Path(__file__).resolve().parent
P=HERE.parent
sys.path.insert(0,str(P/'spatial_audit_20261023/separated'))
from run_separated import Model,fields,HALF_WIDTHS
spec=importlib.util.spec_from_file_location('nondeg_run',P/'report_refresh_20261024/nondegenerate_rk4_20261024/run.py')
non=importlib.util.module_from_spec(spec);spec.loader.exec_module(non)

class FE:
 def __init__(self,m):
  self.m=m;n=len(m.y)
  self.ab=np.zeros((3,n));self.ab[0,1:]=1/6;self.ab[2,:-1]=1/6
  self.ab[1]=2/3;self.ab[1,[0,-1]]=1/3
 def mass(self,z):
  q=2*z/3;q=q.copy();q[[0,-1]]/=2;q[1:]+=z[:-1]/6;q[:-1]+=z[1:]/6
  return q
 def product(self,u,v):
  l=u[:-1]*v[:-1];r=u[1:]*v[1:];cross=u[:-1]*v[1:]+u[1:]*v[:-1]
  q=np.zeros_like(u);q[:-1]+=(3*l+cross+r)/12;q[1:]+=(l+cross+3*r)/12
  return q
 def derivative_load(self,u):
  d=np.diff(u,axis=0)/(2*self.m.h);q=np.zeros_like(u);q[:-1]+=d;q[1:]+=d
  return q
 def rhs(self,t,z):
  m=self.m;u,v=z
  r=-np.diff(m.d1(u*u/2+2*m.a*u),axis=0)/m.h-m.d2((v[1:]+v[:-1])/2)
  lo=m.ut(m.y[:1],t)
  ut=np.concatenate((lo,lo+m.h*np.cumsum(r,axis=0)))
  load=-m.d1(self.product(u,v)+self.mass(2*m.a*v-4*u))-m.d2(self.derivative_load(u))
  vt=solve_banded((1,1),self.ab,load,check_finite=False)
  return np.array([ut,vt])

def model(case):return Model(case,'FD',.1,.1) if case in ('A','D') else non.NondegenerateModel(case,'FD')
def norms(m,e):
 if m.case in ('A','D'):
  R=HALF_WIDTHS[m.case];return [float(abs(q[abs(m.y)<R][:,abs(m.x)<=R]).max()) for q in e]
 return [non.measured(m,q,m.y)[0] for q in e]
def run(case,dt=1e-4):
 m=model(case);fe=FE(m);z0=m.initial();z=z0.copy();start=time.time()
 truth=fields(m,m.y)[2] if case in ('A','D') else np.array([non.initial_data(case,m.x,m.y)[q] for q in ('ut','vt')])
 initial=fe.rhs(0,z0);ini=norms(m,initial-truth)
 for i in range(round(.01/dt)):
  t=i*dt;k1=fe.rhs(t,z);k2=fe.rhs(t+dt/2,z+dt*k1/2);k3=fe.rhs(t+dt/2,z+dt*k2/2);k4=fe.rhs(t+dt,z+dt*k3)
  z+=dt*(k1+2*k2+2*k3+k4)/6
  assert np.isfinite(z).all()
  if (i+1)%25==0:print(case,dt,i+1,flush=True)
 ref=m.profile(m.y,.01);err=norms(m,z-ref)
 stem=case if dt==1e-4 else case+'_halfdt'
 np.savez_compressed(HERE/(stem+'.npz'),x=m.x,y=m.y,z=z,z0=z0,ref=ref,rate=initial,rate_ref=truth)
 record=dict(case=case,method='FE',h=m.h,dx=m.dx,dt=dt,T=.01,nx=m.nx,ny=len(m.y),a=m.a,initial=ini,error=err,seconds=time.time()-start,status='complete')
 (HERE/(stem+'.json')).write_text(json.dumps(record,indent=2),encoding='utf8');print(record,flush=True)
if __name__=='__main__':
 for case in sys.argv[1:] or ['A','D','Gaussian','Sinusoidal']:run(case)
