"""Exact Fourier witness on one fixed Casimir leaf of the periodic bracket.

Fields are periodic trigonometric polynomials. Four parameters alter only
cos(x) modes of reduced p and g, hence keep every x-average of p and g fixed.
Dual rational arithmetic differentiates four invariant functionals exactly.
"""
import json
from pathlib import Path
import sympy as s

I = s.I
Q = s.Rational
NDUAL = 5

def dual(value, d=None):
    v = [s.sympify(value),0,0,0,0]
    if d is not None: v[d+1] = s.Integer(1)
    return tuple(v)

ZERO = dual(0)
ONE = dual(1)

def add(a,b): return tuple(s.expand(x+y) for x,y in zip(a,b))
def neg(a): return tuple(-x for x in a)
def scale(a,b): return tuple(s.expand(x*b) for x in a)
def prod(a,b):
    return (s.expand(a[0]*b[0]),)+tuple(s.expand(a[0]*b[k]+a[k]*b[0]) for k in range(1,NDUAL))

def fc(value): return {0:dual(value)}
def fa(a,b):
    out = dict(a)
    for k,v in b.items(): out[k] = add(out.get(k,ZERO),v)
    return {k:v for k,v in out.items() if any(v)}
def fs(a,c): return {k:scale(v,c) for k,v in a.items() if any(v)}
def fm(a,b):
    out = {}
    for k,v in a.items():
        for j,w in b.items(): out[k+j] = add(out.get(k+j,ZERO),prod(v,w))
    return {k:v for k,v in out.items() if any(v)}
def fd(a,n=1): return {k:scale(v,(I*k)**n) for k,v in a.items() if k or not n}
def fp(a,n):
    out=fc(1)
    for _ in range(n):out=fm(out,a)
    return out
def fsum(items):
    out={}
    for a in items:out=fa(out,a)
    return out

def pmul(a,b,lo=-5):
    out = {}
    for i,ai in a.items():
        for j,bj in b.items():
            for r in range(max(-1,i+j-lo)+1):
                c = s.binomial(i,r)
                if c:
                    power = i+j-r
                    out[power] = fa(out.get(power,{}),fs(fm(ai,fd(bj,r)),c))
    return out

