"""Symbolic checks for a SPECIFIC logarithmic-operator replacement.

Both tau fields are placed at y=j*h. D+ acts on logarithmic potentials,
and nonlinear products on an edge use endpoint arithmetic means.
This is a new model, not the previous staggered integrable pair.
"""
import sympy as s


def zero(expr):
    ans=s.factor(s.together(expr))
    assert ans==0,ans


def main():
    x,y,t=s.symbols('x y t')
    a,lam,h=s.symbols('a lambda h',nonzero=True)
    q=s.Function('q')(x,y,t)
    r=s.Function('r')(x,y,t)
    f=s.exp((r+q)/2)
    g=s.exp((r-q)/2)
    dx=lambda F,G:s.diff(F,x)*G-F*s.diff(G,x)
    B=lambda F,G:(s.diff(F,x,2)*G-2*s.diff(F,x)*s.diff(G,x)
        +F*s.diff(G,x,2)+s.diff(F,t)*G-F*s.diff(G,t)+2*a*dx(F,G))
    S=s.diff(r,x,2)+s.diff(q,x)**2+s.diff(q,t)+2*a*s.diff(q,x)
    zero(B(f,g)/(f*g)-S)
    dyB=B(s.diff(f,y),g)-B(f,s.diff(g,y))
    C=s.diff(q,x,2,y)+s.diff(r,y,t)+2*(s.diff(q,x)+a)*s.diff(r,x,y)+2*lam*s.diff(q,x)
    zero((dyB+2*lam*dx(f,g))/(f*g)-s.diff(q,y)*S-C)
    print('PASS: continuous logarithmic-potential identities')

    # Discrete endpoint potentials: q0,r0 and q1,r1 at j and j+1.
    q0,q1,r0,r1=[s.Function(z)(x,t) for z in ['q0','q1','r0','r1']]
    F0,G0=s.exp((r0+q0)/2),s.exp((r0-q0)/2)
    F1,G1=s.exp((r1+q1)/2),s.exp((r1-q1)/2)
    Clog=(s.diff(q1-q0,x,2)+s.diff(r1-r0,t)
          +(s.diff(q1+q0,x)+2*a)*s.diff(r1-r0,x))/h+lam*s.diff(q1+q0,x)
    cross=(B(F1,G0)/(F1*G0)-B(F0,G1)/(F0*G1))/h
    cross+=lam*(dx(F1,G0)/(F1*G0)+dx(F0,G1)/(F0*G1))
    zero(cross-Clog)
    print('PASS: logarithmic edge equation equals normalized cross-bilinear expression')

    S0=s.diff(r0,x,2)+s.diff(q0,x)**2+s.diff(q0,t)+2*a*s.diff(q0,x)
    S1=s.diff(r1,x,2)+s.diff(q1,x)**2+s.diff(q1,t)+2*a*s.diff(q1,x)
    u0,u1=2*s.diff(q0,x),2*s.diff(q1,x)
    v=2*s.diff(r1-r0,x)/h
    ubar=(u0+u1)/2
    N1=s.diff(u1-u0,t)/h+s.diff((ubar+2*a)*(u1-u0)/h,x)+s.diff(v,x,2)
    N2=s.diff(v,t)+s.diff((ubar+2*a)*v,x)+s.diff(u1-u0,x,2)/h+2*lam*s.diff(ubar,x)
    zero(N1-2*s.diff(S1-S0,x)/h)
    zero(N2-2*s.diff(Clog,x))
    print('PASS: closed nonlinear equations follow by differentiation/differencing')

    E,A,C,R,k,w=s.symbols('E A C R k omega')
    op=lambda poly,coef:s.diff(poly,E)*coef*E
    dxx=lambda poly:op(op(poly,k),k)
    BB=lambda F,G:dxx(F)*G-2*op(F,k)*op(G,k)+F*dxx(G)+op(F,w)*G-F*op(G,w)+2*a*(op(F,k)*G-F*op(G,k))
    XX=lambda F,G:op(F,k)*G-F*op(G,k)
    F0,G0,F1,G1=1+A*E,1+C*E,1+A*R*E,1+C*R*E
    quartic=s.expand(F0*G1*BB(F1,G0)-F1*G0*BB(F0,G1)
          +lam*h*(F0*G1*XX(F1,G0)+F1*G0*XX(F0,G1)))
    # The previous positive single-soliton parameters; solve the E coefficient.
    concrete=s.factor(quartic.subs({A:s.Rational(1,12),C:s.Rational(1,3),k:3,w:3,a:2,lam:-2}))
    Rstar=(8-3*h)/(8+3*h)
    remainder=s.factor(concrete.subs(R,Rstar))
    zero(remainder+s.Rational(45,4)*h**3/(8+3*h)**2*E**2)
    print('One-soliton R=(8-3h)/(8+3h): quartic residual =',remainder)
    print('At h=1/10:',s.factor(remainder.subs(h,s.Rational(1,10))))
    assert remainder!=0

    # A nonempty but trivial exponential-background tau family.
    k0,ell,j=s.symbols('k0 ell j')
    qbg=k0*x-(k0**2+2*a*k0)*t+ell*j*h
    rbg=-2*lam*k0*j*h*t
    Sb=s.diff(rbg,x,2)+s.diff(qbg,x)**2+s.diff(qbg,t)+2*a*s.diff(qbg,x)
    Cb=(s.diff(qbg.subs(j,j+1)-qbg,x,2)+s.diff(rbg.subs(j,j+1)-rbg,t)
        +(s.diff(qbg.subs(j,j+1)+qbg,x)+2*a)*s.diff(rbg.subs(j,j+1)-rbg,x))/h+lam*s.diff(qbg.subs(j,j+1)+qbg,x)
    zero(Sb); zero(Cb)
    print('PASS: explicit exponential-background tau family (u=2*k0, v=0)')


if __name__=='__main__':
    main()
