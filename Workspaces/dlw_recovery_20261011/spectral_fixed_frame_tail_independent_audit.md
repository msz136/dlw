# M=2 固定背景 framed 采样尾部：独立审查

2026-10-11。独立核对 `spectral_independent_review_20261011.md` §7.3、§11 及 `spectral_fixed_frame_tail_checks_20261011.py/.json`，未重新运行原有数值证书。以下只审查非线性 monodromy 采样及其函数空间；不宣称 nonlinear inverse spectral theorem 或原场 Liouville 完备性。

结论：主稿 (48)、(50) 的系数、相位及 Sobolev 端点成立。有限阶 periodic Laurent gauge 给出严格余项；本例换回原始 rank-one 固定背景框架后，采样逐 k 完全相同。另有一个更强但须区分框架的结论：一般基点值变化时，原始固定背景框架产生非零常数阶的 c 通道尾部，按同一物理线性归一化得到 k^{-3/2} 尾部。因此单纯改用不含高阶 jet 的原始系统，并不解决固定框架的序列空间问题。

## 1. 场、均值叶及 scalar pencil

取 L=2π、B=0、S=2δ、0<δ<1/2。一般 free 场写成

\[
q=-S+u,\qquad d_0=\delta+v,\qquad d_1=\delta-v,
\qquad \int u=\int v=0.
\]

由精确物理闭合公式

\[
b_1=-d_0u/S,\qquad b_0=b_1+u
\]

可得 b_0−b_1=u，且 b_0d_0+b_1d_1=0。故固定 q,d 的分量均值等价于固定源 Poisson 叶的相应均值；共同 b 均值不是另加的 Casimir。主稿例 u=v=ε sin x 满足这些条件，并且 b_0,b_1 为有限 Fourier 多项式。

M=2 split 系统确为

\[
\phi_x=\lambda\phi+q\xi,\qquad
\xi_x=r\phi+V\xi,
\]

\[
r=\frac{d_0(S-d_0)(2+q/S)-d_{0,x}}S,
\qquad V=-\frac{2uv}{S}.
\]

q 无零点时，消去 ξ 得

\[
A_\lambda=D^2-(\lambda+W)D+\lambda W-qr,
\qquad W=V+q_x/q.
\]

这是同一 φ 的 jet 系统，不是额外引入的 scalar 模型。一般 u,v 下还有精确恒等式

\[
qr+\delta^2
=v^2+(\delta^2-v^2)u^2/S^2+(1-u/S)v_x.\tag{A1}
\]

sin 例给出

\[
V=-2\varepsilon^2\sin^2x/S,\quad
m_\infty=e^{\int V}=e^{-\varepsilon^2L/S},\quad
W(0)=-\varepsilon/S,\quad qr(0)+\delta^2=\varepsilon.
\]

## 2. 有限阶 gauge 足以给出严格渐近式

设 q,r,V 为固定光滑周期函数，q 无零点。对

\[
A=\begin{pmatrix}\lambda&q\\r&V\end{pmatrix}
\]

构造 periodic 有限 Laurent 矩阵

\[
U_N=\begin{pmatrix}1&a_N\\b_N&1\end{pmatrix}.
\]

其两列分别对应 fast、slow 方向。逐阶匹配以下 Riccati 残差即可：

\[
\lambda b=r+Vb-b_x-qb^2,\qquad
\lambda a=-q+Va+a_x+ra^2.\tag{A2}
\]

其中

\[
b_N=r/\lambda+O(\lambda^{-2}),\qquad
a_N=-q/\lambda-(q_x+Vq)/\lambda^2+O(\lambda^{-3}).
\]

令有限残差为 O(|λ|^{-N})。U_N、U_N^{-1} 一致有界，变换后的系统为

\[
\operatorname{diag}(\lambda+qb_N,V+ra_N)+O(|\lambda|^{-N}).
\]

在纯虚 λ 上，两个对角演化及其逆均一致有界：fast 的 λ 部分模长为 1，剩余系数在固定区间上有界。Duhamel 公式因此给出 monodromy 的 O(|λ|^{-N}) 误差，不需要无限 formal gauge 收敛。

