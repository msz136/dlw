"""Prepare exact initial profiles, native physical errors and y=0 sections."""
from pathlib import Path
import hashlib,json,sys,time
import numpy as np
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
import figure_data as api

def read(p):return json.loads(p.read_text(encoding='utf8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def table_records(case,method):
    if method=='Centered-SD':
        ini=read(api.SELECTION/'initial_results.json');fin=read(api.SELECTION/'results.json')
    elif case in ('A','B','C','D'):
        ini=read(api.PROBE/'rerun_20261024/baselines.json');fin=read(api.BASE/'rk4_spatial/results.json')
    else:
        ini=read(api.BASE/'nondegenerate_rk4_20261024/initial_results.json')
        fin=read(api.BASE/'nondegenerate_rk4_20261024/results.json')
    match=lambda rs:next(r for r in rs if r['case']==case and r['method']==method and r['h']==r['dx']==.1)
    return match(ini),match(fin)

def maximum(case,x,y,arr):
    if case in ('A','B','C','D'):
        r=api.HALF_WIDTHS[case];return float(np.max(abs(arr[abs(y)<r][:,abs(x)<=r])))
    return float(np.max(abs(arr[abs(y)<=1.8+1e-12])))

def sliced_exact_rates(case,x,y):
    rows=[api.exact_rates(case,x,y[j:j+24],0.) for j in range(0,len(y),24)]
    return [np.concatenate([r[k] for r in rows],axis=0) for k in (0,1)]

def full_method(case,method):
    ini,fin=table_records(case,method)
    path=api.ROOT/fin['artifact'];d=np.load(path)
    assert sha(path)==fin['artifact_sha256']
    x,y,yv=d['x'],d['y'],d['yv']
    sources=[dict(path=str(path.relative_to(api.ROOT)),sha256=sha(path))]
    if method=='Centered-SD':
        m=api.Model(case,'Centered-SD',.1,.1) if case in ('A','B','C','D') else api.reference.NondegenerateModel(case,'Centered-SD')
        m.gauge='local'
        u0=d['z0'][0];v0=api.transform(m,*d['z0'])
        ratepath=api.SELECTION/f'initial_{case}.npz';rates=np.load(ratepath)
        ut,vt,utr,vtr=(rates[k] for k in ['ut','vt','ut_ref','vt_ref'])
        sources.append(dict(path=str(ratepath.relative_to(api.ROOT)),sha256=sha(ratepath)))
    elif case in ('A','B','C','D'):
        m=api.Model(case,method,.1,.1)
        u0,v0=d['z0'];ut,vt=m.rhs(0.,d['z0'])
        utr=m.ut(y,0.)
        vtr=sliced_exact_rates(case,x,yv)[1]
    else:
        m=api.reference.NondegenerateModel(case,method)
        u0,v0=d['z0']
        ratepath=api.BASE/'nondegenerate_rk4_20261024'/f'initial_{case}_{method}.npz'
        rates=np.load(ratepath)
        ut,vt,utr,vtr=(rates[k] for k in ['ut','vt','ut_ref','vt_ref'])
        sources.append(dict(path=str(ratepath.relative_to(api.ROOT)),sha256=sha(ratepath)))
    ufr,vfr=(d['u_ref'],d['v_ref']) if 'u_ref' in d.files else (m.profile(y,.01)[0],m.profile(yv,.01)[1])
    u0r,v0r=m.profile(y,0)[0],m.profile(yv,0)[1]
    values={'initial':(u0,v0),'rate':(ut,vt),'final':(d['u'],d['v'])}
    refs={'initial':(u0r,v0r),'rate':(utr,vtr),'final':(ufr,vfr)}
    errors={stage:[maximum(case,x,yy,a-b) for yy,a,b in zip((y,yv),values[stage],refs[stage])]
            for stage in ('rate','final')}
    differences={'rate':[abs(a-b) for a,b in zip(errors['rate'],ini['total'])],
                 'final':[abs(a-b) for a,b in zip(errors['final'],fin['error'])]}
    assert max(differences['rate'])<1e-10,(case,method,differences)
    assert max(differences['final'])<1e-12,(case,method,differences)
    return x,(y,yv),values,refs,dict(table_initial=ini['total'],table_final=fin['error'],
        recomputed_native_maxima=errors,table_maximum_difference=differences,sources=sources)

def prepare(case):
    started=time.perf_counter()
    first=full_method(case,'Endpoint-SD');x=first[0]
    xrange,yrange=api.display_limits(case)
    mx=(x>=xrange[0])&(x<=xrange[1])
    xd=x[mx];line_x=np.linspace(*xrange,2001)
    initial_y=np.linspace(*(yrange if case in ('A','B','C','D') else (-2.,2.)),201)
    out=dict(x=xd,line_x=line_x,exact_initial_y=initial_y)
    # Exact wave surfaces at t=0, independent of all numerical schemes.
    eu,ev=api.exact_fields(case,xd,initial_y,0.)
    out['exact_initial_u']=eu;out['exact_initial_v']=ev
    exacts={}
    for stage,t in [('initial',0.),('rate',0.),('final',.01)]:
        fun=api.exact_rates if stage=='rate' else api.exact_fields
        dense=fun(case,line_x,[0.],t);native=fun(case,xd,[0.],t)
        exacts[stage]=[a[0] for a in native]
        for field,a,b in zip(('u','v'),dense,native):
            out[f'exact_line_{stage}_{field}']=a[0]
            out[f'exact_native_{stage}_{field}']=b[0]
    metadata=dict(case=case,display_x_interval=xrange,display_y_interval=yrange,
        initial_exact_y_interval=[float(initial_y[0]),float(initial_y[-1])],
        section_y=0.,interpolation='12 nearest native nodes, degree 11 barycentric; degree 15 independent control',
        section_values='Numerical physical fields interpolated directly; exact profiles independently evaluated at y=0.',
        methods={})
    for prefix,method in api.METHODS.items():
        xx,ys,vals,refs,meta=first if prefix=='endpoint' else full_method(case,method)
        assert np.array_equal(xx,x)
        meta['interpolation']={};meta['visible_error_maxima']={}
        for field,yy in zip(('u','v'),ys):
            my=(abs(yy)<yrange[1]) if case in ('A','B','C','D') else (abs(yy)<=yrange[1]+1e-12)
            out[f'{prefix}_y_{field}']=yy[my]
        for stage in ('initial','rate','final'):
            meta['interpolation'][stage]={};meta['visible_error_maxima'][stage]={}
            for j,(field,yy) in enumerate(zip(('u','v'),ys)):
                my=(abs(yy)<yrange[1]) if case in ('A','B','C','D') else (abs(yy)<=yrange[1]+1e-12)
                num=vals[stage][j];ref=refs[stage][j]
                out[f'{prefix}_{stage}_{field}']=num[my][:,mx]
                out[f'{prefix}_ref_{stage}_{field}']=ref[my][:,mx]
                out[f'{prefix}_error_{stage}_{field}']=(num-ref)[my][:,mx]
                sec,rule=api.section_at_zero(yy,num[:,mx],11)
                control,_=api.section_at_zero(yy,num[:,mx],15)
                rsec,_=api.section_at_zero(yy,ref[:,mx],11)
                rcontrol,_=api.section_at_zero(yy,ref[:,mx],15)
                truth=exacts[stage][j]
                out[f'{prefix}_line_{stage}_{field}']=sec
                out[f'{prefix}_line_error_{stage}_{field}']=sec-truth
                meta['interpolation'][stage][field]=dict(rule,
                    degree11_vs_degree15_max=float(np.max(abs(sec-control))),
                    exact_sample_degree11_vs_analytic_y0_max=float(np.max(abs(rsec-truth))),
                    exact_sample_degree15_vs_analytic_y0_max=float(np.max(abs(rcontrol-truth))),
                    plotted_section_error_max=float(np.max(abs(sec-truth))))
                meta['visible_error_maxima'][stage][field]=float(np.max(abs((num-ref)[my][:,mx])))
        metadata['methods'][prefix]=meta
    dest=HERE/f'{case}.npz'
    np.savez_compressed(dest,**out)
    metadata.update(data_sha256=sha(dest),data_file=dest.name,elapsed_seconds=time.perf_counter()-started)
    (HERE/f'{case}.json').write_text(json.dumps(metadata,indent=2),encoding='utf8')
    print(json.dumps(dict(case=case,file=str(dest),seconds=metadata['elapsed_seconds'],
         interpolation_max=max(v['degree11_vs_degree15_max'] for m in metadata['methods'].values() for q in m['interpolation'].values() for v in q.values()))),flush=True)
    return metadata

if __name__=='__main__':
    cases=sys.argv[1:] or api.CASES
    rows=[prepare(c) for c in cases]
    if len(cases)==6:
        final=dict(cases=cases,methods=list(api.METHODS.values()),case_metadata=[c+'.json' for c in cases],
            actual_native_reference_bound_non_solitons=1e-13,
            interpolation_scope='Degree-11 physical-field interpolation with degree-15 and exact-sample checks; no interval certificate for interpolated sections.',
            max_table_rate_difference=max(max(m['table_maximum_difference']['rate']) for r in rows for m in r['methods'].values()),
            max_table_final_difference=max(max(m['table_maximum_difference']['final']) for r in rows for m in r['methods'].values()),
            source_sha256={p.name:sha(p) for p in [Path(__file__),HERE.parent/'figure_data.py']})
        (HERE/'validation.json').write_text(json.dumps(final,indent=2),encoding='utf8')
