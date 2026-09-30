# -*- coding: utf-8 -*-
"""dbg8.py -- 用 sympy 精确判定 N=1 时单孤子 tau 与 B_lam 的配对条件。"""
import sympy as sp

x, t = sp.symbols('x t', real=True)
pv = sp.Rational(2, 3)
qv = sp.Rational(-18, 5)
av = sp.Integer(4)
dv = sp.Rational(1, 8)

eta = (pv + qv) * x + (qv ** 2 - pv ** 2) * t


def coef(n, ss):
    return (-(pv - ss) / (qv + ss)) ** n / (pv + qv)


def B(F, G, lam):
    return (sp.diff(F, x, 2) * G - 2 * sp.diff(F, x) * sp.diff(G, x) + F * sp.diff(G, x, 2)
            + sp.diff(F, t) * G - F * sp.diff(G, t)
            + 2 * lam * (sp.diff(F, x) * G - F * sp.diff(G, x)))


print("测试：F = tau_1(j=1, s=sF) , G = tau_0 时，B_lam F.G 在哪些 (lam,sF) 上为零？")
print("（在原点 x=t=0 求值，此时 exp(eta)=1）")
res = {}
for lam_name, lam in [('a', av), ('a-d', av - dv), ('a+d', av + dv),
                      ('(a+sf)/2 变体', None)]:
    for sF_name, sF in [('a', av), ('a-d', av - dv), ('a+d', av + dv)]:
        if lam is None:
            lam = (av + sF) / 2
        cF = coef(1, sF)
        cG = coef(0, av)
        F = 1 + cF * sp.exp(eta)
        G = 1 + cG * sp.exp(eta)
        R0 = sp.simplify(B(F, G, lam))
        if R0 == 0:
            R0 = sp.Integer(0)
        res[(lam_name, sF_name)] = R0
        print("  lam=%-10s sF=%-5s : B = %s" % (lam_name, sF_name, sp.nsimplify(R0)))

print("\n试：G = tau_0(j+1)（即 G 也带 chi^{j+1} 因子）时：")
cG1 = coef(0, av) * ((pv - av + dv) / (pv - av - dv)) * ((qv + av + dv) / (qv + av - dv))
F = 1 + coef(1, av - dv) * sp.exp(eta)
for lam_name, lam in [('a-d', av - dv), ('a', av), ('a+d', av + dv)]:
    G = 1 + cG1 * sp.exp(eta)
    print("  lam=%-5s : B = %s" % (lam_name, sp.nsimplify(sp.simplify(B(F, G, lam)))))

print("\n[关键] 该参数下 chi 的值与其分量：")
print("  lam_p =", sp.nsimplify((pv - av + dv) / (pv - av - dv)),
      " lam_q =", sp.nsimplify((qv + av + dv) / (qv + av - dv)))
print("  p+q =", pv + qv, "  (p-a) =", pv - av, " (q+a) =", qv + av)
print("  p-a+d =", sp.nsimplify(pv - av + dv), " p-a-d =", sp.nsimplify(pv - av - dv))
print("  注意 p-a-d = 0 ? ", sp.simplify(pv - av - dv) == 0)
