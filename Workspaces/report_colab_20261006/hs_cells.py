# %% [markdown]
# 检查计算所需的数学函数和双精度数组。

# %% hs-prepare
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 计算使用 IEEE 754 双精度。
np.set_printoptions(precision=12)
pd.set_option("display.precision", 12)

# %% [markdown]
# 设置网格、RK4 时间步长和误差评价点。

# %% hs-config
# 式（24）：p=5、q=1.25、c=1，初相位为零。
# 加密同一辅助区间时，同时增大 N、减小 a。
hs_cfg = dict(
    N=1600, a=0.005, Xleft=-4.0,
    dt=0.003125, T=0.5,
    xMin=-1.0, xMax=1.0, evaluationPoints=32001,
)
hs_N, hs_a, hs_Xleft = (hs_cfg[k] for k in ("N", "a", "Xleft"))
hs_dt, hs_T = (hs_cfg[k] for k in ("dt", "T"))
hs_xmin, hs_xmax, hs_neval = (hs_cfg[k] for k in ("xMin", "xMax", "evaluationPoints"))
if not np.isfinite([hs_a, hs_Xleft, hs_dt, hs_T, hs_xmin, hs_xmax]).all():
    raise ValueError("网格、时间和评价区间须取有限实数。")
if not (hs_a > 0 and hs_dt > 0 and hs_T >= 0 and hs_xmax > hs_xmin):
    raise ValueError("要求 a>0、dt>0、T≥0、xMax>xMin。")
if not isinstance(hs_N, int) or not 20 <= hs_N <= 6400:
    raise ValueError("N 应为 20—6400 的整数。")
if not isinstance(hs_neval, int) or not 101 <= hs_neval <= 64001:
    raise ValueError("评价点数应为 101—64001 的整数。")
hs_steps = round(hs_T / hs_dt)
if abs(hs_steps * hs_dt - hs_T) > 1e-12 or hs_steps > 3200:
    raise ValueError("T 须为 dt 的整数倍，且步数≤3200。")
hs_Xright = hs_Xleft + hs_N * hs_a
print(pd.DataFrame([{
    "N": hs_N, "a": hs_a, "X 左端": hs_Xleft, "X 右端": hs_Xright,
    "dt": hs_dt, "T": hs_T, "时间步数": hs_steps, "评价点数": hs_neval,
}]).to_string(index=False))

# %% [markdown]
# 定义单孤子解析解，并构造初始物理网格。

# %% hs-reference
def hs_exact_X(X, t):
    """式（24）的解析场；X 可以是标量或数组。"""
    X = np.asarray(X, dtype=float)
    z = np.tanh((3.75 * X - 0.6 * t) / 2)
    S = 1 - z * z
    zX = 1.875 * S
    zXX = -2 * zX * 1.875 * z
    J, JX = 1 + 0.3 * zX, 0.3 * zXX
    u, uX = 0.09 * S, -0.18 * z * zX
    uXX = -0.18 * (zX * zX + z * zXX)
    # 链式法则：d/dx=(1/J)d/dX，其中 J=dx/dX。
    uxx = (uXX * J - uX * JX) / (J * J * J)
    return dict(x=X - 0.5 + 0.3 * z, u=u, rho=1 / J, m=uxx + 2, X=X)

def hs_exact_physical(x, t):
    """利用 dx/dX>0，在 [x+0.2,x+0.8] 中二分反解 X。"""
    x = np.asarray(x, dtype=float)
    lo, hi = x + 0.2, x + 0.8
    for _ in range(60):
        mid = (lo + hi) / 2
        lower = hs_exact_X(mid, t)["x"] < x
        lo, hi = np.where(lower, mid, lo), np.where(lower, hi, mid)
    value = hs_exact_X((lo + hi) / 2, t)
    if np.max(np.abs(value["x"] - x)) > 2e-12:
        raise ArithmeticError("物理坐标反解未达到容差。")
    return value

hs_initial = hs_exact_X(hs_Xleft + np.arange(hs_N + 1) * hs_a, 0)
hs_left, hs_right = hs_initial["x"][[0, -1]]
hs_dx = (hs_right - hs_left) / hs_N
# 固定网格与初始动网格共用物理端点。
hs_fixed_x = hs_left + np.arange(hs_N + 1) * hs_dx
if hs_xmin <= hs_left or hs_xmax >= hs_right:
    raise ValueError("评价区间必须位于初始物理端点内部。")
print(pd.DataFrame([{
    "初始物理左端": hs_left, "初始物理右端": hs_right,
    "FD 的 dx": hs_dx, "峰值 u": 0.09, "谷值 rho": 0.64,
}]).to_string(index=False))

# %% [markdown]
# 定义两种空间格式，并由三对角方程从 m 恢复 u。

