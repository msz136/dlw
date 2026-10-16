"""Original-time normalization algebra; analytic spectral statements are not tested."""
import json
from pathlib import Path
import sympy as s
B,c,h=s.symbols('B c h',nonzero=True)
checks={}
for M in (2,3,4):
    pp=list(s.symbols(f'p0:{M-1}')); ss=list(s.symbols(f's0:{M-1}'))
    pp.append(-sum(pp));ss.append(-sum(ss))
    cross=sum(p*v for p,v in zip(pp,ss))
    u0=[p-cross/(M*c) for p in pp];w=[c+v for v in ss]
    delta=h*sum(2*B*u*v+2*B**2*v-2*B*c*u-4*B**2*c for u,v in zip(u0,w))
    checks[f'physical_B_split_M{M}']=s.expand(delta-2*B*h*cross+2*B**2*c*M*h)==0
q,p,d,a0,a1,k,t=s.symbols('q p d a0 a1 k t',nonzero=True)
H=a0*q*p+a1*(q*p)**2
frequency=d*(a0+2*a1*q*p)
checks['original_weighted_Hamilton_frequency']=s.simplify(d*s.diff(H,p)-frequency*q)==0 and s.simplify(-d*s.diff(H,q)+frequency*p)==0
phase=(frequency-2*s.I*k*B)*t
checks['opposite_phases_preserve_action']=s.simplify((q*s.exp(phase))*(p*s.exp(-phase))-q*p)==0
assert all(checks.values()),checks
out={'scope':'Finite exact algebra only: physical B split and original weighted Hamilton sign; not analytic action descent, all-mode completeness, or infinite time existence.', 'checks':checks,'passed':len(checks)}
Path(__file__).with_name('original_time_validation.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out))
