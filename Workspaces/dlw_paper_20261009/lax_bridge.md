## 8　两种非线性形式的 Lax 表示

### 8.1　变量平移与辅助势

为统一记号，记 $U_j=u_j+2a$、$w_j=W_j-4=4\omega_j/h-4$。这里 $U$ 仅表示平移后的第一物理场，$V_j$ 则专指 Lax 辅助势，与第二物理场 $v_j$ 不同。SD 化为

$$\begin{aligned}
\delta_-\left[U_t+\partial_x\left(\frac{U^2}{2}+\frac{h^2w^2}{32}\right)\right]
+\partial_x^2(\delta_-U+M_-w)&=0,\\
w_t+\partial_x(Uw)-w_{xx}&=0.
\end{aligned}\tag{L1}$$

第一式通量的平移只增减与 $x$ 无关的常数。局部选取辅助势

$$\begin{aligned}
V_{j,x}&=-\frac12\left[U_{j,t}+\partial_x\left(\frac{U_j^2}{2}+\frac{h^2w_j^2}{32}\right)+U_{j,xx}+\frac h2w_{j,xx}\right],\\
V_{j+1}-V_j&=\frac h2w_{j,x}.
\end{aligned}\tag{L2}$$

对第一关系作格点差分，并对第二关系求 $x$ 导数，所得一致性条件正是（L1）的第一式。因此先在一个参考格点积分，再沿格点递推，即可为每个光滑解构造 $V$，其自由度为共同的时间函数。以下论证在局部空间区间和格点链上进行。

### 8.2　SD 的线性问题及相容性证明

取辅助函数 $\psi_j$，定义

$$\boxed{\begin{aligned}
\left(\partial_x-\frac{U_j}{2}+\frac{hw_j}{8}\right)\psi_{j+1}
&=\left(\partial_x-\frac{U_j}{2}-\frac{hw_j}{8}\right)\psi_j,\\
\psi_{j,t}&=-\psi_{j,xx}-V_j\psi_j.
\end{aligned}}\tag{L3}$$

**定理 8.1。** SD 的每个光滑解连同（L2）所确定的势都使（L3）在形式算子意义下相容。反之，在 $w_j\ne0$ 的区域内，相容条件与（L2）的势差关系共同推出（L1）。

**证明。** 置 $\alpha_j=U_j/2+hw_j/8$、$\eta_j=U_j/2-hw_j/8$，并令

$$A_j=\partial_x-\alpha_j,\quad B_j=\partial_x-\eta_j,\quad
T_j=B_j^{-1}A_j,\quad \mathscr Q_j=-\partial_x^2-V_j.\tag{L4}$$

$B_j^{-1}$ 在形式伪微分算子代数中定义。相容条件为

$$T_{j,t}=\mathscr Q_{j+1}T_j-T_j\mathscr Q_j.\tag{L5}$$

定义残差

$$\begin{aligned}
\mathcal E_j^\alpha&=\alpha_{j,t}+\alpha_{j,xx}+2\alpha_j\alpha_{j,x}+V_{j,x},\\
\mathcal E_j^\eta&=\eta_{j,t}+\eta_{j,xx}+2\eta_j\eta_{j,x}+V_{j+1,x}.
\end{aligned}\tag{L6}$$

利用势差关系，直接求得

$$\begin{aligned}
\mathcal E_j^\alpha-\mathcal E_j^\eta&=\frac h4[w_{j,t}-w_{j,xx}+(U_jw_j)_x],\\
\mathcal E_j^\alpha+\mathcal E_j^\eta&=U_{j,t}+\partial_x\left(\frac{U_j^2}{2}+\frac{h^2w_j^2}{32}\right)
+U_{j,xx}+\frac h2w_{j,xx}+2V_{j,x}.
\end{aligned}\tag{L7}$$

原方程和（L2）令两项残差均为零。另一方面，乘积法则给出 Darboux 恒等式

$$\begin{aligned}
&(\partial_t+\partial_x^2+V+2r_x)(\partial_x-r)
-(\partial_x-r)(\partial_t+\partial_x^2+V)\\
&\hspace{2em}=-(r_t+r_{xx}+2rr_x+V_x).
\end{aligned}\tag{L8}$$

分别取 $r=\alpha_j,\eta_j$，共同的中间势为 $V_j+2\alpha_{j,x}=V_{j+1}+2\eta_{j,x}$。两条交织关系代入 $T_{j,t}=(B_j^{-1}A_j)_t$，中间势抵消，即得（L5）。

反向证明只预设势差关系。恒等式

$$B_j(T_{j,t}-\mathscr Q_{j+1}T_j+T_j\mathscr Q_j)
=-\mathcal E_j^\alpha+\mathcal E_j^\eta T_j\tag{L9}$$

结合 $T_j=I-B_j^{-1}hw_j/4$，先比较 $\partial_x^0$ 系数，得 $\mathcal E_j^\alpha=\mathcal E_j^\eta$；再比较 $\partial_x^{-1}$ 系数，得 $w_j\mathcal E_j^\eta=0$。当 $w_j\ne0$ 时，两项残差为零。（L7）的差给出第二场方程，其和作后向格点差分后给出第一场方程。□

对于 τ 函数解，$V_j=2(\log G_j)_{xx}$ 是一个自然选择。此时

$$\alpha_j=\partial_x\log(F_j/G_j)+a-h/2,\qquad
\eta_j=\partial_x\log(F_j/G_{j+1})+a+h/2.\tag{L10}$$

两条半离散双线性方程分别保证相应 Riccati 残差为零，从而将 τ 函数构造与线性问题连接起来。这里得到的是局部 Darboux–Lax 相容表示；本文不以此替代全局谱理论或刘维尔可积性的独立证明。

### 8.3　SD2 的线性问题与规范

在 SD2 中，$U_j=2Q_{j,x}/Q_j+2a$、$w_j=-4Q_jR_j$，且可取 $V_j=2M_{j,x}$。于是（L3）成为

$$\boxed{\begin{aligned}
\left(\partial_x-\frac{Q_{j,x}}{Q_j}-a-\frac h2Q_jR_j\right)\psi_{j+1}
&=\left(\partial_x-\frac{Q_{j,x}}{Q_j}-a+\frac h2Q_jR_j\right)\psi_j,\\
\psi_{j,t}&=-\psi_{j,xx}-2M_{j,x}\psi_j.
\end{aligned}}\tag{L11}$$

约束 $M_{j+1}-M_j=h(1-Q_jR_j)$ 的 $x$ 导数恰好给出（L2）的势差关系。SD2 的两条演化方程则使（L6）为零，因而（L11）相容。在 $Q_jR_j\ne0$ 时，反向论证恢复 SD 的物理场方程。

SD2 还包含势变量的时间规范：物理场在 $Q_j\mapsto c_j(t)Q_j$、$R_j\mapsto c_j(t)^{-1}R_j$ 下不变。由物理场反向积分得到的 $Q$ 方程可含 $c_j'(t)/c_j(t)$ 型项；选择时间归一化将其消去，才得到第 7 节所写的 SD2。故两种表示的物理场对应是精确的，而势变量的反向对应须同时指定规范。
