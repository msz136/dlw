# 半离散 DLW 的 Darboux 与 Lax 表示

从原物理方程重构辅助热势，得到一阶 Darboux 交织及逐格点 Lax 对。热势的局部存在由原方程保证；在逐点非退化支上，传递相容式恢复原方程。

## 1. 原物理方程

设 $U_j(x,t),w_j(x,t)$ 为光滑实值场，$h>0$ 为格距。格点可取整数开链，$x$ 取连续区间。定义

$$Ef_j=f_{j+1},\qquad
\delta_-f_j=\frac{f_j-f_{j-1}}h,\qquad
M_-f_j=\frac{f_j+f_{j-1}}2.\tag{1}$$

半离散 DLW 为

$$\begin{aligned}
\delta_-\!\left[\partial_tU+\partial_x\!\left(\frac{U^2}2+\frac{h^2w^2}{32}\right)\right]
+\partial_x^2(\delta_-U+M_-w)&=0,\\
\partial_tw+\partial_x(Uw)-\partial_x^2w&=0.
\end{aligned}\tag{2}$$

旧变量满足 $U=u+2a$、$w=W-4$，其中 $a$ 是常背景参数。下文的 $w_j\ne0$ 对应 $W_j\ne4$。

## 2. 热势的局部重构

记

$$F_j=\frac{U_j^2}2+\frac{h^2w_j^2}{32},\qquad
S_j=\partial_tU_j+\partial_xF_j+\partial_x^2U_j+\frac h2\partial_x^2w_j.\tag{3}$$

由式（2）的第一式，得到

$$S_{j+1}-S_j=-h\partial_x^2w_j.\tag{4}$$

选定参考点 $x_*$ 和任意函数 $v_0(t)$，在参考格点定义

$$V_0(x,t)=v_0(t)-\frac12\int_{x_*}^{x}S_0(\xi,t)\,d\xi.\tag{5}$$

沿格点递推 $V_{j+1}=V_j+(h/2)\partial_xw_j$。式（4）保证所有格点同时满足

$$\boxed{\partial_xV_j=-\frac12S_j,\qquad
V_{j+1}-V_j=\frac h2\partial_xw_j.}\tag{6}$$

因此原方程为热势的两种重构方式提供了相容条件：沿 $x$ 积分，与沿格点递推得到相同的空间导数。共同加上 $v_0(t)$ 对应辅助波函数的时间规范。

## 3. 一阶 Darboux 因子

定义

$$\alpha_j=\frac{U_j}2+\frac{hw_j}8,\qquad
\eta_j=\frac{U_j}2-\frac{hw_j}8,\qquad
A_j=\partial_x-\alpha_j,\qquad B_j=\partial_x-\eta_j.\tag{7}$$

由式（6），两个因子具有共同的中间热势：

$$V_j^F=V_j+2\partial_x\alpha_j
=V_{j+1}+2\partial_x\eta_j.\tag{8}$$

记 Riccati 残差

$$\begin{aligned}
\mathcal E_j^\alpha&=\partial_t\alpha_j+\partial_x^2\alpha_j
+2\alpha_j\partial_x\alpha_j+\partial_xV_j,\\
\mathcal E_j^\eta&=\partial_t\eta_j+\partial_x^2\eta_j
+2\eta_j\partial_x\eta_j+\partial_xV_{j+1}.
\end{aligned}\tag{9}$$

逐项展开得到

$$\begin{aligned}
\mathcal E_j^\alpha-\mathcal E_j^\eta
&=\frac h4\left[\partial_tw_j-\partial_x^2w_j+\partial_x(U_jw_j)\right],\\
\mathcal E_j^\alpha+\mathcal E_j^\eta&=S_j+2\partial_xV_j.
\end{aligned}\tag{10}$$

第一行由原方程的第二式为零，第二行由热势重构式（6）为零。因此两项残差均为零。

对任意函数 $r,V$，有算子恒等式

$$\begin{aligned}
&(\partial_t+\partial_x^2+V+2\partial_xr)(\partial_x-r)
-(\partial_x-r)(\partial_t+\partial_x^2+V)\\
&\hspace{2em}=-\left(\partial_tr+\partial_x^2r+2r\partial_xr+\partial_xV\right).
\end{aligned}\tag{11}$$

代入式（9），得到完整 Darboux 交织：

$$\begin{aligned}
(\partial_t+\partial_x^2+V_j^F)A_j
&=A_j(\partial_t+\partial_x^2+V_j),\\
(\partial_t+\partial_x^2+V_j^F)B_j
&=B_j(\partial_t+\partial_x^2+V_{j+1}).
\end{aligned}\tag{12}$$

这些恒等式作用于任意辅助函数，包含原方程的两项残差。

## 4. Lax 对

取热方程及格点传递方程：

