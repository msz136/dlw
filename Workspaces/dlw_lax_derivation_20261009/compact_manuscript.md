# 半离散 DLW 的 Lax 对

## 1. 原方程

设 $U_j(x,t)$ 和 $w_j(x,t)$ 为光滑实值场，其中 $x$ 是连续空间变量，$t$ 是时间，$j$ 是离散格点编号，$h>0$ 是格距。格点方向的后向差分与相邻平均分别定义为

$$\delta_-f_j=\frac{f_j-f_{j-1}}h,\qquad
M_-f_j=\frac{f_j+f_{j-1}}2.\tag{1}$$

考虑半离散 DLW 方程

$$\boxed{\begin{aligned}
\delta_-\!\left[\partial_tU+\partial_x\!\left(\frac{U^2}2+\frac{h^2w^2}{32}\right)\right]
+\partial_x^2(\delta_-U+M_-w)&=0,\\
\partial_tw+\partial_x(Uw)-\partial_x^2w&=0.
\end{aligned}}\tag{2}$$

## 2. 辅助势与所需条件

以下在局部空间区间和格点链上讨论。构造 Lax 对需要引入一个由物理场确定的辅助势 $V_j(x,t)$，它满足

$$\boxed{\begin{aligned}
\partial_xV_j&=-\frac12\left[\partial_tU_j+
\partial_x\!\left(\frac{U_j^2}2+\frac{h^2w_j^2}{32}\right)
+\partial_x^2U_j+\frac h2\partial_x^2w_j\right],\\
V_{j+1}-V_j&=\frac h2\partial_xw_j.
\end{aligned}}\tag{3}$$

具体地，先选一个参考格点，将第一式对 $x$ 积分，得到该格点的 $V_j$；再用第二式依次确定相邻格点的势。对第一式取格点差分、对第二式取 $x$ 导数，所得关系由原方程（2）的第一式保证一致。因此，每个光滑的原方程解都能局部构造出这样的辅助势。积分时留下的共同函数 $v_0(t)$ 可任意选取。

由原方程构造 Lax 对的过程允许 $w_j=0$。为进一步证明 Lax 相容条件与原方程等价，下面采用逐点非退化条件

$$\boxed{w_j(x,t)\ne0.}\tag{4}$$

该条件要求每个格点、每个所讨论的 $(x,t)$ 处都有 $w_j\ne0$。若使用原变量 $W_j=w_j+4$，它写成 $W_j\ne4$。

## 3. Lax 对

引入辅助函数 $\psi_j(x,t)$，取如下线性方程组：

$$\boxed{\begin{aligned}
\left(\partial_x-\frac{U_j}2+\frac{hw_j}8\right)\psi_{j+1}
&=\left(\partial_x-\frac{U_j}2-\frac{hw_j}8\right)\psi_j,\\
\partial_t\psi_j&=-\partial_x^2\psi_j-V_j\psi_j.
\end{aligned}}\tag{5}$$

第一行联系相邻格点上的辅助函数，第二行规定它随时间的演化；其中 $V_j$ 由式（3）确定。这两条线性方程组成所求的 Lax 对。

为写出相容条件，记

$$\alpha_j=\frac{U_j}2+\frac{hw_j}8,\quad
\eta_j=\frac{U_j}2-\frac{hw_j}8,\quad
A_j=\partial_x-\alpha_j,\quad B_j=\partial_x-\eta_j.\tag{6}$$

在形式伪微分算子代数中，$B_j$ 的最高阶系数为 $1$，其形式逆可按 $\partial_x$ 的负次幂逐阶展开。于是式（5）可写成 $\psi_{j+1}=T_j\psi_j$、$\partial_t\psi_j=Q_j\psi_j$，其中

$$T_j=B_j^{-1}A_j,\qquad Q_j=-\partial_x^2-V_j.\tag{7}$$

对格点传递式求时间导数，并分别代入相邻两格点的时间方程，得到

$$\begin{aligned}
\partial_t(T_j\psi_j)&=(\partial_tT_j+T_jQ_j)\psi_j,\\
\partial_t\psi_{j+1}&=Q_{j+1}T_j\psi_j.
\end{aligned}$$

