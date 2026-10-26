"""Arb enclosure of every stored final reference sample at exact T=1/100.

The DFT is evaluated on an exact rational grid. A first-order Taylor shift
with a uniform second-derivative enclosure covers each actual binary64 x.
No unvalidated floating-point quadrature or time integration enters the proof.
"""
from pathlib import Path
import math,json,time,hashlib,sys
import numpy as np
from flint import arb,acb,acb_poly,ctx

HERE=Path(__file__).resolve().parent
ctx.prec=160
M=32
METHODS=['Endpoint-SD','CSD0','Centered-SD','FD']
BOUND=arb('1e-13')


def parameters(case):
    if case.lower() in ('sine','sinusoidal'):
        return arb(3)/100,arb.pi()/12,arb(0),1,8
    return arb(1)/20,arb.pi()/96,arb.pi().sqrt()/32,96,1


def truncation(case):
    A,w,C,K,multiple=parameters(case)
    r=arb(1)/20;T=arb(1)/100;gap=arb(1)/40
    if K==1:
        Jn=(1+w)**2/w;Jtail=arb(0);Ftail=arb(0)
        Fn=(1+w)**2*(w*w*T).exp()
    else:
        alpha=9*w*w;n=K+1
        ratio=4*(-alpha*(2*K+3)).exp()
        assert ratio<1
        Jtail=2*C*(-alpha*n*n).exp()*(1+w*n)**2/(w*n)/(1-ratio)
        Jn=sum((2*C*(-alpha*j*j).exp()*(1+w*j)**2/(w*j) for j in range(1,K+1)),arb(0))
        af=(9-T)*w*w;rf=4*(-af*(2*K+3)).exp()
        assert rf<1
        Ftail=2*C*(-af*n*n).exp()*(1+w*n)**2/(1-rf)
        Fn=C+sum((2*C*(-af*j*j).exp()*(1+w*j)**2 for j in range(1,K+1)),arb(0))+Ftail
    assert Fn<2 and Jn+Jtail<11 and C<arb('.056')
    R=r*(Jn+Jtail)
    dq0=R.exp()*(r*Jtail+R**(M+1)/math.factorial(M+1))
    growth=(2*r*r*C*C*T).exp();dq=dq0*growth
    prod_error=2*dq+Ftail*(R.exp()*growth+dq)
    if K!=1:
        assert 1/C<19 and r/(w-r*C)<19
        ep=19*prod_error
    else:
        ep=(1+2*T*w*r)*dq0+r/w*prod_error
    spatial=(r*C*97).exp()*(1+r*C)
    epjets=ep*spatial*2/(gap*gap)
    ehjets=r*dq*spatial*2/(gap*gap)
    epsilon=arb('1e-33')
    assert epjets<epsilon and ehjets<epsilon and Ftail<epsilon
    return epsilon,dict(psi_jet_bound=str(epjets),H_jet_bound=str(ehjets),F_bound=str(Ftail),
                        M=M,K=K,primitive_enclosure=str(epsilon))


def shift(p,k):
    return acb_poly([0]*k+list(p))


def coefficients(case,y):
    A,w,C,K,multiple=parameters(case)
    t=arb(1)/100
    ang=arb.pi()/4*(arb(float(y))+2)
    s=A*ang.sin()/2;sz=A*arb.pi()/4*ang.cos()/2
    J=[acb(0)]*(2*K+1)
    for n in range(1,K+1):
        f=arb(1)/2 if K==1 else C*(-9*(w*n)**2).exp()
        J[K+n]=acb(0,-f/(w*n));J[K-n]=acb(0,f/(w*n))
    J=acb_poly(J)
    term,ts,tss=acb_poly([1]),acb_poly([0]),acb_poly([0])
    Q,Qs,Qss=term,ts,tss
    for m in range(1,M+1):
        term,ts,tss=(-s*J*term*(arb(1)/m),
                    -J*(term+s*ts)*(arb(1)/m),
                    -J*(2*ts+s*tss)*(arb(1)/m))
        Q,Qs,Qss=shift(Q,K)+term,shift(Qs,K)+ts,shift(Qss,K)+tss
    Q0,Qs0,Qss0=Q,Qs,Qss
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
        f=(arb(1)/2 if abs(n)==1 else arb(0)) if K==1 else C*(-9*(w*n)**2).exp()
        fs.append(acb(f*((w*n)**2*t).exp()))
    F=acb_poly(fs)
    P,Ps,Pss=F*Q,F*Qs,F*Qss
    pc=center+K;psi=[[],[],[]]
    for j in range(2*pc+1):
        n=j-pc
        if n==0 and K!=1:
            a0,a1,a2=1/C,arb(0),arb(0)
        elif n!=0:
            d=acb(-s*C,w*n)
            a0=-s/d;a1=-1/d-s*C/(d*d);a2=-2*C/(d*d)-2*s*C*C/(d*d*d)
        else:
            means=[Q0[center],Qs0[center],Qss0[center]]
            for n0 in [-1,1]:
                ind=center-n0
                hs0=[-s*Q0[ind],-Q0[ind]-s*Qs0[ind],-2*Qs0[ind]-s*Qss0[ind]]
                means=[v+acb(0,-w*n0)*t*h for v,h in zip(means,hs0)]
            for row,v in zip(psi,means):row.append(v)
            continue
        psi[0].append(a0*P[j]);psi[1].append(a1*P[j]+a0*Ps[j])
        psi[2].append(a2*P[j]+2*a1*Ps[j]+a0*Pss[j])
    return s,sz,list(map(acb_poly,psi)),[H,Hs,Hss],F


