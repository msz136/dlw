# 2C：DLW 误差方程与受迫 Darboux–Lax 表示

2026-10-13。

**结论。** DLW 的误差可以写成精确受迫场方程，并可通过原 Darboux 因子得到精确 Lax 缺陷。两条相同半离散方程的精确轨道具有守恒的“谱量之差”，但误差算子自身一般不等谱。数值轨道的谱漂移由 Lax 缺陷控制；空间乘积法则失效、辅助势不相容、边界及时间离散必须分别计入。下面给出具体恒等式、条件估计和精确反例，不引入新的“误差可积系统”主张。

## 1. 原方程、残差与辅助势

本文固定同一个 $h>0$，令 $D=\partial_x$、$E f_j=f_{j+1}$，

\[
d_-=\frac{I-E^{-1}}h,\qquad M_-=\frac{I+E^{-1}}2,\qquad
\beta=\frac{h^2}{32}.
\]

物理变量关系为

\[
U=u+2a,\qquad w=v-C_0u-4,\qquad C_0=\frac{E-E^{-1}}{2h}.
\]

背景参数 $a$ 固定。辅助热势记为 $V$，与物理第二场 $v$ 区分。对任意光滑轨道定义

\[
\begin{aligned}
N_{1,j}[U,w]&=
d_-\left[U_t+D\!\left(\frac{U^2}{2}+\beta w^2\right)\right]_j
+D^2(d_-U+M_-w)_j,\\
N_{2,j}[U,w]&=w_{j,t}+D(U_jw_j)-D^2w_j.
\end{aligned}\tag{1}
\]

原半离散 DLW 就是 $N_1=N_2=0$。先在局部 $x$ 区间与格点链讨论；周期、迹与算子逆的条件在后文单列。

令

\[
S_j=U_{j,t}+D\!\left(\frac{U_j^2}{2}+\beta w_j^2\right)
+D^2U_j+\frac h2D^2w_j,
\]
\[
\sigma_j=S_j+2DV_j,\qquad
\kappa_j=V_{j+1}-V_j-\frac h2Dw_j.
\tag{2}
\]

$\sigma$、$\kappa$ 分别测量热势沿 $x$ 和沿格点重构的不相容性。它们不是可以对任意非解轨道同时设为零的自由规范。直接由式（1）得

\[
\boxed{\sigma_{j+1}-\sigma_j=hN_{1,j+1}+2D\kappa_j.}
\tag{3}
\]

特别地，若沿链递推 $V_{j+1}=V_j+(h/2)Dw_j$，即 $\kappa=0$，则

\[
\sigma_j=\sigma_0+h\sum_{k=1}^{j}N_{1,k},\qquad j\ge1.
\tag{4}
\]

在局部区间可由 $DV_0=-S_0/2$ 令 $\sigma_0=0$。这给出物理残差到热势残差的具体累积公式。若要求 $x$ 周期，通常只能设
$DV_0=-(S_0-\langle S_0\rangle_x)/2$，此时
$\sigma_0=\langle S_0\rangle_x$；不能删去该平均缺陷。

## 2. 误差场的精确非线性方程

取参考轨道 $(U,w)$ 与比较轨道 $(\widetilde U,\widetilde w)$，记
$e=\widetilde U-U,\ f=\widetilde w-w$，两者使用相同 $h$ 和同一格点。直接相减得到

\[
\boxed{\begin{aligned}
d_-\!\left[e_t+D\!\left(Ue+\frac{e^2}{2}
+2\beta wf+\beta f^2\right)\right]
+D^2(d_-e+M_-f)&=\widetilde N_1-N_1,\\
f_t+D(Uf+we+ef)-D^2f&=\widetilde N_2-N_2.
\end{aligned}}\tag{5}
\]

这不是线性化，没有丢弃 $e^2,f^2,ef$。物理误差恰为

\[
\epsilon_u=e,\qquad \epsilon_v=f+C_0e.
\tag{6}
\]

因此控制 $(e,f)$ 与控制 $(\epsilon_u,\epsilon_v)$ 之间还有格点导数重构，不能无条件用相同常数比较两个范数。

三种比较必须区分：

