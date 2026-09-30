"""Exact rational enclosures of the original DLW single-soliton h^2 coefficients.

Only analytic x,t derivatives and the y semidiscretization are considered.
No old data are verified and no PDE trajectories are recomputed.
"""
from pathlib import Path
import json
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
import sympy as s

HERE = Path(__file__).resolve().parent
z = s.symbols('s', real=True)
Q = s.Rational
CASES = {'A': (Q(2), Q(1), Q(2)), 'B': (Q(2), Q(4), Q(-3))}


def exp_positive_bounds(a, terms=90):
    """Exact rational enclosure of exp(a), for a >= 0."""
    assert 0 <= a < terms+2
    value, term = Q(1), Q(1)
    for n in range(1,terms+1):
        term *= a/n
        value += term
    next_term = term*a/(terms+1)
    return value, value+next_term/(1-a/(terms+2))


def interval_poly(poly, interval):
    lo, hi = interval
    out = (Q(0), Q(0))
    for c in poly.all_coeffs():
        vals = [out[0]*lo, out[0]*hi, out[1]*lo, out[1]*hi]
        out = (min(vals)+c, max(vals)+c)
    return out


def rational_interval(num, den, interval):
    nl, nu = interval_poly(num, interval)
    dl, du = interval_poly(den, interval)
    if dl <= 0 <= du:
        raise ValueError('Denominator interval contains zero')
    vals = [nl/dl, nl/du, nu/dl, nu/du]
    return min(vals), max(vals)


def outward(value, upper=False, places=12):
    with localcontext() as ctx:
        ctx.prec = 100
        dec = Decimal(int(s.numer(value))) / Decimal(int(s.denom(value)))
        return str(dec.quantize(Decimal(1).scaleb(-places),
                               rounding=ROUND_CEILING if upper else ROUND_FLOOR))


def extrema(expr):
    expr = s.cancel(expr)
    n, d = s.fraction(expr)
    num, den = s.Poly(n,z), s.Poly(d,z)
    # A Sturm isolation checks the complete critical-point set.
    deriv = s.Poly(s.fraction(s.cancel(s.diff(expr,z)))[0],z)
    assert den.count_roots(0,1)==0 and den.eval(0)!=0 and den.eval(1)!=0
    roots = [] if deriv.is_zero else deriv.intervals(eps=Q(1,10**48))
    intervals = [(Q(0),Q(0)),(Q(1),Q(1))]
    intervals += [(l,r) for (l,r), multiplicity in roots if l>0 and r<1]
    enclosures = [rational_interval(num,den,iv) for iv in intervals]
    witnesses = [((l+r)/2, expr.subs(z,(l+r)/2)) for l,r in intervals]
    abs_lower = max(abs(v) for _,v in witnesses)
    abs_upper = max(max(abs(l),abs(r)) for l,r in enclosures)
    min_lo = min(l for l,r in enclosures)
    min_hi = min(v for _,v in witnesses)
    max_lo = max(v for _,v in witnesses)
    max_hi = max(r for l,r in enclosures)
    assert abs_upper >= abs_lower and abs_upper-abs_lower < Q(1,10**22)
    assert min_hi-min_lo < Q(1,10**22) and max_hi-max_lo < Q(1,10**22)
    return {'expression':str(expr), 'numerator':str(n), 'denominator':str(d),
            'derivative_numerator':str(deriv.as_expr()),
            'abs_bound': [outward(abs_lower),outward(abs_upper,True)],
            'min_bound':[outward(min_lo),outward(min_hi,True)],
            'max_bound':[outward(max_lo),outward(max_hi,True)],
            'abs_bound_exact':[str(abs_lower),str(abs_upper)],
            'critical_intervals':[[str(l),str(r)] for l,r in intervals],
            'critical_value_enclosures':[[str(l),str(r)] for l,r in enclosures],
            'witnesses':[[str(t),str(v)] for t,v in witnesses]}, {
                'abs_lo':abs_lower,'abs_hi':abs_upper,
                'min_lo':min_lo,'min_hi':min_hi,'max_lo':max_lo,'max_hi':max_hi,
                'min_witness':min(witnesses,key=lambda item:item[1]),
                'max_witness':max(witnesses,key=lambda item:item[1])}


