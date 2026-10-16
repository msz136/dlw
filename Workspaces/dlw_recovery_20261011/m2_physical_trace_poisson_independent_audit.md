# M2 固定物理谱参数的 Poisson–AKNS 桥：独立审计

2026-10-11。已实际读取 [AKNS 状态逆桥](akns_physical_state_inverse_bridge_20261011.md)，特别是 §4.2–4.5。下面重新核对 source gradient、holonomy、\(b_t\) 和 gauge section。所有 bracket 使用双线性积分；实型由复共轭限制取得。

## 1. 约定与精确结论

本稿使用

\[
\mathcal L_\zeta=\frac\zeta2H+aE_{12}+bE_{21},\qquad
\zeta=\lambda-\eta,
\]
\[
q=u-S,\quad A=\frac14-\frac{v^2}{S^2},\quad
r=A(S+u)-\frac{v_x}{S},\quad
V=-\frac{2uv}{S},\quad
\eta=\langle V\rangle,\quad\theta=KV,\quad
a=e^\theta q,\quad b=e^{-\theta}r.
\tag{1}
\]

\(K=D_0^{-1}P_0\) 是平均零周期 primitive，\(\langle f\rangle=L^{-1}\int f\)，\(S\ne0\)。此处 \(\zeta\) 是状态逆桥 §4 中写作 \((\lambda-\eta)/2\) 的变量的 **两倍**；dimensionless KLTZ 参数为 \(z=iL\zeta/2\)。

令 \(\mathcal T_\zeta(a,b)\) 为实际 AKNS monodromy trace。原物理迹为
\(\mathcal F_\lambda(u,v)=\mathcal T_{\lambda-\eta}(a,b)\)。
下文 \(\mathfrak A(u,v)=(a,b)\) 表示完整势映射，区别于状态逆桥 (5) 的 projected map \(\Phi=(P_0a,P_0b)\)。
其固定物理参数 \(\lambda\) 的 Hamilton 场，在
\(J_{uv}=-\mathrm{swap}\,D/16\) 下，准确推为

\[
\boxed{\begin{aligned}
a_t&=\frac{S^2-\lambda^2}{16S}\,e
-\frac{\langle R_0\rangle}{8S}\,a,\\
b_t&=-\frac{S^2-\lambda^2}{16S}\,f
+\frac{\langle R_0\rangle}{8S}\,b .
\end{aligned}}
\tag{2}
\]

其中 \(e,f\) 是 §2 的实际 periodic adjoint entries，\(R_0\) 见 (11)。
所以在常数 diagonal gauge 的商中，physical trace flow 是
\[
w_\lambda X_{\mathcal T_\zeta}^{\rm can},\qquad
w_\lambda=\frac{S^2-\lambda^2}{16S},\qquad
X_{\mathcal T_\zeta}^{\rm can}=(e,-f).
\tag{3}
\]

这里的 canonical bracket 为 \(x\)-周期势上的
\(J_{\rm can}=\left(\begin{smallmatrix}0&1\\-1&0\end{smallmatrix}\right)\)。
这是一族 **actual trace 场的精确桥**，不声称完整推前张量等于一个 scalar 倍的 canonical 张量。状态逆桥 §3 的二阶、含 nonlocal 项的准确推前保持有效。

## 2. 实际 adjoint 变量与 source frame

取 \(Y_x=\mathcal L_\zeta Y,\ Y(0)=I,\ N=Y(L)\)，并令

\[
W(x)=Y(x)\left(N-\tfrac12\operatorname{tr}N\,I\right)Y(x)^{-1}
=\begin{pmatrix}h&e\\f&-h\end{pmatrix}.
\tag{4}
\]

\(W\) 光滑周期，\(W_x=[\mathcal L_\zeta,W]\)，故

\[
h_x=af-be,\quad
e_x=\zeta e-2ah,\quad
f_x=-\zeta f+2bh.
\tag{5}
\]

实际 Duhamel 变分给

\[
d\mathcal T_\zeta=\int(f\,da+e\,db)\,dx
\quad\text{在固定 }\zeta,\qquad
\partial_\zeta\mathcal T_\zeta=\int h\,dx=L\langle h\rangle.
\tag{6}
\]