# %% hs-spatial
def hs_integrable_fields(t, state):
    # 状态：[b_0,...,b_(N-1), d_0,...,d_(N-1), x_0]。
    b, d = state[:hs_N], state[hs_N:2 * hs_N]
    if not np.isfinite(state).all() or np.any(d <= 0):
        raise ArithmeticError("Integrable 出现非有限状态或非正胞元格距。")
    u0 = hs_exact_X(hs_Xleft, t)["u"]
    u = np.r_[u0, u0 + np.cumsum(b)]
    x = np.r_[state[-1], state[-1] + np.cumsum(d)]
    return dict(x=x, u=u, rhoX=(x[:-1] + x[1:]) / 2, rho=hs_a / d)

def hs_integrable_rhs(t, state):
    # 式（25）：b、d 和 x_0 的时间导数。
    u = hs_integrable_fields(t, state)["u"]
    b, d = state[:hs_N], state[hs_N:2 * hs_N]
    C = d * d - hs_a * (hs_a - 1)
    db = 2 * d * (u[1:] + u[:-1]) + (C * C - b * b) / (2 * d) - d / 2
    return np.r_[db, -b, -u[0]]

def hs_recover_u(m, ub_left, ub_right):
    # Thomas 消元：u_(i-1)-2u_i+u_(i+1)=dx^2*(m_i-2)。
    count = hs_N - 1
    c, d = np.zeros(count), np.zeros(count)
    for j in range(count):
        diagonal = -2 - (c[j - 1] if j else 0)
        rhs = hs_dx * hs_dx * (m[j + 1] - 2)
        if j == 0:
            rhs -= ub_left
        if j == count - 1:
            rhs -= ub_right
        c[j] = 1 / diagonal if j < count - 1 else 0
        d[j] = (rhs - (d[j - 1] if j else 0)) / diagonal
    u = np.empty(hs_N + 1)
    u[0], u[-1] = ub_left, ub_right
    for j in range(count - 1, -1, -1):
        u[j + 1] = d[j] - (c[j] * u[j + 2] if j < count - 1 else 0)
    return u

def hs_fd_fields(t, state):
    # FD 状态为内部 m 与 rho，端点取解析边界。
    boundary = hs_exact_physical(np.array([hs_left, hs_right]), t)
    m = np.r_[boundary["m"][0], state[:hs_N - 1], boundary["m"][1]]
    rho = np.r_[boundary["rho"][0], state[hs_N - 1:], boundary["rho"][1]]
    if not np.isfinite(m).all() or not np.isfinite(rho).all() or np.any(rho <= 0):
        raise ArithmeticError("FD 出现非有限状态或非正密度。")
    u = hs_recover_u(m, *boundary["u"])
    return dict(x=hs_fixed_x, u=u, rhoX=hs_fixed_x, rho=rho, m=m)

def hs_fd_rhs(t, state):
    # 式（28）：固定网格上的一阶中心差分。
    fields = hs_fd_fields(t, state)
    m, rho, u = (fields[k] for k in ("m", "rho", "u"))
    ux = (u[2:] - u[:-2]) / (2 * hs_dx)
    mx = (m[2:] - m[:-2]) / (2 * hs_dx)
    rx = (rho[2:] - rho[:-2]) / (2 * hs_dx)
    return np.r_[u[1:-1] * mx + 2 * m[1:-1] * ux + rho[1:-1] * rx,
                 u[1:-1] * rx + rho[1:-1] * ux]

def hs_initial_states():
    # 初始 m 使用与演化一致的二阶差分模板。
    fields = hs_exact_physical(hs_fixed_x, 0)
    u0 = fields["u"]
    integrable = np.r_[np.diff(hs_initial["u"]), np.diff(hs_initial["x"]), hs_left]
    m0 = (u0[2:] - 2 * u0[1:-1] + u0[:-2]) / (hs_dx * hs_dx) + 2
    fd = np.r_[m0, fields["rho"][1:-1]]
    return integrable, fd

def hs_interpolate(xs, values, targets):
    # 物理节点上的分段线性重构。
    if targets[0] < xs[0] or targets[-1] > xs[-1]:
        raise ValueError("数值网格未覆盖整个评价区间。")
    # side='left' 与原报告在恰好落于节点时采用相同的左区间。
    j = np.clip(np.searchsorted(xs, targets, side="left") - 1, 0, len(xs) - 2)
    weight = (targets - xs[j]) / (xs[j + 1] - xs[j])
    return values[j] + weight * (values[j + 1] - values[j])

# %% [markdown]
# 定义一次 RK4 更新，依次计算空间方程的四个阶段。

# %% hs-rk4
def hs_rk4_step(rhs, t, state, delta):
    # 式（29）：每一级重新恢复场值和解析边界。
    k1 = rhs(t, state)
    k2 = rhs(t + delta / 2, state + delta / 2 * k1)
    k3 = rhs(t + delta / 2, state + delta / 2 * k2)
    k4 = rhs(t + delta, state + delta * k3)
    return state + delta * (k1 + 2 * k2 + 2 * k3 + k4) / 6