def falling(n,k):
    return math.factorial(n)//math.factorial(n-k)


def value_jets(polys,center,w,C,s,x,multiple,epsilon):
    """All s<=2,x<=1 jets at actual binary64 x; return validated real balls."""
    N=len(x)
    X0=arb(float(x[0]))-arb(4)/100
    sums=[[[acb(0) for _ in range(N)] for j in range(3)] for i in range(3)]
    norms=[[arb(0) for j in range(4)] for i in range(3)]
    for k in range(2*center+1):
        n=k-center;d=acb(-s*C,w*n)
        phase=acb(0,w*n*X0).exp()
        b=n*multiple%N
        for i in range(3):
            q=polys[i][k]
            for j in range(4):
                z=d**j*q
                norms[i][j]+=abs(z)
                if j<3:sums[i][j][b]+=z*phase
    raw=[[[z*N for z in acb.dft(sums[i][j],inverse=True)] for j in range(3)] for i in range(3)]
    # Uniform norms over |X|<=97 for the finite polynomial derivatives.
    aa=C*97;ex=(abs(s)*C*97).exp()
    bounds={}
    for i in range(3):
        for j in range(4):
            bound=arb(0)
            for m in range(min(i,j)+1):
                for ell in range(i-m+1):
                    factor=math.comb(i,m)*falling(j,m)*C**m*math.comb(i-m,ell)*aa**(i-m-ell)
                    bound+=factor*norms[ell][j-m]
            bounds[i,j]=ex*bound
    rows=[];max_shift=arb(0);max_shift_remainder=arb(0)
    for ix,xx in enumerate(x):
        X=X0+arb(192)*ix/N
        delta=arb(float(xx))-arb(float(x[0]))-arb(192)*ix/N
        if abs(delta)>max_shift:max_shift=abs(delta)
        a=-C*X;factor=(-s*C*X).exp()
        jets={}
        for i in range(3):
            for j in range(3):
                value=acb(0)
                for m in range(min(i,j)+1):
                    for ell in range(i-m+1):
                        c=math.comb(i,m)*falling(j,m)*(-C)**m*math.comb(i-m,ell)*a**(i-m-ell)
                        value+=c*raw[ell][j-m][ix]
                value*=factor
                assert value.imag.contains(0)
                jets[i,j]=value.real
        vals=[]
        for i,j in [(0,0),(0,1),(1,0),(1,1),(2,0),(2,1)]:
            rem=delta*delta*bounds[i,j+2]/2
            if rem>max_shift_remainder:max_shift_remainder=rem
            radius=arb(0,rem.upper())+arb(0,epsilon.upper())
            vals.append(jets[i,j]+delta*jets[i,j+1]+radius)
        rows.append(vals)
    return rows,max_shift,max_shift_remainder


