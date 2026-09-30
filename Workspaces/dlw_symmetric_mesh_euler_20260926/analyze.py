"""Audit new runs and matched frozen comparators, keeping all failures visible."""
from pathlib import Path
import csv,json
import numpy as np
from scipy.interpolate import make_interp_spline
from sym_model import SymmetricProblem,BASE,evaluate
from experiment import OUT,CASES,sha,dump

HERE=Path(__file__).resolve().parent

def load_rows():
    d=json.loads((OUT/'results.json').read_text(encoding='utf-8'))
    olddocs={n:json.loads((BASE/'out'/f'{n}.json').read_text(encoding='utf-8')) for n in ('main','time_half','space_x','space_y','supplement')}
    old={k:r for dd in olddocs.values() for k,r in dd['rows'].items()}
    return d,olddocs,old

def main():
    d,olddocs,old=load_rows();assert len(d['rows'])==len(d['plan'])
    rows={**old,**d['rows']}
    def record(case,route,branch,phase):return rows.get(f'{case}_{route}_{branch}_{phase}')
    def error(case,route,branch,phase,t=.01,metric='errors'):
        r=record(case,route,branch,phase)
        return None if r is None else r.get('snapshots',{}).get(str(t),{}).get(metric)
    audit=dict(new_counts={},new_profiles_verified=0,reused_profiles_verified=0,source_hashes_verified=True,
        error_readback_max=0.,field_readback_max=0.,same_fd_sd_initial_hashes=True,
        main_evaluation_change=0.,main_reconstruction_change=0.,all_evaluation_change=0.,
        all_reconstruction_change=0.,main_seventh_spline_change=0.,initial_output_error=0.,
        initial_output_fraction=0.,failures=[],ratios={},classifications={},sensitivity={},geometry={})
    for path,hh in d['source_hashes'].items():assert sha(path)==hh,path
    for path,hh in d['comparison_manifests'].items():assert sha(path)==hh,path
    for dd in olddocs.values():
        for path,hh in dd['source_hashes'].items():assert sha(path)==hh,path
    for key,r in old.items():
        if 'profile' in r:
            assert sha(BASE/'out'/r['profile'])==r['profile_sha256'],key
            audit['reused_profiles_verified']+=1
    csvrows=[]
    for key,r in d['rows'].items():
        spec=r['spec'];phase=spec['phase'];route=spec['route'];case=spec['case']
        audit['new_counts'].setdefault(phase,{})[r['status']]=audit['new_counts'].setdefault(phase,{}).get(r['status'],0)+1
        if r['status']!='completed':audit['failures'].append(dict(key=key,failure=r.get('failure',r.get('error'))))
        assert 'profile' in r, (key,'no partial state retained')
        assert sha(OUT/r['profile'])==r['profile_sha256'],key
        audit['new_profiles_verified']+=1;a=np.load(OUT/r['profile'])
        p=SymmetricProblem(CASES[case],**{k:spec[k] for k in ('route','branch','h','nx','L','yhalf')})
        if route=='sd':assert record(case,'fd','symmetric',phase)['initial_hash']==r['initial_hash']
        for ts,snap in r['snapshots'].items():
            t=float(ts);z,s=a[f't{ts}_z'],a[f't{ts}_s'];e=evaluate(p,z,s,t)
            uv=p.m.fields(z,t)
            for i,f in enumerate(('u','v')):
                audit['error_readback_max']=max(audit['error_readback_max'],abs(e[f]-snap['errors'][f]))
                audit['field_readback_max']=max(audit['field_readback_max'],float(np.max(abs(uv[i]-a[f't{ts}_{f}']))))
                ce=abs(snap['evaluation_double'][f]/e[f]-1);cr=abs(snap['reconstruction_double'][f]/e[f]-1)
                audit['all_evaluation_change']=max(audit['all_evaluation_change'],ce)
                audit['all_reconstruction_change']=max(audit['all_reconstruction_change'],cr)
                if phase=='main':
                    audit['main_evaluation_change']=max(audit['main_evaluation_change'],ce)
                    audit['main_reconstruction_change']=max(audit['main_reconstruction_change'],cr)
            csvrows.append(dict(case=case,route=route,phase=phase,status=r['status'],t=t,
                nx=spec['nx'],h=spec['h'],dt=spec['dt'],E_u=e['u'],E_v=e['v']))
            if phase=='main':
                xx=-20+np.arange(p.X.n*4)*40/(p.X.n*4);xx=xx[(xx>=-10)&(xx<10)]
                my=abs(p.m.y)<1.5;ref=p.m.G.uv(p.m.js[my],xx,t)
                for i,f in enumerate(('u','v')):
                    other=make_interp_spline(p.X.x,uv[i][my],k=7,axis=-1)(xx)
                    oe=float(np.max(abs(other-ref[i])))
                    audit['main_seventh_spline_change']=max(audit['main_seventh_spline_change'],abs(oe/e[f]-1))
                    audit['initial_output_fraction']=max(audit['initial_output_fraction'],r['initial_output_error'][f]/e[f])
                audit['initial_output_error']=max(audit['initial_output_error'],*r['initial_output_error'].values())
        # Record all paired comparisons. Failed trajectories are never assigned a finite T=.01 error.
        for b in ('fixed','minus','plus'):
            base=record(case,route,b,phase)
            if base is None:continue
            for k in ('h','nx','L','yhalf','dt','T'):assert spec[k]==base['spec'][k],(key,b,k)
            se=error(case,route,'symmetric',phase);be=error(case,route,b,phase)
            audit['ratios'].setdefault(key,{})[b]=None if se is None or be is None else {f:se[f]/be[f] for f in ('u','v')}

    assert audit['error_readback_max']<1e-14 and audit['field_readback_max']<1e-14
    for phase in ('main','time_half','space_x','space_y','fine_half','fine_quarter','main_quarter'):
        for route in ('fd','sd'):
            cases=[s['case'] for s in d['plan'].values() if s['phase']==phase and s['route']==route]
            if not cases:continue
            cl={b:[] for b in ('fixed','minus','plus','both_branches')};unavailable=[]
            for case in cases:
                ratios=audit['ratios'].get(f'{case}_{route}_symmetric_{phase}',{})
                for b in ('fixed','minus','plus'):
                    if ratios.get(b) is not None and max(ratios[b].values())<1:cl[b].append(case)
                if all(ratios.get(b) is not None and max(ratios[b].values())<1 for b in ('minus','plus')):cl['both_branches'].append(case)
                if error(case,route,'symmetric',phase) is None:unavailable.append(case)
            audit['classifications'][f'{phase}_{route}']=dict(cases=cases,double_field_better=cl,unavailable=unavailable)

    # Main conclusions are checked against a smaller Euler step and denser evaluation.
    for variant in ('time_half','evaluation_double'):
        flips=[];sd_fd_flips=[];max_change=0.
        for case in CASES:
            for route in ('fd','sd'):
                before=error(case,route,'symmetric','main')
                after=error(case,route,'symmetric','time_half') if variant=='time_half' else error(case,route,'symmetric','main',metric=variant)
                max_change=max(max_change,*(abs(after[f]/before[f]-1) for f in ('u','v')))
                for branch in ('fixed','minus','plus'):
                    b0=error(case,route,branch,'main')
                    b1=error(case,route,branch,'time_half') if variant=='time_half' else error(case,route,branch,'main',metric=variant)
                    for f in ('u','v'):
                        if (before[f]<b0[f])!=(after[f]<b1[f]):flips.append([case,route,branch,f])
            for f in ('u','v'):
                oldwin=error(case,'sd','symmetric','main')[f]<error(case,'fd','symmetric','main')[f]
                if variant=='time_half':newwin=error(case,'sd','symmetric','time_half')[f]<error(case,'fd','symmetric','time_half')[f]
                else:newwin=error(case,'sd','symmetric','main',metric=variant)[f]<error(case,'fd','symmetric','main',metric=variant)[f]
                if oldwin!=newwin:sd_fd_flips.append([case,f])
        audit['sensitivity'][variant]=dict(max_change=max_change,comparison_flips=flips,sd_fd_flips=sd_fd_flips)

    mainrows=[r for r in d['rows'].values() if r['spec']['phase']=='main']
    audit['geometry']=dict(minimum_J=min(r['minimum_J'] for r in mainrows),minimum_R=min(r['minimum_R'] for r in mainrows),
        every_step_moving=all(r['steps_with_nonzero_mesh_velocity']==r['steps'] for r in mainrows),
        max_mass_drift=max(abs(tr['geometry']['mass']/r['traces'][0]['geometry']['mass']-1) for r in mainrows for tr in r['traces']),
        max_equidistribution_defect=max(tr['geometry']['relative_equidistribution_defect'] for r in mainrows for tr in r['traces']),
        conservation_residuals={route:max(tr['geometry']['physical_conservation_residual'] for r in mainrows if r['spec']['route']==route for tr in r['traces']) for route in ('fd','sd')},
        motion_range=[min(r['max_displacement_since_initial'] for r in mainrows),max(r['max_displacement_since_initial'] for r in mainrows)])
    dump(OUT/'summary.json',audit)
    with (OUT/'errors.csv').open('w',newline='',encoding='utf-8-sig') as file:
        w=csv.DictWriter(file,fieldnames=list(csvrows[0]));w.writeheader();w.writerows(csvrows)
    print(json.dumps({k:v for k,v in audit.items() if k not in ('ratios','classifications')},ensure_ascii=False,indent=2))
    print(json.dumps(audit['classifications'],ensure_ascii=False,indent=2))

if __name__=='__main__':main()
