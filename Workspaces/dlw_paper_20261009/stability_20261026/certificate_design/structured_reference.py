"""Certified structured x/y perturbations of the existing heat/Laplace family.

F0 -> F0 + eps_x*cos(pi*x/6), s=A/2*(sin(pi*z/4)+eps_y*sin(pi*z/2)).
The physical initial fields remain u0=2*s*F0, v0=4-6*s_z*F0.
This is a restricted exactly solvable family, not arbitrary field perturbation.
Derived from reference_certificate_20261024/nondegenerate_benchmarks/reference.py.
"""
from pathlib import Path
from fractions import Fraction
import argparse,json,math
from flint import arb,acb,acb_poly,ctx
ctx.prec=320
M=48

def parameters(case):
    if case=='sine': return arb(3)/100,arb.pi()/12,arb(0),2
    return arb(1)/20,arb.pi()/96,arb.pi().sqrt()/32,128

def shift(p,k): return acb_poly([0]*k+list(p))

def fourier_coefficient(case,n,eps_x):
    _,w,C,K=parameters(case)
    base=(arb(1)/2 if abs(n)==1 else arb(0)) if case=='sine' else C*(-9*(w*n)**2).exp()
    extra=eps_x/2 if abs(n)==(2 if case=='sine' else 16) else arb(0)
    return base+extra


def initial_polys(case,s,eps_x):
    A,w,C,K=parameters(case)
    js=[acb(0)]*(2*K+1)
    for n in range(1,K+1):
        f=fourier_coefficient(case,n,eps_x)
        js[K+n]=acb(0,-f/(w*n));js[K-n]=acb(0,f/(w*n))
    J=acb_poly(js)
    term,ts,tss=acb_poly([1]),acb_poly([0]),acb_poly([0])
    Q,Qs,Qss=term,ts,tss
    for m in range(1,M+1):
        term,ts,tss=(-s*J*term*(arb(1)/m),
                    -J*(term+s*ts)*(arb(1)/m),
                    -J*(2*ts+s*tss)*(arb(1)/m))
        Q,Qs,Qss=shift(Q,K)+term,shift(Qs,K)+ts,shift(Qss,K)+tss
    return Q,Qs,Qss

def value_jets(polys,center,w,C,s,X):
    vals=[acb(0) for _ in range(6)]
    a=-C*X
    for j in range(2*center+1):
        c,cs,css=(p[j] for p in polys)
        d=acb(-s*C,w*(j-center));e=(d*X).exp()
        e0=c; e1=cs+a*c; e2=css+2*a*cs+a*a*c
        additions=[e0,d*e0,e1,d*e1-C*c,e2,d*e2-2*C*(cs+a*c)]
        vals=[v+b*e for v,b in zip(vals,additions)]
    return vals

