"""Exact DLW error / Darboux-defect identities. SymPy only; no PDE simulation.

Run: python Workspaces/dlw_stage2_20261013/error_lax/verify_error_lax.py
The general noncommutative arguments and operator-domain qualifications are in
REPORT.md. Finite matrices are verification devices, not a claimed integrable
discretization of the differential Lax pair.
"""
from pathlib import Path
import hashlib
import json
import time
import sympy as s

HERE = Path(__file__).resolve().parent
CHECKS = []
x, t = s.symbols('x t', real=True)
h = s.symbols('h', nonzero=True, real=True)


def zero(name, expr):
    entries = list(expr) if isinstance(expr, s.MatrixBase) else [expr]
    residuals = [s.cancel(s.expand(v)) for v in entries]
    ok = all(v == 0 for v in residuals)
    CHECKS.append({'name': name, 'passed': ok, 'entries': len(entries)})
    if not ok:
        raise AssertionError((name, [str(v) for v in residuals if v != 0][:3]))


def fn(name):
    return s.Function(name)(x, t)


def continuum_identities():
    U, w, e, f, V, kappa = [fn(name) for name in ('U', 'w', 'e', 'f', 'V', 'kappa')]
    beta = h*h/32
    flux = lambda u, ww: u*u/2+beta*ww*ww
    n2 = lambda u, ww: s.diff(ww, t)+s.diff(u*ww, x)-s.diff(ww, x, 2)
    zero('exact nonlinear flux difference',
         flux(U+e, w+f)-flux(U,w)-(U*e+e*e/2+2*beta*w*f+beta*f*f))
    zero('exact second physical error equation',
         n2(U+e,w+f)-n2(U,w)
         -(s.diff(f,t)+s.diff(U*f+w*e+e*f,x)-s.diff(f,x,2)))
    Up, wp, Vp = fn('Uplus'), fn('wplus'), fn('Vplus')
    S = lambda uu,ww: s.diff(uu,t)+s.diff(flux(uu,ww),x)+s.diff(uu,x,2)+h*s.diff(ww,x,2)/2
    n1plus = s.diff(Up-U,t)/h+s.diff(flux(Up,wp)-flux(U,w),x)/h
    n1plus += s.diff((Up-U)/h+(wp+w)/2,x,2)
    zero('first PDE residual / heat-potential compatibility',
         S(Up,wp)-S(U,w)+h*s.diff(w,x,2)-h*n1plus)
    sigma = S(U,w)+2*s.diff(V,x)
    Vp = V+h*s.diff(w,x)/2+kappa
    sigmap = S(Up,wp)+2*s.diff(Vp,x)
    zero('sigma difference includes both physical and potential residuals',
         sigmap-sigma-h*n1plus-2*s.diff(kappa,x))
    alpha, eta = U/2+h*w/8, U/2-h*w/8
    riccati = lambda rr,vv: s.diff(rr,t)+s.diff(rr,x,2)+2*rr*s.diff(rr,x)+s.diff(vv,x)
    ea, eb = riccati(alpha,V), riccati(eta,Vp)
    zero('Ealpha = sigma/2 + h*N2/8', ea-sigma/2-h*n2(U,w)/8)
    zero('Eeta = sigma/2 - h*N2/8 + kappa_x',
         eb-sigma/2+h*n2(U,w)/8-s.diff(kappa,x))
    psi, r = fn('psi'), fn('r')
    A = lambda q: s.diff(q,x)-r*q
    H = lambda q: s.diff(q,t)+s.diff(q,x,2)+V*q
    HF = lambda q: s.diff(q,t)+s.diff(q,x,2)+(V+2*s.diff(r,x))*q
    zero('Darboux differential identity acting on arbitrary psi',
         HF(A(psi))-A(H(psi))+riccati(r,V)*psi)


def taylor_lift_identities():
    # y=0 is the midpoint of the first equation; pure symbolic jets.
    eps = s.symbols('eps')
    y = s.symbols('y')
    uj = s.symbols('u0:8')
    wj = s.symbols('w0:8')
    fj = s.symbols('f0:8')
    U = sum(uj[k]*y**k/s.factorial(k) for k in range(8))
    w = sum(wj[k]*y**k/s.factorial(k) for k in range(8))
    F = sum(fj[k]*y**k/s.factorial(k) for k in range(8))
    diff = lambda q: (q.subs(y,eps/2)-q.subs(y,-eps/2))/eps
    avg = lambda q: (q.subs(y,eps/2)+q.subs(y,-eps/2))/2
    zero('centered midpoint backward derivative coefficient',
         s.expand(diff(F)).coeff(eps,2)-fj[3]/24)
    zero('midpoint mean coefficient', s.expand(avg(w)).coeff(eps,2)-wj[2]/8)
    central = (U.subs(y,y+eps)-U.subs(y,y-eps))/(2*eps)
    lift = s.expand(central-s.diff(U,y))
    zero('native physical lift w_h = sampled w - h^2 U_yyy/6',
         lift.coeff(eps,2)-s.diff(U,y,3)/6)
    zero('lift changes midpoint U_yyy coefficient from 1/24 to -1/8',
         s.expand(diff(U)+avg(w)-avg(lift)).coeff(eps,2)
         -(-uj[3]/8+wj[2]/8))


