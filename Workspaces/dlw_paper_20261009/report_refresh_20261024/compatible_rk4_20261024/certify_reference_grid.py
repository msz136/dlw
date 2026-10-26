"""Arb verification of EVERY stored initial/final continuum reference value."""
from pathlib import Path
import json, math, time, hashlib
import numpy as np
from flint import arb, acb, acb_poly, ctx

HERE=Path(__file__).resolve().parent
ctx.prec=160
M=32
BOUND=arb('1e-13')


def parameters(case):
    if case=='Sinusoidal':
        return arb(3)/100,arb.pi()/12,arb(0),1,8,arb.pi()/4
    return arb(1)/20,arb.pi()/96,arb.pi().sqrt()/32,96,1,arb.pi()/4


def derivative_tail(case):
    A,w,C,K,multiple,kappa=parameters(case)
    if K==1:
        J=(1+w)**3/w;tail=arb(0)
    else:
        J=sum((2*C*(-9*(w*n)**2).exp()*(1+w*n)**3/(w*n)
               for n in range(1,K+1)),arb(0))
        n=K+1
        ratio=(arb(K+2)/(K+1))**3*(-9*w*w*(2*K+3)).exp()
        assert ratio<1
        tail=2*C*(-9*(w*n)**2).exp()*(1+w*n)**3/(w*n)/(1-ratio)
    R=A*(1+kappa)*(J+tail)/2
    e=A*(1+kappa)*tail/2
    delta=R.exp()*(e+R**33/math.factorial(33))
    assert delta<arb('1e-30')
    return delta


def coefficients(case,y):
    A,w,C,K,multiple,kappa=parameters(case)
    yy=arb(float(y));ang=kappa*(yy+2)
    s=-A*ang.sin()/2;sz=-A*kappa*ang.cos()/2
    mu=A*C*ang.sin();muz=A*C*kappa*ang.cos()
    J=[acb(0) for _ in range(2*K+1)]
    for n in range(1,K+1):
        f=arb(1)/2 if K==1 else C*(-9*(w*n)**2).exp()
        J[K+n]=acb(0,-f/(w*n));J[K-n]=acb(0,f/(w*n))
    J=acb_poly(J)
    term,termz=acb_poly([1]),acb_poly([0])
    Q,Qz=acb_poly([1]),acb_poly([0])
    for m in range(1,M+1):
        termz=J*(s*termz+sz*term)*(arb(1)/m)
        term=J*term*(s/m)
        Q=acb_poly([0]*K+list(Q))+term
        Qz=acb_poly([0]*K+list(Qz))+termz
    return Q,Qz,w,K,multiple,mu,muz


def final_row(case,x,y,t,tail):
    Q,Qz,w,K,multiple,mu,muz=coefficients(case,y)
    N=len(x);tt=arb(float(t));x0=arb(float(x[0]))
    sums=[[acb(0) for _ in range(N)] for __ in range(5)]
    Bs=[arb(0) for _ in range(4)];Zs=[arb(0) for _ in range(3)]
    for j in range(2*K*M+1):
        n=j-K*M;freq=w*n;d=acb(0,freq)
        heat=(-freq*freq*tt).exp()
        e=acb(-freq*freq*tt,freq*(x0-4*tt-mu*tt)).exp()
        h=Q[j]*e;hz=Qz[j]*e
        b=n*multiple%N
        vals=[h,d*h,d*d*h,hz,d*hz]
        for row,val in zip(sums,vals):row[b]+=val
        for p in range(4):Bs[p]+=abs(Q[j])*heat*abs(freq)**p
        for p in range(3):Zs[p]+=abs(Qz[j])*heat*abs(freq)**p
    Bs=[b+tail for b in Bs];Zs=[z+tail for z in Zs]
    # Derivatives of the exact quotient, uniformly in x and this y.
    lower=arb(3)/5
    lx=2*(Bs[2]/lower+Bs[1]**2/lower**2)
    cy=Zs[0]+abs(muz)*tt*Bs[1]
    by=Zs[1]+abs(muz)*tt*Bs[2]
    ay=Zs[2]+abs(muz)*tt*Bs[3]
    lv=2*(ay/lower+Bs[2]*cy/lower**2+2*Bs[1]*by/lower**2
          +2*Bs[1]**2*cy/lower**3)
    displacement=arb(0)
    for i,xx in enumerate(x):
        di=abs(arb(float(xx))-(x0+arb(192)*i/N))
        if di>displacement:displacement=di
    correction=[lx*displacement,lv*displacement]
    H,B,C,Z,W=[[z*N for z in acb.dft(row,inverse=True)] for row in sums]
    result=[]
    for a,b,c,z,wz in zip(H,B,C,Z,W):
        u=mu-2*b/a
        v=4-muz+2*((wz-muz*tt*c)/a-b*(z-muz*tt*b)/(a*a))
        assert u.imag.contains(0) and v.imag.contains(0)
        result.append((u.real,v.real))
    return result,correction