由于 $\psi_{j+1}=T_j\psi_j$，要求两种计算在算子层面一致，便得到相容条件

$$\boxed{\partial_tT_j=Q_{j+1}T_j-T_jQ_j.}\tag{8}$$

## 4. 相容性与原方程的对应

先证明原方程推出相容条件。为检验两个一阶因子 $A_j$、$B_j$ 与时间演化的关系，定义

$$\begin{aligned}
\mathcal E_j^\alpha&=\partial_t\alpha_j+\partial_x^2\alpha_j
+2\alpha_j\partial_x\alpha_j+\partial_xV_j,\\
\mathcal E_j^\eta&=\partial_t\eta_j+\partial_x^2\eta_j
+2\eta_j\partial_x\eta_j+\partial_xV_{j+1}.
\end{aligned}\tag{9}$$

这两个表达式衡量一阶因子与热方程之间的相容误差。代入 $\alpha_j,\eta_j$ 的定义，并使用式（3）的势差关系，得到

$$\begin{aligned}
\mathcal E_j^\alpha-\mathcal E_j^\eta
&=\frac h4\left[\partial_tw_j-\partial_x^2w_j+\partial_x(U_jw_j)\right],\\
\mathcal E_j^\alpha+\mathcal E_j^\eta
&=\partial_tU_j+\partial_x\!\left(\frac{U_j^2}2+\frac{h^2w_j^2}{32}\right)
+\partial_x^2U_j+\frac h2\partial_x^2w_j+2\partial_xV_j.
\end{aligned}\tag{10}$$

式（10）的第一行正比于原方程的第二式，因而为零；第二行由辅助势的定义为零。所以 $\mathcal E_j^\alpha=\mathcal E_j^\eta=0$。

势差关系还给出共同的中间势 $V_j^F=V_j+2\partial_x\alpha_j=V_{j+1}+2\partial_x\eta_j$。下面的恒等式把上述残差与线性算子的相容性联系起来：

$$\begin{aligned}
&(\partial_t+\partial_x^2+V+2\partial_xr)(\partial_x-r)
-(\partial_x-r)(\partial_t+\partial_x^2+V)\\
&\hspace{2em}=-\left(\partial_tr+\partial_x^2r+2r\partial_xr+\partial_xV\right),
\end{aligned}\tag{11}$$

分别取 $r=\alpha_j$ 和 $r=\eta_j$，右侧均为零。于是 $A_j$ 将势为 $V_j$ 的热方程解变为势为 $V_j^F$ 的热方程解，$B_j$ 将势为 $V_{j+1}$ 的热方程解变为同一个中间热方程的解；这称为 Darboux 交织。

记 $Q_j^F=-\partial_x^2-V_j^F$，两条交织关系分别为 $\partial_tA_j=Q_j^FA_j-A_jQ_j$ 和 $\partial_tB_j=Q_j^FB_j-B_jQ_{j+1}$。将它们代入 $\partial_t(B_j^{-1}A_j)$，中间算子 $Q_j^F$ 的两项抵消，得到式（8）。这就证明了原方程保证线性方程组（5）相容。

再证明反向关系。此时取满足式（3）第二行势差关系的辅助势，并假设相容条件（8）成立。直接计算可得

$$B_j\left(\partial_tT_j-Q_{j+1}T_j+T_jQ_j\right)
=-\mathcal E_j^\alpha+\mathcal E_j^\eta T_j.\tag{12}$$

式（12）的左侧为零。利用 $T_j=I-B_j^{-1}hw_j/4$，比较右侧 $\partial_x^0$ 的系数，得到 $\mathcal E_j^\alpha=\mathcal E_j^\eta$；再比较 $\partial_x^{-1}$ 的系数，得到 $w_j\mathcal E_j^\eta=0$。由非退化条件（4），两项残差均为零。

最后，式（10）的第一行给出原方程的第二式；对第二行取格点后向差分，并使用辅助势的势差关系，便得到原方程的第一式。因此，在 $w_j\ne0$ 的状态域内，配合该势差关系，Lax 相容条件（8）与原半离散 DLW 方程（2）等价。