def final_row(case,x,y,epsilon):
    A,w,C,K,multiple=parameters(case)
    s,sz,P,H,F=coefficients(case,y)
    pjets,shift,pr=value_jets(P,(M+1)*K,w,C,s,x,multiple,epsilon)
    hjets,_,hr=value_jets(H,M*K,w,C,s,x,multiple,epsilon)
    # F is ordinary periodic and uses the same rational-grid Taylor enclosure.
    fs=[acb_poly(F),acb_poly([0]*(len(F))),acb_poly([0]*(len(F)))]
    # acb_poly strips trailing zeros; use a separate periodic evaluator for F.
    N=len(x);X0=arb(float(x[0]))-arb(4)/100
    frows=[[acb(0) for _ in range(N)] for j in range(2)]
    fxx_bound=arb(0)
    for n in range(-K,K+1):
        freq=w*n;d=acb(0,freq);z=F[n+K]*acb(0,freq*X0).exp()
        for j in range(2):frows[j][n*multiple%N]+=d**j*z
        fxx_bound+=freq*freq*abs(F[n+K])
    fv,fx=[[z*N for z in acb.dft(row,inverse=True)] for row in frows]
    result=[]
    for ix,(pv,hv) in enumerate(zip(pjets,hjets)):
        p,px,ps,psx,pss,pssx=pv
        h,hx,hs,hsx,hss,hssx=hv
        delta=arb(float(x[ix]))-arb(float(x[0]))-arb(192)*ix/N
        f=fv[ix].real+delta*fx[ix].real+arb(0,(delta*delta*fxx_bound/2+epsilon).upper())
        D=p*hs-h*ps;Dx=p*hsx-hx*ps
        Ds=p*hss-h*pss;Dxs=p*hssx-hx*pss
        assert p>arb('.6') and abs(D)>arb('.4')
        u=-2*(Dx/D-px/p)
        us=-2*((Dxs*D-Dx*Ds)/(D*D)-(psx*p-px*ps)/(p*p))
        v=4+4*sz*f*D/(p*p)-sz*us
        result.append((u,v))
    return result,dict(maximum_coordinate_shift=str(shift),maximum_primitive_taylor_remainder=str(max(pr,hr)))


def check_values(values,balls):
    maximum=0.
    for value,ball in zip(values,balls):
        err=abs(arb(float(value))-ball)
        assert err<BOUND,(value,ball,err)
        maximum=max(maximum,float(np.nextafter(float(err.upper()),np.inf)))
    return maximum


def certify(case):
    start=time.perf_counter()
    files={m:HERE/f'{case}_{m}_RK4.npz' for m in METHODS}
    data={m:np.load(p) for m,p in files.items()}
    x=data[METHODS[0]]['x']
    assert all(np.array_equal(d['x'],x) for d in data.values())
    assert np.max(abs(x))<=96
    ys=np.unique(np.concatenate([d['y'] for d in data.values()]+[d['yv'] for d in data.values()]))
    epsilon,tailinfo=truncation(case)
    maxima=dict(u=0.,v=0.);counts=dict(u=0,v=0);corrections=[]
    for iy,y in enumerate(ys):
        balls,correction=final_row(case,x,y,epsilon)
        corrections.append(correction)
        for m,d in data.items():
            for col,field,grid in [(0,'u','y'),(1,'v','yv')]:
                for row in np.flatnonzero(d[grid]==y):
                    err=check_values(d[field+'_ref'][row],[b[col] for b in balls])
                    maxima[field]=max(maxima[field],err);counts[field]+=len(x)
        if iy%10==0 or iy==len(ys)-1:
            print(case,iy+1,len(ys),'seconds',round(time.perf_counter()-start,1),'max',maxima,flush=True)
    result=dict(status='verified_all_stored_final_sample_values',case=case,precision_bits=ctx.prec,
                M=M,K=parameters(case)[3],nominal_time='1/100',x_nodes=len(x),distinct_y=len(ys),
                counts=counts,max_certified_enclosures=maxima,uniform_bound_each=1e-13,
                truncation=tailinfo,coordinate_handling='Exact binary64 x and y; DFT lattice corrected by Taylor interval enclosure.',
                time_handling='Arb values evaluated at exact rational T=1/100; stored float-time discrepancies are included in direct comparisons.',
                elapsed_seconds=time.perf_counter()-start,coordinate_corrections=corrections,
                files={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files.values()})
    (HERE/f'reference_certificate_{case}.json').write_text(json.dumps(result,indent=2),encoding='utf8')
    return result


def collect():
    initial=json.loads((HERE/'initial_reference_certificate.json').read_text(encoding='utf8'))
    cases=[json.loads((HERE/f'reference_certificate_{c}.json').read_text(encoding='utf8')) for c in ['Gaussian','Sinusoidal']]
    result=dict(status='verified_all_stored_sample_values',uniform_bound_each=1e-13,
                initial=dict(u=1e-13,v=1e-13,ut=1e-13,vt=1e-13),final=dict(u=1e-13,v=1e-13),
                nominal_final_time='1/100',
                scope='Stored continuum reference values only: analytic Fourier and Taylor tails, Arb finite evaluation, binary64 conversion, exact floating-point coordinates and nominal final time are included.',
                proof_status='Analytic proof with independent review and Arb enclosure checks, not formal proof-assistant verification.',
                reference_source_sha256=hashlib.sha256((HERE/'reference_grid.py').read_bytes()).hexdigest(),
                certificate_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                initial_certificate=initial,cases=cases)
    (HERE/'reference_certificate.json').write_text(json.dumps(result,indent=2),encoding='utf8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('initial_certificate','cases')},indent=2))


if __name__=='__main__':
    if len(sys.argv)>1:certify(sys.argv[1])
    else:collect()
