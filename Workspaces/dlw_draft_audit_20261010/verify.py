from pathlib import Path
import hashlib, json, re, itertools
import sympy as S
from bs4 import BeautifulSoup

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
src=ROOT/'Workspaces/dlw_paper_20261009/manuscript.md'
page=ROOT/'report/dlw_paper_draft.html'
checks=[]
def check(name, expr):
    value=S.simplify(S.expand(expr))
    assert value==0,(name,value)
    checks.append({'name':name,'residual':str(value)})

source=src.read_text(encoding='utf-8')
soup=BeautifulSoup(page.read_text(encoding='utf-8'),'html.parser')
html_math=[n.get_text() for n in soup.select('annotation[encoding="application/x-tex"]')]
source_math=[m[0][2:-2] if m[0].startswith('$$') else m[0][1:-1]
             for m in re.finditer(r'\$\$[\s\S]*?\$\$|(?<!\$)\$(?!\$)[^\n$]+\$',source)]
assert [t.strip() for t in html_math]==[t.strip() for t in source_math]
(HERE/'reviewed_source.md').write_text(source,encoding='utf-8')

x,y,t,h,a=S.symbols('x y t h a',real=True)
D=lambda f,*v:S.diff(f,*v)
r,b=S.Function('r')(x,y,t),S.Function('b')(x,y,t)
f,g=S.exp((b+r)/2),S.exp((b-r)/2)
def hi(f,g,nx=0,ny=0,nt=0):
    return sum((-1)**(i+j+k)*S.binomial(nx,i)*S.binomial(ny,j)*S.binomial(nt,k)*
        D(f,x,nx-i,y,ny-j,t,nt-k)*D(g,x,i,y,j,t,k)
        for i in range(nx+1) for j in range(ny+1) for k in range(nt+1))
E=D(b,x,2)+D(r,x)**2+D(r,t)+2*a*D(r,x)
H=D(b,y,t)+D(r,x,x,y)+2*(D(r,x)+a)*D(b,x,y)-4*D(r,x)
check('continuous B / fg', (hi(f,g,2)+hi(f,g,nt=1)+2*a*hi(f,g,1))/(f*g)-E)
check('continuous cubic Hirota', (hi(f,g,2,1)+hi(f,g,ny=1,nt=1)+2*a*hi(f,g,1,1)-4*hi(f,g,1))/(f*g)-H-D(r,y)*E)
u,v=2*D(r,x),2*D(b,x,y)
check('DLW first residual = 2 E_xy',D(u,y,t)+D(v,x,2)+D((u+2*a)*D(u,y),x)-2*D(E,x,y))
check('DLW second residual = 2 H_x',D(v,t)+D(u,x,x,y)+D((u+2*a)*v-4*u,x)-2*D(H,x))

al,be,bp=[S.Function(z)(x,t) for z in ('alpha','beta','beta_plus')]
u=D(2*al-be-bp,x); w=D(bp-be,x); Z=D(2*al+be+bp,x)
A=D(al+be,x,2)+D(al-be,x)**2+D(al-be,t)+(2*a-h)*D(al-be,x)
C=D(al+bp,x,2)+D(al-bp,x)**2+D(al-bp,t)+(2*a+h)*D(al-bp,x)
check('log equations sum -> (25)',D(A+C,x)-D(u,t)-D((u*u+w*w)/2+2*a*u-h*w,x)-D(Z,x,2))
check('log equations difference -> (25)',D(A-C,x)-D(w,t)-D((u+2*a)*w-h*u,x)+D(w,x,2))
e=S.symbols('e',nonzero=True)
dm=(1-1/e)/h; d0=(e-1/e)/(2*h); mm=(1+1/e)/2; mp=(1+e)/2; lap=(e-2+1/e)/h**2
check('PE delta-minus identity',dm-mm*d0+h*h*lap*dm/4)
check('PE averaging identity',mp*dm-d0)
check('PE second averaging identity',mp*mm-1-h*h*lap/4)

Q,R,M,N=[S.Function(z)(x,t) for z in ('Q','R','M','N')]
u=2*D(Q,x)/Q; w=h*(1-Q*R)
K=D(M+N,x)+h*h*(Q*Q*R*R-1)/4
EQ=D(Q,t)+D(Q,x,2)+2*a*D(Q,x)+K*Q
ER=D(R,t)-D(R,x,2)+2*a*D(R,x)-K*R
check('Cole-Hopf quadratic identity',D(u,x)+u*u/2-2*D(Q,x,2)/Q)
check('PF product evolution',D(Q*R,t)-D(Q*R,x,2)+2*a*D(Q*R,x)+2*D(D(Q,x)*R,x)-R*EQ-Q*ER)
check('PF omega equation',D(w,t)-D(w,x,2)+D((u+2*a)*w-h*u,x)+h*(R*EQ+Q*ER))
check('PF Q equation -> potential u equation',2*D(EQ/Q,x)-D(u,t)-D(D(u,x)+u*u/2+2*a*u+2*D(M+N,x)+w*w/2-h*w,x))

