"""Prospective error-budget decisions on held-out one-soliton parameters.

The SD budget uses its own finite-h exact Gram solution. FD is only compared
to the common continuous solution or to a same-h, finer FD trajectory.
"""
from pathlib import Path
import sys, json, hashlib, time
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'lib'))
from parametric import Parameters, Exact, rk4
from parametric_open import OpenModel
from parametric_open_bounds import sharp

OUT=ROOT/'out/route2'
OUT.mkdir(parents=True,exist_ok=True)
CASES={'P1':Parameters(), 'P6':Parameters(p=1,q=3,rho=4),
       'P10':Parameters(a=2,p=1.5,q=2,rho=3.5)}


def inf(a):return float(np.max(np.abs(a)))


def advance(m,T=.01,dt=.000125):
    z=m.exact(0);n=round(T/dt);assert abs(n*dt-T)<1e-12
    start=time.perf_counter()
    for i in range(n):
        z=rk4(m.rhs,i*dt,z,dt)
        if not np.all(np.isfinite(z)) or inf(z)>1e3:
            raise RuntimeError(f'run stopped: {m.pars}, {m.h}, {m.X.n}, {m.model}, step {i}')
    return z,time.perf_counter()-start


def sampled_defect(m,T=.01):
    rows=[]
    for t in (0.,T/2,T):
        exact=m.exact(t)
        r=m.rhs(t,exact)-m.exact(t,True)
        K,C=sharp(m)
        rows.append({'t':t,'state_defect':inf(r),'K_at_t0':K,'C':C})
    return rows


def run(case,h,nx,model='structure',initial='finite',dt=.000125):
    pars=CASES[case]
    m=OpenModel(pars,h,nx,model=model,continuous=(initial=='continuous'))
    z,seconds=advance(m,dt=dt)
    t=.01
    num=m.fields(z,t)
    finite=Exact(pars,h).uv(m.js,m.X.x,t)
    cont=Exact(pars,h,continuous=True).uv(m.js,m.X.x,t)
    parts={}
    for i,f in enumerate(('u','v')):
        if initial=='finite':
            solver=num[i]-finite[i];model_error=finite[i]-cont[i]
            total=num[i]-cont[i]
            assert inf(total-solver-model_error)<2e-12
            parts[f]={'model':inf(model_error),'solver_vs_finite':inf(solver),
                      'total_vs_continuous':inf(total),
                      'dominance_ratio':inf(model_error)/max(inf(solver),1e-30)}
        else:
            parts[f]={'total_vs_continuous':inf(num[i]-cont[i])}
    cfg={'case':case,'h':h,'nx':nx,'model':model,'initial':initial,'dt':dt,'T':t}
    name='fields_'+hashlib.sha256(json.dumps(cfg,sort_keys=True).encode()).hexdigest()[:12]+'.npz'
    np.savez_compressed(OUT/name,x=m.X.x,y=m.y,u=num[0],v=num[1],
                        finite_u=finite[0],finite_v=finite[1],
                        continuous_u=cont[0],continuous_v=cont[1])
    return {'config':cfg,'errors':parts,'seconds':seconds,'field_file':name,
            'sampled_defect':sampled_defect(m) if initial=='finite' else None}


def find(rows,case,h,nx,model='structure',initial='finite'):
    return next(r for r in rows if all(r['config'][k]==v for k,v in
        [('case',case),('h',h),('nx',nx),('model',model),('initial',initial)]))


def prospective(rows):
    out=[]
    for case in CASES:
        pilot=find(rows,case,.25,256)
        for f in ('u','v'):
            C=pilot['errors'][f]['model']/.25**2
            floor=pilot['errors'][f]['solver_vs_finite']
            hbal=float(np.sqrt(floor/C))
            tests=[]
            for h in (.125,.0625):
                r=find(rows,case,h,256)
                obs=r['errors'][f]
                predicted_ratio=C*h*h/floor
                tests.append({'h':h,'predicted_model_to_pilot_solver':predicted_ratio,
                              'observed_model_to_solver':obs['dominance_ratio'],
                              'observed_total':obs['total_vs_continuous'],
                              'observed_solver':obs['solver_vs_finite']})
            out.append({'case':case,'field':f,'pilot_C':C,'pilot_solver':floor,
                        'predicted_h_balance':hbal,'held_out_h':tests})
    return out


def fd_same_model(rows):
    out=[]
    for case in ('P6','P10'):
        coarse=find(rows,case,.125,256,'fd','continuous')
        fine=next(r for r in rows if r['config']['case']==case and
                  r['config']['h']==.125 and r['config']['nx']==512 and
                  r['config']['model']=='fd' and r['config']['dt']==.0000625)
        fine_full=next(r for r in rows if r['config']['case']==case and
                       r['config']['h']==.125 and r['config']['nx']==512 and
                       r['config']['model']=='fd' and r['config']['dt']==.000125)
        a=np.load(OUT/coarse['field_file']);b=np.load(OUT/fine['field_file'])
        c=np.load(OUT/fine_full['field_file'])
        assert np.max(abs(a['x']-b['x'][::2]))<1e-12
        assert np.max(abs(a['y']-b['y']))<1e-12
        out.append({'case':case,'h':.125,'coarse_nx':256,'fine_nx':512,
                    'same_h_fd_coarse_minus_fine':{f:inf(a[f]-b[f][:,::2]) for f in ('u','v')},
                    'fine_dt_halving':{f:inf(b[f]-c[f]) for f in ('u','v')},
                    'fine_vs_continuous':fine['errors']})
    return out


def main():
    rows=[]
    # Pilot h=.25, nx=256; held-out h and x checks are never used to fit it.
    for case in CASES:
        for h in (.25,.125,.0625):
            row=run(case,h,256)
            rows.append(row)
            print('SD budget',case,h,row['errors'],flush=True)
        for nx in (128,512):
            row=run(case,.0625,nx)
            rows.append(row)
            print('x check',case,nx,row['errors'],flush=True)
        for model in ('structure','fd'):
            row=run(case,.125,256,model,'continuous')
            rows.append(row)
            print('common continuous',case,model,row['errors'],flush=True)
    for case in ('P6','P10'):
        for dt in (.000125,.0000625):
            row=run(case,.125,512,'fd','continuous',dt=dt)
            rows.append(row)
            print('FD same-model fine',case,dt,row['errors'],flush=True)
    decisions=prospective(rows)
    same_model=fd_same_model(rows)
    paths=[Path(__file__),ROOT/'lib/parametric.py',ROOT/'lib/parametric_open.py',
           ROOT/'experiments/parametric_open_bounds.py']
    data={'scope':'fixed L=20,yhalf=1.5, extrapolated open boundary, T=.01',
          'cases':{k:vars(v) for k,v in CASES.items()},'runs':rows,
          'prospective_balances':decisions,'fd_same_h_fine_reference':same_model,
          'sources_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}
    (OUT/'budget.json').write_text(json.dumps(data,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print('wrote route2/budget.json',flush=True)


if __name__=='__main__':main()
