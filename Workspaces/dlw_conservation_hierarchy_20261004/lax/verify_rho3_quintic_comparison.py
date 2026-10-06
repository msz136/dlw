"""General x-field Euler check of rho3 versus Q5red on N=3,G=6,T=12.

This is a symbolic field identity at specified average constants, stronger
than a finite-mode test but not advertised as a general-N identity.
"""
from pathlib import Path
import json
import sympy as s
from verify_monodromy_hierarchy import jet,dx,mul,assert_total_dx

Q=s.Rational
def main():
    g=[jet('g0'),jet('g1')]
    g.append(6-g[0]-g[1])
    p=[jet('r0'),jet('r1')]
    p.append(-p[0]-p[1])
    mean=(12-sum(pi*gi for pi,gi in zip(p,g)))/6
    u=[pi+mean for pi in p]
    pp={0:s.Integer(1)}
    for uj,gj in zip(u,g):
        bj=(uj-gj)/2
        st={0:s.Integer(1),-1:-gj}
        for k in range(1,5):st[-k-1]=s.expand(bj*st[-k]-dx(st[-k]))
        pp=mul(st,pp,lo=-5)
    print('p3,p4,p5 generated',flush=True)
    p3,p4,p5=pp[-3],pp[-4],pp[-5]
    rho3=2*p4+p5/2+p3**2/6+10*p3+96
    rh=s.Matrix([[0,Q(-1,6),Q(1,6)],[Q(1,6),0,Q(-1,6)],[Q(-1,6),Q(1,6),0]])
    a=list(4*rh*s.Matrix([dx(gj) for gj in g]))
    c=list(4*rh*s.Matrix([dx(uj*gj) for uj,gj in zip(u,g)]))
    beta=Q(1,2)
    h0=q4=q5=0
    for uj,wj,aj,cj in zip(u,g,a,c):
        ux,wx=dx(uj),dx(wj)
        h0+=4*(uj**2*wj/2+beta*wj**3/3+wj*ux+wj*aj/2)
        q4+=4*(uj**3*wj/3+2*beta*uj*wj**3/3+2*uj*wj*ux-Q(4,3)*ux*wx+uj*wj*aj)
        q5+=4*(uj**4*wj+12*uj**2*wj*ux-4*wj*ux**2-16*uj*ux*wx+8*ux*dx(wj,2)
               +4*uj**2*wj*aj+4*wj*ux*aj-4*uj*wx*aj+2*wj*aj**2-4*wx*dx(aj)
               +2*uj*wj*cj+4*beta*uj**2*wj**3+4*beta**2*wj**5/5
               +8*beta*wj**3*ux/3-8*beta*wj*wx**2+8*beta*wj**3*aj/3)
    predicted=-q5/128+h0**2/384+3*q4/32-h0/2+Q(228,5)
    residual=s.expand(rho3-predicted)
    print('Euler derivative check starting',flush=True)
    assert_total_dx(residual)
    result={'passed':True,'N':3,'h':4,'G':6,'T':12,
            'certificate':'rho3 = -Q5red/128+3Q4h/32-H0/2+228/5 modulo D for arbitrary four reduced x fields.',
            'scope':'Specified mean constants, general differential fields. Not a general-N proof.'}
    Path(__file__).with_name('rho3_quintic_comparison_checks.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
