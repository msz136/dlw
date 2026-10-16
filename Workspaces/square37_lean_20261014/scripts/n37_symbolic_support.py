"""Recompute conditional support identities and isolate the relevant crossing.

This certifies algebraic identities and rational signs only, not global packing
optimality. The geometric hypotheses are documented in the associated note.
"""
from fractions import Fraction as F
from pathlib import Path
from math import isqrt
import json, hashlib
import sympy as S
import mpmath as mp

BASE=Path(__file__).resolve().parents[1]

class I:
    def __init__(self,a,b=None):self.a=F(a);self.b=F(a if b is None else b)
    def __add__(self,o):
        o=o if isinstance(o,I) else I(o);return I(self.a+o.a,self.b+o.b)
    __radd__=__add__
    def __neg__(self):return I(-self.b,-self.a)
    def __sub__(self,o):return self+-o if isinstance(o,I) else self+I(-o)
    def __rsub__(self,o):return I(o)+-self
    def __mul__(self,o):
        o=o if isinstance(o,I) else I(o);v=[x*y for x in (self.a,self.b) for y in(o.a,o.b)];return I(min(v),max(v))
    __rmul__=__mul__
    def __truediv__(self,o):
        o=o if isinstance(o,I) else I(o)
        assert not (o.a<=0<=o.b)
        return self*I(1/o.b,1/o.a)
    def __pow__(self,n):
        z=I(1)
        for _ in range(n):z=z*self
        return z
    def serial(self):return {'lo':str(self.a),'hi':str(self.b),'lo_float':float(self.a),'hi_float':float(self.b)}

def horner(expr,var,value,other=None):
    poly=S.Poly(expr,var);acc=I(0)
    for co in poly.all_coeffs():
        if other:
            z=S.Poly(co,other[0]); ci=I(0)
            for n in z.all_coeffs():ci=ci*other[1]+F(int(n.p),int(n.q))
        else:ci=I(F(int(co.p),int(co.q)))
        acc=acc*value+ci
    return acc