设
\[
F=e^\theta f,\qquad E=e^{-\theta}e .
\]
这些大写 \(E,F\) 是 scalar adjoint entries，与迹泛函 \(\mathcal F\) 区分。由 \(\theta_x=V-\eta\) 得

\[
h_x=qF-rE,\qquad
F_x=(V-\lambda)F+2rh,\qquad
E_x=(\lambda-V)E-2qh.
\tag{7}
\]

特别是 \(\eta\) 在该闭合系统中完全抵消。这里的 scalar spectral coefficient 是 \(\lambda\)，没有多一个因子 2。

## 3. 固定 \(\lambda\) 的 holonomy 变分精确消去零模

写
\[
B=-\frac{2v(S+u)}{S^2},\qquad
\delta r=A\delta u+B\delta v-\frac{D\delta v}{S},\qquad
\delta V=-\frac2S(v\delta u+u\delta v).
\]

由 (1) 并在周期积分中对 \(D\delta v\) 分部积分，
\[
\int(f\delta a+e\delta b)\,dx
=\int\left((F+AE)\delta u+(BE+E_x/S)\delta v
+(qF-rE)\delta\theta\right)dx.
\tag{8}
\]

最后一项需保留 primitive 的零模。用 \(qF-rE=h_x\)、
\(\delta\theta=K\delta V\)，周期分部积分给

\[
\int h_xK\delta V\,dx
=-\int(h-\langle h\rangle)\delta V\,dx.
\tag{9}
\]

另一方面，固定物理 \(\lambda\) 有 \(\delta\zeta=-\delta\eta\)，所以额外项是

\[
-\partial_\zeta\mathcal T_\zeta\,\delta\eta
=-L\langle h\rangle\,\langle\delta V\rangle
=-\int\langle h\rangle\delta V\,dx.
\]

它与 (9) 精确合成 \(-\int h\delta V\)，不存在剩余常数 primitive 修正。由此得到 source gradient 的一个准确代表

\[
\boxed{
g_u=F+AE+\frac{2vh}{S},\qquad
g_v=BE+\frac{E_x}{S}+\frac{2uh}{S}
=\frac{\lambda-2v}{S}E+2h.}
\tag{10}
\]

第二个化简使用
\(B+(\lambda-V)/S=(\lambda-2v)/S\) 及 \(u-q=S\)。
固定均值叶可再对 \(g_u,g_v\) 作 \(P_0\)；\(D\) 型 Hamilton 场不变。
若遗漏固定参数的 \(-\partial_\zeta\mathcal T\,d\eta\)，(10) 就会留下 \(\langle h\rangle\) 项，后续 Poisson 桥不成立。

## 4. Holonomy 的实际时间导数

物理 Hamilton 场为
\[
u_t=-\frac{Dg_v}{16},\qquad v_t=-\frac{Dg_u}{16}.
\]

定义

\[
R_0=SF+
\left(\frac{\lambda v-v^2}{S}-\frac S4\right)E
+(2v-\lambda)h.
\tag{11}
\]

直接用 (7)、\(q=u-S\)、\(r=A(S+u)-v_x/S\) 展开，得恒等式

\[
DR_0=vDg_v+uDg_u.
\tag{12}
\]

因此

\[
\boxed{
V_t=-\frac2S(vu_t+uv_t)=\frac{DR_0}{8S},\qquad
\eta_t=0,\qquad
\theta_t=KV_t=\frac{R_0-\langle R_0\rangle}{8S}.}
\tag{13}
\]

最后一个平均项由选定的 mean-zero primitive 强制，不能任意删除。它恰好生成 (2) 的常数 diagonal gauge。因为 \(\eta_t=0\)，该 actual trace 流沿轨道也保持 \(\zeta=\lambda-\eta\)，参数不用再次移动。

## 5. 两条 AKNS 演化式；尤其 \(b_t\) 的独立核对

设 \(w_\lambda=(S^2-\lambda^2)/(16S)\)。由 (7) 化简可以先得到

