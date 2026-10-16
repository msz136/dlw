"""Self-contained two-soliton extension to the seven audited HS cells."""
from __future__ import annotations

import nbformat


TWO_REFERENCE = r'''
# 四项 τ 函数的指数系数；q_i=p_i/(p_i-1) 对应 c=1。
hs_two_p = np.array([1.1, 1.25])
hs_two_q = np.array([11.0, 5.0])
hs_two_phase = np.log(6.5)
hs_two_A = 12 / 507
if not np.allclose(hs_two_q, hs_two_p / (hs_two_p - 1)):
    raise ValueError("p、q 必须满足 c=1 的孤子参数约束。")
hs_two_beta = np.r_[0, hs_two_p-hs_two_q, np.sum(hs_two_p-hs_two_q)][:, None]
hs_two_omega = np.r_[0, 1/hs_two_p-1/hs_two_q,
                     np.sum(1/hs_two_p-1/hs_two_q)][:, None]
hs_two_logcoef = np.array([0, hs_two_phase, hs_two_phase,
                          2*hs_two_phase + np.log(hs_two_A)])[:, None]
hs_two_shift = float(np.sum(1/hs_two_q))

def hs_two_exact_X(X, t):
    """u、J=dx/dX 和 m=u_xx+2 均由 τ 的解析导数计算。"""
    X = np.asarray(X, dtype=float)
    flat = X.reshape(-1)
    logs = hs_two_beta*flat + hs_two_omega*t + hs_two_logcoef
    # 减去列最大值避免指数溢出，不改变归一化权重。
    weights = np.exp(logs - np.max(logs, axis=0))
    weights /= np.sum(weights, axis=0)
    mean_o = np.sum(weights*hs_two_omega, axis=0)
    mean_b = np.sum(weights*hs_two_beta, axis=0)
    do, db = hs_two_omega-mean_o, hs_two_beta-mean_b
    u = np.sum(weights*do**2, axis=0)
    cov = np.sum(weights*do*db, axis=0)
    J = 1-cov
    JX = -np.sum(weights*do*db**2, axis=0)
    uX = np.sum(weights*do**2*db, axis=0)
    uXX = (np.sum(weights*do**2*db**2, axis=0)
           - u*np.sum(weights*db**2, axis=0) - 2*cov**2)
    if not np.isfinite(J).all() or np.any(J <= 0):
        raise ArithmeticError("二孤子物理坐标要求 J=dx/dX>0。")
    uxx = (uXX*J-uX*JX)/J**3
    return {k: value.reshape(X.shape) for k, value in dict(
        x=flat-mean_o-hs_two_shift, u=u, rho=1/J, m=uxx+2,
        X=flat, J=J, uX=uX, uXX=uXX, JX=JX).items()}

def hs_two_exact_physical(x, t):
    """由 τ 权重的凸组合界定 X 的区间，再二分反解。"""
    x = np.asarray(x, dtype=float)
    lo = x + hs_two_shift + float(np.min(hs_two_omega))
    hi = x + hs_two_shift + float(np.max(hs_two_omega))
    for _ in range(60):
        mid = (lo+hi)/2
        lower = hs_two_exact_X(mid, t)["x"] < x
        lo, hi = np.where(lower, mid, lo), np.where(lower, hi, mid)
    value = hs_two_exact_X((lo+hi)/2, t)
    if np.max(np.abs(value["x"]-x)) > 2e-12:
        raise ArithmeticError("二孤子物理坐标反解未达到容差。")
    return value
'''

TWO_INITIAL = r'''
# 仅替换解析初值与边界；空间格式、时间格式和评价区间保持相同。
hs_one_results = hs_results
hs_exact_X, hs_exact_physical = hs_two_exact_X, hs_two_exact_physical
hs_initial = hs_exact_X(hs_Xleft + np.arange(hs_N+1)*hs_a, 0)
hs_left, hs_right = hs_initial["x"][[0, -1]]
hs_dx = (hs_right-hs_left)/hs_N
hs_fixed_x = hs_left + np.arange(hs_N+1)*hs_dx
if hs_xmin <= hs_left or hs_xmax >= hs_right:
    raise ValueError("评价区间必须位于二孤子初始物理端点内部。")
if np.any(np.diff(hs_initial["x"]) <= 0):
    raise ArithmeticError("二孤子初始物理网格必须严格递增。")
print(pd.DataFrame([{
    "N": hs_N, "a": hs_a, "dt": hs_dt, "T": hs_T,
    "物理左端": hs_left, "物理右端": hs_right, "FD dx": hs_dx,
    "初始最小 J": float(hs_initial["J"].min()),
}]).to_string(index=False))
'''

