"""A priori uniform O(h^4) residual remainder constants for single solitons.

Taylor integral remainders and exact supremum enclosures are combined.
This bounds the finite-h equation residual, not the time-evolved error.
"""
from pathlib import Path
import json
import sympy as s
from single_bounds import CASES,fields,extrema,outward

HERE=Path(__file__).resolve().parent
z=s.symbols('s',real=True)
Q=s.Rational
base=json.loads((HERE/'single_bounds.json').read_text(encoding='utf-8'))
out={'h_max':'1/8','domain':'All x,y,t on each continuous single soliton',
     'statement':'For 0<h<=1/8: ||Residual_i(h)-h^2 R_i||_infinity <= M_i h^4.',
     'cases':{}}

for name,(a,p,q) in CASES.items():
    k,ell,gamma,_,_,_=fields(a,p,q)
    f=gamma*z/(1+(gamma-1)*z)
    D=lambda w:s.cancel(z*(1-z)*s.diff(w,z))
    u=s.cancel(2*k*(f-z));v=s.cancel(2*k*ell*(D(f)+D(z)))
    cache={}
    def der(w,nx,ny):
        for _ in range(nx+ny):w=D(w)
        return s.cancel(k**nx*ell**ny*w)
    def norm(w):
        w=s.cancel(w)
        key=str(w)
        if key not in cache:
            rec,b=extrema(w);cache[key]=(b['abs_hi'],rec['abs_bound'])
        return cache[key][0]
    N=lambda w,nx,ny:norm(der(w,nx,ny))
    w=s.cancel(v-der(u,0,1))
    G=(w-4)**2/32
    hmax=Q(1,8)
    # W=w-e, e=(delta_0-partial_y)u. Each derivative of e is bounded
    # by h^2/6 times the corresponding third-y derivative of u.
    e= { (nx,ny):N(u,nx,ny+3)/6 for nx,ny in ((0,0),(1,0),(0,1),(1,1)) }
    wdiff=(N(w,0,1)*e[(1,0)]+norm(w-4)*e[(1,1)]
           +e[(0,1)]*N(w,1,0)+e[(0,0)]*N(w,1,1)
           +hmax**2*(e[(0,1)]*e[(1,0)]+e[(0,0)]*e[(1,1)]))/16
    mfd1=N(v,2,4)/480
    mfd2=N(u,2,5)/120
    msd1=mfd1+N(G,1,3)/24+wdiff+N(u,2,5)/32
    product=(N(u*u/2,1,5)+N(u,1,0)*N(u,0,5)+norm(u)*N(u,1,5))/120
    msd2=mfd2+product+N(G,1,3)/6+wdiff+N(w,2,4)/48+N(u,2,5)/24
    row={'M':{},'normalized_finite_h_residual_bound':{},'derivative_norm_count':len(cache)}
    for key,m in {'SD_R1':msd1,'SD_R2':msd2,'FD_R1':mfd1,'FD_R2':mfd2}.items():
        coef=base['cases'][name]['residual'][key]['abs_bound_exact']
        lo,hi=map(Q,coef)
        row['M'][key]={'upper':outward(m,True,places=9),'exact':str(m)}
        row['normalized_finite_h_residual_bound'][key]=[
            outward(max(0,lo-m*hmax*hmax),places=9),outward(hi+m*hmax*hmax,True,places=9)]
        print(name,key,'M',row['M'][key]['upper'],'Residual/h^2',row['normalized_finite_h_residual_bound'][key],flush=True)
    out['cases'][name]=row
    (HERE/'remainder_bounds.json').write_text(json.dumps(out,indent=2),encoding='utf-8')