def main():
    L,t,r,c,s,q=S.symbols('L t r c s q')
    f=((2*L-9)**2+1)*t*t-12*(2*L-9)*t+34
    g=2*(L-5)**2*t*t-14*(L-5)*t+20+r
    Q=6*L**4-(208+64*r)*L**3+(2058+850*r)*L**2-(7936+3658*r)*L+11163+5502*r
    P=36*L**8-2496*L**7+59768*L**6-733760*L**5+5289248*L**4-23462672*L**3+63458276*L**2-96673872*L+64068561
    resultant_identity=S.rem(S.resultant(f,g,t)-(24-16*r)*Q,r*r-2,r)
    norm_identity=S.rem(Q*Q.subs(r,-r)-P,r*r-2,r)
    assert resultant_identity==0 and norm_identity==0
    F1=(3+4*c+5*s)/(c+s)
    F2=(6+8*c+10*s*(c-s)+r)/(2+2*s*(c-s))
    circle=c*c+s*s-1
    left_sum=(c-s)*(c+3*s+S.Rational(3,2)-s*L)+(c+s)*(s+2*c+S.Rational(3,2))
    left_A=3+3*c+s*(c-s)*(5-L)
    assert S.expand(left_sum-left_A-3*circle)==0
    dF1=-s*S.diff(F1,c)+c*S.diff(F1,s)
    derivative1_residual=S.together(dF1-(1-3*(c-s))/(c+s)**2).as_numer_denom()[0]
    assert S.rem(derivative1_residual,circle,c)==0
    k=2-r/2
    H=(c-s)*(4*c*c-k*(c+s))+2*k*c*s
    dF2=-s*S.diff(F2,c)+c*S.diff(F2,s)
    derivative2_residual=S.together(dF2+H/(1+s*(c-s))**2).as_numer_denom()[0]
    assert S.rem(derivative2_residual,circle,c)==0
    diff=S.factor((F1-F2).subs({c:(1-q*q)/(1+q*q),s:2*q/(1+q*q)}))
    numerator,denominator=S.fraction(diff)
    mp.mp.dps=90
    numfun=S.lambdify(q,numerator.subs(r,S.sqrt(2)),'mpmath')
    qr=mp.findroot(numfun,('0.38','0.39'))
    cr=(1-qr*qr)/(1+qr*qr);sr=2*qr/(1+qr*qr)
    lr=(3+4*cr+5*sr)/(cr+sr)
    scale=10**80;rt=isqrt(2*scale*scale);ri=I(F(rt,scale),F(rt+1,scale))
    assert ri.a*ri.a<2<ri.b*ri.b
    scaleq=10**50; qi_floor=int(mp.floor(qr*scaleq));ql=F(qi_floor,scaleq);qu=F(qi_floor+1,scaleq)
    qsigns=[horner(numerator,q,I(z),(r,ri)) for z in (ql,qu)]
    assert qsigns[0].b<0<qsigns[1].a
    qbox=I(ql,qu)
    # These rational interval facts connect the unique positive N root to the
    # correct physical orientation regime; no decimal angle inference is used.
    assert 0<ql<qu<ri.a-1 and qu<1
    cs_difference=(1-qbox*qbox-2*qbox)/(1+qbox*qbox)
    assert cs_difference.a>0 and cs_difference.b<F(1,3)
    coefficient4=4-ri;coefficient2=12-2*ri
    assert coefficient4.a>0 and coefficient2.a>0
    nprime=horner(S.diff(numerator,q),q,qbox,(r,ri))
    assert nprime.a>0
    diff_den=horner(denominator,q,qbox)
    assert diff_den.a>0
    scalel=10**40;li_floor=int(mp.floor(lr*scalel));ll=F(li_floor,scalel);lu=F(li_floor+1,scalel)
    lsigns=[horner(P,L,I(z)) for z in (ll,lu)]
    derivative=horner(S.diff(P,L),L,I(ll,lu))
    assert lsigns[0].a*lsigns[1].a<0 and (derivative.a>0 or derivative.b<0)
    Limage=(7-qbox*qbox+10*qbox)/(1+2*qbox-qbox*qbox)
    assert ll<Limage.a<=Limage.b<lu
    source_manifest=BASE/'references/n37/source_manifest.json'
    record={'scope':'Exact algebraic identities and rational interval evidence for existence and uniqueness of the conditional two-support crossing. Continuous-polynomial IVT supplies existence; positive quartic coefficients supply unique positive root. Not an unrestricted lower bound.','script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'source_manifest_sha256':hashlib.sha256(source_manifest.read_bytes()).hexdigest(),'resultant_identity_zero':True,'norm_identity_zero':True,'left_support_sum_identity_zero':True,'F1_derivative_identity_mod_circle_zero':True,'F2_derivative_identity_mod_circle_zero':True,'quartic':str(Q),'degree_eight':str(P),'crossing_numerator_half_angle':str(numerator),'crossing_denominator_half_angle':str(denominator),'sqrt2_interval':ri.serial(),'q_interval':{'lo':str(ql),'hi':str(qu)},'crossing_numerator_at_q_endpoints':[z.serial() for z in qsigns],'positive_coefficients':{'q4':coefficient4.serial(),'q2':coefficient2.serial()},'crossing_derivative_on_q_interval':nprime.serial(),'crossing_denominator_on_q_interval':diff_den.serial(),'q_regime_exact':{'q_lower_positive':True,'q_upper_below_sqrt2_minus_1':True,'c_minus_s_positive_and_below_1_over_3':True,'c_minus_s_interval':cs_difference.serial()},'L_root_interval':{'lo':str(ll),'hi':str(lu)},'F1_image_of_q_interval':Limage.serial(),'q_to_L_bridge_exact':True,'P_at_L_endpoints':[z.serial() for z in lsigns],'P_derivative_over_L_interval':derivative.serial(),'numeric_q':str(qr),'numeric_L':str(lr),'numeric_theta_degrees':str(2*mp.atan(qr)*180/mp.pi)}
    (BASE/'analysis/n37_symbolic_support.json').write_text(json.dumps(record,indent=2),encoding='utf8')
    print(json.dumps({k:v for k,v in record.items() if k in ['resultant_identity_zero','norm_identity_zero','crossing_numerator_half_angle','numeric_L','numeric_theta_degrees','L_root_interval']},indent=2))

if __name__=='__main__':main()
