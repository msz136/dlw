# -*- coding: utf-8 -*-
"""GSG 半离散化 Thm 2 / Thm 3 的逐项数值复核 (只读探针).

论文: Feng-Sheng-Yu, Numer. Algorithms 94 (2023) 351-370, 式 (3.27)-(3.48).

用论文 (3.6)-(3.7) 的 N=1 tau 函数 + 2-约化 (q=-p, eta0-xi0=i*pi/2+chi),
并按物理规范 fbar=conj(f), gbar=conj(g) (即 tau_n -> tau_n/p^n, 只差常数相位),
用 arctan2 取连续分支避免 log 分支跳变, 直接检验:

  (3.27)  a sin((phi_{k+1}+phi_k)/2) = sin(p_k/2)
  (3.38)  sin^2(p_k/2) + deltaI_k^2/4 = a^2
  (3.31)  d p_k/dtau      = Delta_k sin((u_{k+1}+u_k)/2)
  (3.32)  d deltaI/dtau   = cos(p_k/2)(cos u_{k+1} - cos u_k)
  (3.48)  d deltaIII/dtau = (cos u_{k+1} - cos u_k)

其中 deltaI_k  = 2a cos((phi_{k+1}+phi_k)/2)         (论文 (3.33), 即 Delta_k)
      deltaIII_k = x_{k+1} - x_k,  x_k = 2ka+tau+ln(|g_k|^2/|f_k|^2)  (论文 (3.42))

运行: python -u gsg_semidiscrete_variants_check.py
"""
import mpmath as mp

mp.mp.dps = 40
PI = mp.pi


def make(a, p, chi, xi0, tau):
    """返回 u, phi, x 三个 k -> 实数的函数 (连续分支)."""
    a, p, chi, xi0, tau = map(mp.mpf, (a, p, chi, xi0, tau))

    def ab(k):
        """f_k 的实部/虚部: f_k = e^xi * (A + i B)."""
        xi = tau / (2 * p) + xi0
        A = (1 - a * p) ** (-k) * mp.e ** xi
        B = mp.e ** (chi - tau / p) * (1 + a * p) ** (-k) * mp.e ** xi
        return A, B

    def arg_f(k):
        A, B = ab(k)
        return mp.atan2(B, A)

    def arg_g(k):
        A, B = ab(k)
        return mp.atan2((1 + p) * B, (1 - p) * A)

    def mod_f(k):
        A, B = ab(k)
        return mp.sqrt(A ** 2 + B ** 2)

    def mod_g(k):
        A, B = ab(k)
        return mp.sqrt(((1 - p) * A) ** 2 + ((1 + p) * B) ** 2)

    u = lambda k: 2 * (arg_f(k) + arg_g(k))          # = i ln(Fbar/F)
    phi = lambda k: 2 * (arg_g(k) - arg_f(k))        # = i ln(fbar g/(f gbar))
    x = lambda k: 2 * k * a + tau + 2 * mp.log(mod_g(k) / mod_f(k))
    return u, phi, x


def probe(a, p, tau='0.5', chi='0.3', xi0='0', ks=(0, 1, 2, 3)):
    a, p, tau = mp.mpf(a), mp.mpf(p), mp.mpf(tau)
    h = mp.mpf('1e-8')
    u, phi, x = make(a, p, chi, xi0, tau)
    up, phip, xp = make(a, p, chi, xi0, tau + h)
    um, phim, xm = make(a, p, chi, xi0, tau - h)

    print(f"a={mp.nstr(a,5)}  p={mp.nstr(p,5)}  tau={mp.nstr(tau,5)}")
    print(f"{'k':>2} {'p_k':>10} {'deltaI':>10} {'deltaIII':>10} "
          f"{'I-III':>9} {'(3.27)':>9} {'(3.38)':>9} {'(3.31)':>9} "
          f"{'(3.32)':>9} {'(3.48)':>9}")
    for k in ks:
        pk = u(k + 1) - u(k)
        th = (phi(k + 1) + phi(k)) / 2
        dI = 2 * a * mp.cos(th)
        Dk = mp.sqrt(4 * a ** 2 - 4 * mp.sin(pk / 2) ** 2)
        dIII = x(k + 1) - x(k)
        ubar = (u(k + 1) + u(k)) / 2
        dpk = ((up(k + 1) - up(k)) - (um(k + 1) - um(k))) / (2 * h)
        dphik = ((phip(k + 1) + phip(k)) - (phim(k + 1) + phim(k))) / (2 * h)
        ddeltaI = -a * mp.sin(th) * dphik
        dIII_dt = ((xp(k + 1) - xp(k)) - (xm(k + 1) - xm(k))) / (2 * h)
        cosdiff = mp.cos(u(k + 1)) - mp.cos(u(k))
        r327 = a * mp.sin(th) - mp.sin(pk / 2)
        r338 = mp.sin(pk / 2) ** 2 + dI ** 2 / 4 - a ** 2
        r331 = dpk - Dk * mp.sin(ubar)
        r332 = ddeltaI - mp.cos(pk / 2) * cosdiff
        r348 = dIII_dt - cosdiff
        print(f"{k:>2} {mp.nstr(pk,7):>10} {mp.nstr(dI,7):>10} {mp.nstr(dIII,7):>10} "
              f"{mp.nstr(dI - dIII,3):>9} {mp.nstr(abs(r327),3):>9} {mp.nstr(abs(r338),3):>9} "
              f"{mp.nstr(abs(r331),3):>9} {mp.nstr(abs(r332),3):>9} {mp.nstr(abs(r348),3):>9}")
    print()


if __name__ == '__main__':
    for a in ('0.2', '0.05'):
        for p in ('0.9', '0.5', '2.0'):
            probe(a, p)
