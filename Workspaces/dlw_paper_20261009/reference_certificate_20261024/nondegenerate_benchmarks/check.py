"""Uniform analytic bounds, initial/boundary checks, and leading coefficient."""
from pathlib import Path
import json,math
import sympy as S
from flint import arb
from reference import evaluate,parameters,M

def uniform_bounds():
    r=arb(1)/20; small=arb(1)/40;T=arb(1)/100
    L=arb(11)+arb('.056')*97
    E=(r*L+r*r*arb('.056')**2*T).exp()
    H=r*E;Hx=r*r*2*E;Ht=r*r*(2+4*r)*E
    dp=T*(2*Hx+2*H);dh=T*Ht;gap=r-small
    dhs=dh/gap;dps=dp/gap
    p0=(small*L).exp();hs0=(1+small*L)*p0;ps0=L*p0;h0=small*p0
    dD=dp*hs0+(p0+dp)*dhs+dh*ps0+(h0+dh)*dps
    pmin=1/p0-dp;Dmin=1/(p0*p0)-dD
    assert pmin>arb('.6') and Dmin>arb('.4')
    # Conservative physical error propagation for primitive errors <=1e-60.
    ee=arb('1e-60');dd=20000*ee;bb=arb(10000)
    p,pb,d,db=arb('.6'),arb('.59'),arb('.4'),arb('.39')
    quotient_D=dd/db+bb*dd/(d*db)
    product_D=((2*bb+dd)*dd)/(db*db)+bb*bb*dd*(1/(d*d*db)+1/(d*db*db))
    quotient_px=ee/pb+ee/(p*pb)
    quotient_psx=ee/pb+10*ee/(p*pb)
    product_p=(101+ee)*ee/(pb*pb)+100*ee*(1/(p*p*pb)+1/(p*pb*pb))
    eu=2*(quotient_D+quotient_px)
    eus=2*(quotient_D+product_D+quotient_psx+product_p)
    product_FD=((2+ee)*dd+bb*ee)/(pb*pb)+2*bb*ee*(1/(p*p*pb)+1/(p*pb*pb))
    ev=arb('.08')*product_FD+arb('.02')*eus
    assert eu<arb('1e-40') and ev<arb('1e-40')
    rows={}
    for case in ['sine','gaussian']:
        A,w,C,K=parameters(case)
        if case=='sine':
            Jn=(1+w)**2/w;Jtail=arb(0);Ftail=arb(0)
            Fn=(1+w)**2*(w*w*T).exp()
        else:
            alpha=9*w*w;n=K+1
            ratio=4*(-alpha*(2*K+3)).exp()
            Jtail=2*C*(-alpha*n*n).exp()*(1+w*n)**2/(w*n)/(1-ratio)
            Jn=sum((2*C*(-alpha*j*j).exp()*(1+w*j)**2/(w*j) for j in range(1,K+1)),arb(0))
            af=(9-T)*w*w;rf=4*(-af*(2*K+3)).exp()
            Ftail=2*C*(-af*n*n).exp()*(1+w*n)**2/(1-rf)
            Fn=C+sum((2*C*(-af*j*j).exp()*(1+w*j)**2 for j in range(1,K+1)),arb(0))+Ftail
        assert Fn<2 and Jn+Jtail<11 and C<arb('.056')
        R=r*(Jn+Jtail)
        dq0=R.exp()*(r*Jtail+R**(M+1)/math.factorial(M+1))
        growth=(2*r*r*C*C*T).exp();dq=dq0*growth
        prod_error=2*dq+Ftail*(R.exp()*growth+dq)
        if case=='gaussian':
            assert 1/C<19 and r/(w-r*C)<19
            ep=19*prod_error
        else:
            ep=(1+2*T*w*r)*dq0+r/w*prod_error
        spatial=(r*C*97).exp()*(1+r*C)
        # Cauchy s-derivatives up to order 2, x-derivatives up to order 1.
        epjets=ep*spatial*2/(gap*gap)
        ehjets=r*dq*spatial*2/(gap*gap)
        assert epjets<arb('1e-60') and ehjets<arb('1e-60') and Ftail<arb('1e-60')
        rows[case]={'F_weighted_norm':str(Fn),'J_weighted_norm_bound':str(Jn+Jtail),
                    'psi_jet_truncation_bound':str(epjets),'H_jet_truncation_bound':str(ehjets),
                    'F_truncation_bound':str(Ftail)}
    return {'psi_lower_bound':str(pmin),'abs_D_lower_bound':str(Dmin),
            'uniform_physical_truncation_u':str(eu),'uniform_physical_truncation_v':str(ev),'cases':rows}