| 比较 | 式（5）的源 |
|---|---|
| 相同 $h$ 的两条精确半离散解 | 两项源均为零；方程仍依赖参考场 $U,w$ |
| 精确半离散解减去连续解的格点重构 | $-\tau_h$，其中 $\tau_h=N_h[U^{c,h},w^{c,h}]$ |
| 数值轨道减去连续解的格点重构 | $\nu_h-\tau_h$，$\nu_h$ 是数值轨道的原方程残差 |

“源为零”不等于误差独立满足原 DLW。式（5）包含背景耦合且一般非自治；把背景和误差共同作为未知量只是原两轨道系统的可逆改写。

### 2.1 连续参考的采样必须与物理重构一致

连续极限的变量满足 $U^c=u^c+2a$、$w^c=v^c-u^c_y-4$。如果比较的是原生物理场 $u,v$，应取

\[
U^{c,h}_j=\mathsf S_hU^c,\qquad
w^{c,h}_j=\mathsf S_hv^c-C_0\mathsf S_hu^c-4
=\mathsf S_hw^c-r_h,
\]
\[
r_h=C_0\mathsf S_hU^c-\mathsf S_hU^c_y
=\frac{h^2}{6}\mathsf S_hU^c_{yyy}+O(h^4).
\tag{7}
\]

这里 $\mathsf S_h$ 取物理格点 $y_j=(j+1/2)h$。简单采样 $(U^c,w^c)$ 与采样物理 $(u^c,v^c)$ 后转换并不相同。对后者，第二残差为

\[
\tau_{2,h}=-\left[\partial_t+D\mathcal M_{U^c}-D^2\right]r_h,
\tag{8}
\]

其中 $\mathcal M_{U^c}$ 表示乘法，所有场在同一格点取值。简单采样 $(U^c,w^c)$ 的第二残差则恰为零，因为连续第二式没有 $y$ 导数；不能将这一结论错误地用于式（7）。

第一式的自然位置是相邻物理格点的中点。设
$A^c=U^c_t+D[(U^c)^2/2]$，连续极限满足
$A^c_y+D^2(U^c_y+w^c)=0$。在所需导数一致有界的紧集上，简单采样给出

\[
\tau^{\mathrm{simple}}_{1,h}
=h^2\left[\frac{A^c_{yyy}}{24}
+\frac{D((w^c)^2)_y}{32}
+D^2\left(\frac{U^c_{yyy}}{24}+\frac{w^c_{yy}}8\right)\right]+O(h^4).
\tag{9}
\]

采用物理一致的式（7）后，最后一项改为

\[
\boxed{\tau^{\mathrm{physical}}_{1,h}
=h^2\left[\frac{A^c_{yyy}}{24}
+\frac{D((w^c)^2)_y}{32}
+D^2\left(-\frac{U^c_{yyy}}8+\frac{w^c_{yy}}8\right)\right]+O(h^4).}
\tag{10}
\]

式（8）–（10）只说明光滑参考上的局部截断源；没有把它们提升为数值误差的长期一致界。

### 2.2 时间、空间与边界源

有限时间步序列本身没有 $t$ 导数。选取经过数值节点的连续、分段 $C^1$ 时间重构 $\widehat z_\Delta(t)$，在已固定的闭合及边界条件下定义

\[
r_t=\dot{\widehat z}_\Delta-F_{h,\Delta}(\widehat z_\Delta).
\tag{11}
\]

令 $\mathsf I_\Delta$ 为指定空间重构，$\bar z=\mathsf I_\Delta\widehat z_\Delta$。相对于相同闭合的连续 $x$ 半离散向量场，

\[
\dot{\bar z}-F_h(\bar z)
=\underbrace{\mathsf I_\Delta F_{h,\Delta}(\widehat z_\Delta)
-F_h(\mathsf I_\Delta\widehat z_\Delta)}_{r_x}
+\mathsf I_\Delta r_t.
\tag{12}
\]

对于 $(U,w)$ 形式，式（1）的时间系数为 $\operatorname{diag}(d_-,I)$，所以在同一合法闭合下 $\nu_1=d_-(r_x+\mathsf I_\Delta r_t)_U$、$\nu_2=(r_x+\mathsf I_\Delta r_t)_w$。若均值约束或边界不相容，还须另记约束／边界源；$d_-$ 消去了共同均值，不能仅凭 $N_1=N_2=0$ 判断闭合误差为零。使用不连续重构时，跳跃必须作为分布源保留。

## 3. 原 Darboux 对的精确缺陷桥