\[
Dg_u=-(\lambda+2v)F+A(\lambda-2v)E+4SAh,
\tag{14}
\]
\[
Dg_v=2qF+
\left[\frac{(\lambda-2v)(\lambda-V)}S-2A(S+u)\right]E
-\frac{2(\lambda-2v)q}{S}h.
\tag{15}
\]

(15) 与 (11) 的系数直接相消，给

\[
u_t+\frac{qR_0}{8S}=w_\lambda E.
\tag{16}
\]

乘 \(e^\theta\)，再用 (13)，即为 (2) 的第一式。

第二式必须包含 \(r\) 中 \(v_x\) 的时间变分：

\[
r_t=A u_t+B v_t-\frac{Dv_t}{S}.
\tag{17}
\]

将 \(u_t=-Dg_v/16,\ v_t=-Dg_u/16\) 代入，再利用 (7) 微分 (14)–(15)，准确的 scalar differential identity 为

\[
D^2g_u-SA\,Dg_v-SB\,Dg_u-2rR_0
=-(S^2-\lambda^2)F.
\tag{18}
\]

故

\[
\boxed{\quad r_t-\frac{rR_0}{8S}=-w_\lambda F.\quad}
\tag{19}
\]

\(D^2g_u\) 的导数与 \(r\) 的 \(v_x\) 项均已计入；(18) 不是在常场上作的替代。最后
\[
b_t=e^{-\theta}(r_t-r\theta_t)
=-w_\lambda f+\frac{\langle R_0\rangle}{8S}b,
\]
得 (2) 的第二式。新独立脚本以自由二阶 source jets 和 (7) 的 adjoint 约束核对 (12)、(16)、(18)–(19)，见 §9。

## 6. 真实 \(\tau\) 截面上的 horizontal projection

令 \(\mathcal G=(a,-b)\) 为常数 diagonal gauge 方向。状态逆桥 (B14) 的
\[
(u,v,\tau)\longmapsto(e^\tau a(u,v),e^{-\tau}b(u,v))
\]
是 \(\chi=0\) 上的实际局部图，\(d\tau(\mathcal G)=1\)，原物理 section 为 \(\tau=0\)。

固定 \(\zeta\) 的 canonical trace 场保持 discriminant，因此保持 \(\chi=0\)。式 (2) 在物理 section 上为

\[
D\mathfrak A\,X_{\mathcal F_\lambda}^{\rm physical}
=w_\lambda X_{\mathcal T_\zeta}^{\rm can}
-c_\lambda\mathcal G,\qquad
c_\lambda=\frac{\langle R_0\rangle}{8S}.
\tag{20}
\]

物理场保持 section，所以
\[
w_\lambda\,d\tau(X_{\mathcal T_\zeta}^{\rm can})=c_\lambda.
\]
当 \(w_\lambda\ne0\)，可写

\[
\boxed{
D\mathfrak A\,X_{\mathcal F_\lambda}^{\rm physical}
=w_\lambda\left(
X_{\mathcal T_\zeta}^{\rm can}
-d\tau(X_{\mathcal T_\zeta}^{\rm can})\mathcal G
\right).}
\tag{21}
\]

这就是相对于实际 \(\tau\) 截面的 horizontal projection。调到状态逆桥 (D5) 的固定中央角 section 后，vertical \(\mathcal G\) 仍被消去；(3) 在 reduced Cartesian 坐标中保持成立。

在 \(\lambda=\pm S\) 不能除 \(w_\lambda\)。但未除的 (20) 在所有参数成立。物理平均叶上 \(\mathcal F_{\pm S}=2\) 恒定，故其物理场为零；(12) 使 \(R_0\) 常数，(16) 给 \(qR_0=0\)。由于 \(\langle q\rangle=-S\ne0\)，\(q\) 不恒为零，故 \(R_0=0\)，也有 \(c_\lambda=0\)。这里没有 endpoint 除零。

### 6.1 转成 KLTZ bracket 时的固定常数

