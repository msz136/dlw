# DLW 孤子数值解的误差比较

<p class="abstract">以 DLW 单孤子与二孤子的解析解为参照，比较 SD、SD2 与 FD 三种空间方案、Euler 与 RK4 时间算法，以及固定网格与自适应动网格。通过双场误差与误差曲线，考察各方案的精度及网格效果。</p>

## 1　实验设计

采用 Sheng–Yu 原文的三组孤子参数（表 1），均取 $a=2$、$c_i=1$，初相位为零。SD 与 SD2 是结构半离散方案的两种变量形式，FD 为直接差分；每组参数比较三种空间方案、两种时间算法与两种网格。

<div class="caption">表 1　孤子算例的谱参数。</div>

| 算例 | 原文图号 | 谱参数 |
|---|---|---|
| 单孤子 A | 图 1(a) | $(p,q)=(1,2)$ |
| 单孤子 B | 图 1(b) | $(p,q)=(4,-3)$ |
| 二孤子 C | 图 3 | $(p_1,q_1)=(6,-5)$；$(p_2,q_2)=(4,-3)$ |

计算区间为 $x\in[-20,20)$、$y\in[-1.5,1.5]$，取 $N_x=256$、$h_y=1/8$，共 24 个 $y$ 中点层。$x$ 方向采用四阶中心差分，时间步长为 $\Delta t=1.25\times10^{-4}$，终止时刻为 $T=0.01$。

在 $x\in[-10,10]$ 的 4001 个等距点及全部 $y$ 层上，用三次样条重构数值场，计算最大绝对误差

$$E_f(T)=\max_{(x,y)\in\mathcal G}|f_h(x,y,T)-f_*(x,y,T)|,\qquad f\in\{u,v\}.\tag{1}$$

其中 $f_*$ 为解析解。各方案在同一组物理点上评价，配对条件见表 2。

<div class="caption">表 2　三项配对比较。</div>

| 对照 | 比较因素 | 固定条件 |
|---|---|---|
| 空间离散化 | SD / SD2 / FD | 算例、RK4、固定网格、格距、时间步长 |
| 时间算法 | Euler / RK4 | 算例、空间方案、固定网格、格距、时间步长 |
| 网格策略 | 固定 / 动网格 | 算例、空间方案、RK4、节点数、时间步长 |

## 2　演化方程与数值递推

记 $h=h_y$，在 $y$ 方向定义

$$\begin{aligned}
\delta_-f_j&=\frac{f_j-f_{j-1}}h,&
\delta_0f_j&=\frac{f_{j+1}-f_{j-1}}{2h},\\
M_-f_j&=\frac{f_j+f_{j-1}}2,&
\Delta_hf_j&=\frac{f_{j+1}-2f_j+f_{j-1}}{h^2}.
\end{aligned}\tag{2}$$

在固定 $x$ 网格上采用四阶中心差分

$$
(D_1f)_{j,i}=\frac{f_{j,i-2}-8f_{j,i-1}+8f_{j,i+1}-f_{j,i+2}}{12\Delta x},
\qquad D_2f=D_1(D_1f).
\tag{3}$$

### 2.1　SD

令 $P_j=\delta_-u_j$、$W_j=v_j-\delta_0u_j$，并记

$$H_j=\frac{u_j^2}{2}+2au_j+h^2\left(\frac{W_j^2}{32}-\frac{W_j}{4}\right).\tag{4}$$

非线性半离散方程写为

$$\begin{aligned}
P_{j,t}&=-\delta_-\partial_xH_j
-\partial_x^2\left(M_-v_j-\frac{h^2}{4}\Delta_hP_j\right),\\
W_{j,t}&=-\partial_x[(u_j+2a)W_j-4u_j]+\partial_x^2W_j.
\end{aligned}\tag{5}$$

初始取 $P_j^0=\delta_-u_j^0$、$W_j^0=v_j^0-\delta_0u_j^0$。每个时间级按下式恢复物理场并计算演化右端：

$$\begin{aligned}
u_{j,i}&=u_{j-1,i}+hP_{j,i},\qquad
v_{j,i}=W_{j,i}+(\delta_0u)_{j,i},\\
\mathcal F_{P,j}&=-\delta_-D_1H_j
-D_2\left(M_-v_j-\frac{h^2}{4}\Delta_hP_j\right),\\
\mathcal F_{W,j}&=-D_1[(u_j+2a)W_j-4u_j]+D_2W_j.
\end{aligned}\tag{6}$$

