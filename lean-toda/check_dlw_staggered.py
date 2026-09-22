"""Exact coefficient tests for the staggered determinant-preserving DLW pair.

lambda=-2. B=(Dx^2+Dt+2*a*Dx).
  (B-h*Dx) F_j.G_j = 0
  (B+h*Dx) F_j.G_{j+1} = 0
F_j is located at (j+1/2)*h and G_j at j*h.
The all-N argument is in dlw_staggered_construction.md; finite tests are
independent checks, not its replacement. Standard library only.
"""
from fractions import Fraction as Q
from itertools import product
from math import prod
import json
from pathlib import Path


def determinant_expansion(p, q, a, h):
    d=h/2
    n=len(p)
    rho=[(p[i]-a+d)*(q[i]+a+d)/((p[i]-a-d)*(q[i]+a-d)) for i in range(n)]
    result=[]
    for m in product((0,1), repeat=n):
        active=[i for i in range(n) if m[i]]
        c=prod((1/(p[i]+q[i]) for i in active),start=Q(1))
        for i in active:
            for j in active:
                if i<j:
                    c *= (p[i]-p[j])*(q[i]-q[j])/((p[i]+q[j])*(p[j]+q[i]))
        f=c*prod((-(p[i]-a+d)/(q[i]+a-d) for i in active),start=Q(1))
        result.append((m,f,c,sum(p[i]+q[i] for i in active),
                       sum(q[i]**2-p[i]**2 for i in active),
                       prod((rho[i] for i in active),start=Q(1))))
    return result


def residuals(data,a,h):
    left={}
    right={}
    for m,f,g,k,w,r in data:
        for mm,ff,gg,kk,ww,rr in data:
            mode=tuple(i+j for i,j in zip(m,mm))
            dk=k-kk
            dw=w-ww
            weight=f*gg
            left[mode]=left.get(mode,Q(0))+weight*(dk*dk+dw+(2*a-h)*dk)
            right[mode]=right.get(mode,Q(0))+weight*rr*(dk*dk+dw+(2*a+h)*dk)
    return left,right


def run():
    report=[]
    for seed in range(4):
        for n in range(1,6):
            a=Q(seed+2,3)
            h=Q(seed+1,7+seed)
            p=[Q(3+i*2+seed,2) for i in range(n)]
            q=[Q(7+i*3+seed,3) for i in range(n)]
            data=determinant_expansion(p,q,a,h)
            left,right=residuals(data,a,h)
            badL={str(m):str(v) for m,v in left.items() if v}
            badR={str(m):str(v) for m,v in right.items() if v}
            assert not badL and not badR,(seed,n,badL,badR)
            report.append(dict(seed=seed,N=n,a=str(a),h=str(h),
                               p=list(map(str,p)),q=list(map(str,q)),
                               coefficients_per_equation=len(left),
                               all_residual_coefficients_zero=True))
            print(f'seed={seed}, N={n}, coefficients={len(left)} per equation: exact zero')
    # The previous counterexample, now with the new staggered tau amplitudes.
    a,h=Q(2),Q(1,10)
    left,right=residuals(determinant_expansion([Q(1),Q(0)],[Q(2),Q(3)],a,h),a,h)
    assert not any(left.values()) and not any(right.values())
    report.append(dict(case='previous counterexample parameters',N=2,a=str(a),h=str(h),
                       coefficients_per_equation=len(left),all_residual_coefficients_zero=True))
    Path('dlw_staggered_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('Previous counterexample parameters: both equations now exactly satisfied.')
    print('Total exact coefficient checks:',sum(2*r['coefficients_per_equation'] for r in report))


if __name__=='__main__':
    import sys
    if '--symbolic' in sys.argv:
        import sympy as s
        p=s.symbols('P1 P2')
        q=s.symbols('Q1 Q2')
        h=s.symbols('h')
        # P=p-a, Q=q+a; Dt+2*a*Dx has eigenvalue Q^2-P^2.
        left,right=residuals(determinant_expansion(p,q,s.Integer(0),h),s.Integer(0),h)
        out=[]
        for mode in left:
            l=s.factor(s.together(left[mode]))
            r=s.factor(s.together(right[mode]))
            assert l==0 and r==0,(mode,l,r)
            out.append(dict(mode=list(mode),left=str(l),right=str(r)))
        Path('dlw_staggered_symbolic_two_soliton.json').write_text(
            json.dumps(out,indent=2)+'\n',encoding='utf-8')
        print('All 18 general two-soliton coefficients vanish symbolically.')
    else:
        run()
