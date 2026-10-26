from compare import *

def jets(g,js,x,t):
    _,f=g.tau(js,x,t,True);_,b=g.tau(js,x,t)
    def third(w):
        k=g.rates[:,0,None,None];m=g.mean(w,0)
        return np.sum(w*(k-m)**3,axis=0)
    return dict(u=2*(g.mean(f,0)-g.mean(b,0)),ux=2*(g.cov(f,0,0)-g.cov(b,0,0)),
        uxx=2*(third(f)-third(b)),ut=2*(g.cov(f,0,1)-g.cov(b,0,1)),
        sx=g.mean(f,0)+g.mean(b,0),sxx=g.cov(f,0,0)+g.cov(b,0,0),
        sxxx=third(f)+third(b),sxt=g.cov(f,0,1)+g.cov(b,0,1))

out={}
for case in CASES:
    g=PaperExact(case,.1);h=g.h;js=np.arange(-8,9);x=np.linspace(-3,3,31)
    z=jets(g,js,x,.007);b=jets(g,js-1,x,.007)
    v=2*(z['sx']-b['sx'])/h;vx=2*(z['sxx']-b['sxx'])/h
    vxx=2*(z['sxxx']-b['sxxx'])/h;vt=2*(z['sxt']-b['sxt'])/h
    du=(z['u']-b['u'])/h;dux=(z['ux']-b['ux'])/h;duxx=(z['uxx']-b['uxx'])/h
    avg=(z['u']+b['u'])/2;avgx=(z['ux']+b['ux'])/2
    r1=(z['ut']-b['ut'])/h+((z['u']+4)*z['ux']-(b['u']+4)*b['ux'])/h+vxx
    r2=vt+(avg+4-2*h)*vx+avgx*v+h*v*vx/2-4*avgx+duxx-h*du*dux/2
    out[case]=dict(analytic_nonlinear_residuals=[float(abs(r1).max()),float(abs(r2).max())])
    assert max(out[case]['analytic_nonlinear_residuals'])<1e-9
    # Independent direct-u telescoping check of the evolved P=delta_-u system.
    cfg=case_config(case);m=PaperModel(case,cfg);s=m.initial();p,v=m.unpack(s)
    u=m.recover_u(p,0);dp,dv=m.unpack(m.rhs(0,s))
    j=jets(m.G,[m.js[0]],m.X.x,0)
    reconstructed_ut=j['ut']+h*np.cumsum(dp,axis=0)
    H=m.X.d1(u*u/2+4*u)
    telescoped=-H[1:]-h*np.cumsum(m.X.d2(v[1:]),axis=0)+j['ut']+H[:1]
    err=float(abs(reconstructed_ut-telescoped).max());assert err<1e-10
    out[case]['direct_u_vs_P_rhs']=err
    # Model-gap refinement at fixed continuous physical coordinates (no time solve).
    gaps=[]
    xr=np.linspace(-HALF_WIDTHS[case],HALF_WIDTHS[case],201)
    yr=np.linspace(-HALF_WIDTHS[case],HALF_WIDTHS[case],101)
    for hh in (.1,.05,.025):
        pg=PaperExact(case,hh);cg=Exact(case,hh)
        js=yr/hh-.5
        a=pg.uv(js,xr,.01);b=cg.uv(js,xr,.01)
        gaps.append([float(abs(aa-bb).max()) for aa,bb in zip(a,b)])
    out[case]['model_gap_refinement']=dict(h=[.1,.05,.025],errors=gaps,orders=np.log2(np.array(gaps[:-1])/np.array(gaps[1:])).tolist())
(HERE/'independent_checks.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
