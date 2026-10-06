# %% error-prepare
# 载入 NumPy、pandas 与 Matplotlib，准备双精度残差计算。
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from types import SimpleNamespace
try:
    from IPython.display import display
except ModuleNotFoundError:
    display = print  # 普通 Python 脚本使用文本表；Colab 使用原生表格输出。

# NumPy 使用 IEEE 754 双精度；各段结果保存在 dlw 中。
dlw = SimpleNamespace(ready={"prepare"})

def dlw_require(stage, message):
    if stage not in dlw.ready:
        raise RuntimeError(message)


# %% error-config
# 设置孤子参数、纵向格距 h 和相位采样点。
dlw_require("prepare", "先运行准备环境。")
dlw.ready = {"prepare"}
# 孤子参数 (a,p,q)：A=(2,1,2)，B=(2,4,-3)。
# h：y 方向格距；z：无量纲相位；x、t 导数保持解析。
dlw_cfg = dict(a=2, p=1, q=2, h=1/8,
               zMin=-10, zMax=10, points=1601, levels=3)
a, p, q, h, zMin, zMax = (dlw_cfg[k] for k in
                          ("a", "p", "q", "h", "zMin", "zMax"))
points, levels = dlw_cfg["points"], dlw_cfg["levels"]
if not np.isfinite([a, p, q, h, zMin, zMax]).all():
    raise ValueError("参数必须是有限实数。")
if not (h > 0 and zMax > zMin and zMax-zMin <= 100):
    raise ValueError("要求 h>0、zMax>zMin，且相位区间宽度≤100。")
if (not isinstance(points, int) or not 41 <= points <= 10001 or
        not isinstance(levels, int) or not 1 <= levels <= 6):
    raise ValueError("points 应在 41—10001；levels 应在 1—6，均取整数。")
if h / 2**(levels-1) < 1/1024:
    raise ValueError("最细格距须≥1/1024，以限制浮点消减误差。")
K, P, Q = p+q, p-a, q+a
if not (K > 0 and P != 0 and Q != 0 and -P/Q > 0):
    raise ValueError("单孤子正分支要求 p+q>0，(p-a)(q+a)<0。")
ell, Gamma, Omega = 1/P + 1/Q, -P/Q, q*q-p*p
zeta = K*ell
if not np.isfinite([ell, Gamma, Omega, zeta]).all():
    raise ValueError("参数过近谱极点，所得系数非有限。")
dlw.cfg = dlw_cfg.copy()
dlw.a, dlw.K, dlw.ell, dlw.Gamma = a, K, ell, Gamma
dlw.Omega, dlw.zeta, dlw.h, dlw.levels = Omega, zeta, h, levels
dlw.zs = zMin + (zMax-zMin)*np.arange(points, dtype=np.float64)/(points-1)
dlw.ready = {"prepare", "config"}
display(pd.DataFrame([[K, ell, Gamma, zeta, h, points]],
                     columns=["K", "ℓ", "Γ", "ζ = Kℓ", "h", "相位点数"]))


# %% error-profile
# 定义连续单孤子剖面及其对相位的解析导数。
dlw_require("config", "先运行谱参数配置。")
dlw.ready = {"prepare", "config"}
# s^(n)=s(1-s)*P_n(s)，P_(n+1)=(1-2s)P_n+s(1-s)P_n'。
dlw_polys = [np.array([1.0])]
for n in range(1, 5):
    c = dlw_polys[-1]
    dlw_polys.append(np.array([(k+1)*((c[k] if k < len(c) else 0)
                                    -(c[k-1] if k else 0))
                              for k in range(len(c)+1)]))

def dlw_sigmoid_jet(z):
    z = np.asarray(z, dtype=np.float64)
    e = np.exp(-np.abs(z))
    s = np.where(z >= 0, 1/(1+e), e/(1+e))
    theta = e/(1+e)**2
    return np.array([s] + [theta*np.polynomial.polynomial.polyval(s, c)
                          for c in dlw_polys])

def dlw_profile(z):
    s, f = dlw_sigmoid_jet(z), dlw_sigmoid_jet(z+np.log(dlw.Gamma))
    # u[n]、v[n] 表示对 z 的 n 阶导数，支持标量或整列相位。
    return dict(s=s, f=f, u=2*dlw.K*(f[:4]-s[:4]),
                v=2*dlw.K*dlw.ell*(f[1:4]+s[1:4]))

