"""Complete the defined S5/S6 experiments; never substitute models for S1-S4."""
import csv
import hashlib
import json
import sys
from pathlib import Path
import numpy as np
from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE.parent/'hs_error_theory_20260926'))
import run_designed_cases as eng

OUT = HERE/'out'
METHODS = ('euler','heun','rk4','rk8')
ROUTES = {'S5':'difference_rm','S6':'difference_fixed'}
PS = tuple(range(3,23))
TABLE_PS = (3,4,5,6,8,10,11,12,14,16,18,20,22)
TIMES = (.25,.5)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def writecsv(path, rows):
    with path.open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    eng.OUT=OUT
    eng.TIMES=(0.,.25,.5)
    plan={}
    for p in PS:
        for route in ROUTES.values():
            for method in METHODS:
                for n,dt in ((400,.003125),(200,.0125)):
                    for factor in ((1, .5) if p in (5,12,22) else (1,)):
                        spec=dict(p=float(p),route=route,method=method,n=n,dt=dt*factor,halfwidth=4.,purpose='main' if factor==1 else 'time_half')
                        plan[eng.case_key(spec)]=spec
    hashes=eng.source_hashes()
    sources=[HERE.parent/'hs_waveform_atlas_20260927/out/results.json',
             HERE.parent/'hs_error_theory_20260926/out_dynamic_mesh/results.json',
             HERE.parent/'hs_conserved_mesh_20260925/out/parameter_calibration/results.json']
    catalog={}
    for source in sources:
        d=json.loads(source.read_text(encoding='utf-8'))
        assert all(d['source_hashes'].get(k)==v for k,v in hashes.items())
        for key,row in d['rows'].items():
            if row['status']=='completed': catalog.setdefault(key,(source,row))
    frozen=dict(plan=plan,source_hashes=hashes,driver_sha256=sha(__file__),
                html_sha256=sha(ROOT/'numerical_analysis.html'),
                source_results_sha256={str(s):sha(s) for s in sources})
    eng.dump(OUT/'plan.json',frozen)
    dest=OUT/'results.json'
    saved=json.loads(dest.read_text(encoding='utf-8')) if dest.exists() else {**frozen,'rows':{}}
    assert saved['plan']==plan and saved['source_hashes']==hashes
    for key,spec in plan.items():
        if key in saved['rows']: continue
        try:
            if key in catalog:
                source,r=catalog[key]
                assert all(r['spec'][k]==spec[k] for k in ('p','route','method','n','dt','halfwidth'))
                profile=Path(r['profile'])
                if not profile.is_absolute(): profile=source.parent/profile
                if 'profile_sha256' in r: assert sha(profile)==r['profile_sha256']
                row=dict(status='completed',profile=str(profile.resolve()),profile_sha256=sha(profile),
                         min_h=r['min_h'],min_rho=r['min_rho'],provenance='reused',source_results=str(source))
            else:
                r=eng.run_one(spec)
                profile=OUT/r['profile']
                row={**r,'profile':str(profile.resolve()),'profile_sha256':sha(profile),'provenance':'new','source_results':''}
            assert row['min_h']>0 and row['min_rho']>0
            # Independently read saved fields and evaluate all three sample grids.
            row['snapshots']={}
            with np.load(profile) as z:
                for t in TIMES:
                    data=tuple(z[f't{t}_{name}'] for name in ('x','u','rho_x','rho'))
                    assert all(np.all(np.isfinite(v)) for v in data)
                    assert np.all(np.diff(data[0])>0) and np.all(np.diff(data[2])>0)
                    row['snapshots'][str(t)]={str(size):eng.measure(spec['p'],data,t,size)['core'] for size in (8001,16001,32001)}
            row['spec']=spec
        except Exception as exc:
            row=dict(spec=spec,status='failed',error=f'{type(exc).__name__}: {exc}')
        saved['rows'][key]=row
        eng.dump(dest,saved)
        if len(saved['rows'])%10==0 or row['status']=='failed':print(f"{len(saved['rows'])}/{len(plan)} {key} {row['status']}",flush=True)
    assert all(r['status']=='completed' for r in saved['rows'].values())
    export(saved)