固定背景本征基在 split 坐标中，其矩阵范数 O(k)、逆矩阵范数 O(1)；故最终 framed 误差至多放大 O(k)。取 N≥4 即可使误差不超过 O(k^{-3})。在一个 q 保持无零点、半径有界的 C^R 复球上，R≥10 足以统一全部递推和误差常数。

## 3. 双通道的系数与相位

设 λ_+=i√(k²−4δ²)，Δ=ik，z_s=(λ_+−ik)/2、z_f=z_s+ik。取背景 companion frame

\[
E_0=\begin{pmatrix}1&1\\z_s&z_f\end{pmatrix}.
\]

将 gauge 的列转为 scalar jet 并把第一分量归一为 1，实际 slow、fast 斜率分别是

\[
h_s=W(0)+O(\lambda^{-1}),\qquad
h_f=\lambda+qr(0)/\lambda+O(\lambda^{-2}).
\]

实际列到背景列的转换矩阵可写成

\[
K=\begin{pmatrix}1-\alpha&\beta\\\alpha&1-\beta\end{pmatrix},
\quad
\alpha=\frac{h_s-z_s}{\Delta}
=\frac{W(0)}\lambda+O(\lambda^{-2}),
\]

\[
\beta=\frac{z_f-h_f}{\Delta}
=-\frac{qr(0)+\delta^2}{\lambda^2}+O(\lambda^{-3}).
\]

对应传输因子为

\[
M_s=m_\infty(1+O(\lambda^{-1})),\qquad
M_f=e^{\lambda L}(1+O(\lambda^{-1})).
\]

K diag(M_s,M_f) K^{-1} 的 fs 元素等于

\[
\frac{\alpha(1-\beta)}{1-\alpha-\beta}(M_s-M_f).
\]

背景共振序列上 e^{λ_+L}=1+O(k^{-1})、e^{z_sL}=1+O(k^{-1})，因此

\[
c_{+,k}^{\rm raw}
=\frac{W(0)(m_\infty-1)}{\lambda_+}+O(k^{-2}).\tag{A3}
\]

另一通道在 λ_−=−λ_+，背景列依次为 fast、slow。其 row slow / column fast 混合系数为 −(qr(0)+δ²)/λ_−²，乘 (M_f−M_s) 后得到

\[
c_{-,k}^{\rm raw}
=\frac{(qr(0)+\delta^2)(m_\infty-1)}{\lambda_-^2}
+O(k^{-3}).\tag{A4}
\]

此处加号及 λ_−² 均重要。实型共轭对应 λ_+ 上的 reverse 上三角通道。

## 4. 物理线性归一化与发散端点

按主稿 (26)，τ=√(k²/4−δ²)、|K|=Lkτ/(8S)，所以

\[
Q=k^{-1/2}c_+/\sqrt{|K|},\qquad
P=k^{1/2}\overline{c_-}/\sqrt{|K|}.
\]

记 C=W(0)(m_∞−1)、D_0=(qr(0)+δ²)(m_∞−1)，则

\[
Q_k^{\rm raw}=-i\sqrt{16S/L}\,C k^{-5/2}+O(k^{-7/2}),
\]

\[
P_k^{\rm raw}=-\sqrt{16S/L}\,D_0 k^{-5/2}+O(k^{-7/2}).\tag{A5}
\]

sin 例 C=ε³L/S²+O(ε⁵) 非零。h^{s+1/2} 的 Q 项下界给出 Σ k^{2s−4}，于 s=3/2 为 Σ k^{-1}。于是该光滑、可任意接近背景的物理场不落入目标序列空间，只靠背景线性导数同构不能在 s≥3/2 直接应用 Banach 逆函数定理。

现有 JSON 的 λc_+ 结果趋于 C=0.002430430481717885；k=160 的相对误差为 0.0027991229。数值与公式一致；严格结论由 (A2)–(A5) 支持。

## 5. sin 例回到原始 fixed frame，采样完全不变

原始 rank-one χ 系统到 split 系统的矩阵为

\[
T(d_0)=\begin{pmatrix}d_0/S&1\\1-d_0/S&-1\end{pmatrix},
\]

split 到 companion 的端点矩阵为

\[
G(q_0,\lambda)=\begin{pmatrix}1&0\\\lambda&q_0\end{pmatrix}.
\]