# %% [markdown]
# 从解析初值出发，将两种方案推进至 T。

# %% hs-evolve
hs_integrable, hs_fd = hs_initial_states()
# 时间层 t_n=n*dt；再次执行本单元会从当前配置的初值开始。
for hs_step in range(hs_steps):
    hs_t = hs_step * hs_dt
    hs_integrable = hs_rk4_step(hs_integrable_rhs, hs_t, hs_integrable, hs_dt)
    hs_fd = hs_rk4_step(hs_fd_rhs, hs_t, hs_fd, hs_dt)
hs_live_fields = {
    "Integrable": hs_integrable_fields(hs_T, hs_integrable),
    "FD": hs_fd_fields(hs_T, hs_fd),
}
print(pd.DataFrame([
    {"方案": name, "已推进步数": hs_steps, "当前时间": hs_T, "物理节点数": len(f["x"])}
    for name, f in hs_live_fields.items()
]).to_string(index=False))

# %% [markdown]
# 将重构场与解析解比较，计算并绘制误差。

# %% hs-error
# 式（30）：公共物理网格上的最大绝对误差。
hs_xx = hs_xmin + (hs_xmax - hs_xmin) * np.arange(hs_neval) / (hs_neval - 1)
hs_reference = hs_exact_physical(hs_xx, hs_T)
hs_results, hs_result_rows = {}, []
for hs_name, hs_fields in hs_live_fields.items():
    hs_u = hs_interpolate(hs_fields["x"], hs_fields["u"], hs_xx)
    hs_rho = hs_interpolate(hs_fields["rhoX"], hs_fields["rho"], hs_xx)
    hs_eu = np.abs(hs_u - hs_reference["u"])
    hs_er = np.abs(hs_rho - hs_reference["rho"])
    hs_r = dict(Eu=hs_eu.max(), Erho=hs_er.max(), eu=hs_eu, er=hs_er,
                u=hs_u, rho=hs_rho, minDx=np.diff(hs_fields["x"]).min(),
                minRho=hs_fields["rho"].min())
    hs_results[hs_name] = hs_r
    hs_result_rows.append({"方案": hs_name, "E_u(T)": hs_r["Eu"],
                           "E_rho(T)": hs_r["Erho"], "终点最小格距": hs_r["minDx"],
                           "终点最小密度": hs_r["minRho"]})
print(pd.DataFrame(hs_result_rows).to_string(index=False))

# 每个绘图区间保留其评价点上的最大误差。
hs_bins = 100
hs_centers = hs_xmin + (np.arange(hs_bins) + 0.5) * (hs_xmax - hs_xmin) / hs_bins
hs_bin_index = np.minimum(hs_bins - 1, np.floor(
    (hs_xx - hs_xmin) / (hs_xmax - hs_xmin) * hs_bins).astype(int))
for hs_key, hs_label in (("eu", "u"), ("er", r"\rho")):
    fig, ax = plt.subplots(figsize=(8, 3.5))
    for hs_name, hs_style in (("Integrable", "-"), ("FD", "--")):
        hs_envelope = np.zeros(hs_bins)
        np.maximum.at(hs_envelope, hs_bin_index, hs_results[hs_name][hs_key])
        # 对数图的显示下限为 1e-16；误差范数不截断。
        ax.plot(hs_centers, np.log10(np.maximum(hs_envelope, 1e-16)),
                hs_style, label=hs_name)
    ax.set(xlabel=r"Physical coordinate $x$",
           ylabel=rf"$\log_{{10}}\max|{hs_label}_h-{hs_label}|$")
    ax.legend()
    ax.grid(alpha=0.25)
    fig.tight_layout()
    plt.show()

# 仅原配置与原表核对；输出差值，不添加每段完成标记。
hs_is_default = hs_cfg == dict(N=1600, a=0.005, Xleft=-4.0, dt=0.003125,
                              T=0.5, xMin=-1.0, xMax=1.0, evaluationPoints=32001)
if hs_is_default:
    hs_saved = {"Integrable": (0.010012749796509766, 0.0011496748742060303),
                "FD": (9.399310918062342e-7, 3.046420677166317e-6)}
    hs_audit_rows = []
    for hs_name, (hs_expected_u, hs_expected_rho) in hs_saved.items():
        hs_r = hs_results[hs_name]
        hs_audit_rows.append({
            "方案": hs_name, "原表 E_u": hs_expected_u, "原表 E_rho": hs_expected_rho,
            "E_u 与原表之差": abs(hs_r["Eu"] - hs_expected_u),
            "E_rho 与原表之差": abs(hs_r["Erho"] - hs_expected_rho),
        })
    print(pd.DataFrame(hs_audit_rows).to_string(index=False))
    if max(max(row["E_u 与原表之差"], row["E_rho 与原表之差"]) for row in hs_audit_rows) > 1e-8:
        raise ArithmeticError("默认配置与原报告误差不吻合，请检查已编辑的核心代码。")