def export(saved):
    def cell(section,p,t,method,n,dt,scheme,size,table=''):
        c=dict(section=section,table=table,p=p,t=t,method=method,N=n,dt=dt,evaluation_points=size,scheme=scheme,status='model_not_constructed',u_error=None,rho_error=None,display='—',case_key='',profile='',profile_sha256='')
        if scheme in ROUTES:
            key=eng.case_key(dict(p=p,route=ROUTES[scheme],method=method,n=n,dt=dt,halfwidth=4.))
            r=saved['rows'][key];e=r['snapshots'][str(t)][str(size)]
            c.update(status='completed',u_error=e['u'],rho_error=e['rho'],display=f"{e['u']:.3e} / {e['rho']:.3e}",case_key=key,profile=r['profile'],profile_sha256=r['profile_sha256'])
        return c
    configs=[(5,'2.1',None,.5,'rk4',400,.003125,16001),
             (6,'2.1',None,.25,'euler',400,.003125,16001),
             (7,'2.1',None,.5,'euler',400,.003125,16001),
             (8,'2.1',None,.25,'rk4',400,.003125,16001),
             (11,'2.2',12,.25,None,200,.0125,8001),
             (12,'2.2',5,.25,None,200,.0125,8001),
             (13,'2.2',5,.5,None,200,.0125,8001),
             (14,'2.2',12,.5,None,200,.0125,8001)]
    cells=[];checks=[]
    tables=BeautifulSoup((ROOT/'numerical_analysis.html').read_text(encoding='utf-8'),'html.parser').find_all('table')
    for ti,sec,p,t,method,n,dt,size in configs:
        trs=tables[ti].find_all('tr')[1:]
        for pp in (TABLE_PS if p is None else (p,)):
            for mm in (METHODS if method is None else (method,)):
                for si in range(1,7):
                    scheme=f'S{si}';c=cell(sec,pp,t,mm,n,dt,scheme,size,f'html_table_{ti}')
                    cells.append(c)
                    rr=TABLE_PS.index(pp) if sec=='2.1' else si-1
                    cc=si if sec=='2.1' else METHODS.index(mm)+1
                    old=trs[rr].find_all(['td','th'])[cc].get_text(' ',strip=True)
                    if si>=5:
                        vals=[float(v.strip()) for v in old.split('/')]
                        for field,val in zip(('u','rho'),vals):
                            calc=c[f'{field}_error'];tol=.50001*10**(np.floor(np.log10(abs(val)))-3)
                            checks.append(dict(table=ti,p=pp,t=t,method=mm,scheme=scheme,field=field,html=val,recomputed=calc,passes_rounding=bool(abs(calc-val)<=tol)))
    writecsv(OUT/'html_cells.csv',cells)
    expanded=[];controls=[]
    for p in PS:
        for n,dt,size,sec in ((400,.003125,16001,'2.1_expanded'),(200,.0125,8001,'2.2_expanded')):
            for t in TIMES:
                for method in METHODS:
                    for si in range(1,7):expanded.append(cell(sec,p,t,method,n,dt,f'S{si}',size))
                    if p in (5,12,22):
                        for scheme in ROUTES:controls.append(cell('time_half',p,t,method,n,dt/2,scheme,size))
    writecsv(OUT/'expanded_cells.csv',expanded)
    writecsv(OUT/'time_half_cells.csv',controls)
    writecsv(OUT/'html_rounding_checks.csv',checks)
    metrics=[]
    for key,r in saved['rows'].items():
        for t in TIMES:
            for size in (8001,16001,32001):
                metrics.append(dict(case_key=key,**r['spec'],t=t,evaluation_points=size,**r['snapshots'][str(t)][str(size)],profile=r['profile'],profile_sha256=r['profile_sha256']))
    writecsv(OUT/'all_errors.csv',metrics)
    counts={}
    flips=[];evalchanges=[]
    for n,dt,size in ((400,.003125,16001),(200,.0125,8001)):
        for method in METHODS:
            for t in TIMES:
                count={'u':0,'rho':0}
                for p in PS:
                    es=[cell('',p,t,method,n,dt,s,size) for s in ROUTES]
                    for field in count:count[field]+=int(es[0][field+'_error']<es[1][field+'_error'])
                    if p in (5,12,22):
                        half=[cell('',p,t,method,n,dt/2,s,size) for s in ROUTES]
                        for field in count:
                            f=field+'_error'
                            if (es[0][f]<es[1][f])!=(half[0][f]<half[1][f]):flips.append(dict(p=p,n=n,method=method,t=t,field=field))
                counts[f'N{n}_{method}_t{t}']=count
    for key,r in saved['rows'].items():
        for t in TIMES:
            e=r['snapshots'][str(t)]
            for f in ('u','rho'):evalchanges.append(abs(e['32001'][f]/e['16001'][f]-1))
    summary=dict(runs=len(saved['rows']),new_runs=sum(r['provenance']=='new' for r in saved['rows'].values()),
                 reused_runs=sum(r['provenance']=='reused' for r in saved['rows'].values()),
                 html_cells=len(cells),html_numeric_cells=sum(c['status']=='completed' for c in cells),
                 html_undefined_cells=sum(c['status']!='completed' for c in cells),
                 expanded_numeric_cells=sum(c['status']=='completed' for c in expanded),
                 html_rounding_passes=sum(c['passes_rounding'] for c in checks),html_rounding_checks=len(checks),
                 s5_better_counts_out_of_20=counts,time_half_ranking_flips=flips,
                 max_relative_eval16001_to32001=max(evalchanges),
                 html_unchanged=sha(ROOT/'numerical_analysis.html')==saved['html_sha256'])
    eng.dump(OUT/'summary.json',summary)
    print(json.dumps(summary,indent=2),flush=True)
    assert summary['html_unchanged']

if __name__=='__main__':main()
