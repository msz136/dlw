"""Exact local variational checks for continuous DLW, w=s_y."""
import json
from pathlib import Path
import sympy as S

jets = {}
meta = {}
def jet(f, a=0, b=0):
    k=(f,a,b)
    if k not in jets:
        z=S.Symbol(f if (a,b)==(0,0) else f+'_'+('x'*a+'y'*b))
        jets[k]=z;meta[z]=k
    return jets[k]
def deriv(expr, direction):
    terms=[]
    for z in expr.free_symbols:
        if z in meta:
            f,a,b=meta[z]
            terms.append(S.diff(expr,z)*jet(f,a+(direction=='x'),b+(direction=='y')))
    return S.expand(sum(terms))
def derivatives(expr,a,b):
    for _ in range(a):expr=deriv(expr,'x')
    for _ in range(b):expr=deriv(expr,'y')
    return expr
def euler(expr,f):
    out=0
    for z in expr.free_symbols:
        if z in meta and meta[z][0]==f:
            _,a,b=meta[z]
            out+=(-1)**(a+b)*derivatives(S.diff(expr,z),a,b)
    return S.expand(out)
U=jet('U');s=jet('s');w=jet('w')
Ux=jet('U',1);Uxx=jet('U',2);sx=jet('s',1);sxx=jet('s',2)
flows={'U':-U*Ux-Uxx-sxx,'w':-deriv(U*w,'x')+jet('w',2),'s':-jet('A',1)+sxx}
def timed(expr):
    out=0
    for z in expr.free_symbols:
        if z in meta:
            f,a,b=meta[z]
            out+=S.diff(expr,z)*derivatives(flows[f],a,b)
    return S.expand(out)

h0=w*(U**2/S.Integer(2)+Ux+sx/S.Integer(2))
h4=w*(U**3+6*U*Ux+4*Uxx+3*U*sx)
results={}
for name,h in [('mass',w),('momentum',U*w),('hamilton',h0),('fourth',h4)]:
    ht=timed(h)
    # A_y=Uw, s_y=w. Remove the A_xx terms by certified integration by parts.
    if name=='hamilton':
        assert S.diff(ht,jet('A',2))==-w/S.Integer(2)
        ht=ht.subs(jet('A',2),0)+U*w*sxx/S.Integer(2)
    if name=='fourth':
        assert S.diff(ht,jet('A',2))==-3*U*w
        ht=ht.subs(jet('A',2),0)
    ht=ht.subs({z:jet('s',a,b+1) for z,(f,a,b) in list(meta.items()) if f=='w'})
    eu=euler(ht,'U');es=euler(ht,'s')
    results[name]={'euler_U_zero':eu==0,'euler_s_zero':es==0,'euler_U':str(eu),'euler_s':str(es)}
    print(name,eu==0,es==0)

Path(__file__).with_name('continuous_checks.json').write_text(json.dumps(results,indent=2),encoding='utf-8')

# Fifth Riccati coefficient after formal full-divergence reductions.
sxxx=jet('s',3)
h5local=w*(U**4+12*U**2*Ux+12*Ux**2+16*U*Uxx+8*jet('U',3)
           +4*U**2*sx+8*Ux*sx+4*U*sxx+2*sx**2+4*sxxx)
ht5=timed(h5local)+4*jet('A',1)*timed(U*w)
C=0
for z in list(ht5.free_symbols):
    if z in meta and meta[z][0]=='A':
        _,a,b=meta[z];assert a>=1 and b==0
        C+=(-1)**(a-1)*derivatives(S.diff(ht5,z),a-1,0)
        ht5=ht5.subs(z,0)
print('fifth A_x coefficient:',S.factor(C))
assert S.expand(C-4*(sx*jet('w',1)+jet('w',3)))==0
# C=D_y(2s_x^2+4s_xxx), and A_xy=(Uw)_x.
ht5-=deriv(U*w,'x')*(2*sx**2+4*sxxx)
ht5=ht5.subs({z:jet('s',a,b+1) for z,(f,a,b) in list(meta.items()) if f=='w'})
eu=euler(ht5,'U');es=euler(ht5,'s')
results['fifth']={'euler_U_zero':eu==0,'euler_s_zero':es==0,'euler_U':str(eu),'euler_s':str(es),'A_x_coefficient':str(S.factor(C))}
print('fifth',eu==0,es==0)

# Jacobi obstruction for the naive RD^2 replacement of the two-boson bracket.
# Normalized torus integral, f mode (1,1), g mode (1,2), h mode (-2,-3).
k,l,m,n=map(S.Integer,(1,1,1,2))
jacobi=S.Rational(1,2)*k*m*(k/l-m/n)
assert jacobi==S.Rational(1,4)
results['naive_second_bracket']={'jacobiator':str(jacobi),'is_poisson':False}

# Adjoint Riccati recursion for reduced densities c*r_{n-1}.
b=jet('b');p=[None]+[jet('p'+str(k)) for k in range(1,5)]
r=[S.Integer(1)]
for j in range(4):
    r.append(S.expand(b*r[j]+deriv(r[j],'x')-sum(p[k]*r[j-k] for k in range(1,j+1))))
expected3=b**3+3*b*jet('b',1)+jet('b',2)-2*b*p[1]-jet('p1',1)-p[2]
expected4=b**4+6*b**2*jet('b',1)+3*jet('b',1)**2+4*b*jet('b',2)+jet('b',3)\
    -(3*b**2+3*jet('b',1))*p[1]-3*b*jet('p1',1)-jet('p1',2)+p[1]**2\
    -2*b*p[2]-jet('p2',1)-p[3]
assert S.expand(r[3]-expected3)==0
assert S.expand(r[4]-expected4)==0
results['riccati']={'r3_verified':True,'r4_verified':True}
Path(__file__).with_name('continuous_checks.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
