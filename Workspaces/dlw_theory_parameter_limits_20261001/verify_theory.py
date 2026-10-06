"""Frozen T01 symbolic and directed finite-h checks; no PDE evolution."""
from pathlib import Path
import hashlib
import json
import sympy as s
import mpmath as mp

HERE = Path(__file__).resolve().parent
frozen = json.loads((HERE / 'THEORY_FREEZE.json').read_text(encoding='utf-8'))
checks = []

def zero(name, expression):
    value = s.factor(s.cancel(expression))
    assert value == 0, (name, value)
    checks.append({'name': name, 'residual': '0'})

A, G, al, be, m, d = s.symbols('A G alpha beta m d', nonzero=True)
x, y = A/(1+G), -G*A/(1+G)
L = x+y
C = (G**2+G+1)/(12*(G+1)**2)
T = (1+G+G**2+G**3+G**4)/(80*(G+1)**4)
zero('fixed_Gamma_inverse_difference', x-y-A)
zero('fixed_Gamma_relation', -y/x-G)
zero('normalized_curvature', (x**3+y**3)/(12*L)-C*A**2)
zero('normalized_alpha', (x**2-y**2)/L-A)
zero('normalized_quintic', (x**5+y**5)/(80*L)-T*A**4)
candidate = be+al*A+C*A**2
optimal = candidate.subs({al:-2*C*m,be:C*(m*m-d*d/2)})
zero('minimax_candidate', optimal-C*((A-m)**2-d*d/2))
zero('second_difference_lower_bound', candidate.subs(A,m-d)-2*candidate.subs(A,m)+candidate.subs(A,m+d)-2*C*d*d)
for point, label, sign in [(m-d,'left',1),(m,'middle',-1),(m+d,'right',1)]:
    zero('alternation_'+label, optimal.subs(A,point)-sign*C*d*d/2)
R = 5+2*s.sqrt(5)
zero('tenfold_threshold', (1-1/R)**2/s.Integer(8)-s.Rational(1,10))
K = (G**2-1)/(G*A)
zero('scale_independent_KL', K*L+(G-1)**2/G)
e4_direct = (al*al*(x**3+y**3)+be*al*(x*x-y*y)+be*(x**3+y**3)/4+al*(x**4-y**4)/4+(x**5+y**5)/80)/L
e4_reduced = 12*C*al*al*A*A+al*be*A+3*C*be*A*A+al*(1+G*G)*A**3/(4*(1+G)**2)+T*A**4
zero('fourth_order_coefficient',e4_direct-e4_reduced)
a1,a2,F,B = s.symbols('a1 a2 F B', nonzero=True)
v1=F/a1+al*B/a1**2
v2=F/a2+al*B/a2**2
zero('common_initial_velocity_endpoint_elimination', a2*a2*v2-a1*a1*v1-(a2-a1)*F)

mp.mp.dps=75
directed=[]
for spec in frozen['directed_checks']['cases']:
    gamma=mp.mpf(spec['Gamma']); lo,hi=map(mp.mpf,spec['A_interval'])
    ca=(gamma**2+gamma+1)/(12*(gamma+1)**2)
    mid=(lo+hi)/2; half=(hi-lo)/2
    alpha=-2*ca*mid; beta=ca*(mid**2-half**2/2)
    assert s.Rational(spec['alpha']) == s.simplify(-2*C*m).subs({G:spec['Gamma'],m:s.Rational(sum(spec['A_interval']),2)})
    assert s.Rational(spec['beta']) == (C*(m*m-d*d/2)).subs({G:spec['Gamma'],m:s.Rational(sum(spec['A_interval']),2),d:s.Rational(spec['A_interval'][1]-spec['A_interval'][0],2)})
    for hs in spec['h']:
        h=mp.mpf(str(hs)); H=h*(1+beta*h*h); mu=alpha*h*h
        rows=[]
        for aa in [lo,mid,hi]:
            xx=aa/(1+gamma); yy=-gamma*aa/(1+gamma); ll=xx+yy
            def defect(alpha_,beta_):
                mh=alpha_*h*h; hh=h*(1+beta_*h*h)
                up=xx/(1-mh*xx); vq=yy/(1+mh*yy)
                assert abs(hh*up/2)<1 and abs(hh*vq/2)<1
                return 2*(mp.atanh(hh*up/2)+mp.atanh(hh*vq/2))/(h*ll)-1
            actual=defect(alpha,beta)
            leading=beta+alpha*aa+ca*aa*aa
            tgamma=(1+gamma+gamma**2+gamma**3+gamma**4)/(80*(1+gamma)**4)
            fourth=12*ca*alpha**2*aa**2+alpha*beta*aa+3*ca*beta*aa**2+alpha*(1+gamma**2)*aa**3/(4*(1+gamma)**2)+tgamma*aa**4
            remainder4=(actual-h*h*leading)/h**4
            rows.append({'A':str(aa),'D_h':mp.nstr(actual,22),'D_h_over_h2':mp.nstr(actual/h**2,22),'leading':mp.nstr(leading,22),'fourth_remainder_quotient':mp.nstr(remainder4,22),'fourth_coefficient':mp.nstr(fourth,22),'D_original':mp.nstr(defect(0,0),22)})
        directed.append({'Gamma':str(gamma),'interval':[str(lo),str(hi)],'h':str(h),'alpha':mp.nstr(alpha,20),'beta':mp.nstr(beta,20),'rows':rows,'meaning':'Three predeclared points only; not a certificate of the interval supremum.'})

