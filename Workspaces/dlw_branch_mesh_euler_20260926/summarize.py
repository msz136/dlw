"""Read back saved fields, audit evidence and generate comparison data."""
from pathlib import Path
import csv,json
import numpy as np
from scipy.interpolate import make_interp_spline
from model import BranchProblem,evaluate
from run import CASES,OUT,sha,dump
from supplement import high_band

HERE=Path(__file__).resolve().parent
PHASES=('main','time_half','space_x','space_y','supplement')

def main():
    docs={name:json.loads((OUT/(name+'.json')).read_text(encoding='utf-8')) for name in PHASES}
    rows={k:r for d in docs.values() for k,r in d['rows'].items()}
    audit=dict(counts={},source_hashes_verified=True,profiles_verified=0,error_readback_max=0.,
               field_readback_max=0.,same_fd_sd_initial_hashes=True,
               evaluation_max_relative_change=0.,reconstruction_max_relative_change=0.,
               main_seventh_spline_max_relative_change=0.,main_max_initial_output_error=0.,
               failures=[],main_geometry={},sensitivity={},high_bands={})
    csvrows=[]
    for phase,d in docs.items():
        assert len(d['rows'])==len(d['plan']), f'{phase} unfinished'
        for path,hashed in d['source_hashes'].items():assert sha(path)==hashed,path
        audit['counts'][phase]={s:sum(r['status']==s for r in d['rows'].values()) for s in set(r['status'] for r in d['rows'].values())}
    for key,r in rows.items():
        spec=r['spec']
        if r['status']!='completed':
            audit['failures'].append(dict(key=key,failure=r.get('failure',r.get('error'))))
        if 'profile' not in r:continue
        path=OUT/r['profile'];assert sha(path)==r['profile_sha256'],key
        audit['profiles_verified']+=1;a=np.load(path)
        p=BranchProblem(CASES[spec['case']],**{k:spec[k] for k in ('route','branch','h','nx','L','yhalf')})
        for ts,snap in r['snapshots'].items():
            t=float(ts);z,s=a[f't{ts}_z'],a[f't{ts}_s']
            e=evaluate(p,z,s,t)
            if f't{ts}_u' in a:
                uv=p.m.fields(z,t)
                audit['field_readback_max']=max(audit['field_readback_max'],*(float(np.max(abs(uv[i]-a[f't{ts}_{f}']))) for i,f in enumerate(('u','v'))))
            for f in ('u','v'):
                audit['error_readback_max']=max(audit['error_readback_max'],abs(e[f]-snap['errors'][f]))
                audit['evaluation_max_relative_change']=max(audit['evaluation_max_relative_change'],abs(snap['evaluation_double'][f]/e[f]-1))
                audit['reconstruction_max_relative_change']=max(audit['reconstruction_max_relative_change'],abs(snap['reconstruction_double'][f]/e[f]-1))
            csvrows.append(dict(key=key,case=spec['case'],route=spec['route'],branch=spec['branch'],phase=spec['phase'],
                status=r['status'],h=spec['h'],nx=spec['nx'],dt=spec['dt'],t=t,E_u=e['u'],E_v=e['v']))
            if spec['phase'] in ('main','space_x') and t==.01:
                audit['high_bands'][key]=high_band(p,z,s,t)
            if spec['phase']=='main':
                # Independent high-order interpolation directly in physical x.
                xx=-20+np.arange(p.X.n*4)*40/(p.X.n*4);xx=xx[(xx>=-10)&(xx<10)]
                my=abs(p.m.y)<1.5
                ref=p.m.G.uv(p.m.js[my],xx,t)
                for i,f in enumerate(('u','v')):
                    other=make_interp_spline(p.X.x,a[f't{ts}_{f}'][my],k=7,axis=-1)(xx)
                    err=float(np.max(abs(other-ref[i])))
                    audit['main_seventh_spline_max_relative_change']=max(audit['main_seventh_spline_max_relative_change'],abs(err/e[f]-1))
    assert audit['error_readback_max']<1e-14 and audit['field_readback_max']<1e-14
    for phase in ('main','time_half','space_x','space_y'):
        for r in docs[phase]['rows'].values():
            if r['status']!='completed' or r['spec']['route']!='fd':continue
            spec=r['spec'];other=docs[phase]['rows'][f'{spec["case"]}_sd_{spec["branch"]}_{phase}']
            if other['status']=='completed':assert r['initial_hash']==other['initial_hash']

    def get(case,route,branch,phase,t='.01'):
        rr=rows[f'{case}_{route}_{branch}_{phase}']
        return rr.get('snapshots',{}).get(str(float(t)),{}).get('errors')

    def comparison(phase,cases):
        result=[]
        for case in cases:
            for route in ('fd','sd'):
                base=get(case,route,'fixed',phase)
                for branch in ('minus','plus'):
                    vals=get(case,route,branch,phase)
                    result.append(dict(case=case,route=route,branch=branch,
                        ratios=None if vals is None or base is None else {f:vals[f]/base[f] for f in ('u','v')}))
        return result
    audit['mesh_ratios']={phase:comparison(phase,cases) for phase,cases in [
        ('main',CASES),('time_half',CASES),('space_x',CASES),('space_y',['P1','P2','P6','P10']),
        ('fine_half',['P1','P2','P6','P10']),('fine_quarter',['P6']),('main_quarter',['P5'])]}
    for phase in ('time_half','space_x','space_y'):
        max_change=0.;mesh_flips=[];method_flips=[]
        for key,r in docs[phase]['rows'].items():
            if r['status']!='completed':continue
            spec=r['spec'];case,route,branch=spec['case'],spec['route'],spec['branch']
            for t in (.005,.01):
                base=get(case,route,branch,'main',t);vals=get(case,route,branch,phase,t)
                max_change=max(max_change,*(abs(vals[f]/base[f]-1) for f in ('u','v')))
            for f in ('u','v'):
                if branch!='fixed':
                    before=get(case,route,branch,'main')[f]<get(case,route,'fixed','main')[f]
                    after=get(case,route,branch,phase)[f]<get(case,route,'fixed',phase)[f]
                    if before!=after:mesh_flips.append(dict(case=case,route=route,branch=branch,field=f))
                if route=='sd' and get(case,'fd',branch,phase) is not None:
                    before=get(case,'sd',branch,'main')[f]<get(case,'fd',branch,'main')[f]
                    after=get(case,'sd',branch,phase)[f]<get(case,'fd',branch,phase)[f]
                    if before!=after:method_flips.append(dict(case=case,branch=branch,field=f))
        audit['sensitivity'][phase]=dict(max_relative_error_change=max_change,mesh_benefit_flips=mesh_flips,sd_fd_flips=method_flips)
    mainrows=list(docs['main']['rows'].values());moving=[r for r in mainrows if r['spec']['branch']!='fixed']
    audit['main_geometry']=dict(minimum_J=min(r['minimum_J'] for r in mainrows),
        minimum_R=min(g['min_R'] for r in moving for g in r['geometry']),
        max_relative_mass_drift=max(abs(g['mass']/r['geometry'][0]['mass']-1) for r in moving for g in r['geometry']),
        max_equidistribution_defect=max(g['relative_equidistribution_defect'] for r in moving for g in r['geometry']),
        every_moving_step_verified=all(r['steps_with_nonzero_mesh_velocity']==r['steps'] for r in moving),
        max_endpoint_mismatch=max(r['reference_endpoint_field_and_time_derivative_mismatch'] for r in mainrows),
        conservation_residuals={route:max(g['physical_conservation_residual'] for r in moving if r['spec']['route']==route for g in r['geometry']) for route in ('fd','sd')},
        displacement_range=[min(r['max_displacement_since_initial'] for r in moving),max(r['max_displacement_since_initial'] for r in moving)])
    audit['main_max_initial_output_error']=max(e for r in mainrows for e in r['initial_output_error'].values())
    # Count classification changes when the common physical evaluation grid is doubled.
    evaluation_flips=[]
    for case in CASES:
        for route in ('fd','sd'):
            fixed=docs['main']['rows'][f'{case}_{route}_fixed_main']['snapshots']['0.01']
            for branch in ('minus','plus'):
                r=docs['main']['rows'][f'{case}_{route}_{branch}_main']['snapshots']['0.01']
                for f in ('u','v'):
                    if (r['errors'][f]<fixed['errors'][f])!=(r['evaluation_double'][f]<fixed['evaluation_double'][f]):
                        evaluation_flips.append([case,route,branch,f])
    audit['main_evaluation_mesh_benefit_flips']=evaluation_flips
    dump(OUT/'summary.json',audit)
    with (OUT/'errors.csv').open('w',newline='',encoding='utf-8-sig') as file:
        w=csv.DictWriter(file,fieldnames=list(csvrows[0]));w.writeheader();w.writerows(csvrows)
    print(json.dumps({k:v for k,v in audit.items() if k not in ('mesh_ratios','high_bands','sensitivity')},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