沿用项目已证的因子

\[
\alpha_j=\frac{U_j}{2}+\frac{hw_j}{8},\quad
\eta_j=\frac{U_j}{2}-\frac{hw_j}{8},\quad
A_j=D-\mathcal M_{\alpha_j},\quad B_j=D-\mathcal M_{\eta_j},
\]
\[
T_j=B_j^{-1}A_j,\qquad Q_j=-D^2-\mathcal M_{V_j}.
\tag{13}
\]

$B_j^{-1}$ 首先按形式伪微分逆理解。定义

\[
E^\alpha_j=\alpha_{j,t}+D^2\alpha_j+2\alpha_jD\alpha_j+DV_j,\quad
E^\eta_j=\eta_{j,t}+D^2\eta_j+2\eta_jD\eta_j+DV_{j+1}.
\]

由式（1）–（2）直接展开可得

\[
\boxed{E^\alpha_j=\frac{\sigma_j}{2}+\frac h8N_{2,j},\qquad
E^\eta_j=\frac{\sigma_j}{2}-\frac h8N_{2,j}+D\kappa_j.}
\tag{14}
\]

取共同中间势 $V^F_j=V_j+2D\alpha_j$，$Q^F_j=-D^2-\mathcal M_{V^F_j}$。另一因子的自然中间势为 $V^F_j+\kappa_j$，所以

\[
\begin{aligned}
A_{j,t}-Q^F_jA_j+A_jQ_j&=-\mathcal M_{E^\alpha_j},\\
B_{j,t}-Q^F_jB_j+B_jQ_{j+1}
&=-\mathcal M_{E^\eta_j}-\mathcal M_{\kappa_j}B_j.
\end{aligned}
\tag{15}
\]

定义格点 Lax 缺陷

\[
Z_j=T_{j,t}-Q_{j+1}T_j+T_jQ_j.
\]

对 $A_j=B_jT_j$ 求导，中间算子严格相消，得到

\[
\boxed{B_jZ_j=-\mathcal M_{E^\alpha_j}
+\mathcal M_{E^\eta_j}T_j+\mathcal M_{\kappa_j}A_j.}
\tag{16}
\]

乘法的顺序不能交换。若沿链保证 $\kappa=0$，代入式（14）得

\[
\boxed{
Z_j=B_j^{-1}\left[
\frac12\mathcal M_{\sigma_j}(T_j-I)
-\frac h8\mathcal M_{N_{2,j}}(I+T_j)\right].}
\tag{17}
\]

式（3）、（17）把原两场残差变成具体 Lax 缺陷：第一残差沿格点累积成 $\sigma$，第二残差直接进入两个因子的不同组合。这是原 DLW 表示的受迫版本，对任意光滑轨道都成立。

### 3.1 非退化与势规范

前向恒等式（14）–（17）允许 $w_j=0$。由传递商的零缺陷反推两个 Riccati 残差都为零，则仍需原证明的逐点条件 $w_j\ne0$，以及 $\kappa=0$。因为
$T_j=I-B_j^{-1}\mathcal M_{hw_j/4}$，在 $w=0$ 时 $T=I$ 可能丢失场方程的信息。完整因子残差（15）没有这个信息损失。

共同增加仅依赖时间的热势 $V_j\mapsto V_j+g(t)$，只给所有 $Q_j$ 同加中心算子 $-g(t)I$，不改变 $Z_j$；它对应共同时间规范。不同格点任意选取不同的加法函数会改变 $\kappa$，不能当成同一种无害规范。

## 4. 精确误差 Lax 式、切向式与块表示

两条轨道在同一形式代数、同一边界规范下使用式（13）。记 $\delta T=\widetilde T-T$、$\delta Q=\widetilde Q-Q$、$\delta Z=\widetilde Z-Z$。相减得

\[
\boxed{\begin{aligned}
(\delta T_j)_t={}&Q_{j+1}\delta T_j-\delta T_jQ_j\\
&+\delta Q_{j+1}T_j-T_j\delta Q_j\\
&+\delta Q_{j+1}\delta T_j-\delta T_j\delta Q_j+\delta Z_j.
\end{aligned}}\tag{18}
\]

因子与物理误差的关系是

