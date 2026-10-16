# 零通量次约束正则层的独立审查

2026-10-11。审查 [singular_branch_review_20261011.md](../../刘维尔可积性/research/singular_branch_review_20261011.md) §§2–5。以下推导独立完成，不以原稿的有限 M 检查代替全 M 证明。离线期间推导已通过消息完整交给父任务；恢复连接后先保存本稿，并读取既有新证书结果，没有重跑。

**结论：所审权三变换、配对 Dirac 逆、ρ=Dη、κ 强制守恒及 b 的闭合、三次根迹的合法 cotangent 类、全阶对合及原 Hamiltonian 守恒链均正确。** 本次还得到次约束自括号 N 的全 M 精确式及其在 q=0 上的一阶降阶，并以 χ 的三次根密度给出静态局部切片。后者补强约束阶段的实际场几何存在；它不提供非线性 PDE 解流或谱完备性。

## 1. χ 的权三作用和配对约束矩阵

基础场满足 Πp=Πs=0，J=−offdiag(P0D)，约束泛函 F_f=hM∫fq 生成 δp=−D(fp)、δs=−D(fs)。χ 的所有 cubic 项均变为 −fDχ_cubic−3f_xχ_cubic。一阶 Wronskian p s_x−s p_x 的 f_xx 项由 ps−sp=0 抵消；sRs_x 的相应项由 sRs=0 消失。故

\[
X_{F_f}\chi=-f\chi_x-3f_x\chi
\]

确为全 M 恒等式。在 q=0、χ=κ≠0 上，主/次非零空间模矩阵为

\[
C=\begin{pmatrix}0&K\\K&N\end{pmatrix},\quad K=-3\kappa D,
\quad C^{-1}=\begin{pmatrix}-K^{-1}NK^{-1}&K^{-1}\\K^{-1}&0\end{pmatrix}.
\]

K* =−K，所以两个交叉块都写 K，符合整体斜伴随性。D^−1 只在连续空间零均值函数上使用。这个配对逆不能与 Γ≠0 的单一主约束逆混用。

## 2. 新的次约束自括号精确式

设

\[
g_p=P_0(ps-s_x),\qquad
g_s=P_0(p^2/2+\beta s^2+p_x+Rs_x),\qquad t=p+Rs.
\]

对 hM∫gχ 的独立 Euler 求导给

\[
A_\chi^*g=(-2g g_p+g_xs,\ -2g g_s-g_xt).\tag{A}
\]

记 G=(gp,gs)、z=(s,−t)、S 为两个分量的交换矩阵，则

\[
A_\chi=-2G\cdot-D(z\cdot),\quad J=-SD,
\quad z\cdot Sz=-2\Pi(st)=-2q.
\]

点号使用 Π 配对。直接相乘 AχJAχ*，不代入 q=0，得到

\[
\boxed{N=-2qD^3-3q_xD^2+aD+\tfrac12(a_x+q_{xxx})},\tag{B}
\]

\[
\boxed{a=-8\Pi(g_pg_s)-4\Pi(sg_{s,x}-t g_{p,x})-q_{xx}}.\tag{C}
\]

例如三阶项为 z·Sz；二阶项为 3(z·Sz)_x/2；一阶项为 −4G·SG−4z·SG_x−q_xx。常数项由同一展开给 (a_x+q_xxx)/2，亦与斜伴随条件相符。

所以在整个 q=0 层，而不仅常参考场，

\[
\boxed{N=aD+a_x/2}.
\]

N 并非需要保留三阶估计的算子；K^−1NK^−1 在当前层只有 order−1。系数 a 仍涉及有限场 jets，这个降阶没有证明普通 Sobolev Hamilton 向量场有界或解流适定。

## 3. ρ=Dη、κ 守恒与乘子符号

能量密度

\[
e=\Pi(p^2s/2+\beta s^3/3+s p_x+sRs_x/2)
\]

的点态变分为

\[
\delta e=\Pi(g_p\delta p+g_s\delta s)
+D\Pi(s\delta p+\tfrac12sR\delta s),
\]

这里 δp、δs 的格点均值为零。取 A=−Dgs、S0=−Dgp（本节 S0 区别于交换矩阵 S），有

\[
e_t^0=D\Pi(sA+\tfrac12sRS_0-g_pg_s).
\]

独立 q 通量计算给 q_t^0=Dχ。代入 χ=−2e+q_x，即得

\[
\rho=X_{H_0}\chi=D\eta,\qquad
\eta=2\Pi(g_pg_s-sA)-\Pi(sRS_0)+\chi_x.
\]

