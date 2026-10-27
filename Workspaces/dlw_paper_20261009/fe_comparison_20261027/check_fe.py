from run_fe import *
from numpy.polynomial.legendre import leggauss
def verify():
 m=model('Gaussian');f=FE(m);rng=np.random.default_rng(2710)
 u=rng.normal(size=(len(m.y),3));v=rng.normal(size=u.shape)
 q=np.zeros_like(u);cu=np.zeros_like(u);mass=np.zeros_like(u)
 pts,w=leggauss(4)
 for t,wt in zip((pts+1)/2,w/2):
  ue=(1-t)*u[:-1]+t*u[1:];ve=(1-t)*v[:-1]+t*v[1:]
  q[:-1]+=wt*(1-t)*ue*ve;q[1:]+=wt*t*ue*ve
  mass[:-1]+=wt*(1-t)*ve;mass[1:]+=wt*t*ve
  der=(u[1:]-u[:-1])/m.h
  cu[:-1]+=wt*(1-t)*der;cu[1:]+=wt*t*der
 checks=dict(product=float(abs(q-f.product(u,v)).max()),mass=float(abs(mass-f.mass(v)).max()),derivative=float(abs(cu-f.derivative_load(u)).max()))
 assert max(checks.values())<1e-13
 const=np.ones_like(u);linear=np.tile(m.y[:,None],(1,3))
 checks['constant_derivative']=float(abs(f.derivative_load(const)).max())
 checks['linear_derivative']=float(abs(solve_banded((1,1),f.ab,f.derivative_load(linear))-1).max())
 assert checks['linear_derivative']<1e-12
 z=m.initial();checks['first_equation_matches_fd']=float(abs(f.rhs(0,z)[0]-m.rhs(0,z)[0]).max());assert checks['first_equation_matches_fd']<1e-13
 (HERE/'assembly_validation.json').write_text(json.dumps(checks,indent=2));print(checks,flush=True)
if __name__=='__main__':
 verify()
 for case in ['A','D','Gaussian','Sinusoidal']:run(case,5e-5)