TWO_EVOLVE = r'''
hs_integrable, hs_fd = hs_initial_states()
hs_two_min_edge, hs_two_min_density = np.inf, np.inf
for hs_step in range(hs_steps):
    hs_t = hs_step*hs_dt
    hs_integrable = hs_rk4_step(hs_integrable_rhs, hs_t, hs_integrable, hs_dt)
    hs_fd = hs_rk4_step(hs_fd_rhs, hs_t, hs_fd, hs_dt)
    # 动网格正格距、两种方案正密度须在整个演化区间保持。
    hs_two_min_edge = min(hs_two_min_edge, float(hs_integrable[hs_N:2*hs_N].min()))
    hs_two_min_density = min(hs_two_min_density,
        float(hs_a/hs_integrable[hs_N:2*hs_N].max()),
        float(hs_fd[hs_N-1:].min()))
hs_live_fields = {
    "Integrable": hs_integrable_fields(hs_T, hs_integrable),
    "FD": hs_fd_fields(hs_T, hs_fd),
}
print(pd.DataFrame([
    {"方案": name, "时间步数": hs_steps, "终点时间": hs_T,
     "最小格距": float(np.diff(f["x"]).min()),
     "最小密度": float(f["rho"].min())}
    for name, f in hs_live_fields.items()
]).to_string(index=False))
'''

TWO_ERROR = r'''
hs_xx = np.linspace(hs_xmin, hs_xmax, hs_neval)
hs_reference = hs_exact_physical(hs_xx, hs_T)
hs_results, hs_result_rows = {}, []
for hs_name, hs_fields in hs_live_fields.items():
    hs_u = hs_interpolate(hs_fields["x"], hs_fields["u"], hs_xx)
    hs_rho = hs_interpolate(hs_fields["rhoX"], hs_fields["rho"], hs_xx)
    hs_eu = np.abs(hs_u-hs_reference["u"])
    hs_er = np.abs(hs_rho-hs_reference["rho"])
    hs_results[hs_name] = dict(Eu=float(hs_eu.max()), Erho=float(hs_er.max()),
        eu=hs_eu, er=hs_er, u=hs_u, rho=hs_rho,
        minDx=float(np.diff(hs_fields["x"]).min()), minRho=float(hs_fields["rho"].min()))
    hs_result_rows.append({"方案": hs_name, "E_u(T)": hs_eu.max(),
                          "E_rho(T)": hs_er.max()})
hs_two_results = hs_results
hs_two_summary = {name: dict(Eu=r["Eu"], Erho=r["Erho"])
                  for name, r in hs_results.items()}
print(pd.DataFrame(hs_result_rows).to_string(index=False))
'''

TWO_PLOTS = r'''
fig, axes = plt.subplots(2, 2, figsize=(10, 6), sharex=True, sharey="row")
for col, hs_name in enumerate(("Integrable", "FD")):
    f = hs_live_fields[hs_name]
    for row, (field, coordinates) in enumerate((("u", "x"), ("rho", "rhoX"))):
        ax = axes[row, col]
        ax.plot(hs_xx, hs_reference[field], "r-", lw=1.5, label="Exact")
        mask = (f[coordinates]>=hs_xmin) & (f[coordinates]<=hs_xmax)
        ax.plot(f[coordinates][mask], f[field][mask], "b.", ms=2, label=hs_name)
        ax.set(ylabel="$u$" if field=="u" else r"$\rho$", title=hs_name)
        ax.grid(alpha=0.2)
        ax.legend(fontsize=9)
for ax in axes[-1]:
    ax.set_xlabel(r"Physical coordinate $x$")
fig.tight_layout()
plt.show()

# 将评价区间等分为 100 段，每段取误差最大值。
hs_bins = 100
hs_centers = hs_xmin+(np.arange(hs_bins)+0.5)*(hs_xmax-hs_xmin)/hs_bins
hs_bin_index = np.minimum(hs_bins-1, np.floor(
    (hs_xx-hs_xmin)/(hs_xmax-hs_xmin)*hs_bins).astype(int))
fig, axes = plt.subplots(1, 2, figsize=(10, 3.4), sharex=True)
for ax, key, label in zip(axes, ("eu", "er"), ("u", r"\rho")):
    for name, style in (("Integrable", "-"), ("FD", "--")):
        envelope = np.zeros(hs_bins)
        np.maximum.at(envelope, hs_bin_index, hs_results[name][key])
        ax.plot(hs_centers, np.log10(np.maximum(envelope, 1e-16)), style, label=name)
    ax.set(xlabel=r"Physical coordinate $x$",
           ylabel=rf"$\log_{{10}}\max|{label}_h-{label}|$")
    ax.grid(alpha=0.2)
    ax.legend(fontsize=9)
fig.tight_layout()
plt.show()
print(pd.DataFrame([{"场": field, "Integrable / FD 误差比":
    hs_results["Integrable"][key]/hs_results["FD"][key]}
    for field, key in (("u", "Eu"), ("rho", "Erho"))]).to_string(index=False))

hs_summary_rows = []
for case, results in (("单孤子", hs_single_summary), ("二孤子", hs_two_summary)):
    for name, result in results.items():
        hs_summary_rows.append({"算例": case, "方案": name,
                                "E_u(T)": result["Eu"], "E_rho(T)": result["Erho"]})
print(pd.DataFrame(hs_summary_rows).to_string(index=False))
'''


