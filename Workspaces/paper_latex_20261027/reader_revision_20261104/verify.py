from pathlib import Path
import re,sys,json
from bs4 import BeautifulSoup
import sympy as s
ROOT=Path(__file__).resolve().parents[3];SOURCE=ROOT
sys.path.insert(0,str(SOURCE/'Workspaces/paper_latex_20261027/notation_layout_20261103'))
from edit_manuscript import display_blocks
tex=(ROOT/'pdf/dlw/main.tex').read_text('utf-8');html=(ROOT/'dlw-paper.html').read_text('utf-8')
soup=BeautifulSoup(html,'html.parser')
norm=lambda x:re.sub(r'\s+','',x)
td={tag:norm(body) for _,_,tag,body in display_blocks(tex)}
hd={}
for ann in soup.select('.katex-display annotation'):
 raw=ann.get_text();tags=re.findall(r'\\tag\{([^}]+)\}',raw)
 if not tags:continue
 body=re.sub(r'\\tag\{[^}]+\}','',raw)
 if raw.startswith(r'\begin{align*}'):
  body=body.removeprefix(r'\begin{align*}').removesuffix(r'\end{align*}')
  # compare the separate tagged rows to display_blocks.
  parts=re.split(r'\\tag\{([^}]+)\}',raw.removeprefix(r'\begin{align*}').removesuffix(r'\end{align*}'))
  for i in range(1,len(parts),2):
   b=parts[i-1].strip().lstrip('\\').rstrip('\\').strip()
   hd[parts[i]]=norm(b)
 else:hd[tags[0]]=norm(body)
diff={k:(v,hd.get(k)) for k,v in td.items() if v!=hd.get(k)}
assert not diff,diff
tags=re.findall(r'\\tag\{([^}]+)\}',tex)
assert len(tags)==len(set(tags))
main=[int(n) for n in tags if n.isdigit()];assert main==list(range(1,len(main)+1))
assert len(soup.select('#references ol > li'))==20
assert 'S_k' not in tex and 'C_k' not in tex and 'A_k' not in tex
assert not re.search(r'\((?:9[0-9]|10[01])\)',tex),'stale equation reference'
# Check citation numerals appear as text in HTML, not old equation numbers.
for section in ['section-2.2','section-3.3','appendix-A','appendix-C']:
 assert soup.find(id=section)

# Exact arithmetic checks of both Gram pairings for a full 2x2 constant matrix.
x,t=s.symbols('x t');a=s.Integer(2);h=s.Rational(1,4)
p=[s.Integer(6),s.Integer(4)];q=[s.Integer(-5),s.Integer(-3)]
alpha=[2,3];beta=[-1,2];C=s.Matrix([[1,s.Rational(1,7)],[s.Rational(2,9),1]])
def tau(n,k,b):
 return s.det(s.Matrix(2,2,lambda i,j:C[i,j]+s.Rational(alpha[i]*beta[j],p[i]+q[j])*(-(q[j]+a)/(p[i]-a))**n*((1+h/(p[i]-a))/(1-h/(q[j]+a)))**k*s.exp((p[i]+q[j])*(x-2*(b-a)*t)+(q[j]**2-p[i]**2)*t))).expand()
def residual(f,g,sigma):
 r=s.diff(f,x,2)*g-2*s.diff(f,x)*s.diff(g,x)+f*s.diff(g,x,2)+s.diff(f,t)*g-f*s.diff(g,t)+2*sigma*(s.diff(f,x)*g-f*s.diff(g,x))
 return s.simplify(r.subs({x:0,t:0}))
checks={}
for b in [a,a+h/2,s.Rational(9,5)]:
 for k in [-1,2]:
  f=tau(0,k,b);g=tau(1,k,b);gm=tau(1,k-1,b)
  for label,r in [('same',residual(f,g,b)),('backward',residual(f,gm,b-h))]:
   assert r==0,(b,k,label,r)
   checks[f'b={b},k={k},{label}']=str(r)

# Independent product-rule expansion of the component Lax identity.
b,h=s.symbols('b h');r=s.Function('r')(x,t);qf=s.Function('q')(x,t)
F=s.Function('F')(x,t);Fm=s.Function('Fm')(x,t)
pm=s.Function('pm')(x);pk=s.Function('pk')(x)
Dx=lambda f:s.diff(f,x)
M=lambda f,V:s.diff(f,x,2)-2*b*Dx(f)+2*s.diff(V,x,2)*f
L=lambda fm,fk:Dx(fm)+Dx(r)*fm-Dx(fk)-(Dx(qf)-h)*fk
lhs=s.diff(r,x,t)*pm-s.diff(qf,x,t)*pk+L(M(pm,Fm),M(pk,F))-M(L(pm,pk),F)+2*s.diff(qf,x,2)*L(pm,pk)
expected=(2*s.diff(Fm,x,2)-2*s.diff(F,x,2)+2*(s.diff(qf,x,2)-s.diff(r,x,2)))*Dx(pm)+(s.diff(r,x,t)-s.diff(r,x,3)+2*b*s.diff(r,x,2)+2*s.diff(Fm,x,3)+2*Dx(r)*(s.diff(Fm,x,2)-s.diff(F,x,2))+2*Dx(r)*s.diff(qf,x,2))*pm+(-s.diff(qf,x,t)+s.diff(qf,x,3)-2*(b+Dx(qf)-h)*s.diff(qf,x,2)-2*s.diff(F,x,3))*pk
assert s.expand(lhs-expected)==0
zero=s.expand(expected).subs(s.diff(r,x,t),s.diff(r,x,3)-2*(b+Dx(r))*s.diff(r,x,2)-2*s.diff(Fm,x,3)).subs(s.diff(qf,x,t),s.diff(qf,x,3)-2*(b+Dx(qf)-h)*s.diff(qf,x,2)-2*s.diff(F,x,3))
zero=s.expand(zero).subs(s.diff(Fm,x,2),s.diff(F,x,2)-s.diff(qf,x,2)+s.diff(r,x,2))
assert s.expand(zero)==0
report={'numbered_equations':len(tags),'main_equations':len(main),'html_tex_equations_identical':True,'references':20,'gram_exact_rational_residuals':checks,'lax_component_expansion_symbolic_zero':True,'numerical_experiments_recomputed':False}
(Path(__file__).resolve().parent/'verification.json').write_text(json.dumps(report,indent=2),'utf-8')
print(json.dumps(report,indent=2))
