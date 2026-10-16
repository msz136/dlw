# 2B：实际时间推进是否保持 DLW 辛形式

2026-10-13。结论是：**上一阶段的 Hamilton 空间离散不使 RK4 自动成为辛方法；隐式中点的辛性成立于其隐式方程被精确求解时，有限次 Newton 求解的实际映射还存在可测的求解缺陷。** 本实验对完整切映射作检验，不以能量漂移代替辛性。

## 1. 应检验哪个二形式

如果 $x$ 是固定网格的空间标签，对场相空间的变分有 $\delta x=0$。因而 $\delta u\wedge\delta x$ 限制在这些场变分上恒零，不能检验非退化辛结构。若将 $x$ 视为移动网格变量，也必须从具体括号建立共轭关系；不能预先把物理场 $u$ 和节点位置 $x$ 当作一对正则变量。含空间微分的协变形式也不等于这里的场相空间辛形式。

本实验直接使用上一阶段 1A/1C 已建立的周期 DLW 空间离散。参数为

\[
M=3,\quad h_y=4,\quad c=2,\quad\gamma=4,\quad
L_x=2\pi,\quad N_x=15,\quad \Delta x=L_x/N_x.
\]

使用同一个中心一阶差分 $D^T=-D$，二阶项由 $D^2$ 复合产生。奇数网格使 $\ker D$ 只有常数模，没有偶数中心差分的额外 Nyquist 零模。这是一个新的、小规模完整切映射实验；不是将原 24 点算例的结果直接改名。

原约化坐标为 $p=P_0U,s=w-c$，满足横向均值为零；物理重构为

\[
U=p+\frac{\gamma-\Pi(ps)}c,\qquad w=c+s,
\qquad u=U-2a,\quad v=w+C_0p+4.
\]

这里取 $a=0$，仅固定物理 $u$ 的常数平移。设 $Q_y,Q_x$ 分别是横向、纵向零均值空间的正交基，令

\[
Q=Q_y\otimes Q_x,\qquad E=\operatorname{diag}(Q,Q),\qquad
\binom ps=z_c+E z.
\]

固定的纵向平均是

\[
\overline p=(-3,0,3),\qquad \overline s=(-1,0,1).
\]

横向均值约束后的维数为 $2(M-1)N_x=60$，还要固定四个独立纵向平均 Casimir。因此所用辛叶的维数为 **56**，不是 60。

记 $\varpi=h_y\Delta x$，

\[
D_r=I_{M-1}\otimes(Q_x^TDQ_x),\qquad
B_\mathrm{leaf}=-\frac1\varpi
\begin{pmatrix}0&D_r\\D_r&0\end{pmatrix}.
\]

采用与 2A 相同的约定 $i_{X_H}\omega=dH$，则二形式矩阵为

\[
\boxed{\Omega=-B_\mathrm{leaf}^{-1}
=\varpi\begin{pmatrix}0&D_r^{-1}\\D_r^{-1}&0\end{pmatrix}.}
\]

坐标括号是普通欧氏梯度的 $B_\mathrm{leaf}$，所以权重 $\varpi$ 不可遗漏。它满足 $-\Omega F=\nabla H$。本例条件数约 4.7834，未在病态近退化叶上作矩阵求逆。

## 2. 非线性流、初值与实验尺度

求解的仍是上一阶段的 Hamilton 流

\[
p_t=-P_0Dk,\qquad s_t=-P_0Df,
\]
\[
f=Uw-Dw-\gamma,\qquad
k=U^2/2+\beta w^2+DU+RDw,\quad \beta=h_y^2/32.
\]

代码直接导入 1A 的方程、Hamiltonian、初值与空间算子；不调用该模块的主程序，不改旧文件。初值为原有非线性 Fourier 见证

\[
p=(-3,0,3)+(1/5,-2/5,1/5)\cos x,
\]
\[
g=(1,2,3)+(1/6,1/7,-1/6-1/7)\cos x,\qquad s=4g/h_y-c.
\]

短时间窗为 $T=0.02$。步长从 0.02 依次减半至 0.0003125。每种方法分别检验：从同一非线性初值出发的单步映射，以及经过 $T/\Delta t$ 步的复合映射。另取 $N_x=9,25$，对应辛叶维数 32、96，作结构复查；这些网格结果不作空间收敛阶拟合。

## 3. 切映射与正确的检验量

所报相对缺陷为

\[
\boxed{\mathcal E_\omega(\Phi)
=\frac{\|(D\Phi)^T\Omega D\Phi-\Omega\|_F}{\|\Omega\|_F}.}
\]

