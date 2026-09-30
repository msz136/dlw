"""Read every saved field, export matched tables; do not edit reports or HTML."""
from experiment import *
from scipy.interpolate import CubicSpline

FIELDS=('u','v')
ANCHORS=(.001,.005,.01,.02)


def grid(n=4001): return np.linspace(-10,10,n)


def field(z,t,f,xx=None,y=None):
    xx=grid() if xx is None else xx
    x=z[f't{t:g}_x']
    assert np.all(np.diff(x)>0) and x[0]<=xx[0] and x[-1]>=xx[-1]
    a=CubicSpline(x,z[f't{t:g}_{f}'],axis=-1)(xx)
    if y is not None and not np.array_equal(y,z['y']):
        assert min(y)>=min(z['y']) and max(y)<=max(z['y'])
        a=CubicSpline(z['y'],a,axis=0)(y)
    return a


def main():
    d=json.loads((OUT/'results.json').read_text(encoding='utf-8')); runs=d['runs']
    assert len(runs)==len(plan())==156
    assert len({tuple(sorted(r['spec'].items())) for r in runs})==156
    for p,h in d['sources'].items(): assert io.sha(p)==h,p
    lookup={tuple(r['spec'][k] for k in ('method','case','model','mesh','variant')):r for r in runs}
    def get(method,case,model,mesh,variant='main'): return lookup[method,case,model,mesh,variant]
    def snap(r,t): return next((a for a in r['history'] if abs(a['t']-t)<1e-12),None)
    errors=[]; initial=[]; density=[]; controls=[]; fine=[]; orders=[]; pairs=[]; recon=[]
    readback=0.; boundary=0.; peaks={}
    for case in CASES:
        g=SingleExact(CASES[case],.125)
        peaks[case]=dict(zip(FIELDS,[float(abs(a).max()) for a in g.uv(np.arange(-12,12),grid(16001),0.)]))
    for r in runs:
        s=r['spec']; assert io.sha(r['profile'])==r['profile_sha256']
        ref=io.PaperExact(io.CASES[s['case']],s['h'],True)
        js=np.arange(-round(1.5/s['h']),round(1.5/s['h']))
        b=get(s['method'],s['case'],'SD',s['mesh'],s['variant'])
        with np.load(r['profile']) as z,np.load(b['profile']) as zb:
            assert len(z['y'])==len(js) and np.allclose(z['y'],(js+.5)*s['h'],rtol=0,atol=1e-14)
            diffs={f:float(abs(z['t0_'+f]-zb['t0_'+f]).max()) for f in ('x','u','v')}
            assert max(diffs.values())<1e-10,diffs
            initial.append(dict(**s,**diffs))
            displacements=[]
            for h in r['history']:
                t=h['t']; exact=ref.uv(js,grid(),t)
                bu=ref.uv([js[0]],z[f't{t:g}_x'],t)[0][0]
                boundary=max(boundary,float(abs(z[f't{t:g}_u'][0]-bu).max()))
                assert np.all(np.isfinite(z[f't{t:g}_u'])) and np.all(np.isfinite(z[f't{t:g}_v']))
                displacements.append(float(abs(z[f't{t:g}_x']-z['t0_x']).max()))
                for f,e in zip(FIELDS,exact):
                    er=float(abs(field(z,t,f)-e).max())
                    readback=max(readback,abs(er-h['errors'][f]))
                    errors.append(dict(**s,t=t,field=f,error=er))
                    if s['variant']=='main' and t in (0.,.01,.02):
                        e2=ref.uv(js,grid(8001),t)[FIELDS.index(f)]
                        er2=float(abs(field(z,t,f,grid(8001))-e2).max())
                        density.append(dict(method=s['method'],case=s['case'],model=s['model'],mesh=s['mesh'],t=t,field=f,error_4001=er,error_8001=er2,relative_change=abs(er2/er-1) if er else 0.))
            if s['mesh']=='fixed': assert r['moved_steps']==0 and max(displacements)==0
            elif r['status']=='completed': assert r['moved_steps']==round(s['T']/s['dt']) and displacements[-1]>0
            if s['model']=='SD2':
                p=Problem(s);p.initial();m=p.m
                for t in (0.,.01,.02):
                    if f't{t:g}_Q' not in z: continue
                    m.X.set_s(z[f't{t:g}_x']-m.X.xi);m.boundary(t)
                    state=m.pack(z[f't{t:g}_Q'],z[f't{t:g}_R'])
                    uv=m.fields(state,t)
                    dd={f:float(abs(a-z[f't{t:g}_{f}']).max()) for f,a in zip(FIELDS,uv)}
                    assert max(dd.values())<1e-10
                    recon.append(dict(method=s['method'],case=s['case'],mesh=s['mesh'],variant=s['variant'],t=t,**dd))
    assert readback<1e-12 and boundary<1e-10
    table=[]
    for method in ('RK4','Euler'):
        for case in CASES:
            for mesh in ('fixed','moving'):
                for t in (0.,.001,.005,.01,.02):
                    row=dict(method=method,case=case,mesh=mesh,t=t)
                    for model in ('SD','SD2','FD'):
                        h=snap(get(method,case,model,mesh),t)
                        row.update({model+'_'+f:h['errors'][f] if h else None for f in FIELDS})
                    table.append(row)
                for model in ('SD','SD2','FD'):
                    main=get(method,case,model,mesh)
                    variants=['time_half','x_half','y_half','domain_double']
                    if method=='Euler': variants+=['time_quarter']
                    with np.load(main['profile']) as z0:
                        for variant in variants:
                            r=get(method,case,model,mesh,variant)
                            with np.load(r['profile']) as z:
                                for t in ANCHORS:
                                    a,b=snap(main,t),snap(r,t)
                                    for f in FIELDS:
                                        diff=float(abs(field(z0,t,f)-field(z,t,f,y=z0['y'])).max()) if a and b else None
                                        ea,eb=(a['errors'][f],b['errors'][f]) if a and b else (None,None)
                                        passed=bool(diff is not None and max(ea,eb)<=.01*peaks[case][f] and diff<=.001*peaks[case][f])
                                        controls.append(dict(method=method,case=case,model=model,mesh=mesh,variant=variant,t=t,field=f,main_error=ea,control_error=eb,field_difference=diff,initial_peak=peaks[case][f],pass_threshold=passed))
                    a=get(method,case,model,mesh,'x_half'); b=get(method,case,model,mesh,'x_half_time_half')
                    with np.load(a['profile']) as z1,np.load(b['profile']) as z2:
                        for t in ANCHORS:
                            for f in FIELDS:
                                diff=float(abs(field(z1,t,f)-field(z2,t,f)).max()) if snap(a,t) and snap(b,t) else None
                                ea=snap(a,t)['errors'][f] if snap(a,t) else None
                                eb=snap(b,t)['errors'][f] if snap(b,t) else None
                                fine.append(dict(method=method,case=case,model=model,mesh=mesh,t=t,field=f,x_half_error=ea,x_half_time_half_error=eb,field_difference=diff,initial_peak=peaks[case][f],pass_threshold=bool(diff is not None and max(ea,eb)<=.01*peaks[case][f] and diff<=.001*peaks[case][f])))
                    if method=='Euler':
                        rr=[get(method,case,model,mesh,v) for v in ('main','time_half','time_quarter')]
                        zz=[np.load(r['profile']) for r in rr]
                        for t in ANCHORS:
                            for f in FIELDS:
                                if not all(snap(r,t) for r in rr): continue
                                aa,bb,cc=[field(z,t,f) for z in zz]
                                da=float(abs(aa-bb).max());db=float(abs(bb-cc).max())
                                orders.append(dict(case=case,model=model,mesh=mesh,t=t,field=f,dt_vs_half=da,half_vs_quarter=db,order=float(np.log2(da/db)) if da and db else None))
                        for z in zz: z.close()
    for case in CASES:
        for model in ('SD','SD2','FD'):
            for mesh in ('fixed','moving'):
                a=get('Euler',case,model,mesh);b=get('RK4',case,model,mesh)
                assert {k:v for k,v in a['spec'].items() if k!='method'}=={k:v for k,v in b['spec'].items() if k!='method'}
                with np.load(a['profile']) as za,np.load(b['profile']) as zb:
                    for f in ('x','u','v'): assert np.array_equal(za['t0_'+f],zb['t0_'+f]) or np.max(abs(za['t0_'+f]-zb['t0_'+f]))<1e-12
                    for t in (.01,.02):
                        for f in FIELDS:
                            ea=snap(a,t)['errors'][f];eb=snap(b,t)['errors'][f]
                            pairs.append(dict(case=case,model=model,mesh=mesh,t=t,field=f,Euler_error=ea,RK4_error=eb,Euler_over_RK4=ea/eb,field_difference=float(abs(field(za,t,f)-field(zb,t,f)).max())))
    passing=[]
    for method in ('RK4','Euler'):
        for case in CASES:
            for model in ('SD','SD2','FD'):
                for mesh in ('fixed','moving'):
                    anchors=[]
                    for t in ANCHORS:
                        rows=[r for r in controls+fine if all(r[k]==v for k,v in dict(method=method,case=case,model=model,mesh=mesh,t=t).items())]
                        assert len(rows)==(12 if method=='Euler' else 10)
                        if all(r['pass_threshold'] for r in rows): anchors.append(t)
                    passing.append(dict(method=method,case=case,model=model,mesh=mesh,anchors=anchors))
    status=[dict(**r['spec'],origin=r['origin'],status=r['status'],reached=r['reached'],reason=r['reason']) for r in runs]
    for name,rows in [('comparison',table),('error_time_all',errors),('initial_uv_matching',initial),('evaluation_density',density),('control_comparisons',controls),('fine_time_checks',fine),('Euler_time_order',orders),('euler_vs_rk4',pairs),('qr_reconstruction',recon),('status',status)]: io.csvout(OUT/(name+'.csv'),rows)
    io.csvout(OUT/'index_t001.csv',[r for r in table if r['t']==.01])
    v=dict(total_runs=len(runs),new_runs=sum(r['origin']=='new' for r in runs),reused_runs=sum(r['origin']=='reused' for r in runs),completed=sum(r['status']=='completed' for r in runs),
           profile_hashes_verified=len(runs),source_hashes_verified=len(d['sources']),error_values_readback=len(errors),readback_max=readback,
           initial_uv_node_match_max=max(max(r[f] for f in ('x','u','v')) for r in initial),lower_u_boundary_error_max=boundary,
           qr_reconstruction_max=max(max(r[f] for f in FIELDS) for r in recon),evaluation_double_max_relative_change=max(r['relative_change'] for r in density),
           Euler_order_range=[min(r['order'] for r in orders),max(r['order'] for r in orders)],passing_anchors=passing,
           artifact_sources={str(Path(__file__)):io.sha(__file__),str(OUT/'results.json'):io.sha(OUT/'results.json')})
    io.dump(OUT/'validation.json',v)
    print(json.dumps({k:val for k,val in v.items() if k not in ('passing_anchors','artifact_sources')},indent=2))
    print('PASS: every saved field, hash, matched initial state, boundary and mesh checked.')


if __name__=='__main__': main()