在 χ=κ 空间恒定层，总 χ_t=ρ−3κb_x。周期积分强制 κ_t=0；非零 κ 使

\[
b=(\eta-\bar\eta)/(3\kappa)+B(t).
\]

这与报告正号一致。Dirac 残差为 (0,ρ)，乘配对逆后只有主约束乘子 −D^−1ρ/(3κ)；Dirac 场再减去它，恰加入上式正号 b 的 advection 项。κ 保留为初值状态量，并未预先外固定。

## 4. a3 的全 M 点态证明

令 d_j=hs_j/8、b_j=U_j/2、v_j=b_j−d_j，Σd_j=0。单因子前三项为

\[
A_j=-2d_j,\quad B_j=-2v_jd_j+2d_{j,x},
\quad C_j=-2d_j(v_j^2-v_{j,x})+4v_jd_{j,x}-2d_{j,xx}.
\]

有序乘积 a3 的无导数部分，用 Σd=0 和 Σ_(i>j>k)d_i d_j d_k=(Σd_j³)/3 化为

\[
-2\sum_jd_jb_j^2-\frac23\sum_jd_j^3.
\]

导数部分化为

\[
2\sum_jd_jb_{j,x}+4\sum_jb_jd_{j,x}
-2\sum_jd_jd_{j,x}-4\sum_{i>j}d_i d_{j,x}.
\]

R=hP0(H+I/2)P0 的三角 primitive 点态恒等式将最后两项合为 −(h/16)ΣsRs_x。因此

\[
a_3=\frac h{16}\sum_j[-U_j^2s_j-\tfrac{2\beta}3s_j^3
+2s_jU_{j,x}+4U_js_{j,x}-s_j(Rs_x)_j].
\]

代 U=b+p，所有 common b 的导数项因 Σs=Σs_x=0 消失，恰得到

\[
\boxed{a_3=hM(\chi+3q_x-2bq)/16}.
\]

这独立证明报告第 12 式，且解释了为何只核对积分 −8TrD²(P−I) 不够。在当前 stage a3=hMκ/16=−H0/(8L) 点态常数非零。

## 5. 非恒定 stage 的实际静态正则性

### 5.1 full q=0 映射的 split 正则性

χκ≠0 保证 p、s 不同时在某点为零。Aq(u,v)=Π(su+pv) 的未固定均值 raw 右逆为

\[
g\longmapsto\frac{(s,p)g}{\Pi(s^2+p^2)}.
\]

还需用 ker Aq 中的有限个光滑向量修正其组件空间均值。若这个有限维均值修正映射不满射，则存在非零常向量 (a,b) 与光滑 scalar f(x)，使 fs=a、fp=b。f 无零，于是 p=b/f、s=a/f；q=0 给 a·b=0，所有一阶 Wronskian 与 R 项都消失，χ=κ0/f³。χκ≠0 强制 f 常数，p,s 为常场。

因此在报告讨论的非恒定 stage 点，这个均值修正满射。选有限个 kernel 向量构造固定背景的有界 H^r 右逆，q 的乘积映射（r>1/2）满足 split implicit function theorem。故固定组件均值的 full q=0 层确有局部静态状态图。常场例外恰与报告所指出的零动量非正则点一致。

### 5.2 χ^(1/3) 的显式 Diff 切片

对保向圆微分同胚 F，密度 pullback 给

\[
p_F=F'\,p\circ F,\quad s_F=F'\,s\circ F,
\quad q_F=F'^2q\circ F,\quad\chi_F=F'^3\chi\circ F.
\]

这个 pullback 在 Fε=id+εv 时生成 +D(vp)，对应原 X_Ff=−D(fp) 应取 v=−f；两者轨道相同。组件积分保持。若 χ 同号非零，令

\[
r=\sqrt[3]{\chi}\quad\text{取实根},\quad I=\int_0^Lr\,dx,
\quad Y(x)=\frac LI\int_0^xr(\xi)d\xi,\quad F=Y^{-1}.
\]

Y'>0，且

\[
\chi_F=(I/L)^3=\kappa_{\rm flat}.
\]

κflat 随状态变化。这个由积分、实根、微分同胚逆和密度 pullback 组成的显式构造给 C∞ smooth/tame 的局部次约束切片，不需假设 Γ≠0 邻层的一致算子逆。两种平坦化只差圆周平移。

full q=0 是基础弱辛叶中的 coisotropic 层，其光滑核由全部 X_Ff 组成；χ 常数切片将核条件缩为 f_x=0。所以剩余核恰是平移。自由平移层再取商得到局部弱辛静态图。离散稳定子与常场固定点仍须分层；上述构造不提供普通 Sobolev C¹ 的 Diff 动作图或 PDE 真实时间流。