def main():
    vals = [Q(1,5),Q(-2,5),Q(1,6),Q(1,7)]
    modes = [{1:scale(dual(v,k),Q(1,2)),-1:scale(dual(v,k),Q(1,2))} for k,v in enumerate(vals)]
    ps = [fa(fc(-3),modes[0]), fa(fc(0),modes[1]), fa(fc(3),fs(fa(modes[0],modes[1]),-1))]
    gs = [fa(fc(1),modes[2]), fa(fc(2),modes[3]), fa(fc(3),fs(fa(modes[2],modes[3]),-1))]
    mean_u = fs(fa(fc(12),fs(fa(fa(fm(ps[0],gs[0]),fm(ps[1],gs[1])),fm(ps[2],gs[2])),-1)),Q(1,6))
    us = [fa(p,mean_u) for p in ps]
    pp = {0:fc(1)}
    for u,g in zip(us,gs):
        b = fs(fa(u,fs(g,-1)),Q(1,2))
        st = {0:fc(1),-1:fs(g,-1)}
        for n in range(1,5): st[-n-1] = fa(fm(b,st[-n]),fs(fd(st[-n]),-1))
        pp = pmul(st,pp)
    assert pp[-1] == fc(-6)
    assert pp[-2] == fc(12)
    p3,p4,p5 = pp[-3],pp[-4],pp[-5]
    # At G=6,T=12, a=-6,b=12. Exact representatives from PDO inversion.
    rho2 = fa(fa(fs(p3,Q(4,3)),fs(p4,Q(1,3))),fc(16))
    rho3 = fs(fa(fa(fa(fa(fs(p4,Q(2,3)),fs(p5,Q(1,6))),fs(fm(p3,p3),Q(1,18))),fs(p3,Q(10,3))),fc(32)),3)
    # Compare the independently constructed quintic invariant at this
    # exact Fourier point, including all four tangent derivatives.
    rh = s.Matrix([[0,Q(-1,6),Q(1,6)],[Q(1,6),0,Q(-1,6)],[Q(-1,6),Q(1,6),0]])
    avec = [fs(fsum(fs(fd(gs[k]),rh[j,k]) for k in range(3)),4) for j in range(3)]
    cvec = [fs(fsum(fs(fd(fm(us[k],gs[k])),rh[j,k]) for k in range(3)),4) for j in range(3)]
    ee, qq4, qq5 = [],[],[]
    beta=Q(1,2)
    for u,w,aa,cc in zip(us,gs,avec,cvec):
        ux,wx=fd(u),fd(w)
        ee.append(fsum([fs(fm(fp(u,2),w),Q(1,2)),fs(fp(w,3),beta/3),fm(w,ux),fs(fm(w,aa),Q(1,2))]))
        qq4.append(fsum([fs(fm(fp(u,3),w),Q(1,3)),fs(fm(u,fp(w,3)),2*beta/3),
                        fs(fm(fm(u,w),ux),2),fs(fm(ux,wx),Q(-4,3)),fm(fm(u,w),aa)]))
        qq5.append(fsum([
          fm(fp(u,4),w),fs(fm(fm(fp(u,2),w),ux),12),fs(fm(w,fp(ux,2)),-4),
          fs(fm(fm(u,ux),wx),-16),fs(fm(ux,fd(w,2)),8),fs(fm(fm(fp(u,2),w),aa),4),
          fs(fm(fm(w,ux),aa),4),fs(fm(fm(u,wx),aa),-4),fs(fm(w,fp(aa,2)),2),
          fs(fm(wx,fd(aa)),-4),fs(fm(fm(u,w),cc),2),fs(fm(fp(u,2),fp(w,3)),4*beta),
          fs(fp(w,5),4*beta**2/5),fs(fm(fp(w,3),ux),8*beta/3),
          fs(fm(w,fp(wx,2)),-8*beta),fs(fm(fp(w,3),aa),8*beta/3)]))
    h0=fs(fsum(ee),4)
    q4h=fs(fsum(qq4),4)
    q5h=fs(fsum(qq5),4)
    q5red=fa(q5h,fs(fp(h0,2),Q(-1,3)))
    predicted=fs(fsum([fs(q5red,Q(-1,128)),fs(q4h,Q(3,32)),fs(h0,Q(-1,2)),fc(Q(228,5))]),1)
    residual=fa(rho3,fs(predicted,-1))
    assert residual.get(0,ZERO)==ZERO, residual.get(0,ZERO)
    # H0 ≡ -8p3 modulo constants; mean U represents the old momentum.
    charges = [fs(mean_u,3),fs(p3,-8),rho2,rho3]
    jac = s.Matrix([list(c.get(0,ZERO)[1:]) for c in charges])
    det = s.factor(jac.det())
    assert det != 0
    result = {
      'passed': True,
      'N':3,'h':4,'G':6,'T':12,'period_x':'2*pi',
      'fixed_leaf': 'Every x-average of reduced p_j and g_j is fixed; only cos(x) amplitudes vary.',
      'amplitudes':list(map(str,vals)),
      'Jacobian_of_[sumU,H0,rho2,rho3]':str(jac),
      'determinant':str(det),
      'functional_means':[str(c.get(0,ZERO)[0]) for c in charges],
      'Q5red_comparison': 'rho3=-Q5red/128+3Q4h/32-H0/2+228/5 verified exactly at this Fourier point and for all four tangent derivatives; not a general-field proof.',
      'interpretation':'rho2 and rho3 add two independent functionals to old momentum and Hamilton at this fixed-Casimir-leaf point. This certificate only establishes independence; involution has a separate general proof.'
    }
    Path(__file__).with_name('fixed_leaf_independence_checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