\[
\delta\alpha=e/2+hf/8,\qquad\delta\eta=e/2-hf/8,\qquad
\delta Q=-\mathcal M_{\delta V},
\]
\[
\boxed{\delta T_j=
\widetilde B_j^{-1}
\left[-\mathcal M_{\delta\alpha_j}
+\mathcal M_{\delta\eta_j}T_j\right].}
\tag{19}
\]

这是精确 resolvent 恒等式，不是仅保留一阶。切向极限只需将 $\widetilde B^{-1}$ 换成 $B^{-1}$ 并删去式（18）的二次项；该线性化仍与参考轨道耦合。

对辅助函数差 $\delta\psi=\widetilde\psi-\psi$，可写下三角块对

\[
\mathbf T_j=
\begin{pmatrix}T_j&0\\\delta T_j&\widetilde T_j\end{pmatrix},
\qquad
\mathbf Q_j=
\begin{pmatrix}Q_j&0\\\delta Q_j&\widetilde Q_j\end{pmatrix}.
\tag{20}
\]

但这不产生新的误差谱问题。令

\[
C=\begin{pmatrix}I&0\\-I&I\end{pmatrix},
\quad
\mathbf T_j=C\,\operatorname{diag}(T_j,\widetilde T_j)C^{-1},
\quad
\mathbf Q_j=C\,\operatorname{diag}(Q_j,\widetilde Q_j)C^{-1}.
\tag{21}
\]

它就是两原系统的直和作常共轭。其谱是两个原谱的并集，幂迹是两个原幂迹之和；下三角误差块没有独立的谱信息。切向块的两个对角块相同，谱只重复参考谱。不能据此将误差方程称为新的刘维尔可积系统。

## 5. 周期单值化与原谱积分的误差率

设有 $m$ 个周期格点，按指定顺序定义

\[
\mathcal M=T_{m-1}\cdots T_0.
\]

逐项求导、消去相邻生成算子，得到一般开链公式

\[
\boxed{\mathcal M_t=Q_m\mathcal M-\mathcal M Q_0+\Gamma,\qquad
\Gamma=\sum_{j=0}^{m-1}
T_{m-1}\cdots T_{j+1}\,Z_j\,T_{j-1}\cdots T_0.}
\tag{22}
\]

空乘积为 $I$。只有 $Q_m=Q_0$ 时才可写为
$\mathcal M_t=[Q_0,\mathcal M]+\Gamma$。开放边界另有
$(Q_m-Q_0)\mathcal M$ 源；它不是交换子的迹零项。

### 5.1 原项目使用的逆单值化谱算子

在固定周期平均扇区
$\Pi w=c\ne0,\ \Pi(Uw)=\gamma$ 上，令

\[
G=\frac{hmc}{4},\qquad b_*=\frac{\gamma}{2c},\qquad
\mathscr L=-G(\mathcal M-I)^{-1}+(b_*-G/2)I.
\tag{23}
\]

这与 1A 所用 $\mathscr L$ 的规范一致。局部 Darboux 对自身没有凭空新添的谱参数；周期谱解释来自指定的 Floquet／单值化问题，$\mathscr L$ 是其既有形式归一化。

若 $G,b_*$ 为常数、格点闭合，逆算子求导给出

\[
\boxed{\mathscr L_t=[Q_0,\mathscr L]+\mathscr R,\qquad
\mathscr R=G(\mathcal M-I)^{-1}\Gamma(\mathcal M-I)^{-1}.}
\tag{24}
\]

若均值归一化随时间漂移，还须加上
$-\dot G(\mathcal M-I)^{-1}+(\dot b_*-\dot G/2)I$，不得吸收到“等谱演化”中。开放链则先将边界源加入 $\Gamma$。

对参考及比较轨道使用相同常参数，由式（24）得到所需的精确误差式

\[
\boxed{(\delta\mathscr L)_t
=[Q_0,\delta\mathscr L]
+[\delta Q_0,\mathscr L]
+[\delta Q_0,\delta\mathscr L]
+\delta\mathscr R.}
\tag{25}
\]

即使 $\delta\mathscr R=0$，后两个交换子也一般不能合并成
$[\mathcal B,\delta\mathscr L]$。因此不能断言
$\operatorname{Tr}(\delta\mathscr L)^n$ 守恒。

### 5.2 真正成立的“误差守恒量”

取合法循环迹，并按 1A 的无 $1/n$ 规范定义
$I_n=\operatorname{Tr}\mathscr L^n$。则

