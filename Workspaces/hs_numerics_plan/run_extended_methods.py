"""Time orders 1/2/4/8, direct fixed-grid differences, and collision audit."""
import hashlib
import json
from pathlib import Path
from time import perf_counter
import numpy as np
from hs_exact import Soliton
from hs_fixed import FixedSystem
from hs_solver import MovingSystem,solve

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'out';OUT.mkdir(exist_ok=True)
METHODS=('euler','heun','midpoint','trapezoid','rk4','rk8')

def err(result,system,ref,k0,a):
    t=float(result.t[-1]); f=system.fields(t,result.states[-1]);ex=ref.lattice_state(np.arange(k0,k0+system.edges+1),a,t)
    return {'u_linf':float(np.max(abs(f['u']-ex['u']))),
            'rho_linf':float(np.max(abs(f['rho']-ex['rho']))),
            'x_linf':float(np.max(abs(f['x']-ex['x']))),
            'min_d':float(f['d'].min())}

def semi_discrete_methods():
    ref=Soliton((5.,)); a=.02;k0=-200;m=400
    system=MovingSystem(a,1,m,lambda t:float(ref.lattice(np.array([k0]),a,t)[0][0]))
    z0=system.exact_initial(ref,k0,0)
    rows=[]
    for method in METHODS:
        dts=(.5,.25,.125,.1,.0625) if method=='rk8' else (.1,.05,.025,.0125)
        for dt in dts:
            start=perf_counter()
            result=solve(system,z0,0,1,dt,method,strict=False)
            rows.append({'method':method,'dt':dt,'status':result.status,
                         'seconds':perf_counter()-start,'accepted':result.accepted,
                         'rejected':result.rejected,'residual':result.max_residual,
                         'error':err(result,system,ref,k0,a)})
    return rows

def fixed_grid_methods():
    ref=Soliton((5.,)); nx=201; x=np.linspace(-4,4,nx)
    system=FixedSystem(x,1,ref);z0=system.initial(0);T=.25
    start=perf_counter()
    reference=solve(system,z0,0,T,.000625,'rk8')
    reference_seconds=perf_counter()-start
    zref=reference.states[-1]
    uexact,rhoexact,_=ref.continuous_x(x,T)
    rows=[]
    for method in METHODS:
        for dt in (.02,.01,.005):
            start=perf_counter()
            result=solve(system,z0,0,T,dt,method,strict=False)
            f=system.fields(result.t[-1],result.states[-1])
            if result.status=='completed':
                z_error=float(np.max(abs(result.states[-1]-zref)))
                total_u=float(np.max(abs(f['u']-uexact)))
                total_rho=float(np.max(abs(f['rho']-rhoexact)))
            else:
                z_error=total_u=total_rho=None
            rows.append({'method':method,'dt':dt,'status':result.status,
                         'seconds':perf_counter()-start,'accepted':result.accepted,
                         'temporal_state_linf':z_error,
                         'physical_u_linf':total_u,'physical_rho_linf':total_rho,
                         'max_implicit_residual':result.max_residual})
    return {'nx':nx,'T':T,'reference_method':'rk8','reference_dt':.000625,
            'reference_seconds':reference_seconds,'rows':rows}

def fixed_grid_spatial():
    ref=Soliton((5.,));T=.25;dt=.005
    rows=[]
    for nx in (101,201,401,801):
        x=np.linspace(-4,4,nx); system=FixedSystem(x,1,ref);z0=system.initial(0)
        start=perf_counter();result=solve(system,z0,0,T,dt,'rk8',strict=False)
        f=system.fields(result.t[-1],result.states[-1]);ue,re,_=ref.continuous_x(x,result.t[-1])
        rows.append({'nx':nx,'dx':float(x[1]-x[0]),'T_reached':float(result.t[-1]),
                     'dt':dt,'status':result.status,'seconds':perf_counter()-start,
                     'u_linf':float(np.max(abs(f['u']-ue))),
                     'rho_linf':float(np.max(abs(f['rho']-re)))})
    return rows

def collision_rk8():
    ref=Soliton((1.1,1.25));a=.02;k0=-200;m=400
    system=MovingSystem(a,1,m,lambda t:float(ref.lattice(np.array([k0]),a,t)[0][0]))
    z0=system.exact_initial(ref,k0,-3)
    rows=[]
    for dt in (.05,.025,.0125):
        start=perf_counter()
        r=solve(system,z0,-3,3,dt,'rk8',outputs=[-3,0,3],strict=False)
        rows.append({'dt':dt,'status':r.status,'seconds':perf_counter()-start,
                     'stages':[{'t':float(t),'error':err(
                         type('View',(),{'t':[t],'states':[z]})(),system,ref,k0,a)}
                         for t,z in zip(r.t,r.states)]})
    start=perf_counter()
    long=solve(system,z0,-3,9,.0125,'rk8',outputs=[-3,0,3,6,9],strict=False)
    return {'T_to_3':rows,'long':{'dt':.0125,'status':long.status,
             'seconds':perf_counter()-start,'failure_reason':long.failure_reason,
             'stages':[{'t':float(t),'error':err(
                 type('View',(),{'t':[t],'states':[z]})(),system,ref,k0,a)}
                 for t,z in zip(long.t,long.states)]}}

def main():
    print('semi-discrete time methods',flush=True);sd=semi_discrete_methods()
    print('fixed-grid time methods',flush=True);ft=fixed_grid_methods()
    print('fixed-grid spatial refinement',flush=True);fs=fixed_grid_spatial()
    print('two-soliton RK8',flush=True);collision=collision_rk8()
    report={'semi_discrete':{'a':.02,'p':5,'X':[-4,4],'T':1,'rows':sd},
            'fixed_grid_time':ft,'fixed_grid_spatial':fs,'collision_rk8':collision,
            'rk8_definition':'Fixed-step 12-stage DOP853 eighth-order main formula; not an adaptive tolerance run.',
            'code_sha256':{n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest()
                for n in ('hs_solver.py','hs_fixed.py','hs_exact.py','run_extended_methods.py')}}
    path=OUT/'extended_methods.json'
    path.write_text(json.dumps(report,indent=2),encoding='utf-8')
    print('Wrote',path,flush=True)

if __name__=='__main__':main()
