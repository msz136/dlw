# -*- coding: utf-8 -*-
"""
audit_tau.py -- 用 sympy 独立复核：给定 tau 是否真的满足双线性方程 (7)_h。

不预设任何结论。取
    F = 1 + cF * exp(kF . z) ,   G = 1 + cG * exp(kG . z)
按 jet4 的构造取 (cF,kF)、(cG,kG)，直接算 B_s(F,G) = (D_x^2 + D_t + 2s D_x)F.G，
把结果化到公共基 {1, e^{kF.z}, e^{kG.z}, e^{(kF+kG).z}} 上并读系数。
"""
import sympy as sp

x, t, y = sp.symbols('x t y', real=True)

# 参数（与 nlfinal.py 第一个算例一致）
a = sp.Rational(4)
pp = sp.Rational(2, 3)
qq = sp.Rational(-18, 5)
h = sp.Rational(1, 4)
d = h / 2
s = a - d                      # 7)_h 用 a-d
n = 1

# ---- jet4/jet3 的构造 ----
P = pp - s
Q = qq + s
cF = (-P / Q) ** n / (pp + qq)
SF = pp + qq
RF = qq ** 2 - pp ** 2
TF = 1 / P + 1 / Q

Pa = pp - a
Qa = qq + a
cG = (-Pa / Qa) ** n / (pp + qq)
SG = pp + qq
RG = qq ** 2 - pp ** 2
TG = 1 / Pa + 1 / Qa

print("F 的键 (SF,RF,TF) =", SF, RF, TF)
print("G 的键 (SG,RG,TG) =", SG, RG, TG, "  系数 cF,cG =", cF, cG)
print("两键之差        =", sp.simplify(SF - SG), sp.simplify(RF - RG),
      sp.simplify(TF - TG))
print()

EF = sp.exp(SF * x + RF * t + TF * y)
EG = sp.exp(SG * x + RG * t + TG * y)
F = 1 + cF * EF
G = 1 + cG * EG


def bilin(F, G, mx=0, mt=0):
    tot = 0
    for i in range(mx + 1):
        for j in range(mt + 1):
            tot += (-1) ** (i + j) * sp.binomial(mx, i) * sp.binomial(mt, j) \
                * sp.diff(F, x, mx - i, t, mt - j) * sp.diff(G, x, i, t, j)
    return tot


res = sp.expand(bilin(F, G, 2, 0) + bilin(F, G, 0, 1) + 2 * s * bilin(F, G, 1, 0))
# 把 e^{kF.z} 与 e^{kG.z} 视为独立符号（只在 kF == kG 时才等价）
EFs, EGs = sp.symbols('EF EG', positive=True)
res2 = res.subs({EF: EFs, EG: EGs,
                 sp.exp(2 * (SF * x + RF * t + TF * y)): EFs ** 2,
                 sp.exp(2 * (SG * x + RG * t + TG * y)): EGs ** 2,
                 sp.exp((SF + SG) * x + (RF + RG) * t + (TF + TG) * y): EFs * EGs})
res3 = sp.expand(res2)
print("B_s(F,G) 化到基 {1, EF, EG, EF*EG}:")
for mon in [1, EFs, EGs, EFs * EGs]:
    co = sp.simplify(res3.coeff(mon) if mon != 1 else res3.subs({EFs: 0, EGs: 0}))
    # 更稳妥：逐项取系数
    print("   coeff(", mon, ") =", sp.nsimplify(co))
print()
print("结论：B_s(F,G) 是否恒等于 0 ？",
      sp.simplify(res3) == 0)
print("残余（未化简）:", sp.simplify(res3))