def xjets(case,x):
    A,w,C,K,multiple,kappa=parameters(case)
    result=[]
    for xx in x:
        xx=arb(float(xx))
        if K==1:
            f=(w*xx).cos();fx=-w*(w*xx).sin();fxx=-w*w*f
        else:
            f=fx=fxx=arb(0)
            for j in range(-2,3):
                r=xx+192*j;g=(-(r/6)**2).exp()
                f+=g;fx+=-r*g/18;fxx+=(r*r/324-arb(1)/18)*g
        result.append((f,fx,fxx))
    return result


def initial_row(case,jets,y):
    A,w,C,K,multiple,kappa=parameters(case)
    ang=kappa*(arb(float(y))+2)
    s=ang.sin();sz=kappa*ang.cos()
    result=[]
    for f,fx,fxx in jets:
        u=A*s*f;uy=A*sz*f;ux=A*s*fx;uxy=A*sz*fx
        ut=A*s*fxx-(u+4)*ux
        vt=-A*sz*fxx+uy*ux+(u+4)*uxy
        result.append((u,4-uy,ut,vt))
    return result


def check_values(floats,balls,extra):
    maximum=0.
    for value,ball in zip(floats,balls):
        err=abs(arb(float(value))-ball)+extra
        assert err<BOUND,(value,ball,err)
        maximum=max(maximum,float(np.nextafter(float(err.upper()),np.inf)))
    return maximum


def certify(case):
    start=time.perf_counter()
    methods=['Endpoint-SD','Centered-SD','FD']
    final={m:np.load(HERE/f'{case}_{m}_RK4.npz') for m in methods}
    initial={m:np.load(HERE/f'initial_{case}_{m}.npz') for m in methods}
    x=final[methods[0]]['x'];t=float(final[methods[0]]['reached'])
    for d in final.values():
        assert np.array_equal(d['x'],x) and float(d['reached'])==t
    ys=np.unique(np.concatenate([d['y'] for d in final.values()]+[d['yv'] for d in final.values()]))
    jets=xjets(case,x);tail=derivative_tail(case)
    maxima={k:0. for k in ['initial_u','initial_v','initial_ut','initial_vt','final_u','final_v']}
    counts={k:0 for k in maxima};corr=[0.,0.]
    for iy,y in enumerate(ys):
        ini=initial_row(case,jets,y)
        fin,correction=final_row(case,x,y,t,tail)
        corr=[max(c,float(b.upper())) for c,b in zip(corr,correction)]
        for m in methods:
            for field,grid,col in [('u','y',0),('v','yv',1)]:
                for row in np.flatnonzero(initial[m][grid]==y):
                    for derivative in [False,True]:
                        name=field+('t' if derivative else '')
                        key='initial_'+name
                        src=name+'_ref' if derivative else field+'0_ref'
                        val=check_values(initial[m][src][row],[r[col+2*derivative] for r in ini],arb('1e-100'))
                        maxima[key]=max(maxima[key],val);counts[key]+=len(x)
                for row in np.flatnonzero(final[m][grid]==y):
                    key='final_'+field
                    val=check_values(final[m][field+'_ref'][row],[r[col] for r in fin],correction[col]+arb('1e-32'))
                    maxima[key]=max(maxima[key],val);counts[key]+=len(x)
        if iy%10==0:print(case,iy+1,len(ys),'seconds',round(time.perf_counter()-start,2),flush=True)
    result=dict(case=case,precision_bits=ctx.prec,t_actual_float=repr(t),
                x_nodes=len(x),distinct_y=len(ys),counts=counts,max_certified_enclosures=maxima,
                uniform_bound_each=1e-13,coordinate_error_contribution=corr,
                derivative_tail=str(tail),elapsed_seconds=time.perf_counter()-start,
                files={str(HERE/f'{case}_{m}_RK4.npz'):hashlib.sha256((HERE/f'{case}_{m}_RK4.npz').read_bytes()).hexdigest() for m in methods})
    (HERE/f'reference_certificate_{case}.json').write_text(json.dumps(result,indent=2),encoding='utf8')
    return result


