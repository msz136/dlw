# 2A：固定横向切片的障碍与原结构下的椭圆行波 Liouville 约化

2026-10-13。本文给出一个闭合的最小正结果：在原半离散 DLW 的两格点周期平均叶上，构造显式二维不变辛流形，保留原 Poisson 结构与物理时间；其一个自由度具有真正的 action–angle 坐标，并且频率有非零 twist。它不等于一般二维场的 Liouville 完备性。

## 1. 为什么固定 y₀ 不是所需约化

### 命题 1：单个横向切片不决定其时间导数

连续原方程为

\[
 u_{yt}+v_{xx}+(uu_y)_x+2au_{xy}=0,
\quad
 v_t+(uv)_x+u_{xxy}+2av_x-4u_x=0.
\]

观察 \(y=y_0\) 的 \((u,v)\) 并未指定 \(u_y,u_{xxy}\) 或第一式沿 \(y\) 积分的自由度。退化扇区已经给出直接反例：任意与 \(y\) 无关的 \(u(x,t)\)，配 \(v\equiv4\)，都满足两式。因此同一初始切片可以拥有任意不同的 \(u_t\)。这个例子位于 \(w=v-u_y-4=0\) 扇区，不用它代替正则平均叶的审查。

在原半离散正则平均叶，反例同样存在。取 \(M=3,h>0,c\ne0,\gamma=0\)，周期 \(x\)，\(\beta=h^2/32\)。比较基态 \(p=s=0\) 与

\[
 p=(0,0,0),\qquad s=(0,f(x),-f(x)),\qquad\int f\,dx=0.
\]

两者具有同样的固定分量均值 Casimir；由
\(U=p-\Pi(ps)/c\)、\(w=c+s\)，它们在第 0 格点的完整物理初始切片都为
\(u_0=-2a,v_0=c+4\)。这里 \(v=w+\delta_0u+4\)，两组初始 \(U\) 都为零，所以额外 \(\delta_0u\) 不造成差别。

该叶的
\[
 R=\frac h6\begin{pmatrix}0&-1&1\\1&0&-1\\-1&1&0\end{pmatrix}.
\]
从原 Hamilton 方程直接计算，第二组在该时刻满足

\[
 \boxed{(U_0)_t=\frac h3f_{xx}+\frac{8\beta}3ff_x,}
\]

第一组则 \((U_0)_t=0\)。取 \(f=\sin x\)，在 \(x=\pi/2\) 得到 \((U_0)_t=-h/3\ne0\)。因此原物理 Hamilton 向量场不能投影为只依赖该切片的自治向量场。这个反例是代数层面的 projectability 障碍，不需要假定一般 Sobolev 初值问题适定；精确符号验证见 `verification.json`。