### 2.2　SD2

以 $Q_j,R_j$ 为演化变量，半离散方程为

$$\begin{aligned}
Q_{j,t}&=-Q_{j,xx}-2aQ_{j,x}
-\left[(M_j+M_{j+1})_x+\frac{h^2}{4}(Q_j^2R_j^2-1)\right]Q_j,\\
R_{j,t}&=R_{j,xx}-2aR_{j,x}
+\left[(M_j+M_{j+1})_x+\frac{h^2}{4}(Q_j^2R_j^2-1)\right]R_j,\\
M_{j+1}-M_j&=h(1-Q_jR_j).
\end{aligned}\tag{7}$$

由共同初始物理场求出 $Q_j^0,R_j^0$：

$$
D_1Q_j^0=\frac12u_j^0Q_j^0,\qquad Q_{j,0}^0=1,\qquad
R_j^0=\frac{1-(v_j^0-\delta_0u_j^0)/4}{Q_j^0}.
\tag{8}$$

令 $S_j=Q_jR_j$、$m_j=M_{j,x}$。每个时间级先计算

$$\begin{aligned}
G_j&=\frac{h^2}{4}(S_j^2-1),\\
m_0&=-\frac{Q_{0,t}+D_2Q_0+2aD_1Q_0}{2Q_0}
-\frac{G_0}{2}+\frac h2D_1S_0,\\
m_{j+1}&=m_j-hD_1S_j,\qquad A_j=m_j+m_{j+1}.
\end{aligned}\tag{9}$$

其中第零层的 $Q_0$ 由 $D_1Q_0=u_0Q_0/2$、$Q_{0,0}=1$ 求出，$Q_{0,t}$ 由该式对时间求导得到。随后计算

$$\begin{aligned}
\mathcal F_{Q,j}&=-D_2Q_j-2aD_1Q_j-(A_j+G_j)Q_j,\\
\mathcal F_{R,j}&=D_2R_j-2aD_1R_j+(A_j+G_j)R_j,\\
u_{j,i}&=2\frac{(D_1Q)_{j,i}}{Q_{j,i}},\qquad
v_{j,i}=4(1-Q_{j,i}R_{j,i})+(\delta_0u)_{j,i}.
\end{aligned}\tag{10}$$

### 2.3　FD

连续 DLW 方程为

$$\begin{aligned}
u_{yt}&=-\partial_x[(u+2a)u_y]-v_{xx},\\
v_t&=-\partial_x[(u+2a)v-4u]-u_{xxy}.
\end{aligned}\tag{11}$$

取 $P_j=\delta_-u_j$，初始取 $P_j^0=\delta_-u_j^0$ 和 $v_j^0$。对连续方程作交错中心差分，得到

$$\begin{aligned}
u_{j,i}&=u_{j-1,i}+hP_{j,i},\\
\mathcal F_{P,j}&=-\delta_-D_1\left(\frac{u_j^2}{2}+2au_j\right)-D_2M_-v_j,\\
\mathcal F_{v,j}&=-D_1[(u_j+2a)v_j-4u_j]-D_2\delta_0u_j.
\end{aligned}\tag{12}$$

### 2.4　时间更新与节点运动

分别取 $z=(P,W)$、$z=(Q,R)$ 和 $z=(P,v)$，将上述右端记为 $\mathcal F(t,z)$。Euler 更新为

$$z^{n+1}=z^n+\Delta t\,\mathcal F(t_n,z^n).\tag{13}$$

RK4 更新为

$$\begin{aligned}
K_1&=\mathcal F(t_n,z^n),&
K_2&=\mathcal F\!\left(t_n+\frac{\Delta t}{2},z^n+\frac{\Delta t}{2}K_1\right),\\
K_3&=\mathcal F\!\left(t_n+\frac{\Delta t}{2},z^n+\frac{\Delta t}{2}K_2\right),&
K_4&=\mathcal F(t_n+\Delta t,z^n+\Delta tK_3),\\
z^{n+1}&=z^n+\frac{\Delta t}{6}(K_1+2K_2+2K_3+K_4).
\end{aligned}\tag{14}$$

每一级均按式（6）、（9）—（10）或（12）恢复场值并计算右端。