切片 Hamiltonian 为

\[
H_0=-\frac{hML}2\kappa_{\rm flat}
=-\frac{hM}{2L^2}\left(\int\sqrt[3]{\chi}\right)^3.
\]

I 在 primary Diff 作用下保持，这给 quotient 上的内在延伸。切片之前的 H0 本身不是 primary Diff 轨道恒量；不能混淆这两件事。密度 pullback 也是约束几何作用，不是无需改变 b 的原 Laplacian PDE 坐标对称。

## 6. 三次根的 stage cotangent、全阶对合及守恒

冻结非零数值 a3*，用 Ptilde=P−a1D^−1−a2D^−2 定义实三次根。合法 stage 的迹微分代表是

\[
dF_n^*=\operatorname{Tr}(X_n\,dP)\pmod{da_1,da_2},
\quad X_n=-\frac n{3a_3^*}L_3^{n+3},\quad[X_n,P]=0.
\]

共同 U 商消去 a1 conormal；配对 Dirac 消去 a2 的主约束 conormal。full q 零模的 conormal 生成平移，所审 F_n、H0 均平移不变，所以在正则平移商上代表独立。不能把显式离面 extension 的全部 ambient 梯度错误标成已经次约束切向。

原因子推前的 Adler map 对 Xn 给

\[
\dot P=-\tfrac18[(PX_n)_-,P-I],
\]

两个 scalar 负阶部分分别 ≤−1、−3，首系数乘积相消，交换子 ≤−5。a1,…,a4 点态保持，再经本稿全 M a3 恒等式推出 q、χ 切向。因此 Dirac 修正对这个 cotangent 代表消失，任意两个迹括号由周期 trace 循环性为零。

Hfull=−8TrD²(P−I) 的 ambient 场为 −[D²,P]，未必保持 χ；但 Fn 代表已全部约束切向，所以其与 H0 的 Dirac 配对等于 ambient commuting trace 配对，仍为零。这里投影括号差项含 DΠ(Hfull_U)=Dq=0 或 Π((Fn)_U)=0，故共同 U 商的配对也合法。

实际 a3=−H0/(8L) 的归一化另给 nFn da3/(3a3)。a3 不是 Casimir；额外场是 H0 场。已证明的 {Fn*,H0}_D=0 正是归一化后全阶对合和守恒仍成立的理由。Fns 能降到平移商；若闭合式确有真实光滑解，则其有限-jet 谱迹沿解守恒。

本次因而正面认可报告 §5 的完整形式对合链，不只是 ambient 根的条件计算。它依然没有给全阶独立性、谱像逆、极大性或真实共同流。

## 7. 新证书结果与后续三阶实型桥梁

[singular_stage_independent_certificates.py](singular_stage_independent_certificates.py) 独立核验公式 (B)：把 gp、gs、s、t 当作独立 jets，从 (A) 的实际算子复合展开；维数 1,…,5，各检查完整恒等式及四个算子系数。共 25 条 assert 全部通过；[JSON](singular_stage_independent_certificates.json) 的 SHA-256 与当前脚本一致：52f6c935ab94d6d90226efd2936989435c6d566401ff8054cf09bd4ef0cf6f20。此脚本没有重跑原奇异分支 jets 检查。

离线期间另独立得到一个后续实型计算。若 M=3 的最小微分 Q 和真实商 Lax 桥梁已建立，monic Q=D³+AD²+BD+C 的标准负 t2 生成元为

\[
(Q^{2/3})_+=D^2+\frac{2A}3D+\frac{2B}3-\frac{A^2}9-\frac{A_x}3.
\]

去掉 D² 项后 Qbar=D³+uD+v，负 t2 是

\[
u_t=u_{xx}-2v_x,\quad
v_t=-v_{xx}+\frac23u_{xxx}+\frac23u u_x.
\]

w=v−u_x/2 时 u_t=−2w_x、w_t=u_xxx/6+(2/3)u u_x；高频特征值为 ±ik²/√3。故该三阶实型可能是 dispersive good-Boussinesq，不能搬用 Γ≠0 层的 backward-heat 障碍。actual Q/U/common-U 对应、周期去 AD² 条件和真实逆图由 singular_zero_flux 代理继续核对；本稿没有把这个条件桥梁提前标为原物理流定理。

## 8. 新独立核算：全 M 的兼容常背景 κ 层主符号

此节直接线性化原 Hamilton 方程及闭合 b，不假设已经建立新的谱系流。令 Y=p+Rs/2，则 canonical Poisson 算子仍为 −swap D，且

