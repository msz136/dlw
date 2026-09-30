"""Reproducible E0-E6 study for the 2-HS moving-mesh proposal.

Usage: python Workspaces/hs_numerics_plan/run_study.py [--quick]
Outputs are written only inside Workspaces/hs_numerics_plan/out/.
"""
import argparse
import hashlib
import json
from pathlib import Path
from time import perf_counter
import numpy as np
import scipy
from hs_exact import Soliton
from hs_solver import MovingSystem, solve
from hs_fixed import FixedSystem

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'out'


def primitive(value):
    if isinstance(value,dict): return {k:primitive(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)): return [primitive(v) for v in value]
    if isinstance(value,np.ndarray): return primitive(value.tolist())
    if isinstance(value,(np.integer,np.floating)): return value.item()
    return value


def model(ref,a,k0,m,kind='sd',boundary='lattice'):
    if boundary=='lattice':
        b=lambda t: float(ref.lattice(np.array([k0]),a,t)[0][0])
    else:
        b=lambda t: float(ref.continuous_X(np.array([k0*a]),t)[0][0])
    return MovingSystem(a,ref.c,m,b,kind)


def continuous_initial(ref,a,k0,m):
    X=a*np.arange(k0,k0+m+1)
    u,x,_=ref.continuous_X(X,0)
    return np.r_[np.diff(u),np.diff(x),x[0]]


def norms(error,weights):
    return {'linf':float(np.max(abs(error))),
            'l2':float(np.sqrt(np.sum(weights*error**2)/np.sum(weights)))}


def metrics(ref,a,k0,system,t,z,include_model=True):
    f=system.fields(t,z); k=np.arange(k0,k0+system.edges+1)
    u=f['u']; d=f['d']; x=f['x']; rho=f['rho']
    ustar,rhostar,_=ref.continuous_x(x,t)
    edge_ref=ref.continuous_density_cell_mean(x[:-1],x[1:],t)
    nodeweights=np.r_[d[0]/2,(d[:-1]+d[1:])/2,d[-1]/2]
    result={'physical_u':norms(u-ustar,nodeweights),
            'physical_rho_cell':norms(rho-edge_ref,d),
            'min_d':float(d.min()),'max_d':float(d.max()),
            'mesh_ratio':float(d.max()/d.min()),
            'min_rho':float(rho.min()),'max_rho':float(rho.max()),
            'max_abs_w':float(np.max(abs(f['w']))),
            'peak_x':float(x[np.argmax(u)]),'peak_u':float(u.max())}
    if include_model:
        exact=ref.lattice_state(k,a,t)
        exd=exact['d']
        result['solver_u']=norms(u-exact['u'],nodeweights)
        result['solver_rho']=norms(rho-exact['rho'],d)
        result['solver_x_linf']=float(np.max(abs(x-exact['x'])))
        ec_u,_,_=ref.continuous_x(exact['x'],t)
        ec_rho=ref.continuous_density_cell_mean(exact['x'][:-1],exact['x'][1:],t)
        result['model_u_linf']=float(np.max(abs(exact['u']-ec_u)))
        result['model_rho_cell_linf']=float(np.max(abs(exact['rho']-ec_rho)))
        result['exact_peak_x']=float(exact['x'][np.argmax(exact['u'])])
    return result


def time_methods(quick):
    ref=Soliton((5.,)); a=.02; k0=-200; m=400; t1=1.
    system=model(ref,a,k0,m)
    initial=system.exact_initial(ref,k0,0)
    dts=[.1,.05,.025,.0125] if not quick else [.1,.05,.025]
    rows=[]; saved=None
    for method in ('euler','rk4','trapezoid'):
        for dt in dts:
            start=perf_counter()
            result=solve(system,initial,0,t1,dt,method,outputs=[0,.25,.5,1])
            cost=perf_counter()-start
            check=metrics(ref,a,k0,system,t1,result.states[-1])
            rows.append({'method':method,'dt':dt,'seconds':cost,
                         'accepted':result.accepted,'rejected':result.rejected,
                         'iterations':result.iterations,'max_residual':result.max_residual,
                         'metrics':check})
            if method=='rk4' and dt==dts[-1]: saved=(result,system,ref,k0)
    return rows,saved


def continuum_limit(quick):
    ref=Soliton((5.,)); t=.5
    aa=[.04,.02,.01,.005] if not quick else [.04,.02,.01]
    rows=[]
    for a in aa:
        m=int(round(8/a)); k0=-m//2
        system=model(ref,a,k0,m)
        z0=system.exact_initial(ref,k0,0)
        dt=.002
        result=solve(system,z0,0,t,dt,'rk4')
        rows.append({'a':a,'nodes':m+1,'dt':dt,
                     'metrics':metrics(ref,a,k0,system,t,result.states[-1])})
    return rows


def collision(quick):
    ref=Soliton((1.1,1.25)); a=.02; k0=-200; m=400
    system=model(ref,a,k0,m)
    t0,t1=(-2.,2.) if quick else (-3.,3.)
    times=np.linspace(t0,t1,5)
    z0=system.exact_initial(ref,k0,t0)
    rows=[]; saved=None
    for dt in ([.002,.001] if quick else [.001,.0005]):
        start=perf_counter()
        result=solve(system,z0,t0,t1,dt,'rk4',outputs=times,strict=False)
        cost=perf_counter()-start
        rows.append({'dt':dt,'seconds':cost,'status':result.status,
                     'failure_reason':result.failure_reason,
                     'accepted':result.accepted,'rejected':result.rejected,
                     'stages':[{'t':float(t),'metrics':metrics(ref,a,k0,system,t,z)}
                               for t,z in zip(result.t,result.states)]})
        if dt==([.002,.001] if quick else [.001,.0005])[-1]: saved=(result,system,ref,k0)
    return rows,saved


