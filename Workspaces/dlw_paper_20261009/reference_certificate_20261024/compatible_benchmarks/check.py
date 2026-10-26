"""Symbolic reduction and validated initial/boundary recovery checks."""
import json
from pathlib import Path
import sympy as S
from flint import arb
from reference import evaluate, parameters

x,z,t = S.symbols('x z t')
u = S.Function('u')(x,z,t)
v = 4-S.diff(u,z)
ut = S.diff(u,x,2)-(u+4)*S.diff(u,x)
r1 = S.diff(ut,z)+S.diff(v,x,2)+S.diff((u+4)*S.diff(u,z),x)
r2 = -S.diff(ut,z)+S.diff(u,x,2,z)+S.diff((u+4)*v-4*u,x)
assert S.simplify(r1) == 0 and S.simplify(r2) == 0

# q=e^(-mu X/2+mu²t/4) H(X-mu t,t), H_t=H_YY,
# implies q_t=q_XX. The logarithmic derivative gives Burgers.
q = S.Function('q')(x,t)
ub = -2*S.diff(q,x)/q
rb = S.diff(ub,t)-S.diff(ub,x,2)+ub*S.diff(ub,x)
rb = rb.subs(S.diff(q,x,t), S.diff(q,x,3)).subs(S.diff(q,t),S.diff(q,x,2))
assert S.simplify(rb)==0

checks = []
for case in ['sine','gaussian']:
    A,w,C,K,kappa = parameters(case)
    for xs,zs in [('0','1'),('3','2')]:
        r = evaluate(case,xs,zs,'0')
        xx,zz = arb(xs),arb(zs)
        if case=='sine':
            F=(w*xx).cos()
        else:
            F=sum(((-((xx+192*j)/6)**2).exp() for j in [-1,0,1]),arb(0))
            # Missing images for |x|<=3 are far below this enclosure.
            F += arb('0 +/- 1e-1000')
        initial_u=A*(kappa*zz).sin()*F
        initial_v=4-A*kappa*(kappa*zz).cos()*F
        assert arb(r['u']).overlaps(initial_u)
        assert arb(r['v']).overlaps(initial_v)
        checks.append({'case':case,'check':'initial','x':xs,'z':zs,'passed':True})
    for zs in ['0','4']:
        r=evaluate(case,'3',zs,'.01')
        assert arb(r['u']).contains(0)
        checks.append({'case':case,'check':'boundary','z':zs,'passed':True})
out={'DLW_reduction_symbolic':True,'Cole_Hopf_symbolic':True,'checks':checks,
     'meaning':'Checks support the analytic proof, not a formal proof of every step.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