\[
q=\Pi(Ys),\quad H_0=hM\int[V(Y,s)+\Pi(sY_x)]\,dx,
\]

\[
V=\Pi\left[\frac12(Y-Rs/2)^2s+\frac\beta3s^3\right],
\quad \chi=-2V+\Pi(Ys_x-sY_x).
\]

取兼容常背景 (Y,s)=(t,S)，Πt=ΠS=Π(tS)=0，κ=−2V(t,S)≠0。记 c=V_Y、e=V_s（梯度都限制在组件平均零空间），则 cubic Euler 恒等式给

\[
c\cdot t+e\cdot S=-3\kappa/2,\quad
V_{YY}t+V_{Ys}S=2c,\quad V_{sY}t+V_{ss}S=2e.
\]

点积在本节统一采用 Π。原始、未加 b 的线性方程为

\[
y_t=-y_{xx}-D(V_{sY}y+V_{ss}z),\quad
z_t=z_{xx}-D(V_{YY}y+V_{Ys}z).
\]

线性化 χ 后再对 t 求导，ρ=Dη 的最高两层给

\[
\eta_{\rm lin}=(S\cdot y+t\cdot z)_{xx}
+(4c-2V_{YY}t)\cdot y_x-2(V_{sY}t)\cdot z_x
+\text{零阶项}.
\]

第一项由 primary 约束精确消掉。因此 b=η/(3κ) 的主部给

\[
\partial_t\binom yz=D^2T\binom yz+O(D)\binom yz,
\quad T=\operatorname{diag}(-I,I)-\binom tS\ell,
\]

\[
\ell(y,z)=\frac{(4c-2V_{YY}t)\cdot y-2(V_{sY}t)\cdot z}{3\kappa}.
\]

非零大频率的精确约束是

\[
S\cdot y+t\cdot z=0,\quad
-2c\cdot y-2e\cdot z+ik(t\cdot z-S\cdot y)=0.
\]

因而其有界主阶图趋向 E={S·y=0,t·z=0}。这说明上述 T 应限制于 E，不能误用 ambient 未约束矩阵。q=0 又使 (t,S)∈E；T 保持 E。

这里还能完全核算两个非实特征值。令 r=RS。周期 skew primitive 满足

\[
r_j+\tfrac h2S_j=r_{j+1}-\tfrac h2S_{j+1}.
\]

逐格三次方相减再求和，得到对全 M 的精确代数式

\[
0=\sum_j\left[(r_j+hS_j/2)^3-(r_j-hS_j/2)^3\right]
=3h\sum_jS_jr_j^2+\frac{h^3}4\sum_jS_j^3,
\]

\[
\boxed{\Pi(Sr^2)=-\frac{h^2}{12}\Pi(S^3).}
\]

c·t=Π[S(t−r/2)t]、t·VYYt=Π(St²)，所以

\[
a:=\ell(t,0)=\frac{2\Pi[S(t-r/2)^2]-\Pi(Sr^2)/2}{3\kappa}
=-\frac23.
\]

Euler 恒等式又给 ℓ(t,S)=0，因此 b:=ℓ(0,S)=2/3。这同时证明 t、S 都非零。以 (t,0),(0,S) 为基，T 的二维块恰为

\[
\begin{pmatrix}-1/3&-2/3\\2/3&1/3\end{pmatrix},
\quad\lambda=\pm i/\sqrt3.
\]

其余 −1 特征空间为 {(y,0):S·y=ℓ(y,0)=0}，+1 特征空间为 {(0,z):t·z=ℓ(0,z)=0}，维数各 M−3。两个线性条件独立，因为 a、b 非零。这些空间与二维块形成直和，故

\[
\boxed{\operatorname{spec}(T|_E)=
\{-1^{(M-3)},+1^{(M-3)},+i/\sqrt3,-i/\sqrt3\},}
\]

且 T|E 可对角化。真实时间频率的二阶项为 −k²λ：M=3 只有 ±ik²/√3，M>3 同时有各 M−3 个 ±k² 实模。

这个 universal 谱结论严格属于兼容常背景；非恒定背景 χ 还有 Wronskian，不能用 κ=−2V 重用 a=−2/3。常背景在固定组件均值的 full Γ=0 零模上也是动量临界点。因此本节本身尚不构成每个正则 quotient leaf 的精确高频轨道或 Sobolev C¹ 非存在定理；M>3 的一般正则背景与精确 stage 曲线仍需另证。它已经独立说明 M3 的色散主部与全 M 的额外 heat 模来自原方程约束闭合。

