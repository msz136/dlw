"""Frozen one-step source/transport intervention; independent exact-reference defects."""
from pathlib import Path
import argparse,csv,hashlib,importlib.util,json,time
import numpy as np
import common as C

HERE=Path(__file__).resolve().parent
KINDS=('SD','FD')

def dump_csv(path,rows):
    with path.open('w',newline='',encoding='utf-8') as stream:
        keys=list(dict.fromkeys(k for r in rows for k in r))
        w=csv.DictWriter(stream,fieldnames=keys);w.writeheader();w.writerows(rows)

def metric_row(case,t,label,obj,z,mask):
    f=C.cropped_error(obj,z,mask)
    return dict(case=case,t=t,label=label,**C.field_stats(f))

def run(case,T=None,dt=None,parts=False,intervention=False,source_cache=False):
    cfg=C.NS['case_config'](case)
    if T is not None:cfg['T']=T
    if dt is not None:cfg['dt']=dt
    dt=cfg['dt'];nsteps=round(cfg['T']/dt)
    tag=f'{case}_T{cfg["T"]:.3f}_dt{dt:.6f}'+('_parts' if parts else '')+('_cache5' if source_cache else '')
    out=HERE/tag;out.mkdir(exist_ok=True)
    if (out/'validation.json').exists():
        print('EXISTS',tag,flush=True);return
    models={k:C.setup(case,k,cfg)[0] for k in KINDS};obj=models['FD']
    mask=C.masks(obj,cfg);z0=C.reference(obj,0.)
    actual={k:z0.copy() for k in KINDS}
    pred={k:np.zeros((2,z0.size)) for k in KINDS}
    accum=np.zeros((2,z0.size));normsum=np.zeros(2)
    correction={k:{lam:z0.copy() for lam in (.5,1.)} for k in KINDS} if intervention else {}
    rows=[];comparisons=[];source_rows=[];interventions=[];source_comparison=[]
    part_names=('y_model','x_stencil','x_wrap')
    if parts:
        spec=importlib.util.spec_from_file_location('transport_sources',HERE.parent/'sources/common_sources.py')
        S=importlib.util.module_from_spec(spec);spec.loader.exec_module(S)
        if source_cache:
            from source_cache import SourceCache
            S=SourceCache(out,S,models,cfg['T'])
        ep={k:np.zeros((3,z0.size)) for k in KINDS}
        src0={k:S.source_parts(models[k],0.) for k in KINDS}
    started=time.perf_counter();max_local_parts=0.;max_sum_parts=0.;max_checks=0.
    def observe(n):
        t=n*dt;ref=C.reference(obj,t);frame={}
        for j,k in enumerate(KINDS):
            err=actual[k]-ref
            rows.append(metric_row(case,t,f'actual_{k}',obj,err,mask))
            rows.append(metric_row(case,t,f'full_actual_{k}',obj,err,None))
            frame[f'actual_{k}']=C.cropped_error(obj,err,mask)
            for l,s in enumerate(KINDS):
                label=f'{k}_from_{s}'
                f=C.cropped_error(obj,pred[k][l],mask);a=C.cropped_error(obj,accum[l],mask)
                rows.append(dict(case=case,t=t,label=label,**C.field_stats(f)))
                v=C.compare(f,a)
                comparisons.append(dict(case=case,t=t,propagator=k,source=s,
                    comparison='against_unpropagated_sum',**v))
                if k==s:
                    comparisons.append(dict(case=case,t=t,propagator=k,source=s,
                        comparison='against_actual',**C.compare(f,frame[f'actual_{k}'])))
                frame[label]=f
            frame[f'unpropagated_{k}']=C.cropped_error(obj,accum[j],mask)
            rows.append(metric_row(case,t,f'unpropagated_{k}',obj,accum[j],mask))
            if parts:
                pf=C.cropped_error(obj,ep[k],mask)
                total=pf.sum(axis=0);diagonal=frame[f'{k}_from_{k}']
                source_comparison.append(dict(case=case,t=t,kind=k,comparison='sum_parts_vs_one_step',**C.compare(total,diagonal)))
                for i,name in enumerate(part_names):
                    rows.append(dict(case=case,t=t,label=f'{k}_part_{name}',**C.field_stats(pf[i])))
                    frame[f'{k}_part_{name}']=pf[i]
                for field,index in [('joint',slice(None)),('u',0),('v',1)]:
                    y=pf[0,index].ravel();x=pf[1,index].ravel()
                    sy=np.linalg.norm(y);sx=np.linalg.norm(x)
                    source_comparison.append(dict(case=case,t=t,kind=k,comparison=f'part_angle_{field}',
                        cosine=float(y@x/(sy*sx)) if sy*sx else np.nan,
                        cancellation_ratio=float(np.linalg.norm(y+x)/(sy+sx)) if sy+sx else np.nan))
            if intervention:
                for lam in (.5,1.):
                    cf=C.cropped_error(obj,correction[k][lam]-ref,mask)
                    cf_pred=(1-lam)*frame[f'{k}_from_{k}']
                    interventions.append(dict(case=case,t=t,kind=k,lam=lam,**C.field_stats(cf),
                        **{'prediction_'+key:value for key,value in C.compare(cf_pred,cf).items()}))
                    if n%max(1,nsteps//20)==0:frame[f'{k}_cancel_{lam}']=cf
        if n%max(1,nsteps//20)==0 or n==nsteps:
            np.savez_compressed(out/f'frame_{n:05d}.npz',t=t,x=obj.X.x[mask[1]],y=obj.y[mask[0]],**frame)
    print('START',tag,'state',z0.size,flush=True)
    start_step=0
    if (out/'checkpoint.json').exists() and (out/'checkpoint.npz').exists():
        meta=json.loads((out/'checkpoint.json').read_text(encoding='utf-8'))
        with np.load(out/'checkpoint.npz') as cp:
            if int(cp['n'])==meta['n']:
                start_step=meta['n'];accum=cp['accum'].copy();normsum=cp['normsum'].copy()
                for k in KINDS:
                    actual[k]=cp['actual_'+k].copy();pred[k]=cp['pred_'+k].copy()
                    if parts:ep[k]=cp['ep_'+k].copy()
                rows=meta['rows'];comparisons=meta['comparisons'];source_rows=meta['source_rows']
                source_comparison=meta['source_comparison'];interventions=meta['interventions']
                max_local_parts=meta['max_local_parts'];max_sum_parts=meta['max_sum_parts'];max_checks=meta['max_checks']
                if parts:src0={k:S.source_parts(models[k],start_step*dt) for k in KINDS}
                print('RESUME',start_step,flush=True)
    if start_step==0:observe(0)
    for n in range(start_step,nsteps):
        t=n*dt;ref=C.reference(obj,t);nextref=C.reference(obj,(n+1)*dt)
        defects={};transported={}
        for k in KINDS:
            directions=np.concatenate((pred[k],ep[k]),axis=0) if parts else pred[k]
            stepped,td=C.step_and_jvp(models[k],t,ref,directions,dt)
            defects[k]=stepped-nextref;transported[k]=td
        if parts:
            sm={k:S.source_parts(models[k],t+dt/2) for k in KINDS}
            se={k:S.source_parts(models[k],(n+1)*dt) for k in KINDS}
        for j,k in enumerate(KINDS):
            model=models[k]
            actual[k]=C.common_step(model,t,actual[k],dt)
            pred[k]=transported[k][:2]+np.stack([defects[s] for s in KINDS])
            accum[j]+=defects[k]
            f=C.cropped_error(obj,defects[k],mask);normsum[j]+=C.field_stats(f)['joint_rms']
            source_rows.append(dict(case=case,t=(n+1)*dt,kind=k,**C.field_stats(f),
                sum_individual_joint_norm=normsum[j],accumulated_joint_norm=C.field_stats(C.cropped_error(obj,accum[j],mask))['joint_rms']))
            if intervention:
                for lam in (.5,1.):
                    correction[k][lam]=C.common_step(model,t,correction[k][lam],dt)-lam*defects[k]
            if parts:
                # Inhomogeneous RK4 variational integral along the independently sampled exact reference.
                def forcing(source):return C.tangent_to_native(model,np.stack([source[name] for name in part_names]))
                r1,rm,re=forcing(src0[k]),forcing(sm[k]),forcing(se[k])
                a1=r1
                a2=C.native_rhs_jvp(model,t+dt/2,sm[k]['native_ref'],dt*a1/2)+rm
                a3=C.native_rhs_jvp(model,t+dt/2,sm[k]['native_ref'],dt*a2/2)+rm
                a4=C.native_rhs_jvp(model,t+dt,se[k]['native_ref'],dt*a3)+re
                part_d=C.tangent_from_native(model,dt*(a1+2*a2+2*a3+a4)/6)
                ep[k]=transported[k][2:]+part_d
                ff=C.cropped_error(obj,part_d.sum(axis=0)-defects[k],mask)
                dd=C.cropped_error(obj,defects[k],mask)
                rel=float(np.linalg.norm(ff)/max(np.linalg.norm(dd),1e-100))
                max_local_parts=max(max_local_parts,rel)
                max_checks=max(max_checks,max(se[k]['checks'].values()))
                max_sum_parts=max(max_sum_parts,float(np.max(abs(se[k]['total']-se[k]['y_model']-se[k]['x_stencil']-se[k]['x_wrap']))))
        if parts:src0=se
        observe(n+1)
        if source_cache and (n+1)%10==0:
            cp={'n':n+1,'accum':accum,'normsum':normsum}
            cp.update({'actual_'+k:actual[k] for k in KINDS});cp.update({'pred_'+k:pred[k] for k in KINDS})
            if parts:cp.update({'ep_'+k:ep[k] for k in KINDS})
            np.savez(out/'checkpoint.npz',**cp)
            (out/'checkpoint.json').write_text(json.dumps(dict(n=n+1,rows=rows,comparisons=comparisons,
                source_rows=source_rows,source_comparison=source_comparison,interventions=interventions,
                max_local_parts=max_local_parts,max_sum_parts=max_sum_parts,max_checks=max_checks)),encoding='utf-8')
        if (n+1)%max(1,nsteps//10)==0:print('PROGRESS',tag,n+1,nsteps,'sec',round(time.perf_counter()-started,1),flush=True)
    dump_csv(out/'timeseries.csv',rows);dump_csv(out/'comparison.csv',comparisons);dump_csv(out/'sources.csv',source_rows)
    if parts:dump_csv(out/'source_budget.csv',source_comparison)
    if intervention:dump_csv(out/'intervention.csv',interventions)
    finals={f'actual_{k}':actual[k] for k in KINDS}
    finals.update({f'pred_{k}':pred[k] for k in KINDS});finals['accum']=accum
    if parts:finals.update({f'parts_{k}':ep[k] for k in KINDS})
    np.savez_compressed(out/'final_common.npz',reference=nextref,**finals)
    regression={};regression_physical_error={}
    if np.isclose(cfg['T'],.01):
        for k in KINDS:
            with np.load(C.ROOT/f'Workspaces/dlw_three_tracks_20261013/shared/{case}_{k}_RK4_endpoints.npz') as old:
                old_common=C.from_native(models[k],old['final'],cfg['T'])
            regression[k]=float(np.max(abs(old_common-actual[k])))
            old_error=C.cropped_error(obj,old_common-nextref,mask)
            new_error=C.cropped_error(obj,actual[k]-nextref,mask)
            regression_physical_error[k]=C.compare(new_error,old_error)
    result=dict(case=case,config=cfg,seconds=time.perf_counter()-started,
        parts=parts,intervention=intervention,regression_common_linf=regression,
        regression_against_original_time_step=regression_physical_error,
        final_metrics=[r for r in rows if r['t']==cfg['T']],
        final_comparisons=[r for r in comparisons if r['t']==cfg['T']],
        final_source_budget=[r for r in source_comparison if r['t']==cfg['T']],
        max_local_parts_relative_residual=max_local_parts,max_algebra_source_sum_linf=max_sum_parts,
        max_source_independent_check=max_checks,
        source_interpolation_validation=S.validation if source_cache else None,
        protocol_sha256=hashlib.sha256((HERE/'PROTOCOL.md').read_bytes()).hexdigest(),
        common_sha256=hashlib.sha256((HERE/'common.py').read_bytes()).hexdigest(),
        frozen_solver_sha256=hashlib.sha256((C.ROOT/'Workspaces/dlw_three_tracks_20261013/shared/solver_cells.json').read_bytes()).hexdigest())
    if np.isclose(dt,.0001):assert all(v<1e-9 for v in regression.values()),regression
    else:assert all(v['relative_residual']<.001 for v in regression_physical_error.values()),regression_physical_error
    assert np.isfinite(np.concatenate(list(actual.values()))).all()
    result['passed']=True
    (out/'validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print('DONE',tag,'seconds',result['seconds'],flush=True)
    print(json.dumps(result['final_comparisons'],indent=2),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--case',choices=KINDS+('A','C'),required=True)
    p.add_argument('--T',type=float);p.add_argument('--dt',type=float)
    p.add_argument('--parts',action='store_true');p.add_argument('--intervention',action='store_true')
    p.add_argument('--source-cache',action='store_true')
    a=p.parse_args();run(a.case,a.T,a.dt,a.parts,a.intervention,a.source_cache)