def fields(a,p,q):
    k, ell = p+q, 1/(p-a)+1/(q+a)
    gamma = -(p-a)/(q+a)
    f = gamma*z/(1+(gamma-1)*z)
    D = lambda w: s.cancel(z*(1-z)*s.diff(w,z))
    u = s.cancel(2*k*(f-z))
    v = s.cancel(2*k*ell*(D(f)+D(z)))
    def diff(w,n):
        for _ in range(n):w=D(w)
        return w
    w = s.cancel(v-ell*D(u))
    nonlinear = k*ell*diff((w-4)**2/32,2)
    product = k*ell**3*D(D(u)*diff(u,2))/2
    vterm, uterm = k*k*ell*ell*diff(v,4), k*k*ell**3*diff(u,5)
    residual = {'SD_R1':s.cancel(nonlinear+vterm/12-uterm/4),
                'SD_R2':s.cancel(nonlinear+product+vterm/4-uterm/12),
                'FD_R1':s.cancel(vterm/12),'FD_R2':s.cancel(uterm/6)}
    # R1 = partial_y B. With equal physical initial fields and a fixed u base
    # at y0, the leading u-error velocity is -(B(y)-B(y0)).
    primitive = {'SD':s.cancel(k*D((w-4)**2/32)+k*k*ell*diff(v,3)/12-k*k*ell*ell*diff(u,4)/4),
                 'FD':s.cancel(k*k*ell*diff(v,3)/12)}
    for model in primitive:
        assert s.cancel(ell*D(primitive[model])-residual[model+'_R1']) == 0
    C=(1/(p-a)**3+1/(q+a)**3)/12
    E=(1/(q+a)**2-1/(p-a)**2)/8
    # Exact-family coefficient, which has different initial data from the
    # equal-physical-initial-fields comparison.
    coeff = {}
    for y in (Q(-3,2),Q(3,2)):
        coeff['u_y'+str(y)]=s.cancel(2*k*((y*C+E)*D(f)-y*C*D(z))-k*ell**2*diff(z,2)/4)
        coeff['v_y'+str(y)]=s.cancel(2*k*C*(D(f)+D(z))+2*k*ell*((y*C+E)*diff(f,2)+y*C*diff(z,2))+k*ell**3*(diff(f,3)/3-5*diff(z,3)/12))
    return k,ell,gamma,residual,primitive,coeff


def main():
    out={'scope':'Global x; y in [-3/2,3/2]; analytic x,t; pure y h^2 coefficients.',
         'proof_method':'Exact rational Sturm root isolation; rational interval Horner evaluation; outward decimal rounding.',
         'cases':{}}
    for name, pars in CASES.items():
        a,p,q=pars
        k,ell,gamma,residual,primitive,coeff = fields(*pars)
        row={'a':str(a),'p':str(p),'q':str(q),'k':str(k),'ell':str(ell),'gamma':str(gamma),
             'residual':{},'primitive':{},'equal_initial_velocity':{},'exact_family':{}}
        for key,expr in residual.items():
            rec,intern=extrema(expr);row['residual'][key]=rec
            print(name,key,rec['abs_bound'],flush=True)
        for model,expr in primitive.items():
            rec,intern=extrema(expr);row['primitive'][model]=rec
            min_s,min_v=intern['min_witness'];max_s,max_v=intern['max_witness']
            odds1,odds2=max_s/(1-max_s),min_s/(1-min_s)
            odds_ratio=max(odds1/odds2,odds2/odds1)
            phase_distance=s.log(odds_ratio)
            exp_lo,exp_hi=exp_positive_bounds(3*abs(ell))
            assert odds_ratio < exp_lo or odds_ratio > exp_hi
            feasible=bool(odds_ratio < exp_lo)
            # The oscillation is always an upper bound. A rational pair with
            # |phase difference| <= 3|ell| supplies an attainable lower bound.
            if not feasible:
                pairs=[]
                for i in range(1,100):
                    t0=Q(i,100)
                    # Choose an exact rational odds factor safely inside the
                    # physical phase window; exp(3 ell) is checked below.
                    odds_factor=Q(1,8) if name=='A' else Q(1,4)
                    t1=odds_factor*t0/(1-t0+odds_factor*t0)
                    pairs.append(abs(expr.subs(z,t0)-expr.subs(z,t1)))
                witness_lower=max(pairs)
                assert 1/odds_factor < exp_lo
            else:witness_lower=max_v-min_v
            upper=intern['max_hi']-intern['min_lo']
            row['equal_initial_velocity'][model+'_u']={
                'bound':[outward(witness_lower),outward(upper,True)],
                'oscillation_attainable':feasible,
                'extrema_phase_distance':str(phase_distance.evalf(25)),
                'available_phase_span':str(3*abs(ell)),
                'meaning':'Norm of -B(y)+B(y0); y0=-3/2. Pure-y leading physical u error velocity at t=0.'}
            row['equal_initial_velocity'][model+'_v']={
                'bound':row['residual'][model+'_R2']['abs_bound'],
                'meaning':'Norm of -R2; pure-y leading physical v error velocity at t=0.'}
        for key,expr in coeff.items():
            rec,_=extrema(expr);row['exact_family'][key]=rec
        out['cases'][name]=row
    (HERE/'single_bounds.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    print('SAVED single_bounds.json',flush=True)


if __name__=='__main__':main()