范数在固定正交叶坐标中计算。换到非正交坐标后，原始矩阵 Frobenius 范数未必不变，因此物理坐标核验将矩阵重新拉回同一叶坐标再比较。理论上的“二形式缺陷为零”与坐标无关。

RK4 对全部内部级逐级求导；总时间切映射按链式法则逐步相乘。空间 Jacobian 由多项式方程解析求导，并以复步长方向微分独立核验。校验还包含

\[
A(z)^T\Omega+\Omega A(z)=0,\qquad A=DF,
\]

确认数值检验确实针对 Hamilton 向量场。

Euler 的缺陷有精确恒等式

以下时间推进公式中的 $h$ 表示时间步长；横向格距仍记为 $h_y$。

\[
(I+hA)^T\Omega(I+hA)-\Omega=h^2 A^T\Omega A.
\]

因此本例单步精化精确显示二阶，固定总时间显示约一阶。

隐式中点的精确映射满足

\[
y=z+hF((z+y)/2),\qquad
D\Phi=(I-hA_m/2)^{-1}(I+hA_m/2),
\]

其中 $A_m=DF((z+y)/2)$。Hamilton 恒等式保证这个 Cayley 矩阵保持 $\Omega$。一般显式 RK4 不满足辛 RK 的代数条件；实际 DLW 结果中也可观测到非零缺陷。

单独的解析校准使用谐振子 $A=\left(\begin{smallmatrix}0&1\\-1&0\end{smallmatrix}\right)$。对经典 RK4，

\[
R_4(hA)^T\Omega R_4(hA)-\Omega
=\left(-\frac{h^6}{72}+\frac{h^8}{576}\right)\Omega.
\]

这一精确公式说明：线性 Hamilton 系统的 RK4 辛缺陷可以首先出现在六阶，不能预设所有非线性数据的单步缺陷都表现为五阶。谐振子只作单独标明的校准，未混入 DLW 实验图表。

## 4. Newton 求解不能用理想公式冒充实际切映射

若非线性方程未充分收敛，仍在近似中点套用上述 Cayley 公式，它依然代数保辛。这只能检验一个形式矩阵，无法判断实际有限次 Newton 程序。

本实验从 Euler 预测值开始，令 $Y=\partial y/\partial z$，每次 Newton 校正为

\[
m=(z+y)/2,\quad r=y-z-hF(m),\quad J=I-hA(m)/2,
\quad\delta=J^{-1}r,\quad y^+=y-\delta.
\]

实际切映射同步更新为

\[
\boxed{Y^+=Y-J^{-1}\left[
Y-I-\frac h2A(m)(I+Y)
+\frac h4\bigl(DA(m)[\delta]\bigr)(I+Y)
\right].}
\]

这里的最后一项不能丢掉。代码以复步长计算多项式的 $DA(m)[\delta]$，并将整个固定迭代次数的 Newton 程序再次独立作复步长方向微分，核对实际 $Y$。它描述停止次数保持不变的局部分支；跨越停止次数切换边界时，程序未必可微。

在 $h=0.02$ 的同一 DLW 初值上，得到：

| Newton 绝对容差 | 校正次数 | 方程残差 $\lVert r\rVert_\infty$ | 实际辛缺陷 | 套用理想公式的缺陷 |
|---:|---:|---:|---:|---:|
| $10^{-3}$ | 0 | $6.4143\times10^{-4}$ | $9.1148\times10^{-3}$ | $4.33\times10^{-16}$ |
| $10^{-8}$ | 1 | $1.3736\times10^{-9}$ | $1.7904\times10^{-8}$ | $4.74\times10^{-16}$ |
| $10^{-14}$ | 2 | $1.3010\times10^{-16}$ | $3.1757\times10^{-16}$ | $4.95\times10^{-16}$ |

这明确分离了积分方法的理论辛性、非线性求解误差与浮点矩阵误差。

## 5. 主要数值结果与精度的区别

固定 $T=0.02,\Delta t=0.0025$，共八步。物理场误差是相对于同一个半离散 ODE 的高精度 DOP853 参考轨道，比较 $u,v$ 全网格的最大绝对差；它不是对原 PDE 的总误差。

| 方法 | 相对辛缺陷 | 物理场时间误差 $\max(\lvert\Delta u\rvert,\lvert\Delta v\rvert)$ |
|---|---:|---:|
| Euler | $1.1398\times10^{-3}$ | $9.6089\times10^{-5}$ |
| RK4 | $1.6479\times10^{-12}$ | $1.7304\times10^{-12}$ |
| 隐式中点 | $1.0662\times10^{-15}$ | $1.5474\times10^{-7}$ |