def nc_algebra_identities():
    # These equalities expand in the free noncommutative algebra: all sizes.
    B,T,Tt,Bt,QF,Q0,Q1 = s.symbols('B T Tt Bt QF Q0 Q1', commutative=False)
    A = B*T
    At = Bt*T+B*Tt
    FA = At-QF*A+A*Q0
    FB = Bt-QF*B+B*Q1
    zero('noncommutative quotient residual B*Z = FA-FB*T',
         FA-FB*T-B*(Tt-Q1*T+T*Q0))
    L,dL,Q,dQ,R,dR = s.symbols('L dL Q dQ R dR', commutative=False)
    comm = lambda a,b: a*b-b*a
    zero('exact Lax difference including quadratic commutator',
         comm(Q+dQ,L+dL)+(R+dR)-comm(Q,L)-R
         -comm(Q,dL)-comm(dQ,L)-comm(dQ,dL)-dR)
    T0,T1,T2,Z0,Z1,Z2,Q2,Q3 = s.symbols(
        'T0 T1 T2 Z0 Z1 Z2 Q2 Q3', commutative=False)
    td0,td1,td2=Q1*T0-T0*Q0+Z0,Q2*T1-T1*Q1+Z1,Q3*T2-T2*Q2+Z2
    mono=T2*T1*T0
    monodot=td2*T1*T0+T2*td1*T0+T2*T1*td0
    gamma=Z2*T1*T0+T2*Z1*T0+T2*T1*Z0
    zero('open-chain monodromy residual telescopes with endpoint generators',
         monodot-Q3*mono+mono*Q0-gamma)


