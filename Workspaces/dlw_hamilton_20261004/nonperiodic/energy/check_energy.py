"""Audits actual paper A/B/C h-soliton Hamilton density integrability.

Finite x quadratures support analytic rational one-soliton calculations only;
the divergence proofs are in ENERGY_NOTES.md, not inferred from truncation.
"""
from pathlib import Path
import json
import sys
import sympy as sp
import numpy as np
from scipy.integrate import quad
from scipy.special import expit, logsumexp

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
sys.path.insert(0,str(ROOT/'Workspaces/dlw_two_soliton_20260929'))
from reference import CASES,TwoExact

def rational_integral(p,q,a,h):
    y=sp.symbols('y',positive=True)
    s=p+q; P=p-a; Q=q+a
    rho=-(P+h/2)/(Q-h/2)
    mu=(P+h/2)/(P-h/2)*(Q+h/2)/(Q-h/2)
    sig=lambda b:b*y/(1+b*y)
    deriv=lambda b:b*y/(1+b*y)**2
    u=s*(2*sig(rho)-sig(1)-sig(mu))
    ux=s*s*(2*deriv(rho)-deriv(1)-deriv(mu))
    omega=4*s/h*(sig(mu)-sig(1))
    w=omega-4; U=u+2*a
    r=2*s*s*(deriv(1)+deriv(mu))
    vacuum=-8*a*a-sp.Rational(2,3)*h*h
    density=sp.cancel(U*U*w/2+h*h*w**3/96+w*ux+w*r/2-vacuum)
    integrand=sp.cancel(density/(s*y))
    parts=sp.apart(integrand,y)
    # Integrate monic rational poles explicitly, retaining logs separately.
    # This avoids simplification into huge single logarithmic integers.
    finite=[]; residues=[]
    for term in sp.Add.make_args(parts):
        num,den=term.as_numer_denom()
        leading,factors=sp.factor_list(den,y)
        assert len(factors)==1 and sp.degree(num,y)==0
        pole,k=factors[0];assert sp.degree(pole,y)==1
        slope=sp.Poly(pole,y).coeff_monomial(y)
        offset=pole.subs(y,0);C=num/leading
        if k==1:
            residues.append(C/slope)
            finite.append(C/slope*sp.log(slope/offset))
        else:finite.append(C/(slope*(k-1)*offset**(k-1)))
    assert sp.simplify(sum(residues))==0
    ans=sum(finite)
    mass_u=2*sp.log(rho)-sp.log(mu)
    energy_gamma=ans+8*a*mass_u
    # Direct numerical integration in the phase coordinate avoids using the
    # same antiderivative as the evaluation check.
    evaluate=sp.lambdify(y,density,'numpy')
    numeric=quad(lambda phase:float(evaluate(np.exp(phase)))/float(s),-45,45,
                 epsabs=1e-10,epsrel=1e-11,limit=400)[0]
    return {'s':str(s),'rho':str(rho),'mu':str(mu),'chi':float(sp.log(mu)),
            'vacuum_density':str(vacuum),'per_site_integral_exact':str(ans),
            'per_site_integral':float(ans.evalf(30)),'quadrature':numeric,
            'mass_u_exact':str(mass_u),'mass_u':float(mass_u.evalf(30)),
            'natural_gamma_per_site_integral_exact':str(energy_gamma),
            'natural_gamma_per_site_integral':float(energy_gamma.evalf(30)),
            'check_error':abs(float(ans.evalf(30))-numeric),
            'density_at_phase_zero':float(density.subs(y,1))}

def density_two(ref,j,x,t):
    # x derivative moments/covariances directly from the native positive tau.
    def m(k,f=False):
        _,weight=ref.tau([k],[x],t,f)
        return ref.mean(weight,0)[0,0],ref.cov(weight,0,0)[0,0]
    mf,ff=m(j,True);mg,gg=m(j);mg1,gg1=m(j+1)
    u=2*mf-mg-mg1;ux=2*ff-gg-gg1
    w=4/ref.h*(mg1-mg)-4;U=u+2*ref.case.a
    r=2*(gg+gg1)
    vacuum=-8*ref.case.a**2-2/3*ref.h**2
    return .5*U*U*w+ref.h**2*w**3/96+w*ux+.5*w*r-vacuum

def two_integral(ref,j,t):
    centers=-(ref.chi*j+ref.T*t+np.log(ref.coeff[1:3]))/ref.S
    breaks=sorted(set([min(centers)-45,max(centers)+45,*centers]))
    result=sum(quad(lambda x:density_two(ref,j,x,t),l,r,
                    epsabs=2e-9,epsrel=1e-10,limit=250)[0]
               for l,r in zip(breaks[:-1],breaks[1:]))
    return result

def main():
    h=sp.Rational(1,8);a=sp.Integer(2)
    singles={'A':(sp.Integer(1),sp.Integer(2)),
             'B':(sp.Integer(4),sp.Integer(-3)),
             'C_component_1':(sp.Integer(6),sp.Integer(-5))}
    out={'h':str(h),'a':str(a),'single':{}}
    for label,(p,q) in singles.items():
        out['single'][label]=rational_integral(p,q,a,h)
    ref=TwoExact(CASES['fig3'],float(h),continuous=False)
    out['two']={'chi':ref.chi.tolist(),'x_per_site_slope':(-ref.chi/ref.S).tolist(),
                'asymptotic_per_site_integral':out['single']['B']['per_site_integral']+
                    out['single']['C_component_1']['per_site_integral'],
                'asymptotic_natural_gamma_per_site_integral':
                    out['single']['B']['natural_gamma_per_site_integral']+
                    out['single']['C_component_1']['natural_gamma_per_site_integral'],
                'samples':[{'j':j,'t':t,'per_site_integral':two_integral(ref,j,t)}
                           for t in (0.,.01) for j in (-1000,-250,-25,0,25,250,1000)]}
    (HERE/'energy_checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(out,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