动网格取 $x_i=\xi_i+s_i$、$J_i=1+(D_\xi s)_i$，其中 $D_\xi$ 为式（3）在均匀 $\xi$ 节点上的四阶中心算子；此时 $D_1=J^{-1}D_\xi$、$D_2=D_1(D_1)$。令 $N_y$ 为 $y$ 层数，节点及演化变量按下式更新：

$$\begin{aligned}
\rho_j&=1-\frac{v_j-\delta_0u_j}{4},\\
\bar\rho_i&=\frac1{N_y}\sum_j\rho_{j,i},\qquad
\bar q_i=\frac1{N_y}\sum_j\bigl[(u_j+2a)\rho_j-D_1\rho_j-2a\bigr]_i,\\
V_i&=\frac{\bar q_i-\bar q_0}{\bar\rho_i},\qquad
\dot x_i=V_i,\qquad \dot z=\mathcal F(t,z)+VD_1z.
\end{aligned}\tag{15}$$

固定网格取 $V_i=0$；两种网格均采用式（13）或（14）的时间更新。

### 2.5　递推伪代码

三种方案分别以 $z=(P,W)$、$z=(Q,R)$、$z=(P,v)$ 为状态。下面的 `delta_minus`、`delta0`、`M_minus` 与 `Delta_h` 对应正文的 $y$ 向差分算子；`Dxi` 为四阶中心差分，`D1=Dxi/J`，`D2=D1(D1)`。

`recover_u(P,t,x)` 取 $u_0=u_*(y_0,x,t)$，然后逐层计算 $u_j=u_{j-1}+hP_j$。`ghost_u(u,t,x)` 在 $y$ 下侧取解析虚点，在上侧取解析值加 $3e_{-1}-3e_{-2}+e_{-3}$，其中 $e$ 为最后三层 $u$ 与解析解之差。`pack_qr` 保存 $Q$ 的第 1 层至末层及全部 $R$。

<p class="algorithm-label">SD：恢复双场并更新 $P,W$</p>

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

<p class="algorithm-label">SD2：更新 $Q,R$ 与随时间变化的下边界</p>

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

<p class="algorithm-label">FD：直接更新 $P,v$</p>

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

<p class="algorithm-label">共用节点运动与 Euler / RK4 推进</p>

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


## 3　空间离散化的比较

在 RK4 与固定网格下比较三种空间方案。表 3 列出双场最大绝对误差，加粗值为每行的最小误差。

<div class="caption">表 3　三种空间方案的误差，$T=0.01$。</div>

<table class="result-table">
<thead><tr><th scope="col">算例</th><th scope="col">场</th><th scope="col">SD</th><th scope="col">SD2</th><th scope="col">FD</th></tr></thead>
<tbody>
<tr class="case-start">
<th class="case-label" scope="rowgroup" rowspan="2">单孤子 A</th>
<th class="field-label" scope="row">$u$</th>
<td class="error-value" data-error="0.0005424866284184926"><strong>5.425e-4</strong></td>
<td class="error-value" data-error="0.0023488093746311112">2.349e-3<sup>†</sup></td>
<td class="error-value" data-error="0.00077164292627296405">7.716e-4</td>
</tr>
<tr class="">
<th class="field-label" scope="row">$v$</th>
<td class="error-value" data-error="0.00099397444268767288"><strong>9.940e-4</strong></td>
<td class="error-value" data-error="0.0017033965967641063">1.703e-3<sup>†</sup></td>
<td class="error-value" data-error="0.0011819604362610647">1.182e-3</td>
</tr>
<tr class="case-start">
<th class="case-label" scope="rowgroup" rowspan="2">单孤子 B</th>
<th class="field-label" scope="row">$u$</th>
<td class="error-value" data-error="7.835417345947171e-06">7.835e-6</td>
<td class="error-value" data-error="8.5311604314519673e-06">8.531e-6</td>
<td class="error-value" data-error="4.4866620274586211e-06"><strong>4.487e-6</strong></td>
</tr>
<tr class="">
<th class="field-label" scope="row">$v$</th>
<td class="error-value" data-error="2.9349494853336822e-06">2.935e-6</td>
<td class="error-value" data-error="3.6541425808001016e-06">3.654e-6</td>
<td class="error-value" data-error="1.5400575441582021e-06"><strong>1.540e-6</strong></td>
</tr>
<tr class="case-start">
<th class="case-label" scope="rowgroup" rowspan="2">二孤子 C</th>
<th class="field-label" scope="row">$u$</th>
<td class="error-value" data-error="9.9384573042371471e-06">9.938e-6</td>
<td class="error-value" data-error="1.319223049484064e-05">1.319e-5</td>
<td class="error-value" data-error="8.5941230213992803e-06"><strong>8.594e-6</strong></td>
</tr>
<tr class="">
<th class="field-label" scope="row">$v$</th>
<td class="error-value" data-error="3.4778979492999795e-06">3.478e-6</td>
<td class="error-value" data-error="5.9203893424397691e-06">5.920e-6</td>
<td class="error-value" data-error="1.9595038985853463e-06"><strong>1.960e-6</strong></td>
</tr>
</tbody>
</table>