def comparison(quick):
    ref=Soliton((5.,));a=.02;k0=-200;m=400
    t1=.25 if quick else .5
    dt=.001
    rows=[]; saved={}
    for kind in ('sd','fd'):
        system=model(ref,a,k0,m,kind,'continuous')
        z0=continuous_initial(ref,a,k0,m)
        start=perf_counter()
        result=solve(system,z0,0,t1,dt,'rk4')
        cost=perf_counter()-start
        check=metrics(ref,a,k0,system,t1,result.states[-1],False)
        rows.append({'kind':kind,'method':'rk4','dt':dt,'seconds':cost,
                     'status':result.status,'metrics':check})
        saved[kind]=system.fields(t1,result.states[-1])
    fixed=FixedSystem(np.linspace(-4,4,m+1),1.,ref)
    z0=fixed.initial(0)
    start=perf_counter()
    result=solve(fixed,z0,0,t1,dt,'trapezoid')
    cost=perf_counter()-start
    f=fixed.fields(t1,result.states[-1]); ue,re,_=ref.continuous_x(f['x'],t1)
    dx=fixed.dx; weights=np.r_[dx/2,np.full(m-1,dx),dx/2]
    rows.append({'kind':'fixed','method':'crank-nicolson','dt':dt,'seconds':cost,
                 'status':result.status,'max_residual':result.max_residual,
                 'iterations':result.iterations,
                 'metrics':{'physical_u':norms(f['u']-ue,weights),
                            'physical_rho_node':norms(f['rho']-re,weights),
                            'min_rho':float(f['rho'].min())}})
    saved['fixed']=f
    return rows,saved,t1


def steepness(quick):
    rows=[]; ps=[3.,5.] if quick else [3.,5.,10.]
    for p in ps:
        ref=Soliton((p,));a=.01;k0=-400;m=800
        system=model(ref,a,k0,m)
        z0=system.exact_initial(ref,k0,0)
        result=solve(system,z0,0,.25,.0005,'rk4',strict=False)
        t=result.t[-1]
        rows.append({'p':p,'q':float(ref.q[0]),'status':result.status,
                     'failure_reason':result.failure_reason,
                     'metrics':metrics(ref,a,k0,system,t,result.states[-1])})
    return rows


def save_snapshots(single,collision_data,comparison_data,tcompare):
    sr,ss,sref,sk0=single
    dr,ds,dref,dk0=collision_data
    k=np.arange(sk0,sk0+ss.edges+1)
    kd=np.arange(dk0,dk0+ds.edges+1)
    np.savez_compressed(OUT/'snapshots.npz',
        single_times=sr.t,single_x=np.array([ss.fields(t,z)['x'] for t,z in zip(sr.t,sr.states)]),
        single_u=np.array([ss.fields(t,z)['u'] for t,z in zip(sr.t,sr.states)]),
        single_rho=np.array([ss.fields(t,z)['rho'] for t,z in zip(sr.t,sr.states)]),
        single_exact_u=np.array([sref.lattice_state(k,ss.a,t)['u'] for t in sr.t]),
        double_times=dr.t,double_x=np.array([ds.fields(t,z)['x'] for t,z in zip(dr.t,dr.states)]),
        double_u=np.array([ds.fields(t,z)['u'] for t,z in zip(dr.t,dr.states)]),
        double_rho=np.array([ds.fields(t,z)['rho'] for t,z in zip(dr.t,dr.states)]),
        double_exact_u=np.array([dref.lattice_state(kd,ds.a,t)['u'] for t in dr.t]),
        compare_t=tcompare,
        compare_sd_x=comparison_data['sd']['x'],compare_sd_u=comparison_data['sd']['u'],
        compare_fd_x=comparison_data['fd']['x'],compare_fd_u=comparison_data['fd']['u'],
        compare_fixed_x=comparison_data['fixed']['x'],
        compare_fixed_u=comparison_data['fixed']['u'])


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--quick',action='store_true')
    args=parser.parse_args();OUT.mkdir(exist_ok=True)
    total=perf_counter()
    print('E1: time methods',flush=True)
    e1,single=time_methods(args.quick)
    print('E2/E3: lattice refinement and continuum',flush=True)
    e23=continuum_limit(args.quick)
    print('E4: two-soliton interaction',flush=True)
    e4,double=collision(args.quick)
    print('E5: method comparison',flush=True)
    e5,comp,tc=comparison(args.quick)
    print('E6: smooth steepness scan',flush=True)
    e6=steepness(args.quick)
    save_snapshots(single,double,comp,tc)
    files=('hs_exact.py','hs_solver.py','hs_fixed.py','run_study.py','verify_formulas.py')
    report={'mode':'quick' if args.quick else 'full','elapsed_seconds':perf_counter()-total,
            'environment':{'numpy':np.__version__,'scipy':scipy.__version__},
            'code_sha256':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in files},
            'E1_time_methods':e1,'E2_E3_continuum':e23,'E4_collision':e4,
            'E5_comparison':e5,'E6_steepness':e6,
            'interpretation':{'grid':'u on nodes, rho=a/d on edges',
                              'boundary':'exact left trace at every RK/CN stage',
                              'single_ref':'finite-a exact lattice tau',
                              'comparison_initial':'same continuous X-grid initial state for SD/FD; fixed grid samples continuous physical state',
                              'failure':'failed runs retain a partial state and reason; no clipping or exact interior reset'}}
    (OUT/'results.json').write_text(json.dumps(primitive(report),indent=2,ensure_ascii=False),encoding='utf-8')
    print('Wrote',OUT/'results.json','elapsed',round(report['elapsed_seconds'],2),flush=True)


if __name__=='__main__': main()