def evaluate(case,x='0',z='1',t='.01',eps_x='.001',eps_y='.001',enclose=True):
    assert 0<=Fraction(z)<=4 and 0<=Fraction(t)<=Fraction(1,100)
    assert -96<=Fraction(x)<=96
    assert abs(Fraction(eps_x))<=Fraction(1,1000) and abs(Fraction(eps_y))<=Fraction(1,1000)
    x,z,t=arb(x),arb(z),arb(t)
    eps_x,eps_y=arb(eps_x),arb(eps_y)
    A,w,C,K=parameters(case)
    kappa=arb.pi()/4
    s=A*((kappa*z).sin()+eps_y*(2*kappa*z).sin())/2
    sz=A*kappa*((kappa*z).cos()+2*eps_y*(2*kappa*z).cos())/2
    X=x-4*t
    Q0,Qs0,Qss0=initial_polys(case,s,eps_x)
    center=K*M
    coeffs=[[],[],[]]
    for j in range(2*center+1):
        d=acb(-s*C,w*(j-center));E=(d*d*t).exp()
        Es=-2*C*d*t*E;Ess=(2*C*C*t+4*C*C*d*d*t*t)*E
        q,qs,qss=Q0[j],Qs0[j],Qss0[j]
        coeffs[0].append(q*E)
        coeffs[1].append(qs*E+q*Es)
        coeffs[2].append(qss*E+2*qs*Es+q*Ess)
    Q,Qs,Qss=map(acb_poly,coeffs)
    H,Hs,Hss=-s*Q,-Q-s*Qs,-2*Qs-s*Qss
    fs=[]
    for n in range(-K,K+1):
        f=fourier_coefficient(case,n,eps_x)
        fs.append(acb(f*((w*n)**2*t).exp()))
    F=acb_poly(fs)
    P,Ps,Pss=F*Q,F*Qs,F*Qss
    pc=center+K
    psi=[[],[],[]]
    for j in range(2*pc+1):
        n=j-pc
        if n==0 and case=='gaussian':
            a0,a1,a2=1/C,arb(0),arb(0)
        elif n!=0:
            d=acb(-s*C,w*n)
            a0=-s/d;a1=-1/d-s*C/(d*d);a2=-2*C/(d*d)-2*s*C*C/(d*d*d)
        else:
            means=[Q0[center],Qs0[center],Qss0[center]]
            for n0 in [-2,-1,1,2]:
                ind=center-n0
                hs0=[-s*Q0[ind],-Q0[ind]-s*Qs0[ind],-2*Qs0[ind]-s*Qss0[ind]]
                f0=fourier_coefficient(case,n0,eps_x)
                means=[v+acb(0,-2*w*n0)*f0*t*h for v,h in zip(means,hs0)]
            for row,v in zip(psi,means):row.append(v)
            continue
        psi[0].append(a0*P[j]);psi[1].append(a1*P[j]+a0*Ps[j])
        psi[2].append(a2*P[j]+2*a1*Ps[j]+a0*Pss[j])
    pj=value_jets(list(map(acb_poly,psi)),pc,w,C,s,X)
    hj=value_jets([H,Hs,Hss],center,w,C,s,X)
    fv=sum((F[n+K]*acb(0,w*n*X).exp() for n in range(-K,K+1)),acb(0))
    for a in pj+hj+[fv]:
        assert a.imag.contains(0)
        assert a.real.rad()<arb('1e-65')
    # All six jets plus F have uniform analytic truncation errors <1e-60.
    err=arb('0 +/- 1e-60') if enclose else arb(0)
    p,px,ps,psx,pss,pssx=[a.real+err for a in pj]
    h,hx,hs,hsx,hss,hssx=[a.real+err for a in hj]
    f=fv.real+err
    D=p*hs-h*ps;Dx=p*hsx-hx*ps
    Ds=p*hss-h*pss;Dxs=p*hssx-hx*pss
    assert p>arb('.6') and abs(D)>arb('.4')
    u=-2*(Dx/D-px/p)
    us=-2*((Dxs*D-Dx*Ds)/(D*D)-(psx*p-px*ps)/(p*p))
    v=4+4*sz*f*D/(p*p)-sz*us
    assert u.rad()<arb('1e-50') and v.rad()<arb('1e-50')
    return {'case':case,'x':str(x),'z':str(z),'t':str(t),'u':str(u),'v':str(v),
            'u_radius':str(u.rad()),'v_radius':str(v.rad()),'psi':str(p),'D':str(D),
            'eps_x':str(eps_x),'eps_y':str(eps_y),
            'initial_family':'u0=A[sin(pi*z/4)+eps_y*sin(pi*z/2)]*[F0+eps_x*cos(pi*x/6)], v0=4-3*u0_z',
            'scope':'structured perturbation; not an arbitrary physical-field perturbation'}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--case',choices=['sine','gaussian'])
    ap.add_argument('--x',default='0');ap.add_argument('--z',default='1');ap.add_argument('--t',default='.01')
    ap.add_argument('--eps-x',default='.001');ap.add_argument('--eps-y',default='.001')
    args=ap.parse_args()
    if args.case:out=evaluate(args.case,args.x,args.z,args.t,args.eps_x,args.eps_y)
    else:
        out={'samples':[evaluate(c) for c in ['sine','gaussian']],
             'precision_bits':ctx.prec,'M':M,'proof_status':'self-reviewed proof and Arb enclosure, not formal verification'}
        Path(__file__).with_name('samples.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps(out,indent=2))