<p class="table-note">† 表 3–5 中，单孤子 A 的 SD2 固定网格结果对空间分辨率敏感。</p>

单孤子 A 中，SD 的双场误差最小，较 FD 分别降低约 30% 和 16%。单孤子 B 与二孤子 C 中，FD 的双场误差最小，SD 次之，SD2 较大。

## 4　时间算法的比较

在相同空间方案、固定网格与时间步长下比较 Euler 和 RK4。表 4 将两种算法的误差并列，加粗值为每行的较小误差。

<div class="caption">表 4　Euler 与 RK4 的误差，固定网格，$T=0.01$。</div>

<table class="result-table">
<thead><tr><th scope="col">算例</th><th scope="col">空间方案</th><th scope="col">场</th><th scope="col">Euler</th><th scope="col">RK4</th></tr></thead>
<tbody>
<tr class="case-start">
<th class="case-label" scope="rowgroup" rowspan="6">单孤子 A</th>
<th class="scheme-label" scope="rowgroup" rowspan="2">SD</th>
<th class="field-label" scope="row">$u$</th>
<td class="error-value" data-error="0.00054359627223088403">5.436e-4</td>
<td class="error-value" data-error="0.0005424866284184926"><strong>5.425e-4</strong></td>
</tr>
<tr class="">
<th class="field-label" scope="row">$v$</th>
<td class="error-value" data-error="0.00098993693257942716"><strong>9.899e-4</strong></td>
<td class="error-value" data-error="0.00099397444268767288">9.940e-4</td>
</tr>
<tr class="pair-start">
<th class="scheme-label" scope="rowgroup" rowspan="2">SD2</th>
<th class="field-label" scope="row">$u$</th>
<td class="error-value" data-error="0.002339461689020661"><strong>2.339e-3</strong><sup>†</sup></td>
<td class="error-value" data-error="0.0023488093746311112">2.349e-3<sup>†</sup></td>
</tr>
<tr class="">
<th class="field-label" scope="row">$v$</th>
<td class="error-value" data-error="0.0016962276303151835"><strong>1.696e-3</strong><sup>†</sup></td>
<td class="error-value" data-error="0.0017033965967641063">1.703e-3<sup>†</sup></td>
</tr>
<tr class="pair-start">
<th class="scheme-label" scope="rowgroup" rowspan="2">FD</th>
<th class="field-label" scope="row">$u$</th>
<td class="error-value" data-error="0.00076397286443774526"><strong>7.640e-4</strong></td>
<td class="error-value" data-error="0.00077164292627296405">7.716e-4</td>
</tr>
<tr class="">
<th class="field-label" scope="row">$v$</th>
<td class="error-value" data-error="0.0011767735258552126"><strong>1.177e-3</strong></td>
<td class="error-value" data-error="0.0011819604362610647">1.182e-3</td>
</tr>
<tr class="case-start">
<th class="case-label" scope="rowgroup" rowspan="6">单孤子 B</th>
<th class="scheme-label" scope="rowgroup" rowspan="2">SD</th>
<th class="field-label" scope="row">$u$</th>
<td class="error-value" data-error="1.256240978528278e-05">1.256e-5</td>
<td class="error-value" data-error="7.835417345947171e-06"><strong>7.835e-6</strong></td>
</tr>
<tr class="">
<th class="field-label" scope="row">$v$</th>
<td class="error-value" data-error="7.5768670850795417e-06">7.577e-6</td>
<td class="error-value" data-error="2.9349494853336822e-06"><strong>2.935e-6</strong></td>
</tr>
<tr class="pair-start">
<th class="scheme-label" scope="rowgroup" rowspan="2">SD2</th>
<th class="field-label" scope="row">$u$</th>
<td class="error-value" data-error="9.2446783789557063e-06">9.245e-6</td>
<td class="error-value" data-error="8.5311604314519673e-06"><strong>8.531e-6</strong></td>
</tr>
<tr class="">
<th class="field-label" scope="row">$v$</th>
<td class="error-value" data-error="2.1721098672600192e-05">2.172e-5</td>
<td class="error-value" data-error="3.6541425808001016e-06"><strong>3.654e-6</strong></td>
</tr>
<tr class="pair-start">
<th class="scheme-label" scope="rowgroup" rowspan="2">FD</th>
<th class="field-label" scope="row">$u$</th>
<td class="error-value" data-error="7.1971243691681952e-06">7.197e-6</td>
<td class="error-value" data-error="4.4866620274586211e-06"><strong>4.487e-6</strong></td>
</tr>
<tr class="">
<th class="field-label" scope="row">$v$</th>
<td class="error-value" data-error="7.20898280298643e-06">7.209e-6</td>
<td class="error-value" data-error="1.5400575441582021e-06"><strong>1.540e-6</strong></td>
</tr>
<tr class="case-start">
<th class="case-label" scope="rowgroup" rowspan="6">二孤子 C</th>
<th class="scheme-label" scope="rowgroup" rowspan="2">SD</th>
<th class="field-label" scope="row">$u$</th>
<td class="error-value" data-error="2.0237563061520358e-05">2.024e-5</td>
<td class="error-value" data-error="9.9384573042371471e-06"><strong>9.938e-6</strong></td>
</tr>
<tr class="">
<th class="field-label" scope="row">$v$</th>
<td class="error-value" data-error="1.4301289773532844e-05">1.430e-5</td>
<td class="error-value" data-error="3.4778979492999795e-06"><strong>3.478e-6</strong></td>
</tr>
<tr class="pair-start">
<th class="scheme-label" scope="rowgroup" rowspan="2">SD2</th>
<th class="field-label" scope="row">$u$</th>
<td class="error-value" data-error="1.5692735947370196e-05">1.569e-5</td>
<td class="error-value" data-error="1.319223049484064e-05"><strong>1.319e-5</strong></td>
</tr>
<tr class="">
<th class="field-label" scope="row">$v$</th>
<td class="error-value" data-error="6.7165987521211612e-05">6.717e-5</td>
<td class="error-value" data-error="5.9203893424397691e-06"><strong>5.920e-6</strong></td>
</tr>
<tr class="pair-start">
<th class="scheme-label" scope="rowgroup" rowspan="2">FD</th>
<th class="field-label" scope="row">$u$</th>
<td class="error-value" data-error="1.2657853485809056e-05">1.266e-5</td>
<td class="error-value" data-error="8.5941230213992803e-06"><strong>8.594e-6</strong></td>
</tr>
<tr class="">
<th class="field-label" scope="row">$v$</th>
<td class="error-value" data-error="1.4118654005135234e-05">1.412e-5</td>
<td class="error-value" data-error="1.9595038985853463e-06"><strong>1.960e-6</strong></td>
</tr>
</tbody>
</table>