\[
\boxed{\frac{d}{dt}(\widetilde I_n-I_n)
=n\operatorname{Tr}\!\left(
\widetilde{\mathscr L}^{\,n-1}\widetilde{\mathscr R}
-\mathscr L^{n-1}\mathscr R\right).}
\tag{26}
\]

证明只用幂求导及迹的循环性，交换子部分消失。若两条相同 $h$ 的轨道均精确、边界及规范相容，则 $\mathscr R=\widetilde{\mathscr R}=0$，从而

\[
\boxed{\Delta I_n(t)=\Delta I_n(0).}\tag{27}
\]

这是一组确实继承的相对谱不变量。它们是
$I_n[U+e,w+f]-I_n[U,w]$，依赖参考轨道，通常不是只依赖误差 $(e,f)$ 的自治守恒量。若参考为连续解的格点重构，$\mathscr R$ 包含截断源，即使比较轨道是精确半离散解，式（27）也一般失效。

一阶切向形式为

\[
\delta I_n=n\operatorname{Tr}(\mathscr L^{n-1}\delta\mathscr L),\qquad
\frac{d}{dt}\delta I_n
=n\operatorname{Tr}(\mathscr L^{n-1}\mathscr R^{(1)})
\tag{28}
\]

（精确参考、固定规范）。它给出谱方向的受迫调制，而不是整个误差范数的守恒。

一个一般 Lax 反例说明上述区别必要：取同一自主等谱流
$L_t=[[N,L],L]$，$N=\operatorname{diag}(1,-1)$。在两状态
$L_0=N,\ L_1=\left(\begin{smallmatrix}0&1\\1&0\end{smallmatrix}\right)$，
各自 $\frac d{dt}\operatorname{tr}L_a^2=0$，但

\[
\frac d{dt}\operatorname{tr}(L_1-L_0)^2=-16.
\tag{29}
\]

这是一般 Lax 推论的反例，不将它声称为 DLW 解。

## 6. 哪些迹与边界条件可以使用

公式（26）有三种不同的严格使用方式：

1. **形式伪微分层。** 用 Adler 迹
   $\operatorname{Tr}A=\int_0^{L_x}\operatorname{res}_D A\,dx$，
   系数足够光滑且 $x$ 周期；此时交换子的留数积分为零。它不是无界微分算子的普通 Hilbert 空间迹。形式公式成立不自动给出算子范数估计或完整谱变换。
2. **有限矩阵层。** 对实际定义的有限矩阵及它们的精确缺陷使用普通迹，所有恒等式是线性代数。但数值 $D$ 替换原微分算子后必须加入第 7 节的代数缺陷；矩阵幂迹不能自动等同于 1A 的指定 PDO 密度求积。
3. **解析算子层。** 必须给出共同定义域、相应逆的存在、乘积和迹类条件及迹循环性。可用相对迹，但须证明相关差为迹类。一般原 DLW 光滑场上的这些条件尚未由本报告完成。

格点周期势需要 $D\sum_jw_j=0$。热势在 $x$ 方向也周期还要求精确轨道满足 $\int S_j\,dx=0$，等价于相应 $U_j$ 空间平均恒定。对数值轨道，如果均值变化不能忽略，应保留式（2）的平均 $\sigma$，不能借非周期的 $V$ 使用周期迹。

$B_j^{-1}$ 的形式存在不要求实际边值算子可逆。式（23）的形式逆需要 $G\ne0$；实际算子 $\mathcal M-I$ 的逆可能有核、造成导数损失或很大的条件数。后面的范数界将这些性质作为明确前提。

## 7. 新增 $x$ 差分后的两层乘积法则缺陷

这是与 1A、1C 衔接时不能跳过的一步。现在 $D$ 是有限矩阵，$\mathcal M_f=\operatorname{diag}(f)$，向量点乘仍记为普通乘积。即使 $D^T=-D$，一般也有

\[
C_1(f)=[D,\mathcal M_f]-\mathcal M_{Df}\ne0,\qquad
C_2(f)=[D^2,\mathcal M_f]-2\mathcal M_{Df}D-\mathcal M_{D^2f}\ne0.
\tag{30}
\]

并且
$C_2(f)=C_1(Df)+DC_1(f)+C_1(f)D$。

### 7.1 系数桥本身的修正

