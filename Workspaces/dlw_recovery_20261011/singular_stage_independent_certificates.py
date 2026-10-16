"""New operator certificate: the secondary bracket drops to order one at q=0.

This does not rerun singular_zero_flux_certificates.py. It treats the
Euler-gradient vectors as independent jets and verifies the composition
A_chi J A_chi^* before substituting the DLW gradient expressions.
"""
from pathlib import Path
import hashlib
import json
import sympy as sp

records=[]
for n in range(1,6):
    jets={}
    vectors={}
    for name in ('u','v','s','t'):
        rows=[]
        for r in range(4):
            rows.append(sp.Matrix(sp.symbols(f'{name}{r}_0:{n}')))
        for r in range(3):
            jets.update(zip(rows[r],rows[r+1]))
        vectors[name]=rows
    gs=sp.symbols('g0:5')
    jets.update(zip(gs[:-1],gs[1:]))
    def D(a):
        return sp.expand(sum(sp.diff(a,x)*dx for x,dx in jets.items()))
    def VD(a):
        return a.applyfunc(D)
    def dot(a,b):
        return sum(a[i]*b[i] for i in range(n))/n
    U,UX=vectors['u'][:2]
    V,VX=vectors['v'][:2]
    s,sx=vectors['s'][:2]
    t,tx=vectors['t'][:2]
    q=dot(s,t)
    # A_chi^* g = (-2 g U+s g_x,-2 g V-t g_x).
    gradp=-2*gs[0]*U+gs[1]*s
    grads=-2*gs[0]*V-gs[1]*t
    Jp=-VD(grads)
    Js=-VD(gradp)
    composed=-2*dot(U,Jp)-2*dot(V,Js)-D(dot(s,Jp)-dot(t,Js))
    a=-8*dot(U,V)-4*(dot(s,VX)-dot(t,UX))-D(D(q))
    expected=-2*q*gs[3]-3*D(q)*gs[2]+a*gs[1]+(D(a)+D(D(D(q))))*gs[0]/2
    assert sp.expand(composed-expected)==0
    for r in range(4):
        assert sp.expand(sp.diff(composed,gs[r])-sp.diff(expected,gs[r]))==0
    records.append({'dimension':n,'secondary_operator_identity':True,'coefficient_checks':4})

out={'status':'all new independent operator checks passed',
     'sympy':sp.__version__,'checks':records,'assert_count':25,
     'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
     'scope':'Abstract Euler-gradient composition; all-M proof and the DLW substitution are in singular_branch_independent_audit.md. No nonlinear flow claim.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(out['status'])