单孤子 A 中，两种算法的误差相近，差异约在 1% 以内。单孤子 B 与二孤子 C 中，RK4 在三种空间方案下均有较小的双场误差；SD2 的 $v$ 误差分别降至 Euler 的约 $1/5.9$ 和 $1/11.3$。

后两组算例中，$u$ 场在 RK4 下为 SD 优于 SD2，在 Euler 下为 SD2 优于 SD；$v$ 场则均为 SD 优于 SD2。

固定空间配置，取 $\Delta t$、$\Delta t/2$、$\Delta t/4$，以相邻时间步长的数值场差计算观测阶

$$p_f=\log_2\frac{\|f_{\Delta t}-f_{\Delta t/2}\|_{\infty,\mathcal G}}{\|f_{\Delta t/2}-f_{\Delta t/4}\|_{\infty,\mathcal G}},\qquad f\in\{u,v\}.\tag{16}$$

Euler 的单孤子试验观测阶为 0.9874–1.0025；SD2 在原文图 3–5 二孤子中的观测阶为 0.9903–1.0001，均接近一阶。

## 5　网格策略的比较

在相同算例、空间方案、RK4、节点数和时间步长下，比较均匀固定网格与自适应动网格。加粗值为每行的较小误差。

<div class="caption">表 5　固定网格与动网格的误差，RK4，$T=0.01$。</div>