dlw.profile = dlw_profile
dlw.ready = {"prepare", "config", "profile"}


# %% error-coefficient
# 定义二阶残差主系数及全波形上界。
dlw_require("profile", "先运行连续剖面。")
dlw.ready = {"prepare", "config", "profile"}

def dlw_coefficient(z):
    c = dlw.profile(z)
    s, f, zeta = c["s"], c["f"], dlw.zeta
    d1, d2, d3 = f[1]-s[1], f[2]-s[2], f[3]-s[3]
    # B=(s″)²+s′*s‴=0.5*((s′)²)″。
    B = s[2]**2 + s[1]*s[3]
    return {
        "FD": np.array([zeta**3*(f[5]+s[5])/6,
                        zeta**3*(f[5]-s[5])/3]),
        "SD": np.array([zeta**3*((2*s[5]-f[5])/3+B)-zeta**2*s[3],
                        zeta**3*((f[5]+2*s[5])/3+B+2*(d2*d2+d1*d3))
                        -zeta**2*s[3]])
    }

# 解析上界覆盖全部实相位 z，不依赖相位区间与采样点数。
Z = abs(dlw.zeta)
dlw.bounds = {"FD": np.array([Z**3/12, Z**3/6]),
              "SD": np.array([251*Z**3/864+Z**2/8,
                              59*Z**3/96+Z**2/8])}
dlw.coefficient = dlw_coefficient
dlw.ready = {"prepare", "config", "profile", "coefficient"}


# %% error-residual
# 定义有限格距 h 下的 SD 和 FD 方程残差。
dlw_require("coefficient", "先运行二阶主系数。")
dlw.ready = {"prepare", "config", "profile", "coefficient"}

def dlw_residual(z, hh, scheme):
    if scheme not in ("SD", "FD"):
        raise ValueError("scheme 应为 SD 或 FD。")
    z = np.asarray(z, dtype=np.float64)
    a, K, ell, Omega = dlw.a, dlw.K, dlw.ell, dlw.Omega
    cache = {}

    def node(j):
        if j in cache:
            return cache[j]
        c = dlw.profile(z+ell*hh*j)
        plus = dlw.profile(z+ell*hh*(j+1))
        minus = dlw.profile(z+ell*hh*(j-1))
        # 每个偏移节点重新构造 D=δ₀u、W=v−δ₀u。
        D = (plus["u"][:3]-minus["u"][:3])/(2*hh)
        W = c["v"]-D
        u = c["u"]
        Ax = K*(u[0]+2*a)*u[1]
        Hx = Ax + (hh*hh*K*(W[0]/16-1/4)*W[1] if scheme == "SD" else 0)
        out = dict(c, D=D, W=W, Ax=Ax, Hx=Hx)
        cache[j] = out
        return out

    # 第一式在交错中点，第二式在节点 j=0；x、t 导数保持解析。
    plus, minus, c = node(1/2), node(-1/2), node(0)
    r1 = Omega*(plus["u"][1]-minus["u"][1])/hh
    r1 += (plus["Hx"]-minus["Hx"])/hh
    r1 += K*K*((plus["u"][2]-minus["u"][2])/hh
               +(plus["W"][2]+minus["W"][2])/2 if scheme == "SD"
               else (plus["v"][2]+minus["v"][2])/2)
    u, v, W, D = c["u"], c["v"], c["W"], c["D"]
    r2 = Omega*v[1]
    if scheme == "SD":
        pp, mm = node(1), node(-1)
        r2 += ((pp["Hx"]-mm["Hx"])/(2*hh)
               +K*(u[1]*W[0]+(u[0]+2*a)*W[1]-4*u[1])
               +K*K*(D[2]+(pp["W"][2]-2*W[2]+mm["W"][2])/4))
    else:
        r2 += K*(u[1]*v[0]+(u[0]+2*a)*v[1]-4*u[1])+K*K*D[2]
    return np.array([r1, r2])

dlw.residual = dlw_residual
dlw.ready = {"prepare", "config", "profile", "coefficient", "residual"}


