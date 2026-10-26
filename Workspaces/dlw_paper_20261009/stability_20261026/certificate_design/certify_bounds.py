"""Arb checks of uniform bounds for structured x/y-perturbed references."""
from pathlib import Path
import json,math
from flint import arb,ctx
ctx.prec=320
HERE=Path(__file__).resolve().parent

def certify():
    r=arb('.05');S=arb('.026');T=arb('.01');eps=arb('.001')
    L=arb('16.432');Cmax=arb('.056');gap=r-S
    E=(r*L+r*r*Cmax*Cmax*T).exp()
    H=r*E;Hx=2*r*r*E;Ht=r*r*(2+4*r)*E
    dp=T*(2*Hx+2*H);dh=T*Ht;p0=(S*L).exp()
    dD=dp*(1+S*L)*p0+(p0+dp)*dh/gap+dh*L*p0+(S*p0+dh)*dp/gap
    pmin=1/p0-dp;Dmin=1/(p0*p0)-dD
    assert pmin>arb('.6') and Dmin>arb('.4')
    rows={}
    for case in ['sine','gaussian']:
        w=arb.pi()/(12 if case=='sine' else 96)
        C=arb(0) if case=='sine' else arb.pi().sqrt()/32
        K=2 if case=='sine' else 128
        kpert=arb.pi()/6
        Jextra=eps*(1+kpert)**2/kpert
        Fextra=eps*(1+kpert)**2*(kpert*kpert*T).exp()
        if case=='sine':
            Jn=(1+w)**2/w+Jextra;Jtail=Ftail=arb(0)
            Fn=(1+w)**2*(w*w*T).exp()+Fextra
        else:
            alpha=9*w*w;n=K+1;ratio=4*(-alpha*(2*K+3)).exp()
            Jtail=2*C*(-alpha*n*n).exp()*(1+w*n)**2/(w*n)/(1-ratio)
            Jn=sum((2*C*(-alpha*j*j).exp()*(1+w*j)**2/(w*j) for j in range(1,K+1)),arb(0))+Jextra
            af=(9-T)*w*w;rf=4*(-af*(2*K+3)).exp()
            Ftail=2*C*(-af*n*n).exp()*(1+w*n)**2/(1-rf)
            Fn=C+sum((2*C*(-af*j*j).exp()*(1+w*j)**2 for j in range(1,K+1)),arb(0))+Ftail+Fextra
        assert Fn<2 and Jn+Jtail<11 and C<Cmax
        R=r*(Jn+Jtail);M=48
        dq0=R.exp()*(r*Jtail+R**(M+1)/math.factorial(M+1))
        growth=(2*r*r*C*C*T).exp();dq=dq0*growth
        pe=2*dq+Ftail*(R.exp()*growth+dq)
        if case=='gaussian':
            assert 1/C<19 and r/(w-r*C)<19
            ep=19*pe
        else:
            # Mean psi_t = sum -2i*k_n F_n H_-n. All harmonics included.
            mean_multiplier=2*T*r*(w+eps*kpert)
            ep=(1+mean_multiplier)*dq0+r/w*pe
        spatial=(r*C*97).exp()*(1+r*C)
        epjets=ep*spatial*2/gap**2;ehjets=r*dq*spatial*2/gap**2
        assert epjets<arb('1e-60') and ehjets<arb('1e-60') and Ftail<arb('1e-60')
        rows[case]={'F_weighted_norm':str(Fn),'J_weighted_norm':str(Jn+Jtail),'psi_jet_truncation':str(epjets),'H_jet_truncation':str(ehjets),'F_truncation':str(Ftail)}
    # Conservative quotient-error propagation, primitive errors <=1e-60.
    e=arb('1e-60');dd=20000*e;B=arb(10000)
    p,pb,d,db=map(arb,['.6','.59','.4','.39'])
    qD=dd/db+B*dd/(d*db)
    pD=((2*B+dd)*dd)/(db*db)+B*B*dd*(1/(d*d*db)+1/(d*db*db))
    qx=e/pb+e/(p*pb);qs=e/pb+10*e/(p*pb)
    pp=(101+e)*e/(pb*pb)+100*e*(1/(p*p*pb)+1/(p*pb*pb))
    eu=2*(qD+qx);eus=2*(qD+pD+qs+pp)
    pFD=((2+e)*dd+B*e)/(pb*pb)+2*B*e*(1/(p*p*pb)+1/(p*pb*pb))
    szmax=arb('.05')/2*(arb.pi()/4)*(1+2*eps)
    assert szmax<arb('.02')
    ev=arb('.08')*pFD+arb('.02')*eus
    assert eu<arb('1e-40') and ev<arb('1e-40')
    return {'scope':'restricted heat/Laplace family, not arbitrary additive fields',
       'abs_eps_x_max':'.001','abs_eps_y_max':'.001','domain':{'x':[-96,96],'z':[0,4],'t':[0,.01]},
       'psi_lower':str(pmin),'abs_D_lower':str(Dmin),'cases':rows,
       'primitive_uniform_bound':'1e-60','uniform_physical_truncation_u':str(eu),'uniform_physical_truncation_v':str(ev),
       'safe_uniform_truncation_bound':'1e-40','arb_precision_bits':320,
       'per_call_physical_radius_limit':'1e-50; successful calls only',
       'proof_status':'analytic derivation plus outward-rounded constants; pending independent review'}

if __name__=='__main__':
    result=certify();(HERE/'bounds.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result,indent=2))
