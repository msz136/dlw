# DLW 数值递推伪代码

三种方案分别以 $z=(P,W)$、$z=(Q,R)$、$z=(P,v)$ 为状态。下面的 `delta_minus`、`delta0`、`M_minus` 与 `Delta_h` 对应正文的 $y$ 向差分算子；`Dxi` 为四阶中心差分，`D1=Dxi/J`，`D2=D1(D1)`。

`recover_u(P,t,x)` 取 $u_0=u_*(y_0,x,t)$，然后逐层计算 $u_j=u_{j-1}+hP_j$。`ghost_u(u,t,x)` 在 $y$ 下侧取解析虚点，在上侧取解析值加 $3e_{-1}-3e_{-2}+e_{-3}$，其中 $e$ 为最后三层 $u$ 与解析解之差。`pack_qr` 保存 $Q$ 的第 1 层至末层及全部 $R$。

## SD：恢复双场并更新 $P,W$

```python
def RHS_SD(t, z, x, J, D1, D2, mesh):
    P, W = unpack_pw(z)
    u = recover_u(P, t, x)
    gl, gr = ghost_u(u, t, x)
    v = W + delta0(u, gl, gr)
    V = velocity(u, 1 - W/4, D1, mesh)
    H = u**2/2 + 2*a*u + h**2*(W**2/32 - W/4)
    lapP = Delta_h(P, left=(u[0]-gl)/h, right=(gr-u[-1])/h)
    FP = -delta_minus(D1(H)) - D2(M_minus(v) - h**2*lapP/4)
    FW = -D1((u + 2*a)*W - 4*u) + D2(W)
    return pack_pw(FP + V*D1(P), FW + V*D1(W)), V
```

## SD2：更新 $Q,R$ 与随时间变化的下边界

`Dxi(f,jump)` 在跨越 $x$ 端点时按 $f(x+L)=f(x)+jump$ 延拓。离散提升同时求出 $Q$ 与端点跃变量：$D_\xi Q+b\,jump=JuQ/2$、$Q(x_0)=1$；$b$ 是四阶差分中跨端点项的系数向量。每个时间级按当前 $t,x,J$ 求出第零层 $Q_0$。

```python
def lift(u, J):
    L = block_matrix([[Dxi_matrix - diag(J*u/2), b], [e0.T, 0]])
    Q, jump = split(solve(L, join(zeros(Nx), 1)))
    return Q, jump, L

def RHS_SD2(t, z, x, J, D1, D2, mesh):
    Qint, R = unpack_qr(z)
    u0, u0t, u0x = exact_lower_u_and_derivatives(t, x)
    Q0, jump0, L = lift(u0, J)
    Q = stack(Q0, Qint)
    right = right_init * (1 + jump0) / right_init[0]
    Qx, Rx = D1(Q, right-1), D1(R, 1/right-1)
    u = 2*Qx/Q
    gl, gr = ghost_u(u, t, x)
    v = 4*(1-Q*R) + delta0(u, gl, gr)
    V = velocity(u, Q*R, D1, mesh)
    rhs0 = (Dxi(V)*u0 + J*(u0t + V*u0x))*Q0/2
    Q0t = solve(L, join(rhs0, 0))[:-1] - V*Qx[0]
    Qxx, Rxx, S = D1(Qx), D1(Rx), Q*R
    G, Sx = h**2*(S**2-1)/4, D1(S)
    m0 = -(Q0t+Qxx[0]+2*a*Qx[0])/(2*Q0) - G[0]/2 + h*Sx[0]/2
    m = m0 - h*prepend_zero(cumsum(Sx, axis="y"))
    A = m[:-1] + m[1:]
    FQ = -Qxx - 2*a*Qx - (A+G)*Q
    FR =  Rxx - 2*a*Rx + (A+G)*R
    return pack_qr(FQ + V*Qx, FR + V*Rx), V
```

## FD：直接更新 $P,v$

```python
def RHS_FD(t, z, x, J, D1, D2, mesh):
    P, v = unpack_pv(z)
    u = recover_u(P, t, x)
    gl, gr = ghost_u(u, t, x)
    uy = delta0(u, gl, gr)
    V = velocity(u, 1-(v-uy)/4, D1, mesh)
    FP = -delta_minus(D1(u**2/2 + 2*a*u)) - D2(M_minus(v))
    Fv = -D1((u+2*a)*v - 4*u) - D2(uy)
    return pack_pv(FP + V*D1(P), Fv + V*D1(v)), V
```

## 共用节点运动与 Euler / RK4 推进

初始 $P=\delta_-u_*$、$W=v_*-\delta_0u_*$。SD2 初始逐层调用 `lift` 得到 $Q$ 与 `right_init=1+jump`，再取 $R=[1-(v_*-\delta_0u_*)/4]/Q$。动网格初始节点由解析监测密度的累积积分等分得到。场变量与节点位移组成同一状态 $Y=(z,s)$；RK4 每一级重建节点、算子、场与边界。

```python
def velocity(u, rho, D1, mesh):
    if mesh == "fixed": return zeros(Nx)
    rho_bar = mean(rho, axis="y")
    q_bar = mean((u+2*a)*rho - D1(rho) - 2*a, axis="y")
    return (q_bar-q_bar[0]) / rho_bar

def stage(t, Y):
    z, s = split_state(Y)
    x, J = xi+s, 1+Dxi(s)
    D1 = lambda f, jump=0: Dxi(f, jump)/J
    D2 = lambda f: D1(D1(f))
    dz, V = RHS[model](t, z, x, J, D1, D2, mesh)
    return join(dz, V)

x0 = xi if mesh == "fixed" else equidistribute(exact_initial_density)
Y = join(initial_state(model, x0), x0-xi)
for n in range(Nt):
    t = n*dt
    if method == "Euler":
        Y = Y + dt*stage(t, Y)
    else:
        K1 = stage(t, Y)
        K2 = stage(t+dt/2, Y+dt*K1/2)
        K3 = stage(t+dt/2, Y+dt*K2/2)
        K4 = stage(t+dt, Y+dt*K3)
        Y = Y + dt*(K1+2*K2+2*K3+K4)/6
```

实现来源：`Workspaces/dlw_sd2_uv_init_20260929/consistent_sd2.py`、`Workspaces/dlw_two_soliton_20260929/models.py`、`Workspaces/dlw_semidiscrete/numerics/lib/parametric_open.py`、`moving_mesh.py`、`parametric.py`、`solver.py`。单孤子入口为 `Workspaces/dlw_single_aligned_20260929/experiment.py`。