状态逆桥 §4 使用
\[
\varphi_1(t)=-iLa(Lt)/2,\qquad
\varphi_2(t)=2iLb(Lt),\qquad t=x/L,
\]
及 \(\{F,G\}_{\rm NLS}=i\int_0^1(F_1G_2-F_2G_1)\,dt\)。
由 (6) 换变量，
\[
\mathcal T_{\varphi_1}=2if,\qquad
\mathcal T_{\varphi_2}=-ie/2,
\]
故该论文 canonical flow 换回 \(a,b\) 为
\[
X_{\mathcal T}^{\rm NLS}=\frac iL(e,-f).
\]
因此以 KLTZ 的 exact normalization 表达 (3)，权重为
\[
\boxed{\quad
\pi_*D\mathfrak A\,X_{\mathcal F_\lambda}^{\rm physical}
=-iLw_\lambda\,\pi_*X_{\Delta(z)}^{\rm NLS}.
\quad}
\tag{22}
\]
\(\pi\) 表示去常数 gauge、固定中央角后读出的非中央 Cartesian 图。
这个固定非零常数不会改变张成闭包，但 action/angle 速度不能把它略去。

## 7. 最低 mixed 空间上的实际 order-zero 场

式 (14)、(16) 还给一个有用的函数空间增强。在
\[
\widetilde X_0=L^2_0\times H^1_0
\]
中，状态逆桥保证 \(a,b\in L^2,\theta\in H^1\)。实际 AKNS ODE 的 fundamental matrix 和 \(W\) 属于 \(H^1\)，且在有界源球与紧 \(\lambda\) 集上解析、局部有界。因此
\(E,F,h,R_0\in H^1\)。一维 \(H^1\) 为乘法代数，并是 \(L^2\) multiplier，故

\[
u_t=w_\lambda E-\frac{qR_0}{8S}\in L^2,
\]
\[
v_t=\frac{(\lambda+2v)F-A(\lambda-2v)E-4SAh}{16}
\in H^1.
\tag{23}
\]

这给 \(X_{\mathcal F_\lambda}:\widetilde X_0\to\widetilde X_0\) 的实际复解析 order-zero 场；两组件均值为零仍由原来的 \(Dg\) 形式保证。恒等式在此域由光滑密度和上述乘法、ODE 连续性延拓，不能只看 \(v_t=-Dg_u/16\) 而误判为 \(H^1\to L^2\) 的损失。

同样，对每个整数 \(N\ge0\)，
\[
\widetilde X_N=H^N_0\times H^{N+1}_0
\quad\Longrightarrow\quad
E,F,h,R_0\in H^{N+1},
\quad X_{\mathcal F_\lambda}:\widetilde X_N\to\widetilde X_N
\text{ 解析}.
\]
紧参数轮廓上的积分继承该性质。低阶实际 Picard 流与 translation equivariance 又给光滑数据的同窗口持久性，与同一最低状态逆域相容。

## 8. 对有限截断闭包路线的条件性推论

本节明确以状态逆桥 §4.4–4.5 已保存的 action factorization、中央约束和 reduced 双解析图为输入；不在这里重新声称文献定理已证明物理 canonical 性。

固定该图中的一个光滑实际点，要求
\[
(w_n,z_n)\ne(0,0)\qquad(n\ne0).
\tag{24}
\]
所有非中央 actions 非零是更强的充分条件。(24) 是逐点的无限正则条件，未宣称它为某个 Sobolev 开集。

### 8.1 共同迹微分核等于非中央 action 微分核

状态逆桥 (A5)–(A6) 包含 fixed-\(\lambda\) holonomy cancellation，因此
\(\delta\mathcal F_\lambda=0\) 对全部参数蕴含全部 \(dI_n=0\)。
反向使用 (C6)–(C9)：中央 action 和 \(\eta\) 都是非中央 actions 的解析函数，完整 AKNS discriminant 也依赖 actions；全部非中央 action 微分为零便给固定物理参数的 \(d\mathcal F_\lambda=0\)。所以在该点

\[
\mathcal K=
\bigcap_{\lambda\in\mathbb C}\ker d\mathcal F_\lambda
=\bigcap_{n\ne0}\ker dI_n.
\tag{25}
\]

这一步所需的是实际 trace/contour 身份与完整 action factorization，单有有限 action 对合不够。

### 8.2 每个 canonical action 的 reduced 场属于 physical trace 闭包