# %% error-main
# 计算采样主系数，核对上界并测量连续方程残差。
dlw_require("residual", "先运行有限格距残差。")
dlw.ready = {"prepare", "config", "profile", "coefficient", "residual"}
dlw.tau = dlw.coefficient(dlw.zs)
c = dlw.profile(dlw.zs)
u, v, b = c["u"], c["v"], c["u"][0]+2*dlw.a
K, ell, Omega = dlw.K, dlw.ell, dlw.Omega
terms1 = np.array([ell*Omega*u[2], K*K*v[2],
                   K*ell*(u[1]*u[1]+b*u[2])])
terms2 = np.array([Omega*v[1], K*K*ell*u[3],
                   K*(u[1]*v[0]+b*v[1]-4*u[1])])
# 两条连续方程的归一化残差 abs(sum)/(1+sum(abs))。
dlw.continuumDefect = max(float(np.max(np.abs(terms.sum(axis=0))
                                     /(1+np.abs(terms).sum(axis=0))))
                          for terms in (terms1, terms2))
if dlw.continuumDefect > 1e-10:
    raise ArithmeticError("连续 DLW 方程核对失败，请检查剖面或谱参数。")
dlw.coeffRows = []
for S in ("SD", "FD"):
    for i in range(2):
        sampled = float(np.max(np.abs(dlw.tau[S][i])))
        bound = float(dlw.bounds[S][i])
        if not np.isfinite(sampled) or sampled > bound*(1+1e-10):
            raise ArithmeticError(f"{S} 第 {i+1} 式超出解析主系数上界。")
        dlw.coeffRows.append([f"{S}{' / SDR' if S == 'SD' else ''} · {i+1}",
                              sampled, bound, dlw.h**2*sampled, dlw.h**2*bound])
display(pd.DataFrame(dlw.coeffRows, columns=["方程", "采样 max |τ|", "全波形解析上界",
                                           "采样 h² max |τ|", "h² 解析上界"]))
print("continuumDefect =", dlw.continuumDefect)
dlw.ready = {"prepare", "config", "profile", "coefficient", "residual", "main"}


# %% error-convergence
# 逐次减半格距，比较并绘制缩放残差与主系数。
dlw_require("main", "先运行主系数计算。")
dlw.ready = {"prepare", "config", "profile", "coefficient", "residual", "main"}
# R_h/h²−τ=O(h²)：相邻两档误差之比应趋近 4。
dlw.convergence, dlw.finest, previous = [], {}, {}
for level in range(dlw.levels):
    hh = dlw.h/2**level
    for S in ("SD", "FD"):
        values = dlw.residual(dlw.zs, hh, S)/(hh*hh)
        if not np.isfinite(values).all():
            raise ArithmeticError("有限 h 残差非有限，请检查参数。")
        errors = values-dlw.tau[S]
        for i in range(2):
            err = float(np.max(np.abs(errors[i])))
            old = previous.get((S, i))
            rate = np.log2(old/err) if old is not None and old > 0 and err > 0 else np.nan
            dlw.convergence.append([f"{S} · {i+1}", hh,
                                    float(np.max(np.abs(values[i]))), err, rate])
            previous[S, i] = err
        if level == dlw.levels-1:
            dlw.finest[S] = values
display(pd.DataFrame(dlw.convergence, columns=["方程", "h", "采样 max |R_h / h²|",
                                             "采样 max |R_h / h² − τ|", "减半收敛阶"]))
for i in range(2):
    fig, ax = plt.subplots(figsize=(8, 3.8))
    ax.plot(dlw.zs, dlw.tau["SD"][i], label=r"SD / SDR $\tau$")
    ax.plot(dlw.zs, dlw.tau["FD"][i], label=r"FD $\tau$")
    hh = dlw.h/2**(dlw.levels-1)
    ax.plot(dlw.zs, dlw.finest["SD"][i], "--", label=f"SD h={hh:g}")
    ax.plot(dlw.zs, dlw.finest["FD"][i], "--", label=f"FD h={hh:g}")
    ax.set(title=f"DLW equation {i+1}", xlabel="Phase z", ylabel=r"Residual / $h^2$")
    ax.grid(alpha=.2)
    ax.legend()
    fig.tight_layout()
    plt.show()
dlw.ready = {"prepare", "config", "profile", "coefficient", "residual", "main", "convergence"}