式（14）使用了连续乘积法则。定义点乘缺陷

\[
c_q=D(U^2/2+\beta w^2)-U\,DU-2\beta w\,Dw,\qquad
c_p=D(Uw)-U\,Dw-w\,DU.
\]

以相同有限矩阵 $D$ 计算 $N_2,\sigma,\kappa,E^\alpha,E^\eta$ 后，正确关系是

\[
\boxed{\begin{aligned}
E^\alpha&=\sigma/2+hN_2/8-c_q/2-hc_p/8,\\
E^\eta&=\sigma/2-hN_2/8+D\kappa-c_q/2+hc_p/8.
\end{aligned}}\tag{31}
\]

因此有限网格上的 $N_1=N_2=\sigma=\kappa=0$ 并不推出
$E^\alpha=E^\eta=0$。

### 7.2 算子交织本身的修正

对 $A=D-\mathcal M_r$、$Q=-D^2-\mathcal M_V$、
$Q^F=-D^2-\mathcal M_{V+2Dr}$，矩阵直接相乘给出

\[
\boxed{A_t-Q^FA+AQ
=-\mathcal M_{r_t+D^2r+2rDr+DV}
+\Lambda_D(r,V),\quad
\Lambda_D(r,V)=-C_2(r)-C_1(V).}
\tag{32}
\]

故有限矩阵版的式（16）必须改成

\[
\boxed{BZ=-\mathcal M_{E^\alpha}+\mathcal M_{E^\eta}T
+\mathcal M_\kappa A
+\Lambda_D(\alpha,V)-\Lambda_D(\eta,V_{j+1})T.}
\tag{33}
\]

式（31）和（33）分别是系数乘积法则及算子交换法则的缺陷，两层都需要保留。定义因子残差
$F_A=A_t-Q^FA+AQ,\ F_B=B_t-Q^FB+BQ_+$ 后，
$BZ=F_A-F_BT$ 对任意矩阵仍严格成立，因此是安全的计算入口。

### 7.3 精确有理见证

取 1C 的 Hamilton 空间离散、连续时间，参数

\[
m=N_x=3,\quad h=2/3,\quad\Delta x=3/5,\quad c=-4,\quad\gamma=0,
\]
\[
p=0,\qquad
s=\begin{pmatrix}2/7&-1/7&-1/7\\-2/7&1/7&1/7\\0&0&0\end{pmatrix},
\quad U=p+\frac{\gamma-\Pi(ps)}c,\quad w=c+s.
\tag{34}
\]

用其精确 Hamilton 向量场给出 $U_t,w_t$，以中心 $D$ 构造 $V$。脚本以有理数验证

\[
N_1=N_2=\sigma=\kappa=0.
\]

然而把同一 $D$ 直接放入 Darboux 因子后，各格点
$Z_j=T_{j,t}-Q_{j+1}T_j+T_jQ_j$ 的 Frobenius 范数分别约为

\[
\boxed{0.1398142964,\qquad0.1406497639,\qquad0.0426228327.}\tag{35}
\]

全部 $B_j$ 在这个有限矩阵见证中可逆，完整矩阵与范数平方的精确分数见 JSON。式（33）逐项成立；非零项来自式（31）、（32）的空间代数缺陷。这里 $E^\alpha,E^\eta$ 一般不为零。

此结果严格排除了“原方程的逐项空间差分式成立、Poisson 与能量保留，所以原微分 Lax 表示也自动保留”的推论。它不证明不存在另一种可积 $x$ 离散；也不将这个朴素矩阵谱问题等同于 1A 的 PDO 密度诊断。

## 8. 可使用的条件误差界

以下必须在有限矩阵情形，或在所有乘积具有所列有界／迹类性质的共同算子空间中使用；不能直接把形式 PDO 当作 $L^2$ 上的有界矩阵。

### 8.1 从场残差到 Lax 源

若 $\kappa=0$，式（17）给出

\[
\|Z_j\|\le\|B_j^{-1}\|
\left[\frac12\|\mathcal M_{\sigma_j}\|\|T_j-I\|
+\frac h8\|\mathcal M_{N_{2,j}}\|(1+\|T_j\|)\right].
\tag{36}
\]

由式（4），有限链上
$\|\sigma_j\|\le\|\sigma_0\|+h\sum_{k=1}^j\|N_{1,k}\|$。
再由式（22）逐乘积求和估计 $\Gamma$，以及