<table class="result-table">
<thead><tr><th scope="col">算例</th><th scope="col">空间方案</th><th scope="col">场</th><th scope="col">固定网格</th><th scope="col">动网格</th></tr></thead>
<tbody>
<tr class="case-start">
<th class="case-label" scope="rowgroup" rowspan="6">单孤子 A</th>
<th class="scheme-label" scope="rowgroup" rowspan="2">SD</th>
<th class="field-label" scope="row">$u$</th>
<td class="error-value" data-error="0.0005424866284184926">5.425e-4</td>
<td class="error-value" data-error="0.00033167767151121019"><strong>3.317e-4</strong></td>
</tr>
<tr class="">
<th class="field-label" scope="row">$v$</th>
<td class="error-value" data-error="0.00099397444268767288">9.940e-4</td>
<td class="error-value" data-error="0.00059698767520566243"><strong>5.970e-4</strong></td>
</tr>
<tr class="pair-start">
<th class="scheme-label" scope="rowgroup" rowspan="2">SD2</th>
<th class="field-label" scope="row">$u$</th>
<td class="error-value" data-error="0.0023488093746311112">2.349e-3<sup>†</sup></td>
<td class="error-value" data-error="0.00057022367152970155"><strong>5.702e-4</strong></td>
</tr>
<tr class="">
<th class="field-label" scope="row">$v$</th>
<td class="error-value" data-error="0.0017033965967641063">1.703e-3<sup>†</sup></td>
<td class="error-value" data-error="0.00078984608385623822"><strong>7.898e-4</strong></td>
</tr>
<tr class="pair-start">
<th class="scheme-label" scope="rowgroup" rowspan="2">FD</th>
<th class="field-label" scope="row">$u$</th>
<td class="error-value" data-error="0.00077164292627296405">7.716e-4</td>
<td class="error-value" data-error="0.00052930742648849005"><strong>5.293e-4</strong></td>
</tr>
<tr class="">
<th class="field-label" scope="row">$v$</th>
<td class="error-value" data-error="0.0011819604362610647">1.182e-3</td>
<td class="error-value" data-error="0.00079265537835060407"><strong>7.927e-4</strong></td>
</tr>
<tr class="case-start">
<th class="case-label" scope="rowgroup" rowspan="6">单孤子 B</th>
<th class="scheme-label" scope="rowgroup" rowspan="2">SD</th>
<th class="field-label" scope="row">$u$</th>
<td class="error-value" data-error="7.835417345947171e-06"><strong>7.835e-6</strong></td>
<td class="error-value" data-error="8.4195457020763698e-06">8.420e-6</td>
</tr>
<tr class="">
<th class="field-label" scope="row">$v$</th>
<td class="error-value" data-error="2.9349494853336822e-06"><strong>2.935e-6</strong></td>
<td class="error-value" data-error="3.1232775912215516e-06">3.123e-6</td>
</tr>
<tr class="pair-start">
<th class="scheme-label" scope="rowgroup" rowspan="2">SD2</th>
<th class="field-label" scope="row">$u$</th>
<td class="error-value" data-error="8.5311604314519673e-06"><strong>8.531e-6</strong></td>
<td class="error-value" data-error="8.5977653438984447e-06">8.598e-6</td>
</tr>
<tr class="">
<th class="field-label" scope="row">$v$</th>
<td class="error-value" data-error="3.6541425808001016e-06">3.654e-6</td>
<td class="error-value" data-error="3.4589334964030272e-06"><strong>3.459e-6</strong></td>
</tr>
<tr class="pair-start">
<th class="scheme-label" scope="rowgroup" rowspan="2">FD</th>
<th class="field-label" scope="row">$u$</th>
<td class="error-value" data-error="4.4866620274586211e-06">4.487e-6</td>
<td class="error-value" data-error="3.5798707945233765e-06"><strong>3.580e-6</strong></td>
</tr>
<tr class="">
<th class="field-label" scope="row">$v$</th>
<td class="error-value" data-error="1.5400575441582021e-06"><strong>1.540e-6</strong></td>
<td class="error-value" data-error="1.6975730521839871e-06">1.698e-6</td>
</tr>
<tr class="case-start">
<th class="case-label" scope="rowgroup" rowspan="6">二孤子 C</th>
<th class="scheme-label" scope="rowgroup" rowspan="2">SD</th>
<th class="field-label" scope="row">$u$</th>
<td class="error-value" data-error="9.9384573042371471e-06">9.938e-6</td>
<td class="error-value" data-error="9.744408561107587e-06"><strong>9.744e-6</strong></td>
</tr>
<tr class="">
<th class="field-label" scope="row">$v$</th>
<td class="error-value" data-error="3.4778979492999795e-06"><strong>3.478e-6</strong></td>
<td class="error-value" data-error="3.7251165048712842e-06">3.725e-6</td>
</tr>
<tr class="pair-start">
<th class="scheme-label" scope="rowgroup" rowspan="2">SD2</th>
<th class="field-label" scope="row">$u$</th>
<td class="error-value" data-error="1.319223049484064e-05">1.319e-5</td>
<td class="error-value" data-error="1.0924825935898497e-05"><strong>1.092e-5</strong></td>
</tr>
<tr class="">
<th class="field-label" scope="row">$v$</th>
<td class="error-value" data-error="5.9203893424397691e-06">5.920e-6</td>
<td class="error-value" data-error="4.5031601834666368e-06"><strong>4.503e-6</strong></td>
</tr>
<tr class="pair-start">
<th class="scheme-label" scope="rowgroup" rowspan="2">FD</th>
<th class="field-label" scope="row">$u$</th>
<td class="error-value" data-error="8.5941230213992803e-06">8.594e-6</td>
<td class="error-value" data-error="5.8073944056991067e-06"><strong>5.807e-6</strong></td>
</tr>
<tr class="">
<th class="field-label" scope="row">$v$</th>
<td class="error-value" data-error="1.9595038985853463e-06"><strong>1.960e-6</strong></td>
<td class="error-value" data-error="2.1573692995380256e-06">2.157e-6</td>
</tr>
</tbody>
</table>

