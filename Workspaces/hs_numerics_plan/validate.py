"""Independent implementation checks for reference fields and solvers."""
import numpy as np
from hs_exact import Soliton
from hs_solver import MovingSystem,solve
from hs_fixed import FixedSystem

def check_exact_rhs(reference,a,k0,m,t):
    system=MovingSystem(a,1.,m,lambda time:reference.lattice(np.array([k0]),a,time)[0][0])
    h=2e-5
    f=lambda time:system.exact_initial(reference,k0,time)
    z=f(t)
    finite_difference=(f(t+h)-f(t-h))/(2*h)
    assert np.max(abs(finite_difference-system.rhs(t,z))) < 5e-9
    state=system.fields(t,z)
    assert np.allclose(np.diff(state['x']),state['d'],atol=2e-14)
    assert np.allclose(state['rho']*state['d'],a,atol=2e-14)

for ref in (Soliton((5.,)),Soliton((1.1,1.25))):
    check_exact_rhs(ref,.02,-100,200,.12)

ref=Soliton((5.,)); a=.02; k0=-200; m=400
system=MovingSystem(a,1.,m,lambda t:ref.lattice(np.array([k0]),a,t)[0][0])
z0=system.exact_initial(ref,k0,0)
errors={}
for method in ('euler','heun','midpoint','rk4','trapezoid','rk8'):
    errors[method]=[]
    for dt in ((.5,.25) if method=='rk8' else (.05,.025)):
        result=solve(system,z0,0,1,dt,method)
        u=system.fields(1,result.states[-1])['u']
        exact=ref.lattice_state(np.arange(k0,k0+m+1),a,1)['u']
        errors[method].append(np.max(abs(u-exact)))
assert errors['euler'][0]/errors['euler'][1] > 1.3
assert errors['heun'][0]/errors['heun'][1] > 3
assert errors['midpoint'][0]/errors['midpoint'][1] > 3
assert errors['rk4'][0]/errors['rk4'][1] > 12
assert errors['trapezoid'][0]/errors['trapezoid'][1] > 3
assert errors['rk8'][0]/errors['rk8'][1] > 100

fixed=FixedSystem(np.linspace(-4,4,201),1.,ref)
z0=fixed.initial(0)
u=fixed.fields(0,z0)['u']
ue,_,_=ref.continuous_x(fixed.x,0)
assert np.max(abs(u-ue)) < 2e-12
print('PASS: exact ODE traces, geometry, six time methods, fixed Poisson reconstruction')
