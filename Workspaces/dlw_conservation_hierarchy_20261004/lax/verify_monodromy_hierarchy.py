"""Formal PDO checks and an exact independence witness for DLW monodromy.

All checks use polynomial/rational algebra, not a fitted wave function.
Normal form: sum coefficient(x) D**power, D = d/dx.
"""
import json
from pathlib import Path
import sympy as s
from functools import lru_cache

OUT = Path(__file__).parent
jets = {}
jet_names = {}

def jet(name, k=0):
    key = (name, k)
    if key not in jets:
        jets[key] = s.Symbol(name if k == 0 else name + '_x' + str(k))
        jet_names[jets[key]] = key
    return jets[key]

@lru_cache(maxsize=20000)
def dx(f, n=1):
    f = s.sympify(f)
    for _ in range(n):
        f = s.expand(sum(s.diff(f, z) * jet(jet_names[z][0], jet_names[z][1]+1)
                         for z in f.free_symbols if z in jet_names))
    return f

def mul(a, b, lo=-10, hi=12):
    out = {}
    for i, ai in a.items():
        for j, bj in b.items():
            for r in range(max(0, i+j-hi), max(-1, i+j-lo)+1):
                c = s.binomial(i, r)
                if c:
                    power = i+j-r
                    out[power] = out.get(power, 0) + c*ai*dx(bj, r)
    return {i: s.expand(v) for i, v in out.items() if v != 0}

def powers(l, count, lo=-10):
    ans, current = [], {0: s.Integer(1)}
    for n in range(1, count+1):
        current = mul(current, l, lo=-(count-n+2))
        ans.append(current)
    return ans

def euler(f, name):
    value = 0
    for (nm, k), z in list(jets.items()):
        if nm == name:
            value += (-1)**k * dx(s.diff(f, z), k)
    return s.expand(value)

def assert_total_dx(expr):
    for name in set(jet_names[z][0] for z in expr.free_symbols if z in jet_names):
        assert euler(expr, name) == 0, (name, euler(expr, name))