def build_two_soliton_cells() -> list:
    """Append to the original audited seven single-soliton code cells."""
    cells = []

    def markdown(cid, text):
        cells.append(nbformat.v4.new_markdown_cell(text.strip()+"\n", id=cid))

    def code(cid, text):
        cells.append(nbformat.v4.new_code_cell(text.strip()+"\n", id=cid))

    markdown("hs-two-theory", r'''
## 5　二孤子

取 $p_1=1.1$、$p_2=1.25$、$q_1=11$、$q_2=5$、$c=1$，相位常数均为 $\log6.5$。
连续二孤子的 $\tau$ 函数为

$$\begin{aligned}
f&=1+e^{\theta_1}+e^{\theta_2}+A_{12}e^{\theta_1+\theta_2},
\qquad A_{12}=\frac{12}{507},\\
\theta_i&=(p_i-q_i)X+\left(\frac1{p_i}-\frac1{q_i}\right)t+\log6.5.
\end{aligned}\tag{9}$$

相应的物理坐标与场为

$$u=\partial_t^2\log f,\qquad
x=X-\partial_t\log f-\frac1{q_1}-\frac1{q_2},\qquad
\rho=\frac1{1-\partial_X\partial_t\log f}.\tag{10}$$

归一化后的四项指数构成权重。$u$ 是时间指数系数的方差，
$J=\partial x/\partial X$ 由时间、空间指数系数的协方差给出；
进一步的混合导数确定 $m=u_{xx}+2$，供 FD 边界使用。
''')
    code("hs-two-reference", TWO_REFERENCE)
    markdown("hs-two-grid", r'''
辅助节点仍取 $X_k=-4+ka$。网格、时间步长、终点与误差评价区间沿用单孤子的配置，
初值改为二孤子的 $u(X_k,0)$、$x(X_k,0)$；FD 在相同物理端点间均匀布点。
''')
    code("hs-two-initial", TWO_INITIAL)
    markdown("hs-two-time", r'''
二孤子采用相同的空间方程。Integrable 的初始增量为
$b_k^0=u_{k+1}^0-u_k^0$、$d_k^0=x_{k+1}^0-x_k^0$，并演化

$$\begin{aligned}
\dot d_k&=-b_k,\qquad \dot x_0=-u_0(t),\\
\dot b_k&=2d_k(u_{k+1}+u_k)
+\frac{[d_k^2-a(a-1)]^2-b_k^2}{2d_k}-\frac{d_k}{2},\\
u_{k+1}&=u_k+b_k,\qquad x_{k+1}=x_k+d_k,\qquad \rho_{k+1/2}=\frac a{d_k}.
\end{aligned}\tag{11}$$

FD 初始取 $m_i^0=(D_2u^0)_i+2$、$\rho_i^0=\rho(x_i,0)$，并演化

$$\begin{aligned}
\dot m_i&=u_i(D_1m)_i+2m_i(D_1u)_i+\rho_i(D_1\rho)_i,\\
\dot\rho_i&=u_i(D_1\rho)_i+\rho_i(D_1u)_i,\\
u_{i+1}-2u_i+u_{i-1}&=\Delta x^2(m_i-2).
\end{aligned}\tag{12}$$

每个 RK4 阶段采用二孤子的解析边界，时间更新仍取式（7）。
''')
    code("hs-two-evolve", TWO_EVOLVE)
    markdown("hs-two-error-theory", r'''
在同一物理评价点集上按式（8）计算 $u$ 与 $\rho$ 的最大绝对误差。
''')
    code("hs-two-error", TWO_ERROR)
    markdown("hs-two-figures", r'''
终点波形与连续二孤子作直接比较。误差曲线将评价区间等分为 100 段，
每段保留最大绝对误差；对数图的显示下限为 $10^{-16}$，误差范数本身不截断。
''')
    code("hs-two-plots", TWO_PLOTS)
    markdown("hs-two-discussion", r'''
这里比较的是连续解析初值下的终点场误差，包含空间离散、RK4 时间推进、边界与线性重构的共同影响。
Integrable 采用原半离散方程的有限格距系数，FD 采用固定网格中心差分；
这一参数组的误差排序反映两种具体实现的表现。
''')
    return cells