**中点保持二形式的表现更好；RK4 在这个短时间、相同步长实验中的场精度更高。** 两种结论衡量的对象不同，不能以保辛排名替代精度排名。CSV 同时保留叶坐标误差和物理 $u,v$ 误差，命名明确区分。

RK4 单步缺陷在较粗的可分辨两级上观测阶为 5.9195、5.7245；固定总时间的前三个可分辨级为 4.9233、4.7364、4.4055。这里只报告实际比值，不把它提升为统一阶数定理；低于 $10^{-12}$ 的点不拟合阶。图中的浅灰带表示此保守拟合排除区，不代表其内的所有数值都纯属舍入。

默认中点采用残差阈值 $10^{-14}$。在 $\Delta t=0.00125$ 时，一次 Newton 已满足这一阈值，因而提前停止；固定总时间辛缺陷反而达到 $2.7315\times10^{-13}$，高于若干较粗步长。**这个小峰来自有限求解程序的停止分支，不是理论中点公式失去辛性。** 保留相同容差、但要求至少两次 Newton 校正的对照，将该点缺陷降为 $1.5069\times10^{-15}$。这一对照的全部步长缺陷位于约 $3.2\times10^{-16}$ 到 $3.8\times10^{-15}$，见 `midpoint_min_two_iterations.csv`。

所有轨道的 Casimir 均值漂移处于浮点舍入量级。能量漂移只作为额外背景列：中点可精确保辛而不精确保当前非二次 Hamiltonian；RK4 的很小能量漂移也不能作为辛性证据。

## 6. 物理坐标中的独立拉回核验

令 $T:z\mapsto(u,v)$ 为固定 Casimir 叶的非线性嵌入，$A_j=DT(z_j)$。它有固定的左逆微分

\[
L=E^T\begin{pmatrix}P_0&0\\-C_0P_0&P_0\end{pmatrix},
\qquad LA_j=I.
\]

式中 $P_0,C_0$ 均已延拓到整个 $x$ 网格。环境中的矩阵代表 $\Omega_\mathrm{phys}=L^T\Omega L$ 本身退化；这里只把它限制到该非线性辛叶。对实际时间映射，

\[
D\Phi_\mathrm{phys}=A_1D\Phi L,
\]
\[
A_0^T\bigl[(D\Phi_\mathrm{phys})^T\Omega_\mathrm{phys}
D\Phi_\mathrm{phys}-\Omega_\mathrm{phys}\bigr]A_0
=(D\Phi)^T\Omega D\Phi-\Omega.
\]

三个方法的完整矩阵等式均已独立核验，相对残差不超过 $7.7\times10^{-16}$。这不是把 $u$ 误当作正则坐标，也不是对 90 维退化环境直接求辛逆。

## 7. 验证、文件与复现

```powershell
python Workspaces/dlw_stage2_20261013/symplectic/symplectic_experiment.py
```

仅使用既有 NumPy、SciPy、Matplotlib，无新增依赖。一次完整运行约五秒。

- `symplectic_defect.png/.pdf`：单步、固定总时间和累计辛缺陷。
- `midpoint_solver_tolerance.png/.pdf`：实际 Newton 程序与理想隐式公式的差别。
- `single_step.csv`、`fixed_time.csv`、`defect_timeseries.csv`：完整缺陷及轨道诊断。
- `midpoint_tolerance.csv`、`midpoint_min_two_iterations.csv`：容差和至少两次校正的对照。
- `single_step_orders.csv`、`fixed_time_orders.csv`：只对可靠量级作观测阶估计。
- `grid_checks.csv`：另外两个奇数网格的结构复查。
- `physical_pullback.csv`、`harmonic_calibration.csv`：坐标拉回及解析校准。
- `tangent_maps.npz`：$\Omega,B,E$、叶中心、初值、参考切映射与三个八步实际切映射。
- `validation.json`：40 项校验、参数、源脚本 SHA-256、版本、参考轨道精化。

DOP853 同时推进状态与完整变分方程，两组容差精化后的物理场差为 $1.33\times10^{-15}$，切映射相对差为 $4.03\times10^{-16}$。这支持本次短时误差比较；它不是一般高精度求解保证。

绘图继续使用已选的并排科学时序面板、共享方法配色、独立量纲轴。两张成图已目视核查，轴数值与 CSV 一致。全部结论限于指定周期 Hamilton 空间离散与短时间测试；不涉及全离散可积性、长期场误差有界或论文开放边界 PE/PF 算法的辛性。
