"""Recompute source/propagator attribution and closure from saved field arrays."""
from pathlib import Path
import csv,json
import numpy as np

HERE=Path(__file__).resolve().parent

def metrics(a,b):
    norm=np.linalg.norm(b)
    return dict(relative_residual=float(np.linalg.norm(a-b)/norm),
                norm_ratio=float(np.linalg.norm(a)/norm),
                cosine=float(np.vdot(a,b)/(np.linalg.norm(a)*norm)))

def rms(a):
    return float(np.sqrt(np.mean(a*a,axis=(-2,-1)).sum()))

def dump(path,rows):
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for r in rows for k in r)))
        w.writeheader();w.writerows(rows)

def run():
    rows=[];checks=[];budgets=[];controls=[]
    c_tag='C_T0.010_dt0.000100_parts_cache5'
    if not (HERE/c_tag/'validation.json').exists():c_tag='C_T0.010_dt0.000500_parts_cache5'
    tags=['A_T0.010_dt0.000100_parts','A_T0.040_dt0.000100',c_tag]
    for tag in tags:
        path=HERE/tag
        if not (path/'validation.json').exists():continue
        record=json.loads((path/'validation.json').read_text())
        for kind,value in record.get('regression_against_original_time_step',{}).items():
            controls.append(dict(case=record['case'],t=record['config']['T'],label='archive_'+kind,
                dt=record['config']['dt'],**value,passed=value['relative_residual']<.001))
        n=round(record['config']['T']/record['config']['dt'])
        with np.load(path/f'frame_{n:05d}.npz') as z:
            E={(p,s):z[f'{p}_from_{s}'] for p in ('SD','FD') for s in ('SD','FD')}
            for kind in ('SD','FD'):
                actual=z['actual_'+kind]
                closure=metrics(E[kind,kind],actual)
                checks.append(dict(tag=tag,kind=kind,check='independent_error_closure',**closure,passed=closure['relative_residual']<.05))
                if record['parts']:
                    parts={name:z[f'{kind}_part_{name}'] for name in ('y_model','x_stencil','x_wrap')}
                    total=sum(parts.values())
                    closure=metrics(total,actual)
                    checks.append(dict(tag=tag,kind=kind,check='independent_three_source_closure',**closure,passed=closure['relative_residual']<.05))
                    for field,sl in [('joint',slice(None)),('u',slice(0,1)),('v',slice(1,2))]:
                        y=parts['y_model'][sl];x=parts['x_stencil'][sl];w=parts['x_wrap'][sl]
                        a=total[sl]; norm2=float(np.vdot(a,a))
                        y2=float(np.vdot(y,y));x2=float(np.vdot(x,x));cross=float(2*np.vdot(x,y))
                        wrap=float(np.vdot(w,w)+2*np.vdot(w,x+y))
                        budgets.append(dict(tag=tag,kind=kind,field=field,y_rms=rms(y),x_rms=rms(x),wrap_rms=rms(w),
                            total_rms=rms(a),cosine_y_x=float(np.vdot(x,y)/np.sqrt(x2*y2)),
                            energy_y_fraction=y2/norm2,energy_x_fraction=x2/norm2,
                            energy_cross_fraction=cross/norm2,energy_wrap_fraction=wrap/norm2,
                            energy_identity_relative_residual=abs(y2+x2+cross+wrap-norm2)/norm2))
            # Symmetric 2x2 factorial effects. No unexplained regression fit.
            source=.5*((E['SD','SD']-E['SD','FD'])+(E['FD','SD']-E['FD','FD']))
            prop=.5*((E['SD','SD']-E['FD','SD'])+(E['SD','FD']-E['FD','FD']))
            gap=E['SD','SD']-E['FD','FD'];g2=float(np.vdot(gap,gap))
            gap_check=metrics(gap,z['actual_SD']-z['actual_FD'])
            checks.append(dict(tag=tag,kind='SD_minus_FD',check='between_method_gap_closure',**gap_check,passed=gap_check['relative_residual']<.05))
            for field,sl in [('joint',slice(None)),('u',slice(0,1)),('v',slice(1,2))]:
                M={key:rms(val[sl]) for key,val in E.items()}
                es=.5*((M['SD','SD']-M['SD','FD'])+(M['FD','SD']-M['FD','FD']))
                ep=.5*((M['SD','SD']-M['FD','SD'])+(M['SD','FD']-M['FD','FD']))
                denominator=M['SD','SD']-M['FD','FD']
                gs=gap[sl];g2=float(np.vdot(gs,gs))
                rows.append(dict(tag=tag,field=field,SD_from_SD=M['SD','SD'],SD_from_FD=M['SD','FD'],
                    FD_from_SD=M['FD','SD'],FD_from_FD=M['FD','FD'],rms_gap=denominator,
                    source_rms_gap_effect=es,propagation_rms_gap_effect=ep,
                    source_rms_gap_fraction=es/denominator,propagation_rms_gap_fraction=ep/denominator,
                    source_field_gap_projection_fraction=float(np.vdot(source[sl],gs)/g2),
                    propagation_field_gap_projection_fraction=float(np.vdot(prop[sl],gs)/g2),
                    field_additive_identity_relative_residual=float(np.linalg.norm(source[sl]+prop[sl]-gs)/np.linalg.norm(gs))))
    base=HERE/'A_T0.040_dt0.000100'
    half=HERE/'A_T0.040_dt0.000050'
    if (half/'validation.json').exists():
        with np.load(base/'frame_00400.npz') as b,np.load(half/'frame_00800.npz') as h:
            for kind in ('SD','FD'):
                for label in (f'actual_{kind}',f'{kind}_from_{kind}'):
                    result=metrics(b[label],h[label])
                    controls.append(dict(case='A',t=.04,label=label,**result,passed=result['relative_residual']<.01))
    fine_c=HERE/'C_T0.010_dt0.000100_parts_cache5'/'frame_00020.npz'
    coarse_c=HERE/'C_T0.010_dt0.000500_parts_cache5'/'frame_00004.npz'
    if fine_c.exists() and coarse_c.exists():
        with np.load(fine_c) as f,np.load(coarse_c) as c:
            for label in ('actual_SD','actual_FD','SD_from_SD','SD_from_FD','FD_from_SD','FD_from_FD',
                          'SD_part_y_model','SD_part_x_stencil','FD_part_y_model','FD_part_x_stencil'):
                result=metrics(c[label],f[label])
                controls.append(dict(case='C',t=.002,label='coarse_fine_'+label,dt=.0005,
                    **result,passed=result['relative_residual']<.001))
    dump(HERE/'cross_source_attribution.csv',rows);dump(HERE/'transported_source_budget.csv',budgets)
    dump(HERE/'independent_closure.csv',checks)
    if controls:dump(HERE/'time_refinement_validation.csv',controls)
    out=dict(completed_tags=[r['tag'] for r in rows if r['field']=='joint'],
        checks=checks,time_refinement=controls,all_completed_checks_passed=all(r['passed'] for r in checks+controls),
        attribution=rows,source_budgets=budgets)
    (HERE/'analysis_validation.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps(out,indent=2))

if __name__=='__main__':run()
