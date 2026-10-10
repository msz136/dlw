from pathlib import Path
import sympy as S,json
from bs4 import BeautifulSoup
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
x,y,t,h,a=S.symbols('x y t h a')
u=sum(S.Function(f'u{i}')(x,t)*y**i/S.factorial(i) for i in range(6))
v=sum(S.Function(f'v{i}')(x,t)*y**i/S.factorial(i) for i in range(5))
Dx=lambda f,n=1:S.diff(f,x,n)
Dy=lambda f,n=1:S.diff(f,y,n)
Dt=lambda f:S.diff(f,t)
at=lambda f:S.expand(f.subs(y,0))
checks=[]
def ck(name,e):
    e=S.expand(e)
    assert e==0,(name,e)
    checks.append(name)
def shifted(f,offset):
    return f.subs(y,offset*h)
def W(offset):
    return shifted(v,offset)-(shifted(u,offset+1)-shifted(u,offset-1))/(2*h)
def A(offset):
    return shifted(u,offset)**2/2+2*a*shifted(u,offset)+h*h*(W(offset)**2/32-W(offset)/4)
def coeff(f,n):return S.expand(f).coeff(h,n)
half=S.Rational(1,2)
P=(shifted(u,half)-shifted(u,-half))/h
Wavg=(W(half)+W(-half))/2
N1=Dt(P)+Dx((A(half)-A(-half))/h)+Dx(P+Wavg,2)
A0=u*u/2+2*a*u;W0=v-Dy(u);A2=W0**2/32-W0/4
C1=Dy(Dt(u))+Dx(v,2)+Dx(Dy(A0))
T1=Dy(Dt(u),3)/24+Dx(Dy(A0,3)/24+Dy(A2))+Dx(Dy(v,2)/8-Dy(u,3)/4,2)
ck('PE first leading Taylor coefficient',coeff(N1,0)-at(C1))
ck('PE first h2 Taylor coefficient',coeff(N1,2)-at(T1))
N2=Dt(shifted(v,0))+Dx((A(1)-A(-1))/(2*h)+(shifted(u,0)+2*a)*W(0)-4*shifted(u,0))+Dx((shifted(u,1)-shifted(u,-1))/(2*h)+h*h/4*(W(1)-2*W(0)+W(-1))/h**2,2)
C2=Dt(v)+Dx(Dy(u),2)+Dx((u+2*a)*v-4*u)
T2=Dx(Dy(u)*Dy(u,2)/2+Dy(A2))+Dx(Dy(v,2)/4-Dy(u,3)/12,2)
ck('PE second leading Taylor coefficient',coeff(N2,0)-at(C2))
ck('PE second h2 Taylor coefficient',coeff(N2,2)-at(T2))
e=S.symbols('e',nonzero=True)
d1=(e-1/e)/(2*h);d2=(e-2+1/e)/h**2
ck('D2 minus D1 squared stencil',S.cancel(d2-d1*d1+h*h*d2*d2/4))
s,k,K,cot=S.symbols('s k K cot')
mat=S.Matrix([[s-K,S.I*(-k*h*h/4+K*h*cot/2)],[-4*S.I*k,s+K]])
ck('x-discrete PE characteristic',mat.det()-(s*s-K*K+h*h*k*k-2*h*k*K*cot))
C=S.Matrix([[1,S.Rational(1,3)],[-1,1]])
ck('C two-soliton minor',C.det()-S.Rational(4,3))
ck('C f mixed coefficient',C.det()*S.Rational(4,3)*2-S.Rational(32,9))
soup=BeautifulSoup((ROOT/'report/dlw_paper_draft.html').read_text(encoding='utf-8'),'html.parser')
tables=soup.select('table.comparison')
time_rows=[[float(c.get_text()) for c in row.select('td')] for row in tables[1].select('tbody tr')]
relative=[abs(c-r)/r*100 for _,r,c in time_rows]
reductions=[]
for row in tables[2].select('tbody tr'):
    fixed,moving=[[float(z) for z in c.get_text().split('/')] for c in row.select('td')]
    reductions.extend([(1-m/f)*100 for f,m in zip(fixed,moving)])
result={'additional_checks':len(checks),'checks':checks,'max_CN_RK4_percent_difference':max(relative),
        'moving_error_reduction_percent':[min(reductions),max(reductions)]}
(HERE/'supplement.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