def main():
    # A general normalized first-order PDO, sufficient through residue L^5.
    ell = [None] + [jet('ell'+str(k)) for k in range(1, 10)]
    l = {1: s.Integer(1), **{-k: ell[k] for k in range(1, 10)}}
    lp = powers(l, 5, lo=-10)
    print('PDO powers computed', flush=True)
    reps = [ell[1], 2*ell[2], 3*(ell[3]+ell[1]**2),
            4*(ell[4]+3*ell[1]*ell[2]),
            5*(ell[5]+4*ell[1]*ell[3]+2*ell[2]**2+2*ell[1]**3
               +2*ell[1]*dx(ell[2])-dx(ell[1])**2)]
    for op, rho in zip(lp, reps):
        assert_total_dx(op[-1]-rho)
    print('First five reduced densities verified', flush=True)
    # Derive rather than guess a representative for the fifth density.
    rho5 = lp[4][-1]
    # Exact residue-flux identity for M = -D^2-V for all five powers.
    v = jet('V')
    m = {2: -s.Integer(1), 0: -v}
    for op in lp:
        comm = mul(m, op, lo=-3)[-1] - mul(op, m, lo=-3)[-1]
        assert s.expand(comm + dx(dx(op[-1])+2*op[-2])) == 0
    print('Five exact residue flux identities verified', flush=True)
    # First three normalized coefficients from F L = p1 + (p2/p1) F.
    a, b = s.symbols('p1 p2', nonzero=True)
    p = {1: a, 2: b, **{k: jet('p'+str(k)) for k in range(3, 8)}}
    f = {-k: p[k] for k in p}
    coeffs = []
    work = {1: s.Integer(1)}
    for k in range(1, 6):
        target = s.expand(mul(f, work, lo=-k-1).get(-k-1, 0))
        val = s.expand((b/a*p[k+1] - target)/a)
        coeffs.append(val)
        work[-k] = val
        assert s.expand(mul(f, work, lo=-k-1)[-k-1] - b/a*p[k+1]) == 0
    print('First five normalized coefficients verified', flush=True)
    # Field-level p1,p2 and the precise Hamilton duplicate identity.
    gc = s.Symbol('G', nonzero=True)
    gx = [jet('g0'), jet('g1')]
    gx.append(gc-gx[0]-gx[1])
    ux = [jet('U0'),jet('U1'),jet('U2')]
    pm = {0:s.Integer(1)}
    for gj,uj in zip(gx,ux):
        bj = (uj-gj)/2
        sc = {0:s.Integer(1),-1:-gj}
        for n in range(1,3):
            sc[-n-1] = s.expand(bj*sc[-n]-dx(sc[-n]))
        pm = mul(sc,pm,lo=-3)
    tx = sum(uj*gj for uj,gj in zip(ux,gx))
    assert s.expand(pm[-1]+gc) == 0
    assert s.expand(pm[-2]-(gc**2-tx)/2) == 0
    em = s.Matrix([[0,0,1],[1,0,0],[0,1,0]])
    pr = s.eye(3)-s.ones(3)/3
    rh = (s.eye(3)-em+s.ones(3)/3).inv()*(s.eye(3)+em)/2*pr
    h0 = (2*sum(uj**2*gj for uj,gj in zip(ux,gx))
          +s.Rational(2,3)*sum(gj**3 for gj in gx)
          +4*sum(gj*dx(uj) for uj,gj in zip(ux,gx))
          +8*(s.Matrix(gx).T*rh*s.Matrix([dx(gj) for gj in gx]))[0])
    dup = s.expand(pm[-3]+h0/8-gc*tx/2+gc**3/6)
    assert_total_dx(dup)
    print('Field-level mean coefficients and Hamilton duplicate verified', flush=True)
    # Compare rho2 with the independently derived quartic charge on the
    # fixed G,T leaf. The comparison is done at field level modulo D.
    tc = s.Symbol('T')
    px = [jet('r0'),jet('r1')]
    px.append(-px[0]-px[1])
    bu = s.expand((tc-sum(pj*gj for pj,gj in zip(px,gx)))/gc)
    ur = [pj+bu for pj in px]
    pm4 = {0:s.Integer(1)}
    for gj,uj in zip(gx,ur):
        bj = (uj-gj)/2
        sc = {0:s.Integer(1),-1:-gj}
        for n in range(1,4): sc[-n-1] = s.expand(bj*sc[-n]-dx(sc[-n]))
        pm4 = mul(sc,pm4,lo=-4)
    rgx = list(rh*s.Matrix([dx(gj) for gj in gx]))
    h0r = (2*sum(uj**2*gj for uj,gj in zip(ur,gx))
           +s.Rational(2,3)*sum(gj**3 for gj in gx)
           +4*sum(gj*dx(uj) for uj,gj in zip(ur,gx))
           +8*sum(gj*rj for gj,rj in zip(gx,rgx)))
    q4 = sum(s.Rational(4,3)*(uj**3*gj+uj*gj**3)
             +8*uj*gj*dx(uj)-s.Rational(16,3)*dx(uj)*dx(gj)
             +16*uj*gj*rj for uj,gj,rj in zip(ur,gx,rgx))
    comp4 = s.expand(pm4[-4]+s.Rational(3,32)*q4-gc*h0r/8
                     -(tc**2/8-gc**2*tc/4+gc**4/24))
    assert_total_dx(comp4)
    print('rho2 = Q4 plus old Hamilton confirmed modulo D', flush=True)
    # General-N proof primitives: one-site logarithm and pair commutator.
    u,g = jet('oneU'),jet('oneg')
    bb = (u-g)/2
    st = {-1:-g}
    for k in range(1,4): st[-k-1] = s.expand(bb*st[-k]-dx(st[-k]))
    current, logarithm = {0:s.Integer(1)}, {}
    for k in range(1,5):
        current = mul(current,st,lo=-4)
        for power,value in current.items():
            logarithm[power] = logarithm.get(power,0)+(-1)**(k+1)*value/s.Integer(k)
    l3 = -u**2*g/4-g**3/12+u*dx(g)/2
    l4 = -(u**3*g+u*g**3)/8-3*u*g*dx(u)/4+dx(u)*dx(g)/2
    assert_total_dx(s.expand(logarithm[-3]-l3))
    assert_total_dx(s.expand(logarithm[-4]-l4))
    ai,aj,bi,bj = [jet(k) for k in ['ai','aj','bi','bj']]
    oi,oj = {-1:ai,-2:bi},{-1:aj,-2:bj}
    comm4 = mul(oi,oj,lo=-4)[-4]-mul(oj,oi,lo=-4)[-4]
    assert_total_dx(s.expand(comm4-3*(bj*dx(ai)-bi*dx(aj))))
    print('General coefficient proof primitives verified', flush=True)
    r2 = s.expand(2*coeffs[1])
    r3 = s.expand(3*(coeffs[2]+coeffs[0]**2))
    r2rep = 4*b*p[3]/a**2 - 2*p[4]/a - 2*b**3/a**3
    r3rep = 3*(2*b*p[4]/a**2 - p[5]/a + 2*p[3]**2/a**2
               - 5*b**2*p[3]/a**3 + 2*b**4/a**4)
    assert_total_dx(r2-r2rep)
    assert_total_dx(r3-r3rep)
    # Exact constant-x witness on N=3, G=6,T=12.
    # Four leaf coordinates: U0,U1,g0,g1. No x-derivative can hide a relation.
    u0,u1,g0,g1 = s.symbols('U0 U1 g0 g1')
    gs = [g0, g1, 6-g0-g1]
    us = [u0, u1, (12-u0*g0-u1*g1)/gs[2]]
    z = s.Symbol('z')
    # log(P) coefficients a_n = sum(B^n-A^n)/n.
    logc = {n: s.expand(sum((((u-g)/2)**n-((u+g)/2)**n)/n
                           for u,g in zip(us,gs))) for n in range(1,6)}
    pc = {1: -s.Integer(6), 2: s.Integer(12),
          3: logc[3], 4: logc[4]-6*logc[3]-36,
          5: logc[5]-6*logc[4]+12*logc[3]+s.Rational(216,5)}
    sub = {a:pc[1],b:pc[2],p[3]:pc[3],p[4]:pc[4],p[5]:pc[5]}
    funcs = [sum(us), -8*logc[3], r2rep.subs(sub), r3rep.subs(sub)]
    pt = {u0:-2,u1:1,g0:1,g1:2}
    jac = s.Matrix([[s.diff(fn,q).subs(pt) for q in [u0,u1,g0,g1]] for fn in funcs])
    det = s.factor(jac.det())
    assert det != 0
    result = {
      'passed': True,
      'exact_checks': 5+5+5+2+3+1+1+3,
      'rho_exact_first_five': [str(op[-1]) for op in lp],
      'rho_mod_D_first_five': [str(v) for v in reps],
      'rho5_exact': str(rho5),
      'ell_in_p_first_five': [str(v) for v in coeffs],
      'rho2_in_p_mod_D': str(r2rep),
      'rho3_in_p_mod_D': str(r3rep),
      'independence_witness': {'N':3, 'G':6, 'T':12, 'point': {str(k):str(v) for k,v in pt.items()},
                             'Jacobian':str(jac), 'determinant':str(det)},
      'warning': 'Formal periodic monodromy hierarchy. Involution is proved separately in MONODROMY_POISSON_PROOF.md; infinite independence and the nonperiodic relative scattering generator remain unproved.'
    }
    (OUT/'monodromy_hierarchy_checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k in ['passed','exact_checks','independence_witness']},ensure_ascii=False,indent=2))

if __name__ == '__main__':
    main()