[singular_principal_independent_certificates.py](singular_principal_independent_certificates.py) 是本节的新证书，直接构造周期 R、exact rational 常背景和 full constraint-nullspace。M=3,…,10 每个背景核对 R skew、离散 cubic 恒等式、q/κ、a/b、切向性、完整特征多项式和 square-free annihilator，共 56 条 assert 全通过，运行 exit code 0。脚本 SHA-256 为 c1f91fb9ab14d06e7985d8eddc27140a5ccbc9e53aadbbd570d4dc06bcbb66fa；结果见 [JSON](singular_principal_independent_certificates.json)。这是新主符号的独立验证，没有重复旧 stage 脚本。本稿两份证书共 81 条 assert；先前 c0 独立证书另有 49 条。

## 9. 再推进：完整变系数消元使 universal 谱适用于非恒定背景

§8 的常背景 proof 不能直接用 κ=−2V 外推。singular_zero_flux 代理随后提出补全 variable primary 三阶项的消元；本节独立复核这一新步骤，结果通过。因此“尚只确认常背景”的限制已由以下新证明解除，真实非线性全 M 流的限制仍保留。

令非恒定背景 Y=T(x)、s=S(x)，q=Π(TS)=0、χ=κ≠0，并记 c=VY、e=Vs、χpot=−2V、Ω=Π(TSx−STx)，所以 κ=χpot+Ω。未闭合 canonical 向量为 F0=(−Txx−De,Sxx−Dc)。χ 的实际线性化算子是

\[
A_\chi=(-S D-2c+S_x,\ T D-2e-T_x).
\]

ρ=AχF0 变分的 δAχ·F0 只有一阶，因而二阶主项全部来自 AχδF0。直接复合并用 pointwise cubic Euler Hessian 恒等式，得到

\[
\delta\rho=(S,T)D^3(y,z)^T
+(4c-2V_{YY}T-S_x,\ -2V_{sY}T-T_x)D^2(y,z)^T+O(D).
\]

不能只把 (S,T)D³ 当作已消失，因为 S、T 依赖 x。真实主约束 φ=Π(Sy+Tz)=0 给

\[
0=D^3\phi=\Pi[(S,T)D^3(y,z)^T+3(S_x,T_x)D^2(y,z)^T]+O(D).
\]

完整消元因此给

\[
r_y=4c-2V_{YY}T-4S_x,\quad
r_z=-2V_{sY}T-4T_x,
\]

\[
\ell(y,z)=\Pi(r_yy+r_zz)/(3\kappa),\qquad
L_{\rm princ}=D^2[\operatorname{diag}(-I,I)-(T,S)^T\ell]
\quad\text{在 }E=\{\Pi(Sy)=\Pi(Tz)=0\}.
\]

若从完整 F0−D(bT,bS) 而不是 ρ 计算，r 中另出现 bS、−bT；它们在 E 上为零。其余 δb·(Tx,Sx) 项经上述消元后只是一阶，未改变二阶主符号。

§8 的 lattice cubic 恒等式 pointwise 仍成立，故非导数部分 ry·T=−2χpot。主约束 qx=0 又给 2Π(TSx)=Ω。因此

\[
\boxed{\ell(T,0)=\frac{-2\chi_{\rm pot}-4\Pi(TS_x)}{3\kappa}
=-\frac23,}
\]

\[
\ell(T,S)=-4q_x/(3\kappa)=0,\quad\boxed{\ell(0,S)=2/3.}
\]

正是减去 D³φ 的额外 −3Sx、−3Tx，补偿了 χ 的 Wronskian；省略这一步才会产生错误的非 universal a。

κ≠0 还强制 T、S 在每个 x 都非零。若 S(x0)=0，V=0，而 qx=0 给 Π(TSx)=0，故 χ=0 矛盾。若 T(x0)=0，cubic 恒等式给 V(0,S)=Π[S(RS)²]/8+βΠS³/3=0；qx=0 又给 Π(STx)=0，同样矛盾。因此 E 是全圆上的光滑 rank 2(M−2) bundle，振荡二维子 bundle 由 (T,0),(0,S) 全局生成。

同样的直和分解逐点给 ±i/√3 各 1 个及 ±1 各 M−3 个。特征值常数，简单振荡块与两类实热块的谱投影是该 principal 矩阵的固定多项式，因而全圆光滑；不需要只在一个常背景上冻结。于是所有光滑 q=0、χ=κ≠0 背景的约束主符号都有同样的振荡/heat 类型。此处尚未构造 exact 高频轨道、线性半群或非线性 mixed 时间边界解，故不把 principal 分解提前解释成 Sobolev C¹ 反例或全 M 真流定理。