两者都是周期 gauge，故只按其基点值共轭 monodromy。sin 例在 x=0 满足 d_0=δ、q_0=−S、b_0=b_1=0，两个端点矩阵均等于背景。若原始固定背景 frame 定义为

\[
F_{\chi,0}=T(\delta)G(-S,\lambda)^{-1}E_0,
\]

则精确有

\[
F_{\chi,0}^{-1}\mathsf T_\chi F_{\chi,0}
=E_0^{-1}\mathsf T_{\rm companion}E_0.
\tag{A6}
\]

因此不含 high jet 的原始系统仍保留同一尾部；它不是 companion 转换的人为伪影。

## 6. 一般基点变化时，原始固定背景框架的尾部更慢

这项结论只针对 (A6) 所指定的原始背景 frame 和同一 (26) 归一化，须与 state-adapted companion frame 区分。记 u_0=u(0)、v_0=v(0)、q_0=−S+u_0，则精确端点转换为

\[
G(-S,\lambda)T(\delta)^{-1}T(d_0)
G(q_0,\lambda)^{-1}
=\begin{pmatrix}
1&0\\\lambda u_0/q_0-v_0&-S/q_0
\end{pmatrix}.\tag{A7}
\]

作用到实际 scalar slow 列后，其斜率为 λu_0/q_0+O(1)；fast 列斜率为 λ+O(1)。于是相对于 E_0 的 α=u_0/q_0+O(k^{-1})、β=O(k^{-1})、1−α−β=−S/q_0+O(k^{-1})。同一 monodromy 计算给出

\[
c_{+,k}^{\chi,\rm fixed}
=-\frac{u_0}{S}(m_\infty-1)+O(k^{-1}).\tag{A8}
\]

例如 u=v=ε cos x 是同一均值叶内的光滑场，u_0=ε、m_∞=e^{−ε²L/S}，首项非零。于是

\[
Q_k^{\chi,\rm fixed}
=\sqrt{16S/L}\left[-\frac{\varepsilon}{S}(m_\infty-1)\right]
k^{-3/2}+O(k^{-5/2}).
\]

目标范数对应 Σ k^{2s−2}，在 s≥1/2 发散。这排除了未经端点调整的原始固定背景采样在通常 H^s、s>1/2 上直接给出目标 h^{s+1/2} 图。它不排除 state-adapted frame 或其他 renormalized 坐标。

## 7. 可严格成立的有限正则性解析 lemma

在上述 q 无零点的 C^R 小复球、R≥10 中，(A3)–(A5) 的常数一致。因此 companion raw 采样给出真实解析映射 C^R→h^t，t<2；同时从两个 c 通道分别减去 (A3)、(A4) 的显示首项后，(Q_ren,P_ren)=O(k^{-7/2})，给出真实解析映射 C^R→h^t，t<3。

证明：每个有限 monodromy 坐标由参数依赖 ODE 得到，具有复解析依赖；统一尾估计使有限序列投影在 h^t 中局部一致收敛。对 P 的复化应使用 λ_+ 上的 reverse 采样，不能把场变量的复共轭误称为 holomorphic；该 reverse 采样在实场上恰等于 bar(c_−)。局部一致极限及 Cauchy 估计给出目标空间中的解析性。

由于 V=−2uv/S，m_∞−1 从二阶开始，而 W(0) 及 qr(0)+δ² 从一阶开始；减去的边界项从三阶开始，保留背景第一、第二 jet。这是 open C^R source 到较低序列空间的实际非线性 lemma。它不提供同阶 H^s→h^{s+1/2} 的导数同构和 C¹ 余项，不能据此使用 IFT。

companion raw 在 1/2<s<3/2 的同阶 Sobolev 图仍未证实，也未被 sin 例排除。低阶导数的点值在该区间不连续，并不能单独构成反证：尾部渐近阈值会随源高频变化，需要统一序列估计才能判断。原始 fixed frame 的 (A8) 则已给出这个区间内的独立硬障碍。

补充验证：本次另用 SymPy 精确核对 (A7) 的端点矩阵乘积和 K diag(M_s,M_f) K^{-1} 的 fs 恒等式，均通过，进程退出码 0。未重新运行 monodromy 数值积分，也未改动主稿或共享记录。