**Poisson 限定。** 动力不封闭并不意味着任何单站投影都没有 Poisson 意义。例如自由 \((p_j,s_j)\) 坐标的线性单站投影，可给柱状泛函继承常括号的一部分。但是原 Hamiltonian 不能因此下降为该切片上的 Hamiltonian，故这不是原系统的闭合 Hamilton 约化。连续 \(y\) 上的点值泛函还需处理 \(y\) 方向分布；不能直接将含 \(\delta(y-y')\) 的场括号在两处同时令 \(y=y_0\)。

即使一个横向约化已闭合，只要 \(x\) 仍连续且任意，所得相空间仍无限维。单取 \(M=2\) 或固定 \(y_0\) 不能完成有限维的 Liouville 计数。

## 2. 原场结构与最小周期横向模型

以下只使用项目已经建立的周期平均叶结构。令

\[
 \Pi w=c\ne0,\qquad \Pi(Uw)=\gamma,
\quad p=P_0U,\quad s=w-c,
\quad U=p+\frac{\gamma-\Pi(ps)}c.
\]

原 Poisson 算子为
\[
 J_{\mathrm{red}}=-\begin{pmatrix}0&P_0D\\P_0D&0\end{pmatrix},\qquad D=\partial_x,
\]
配对为 \(h\sum_j\int_0^L dx\)。\(x\) 分量均值是 Casimir。

取两格点周期 \(M=2\)，写
\(p_0=p,p_1=-p,s_0=s,s_1=-s\)。这一交替模态上 \(R=0\)。设 \(\gamma=0\)，固定
\(\int p\,dx=\int s\,dx=0\)。物理变量可明确恢复为

\[
 U_0=p-ps/c,\quad U_1=-p-ps/c,
\qquad w_0=c+s,\quad w_1=c-s.
\]

\(u_j=U_j-2a\)；由于两格点上 \(\delta_0=0\)，\(v_j=w_j+4\)。这给出原两场方程的真实解，未引入任意新的孤子参数括号。

令 \(\beta=h^2/32\)。从原物理 Hamiltonian 只减去常背景
\(2h\beta c^3L/3\)，得到

\[
 \boxed{H=2h\int_0^L\kappa\,dx,\qquad
 \kappa=\frac c2p^2-\frac{p^2s^2}{2c}+\beta c s^2+s p_x.}
 \tag{1}
\]

原平移动量为
\[
 P=2h\int_0^Lps\,dx.\tag{2}
\]

以普通 \(\int dx\) 泛函导数书写，标量物理括号是
\(J_0/(2h)\)，其中
\[
 J_0=-\begin{pmatrix}0&D\\D&0\end{pmatrix}.
\]
等价地，用 \(J_0\) 和 \(H/(2h)\) 生成同一个物理时间流。以下记号 \(\kappa_p,\kappa_s\) 始终表示密度的 Euler–Lagrange 变分导数，而非忽略导数项的普通偏导：

\[
 \kappa_p:=\frac{\partial\kappa}{\partial p}
       -D\frac{\partial\kappa}{\partial p_x}
       =cp-ps^2/c-s_x,
 \qquad
 \kappa_s:=\frac{\partial\kappa}{\partial s}
       -D\frac{\partial\kappa}{\partial s_x}
       =-p^2s/c+2\beta c s+p_x.
\]

其完整方程是

\[
 p_t=-D\left[-p^2s/c+2\beta c s+p_x\right],
\quad
 s_t=-D\left[cp-ps^2/c-s_x\right].\tag{3}
\]

原动量生成负向 \(x\) 平移：\(X_P=-(p_x,s_x)\)。

## 3. 显式椭圆行波族

记

\[
 q=|hc|/4=\sqrt{2\beta c^2},\qquad k_0=2\pi/L,
 \qquad 0<k_0<q.
\]

\(\mathbf K(m)\) 为参数 \(m\) 的第一类完全椭圆积分。取 \(0<m<1\)，定义

\[
 b(m)=\frac{4\mathbf K(m)}L,\qquad A(m)=\sqrt m\,b(m),
\]
\[
 \nu(m)=\frac{\sigma}{q}
 \sqrt{(q^2-A(m)^2)(q^2-b(m)^2)},
 \qquad\sigma\in\{+1,-1\}.\tag{4}
\]

限制到 \(b(m)<q\) 的分支；此时 \(A<b<q\) 且 \(\nu\ne0\)。设 \(\phi\in\mathbb R/L\mathbb Z\)，\(\xi=x-\phi\)，并令

\[
 \boxed{
 p(x;m,\phi)=A\,\operatorname{sn}(b\xi\mid m),
 \qquad
 s(x;m,\phi)=c\frac{p_x-\nu p}{p^2-q^2}.}
 \tag{5}
\]

分母不为零。两函数的周期均为 \(L\)，且满足
\(p(x+L/2)=-p(x),s(x+L/2)=-s(x)\)，所以它们自动位于同一个零分量均值辛叶。

### 命题 2：式 (5) 是原物理时间流的不变族

取 \(m\) 恒定、\(\phi(t)=\phi_0+\nu(m)t\)，则式 (5) 经上述物理重构满足原半离散 DLW 两式，且对全部实时间光滑存在。

**证明。** Jacobi 恒等式给出

\[
 p_x^2=(A^2-p^2)(b^2-p^2),\qquad
 p_{xx}=2p^3-(A^2+b^2)p.\tag{6}
\]

由式 (4) 的速度关系
\(\nu^2=(q^2-A^2)(q^2-b^2)/q^2\)，将式 (5) 微分并利用式 (6)，直接得到

\[
 p_x=\nu p+(p^2/c-2\beta c)s,
\qquad
 s_x=cp-\nu s-ps^2/c.\tag{7}
\]

因此 \(\kappa_s=\nu p\)、\(\kappa_p=\nu s\)，代入式 (3) 得到
\((p_t,s_t)=-\nu(p_x,s_x)\)，正是所述相位演化。已知周期平均闭合与原两场方程双向等价，故重构给原方程解。或者将重构直接代回原两式，亦得到零。分母与椭圆实函数在整个相位圆上保持正则，刚性平移给出全部实时间存在。证毕。

式 (7) 的**空间轮廓**还拥有另一个二维 Hamilton 描述；此处 \(G_p,G_s\) 是有限维函数的普通偏导：

\[
 G(p,s)=\nu ps+(p^2/(2c)-\beta c)s^2-cp^2/2,
 \qquad p_x=G_s,\quad s_x=-G_p.\tag{8}
\]

在式 (5) 上
\(G=-cA^2b^2/(2q^2)\)。这条空间 Hamilton 结构用来构造轮廓；它本身不证明原物理时间的 Liouville 可积性。后者须由下一节原场辛形式的继承完成。轮廓曲线 \(r^2=(A^2-p^2)(b^2-p^2)\) 的四个分支点互异，作为复曲线具有 genus one；本文没有将其等同于原 Lax 算子的谱曲线。

## 4. 原场辛形式的继承

在固定零分量均值叶上，\(D_0^{-1}\) 是周期零均值原函数。本文采用
\(\iota_{X_F}\omega=dF\)、\(\{F,G\}=dF(X_G)\) 约定，故标准式为 \(dQ\wedge dP\)。原场弱辛形式是

\[
 \omega(v,w)=2h\langle J_0^{-1}v,w\rangle
 =-2h\int_0^L\big[(D_0^{-1}v_s)w_p
                         +(D_0^{-1}v_p)w_s\big]dx.\tag{9}
\]

若采用矩阵 \(B^{-1}\) 对应的相反二形式，并以 \(\iota_X\Omega=-dH\) 定义 Hamilton 场，则 \(\Omega=-\omega\)；两种约定给出完全相同的物理向量场和坐标 Poisson 括号。此处不把整体符号差当作结构差异。

记式 (5) 的参数映射为 \(\iota:(m,\phi)\mapsto(p,s)\)。由于 \(\partial_\phi\iota=X_P\)，有

\[
 (\iota^*\omega)(\partial_\phi,\partial_m)=\frac{dP(m)}{dm}.
\]

参数面只有二维，因此

\[
 \boxed{\iota^*\omega=d\phi\wedge dP(m).}\tag{10}
\]

这直接来自原 \(D^{-1}\) 辛形式；不是先在参数平面指定方便括号后宣称继承。只要 \(P'(m)\ne0\)，它闭且非退化，所以参数像是原场辛叶中的二维辛子流形。结合物理流切向性，\(H\) 的限制就是该流形上原物理时间的 Hamiltonian。这里不声称包含映射对任意 ambient 泛函都是 Poisson 映射；使用的是确切的辛形式拉回与切向 Hamilton 流。

动量可以精确求出。式 (5) 给

\[
 ps=c\frac{pp_x}{p^2-q^2}
       +c\nu\frac{p^2}{q^2-p^2}.
\]

第一项是周期全导数。令 \(n=A^2/q^2\)，\(\mathbf\Pi(n\mid m)\) 为第三类完全椭圆积分，得到

\[
 \boxed{P(m)=\frac{8hc\nu(m)}{b(m)}
             [\mathbf\Pi(A(m)^2/q^2\mid m)-\mathbf K(m)].}\tag{11}
\]

\(\mathbf K(m)=\frac\pi2(1+m/4+O(m^2))\) 给出

\[
 P(m)=\frac{hcL\nu_0k_0^2}{q^2}\,m+O(m^2),
 \qquad \nu_0=\sigma\sqrt{q^2-k_0^2}.\tag{12}
\]

系数非零，故存在 \(m_*>0\)，使 \(0<m<m_*\) 为非退化辛环域。\(A(m)\) 严格递增，且每个非零轮廓具有最小周期 \(L\)，所以参数像无振幅重叠或额外相位识别。式 (10) 也直接保证浸入性。

### 一个全部常数明确的正则区间

可以取

\[
 \boxed{c=-4,\quad h=2,\quad L=2\pi,\quad \gamma=0,
 \quad 0<m<1/20,\quad \sigma=+1.}\tag{13}
\]

此时 \(q=2,k_0=1\)。不仅存在某个未知的小邻域，而且整个所列区间都有 \(P'(m)<0\)。证明如下。

令 \(J(m)=\int_0^L p^2/(q^2-p^2)\,dx>0\)，则 \(P=2hc\nu J\)。由

\[
 J=\frac4b\int_0^{\pi/2}
 \frac{n\sin^2\theta}{1-n\sin^2\theta}
 \frac{d\theta}{\sqrt{1-m\sin^2\theta}},
 \quad n=mb^2/4,
\]

对正被积函数取对数导数，得到
\[
 J'/J\ge-b'/b+n'/n=1/m+b'/b>1/m\ge20.
\]

另一方面，\(\mathbf K'/\mathbf K\le[2(1-m)]^{-1}\)，所以在 \(m\le1/20\)

\[
 b^2\le20/19,\quad A^2\le1/19,
 \quad (b^2)',(A^2)'\le400/361.
\]

由速度式

\[
 |\nu'/\nu|
 \le\frac12\frac{400}{361}
      \left(\frac{19}{75}+\frac{19}{56}\right)
 =\frac{131}{399}<1.
\]

因此 \((\nu J)'/\nu J>19\)，而 \(2hc<0\)，故 \(P'<0\)。此外 \(A<1/4,b<2,\nu<2\)，由式 (5) 得 \(|s|<4/3<|c|\)，故 \(w_0,w_1\) 都不经过零；\(|p|<1/4\) 也避开既有两格点 Miura 图的 \(p=\pm2\eta\) 奇点。上述区间是解析不等式证明，不依赖浮点抽样的符号。

## 5. Liouville 定理与 action–angle

### 定理 3：原物理结构下的一个自由度 Liouville 辛环域

在第 4 节任意 \(P'(m)\ne0\) 的分支上，特别是式 (13)，式 (5) 定义原半离散 DLW 的二维不变辛流形。其物理时间系统具有一个微分独立的积分 \(P\)，并且 \(H=H(P)\)、\(H'(P)=\nu(P)\ne0\)。因此它是一个自由度的 Liouville 可积系统。

**证明。** 非退化性与原结构继承已由式 (9)–(12) 证明。每个泛函对参数面的任意切向变分满足

\[
 dH=2h\int(\kappa_p\,dp+\kappa_s\,ds)
    =2h\nu\int(s\,dp+p\,ds)=\nu\,dP,\tag{14}
\]

其中用了式 (7)。\(P'\ne0\) 保证 \(dP\ne0\)，\(\nu\ne0\) 保证 \(dH\ne0\)。二维辛流形只需一个独立积分；\(\{P,P\}=0\)，也有 \(\{P,H\}=0\)。物理向量场为 \(\dot m=0,\dot\phi=\nu(m)\)，其正则积分叶是紧相位圆。证毕。

标准角与 action 为

\[
 \boxed{\theta=k_0\phi\pmod{2\pi},\qquad
 I=P/k_0=\frac{L}{2\pi}P,
 \qquad \omega=d\theta\wedge dI,\quad\{\theta,I\}=1.}\tag{15}
\]

相应

\[
 \dot I=0,\qquad \dot\theta=\Omega(I)=k_0\nu(I).
\]

这是有向 action；若希望所选分支的 action 为正，可同时反转角与 action 的方向。零振幅 \(m=0\) 时相位圆塌缩，本文的角坐标只定义在 \(m>0\) 辛环域，不声称它在塌缩点仍是 Darboux 坐标。

所有平移不变的原谱量在这个流形上只依赖 \(m\)，因而局部都是 \(P\) 的函数；其两两对合继承成立，但不能将这些函数计算为多个独立积分。尤其 \(H,P,I_1,I_2,\ldots\) 在这里的独立数量至多为一。

### 非零 twist 与严格可计算的相位误差

继续展开式 (4)、(12)，得到

\[
 \nu'_m(0)=-\frac{k_0^2(3q^2-2k_0^2)}{4q^2\nu_0},
\]
\[
 \boxed{\lim_{m\downarrow0}\frac{d\Omega}{dI}
 =-\frac{k_0^2(3q^2-2k_0^2)}
 {4hcL(q^2-k_0^2)}\ne0.}\tag{16}
\]

式 (13) 的极限为 \(5/(96\pi)\)。所以这不是等时圆周运动族。对两条**同一辛环域内的精确轨道**，

\[
 \Delta I(t)=\Delta I(0),\qquad
 \Delta\theta(t)=\Delta\theta(0)
       +[\Omega(I_2)-\Omega(I_1)]t.
\]

在任意紧子环域上，\(|\Delta\theta(t)|\le|\Delta\theta(0)|+
\sup|\Omega'|\,|\Delta I(0)|\,|t|\)，这里采用连续提升的角。这个结论说明守恒的 action 误差仍可产生线性增长的相位误差。它不自动适用于离开此不变流形的任意数值轨道。

## 6. 谱接口与未完成处

沿任意平移波，原 Lax 算子满足 \(L_t=-\nu L_x\)。结合原
\(L_t=[-D^2-V,L]\) 与 \(L_x=[D,L]\)，得到

\[
 [-D^2-V+\nu D,L]=0.
\]

这给出后续谱几何工作可直接使用的定常层级约束。但本文未构造上述椭圆族的完整 Bloch 曲线、未证明轮廓四次曲线与 Lax 谱曲线同构，也未证明任意有限隙谱数据都能反向落入原场实辛叶。

本约化的价值在于原场继承、固定均值、显式周期族、真实物理时间和可计算非等时性全部闭合。其限度同样明确：只有一个自由度，尚不足以体现多自由度积分的非平凡对合与完备性。下一步应优先追求一个四维原结构不变辛流形或明确的两有效隙约化，而不是将本环域的同一个积分重复计数。

此外这是两格点交替横向模态，存在条件 \(2\pi/L<|hc|/4\)。若固定 \(L,c,M=2\) 后令 \(h\to0\)，该条件失效；同时横向周期 \(2h\) 被压缩。因此不能把本例写成固定二维物理区域下连续 DLW 的一般有限维约化。保持 \(L\sim h^{-1}\) 的长波缩放是另一个问题。

## 7. 验证记录

`verify_reduction.py` 精确核验式 (7)、空间 Hamilton 能级、\(\delta H=\nu\delta P\)、动量全导数分解、正则切片反例及 twist 代数。全部符号残差为零。`verification.json` 与 `elliptic_family_checks.csv` 另给式 (13) 内五个实际椭圆波的数值代回与辛形式配对：

- 原两式的 Fourier 代回残差最大约 \(1.1\times10^{-10}\)；
- 椭圆积分动量公式与直接周期求积差小于 \(3.5\times10^{-14}\)；
- 原辛形式配对与 \(P'_m\) 的独立五点微分差约 \(10^{-11}\)；
- \(H'_m-\nu P'_m\) 最大约 \(2.2\times10^{-11}\)；
- 例中 \(d\Omega/dI\) 从 0.016577 平滑变到 0.016538，吻合非零极限。

这些浮点结果核验实现与符号，不承担存在性或非退化性的证明；后两者已有上面的解析证明。运行：`python Workspaces/dlw_stage2_20261013/reduction/verify_reduction.py`。只使用已有 SymPy、NumPy、SciPy。

原结构依据：[一般场两格点 Poisson 铅笔](../../dlw_general_field_20261006/TWO_SITE_POISSON_PENCIL.md)、[原非线性闭合](../../dlw_semidiscrete/NONLINEAR_CLOSURE.md)、[第一阶段括号推导](../../dlw_three_tracks_20261013/poisson/report.md)。本阶段未改写既有一般场 action–angle 工作。
