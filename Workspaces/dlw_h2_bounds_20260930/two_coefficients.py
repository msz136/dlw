"""Original two-soliton C: exact rational coefficient functions and bounds."""
from pathlib import Path
import json
import sympy as s
from fractions import Fraction
from bernstein import abs_sup
from single_bounds import outward

HERE=Path(__file__).resolve().parent
r,t=s.symbols('r t',real=True)
Q=s.Rational


def deriv(expr,weights):
    num,den=s.fraction(expr)
    top=0
    for v,w in zip((r,t),weights):
        top += w*v*(1-v)*(s.diff(num,v)*den-num*s.diff(den,v))
    return s.cancel(top/den**2)


def main():
    # Both x rates are 1. The transverse rates are -1/12 and -1/2.
    X=(Q(1),Q(1));Y=(Q(-1,12),Q(-1,2))
    fg=1+r*t/3
    ff=1+r/3+t+Q(11,9)*r*t
    # log tau = log normalized_tau - log(1-r)-log(1-t).
    def logx(poly):return s.cancel(sum(v*(1-v)*s.diff(poly,v) for v in (r,t))/poly+r+t)
    lx_f,lx_g=logx(ff),logx(fg)
    u=s.cancel(2*(lx_f-lx_g))
    v=s.cancel(2*deriv(lx_f+lx_g,Y))
    cache={}
    def diff(expr,nx,ny):
        for _ in range(nx):expr=deriv(expr,X)
        for _ in range(ny):expr=deriv(expr,Y)
        return expr
    w=s.cancel(v-diff(u,0,1))
    print('u/v rational functions constructed',flush=True)
    nonlinear=diff((w-4)**2/32,1,1)
    print('nonlinear coefficient constructed',flush=True)
    product=diff(diff(u,0,1)*diff(u,0,2),1,0)/2
    vterm,uterm=diff(v,2,2),diff(u,2,3)
    exprs={'SD_R1':s.cancel(nonlinear+vterm/12-uterm/4),
           'SD_R2':s.cancel(nonlinear+product+vterm/4-uterm/12),
           'FD_R1':s.cancel(vterm/12),'FD_R2':s.cancel(uterm/6)}
    out={'case':'C: a=2, (p1,q1)=(6,-5), (p2,q2)=(4,-3)',
         'domain':'Global x,y at fixed t: the two phases are independent; all r,t in [0,1] are covered.',
         'scope':'Residual coefficients only; not evolved solution coefficients.',
         'normalized_tau_g':str(fg),'normalized_tau_f':str(ff),'bounds':{}}
    for name,expr in exprs.items():
        print('bounding',name,flush=True)
        bound=abs_sup(expr,(r,t),tolerance=Fraction(1,10**6),seconds=120)
        bound['bound']=[outward(s.Rational(bound['lower_exact']),places=9),outward(s.Rational(bound['upper_exact']),True,places=9)]
        bound['expression']=str(expr)
        out['bounds'][name]=bound
        (HERE/'two_bounds.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
        print(name,bound['bound'],bound['subdivisions'],bound['tolerance_reached'],flush=True)


if __name__=='__main__':main()