\[
\|\mathscr R\|\le |G|\,\|(\mathcal M-I)^{-1}\|^2\,\|\Gamma\|.
\tag{37}
\]

有限网格若使用原因子，式（36）还须加入式（31）、（33）的空间代数源；它们不是物理残差已经为零就会消失的项。长格点链、近不可逆因子或谱退化会放大源，因而没有无条件统一常数。

### 8.2 谱量误差的积分界

若 $\mathscr R,\widetilde{\mathscr R}$ 为迹类且
$\mathscr L,\widetilde{\mathscr L}$ 在相应配对上有界，式（26）给出

\[
\boxed{\begin{aligned}
|\Delta I_n(t)-\Delta I_n(0)|
\le n\int_0^t\bigl(
\|\widetilde{\mathscr L}\|^{n-1}\|\widetilde{\mathscr R}\|_1
+\|\mathscr L\|^{n-1}\|\mathscr R\|_1\bigr)\,ds.
\end{aligned}}\tag{38}
\]

精确参考时第二项为零。形式 Adler 迹层面的同类数值上界，需要改用有限阶系数及其 Sobolev 范数并独立证明乘积估计，不能引用式（38）代替。

若 $\lambda(t)$ 是实际有限矩阵 $\widetilde{\mathscr L}$ 的简单本征值，左右本征向量为 $\ell,r$，则

\[
\dot\lambda=\frac{\ell^*\widetilde{\mathscr R}r}{\ell^*r},
\qquad
|\dot\lambda|\le
\frac{\|\ell\|\|r\|}{|\ell^*r|}\|\widetilde{\mathscr R}\|.
\tag{39}
\]

它需要简单谱及有界条件数。特征值碰撞、非正规性或谱问题选取改变时，这一估计可能失去效力。未建立相应连续 DLW 谱问题之前，不据此宣布发现或排除新的离散谱点。

### 8.3 谱控制不等于物理误差控制

在实际存在可逆传播算子 $Y_t=Q_0Y$ 的条件下，式（25）等价于

\[
\frac d{dt}(Y^{-1}\delta\mathscr LY)
=Y^{-1}\left([\delta Q_0,\widetilde{\mathscr L}]
+\delta\mathscr R\right)Y.
\tag{40}
\]

所以即使谱源小，场／算子误差还受背景传播条件数及 $\delta Q$ 耦合影响。DLW 的热型生成算子不是反 Hermitian，存在高频增长方向，不能假设该条件数为一。要得到物理场界，还需可控谱重构或能量强制性。

本轮 2A 的原结构椭圆行波环带提供更小而明确的接口：在两条始终留在该环带的精确轨道之间，$\Delta I$ 恒定，但
$\Delta\theta(t)=\Delta\theta(0)+t[\Omega(I+\Delta I)-\Omega(I)]$。
这说明作用量控制与相位增长可以同时出现；此接口不涵盖离开该流形的一般数值轨道。

## 9. 验证与可复用结果

- [verify_error_lax.py](verify_error_lax.py)：SymPy 精确核验，无数值演化或拟合。
- [exact_checks.json](exact_checks.json)：38 项、158 个标量条目全部通过。
- 检查包括完整非线性误差展开、热势残差桥、Darboux 微分恒等式、物理采样修正、自由非交换代数中的误差及单值化恒等式、矩阵乘积法则异常、谱迹源公式、块共轭结构及两个反例。
- 有限矩阵检查不替代一般证明；任意维数的依据是正文中的算子代数推导。一般分析谱域和长期误差界仍未完成。

源公式取自项目的 [物理 Darboux–Lax 推导](../../dlw_lax_derivation_20261009/local_manuscript.md)、[论文 Lax 桥](../../dlw_paper_20261009/lax_bridge.md)、[周期单值化与谱积分证明](../../dlw_conservation_hierarchy_20261004/lax/MONODROMY_POISSON_PROOF.md)。与 1A 的联系以原谱积分的指定规范为准，与 1C 的联系以原平均约束的 Hamilton 空间离散为准。

最直接的后续实现是同时记录物理残差、势重构残差、两层空间代数残差和时间重构残差，再由式（22）、（26）核对谱量漂移。只有在它们及相应谱域都可控后，才能把“谱保护改善误差”的判断推进为条件定理。