def nominal_time_correction(case,t):
    """W4 controls derivatives needed for a conservative |u_t|,|v_t|<1e5."""
    A,w,C,K,multiple,kappa=parameters(case)
    if K==1:
        J=(1+w)**4/w;tail=arb(0)
    else:
        J=sum((2*C*(-9*(w*n)**2).exp()*(1+w*n)**4/(w*n)
               for n in range(1,K+1)),arb(0))
        n=K+1
        ratio=(arb(K+2)/(K+1))**4*(-9*w*w*(2*K+3)).exp()
        assert ratio<1
        tail=2*C*(-9*(w*n)**2).exp()*(1+w*n)**4/(w*n)/(1-ratio)
    R=A*(1+kappa)*(J+tail)/2
    assert R<1
    difference=abs(arb(float(t))-arb(1)/100)
    correction=100000*difference
    return correction,dict(weight4_exponent_norm=str(R),
                            time_derivative_bound_each=100000,
                            nominal_time='1/100',actual_time=str(arb(float(t))),
                            correction_upper=float(np.nextafter(float(correction.upper()),np.inf)))


if __name__=='__main__':
    import sys
    if len(sys.argv)>1:
        certify(sys.argv[1])
    else:
        cases=[json.loads((HERE/f'reference_certificate_{c}.json').read_text(encoding='utf8')) for c in ['Gaussian','Sinusoidal']]
        for row in cases:
            corr,time_info=nominal_time_correction(row['case'],float(row['t_actual_float']))
            row['nominal_time_correction']=time_info
            row['nominal_final_enclosures']={}
            for f in ['u','v']:
                raw=float(np.nextafter(row['max_certified_enclosures']['final_'+f],np.inf))
                total=arb(raw)+corr
                assert total<BOUND
                row['nominal_final_enclosures'][f]=float(np.nextafter(float(total.upper()),np.inf))
        result=dict(status='verified_all_stored_sample_values',uniform_bound_each=1e-13,
                    initial=dict(u=1e-13,v=1e-13,ut=1e-13,vt=1e-13),final=dict(u=1e-13,v=1e-13),
                    scope='Stored continuum reference evaluations only; analytic truncation, Arb finite evaluation, float conversion, actual float-coordinate displacement are included.',
                    nominal_final_time='1/100',
                    reference_source_sha256=hashlib.sha256((HERE/'reference_grid.py').read_bytes()).hexdigest(),
                    certificate_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                    proof_status='Analytic proof and Arb computational certificate; not a formal proof assistant verification.',cases=cases)
        (HERE/'reference_certificate.json').write_text(json.dumps(result,indent=2),encoding='utf8')
        print(json.dumps(result,indent=2))