def symbolic_laplace():
    x,y,t=S.symbols('x y t')
    U=S.Function('U')(x,y,t);P=S.Function('P')(x,y,t)
    Ut=S.Function('B')(x,t)+S.diff(U*U-U.diff(x),x)+2*S.Integral(P.diff(x,2),(y,0,y))
    # Local identity: transformed second equation residual equals
    # original first residual + differentiated original second residual / P.
    V=U+P.diff(x)/P;Q=P+V.diff(y)
    R1=U.diff(y,t)-S.diff(U*U-U.diff(x),x,y)-2*P.diff(x,2)
    R2=P.diff(t)-P.diff(x,2)-2*S.diff(U*P,x)
    newR1=V.diff(y,t)-S.diff(V*V-V.diff(x),x,y)-2*Q.diff(x,2)
    newR2=Q.diff(t)-Q.diff(x,2)-2*S.diff(V*Q,x)
    assert S.simplify(newR1-R1-S.diff(R2/P,x,y))==0
    assert S.simplify(newR2-R2-R1-S.diff(R2/P,x,y))==0
    p=S.Function('p')(x)
    assert S.simplify(-S.diff((4-3*p-4)**2-p*p,x)/4+4*p*p.diff(x))==0
    return True

if __name__=='__main__':
    out={'uniform_bounds':uniform_bounds(),'Laplace_and_leading_symbolic':symbolic_laplace(),'checks':[]}
    for case in ['sine','gaussian']:
        A,w,C,K=parameters(case)
        for xs,zs in [('0','1'),('3','2')]:
            val=evaluate(case,xs,zs,'0')
            x,z=arb(xs),arb(zs);k=arb.pi()/4
            F=(w*x).cos() if case=='sine' else sum(((-((x+192*j)/6)**2).exp() for j in [-1,0,1]),arb(0))+arb('0 +/- 1e-1000')
            assert arb(val['u']).overlaps(A*(k*z).sin()*F)
            assert arb(val['v']).overlaps(4-3*A*k*(k*z).cos()*F)
            out['checks'].append({'case':case,'initial_x':xs,'initial_z':zs,'passed':True})
        for zs in ['0','4']:
            val=evaluate(case,'3',zs,'.01')
            assert arb(val['u']).contains(0)
            out['checks'].append({'case':case,'boundary_z':zs,'passed':True})
        eps=arb('1e-8');r0=evaluate(case,'3','1','0');r1=evaluate(case,'3','1','1e-8')
        x=arb(3);zz=arb(1);kap=arb.pi()/4
        if case=='sine':
            f=(w*x).cos();fx=-w*(w*x).sin();fxx=-w*w*f
        else:
            f=fx=fxx=arb(0)
            for j in [-1,0,1]:
                q=x+192*j;g=(-q*q/36).exp()
                f+=g;fx+=-q*g/18;fxx+=(q*q/324-arb(1)/18)*g
        a=A*(kap*zz).sin();az=A*kap*(kap*zz).cos()
        u,ux,uxx,p,px,pxx=a*f,a*fx,a*fxx,az*f,az*fx,az*fxx
        expected=[3*uxx-(u+4)*ux,-pxx+3*(ux*p+(u+4)*px)]
        differences=[(arb(r1[key])-arb(r0[key]))/eps-rate for key,rate in zip(['u','v'],expected)]
        assert all(abs(d)<arb('1e-7') for d in differences)
        out['checks'].append({'case':case,'initial_time_rate_difference_at_dt_1e-8':[str(d) for d in differences],
                              'meaning':'finite-step consistency check, not the truncation certificate','passed':True})
    out['proof_status']='Self-reviewed analytic proof, symbolic identities and Arb constants; not formal verification.'
    Path(__file__).with_name('certificate.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps(out,indent=2))