单孤子 A 中，动网格降低三种方案的双场误差。单孤子 B 中，FD 的 $u$ 误差降低约 20%，$v$ 误差增加约 10%。二孤子 C 中，SD2 的双场误差分别降低约 17% 和 24%；FD 的 $u$ 误差降低约 32%，$v$ 误差增加约 10%。

<!-- DLW_SAVED_FIELDS_BEGIN -->

## 6　Euler 局部误差曲线

取 $T=0.01$、$x\in[-1,1]$，横轴为 $x$，纵轴为各 $y$ 层上的最大绝对误差 $e_f(x)=\max_j|f_h(x,y_j,T)-f_*(x,y_j,T)|$。每图用蓝、橙、绿三条曲线分别表示 SD、SD2、FD；曲线越低，误差越小。同一算例、同一场的固定网格与动网格图采用相同纵轴尺度。


<h3 id="error-case-A">单孤子 A</h3>
<div class="error-curve-pair">
<figure class="field-figure">
<img alt="算例 A，固定网格：u 的绝对误差随 x 的变化。" decoding="async" loading="lazy" src="Workspaces/index_readability_20261006/figures/fig1a_euler_fixed_u_error_curve.png"/>
<figcaption>图 1　算例 A，固定网格：u 的绝对误差随 x 的变化。</figcaption>
</figure>
<figure class="field-figure">
<img alt="算例 A，固定网格：v 的绝对误差随 x 的变化。" decoding="async" loading="lazy" src="Workspaces/index_readability_20261006/figures/fig1a_euler_fixed_v_error_curve.png"/>
<figcaption>图 2　算例 A，固定网格：v 的绝对误差随 x 的变化。</figcaption>
</figure>
</div>
<div class="error-curve-pair">
<figure class="field-figure">
<img alt="算例 A，移动网格：u 的绝对误差随 x 的变化。" decoding="async" loading="lazy" src="Workspaces/index_readability_20261006/figures/fig1a_euler_moving_u_error_curve.png"/>
<figcaption>图 3　算例 A，动网格：u 的绝对误差随 x 的变化。</figcaption>
</figure>
<figure class="field-figure">
<img alt="算例 A，移动网格：v 的绝对误差随 x 的变化。" decoding="async" loading="lazy" src="Workspaces/index_readability_20261006/figures/fig1a_euler_moving_v_error_curve.png"/>
<figcaption>图 4　算例 A，动网格：v 的绝对误差随 x 的变化。</figcaption>
</figure>
</div>
<h3 id="error-case-B">单孤子 B</h3>
<div class="error-curve-pair">
<figure class="field-figure">
<img alt="算例 B，固定网格：u 的绝对误差随 x 的变化。" decoding="async" loading="lazy" src="Workspaces/index_readability_20261006/figures/fig1b_euler_fixed_u_error_curve.png"/>
<figcaption>图 5　算例 B，固定网格：u 的绝对误差随 x 的变化。</figcaption>
</figure>
<figure class="field-figure">
<img alt="算例 B，固定网格：v 的绝对误差随 x 的变化。" decoding="async" loading="lazy" src="Workspaces/index_readability_20261006/figures/fig1b_euler_fixed_v_error_curve.png"/>
<figcaption>图 6　算例 B，固定网格：v 的绝对误差随 x 的变化。</figcaption>
</figure>
</div>
<div class="error-curve-pair">
<figure class="field-figure">
<img alt="算例 B，移动网格：u 的绝对误差随 x 的变化。" decoding="async" loading="lazy" src="Workspaces/index_readability_20261006/figures/fig1b_euler_moving_u_error_curve.png"/>
<figcaption>图 7　算例 B，动网格：u 的绝对误差随 x 的变化。</figcaption>
</figure>
<figure class="field-figure">
<img alt="算例 B，移动网格：v 的绝对误差随 x 的变化。" decoding="async" loading="lazy" src="Workspaces/index_readability_20261006/figures/fig1b_euler_moving_v_error_curve.png"/>
<figcaption>图 8　算例 B，动网格：v 的绝对误差随 x 的变化。</figcaption>
</figure>
</div>
<h3 id="error-case-C">二孤子 C</h3>
<div class="error-curve-pair">
<figure class="field-figure">
<img alt="算例 C，固定网格：u 的绝对误差随 x 的变化。" decoding="async" loading="lazy" src="Workspaces/index_readability_20261006/figures/fig3_euler_fixed_u_error_curve.png"/>
<figcaption>图 9　算例 C，固定网格：u 的绝对误差随 x 的变化。</figcaption>
</figure>
<figure class="field-figure">
<img alt="算例 C，固定网格：v 的绝对误差随 x 的变化。" decoding="async" loading="lazy" src="Workspaces/index_readability_20261006/figures/fig3_euler_fixed_v_error_curve.png"/>
<figcaption>图 10　算例 C，固定网格：v 的绝对误差随 x 的变化。</figcaption>
</figure>
</div>
<div class="error-curve-pair">
<figure class="field-figure">
<img alt="算例 C，移动网格：u 的绝对误差随 x 的变化。" decoding="async" loading="lazy" src="Workspaces/index_readability_20261006/figures/fig3_euler_moving_u_error_curve.png"/>
<figcaption>图 11　算例 C，动网格：u 的绝对误差随 x 的变化。</figcaption>
</figure>
<figure class="field-figure">
<img alt="算例 C，移动网格：v 的绝对误差随 x 的变化。" decoding="async" loading="lazy" src="Workspaces/index_readability_20261006/figures/fig3_euler_moving_v_error_curve.png"/>
<figcaption>图 12　算例 C，动网格：v 的绝对误差随 x 的变化。</figcaption>
</figure>
</div>


<!-- DLW_SAVED_FIELDS_END -->

## 7　结论

在 RK4 固定网格下，单孤子 A 的 SD 双场误差最小，单孤子 B 与二孤子 C 的 FD 双场误差最小。后两组采用 RK4 时精度提升明显；动网格在单孤子 A 中降低双场误差，在单孤子 B 与二孤子 C 中呈现不同的场间表现。Euler 的时间自收敛观测阶接近 1。

## 参考资料

<div class="references">
<p>[1] H.-H. Sheng and G.-F. Yu. Solitons, breathers and rational solutions for a (2+1)-dimensional dispersive long wave system. <em>Physica D</em>, 432 (2022), 133140.</p>
<p>[2] <a href="../dlw_single_aligned_20260929/HANDOFF.md">DLW 原文单孤子三方案的误差结果</a>。</p>
<p>[3] <a href="../dlw_sd2_uv_init_20260929/HANDOFF.md">DLW 原文二孤子三方案的误差结果</a>。</p>
</div>