对一个固定非中央 contour \(\Gamma_n\)，可使其避开
\(\lambda=\pm S\)，并保持 \(R(z)\ne0\)。冻结当前源点、
\(\lambda(z)=\eta-2iz/L\) 及全部 scalar weights。Canonical action variation 给
\[
\pi_*X_{I_n}^{\rm NLS}
=-\frac1\pi\oint_{\Gamma_n}
\frac{\pi_*X_{\Delta(z)}^{\rm NLS}}{R(z)}\,dz
=-\frac1\pi\oint_{\Gamma_n}
\frac{\pi_*D\mathfrak A X_{\mathcal F_{\lambda(z)}}^{\rm physical}}
{(-iL)w_{\lambda(z)}R(z)}\,dz.
\tag{26}
\]

这是一个固定点的向量等式；冻结的积分权重不是在此偷偷宣称一个新的全域 Hamiltonian。

Actual trace 场对紧谱参数集在每个 smooth seminorm 连续。故 (26) 的 contour integral 是有限 scalar 线性组合的 Riemann-sum 极限；经 reduced 状态图的微分逆，所得物理向量属于 actual physical trace Hamilton 场的 \(C^\infty\) 闭包。对每个固定整数 \(N\)，同一结论也在 \(\widetilde X_N\) 范数成立。这里不需要不同频率 contour 的统一上界。

### 8.3 有限 Cartesian 截断确实覆盖共同核的闭包

对 reduced 切向 \((\dot w_n,\dot z_n)\) 满足
\[
z_n\dot w_n+w_n\dot z_n=0,
\]
条件 (24) 使每个坐标对的核恰为一维，张成于该坐标的 canonical action rotation \((-iw_n,iz_n)\)。将给定切向保留在有限个非中央坐标，其余置零，仍满足全部 action 切向约束。中央 action 的微分为零，固定中央角不动。因此每个有限截断为有限个 reduced canonical \(X_{I_n}\) 的线性组合。

有限截断在全部 \(h^N\) 范数收敛。Reduced 状态逆各阶微分连续，故经物理逆后在 \(C^\infty\) 收敛。逐个使用 (26)，再对有限 seminorm 作 diagonal Riemann-sum 逼近，得到条件性结论

\[
\boxed{
\mathcal K=
\overline{\operatorname{span}_{\mathbb C}
\{X_{\mathcal F_\lambda}^{\rm physical}:\lambda\in\mathbb C\}}
^{\,C^\infty}
\quad\text{在 (24) 的实际点。}}
\tag{27}
\]

相反包含由已经证明的 physical trace 对合和微分连续性给出。真实点的真实切向取近似物理向量的实部，得到
\(\operatorname{Re}\mathcal F_\lambda,\operatorname{Im}\mathcal F_\lambda\)
的真实 Hamilton 张成闭包。相同有限截断论证可在每个固定 \(\widetilde X_N\) 范数执行。

系数可以随坐标增长而很大；有限截断只需要各次为有限数。这里证明的是闭包，并未定义一个无限谱时间的绝对收敛线性组合。

这条推论提供 ambient 实际物理叶上的非线性梯度闭包桥。它不自动证明实际共同谱纤维是 Banach/Fréchet 子流形，不把全部 ambient 微分核等同于 inherited strong 纤维的内部 tangent；后者还需与 strong diffeology 及其内部拓扑接合。若某坐标对为 \((0,0)\)，有限 rotation 为零而 product 微分核为二维，此证明失效，与此前均匀临界稳定图反例一致。

## 9. 新独立证据

新增 [精确 jet 脚本](m2_physical_trace_poisson_independent_checks.py) 与
[JSON 结果](m2_physical_trace_poisson_independent_checks.json) 的 **16 项 exact checks 全部通过**，exit code 0。脚本 SHA256 为
1e808d56cfa35646200ce2f971854b258f6219a1b1c5ae1857d284f2bf19cdeb。
检查涵盖 adjoint gauge 参数、holonomy 零模、\(r\) 的三项变分、order-zero 消去、\(R_0\) primitive，以及 \(a_t,b_t\) 的完整常数 gauge 项。没有运行任何旧脚本。§8 的无限闭包依据已明确列出的状态图和证明，而不是把这 16 项代数检查当成函数空间定理。
