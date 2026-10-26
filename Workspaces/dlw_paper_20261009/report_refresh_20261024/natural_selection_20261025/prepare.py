"""Select the natural Centered-SD of manuscript Section 3.2.

Reuse six saved RK4 trajectories; evaluate their initial vector fields and
independently check the physical-field equations with omega=h*w/4.
"""
from pathlib import Path
import importlib.util
import hashlib
import json
import sys
import numpy as np

HERE=Path(__file__).resolve().parent
BASE=HERE.parent
ROOT=BASE.parents[2]
NATURAL=BASE/'natural_edge_rk4_20261024'
PROBE=BASE.parent/'spatial_audit_20261023/separated/reconstruction_probe'
sys.path.insert(0,str(PROBE))
from probe import Model,fields,HALF_WIDTHS,transform
from rerun_20261024 import rhs,physical_rates
spec=importlib.util.spec_from_file_location('nondegenerate_reference_runner',BASE/'nondegenerate_rk4_20261024/run.py')
reference=importlib.util.module_from_spec(spec)
spec.loader.exec_module(reference)

def read(p):return json.loads(p.read_text(encoding='utf8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def measured(m,z,y):
    if m.case in 'ABCD':
        rad=HALF_WIDTHS[m.case]
        my=abs(y)<rad;mx=abs(m.x)<=rad
    else:
        my=abs(y)<=1.8+1e-12;mx=np.ones(len(m.x),dtype=bool)
    sub=abs(z[my][:,mx])
    iy,ix=np.unravel_index(np.argmax(sub),sub.shape)
    return float(sub[iy,ix]),[float(m.x[mx][ix]),float(y[my][iy])]

def prepare(case):
    old=read(NATURAL/f'{case}.json')
    artifact=ROOT/old['artifact']
    assert sha(artifact)==old['artifact_sha256']
    data=np.load(artifact)
    m=Model(case,'Centered-SD',.1,.1) if case in 'ABCD' else reference.NondegenerateModel(case,'Centered-SD')
    m.gauge='local'
    yv=(m.y[1:]+m.y[:-1])/2
    for key,array in [('x',m.x),('y',m.y),('yv',yv)]:
        assert np.array_equal(data[key],array)
    z0=data['z0'];u,w=z0;v=transform(m,u,w)
    dz=rhs(m,0,z0);ut,vt=physical_rates(m,z0,dz)
    omega=m.h*w/4
    # Independent assembly of manuscript Proposition 3.2, both physical rates.
    flux=u*u/2+2*m.a*u+omega*omega/2-m.h*omega
    rate_diff=-np.diff(m.d1(flux),axis=0)/m.h-m.d2(v)
    lower=m.ut(m.y[:1],0)
    ut_prop=np.concatenate((lower,lower+m.h*np.cumsum(rate_diff,axis=0)))
    transport=(2/m.h)*((u[1:]+2*m.a)*omega[1:]+(u[:-1]+2*m.a)*omega[:-1]-m.h*(u[1:]+u[:-1]))
    vt_prop=-m.d2(np.diff(u,axis=0)/m.h)-m.d1(np.diff(flux,axis=0)/m.h+transport)
    reconstruction_error=float(np.max(abs(omega[1:]-(m.h*(v-np.diff(u,axis=0)/m.h)/2-omega[:-1]))))
    identities=[float(np.max(abs(ut_prop-ut))),float(np.max(abs(vt_prop-vt)))]
    assert max(identities)<1e-8,(case,identities)
    assert reconstruction_error<1e-12
    if case in 'ABCD':
        utref=m.ut(m.y,0)
        vtref=np.concatenate([fields(m,yv[i:i+32])[2][1] for i in range(0,len(yv),32)])
        uref0=m.profile(m.y,0)[0];vref0=m.profile(yv,0)[1]
        uref=m.profile(m.y,.01)[0];vref=m.profile(yv,.01)[1]
        previous=read(PROBE/f'{case}_0.1_local.json')['defects']
    else:
        utref=reference.initial_data(case,m.x,m.y)['ut']
        vtref=reference.initial_data(case,m.x,yv)['vt']
        uref0=reference.initial_data(case,m.x,m.y)['u']
        vref0=reference.initial_data(case,m.x,yv)['v']
        uref=data['u_ref'];vref=data['v_ref']
        previous=None
        certified_path=ROOT/old['reference_values_identical_to_certified_artifact']
        certified=np.load(certified_path)
        assert sha(certified_path)==old['certified_artifact_sha256']
        for key in ['x','y','yv','u_ref','v_ref']:
            assert np.array_equal(data[key],certified[key]),key
        initial_certified_path=BASE/'nondegenerate_rk4_20261024'/f'initial_{case}_Centered-SD.npz'
        initial_certified=np.load(initial_certified_path)
        initial_certificate=read(BASE/'nondegenerate_rk4_20261024/initial_reference_certificate.json')
        proof=next(c for c in initial_certificate['cases'] if c['case']==case)
        listed=next(s for s in proof['sources'] if s['path']==initial_certified_path.name)
        assert sha(initial_certified_path)==listed['sha256']
        for key,array in [('x',m.x),('y',m.y),('yv',yv),('ut_ref',utref),('vt_ref',vtref)]:
            assert np.array_equal(initial_certified[key],array),key
    eut,put=measured(m,ut-utref,m.y);evt,pvt=measured(m,vt-vtref,yv)
    init_mismatch=[measured(m,u-uref0,m.y)[0],measured(m,v-vref0,yv)[0]]
    initial=dict(case=case,method='Centered-SD',status='complete',h=.1,dx=.1,t=0,a=2.,total=[eut,evt],
                 argmax_ut=put,argmax_vt=pvt,initial_physical_error=init_mismatch,
                 proposition_3_2_rate_difference=identities,reconstruction_recurrence_difference=reconstruction_error,
                 previous_defect_difference=None if previous is None else [abs(a-b) for a,b in zip([eut,evt],previous)],
                 numerical_state='u,w; w=4*omega/h; v=Delta_h u+adjacent average w',
                 source_artifact=old['artifact'],source_artifact_sha256=old['artifact_sha256'],
                 reference='continuous exact initial time derivatives at native physical-field sites')
    if case not in 'ABCD':
        initial.update(reference_bound=1e-13,
                       reference_values_identical_to_certified_artifact=str(initial_certified_path.relative_to(ROOT)),
                       certified_artifact_sha256=sha(initial_certified_path))
    if previous is not None:assert max(initial['previous_defect_difference'])<1e-11
    source_rate_path=HERE/f'initial_{case}.npz'
    np.savez_compressed(source_rate_path,x=m.x,y=m.y,yv=yv,ut=ut,vt=vt,ut_ref=utref,vt_ref=vtref)
    initial.update(artifact=str(source_rate_path.relative_to(ROOT)),artifact_sha256=sha(source_rate_path))
    # Recompute final errors from the previously saved numerical fields.
    mapped=np.diff(data['z'][0],axis=0)/m.h+(data['z'][1,1:]+data['z'][1,:-1])/2
    map_error=float(np.max(abs(mapped-data['v'])))
    error=[measured(m,data['u']-uref,m.y)[0],measured(m,data['v']-vref,yv)[0]]
    final_difference=max(abs(a-b) for a,b in zip(error,old['error']))
    assert map_error==0 and final_difference==0
    result=dict(old)
    result.update(method='Centered-SD',source_method=old['method'],source_record=str((NATURAL/f'{case}.json').relative_to(ROOT)),
                  source_record_sha256=sha(NATURAL/f'{case}.json'),section_3_2_normalization='omega=h*w/4',
                  section_3_2_field_map='v=Delta_h u+2*(omega_k+omega_(k-1))/h',
                  recomputed_error=error,final_record_difference=final_difference,map_error=map_error)
    (HERE/f'initial_{case}.json').write_text(json.dumps(initial,indent=2),encoding='utf8')
    (HERE/f'{case}.json').write_text(json.dumps(result,indent=2),encoding='utf8')
    print(json.dumps(dict(case=case,initial=initial['total'],final=error,identities=identities)),flush=True)
    return initial,result

if __name__=='__main__':
    rows=[prepare(c) for c in ['A','B','C','D','Gaussian','Sinusoidal']]
    initials=[r[0] for r in rows];finals=[r[1] for r in rows]
    (HERE/'initial_results.json').write_text(json.dumps(initials,indent=2),encoding='utf8')
    (HERE/'results.json').write_text(json.dumps(finals,indent=2),encoding='utf8')
    validation=dict(records=len(finals),complete=sum(r['status']=='complete' for r in finals),
       max_record_difference=max(r['final_record_difference'] for r in finals),
       max_map_difference=max(r['map_error'] for r in finals),
       max_initial_rate_identity_difference=max(max(r['proposition_3_2_rate_difference']) for r in initials),
       max_reconstruction_recurrence_difference=max(r['reconstruction_recurrence_difference'] for r in initials),
       max_initial_physical_error=max(max(r['initial_physical_error']) for r in initials),
       non_soliton_initial_and_final_references_bitwise_identical_to_certified_arrays=True,
       non_soliton_reference_bound=1e-13,
       reused_terminal_trajectories=True,manuscript_source_sha256=sha(BASE.parent/'natural_centered_section_20261025/section_3_2.md'),
       script_sha256=sha(Path(__file__)))
    (HERE/'validation.json').write_text(json.dumps(validation,indent=2),encoding='utf8')
    print(json.dumps(validation,indent=2))