U,w,V=[S.Function(z)(x,t) for z in ('U','w','V')]
alpha=U/2+h*w/8; eta=U/2-h*w/8
Ea=D(alpha,t)+D(alpha,x,2)+2*alpha*D(alpha,x)+D(V,x)
Ee=D(eta,t)+D(eta,x,2)+2*eta*D(eta,x)+D(V,x)+h*D(w,x,2)/2
check('Lax residual difference',Ea-Ee-h*(D(w,t)-D(w,x,2)+D(U*w,x))/4)
check('Lax residual sum',Ea+Ee-D(U,t)-D(U*U/2+h*h*w*w/32,x)-D(U,x,2)-h*D(w,x,2)/2-2*D(V,x))
z,rr=S.Function('z')(x,t),S.Function('rr')(x,t)
L=lambda f,v:D(f,t)+D(f,x,2)+v*f
B=lambda f:D(f,x)-rr*f
check('Darboux identity (52)',L(B(z),V+2*D(rr,x))-B(L(z,V))+(D(rr,t)+D(rr,x,2)+2*rr*D(rr,x)+D(V,x))*z)

# Independent determinant check through principal-minor exponential expansion.
def tau_terms(p,q,rho,hh,aa,j,n,ss):
    terms=[]; dd=hh/2
    lam=lambda z:(z+dd)/(z-dd)
    for k in range(len(p)+1):
        for I in itertools.combinations(range(len(p)),k):
            coeff=S.Matrix([[1/(p[i]+q[l]) for l in I] for i in I]).det() if I else S.Integer(1)
            for i in I:
                coeff*=rho[i]*(-(p[i]-ss)/(q[i]+ss))**n*(lam(p[i]-aa)*lam(q[i]+aa))**j
            terms.append((coeff,sum((p[i]+q[i] for i in I),S.Integer(0)),sum((q[i]**2-p[i]**2 for i in I),S.Integer(0))))
    return terms
def bill(F,G,ss):
    # Collect each exponential coefficient, stronger than one evaluation point.
    out={}
    for c,k,o in F:
        for d,l,v in G:
            key=(k+l,o+v)
            out[key]=out.get(key,0)+c*d*((k-l)**2+o-v+2*ss*(k-l))
    return list(out.values())
for nn in range(1,5):
    p=list(map(S.Rational,range(1,nn+1))); q=[S.Rational(i+1,3) for i in range(nn)]
    rho=[S.Rational(i+1,2) for i in range(nn)]; aa=S.Integer(7); hh=S.Rational(1,5)
    for j in (-2,0,3):
        for sign in (-1,1):
            ss=aa+sign*hh/2
            for n in (0,1,2):
                residual=bill(tau_terms(p,q,rho,hh,aa,j,n+1,ss),tau_terms(p,q,rho,hh,aa,j,n,ss),ss)
                for k,ex in enumerate(residual):check(f'Gram N{nn} j{j} sign{sign} n{n} coeff{k}',ex)
        F=tau_terms(p,q,rho,hh,aa,j,1,aa-hh/2)
        G=tau_terms(p,q,rho,hh,aa,j+1,0,aa+hh/2)
        for k,ex in enumerate(bill(F,G,aa+hh/2)):check(f'Gram crossed N{nn} j{j} coeff{k}',ex)
zz,ww,dd=S.symbols('z w d',nonzero=True)
check('spectral shifted layer identity',-(zz-dd)/(ww+dd)*(zz+dd)/(zz-dd)*(ww+dd)/(ww-dd)+(zz+dd)/(ww-dd))
check('centered amplitude squared identity',((zz+dd)/(ww-dd))**2/((zz+dd)/(zz-dd)*(ww+dd)/(ww-dd))-(zz/ww)**2*(1-dd*dd/zz**2)/(1-dd*dd/ww**2))

# Grid source for FD: the nonlinear discrete product rule is not exact.
um,u0,up,aa=S.symbols('um u0 up aa')
check('FD nonlinear product defect',(up*up/2+2*aa*up-um*um/2-2*aa*um)/(2*h)-(u0+2*aa)*(up-um)/(2*h)-h*h/2*((up-um)/(2*h))*((up-2*u0+um)/h**2))
sigma,k,cot=S.symbols('sigma k cot')
matrix=S.Matrix([[sigma-k*k,S.I*(-k*h*h/4+k*k*h*cot/2)],[-4*S.I*k,sigma+k*k]])
check('PE Fourier characteristic polynomial',matrix.det()-(sigma*sigma-k**4+k*k*h*h-2*k**3*h*cot))
ell=S.symbols('ell',nonzero=True)
matrix=S.Matrix([[S.I*ell*sigma,-k*k],[-S.I*(k*k*ell+4*k),sigma]])
check('continuous Fourier characteristic polynomial',matrix.det()-S.I*ell*(sigma*sigma-k**4-4*k**3/ell))

result={'source':str(src),'html':str(page),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),
 'html_sha256':hashlib.sha256(page.read_bytes()).hexdigest(),'math_expressions_matched':len(html_math),
 'symbolic_checks':len(checks),'checks':checks}
(HERE/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},ensure_ascii=False))
