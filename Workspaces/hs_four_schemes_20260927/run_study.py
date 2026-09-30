"""Four complete 2HS methods. S3 uses paper initial nodes and V=-u at ALL nodes."""
import csv
import hashlib
import json
import sys
from pathlib import Path
import numpy as np
from scipy.integrate._ivp import dop853_coefficients as dc
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE.parent/'hs_error_theory_20260926'))
import run_designed_cases as eng
import run_mesh_comparison as ale
OUT=HERE/'out'
SCHEMES={'S1':'integrable_original','S2':'integrable_calibrated','S3':'difference_paper_ale','S4':'difference_fixed'}
METHODS=('euler','heun','rk4','rk8')
TIMES=(.25,.5)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def writecsv(path,rows):
    with path.open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def butcher(method):
    if method=='euler':return np.zeros((1,1)),np.array([0.]),np.array([1.])
    if method=='heun':return np.array([[0.,0.],[1.,0.]]),np.array([0.,1.]),np.array([.5,.5])
    if method=='rk4':return np.array([[0,0,0,0],[.5,0,0,0],[0,.5,0,0],[0,0,1.,0]]),np.array([0,.5,.5,1.]),np.array([1,2,2,1])/6
    assert method=='rk8'
    return dc.A[:12,:12],dc.C[:12],dc.B[:12]

def paper_ale_rhs(state,sol,t):
    x=state[0]
    m,rho,u,R=ale.unpack(state,sol,t,float(x[0]),float(x[-1]))
    ux=ale.first_derivative(u,x)
    # u+V=0, so the advective terms vanish. Same ALE D1/D2 as S4.
    return (-u,2*ux*m[1:-1]+rho[1:-1]*ale.first_derivative(rho,x),rho[1:-1]*ux)

def run_paper_ale(spec):
    sol,_,_,a,_=eng.initialize(spec['p'],'integrable_original',spec['n'],spec['halfwidth'])
    X=np.linspace(-spec['halfwidth'],spec['halfwidth'],spec['n']+1)
    u,x,_=sol.continuous_X(X,0.)
    _,rho,_,_=eng.safe_reference(sol,x,0.)
    state=(x.copy(),ale.second_derivative(u,x)+2,rho[1:-1].copy())
    arrays={};min_h=min_rho=np.inf
    init_hash=hashlib.sha256(b''.join(v.tobytes() for v in state)).hexdigest()
    A,c,b=butcher(spec['method']);dt=spec['dt'];calls=0
    def save(t):
        xx=state[0];_,rr,uu,_=ale.unpack(state,sol,t,float(xx[0]),float(xx[-1]))
        for name,arr in zip(('x','u','rho_x','rho'),(xx,uu,xx,rr)):arrays[f't{t}_{name}']=arr.copy()
    save(0.)
    for j in range(int(round(.5/dt))):
        ks=[]
        for i in range(len(b)):
            trial=tuple(v+dt*sum(A[i,k]*ks[k][part] for k in range(i) if A[i,k]!=0) for part,v in enumerate(state))
            ks.append(paper_ale_rhs(trial,sol,(j+c[i])*dt));calls+=1
        state=tuple(v+dt*sum(b[k]*ks[k][part] for k in range(len(b)) if b[k]!=0) for part,v in enumerate(state))
        _,rr,_,_=ale.unpack(state,sol,(j+1)*dt,float(state[0][0]),float(state[0][-1]))
        min_h=min(min_h,float(np.min(np.diff(state[0]))));min_rho=min(min_rho,float(np.min(rr)))
        for t in TIMES:
            if j+1==round(t/dt):save(t)
    profile=OUT/'profiles'/(eng.case_key(spec)+'.npz');profile.parent.mkdir(parents=True,exist_ok=True)
    np.savez_compressed(profile,**arrays)
    return dict(status='completed',profile=str(profile),min_h=min_h,min_rho=min_rho,initial_state_sha256=init_hash,rhs_calls=calls)