def finite_matrix_identities():
    D=s.Matrix([[0,1,-1],[-1,0,1],[1,-1,0]])*s.Rational(5,6)
    r=s.Matrix(s.symbols('r0:3')); rt=s.Matrix(s.symbols('rt0:3'))
    V=s.Matrix(s.symbols('V0:3'))
    diag=lambda v:s.diag(*v)
    A=D-diag(r); Q=-D*D-diag(V); QF=-D*D-diag(V+2*D*r)
    F=-diag(rt)-QF*A+A*Q
    E=rt+D*D*r+2*r.multiply_elementwise(D*r)+D*V
    C1=lambda v:D*diag(v)-diag(v)*D-diag(D*v)
    C2=lambda v:D*D*diag(v)-diag(v)*D*D-2*diag(D*v)*D-diag(D*D*v)
    Lambda=-C2(r)-C1(V)
    zero('exact finite-matrix Darboux anomaly',F+diag(E)-Lambda)
    zero('C2 decomposition into first-order Leibniz anomalies',
         C2(r)-C1(D*r)-D*C1(r)-C1(r)*D)
    U=s.Matrix(s.symbols('u0:3'));w=s.Matrix(s.symbols('w0:3'))
    Ut=s.Matrix(s.symbols('ut0:3'));wt=s.Matrix(s.symbols('wt0:3'))
    kap=s.Matrix(s.symbols('kap0:3'))
    hh=s.Rational(2,3); beta=hh*hh/32
    alpha,eta=U/2+hh*w/8,U/2-hh*w/8
    at,et=Ut/2+hh*wt/8,Ut/2-hh*wt/8
    Vp=V+hh*D*w/2+kap
    ea=at+D*D*alpha+2*alpha.multiply_elementwise(D*alpha)+D*V
    eb=et+D*D*eta+2*eta.multiply_elementwise(D*eta)+D*Vp
    n2=wt+D*U.multiply_elementwise(w)-D*D*w
    flux=U.multiply_elementwise(U)/2+beta*w.multiply_elementwise(w)
    sigma=Ut+D*flux+D*D*U+hh*D*D*w/2+2*D*V
    cq=D*flux-U.multiply_elementwise(D*U)-2*beta*w.multiply_elementwise(D*w)
    cp=D*U.multiply_elementwise(w)-U.multiply_elementwise(D*w)-w.multiply_elementwise(D*U)
    zero('finite-grid Ealpha includes point-product defects',
         ea-sigma/2-hh*n2/8+cq/2+hh*cp/8)
    zero('finite-grid Eeta includes point-product defects',
         eb-sigma/2+hh*n2/8-D*kap+cq/2-hh*cp/8)
    # Generic 2x2 matrices verify the inverse-normalization and trace formulas.
    cc=s.Matrix(2,2,s.symbols('c0:4'))
    qq=s.Matrix(2,2,s.symbols('q0:4'))
    rr=s.Matrix(2,2,s.symbols('z0:4'))
    G,beta0=s.symbols('G beta0')
    ci=cc.inv(); L=-G*ci+beta0*s.eye(2)
    mdot=qq*cc-cc*qq+rr
    Ldot=G*ci*mdot*ci
    R=G*ci*rr*ci
    zero('inverse-monodromy normalized Lax source',
         Ldot-(qq*L-L*qq)-R)
    # Polynomial trace proof is independent of the inverse expression.
    LL=s.Matrix(2,2,s.symbols('l0:4'))
    for n in range(1,5):
        derivative=sum((s.trace(LL**i*(qq*LL-LL*qq+rr)*LL**(n-1-i))
                        for i in range(n)),s.Integer(0))
        zero(f'trace-power defect rate n={n}',
             derivative-n*s.trace(LL**(n-1)*rr))
    I=s.eye(2); Z=s.zeros(2)
    Ltilde=s.Matrix([[2,3],[5,7]])
    Lref=s.Matrix([[1,2],[0,4]])
    Qtilde=s.Matrix([[3,1],[-1,2]]);Qref=s.Matrix([[0,2],[1,3]])
    C=s.BlockMatrix([[I,Z],[-I,I]]).as_explicit()
    Cinv=s.BlockMatrix([[I,Z],[I,I]]).as_explicit()
    block=s.BlockMatrix([[Lref,Z],[Ltilde-Lref,Ltilde]]).as_explicit()
    zero('exact error block is constant conjugate to original direct sum',
         block-C*s.diag(Lref,Ltilde)*Cinv)
    for n in range(1,5):
        zero(f'block spectral trace contains only original spectra n={n}',
             s.trace(block**n)-s.trace(Lref**n)-s.trace(Ltilde**n))
    # Same autonomous isospectral flow, changing spectrum of the difference.
    N=s.diag(1,-1); L0=N; L1=s.Matrix([[0,1],[1,0]])
    gen=lambda a:N*a-a*N
    vel=lambda a:gen(a)*a-a*gen(a)
    err=L1-L0
    rate=s.trace(2*err*(vel(L1)-vel(L0)))
    zero('same autonomous double-bracket flow: each quadratic trace constant',
         s.trace(2*L1*vel(L1)))
    zero('error quadratic trace is not conserved (rate = -16)',rate+16)
    return {'generic_isospectral_counterexample':{
        'flow':'L_t=[[diag(1,-1),L],L]',
        'L_reference':[[1,0],[0,-1]],'L_perturbed':[[0,1],[1,0]],
        'd_trace_error_squared_dt':str(rate),
        'scope':'generic Lax counterexample; not asserted to be a DLW solution'}}