$$\boxed{\begin{aligned}
\left(\partial_x-\frac{U_j}2+\frac{hw_j}8\right)\psi_{j+1}
&=\left(\partial_x-\frac{U_j}2-\frac{hw_j}8\right)\psi_j,\\
\partial_t\psi_j&=-\partial_x^2\psi_j-V_j\psi_j.
\end{aligned}}\tag{13}$$

热势由式（6）给出。这就是原半离散 DLW 的逐格点辅助线性对。

在形式伪微分算子代数中，首一因子 $B_j$ 具有按 $\partial_x$ 负次幂展开的形式逆。定义

$$\boxed{T_j=B_j^{-1}A_j,\qquad Q_j=-\partial_x^2-V_j.}\tag{14}$$

令 $Q_j^F=-\partial_x^2-V_j^F$。式（12）给出 $\partial_tA_j=Q_j^FA_j-A_jQ_j$ 和 $\partial_tB_j=Q_j^FB_j-B_jQ_{j+1}$。对 $T_j$ 求导，中间热算子消去：

$$\boxed{\partial_tT_j=Q_{j+1}T_j-T_jQ_j.}\tag{15}$$

式（15）表达了格点传递和时间演化的相容性。它由原物理方程经式（4）至式（12）导出。

## 5. 非退化支上的反向等价

反向推导取光滑场及满足势差 $V_{j+1}-V_j=(h/2)\partial_xw_j$ 的热势。保持这条势差关系，传递残差满足

$$B_j\left(\partial_tT_j-Q_{j+1}T_j+T_jQ_j\right)
=-\mathcal E_j^\alpha+\mathcal E_j^\eta T_j.\tag{16}$$

记 $g_j=hw_j/4$，则 $T_j=I-B_j^{-1}g_j$。若式（15）成立，便有

$$\mathcal E_j^\eta-\mathcal E_j^\alpha
=\mathcal E_j^\eta B_j^{-1}g_j.\tag{17}$$

比较两侧 $\partial_x^0$ 的系数，得到 $\mathcal E_j^\alpha=\mathcal E_j^\eta$；比较 $\partial_x^{-1}$ 的系数，得到 $\mathcal E_j^\eta g_j=0$。在

$$\boxed{w_j(x,t)\ne0\quad\text{对所有 }j,x,t\text{ 成立},\qquad
\text{即 }W_j(x,t)\ne4}\tag{18}$$

的状态域内，两项 Riccati 残差均为零。式（10）的第一行恢复原方程的第二式；第二行给出 $S_j+2\partial_xV_j=0$，结合势差恢复式（4），再恢复原方程的第一式。

因此，在势差关系和条件（18）下，逐格点 Lax 相容式与原半离散 DLW 等价。完整交织式（12）通过式（10）恢复两条物理方程，允许 $w_j=0$；条件（18）用于从传递商恢复两个因子残差。

## 6. 周期格点与条件

若格点首尾相接，热势闭合的条件是 $\partial_x\sum_{j=0}^{M-1}w_j=0$。当物理场同时在 $x$ 方向周期时，对原方程第一式求格点和，得到 $\partial_x^2\sum_jw_j=0$；空间周期性给出上述闭合条件。

若还要求热势在 $x$ 方向周期，式（5）的积分相容条件为 $\int_0^{L_x}S_j\,dx=0$，即 $\partial_t\int_0^{L_x}U_j\,dx=0$。原方程使各格点的这一时间导数相同。在共同空间平均不随时间变化的周期演化中，式（5）、（6）给出双周期热势。

格点热势闭合时，定义周期单值算子，得到

$$\boxed{\mathcal M=T_{M-1}\cdots T_0,\qquad
\partial_t\mathcal M=[Q_0,\mathcal M].}\tag{19}$$

这是式（15）沿格点环相乘的结果。辅助谱问题可取 $\psi_M=\mu\psi_0$，对应 $\mathcal M\psi_0=\mu\psi_0$。

| 表示或推导 | 条件 |
|---|---|
| 局部辅助线性对（13） | 光滑原方程解，$h>0$；热势由式（5）、（6）局部重构 |
| 完整 Darboux 交织（12） | 同一套热势与中间热势；允许 $w_j=0$ |
| 形式传递方程（15） | 在形式伪微分算子代数中求首一因子的逆 |
| 从传递相容式恢复原方程 | 势差关系；逐点 $w_j\ne0$，即 $W_j\ne4$ |
| 周期单值方程（19） | 物理场和热势在格点方向闭合 |
| 双周期热势 | 空间周期场；共同空间平均的时间导数为零 |

<footer><p>推导依据：<a href="../Workspaces/dlw_integrability_audit_20261002/LAX_AUDIT.md">完整 Darboux 恒等式与局部热势重构</a>；<a href="../Workspaces/dlw_conservation_hierarchy_20261004/lax/MONODROMY_POISSON_PROOF.md">周期传递与单值算子</a>。</p></footer>
