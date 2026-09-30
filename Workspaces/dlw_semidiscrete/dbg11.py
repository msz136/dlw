# -*- coding: utf-8 -*-
"""dbg11.py -- 用 engine2 在显式数值点上核对 (7)_h 与 (6)_h。"""
import sympy as sp
from engine2 import Model, eadd, escale, emul

H = sp.Rational(1, 4)
for (N, av, pv, qv) in [(1, sp.Integer(4), [sp.Rational(2, 3)], [sp.Rational(-18, 5)]),
                        (1, sp.Integer(-2), [sp.Integer(1)], [sp.Integer(-2)]),
                        (1, sp.Rational(5, 3), [sp.Rational(1, 5)], [sp.Integer(-1)]),
                        (2, sp.Integer(1), [sp.Rational(13, 5), sp.Rational(4, 3)],
                         [sp.Integer(-12), sp.Integer(-15)])]:
    m = Model(N, h=H)
    pt = {m.a: av}
    for i, v in enumerate(pv):
        pt[m.p[i]] = v
    for k, v in enumerate(qv):
        pt[m.q[k]] = v
    m.subs_point(pt)
    d = m.h / 2

    def scal(dd):
        return sp.nsimplify(sp.simplify(list(dd.values())[0])) if len(dd) == 1 else \
            (sp.Integer(0) if len(dd) == 0 else ('MULTI:' + str(len(dd))))

    for j in (0, 1, 2):
        r7 = m.B(m.tau(1, j=j, s=m.a - d, mu=m.a), m.tau(0, j=j, mu=m.a), s=m.a - d)
        r6 = m.B(m.tau(1, j=j, s=m.a - d, mu=m.a), m.tau(0, j=j + 1, mu=m.a), s=m.a + d)
        print("N=%d a=%-6s p=%-14s q=%-14s j=%d : (7)_h=%s   (6)_h=%s"
              % (N, av, pv, qv, j, scal(r7), scal(r6)))
    print()