contract=json.loads((HERE/'CERTIFICATE_CONTRACT.json').read_text(encoding='utf-8'))
certificates=[]
for spec in contract['phase_certificates']:
    gamma=s.Rational(contract['Gamma']); lo,hi=map(s.Rational,spec['interval'])
    aa=s.Rational(contract['parameter_box']['abs_alpha_max']); bb=s.Rational(contract['parameter_box']['abs_beta_max'])
    h0=s.Rational(contract['uniform_h0']); hm=s.Rational(spec['h_max']); eps=h0*h0
    cc=(gamma*gamma+gamma+1)/(12*(gamma+1)**2); tt=sum(gamma**j for j in range(5))/(80*(gamma+1)**4)
    ss=max(1,gamma)/(1+gamma)*hi; rho=aa*eps*ss; rb=1+bb*eps; delta=(1-rho)**2; q=h0*rb*ss/(2*(1-rho))
    assert rho<1 and q<1 and bb*eps<1
    base=cc*hi*hi; jj=gamma/(1+gamma)**2*hi**2
    br=bb*(3+3*bb*eps+bb**2*eps**2)
    bound=(aa*bb*hi+12*aa**2*base+eps*aa**2*jj*(bb+aa*hi))/delta+base*(br+aa*hi+eps*aa**2*jj)/delta**2+aa*ss**3/(2*delta)+rb**5*tt*hi**4/(delta**3*(1-q*q))
    original_bound=tt*hi**4/(1-(h0*ss/2)**2)
    optimum=cc*(hi-lo)**2/8
    alpha_star=-cc*(lo+hi); beta_star=cc*((lo+hi)**2/4-(hi-lo)**2/8)
    assert abs(alpha_star)<=aa and abs(beta_star)<=bb
    if hi==2:
        margin=base/10-optimum-hm**2*bound
        status='certified_tenfold_for_fixed_Chebyshev_pair'
    else:
        margin=optimum-hm**2*bound-(base+hm**2*original_bound)/10
        status='certified_no_tenfold_for_entire_parameter_box'
    assert margin>0, margin
    certificates.append({'interval':spec['interval'],'h_max':str(hm),'status':status,'B_exact':str(bound),'B_decimal':str(s.N(bound,12)),'B0_exact':str(original_bound),'E0_exact':str(base),'E_star_exact':str(optimum),'strict_margin_exact':str(margin),'strict_margin_decimal':str(s.N(margin,12)),'uniform_branch':{'rho':str(rho),'q':str(q),'beta_h0_squared':str(bb*eps)}})

result={'status':'passed','exact_check_count':len(checks),'exact_checks':checks,'directed':directed,'finite_h_certificates':certificates,'new_pde_runs':0,'freeze_sha256':hashlib.sha256((HERE/'THEORY_FREEZE.json').read_bytes()).hexdigest(),'certificate_contract_sha256':hashlib.sha256((HERE/'CERTIFICATE_CONTRACT.json').read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'meaning':'Proof audit, directed formula checks, and exact rational interval certificates. No empirically selected parameters or propagation certificate.'}
(HERE/'theory_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':result['status'],'exact_check_count':len(checks),'directed_cases':len(directed),'new_pde_runs':0}))