def main():
    OUT.mkdir(parents=True,exist_ok=True);eng.OUT=OUT;eng.TIMES=(0.,.25,.5)
    plan={}
    for p in range(3,23):
        for route in SCHEMES.values():
            for method in METHODS:
                for n,dt in ((400,.003125),(200,.0125)):
                    for factor in ((1.,.5) if p in (5,12,22) else (1.,)):
                        s=dict(p=float(p),route=route,method=method,n=n,dt=dt*factor,halfwidth=4.,purpose='main' if factor==1 else 'time_half')
                        plan[eng.case_key(s)]=s
    sources=[HERE.parent/p for p in ('hs_table_data_20260927/out/results.json','hs_waveform_atlas_20260927/out/results.json','hs_error_theory_20260926/out_dynamic_mesh/results.json','hs_conserved_mesh_20260925/out/parameter_calibration/results.json')]
    hashes=eng.source_hashes();catalog={}
    for path in sources:
        d=json.loads(path.read_text(encoding='utf-8'))
        assert all(d['source_hashes'].get(k)==v for k,v in hashes.items())
        for key,r in d['rows'].items():
            if r['status']=='completed':catalog.setdefault(key,(path,r))
    frozen=dict(schemes=SCHEMES,plan=plan,source_hashes=hashes,driver_sha256=sha(__file__),engine_sha256=sha(eng.__file__),html_sha256=sha(ROOT/'numerical_analysis.html'),sources={str(p):sha(p) for p in sources})
    path=OUT/'results.json'
    saved=json.loads(path.read_text()) if path.exists() else {**frozen,'rows':{}}
    assert all(saved[k]==frozen[k] for k in ('plan','source_hashes','driver_sha256','engine_sha256'))
    eng.dump(OUT/'plan.json',frozen)
    for key,spec in plan.items():
        if key in saved['rows']:continue
        try:
            if key in catalog:
                source,r=catalog[key]
                assert all(r['spec'][k]==spec[k] for k in ('p','route','method','n','dt','halfwidth'))
                profile=Path(r['profile'])
                if not profile.is_absolute():profile=source.parent/profile
                if 'profile_sha256' in r:assert sha(profile)==r['profile_sha256']
                row=dict(status='completed',min_h=r['min_h'],min_rho=r['min_rho'],provenance='reused',source_results=str(source))
            else:
                r=run_paper_ale(spec) if spec['route']=='difference_paper_ale' else eng.run_one(spec)
                profile=Path(r['profile'])
                if not profile.is_absolute():profile=OUT/profile
                row={k:v for k,v in r.items() if k not in ('snapshots','profile')}
                row.update(provenance='new',source_results='')
            row.update(profile=str(profile.resolve()),profile_sha256=sha(profile),spec=spec,snapshots={})
            assert row['min_h']>0 and row['min_rho']>0
            with np.load(profile) as z:
                for t in TIMES:
                    data=tuple(z[f't{t}_{n}'] for n in ('x','u','rho_x','rho'))
                    assert all(np.all(np.isfinite(a)) for a in data)
                    assert all(np.all(np.diff(data[i])>0) for i in (0,2))
                    row['snapshots'][str(t)]={str(size):eng.measure(spec['p'],data,t,size)['core'] for size in (8001,16001,32001)}
        except Exception as exc:row=dict(spec=spec,status='failed',error=f'{type(exc).__name__}: {exc}')
        saved['rows'][key]=row;eng.dump(path,saved)
        if len(saved['rows'])%20==0 or row['status']=='failed':print(f"{len(saved['rows'])}/{len(plan)} {key}: {row['status']}",flush=True)
    export(saved)

def export(saved):
    rows=[];failed=[]
    for key,r in saved['rows'].items():
        spec=r['spec'];scheme=next(s for s,v in SCHEMES.items() if v==spec['route'])
        if r['status']!='completed':failed.append(dict(case_key=key,**r));continue
        for t in TIMES:
            size=16001 if spec['n']==400 else 8001
            e=r['snapshots'][str(t)][str(size)]
            rows.append(dict(case_key=key,scheme=scheme,**spec,t=t,evaluation_points=size,u_error=e['u'],rho_error=e['rho'],display=f"{e['u']:.3e} / {e['rho']:.3e}",profile=r['profile'],profile_sha256=r['profile_sha256'],provenance=r['provenance']))
    writecsv(OUT/'all_cells.csv',rows)
    for purpose in ('main','time_half'):
        subset=[r for r in rows if r['purpose']==purpose];writecsv(OUT/f'{purpose}_cells.csv',subset)
        groups={}
        for r in subset:
            cols=('p','method','n','dt','t','evaluation_points');key=tuple(r[k] for k in cols)
            g=groups.setdefault(key,{k:r[k] for k in cols});g[r['scheme']]=r['display']
        writecsv(OUT/f'{purpose}_wide.csv',list(groups.values()))
    comparisons=[]
    for r in rows:
        if r['scheme']!='S1':continue
        spec=r
        for num,den in (('S2','S1'),('S3','S4'),('S1','S3'),('S2','S3')):
            def value(s):
                k=eng.case_key({**spec,'route':SCHEMES[s]})
                return saved['rows'][k]['snapshots'][str(r['t'])][str(r['evaluation_points'])]
            a,b=value(num),value(den)
            comparisons.append({k:r[k] for k in ('p','method','n','dt','t','purpose')}|dict(comparison=f'{num}/{den}',u_ratio=a['u']/b['u'],rho_ratio=a['rho']/b['rho']))
    writecsv(OUT/'comparisons.csv',comparisons)
    summary=dict(runs=len(saved['rows']),failed=failed,new_runs=sum(r.get('provenance')=='new' for r in saved['rows'].values()),reused_runs=sum(r.get('provenance')=='reused' for r in saved['rows'].values()),main_cells=sum(r['purpose']=='main' for r in rows),time_half_cells=sum(r['purpose']=='time_half' for r in rows),html_unchanged=sha(ROOT/'numerical_analysis.html')==saved['html_sha256'])
    eng.dump(OUT/'summary.json',summary);print(json.dumps(summary,indent=2),flush=True)
    assert not failed and summary['html_unchanged']

if __name__=='__main__':main()