def dlw_grid_witness():
    """Hamilton DLW RHS has N1=N2=0, but sampled matrix Lax is not exact."""
    m,n=3,3
    hh,dx,c,gamma=s.Rational(2,3),s.Rational(3,5),s.Integer(-4),s.Integer(0)
    E=s.Matrix([[0,1,0],[0,0,1],[1,0,0]])
    mean=s.ones(m)/m; P=s.eye(m)-mean
    dy=(s.eye(m)-E.T)/hh; my=(s.eye(m)+E.T)/2
    R=hh*sum(((s.Rational(ell,m)-s.Rational(1,2))*E**ell
              for ell in range(1,m)),s.zeros(m))
    D=s.Matrix([[0,1,-1],[-1,0,1],[1,-1,0]])/(2*dx)
    p=s.zeros(m,n)
    shape=s.Matrix([[s.Rational(2,7),s.Rational(-1,7),s.Rational(-1,7)]])
    ss=shape.col_join(-shape).col_join(s.zeros(1,n))
    U=p+s.ones(m,1)*s.Matrix([[ (gamma-sum(p[j,i]*ss[j,i] for j in range(m))/m)/c
                               for i in range(n)]])
    w=ss+c*s.ones(m,n)
    deriv=lambda f:f*D.T
    point=lambda a,b:a.multiply_elementwise(b)
    beta=hh*hh/32
    f=point(U,w)-deriv(w)-gamma*s.ones(m,n)
    flux=point(U,U)/2+beta*point(w,w)
    k=flux+deriv(U)+R*deriv(w)
    pt,st=-P*deriv(k),-P*deriv(f)
    bdot=s.Matrix([[-sum(pt[j,i]*ss[j,i]+p[j,i]*st[j,i] for j in range(m))/(m*c)
                   for i in range(n)]])
    Ut=pt+s.ones(m,1)*bdot;wt=st
    n1=dy*(Ut+deriv(flux))+deriv(deriv(dy*U+my*w))
    n2=wt+deriv(point(U,w))-deriv(deriv(w))
    zero('DLW Hamilton-grid witness: exact first equation residual',n1)
    zero('DLW Hamilton-grid witness: exact second equation residual',n2)
    S=Ut+deriv(flux)+deriv(deriv(U))+hh*deriv(deriv(w))/2
    pi_x=s.ones(n)/n
    Dinv=(D+pi_x).inv()-pi_x
    V=-s.Rational(1,2)*S*Dinv.T
    sigma=S+2*deriv(V)
    kappa=(E-s.eye(m))*V-hh*deriv(w)/2
    zero('DLW Hamilton-grid witness: potential x compatibility sigma=0',sigma)
    zero('DLW Hamilton-grid witness: potential y compatibility kappa=0',kappa)
    total_defect_squared=s.Integer(0); records=[]
    for j in range(m):
        nj=(j+1)%m
        col=lambda f: s.Matrix(f.row(j)).T
        uu,ww,vv=col(U),col(w),col(V)
        u_t,w_t=col(Ut),col(wt)
        vn=s.Matrix(V.row(nj)).T
        alpha,eta=uu/2+hh*ww/8,uu/2-hh*ww/8
        at,et=u_t/2+hh*w_t/8,u_t/2-hh*w_t/8
        A=D-s.diag(*alpha);B=D-s.diag(*eta);T=B.inv()*A
        Q=-D*D-s.diag(*vv);Qn=-D*D-s.diag(*vn)
        At=-s.diag(*at);Bt=-s.diag(*et)
        Tt=B.inv()*(At-Bt*T)
        Z=Tt-Qn*T+T*Q
        ea=at+D*D*alpha+2*point(alpha,D*alpha)+D*vv
        eb=et+D*D*eta+2*point(eta,D*eta)+D*vn
        C1=lambda f:D*s.diag(*f)-s.diag(*f)*D-s.diag(*(D*f))
        C2=lambda f:D*D*s.diag(*f)-s.diag(*f)*D*D-2*s.diag(*(D*f))*D-s.diag(*(D*D*f))
        la=-C2(alpha)-C1(vv);lb=-C2(eta)-C1(vn)
        zero(f'DLW Hamilton-grid witness: full Lax anomaly identity j={j}',
             B*Z+s.diag(*ea)-s.diag(*eb)*T-la+lb*T)
        size=s.factor(sum(z*z for z in Z))
        total_defect_squared+=size
        records.append({'j':j,'B_determinant':str(B.det()),
                        'lax_defect_frobenius_squared_exact':str(size),
                        'lax_defect_frobenius_float':float(s.sqrt(size))})
    assert total_defect_squared != 0
    CHECKS.append({'name':'DLW Hamilton-grid witness: matrix Lax defect is nonzero',
                   'passed':True,'entries':m*n*n})
    return {'M':m,'Nx':n,'h':str(hh),'dx':str(dx),'c':str(c),'gamma':str(gamma),
            'p':[[str(v) for v in p.row(j)] for j in range(m)],
            's':[[str(v) for v in ss.row(j)] for j in range(m)],
            'U_t':[[str(v) for v in Ut.row(j)] for j in range(m)],
            'w_t':[[str(v) for v in wt.row(j)] for j in range(m)],
            'V':[[str(v) for v in V.row(j)] for j in range(m)],
            'N1':'0','N2':'0','sigma':'0','kappa':'0','sites':records,
            'scope':'Exact rational finite-grid counterexample to naive differential-Lax inheritance.'}


def main():
    start=time.perf_counter()
    continuum_identities()
    taylor_lift_identities()
    nc_algebra_identities()
    extra=finite_matrix_identities()
    witness=dlw_grid_witness()
    out={'passed':all(c['passed'] for c in CHECKS),'check_count':len(CHECKS),
         'checked_scalar_entries':sum(c['entries'] for c in CHECKS),
         'checks':CHECKS,'dlw_hamilton_grid_lax_defect_witness':witness,**extra,
         'elapsed_seconds':round(time.perf_counter()-start,3),'sympy_version':s.__version__,
         'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'interpretation':'Exact algebra certificates. General operator proofs and trace/domain hypotheses are in REPORT.md.'}
    (HERE/'exact_checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'passed':out['passed'],'checks':out['check_count'],
                      'entries':out['checked_scalar_entries'],'seconds':out['elapsed_seconds']},
                     ensure_ascii=False))


if __name__=='__main__':
    main()
