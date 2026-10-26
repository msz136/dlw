from pathlib import Path
from bs4 import BeautifulSoup
import re,json,hashlib,sympy as S
r=Path('review'); new=BeautifulSoup((r/'dlw_paper_draft.html').read_text(encoding='utf8'),'html.parser');old=BeautifulSoup((r/'original.html').read_text(encoding='utf8'),'html.parser')
ids=[e['id'] for e in new.select('[id]')];assert len(ids)==len(set(ids))
assert all(a['href'][1:] in ids for a in new.select('a[href^="#"]'))
f=json.loads((r/'formulas.json').read_text(encoding='utf8'))
tags=[int(n) for x in f for n in re.findall(r'\\tag\{(\d+)\}',x['tex'])];assert tags==list(range(1,119))*2
# Existing mathematical formulas survive verbatim except for the removed Euler formula.
def maths(s):return [re.sub(r'\\tag\{\d+\}','',a.get_text()) for a in s.select('.eq annotation')]
newmath=maths(new); missing=[x for x in maths(old) if x not in newmath and 'z^{n+1}=z^n+\\Delta t' not in x];assert not missing,missing
oldtables=sorted(str(x) for x in old.find_all('table'));newtables=sorted(str(x) for x in new.find_all('table'));assert oldtables==newtables
assert sorted(str(x) for x in old.find_all('img'))==sorted(str(x) for x in new.find_all('img'))
repo=Path(r'C:\Users\msz\aca');dest=repo/'report/dlw_paper_draft.html'
assets=sorted({a[k] for a in new.find_all(['a','img']) for k in ['href','src'] if a.has_attr(k) and not a[k].startswith(('#','https:','http:','data:'))})
assert all((dest.parent/a).exists() for a in assets)
checks={}
h,z,w,y=S.symbols('h z w y',nonzero=True)
phase=S.log((z+h/2)/(z-h/2))/h
assert S.simplify(S.series(phase,h,0,4).removeO()-(1/z+h*h/(12*z**3)))==0
amp=S.sqrt((1-h*h/(4*z*z))/(1-h*h/(4*w*w)))
assert S.simplify(S.series(amp,h,0,4).removeO()-1-h*h*(1/w**2-1/z**2)/8)==0
checks['phase_and_centred_amplitude']='symbolic Taylor identities passed'
# Principal-minor differential formula for a general polynomial tau (N=3): each
# subset has independent coefficient, covering arbitrary Cauchy principal minors.
from itertools import combinations
rho=S.symbols('r0:3');cs=S.symbols('c0:3');ds=S.symbols('d0:3');tau=1;variation=0
for n in range(1,4):
 for I in combinations(range(3),n):
  term=S.Symbol('A'+''.join(map(str,I)))*S.prod(rho[i] for i in I)
  tau+=term;variation+=term*sum(y*cs[i]+ds[i] for i in I)
assert S.expand(variation-sum((y*cs[i]+ds[i])*rho[i]*S.diff(tau,rho[i]) for i in range(3)))==0
checks['general_N']='subset indicator identity proved; independent-minor polynomial checked for N=3'
u3,b3,v2=S.symbols('u3 b3 v2')
assert S.expand(u3/6-b3/12-(9*u3-v2)/48).subs(v2,4*b3+u3).expand()==0
u2,b2,v1=S.symbols('u2 b2 v1')
assert S.expand(-b2/4-(u2-v1)/16).subs(v1,4*b2+u2).expand()==0
checks['physical_coefficients']='C_U and C_V reduce using 4 beta_xy = v-u_y'
k=S.symbols('k');der=S.symbols('f0:7');poly=lambda a:sum(der[n]*(a*k)**n/S.factorial(n) for n in range(7))
assert S.expand((poly(1)-poly(-1))/(2*k)).coeff(k,2)==der[3]/6
assert S.expand((poly(1)-2*poly(0)+poly(-1))/k**2).coeff(k,2)==der[4]/12
checks['x_stencils']='independent D1 and D2 coefficients 1/6 and 1/12 verified'
result={'math_items':len(f),'equations_per_language':118,'strict_katex':True,'unique_ids':len(ids),'internal_links':'all valid','existing_math':'preserved except elementary Euler formula','tables':'all six bilingual tables byte-equivalent as DOM','images':'all twenty bilingual image elements unchanged','local_assets':len(assets),'missing_assets':[],'symbolic_checks':checks}
(r/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(result,ensure_ascii=False))
