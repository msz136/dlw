# DLW 系统参数与离散结构的误差映射

2026年9月30日。本报告从连续 DLW、现有半离散方程及实际差分模板建立误差模型。输入是系统参数、解结构、网格、时间算法、初边值和评价方式；输出是有符号物理误差场及其条件上下界。模型和下述常数均不以已有误差表拟合。本轮完成解析推导与40项精确符号核对；数值演化验证留到模型和适用条件冻结之后。

主映射为

$$
\boxed{\text{参数与解结构}\longrightarrow\text{背景场及导数}
\longrightarrow\text{离散缺陷与线性化算子}
\longrightarrow\text{受迫误差场}\longrightarrow\text{物理输出与误差指标}.}
$$

一个因素可以同时改变缺陷、传播和输出条件性。只比较截断阶或残差范数，不能判定终点误差排名。

## 1 比较对象与理论层次

连续系统固定为

$$
u_{yt}+v_{xx}+\partial_x[(u+2a)u_y]=0,\qquad
v_t+u_{xxy}+\partial_x[(u+2a)v-4u]=0.\tag{1}
$$

记 $h=\Delta y$、$k=\Delta x$、$\delta=\Delta t$。SD 为 Report 式7和8的两场结构形式；SDR 即项目中的 SD2，为式21和22的 $Q,R,M$ 形式；FD 为当前实际交错通量差分。保留解析 $x,t$ 微分时，SD 与 SDR 在非零变量、相容规范和初边值下恢复同一有限 $h$ 物理方程。两条实现的全离散误差仍需分别建模。

输入分为

$$
\Theta=(a,\{p_i,q_i,c_i,\phi_i\}_{i=1}^N,\text{正则分支}),\qquad
\nu=(S,\alpha,\beta,h,k,\delta,T,X,\mathcal B,\mathcal I,\mathcal O).\tag{2}
$$

其中 $S$ 是空间方案，$\alpha,\beta$ 是双线性参数族的两个常数，$X$ 是网格映射，$\mathcal B$ 是边界闭合，$\mathcal I$ 是初始提升和规范，$\mathcal O$ 是物理重构与评价算子。对非孤子解，可直接用给定初态和所需导数界替代谱参数。有限 $h$ 的谱数据还须使 $p_i-s_\pm$、$q_i+s_\pm$ 及 Gram 的交叉分母避开零点，并保持所选实正分支；仅连续参数非退化还不足以覆盖任意粗格距。

本文区分三层陈述。有限维误差恒等式对实际光滑更新映射精确成立；Taylor首项在所需导数受控的区域成立；连续时间的解误差展开和上下界还要求指定空间中的传播控制。40项符号核对检查下面列出的代数关系，不代替最后一项分析条件。

## 2 有限维的精确误差模型

先固定节点和边界闭合。以 $Y$ 表示各方案实际推进的状态，参考状态 $Y_*(t;\Theta,\nu)$ 由同一连续物理真解提升得到。SD 可以用 $(P,W)$，FD 用 $(P,v)$，SDR 用固定规范后的 $(Q,R)$。SDR 提升须在所用差分与远场延拓下存在，并沿选定非零分支光滑；不能用未经检验的连续积分替代离散提升。

若空间离散方程为 $Y_t=F_S(t,Y)$，定义

$$
r_S=F_S(t,Y_*)-\dot Y_*,\quad A_S=F_{S,Y}(t,Y_*),\quad
\epsilon=Y-Y_*.
$$

则

$$
\boxed{\dot\epsilon=A_S\epsilon+r_S+N_S(\epsilon),\quad
N_S(\epsilon)=F_S(t,Y_*+\epsilon)-F_S(t,Y_*)-A_S\epsilon.}\tag{3}
$$

令 $\Phi_S(t,s)$ 为 $A_S$ 的传播算子，便有

$$
\epsilon(T)=\Phi_S(T,0)\epsilon(0)+
\int_0^T\Phi_S(T,s)[r_S(s)+N_S(\epsilon(s))]ds.\tag{4}
$$

SD和FD在共同物理状态、仿射闭合下的右端为二次多项式，二次余项可以精确写出。SDR的原生右端一般含更高次乘积，且物理重构含商，不能把它的余项也称作精确二次多项式；在分母远离零的局部区域仍可用 $\|N_S(\epsilon)\|\le C_S\|\epsilon\|^2$。

时间全离散也有直接的精确版本。设实际一步映射为 $\Psi_{S,n}$，则

$$
B_n=D\Psi_{S,n}(Y_*^n),\qquad
d_n=\Psi_{S,n}(Y_*^n)-Y_*^{n+1},
$$

$$
\epsilon^{n+1}=B_n\epsilon^n+d_n+q_n(\epsilon^n).\tag{5}
$$

$q_n$ 是该更新映射减去常数项和线性项后的精确余项。令 $\Pi_{N,m}=B_{N-1}\cdots B_m$、$\Pi_{N,N}=I$，得到

$$
\boxed{\epsilon^N=\Pi_{N,0}\epsilon^0+
\sum_{n=0}^{N-1}\Pi_{N,n+1}[d_n+q_n(\epsilon^n)].}\tag{6}
$$

式6在有限维上无需假定连续 PDE 网格一致稳定。它给出了 Euler、RK4、边界覆盖和变量恢复的统一模型。变动节点时将节点状态一并纳入 $Y$；每个节点状态上的解析物理采样也必须随之定义。

若还研究有限精度算术，把计算一步相对于精确实数映射的差定义为 $\rho_n$，式5右侧再加 $\rho_n$，式6相应增加 $\sum_n\Pi_{N,n+1}\rho_n$。这是算术误差到物理误差的同一传播映射。每步源界须来自具体运算与线性求解的误差分析；初始SDR提升还需计入所解线性系统的条件性，不能把重构残差小直接当作所有方向的提升误差小。若获得 $\|\rho_n\|\le R_n^{\rm arith}$，则线性算术响应由 $\sum_n\|\Pi_{N,n+1}\|R_n^{\rm arith}$ 控制，并计入同一非线性余项包围。

## 3 纯空间缺陷的显式来源

令

$$b=u+2a,\quad w=v-u_y,\quad A(u)=u^2/2+2au,\quad B(w)=w^2/32-w/4.$$

把连续真解代入半离散方程，第一式在交错中点展开，第二式在原物理节点展开，已有推导给出

$$
\tau_y^{FD}=\binom{v_{xxyy}/12}{u_{xxyyy}/6},\tag{7}
$$

$$
\tau_y^{SD}=\tau_y^{SDR}=
\binom{v_{xxyy}/12-u_{xxyyy}/4+B(w)_{xy}}
{v_{xxyy}/4-u_{xxyyy}/12+B(w)_{xy}+(u_yu_{yy})_x/2}.\tag{8}
$$

这些系数是方程左端残差；演化右端的缺陷首项取其负号。辅助变量 $\omega=h(v-\delta_0u)/4$ 的尺度不能当作物理误差阶。

实际均匀 $x$ 差分是 $D=D_1$、$D_2=D^2$，故

$$D=\partial_x-k^4\partial_x^5/30+O(k^6),\qquad
D^2=\partial_x^2-k^4\partial_x^6/15+O(k^6).\tag{9}$$

在 $h\to0$ 的共同主项上，SD和FD的 $x$ 残差为

$$
\chi_x^{SD}=\chi_x^{FD}=
\binom{-\partial_x^5(bu_y)/30-\partial_x^6v/15}
{-\partial_x^5(bv-4u)/30-\partial_x^6u_y/15}.\tag{10}
$$

有限 $h$ 还包含 $h^2k^4$ 等混合项。实际残差首项为 $h^2\tau_y+k^4\chi_x$；把 $D^2$ 换成独立五点二阶导数，会改变式10的系数。

SDR另外受差分乘积缺陷影响。定义

$$\mathcal C_D(f,g)=D(fg)-fDg-gDf,$$

$$
\mathcal C_D(f,g)=-\frac{k^4}{30}
\sum_{r=1}^4\binom5r f^{(r)}g^{(5-r)}+O(k^6).\tag{11}
$$

针对原参数族 $\alpha=\beta=0$，SDR令 $S=QR$、$G_j=h^2(S_j^2-1)/4$、$H_j=m_j+m_{j+1}+G_j$，其中 $m_{j+1}-m_j=-hDS_j$，原生右端为 $F_Q=-D^2Q-2aDQ-HQ$、$F_R=D^2R-2aDR+HR$。固定网格内点令 $r=DQ/Q$、$\sigma=F_Q/Q$，则推到共同物理状态 $(P,v)$ 后，SDR与SD的空间右端差为

$$\Delta_x=\binom{\delta_-d_u}{d_W+\delta_0d_u},\tag{12}$$

$$d_u=2\mathcal C_D(Q,\sigma)/Q-2D[\mathcal C_D(Q,r)/Q],$$

$$d_W=4[\mathcal C_D(Q,DR)-\mathcal C_D(R,DQ)
+D\mathcal C_D(Q,R)-2a\mathcal C_D(Q,R)].$$

这由 $D(Qr)=QDr+rDQ+\mathcal C_D(Q,r)$、$D(Q\sigma)=QD\sigma+\sigma DQ+\mathcal C_D(Q,\sigma)$ 及 $S=QR$ 的演化直接整理得到。若 $Q$ 非零且相关导数一致受控，$\Delta_x=k^4\Lambda_x+O(k^6)$。按左端残差定义，SDR的 $x$ 主项比SD多 $-\Lambda_x$。边界的远场跳跃、鬼点及覆盖行需用实际延拓再计算；式11不能自动用于粗糙或不相容的延拓。

## 4 单孤子的系统参数映射

取正则单孤子，$K=p+q>0$、$P=p-a$、$Q=q+a$、$\Gamma=-P/Q>0$、$PQ\ne0$。定义

$$
\ell=\frac1P+\frac1Q=\frac K{PQ},\qquad
\Omega=q^2-p^2,
$$

$$z=Kx+\ell y+\Omega t+\varphi,\quad
s(z)=\frac1{1+e^{-z}},\quad f(z)=s(z+\log\Gamma),\quad d=f-s,\quad c=f+s.\tag{13}$$

$\varphi$ 含权重和初相位；原文单位权重对应其中的 $\log(1/K)$。连续物理场为

$$u=2Kd,\qquad v=2K\ell c',\qquad w=4K\ell s'.\tag{14}$$

撇号表示 $z$ 导数，故 $\partial_x=K\partial_z$、$\partial_y=\ell\partial_z$、$\partial_t=\Omega\partial_z$。设 $\zeta=K\ell$，将式14代入式7和8，得到对任意允许参数都成立的显式系数：

$$
\tau_{y,1}^{FD}=\frac{\zeta^3}{6}(f^{(5)}+s^{(5)}),\qquad
\tau_{y,2}^{FD}=\frac{\zeta^3}{3}(f^{(5)}-s^{(5)}),\tag{15}
$$

$$
\tau_{y,1}^{SD}=\zeta^3
\left[\frac{2s^{(5)}-f^{(5)}}3+\frac12((s')^2)''\right]
-\zeta^2s''',\tag{16}
$$

$$
\tau_{y,2}^{SD}=\zeta^3
\left[\frac{f^{(5)}+2s^{(5)}}3+\frac12((s')^2)''+2(d'd'')'\right]
-\zeta^2s'''.\tag{17}
$$

因此系统参数先映射为 $(K,\ell,\Gamma,\Omega,\varphi)$，再映射为带符号残差剖面。$\zeta^3$ 与 $\zeta^2$ 项可以抵消，$\Gamma$ 改变两个 sigmoid 过渡的相对位置；参数作用不是只乘一个正数常量。

下面得到一组完全由理论确定的全波形上界。令 $S_m=\sup_z|s^{(m)}(z)|$。由 $t=s(1-s)\in[0,1/4]$，

$$
(s'')^2=t^2(1-4t),\quad s'''=t(1-6t),\quad
s^{(5)}=t(1-30t+120t^2).
$$

对上述低次多项式求全部临界点可得

$$S_1=1/4,\quad S_2^2=1/108,\quad S_3=1/8,\quad S_5=1/4.$$

$f$ 是 $s$ 的平移，具有相同导数范数。利用 $|d^{(m)}|\le2S_m$，式15至17给出

$$
\boxed{\begin{aligned}
\|\tau_{y,1}^{FD}\|_\infty&\le |\zeta|^3/12,\\
\|\tau_{y,2}^{FD}\|_\infty&\le |\zeta|^3/6,\\
\|\tau_{y,1}^{SD}\|_\infty&\le(251/864)|\zeta|^3+\zeta^2/8,\\
\|\tau_{y,2}^{SD}\|_\infty&\le(59/96)|\zeta|^3+\zeta^2/8.
\end{aligned}}\tag{18}
$$

例如 $(251/864)=S_5+S_2^2+S_1S_3$；第二式中 $2(d'd'')'$ 的估计使相应组合变成 $S_5+9(S_2^2+S_1S_3)$。这些是统一保守上界，并非最优系数或SD/FD排名。它们显示谱极点附近 $|K^2/(PQ)|$ 增大时，可控上界按二次和三次幂恶化；实际误差还依赖有符号剖面及传播，不能据此宣布单调增长。

空间和时间分辨率应先相对于该解本身描述：$kK$、$h|\ell|$、$\delta|\Omega|$ 分别衡量解析剖面的横向、纵向和时间相位分辨率。它们控制光滑剖面Taylor展开的适用性；时间推进的高频条件还需单独看实际演化算子的谱。

$a$ 具有两种不同作用。保持共同物理初态不变时，连续式1中的 $2a$ 是统一的 $x$ 平移速度；保持 $p,q$ 不变却改变 $a$ 时，$P,Q,\ell,\Gamma$ 都改变，初始孤子也改变。这两个参数比较不能混用。

对固定谱参数族，参数的一次映射还可以完全求导。由于 $\zeta=K^2/(PQ)$，

$$
\begin{array}{c|ccc}
\theta&a&p&q\\\hline
\partial_\theta\log|\zeta|&1/P-1/Q&2/K-1/P&2/K-1/Q\\
\partial_\theta\log\Gamma&-1/P-1/Q&1/P&-1/Q\\
\partial_\theta\Omega&0&-2p&2q
\end{array}
$$

若任一残差分量写成 $\tau=\zeta^3R_3(z,\Gamma)+\zeta^2R_2(z)$，则

$$
\partial_\theta\tau=3\zeta^2\zeta_\theta R_3
+\zeta^3[(\partial_{\log\Gamma}R_3)(\log\Gamma)_\theta+R_3'z_\theta]
+2\zeta\zeta_\theta R_2+\zeta^2R_2'z_\theta,
$$

其中 $z_\theta=K_\theta x+\ell_\theta y+\Omega_\theta t+\varphi_\theta$。$\partial_{\log\Gamma}f=f'$，因而所有 $R_3$ 的形状响应也能显式求出。第一项和第三项改变系数尺度，第二项改变两个过渡的相对位置和观测点上的相位；这给出了参数改变残差场的直接响应，随后再用式38计入传播变化。固定 $p,q$ 时，$P<0<Q$ 分支中增大 $a$ 会减小 $|\zeta|$，$Q<0<P$ 分支中则相反，所以式18的保守残差上界尺度有明确的分支相关方向。$\zeta$ 的导数符号仍不能代替完整残差或最终误差的导数符号。

## 5 孤子数与相互作用的结构映射

在正系数 Gram 分支上，可以将每个 $\tau$ 写成

$$\tau=\sum_{S\subset\{1,\ldots,N\}} C_S
e^{K_Sx+L_Sy+\Omega_St},\qquad C_S>0,$$

其中 $K_S=\sum_{i\in S}K_i$、$L_S=\sum_{i\in S}\ell_i$，相互作用系数

$$A_{ij}=\frac{(p_i-p_j)(q_i-q_j)}{(p_i+q_j)(p_j+q_i)}$$

进入 $C_S$，权重与初相位也进入 $C_S$。定义概率权重 $\pi_S=C_Se^{K_Sx+L_Sy+\Omega_St}/\tau$，则对 $r+s=m\ge1$，

$$\partial_x^r\partial_y^s\log\tau
=\operatorname{cum}(\underbrace{K_S,\ldots,K_S}_{r},
\underbrace{L_S,\ldots,L_S}_{s}).\tag{19}$$

这是有限指数和的精确恒等式。累积量的分割公式给出一个直接上界：若 $K_\Sigma=\sum_i|K_i|$、$L_\Sigma=\sum_i|\ell_i|$，

$$
|\partial_x^r\partial_y^s\log\tau|
\le c_m K_\Sigma^rL_\Sigma^s,\qquad
c_m=\sum_{j=1}^m\left\{\begin{matrix}m\\j\end{matrix}\right\}(j-1)!.\tag{20}
$$

花括号为第二类 Stirling 数。连续 $u=2\partial_x\log(F/G)$、$v=2\partial_{xy}\log(FG)$，故式20直接控制式7和8需要的至多六阶对数导数。相互作用和相位通过概率权重改变混合累积量及残差形状，而不改变指数的导数规则。

因此孤子数本身不能决定误差大小；需要同时看总相位尺度和过渡重叠。正系数保证这条导数界不会因为 $\tau$ 项相消而失效。若转入混号系数分支，则必须另外给出 $\inf|F|$、$\inf|G|$ 及导数分子界，式20不能照搬。$A_{ij}$ 的大小也不单独决定误差，更不能把相互作用项的消失自动当成奇点。

## 6 从残差到共同初值下的物理误差

为写出统一连续首项，令 $p=u_y$、$z=(p,v)$，并固定左端 $u(x,y_0,t)$。在零误差基值下，$u$ 误差由

$$\mathcal J e_p(x,y)=\int_{y_0}^y e_p(x,\eta)d\eta,\qquad
\|\mathcal J\|_\infty\le L_y$$

恢复。连续背景 $(\bar u,\bar p,\bar v)$ 的线性化为

$$
\mathcal A_\Theta\binom{e_p}{e_v}=
\binom{-e_{v,xx}-\partial_x[(\bar u+2a)e_p+\bar p\mathcal Je_p]}
{-e_{p,xx}-\partial_x[(\bar u+2a)e_v+(\bar v-4)\mathcal Je_p]}.
\tag{21}
$$

物理输出为 $\mathcal C(e_p,e_v)=(\mathcal Je_p,e_v)$。因此在首项展开和传播存在的空间内，定义

$$
\mathcal K_\Theta[r](T)=\mathcal C\int_0^T\Phi_\Theta(T,s)r(s)ds.\tag{22}
$$

这就是从残差函数到物理误差函数的线性映射。纯 $y$ 首项满足 $a_y^S=\mathcal K_\Theta[-\tau_y^S]$，纯 $x$ 首项满足 $a_x^S=\mathcal K_\Theta[-\chi_x^S]$。相容边界存在偏差时，式21的源和物理输出都须加入对应基值项。

在具有受控余项的解类中，总误差的组织形式为

$$
\boxed{e_{u,v}(T)=e_{\rm init}(T)+h^2a_y^S(T)
+k^4a_x^S(T)+\delta^pa_t^S(T)
+e_{\rm boundary}(T)+e_{\rm evaluation}(T)+\mathcal R(T).}\tag{23}
$$

这是误差场的有符号相加。$\mathcal R$ 包含 $h^4,k^6,h^2k^4$、时间高阶项、混合项和非线性误差反馈；逐项大小和可忽略性需由所选解类证明。式23不自动成为任意光滑数据下的网格一致收敛定理。

共同初值给出 $a_y(0)=0$。其初始速度为

$$\partial_T a_{y,u}(0)=-\int_{y_0}^y\tau_{y,1}(x,\eta,0)d\eta,
\qquad\partial_T a_{y,v}(0)=-\tau_{y,2}(x,y,0).\tag{24}$$

对单孤子，式16和15的第一分量具有显式 $z$ 原函数

$$H_{SD}=\zeta^3[(2s^{(4)}-f^{(4)})/3+((s')^2)'/2]-\zeta^2s'',$$

$$H_{FD}=\zeta^3(f^{(4)}+s^{(4)})/6.$$

所以

$$\partial_Ta_{y,u}(0)=-[H_S(z)-H_S(z_0)]/\ell,
\quad z_0=Kx+\ell y_0+\varphi.\tag{25}$$

式25保留边界位置和两端抵消。可以用 $L_y\|\tau_{y,1}\|$，也可以用 $2\|H_S\|/|\ell|$ 控制其范数，取二者较小者。要将 $Ta_y'(0)$ 变为指定有限时间的上下界，还需包围二阶时间余项。

## 7 结构和频率如何改变误差传播

以下 Fourier 模型用于零背景、非零横向波数 $\eta$ 和固定模态，边界须允许该模态分析。它是可以完全写出的理论子问题，不直接代替变系数孤子背景的式21。

连续物理振幅 $(u,v)$ 的矩阵为

$$M_0=\begin{pmatrix}-2ia\xi&-i\xi^2/\eta\\
i(\xi^2\eta+4\xi)&-2ia\xi\end{pmatrix},\qquad
\lambda_\pm=-2ia\xi\pm\sqrt{\xi^4+4\xi^3/\eta}.\tag{26}$$

记 $d_h=2\sin(\eta h/2)/h$、$m_h=\cos(\eta h/2)$，双参数族取 $A=a+\alpha h^2$、$r=1+\beta h^2$。FD的判别式为

$$D_{FD}=\xi^4m_h^2+4\xi^3m_h/d_h,$$

SD的判别式为

$$D_{SD}=\xi^4+4r\xi^3m_h/d_h-r^2\xi^2h^2.\tag{27}$$

更完整地，在共同物理振幅下写 $M_S=M_0+h^2M_{2,S}+O(h^4)$，令 $L=(\xi^2\eta^2+\xi\eta)/4$，可得

$$M_{2,FD}=\begin{pmatrix}0&i\xi^2\eta/12\\-i\xi^2\eta^3/6&0\end{pmatrix},\tag{28}$$

$$M_{2,SD}=\begin{pmatrix}
L-2i\alpha\xi&i(\xi/4+\xi^2\eta/12)\\
i(\xi^2\eta^3/12+\xi\eta^2/4+4\beta\xi)&-L-2i\alpha\xi
\end{pmatrix}.\tag{29}$$

一种推导是先在 $(u,W)$ 下写SD矩阵，再用 $v=W+id_hm_hu$ 作矩阵相似变换；所有式28和29的分量已精确符号核对。共同初始振幅 $z_0$ 的二阶误差为

$$
\boxed{a_{y,S}^{\rm mode}(T)=
\int_0^T e^{(T-s)M_0}M_{2,S}e^{sM_0}z_0\,ds.}\tag{30}
$$

式30同时包含特征值、特征向量和初态方向的影响。只比较特征频率不能判断每个物理场的误差。例如 $\xi=1,\eta=-3,\alpha=\beta=0$ 时，SD二阶特征频率变化为零，但 $M_{2,SD}=\operatorname{diag}(3/2,-3/2)$，对 $(1,0)$ 初态仍注入 $u$ 误差。

若同时采用均匀 $x$ 差分，SD和FD的有限网格矩阵将 $\xi$ 替换为实际符号 $\widetilde\xi=[8\sin(\xi k)-\sin(2\xi k)]/(6k)$。增长预算应据此和实际边界计算；$\xi k=\pi$ 的交替模态被 $D,D^2$ 消灭，不能简单把连续最高波数代入增长率。在静止常数 $Q,R$ 背景、固定规范下，式12的乘积缺陷没有扰动的一次项；对光滑幅度 $\varepsilon_a$ 的扰动，SDR额外空间差异从 $O(k^4\varepsilon_a^2)$ 进入。由此同一线性背景不能独自解释SDR与SD在有限振幅孤子上的差异；非线性背景、时间曲率和边界仍须保留。恢复任意物理线性模态还要求所用 $D$ 符号非退化。

作为频率误差的局部判据，原SD在 $-4<\xi\eta<-2$ 的振荡带上领先特征频率误差比FD小。这一结论不构成孤子双场误差的优势域。若判别式接近零，单个特征值的平方根展开不再一致，应使用矩阵式30；不能仅由特征值合并断言物理传播发散。

固定非零 $\eta$ 时，高 $|\xi|$ 存在增长率约 $\xi^2$ 的分支。要给温和传播界，必须指定有限频率截断或其他可控函数空间。$\eta\to0$ 的逆导数与零模态也需由边界或规范闭合；一个 $h|\eta|$ 分辨率条件不足以处理它们。

## 8 时间算法和变量重构的响应

固定空间离散后，令 $F$ 为原生状态向量场。Euler一步相对于该ODE精确流的局部缺陷为

$$-\delta^2(F_t+F_YF)/2+O(\delta^3).$$

因而其首项修正向量场为 $F-\delta(F_t+F_YF)/2$。RK4的首项局部缺陷为 $\delta^5g_{4,S}$，$g_{4,S}$ 由一步映射与精确流的五阶Taylor系数差定义，可从向量场导数计算，不是待拟合常数。它们分别产生一阶和四阶全局时间响应，系数仍需经过式4或6传播。

在线性标量模态 $Y_t=\lambda Y$ 上，两个系数完全显式：

$$\lambda_{E,\rm eff}=\lambda-\delta\lambda^2/2+O(\delta^2\lambda^3),$$

$$\lambda_{RK4,\rm eff}=\lambda-\delta^4\lambda^5/120+O(\delta^5\lambda^6).\tag{31}$$

在 $|\delta\lambda|\ll1$ 且首项累积足够小的范围，终点误差幅度的主尺度分别为 $|e^{T\lambda}|T\delta|\lambda|^2/2$ 和 $|e^{T\lambda}|T\delta^4|\lambda|^5/120$，还需乘初始模态幅值。时间阶越高并不意味着系数与空间频率无关。衰减模态另外需要对应稳定多项式的稳定区条件；增长模态的物理增长不能用数值稳定标签消去。

对固定网格内点的非线性物理重构 $z=\mathcal T(Y)$，即使两个空间向量场精确共轭，Euler仍有

$$\mathcal T(Y+\delta F)-[\mathcal T(Y)+\delta\mathcal T_YF]
=\delta^2\mathcal T_{YY}[F,F]/2+O(\delta^3).\tag{32}$$

SDR中 $u=2DQ/Q$、$W=4(1-QR)$，故令 $\sigma=F_Q/Q$，有精确一步关系

$$u^+-u=\delta\dot u/(1+\delta\sigma),\qquad
W^+-W=\delta\dot W-4\delta^2F_QF_R.\tag{33}$$

这说明同为Euler仍有不同时间系数。若重构或规范显含时间，还须加入 $\mathcal T_{tt}$、$\mathcal T_{tY}$ 等项；RK4在精确共轭和光滑条件下的坐标差异从五阶局部项进入四阶全局项。

重构条件性也应按物理方向衡量。对 $\varepsilon_Q=\delta Q/Q$、$\varepsilon_R=\delta R/R$，

$$\delta u=2D\varepsilon_Q+2\mathcal C_D(Q,\varepsilon_Q)/Q,$$

$$\delta v=-4QR(\varepsilon_Q+\varepsilon_R)+\delta_0\delta u.\tag{34}$$

纯规范方向 $(\varepsilon_Q,\varepsilon_R)=(c,-c)$ 在固定网格内点给零物理变化；只看 $\|\delta Q\|$ 或 $1/\min|Q|$ 的粗界会丢失这一抵消。时间变化的规范却可以改变原生Euler的曲率项，故规范必须固定。粗糙 $u$ 误差的 $\delta_0$ 最坏范数为 $1/h$；光滑误差或相容开链误差应使用其实际输出算子，不能默认损失一阶。

## 9 网格与边界的映射

均匀固定网格的首项是式9。动网格令 $x=X(\xi,t)$、$J=X_\xi>0$、$V=X_t$，计算格距为 $\varepsilon$，则精确坐标关系为

$$\partial_x=J^{-1}\partial_\xi,\qquad
\partial_t\widetilde f=f_t+Vf_x.$$

节点运动本身是坐标变换；误差由差分几何、时间更新和状态驱动的网格响应进入。若 $J$ 精确，$D_x^h=J^{-1}D_\xi$ 的首项为

$$D_x^hf=f_x+\varepsilon^4E_Xf+O(\varepsilon^6),\qquad
E_Xf=-\partial_\xi^5\widetilde f/(30J).$$

实际实现为 $X=\xi+s$、$J_h=1+D_\xi s$，则还需计入 $J_h-J=-\varepsilon^4X_{\xi^5}/30+O(\varepsilon^6)$，得到

$$E_Xf=-\frac{\partial_\xi^5\widetilde f}{30J}
+\frac{X_{\xi^5}}{30J}f_x.\tag{35}$$

相应二阶算子的首项为 $\partial_xE_X+E_X\partial_x$。式35须在 $J\ge J_{\min}>0$、网格和场导数一致受控时使用；密集节点减少局部物理格距，同时网格高阶导数和 $1/J_{\min}$ 也改变误差系数。只看最小格距无法判断收益。不同方法各自驱动节点时，要用包含节点的式5建立响应，而非把两条轨道当作同一个预先给定网格。

左基值误差直接进入 $u$ 输出；在共同状态 $P=\delta_-u$ 下，$u$ 误差累加算子范数至多为物理链长。右端闭合会进一步改变 $\delta_0u$ 输出及传播矩阵。已有推导显示：固定精确右鬼点、内部自由累加时可有 $O(L_y/h)$ 的最坏输出放大；相容的背景相对二次外推可把对应输出范数控制为2，但这是改变了边界近似。当前闭合必须逐项对应，不能从旧闭合继承常数。

边界源可精确定义为 $r_{\mathcal B}=F_{\mathcal B}(Y_*)-F_{\mathcal B_*}(Y_*)$，再通过式4或6传播。单孤子相位和权重在全空间只平移剖面，但在有限域改变它与边界及网格的距离。正则孤子尾部按相应相位的指数衰减；远场误差经差分可能带上 $k^{-r}$ 系数。因此扩域减少尾部注入与保持 $k$ 细化是两种不同因素。

## 10 可调结构参数的理论响应

保持物理 $a,h$ 和目标初态不变，取

$$s_\pm=a+\alpha h^2\pm(h+\beta h^3)/2.$$

该重参数族保持已有Gram双线性和孤子结构。按同一物理格距重新非线性化与重构，二阶残差变化为

$$\tau_y^{\alpha,\beta}=\tau_y^{SD}+\alpha\Psi_\alpha+\beta\Psi_\beta,
\quad\Psi_\alpha=\binom{2u_{xy}}{2v_x},\quad
\Psi_\beta=\binom0{-4u_x}.\tag{36}$$

在单孤子变量下，$\Psi_\alpha=(4K\zeta d'',4K\zeta c'')$，$\Psi_\beta=(0,-8K^2d')$。令 $a_0=\mathcal K_\Theta[-\tau_y^{SD}]$、$a_\alpha=\mathcal K_\Theta[-\Psi_\alpha]$、$a_\beta=\mathcal K_\Theta[-\Psi_\beta]$，便得到

$$\boxed{a_y^{\alpha,\beta}(T)=a_0(T)+\alpha a_\alpha(T)+\beta a_\beta(T).}\tag{37}$$

只有右侧两个响应方向可调。在全空间或平移相容边界、共同初值下，$a_\alpha=-2T(u_x,v_x)$，对应相位漂移；固定精确边界未必平移相容，需解同一受迫问题。$\beta$ 从第二式源进入，经耦合影响两个物理场。

若目标是降低终点误差，应优化式37的场范数。对给定加权内积，令 $G_{ij}=\langle a_i,a_j\rangle$、$b_i=\langle a_i,a_0\rangle$，$i,j\in\{\alpha,\beta\}$，则可逆时最优常数为 $-(G^{-1}b)$，剩余平方范数为 $\|a_0\|^2-b^TG^{-1}b$。最大范数可采用对应的连续或采样 minimax 问题，但采样最优值仍需点间导数界才能控制连续域。

因此两常数通常只能减小特定解类的二阶系数。只要 $-\tau_y^{SD}$ 不属于两源方向张成的空间，就无法普适消去二阶残差；式29也显示它们不能消去所有波数上的全部矩阵修正。已有孤子结构不自动意味着一般初值的逆散射理论已建立，更不自动意味着增加 $x,t$ 差分后误差更小。

## 11 各因素的敏感度和条件上下界

令线性误差预测满足 $\dot\epsilon_L=A\epsilon_L+r$。对任意连续因素 $\theta$，在固定维数、光滑分支和可微输入下，

$$\boxed{\dot S_\theta=AS_\theta+(\partial_\theta A)\epsilon_L
+\partial_\theta r,\qquad S_\theta(0)=\partial_\theta\epsilon(0).}\tag{38}$$

物理响应另加输出算子的变化：$\partial_\theta e_L=(\partial_\theta\mathcal C)\epsilon_L+\mathcal C S_\theta$。式38把一个参数的作用分成源变化、传播变化和输出变化。调节双线性常数的领先 $h^2$ 响应是式37；实际系统参数 $a,p_i,q_i$ 还会改变背景和传播。

对离散选择因素，采用精确差分映射，如SD与FD的残差差、SDR与SD的式12、Euler与RK4的更新映射差。改变 $h,k$ 造成维数变化时，应先在共同物理评价空间中比较或建立嵌套提升；不能直接对不同长度数组作参数微分。

最大范数在峰值切换处未必可微，但有

$$|\|e(\theta_2)\|_\infty-\|e(\theta_1)\|_\infty|
\le\|e(\theta_2)-e(\theta_1)\|_\infty.$$

所以响应范数可给变化幅度上界，而其正负通常依赖局部误差场。即使只改变 $h$，$h^2a_y$ 与其他误差场的抵消也可能使当前总误差非单调。

下面给一个可以明确联系参数的保守传播上界。限定固定均匀 $x$ 网格、原生SD状态 $(P,W)$ 或FD状态 $(P,v)$，共同左基值，并采用既有相容的背景相对二次外推，使 $\|\delta_0\mathcal J_h\|\le2$，外侧P与恢复u相容。令 $d_x=3/(2k)$、$U=\|\bar u\|$、$B_P=\|\bar P\|$、$W_0=\|\bar W\|$、$V_0=\|\bar v\|$、$b_{SD}=U+2|a+\alpha h^2|$、$b_{FD}=U+2|a|$、$r=1+\beta h^2$，在状态块最大范数下可沿用离散乘积恒等式给出

$$K_{SD}=\max\{d_x[b_{SD}+L_y B_P+h(W_0/8+|r|/2)]+4d_x^2,
\ d_x[b_{SD}+(W_0+4|r|)L_y]+d_x^2\},$$

$$K_{FD}=\max\{d_x[b_{FD}+L_yB_P]+d_x^2,
\ d_x[b_{FD}+V_0L_y]+2d_x^2+4d_xL_y\}.\tag{39}$$

二次余项系数可取 $C_{SD}=d_xL_y+d_xh/16$、$C_{FD}=d_xL_y$。SD物理输出范数可取 $\max\{L_y,3\}$，FD取 $\max\{L_y,1\}$。式40来自 $\delta_-[(\bar u+2A)\eta]=M_-(\bar u+2A)e_P+M_-\eta\bar P$，避免把复合算子粗估成 $h^{-1}$；它们是上界，非精确增长率。该闭合与任一当前实验若不完全一致，须重新对应边界行，不能直接套用。

对于本报告的单孤子连续采样背景，可以再代入 $U\le2K$、$B_P\le K|\ell|$、$V_0\le K|\ell|$、$W_0\le2K|\ell|$，这些界由式14、中心差分的积分表示和 $S_1=1/4$ 得到。于是系统参数、链长和网格到 $K_S,C_S$ 的映射完全显式。取区间上一致上界 $K,C$，$G(t,s)=e^{K(t-s)}$，并用 $B'=KB+CB^2+R(t)$、$R(t)\ge\|r(t)\|$ 得到标量上解，直到其存在的时间。该粗界在固定 $k$、相容闭合下不随 $h\to0$ 发散，但随 $k\to0$ 可按 $k^{-2}$ 恶化；这正是一致性和传播控制必须分别处理的原因。SDR须另外包围原生雅可比与重构，或在相容局部物理分支上包围式12的额外项。

一般地，要得到严格界，假设所用有限维或受控函数空间中 $\|\Phi(t,s)\|\le G(t,s)$，$\|N(\epsilon)\|\le C\|\epsilon\|^2$，并包围误差源余项。若标量上解 $B$ 满足相应积分不等式，则从式4得

$$\|\epsilon-\epsilon_L\|(T)\le
\int_0^T G(T,s)C B(s)^2ds.$$

使用首项源而非完整缺陷时，右侧再加 $\int G\|r-r_{\rm lead}\|$；非线性输出还需加入自身Taylor余项。相应每个物理场的认证余量记为 $\eta_f(T)$，则

$$\boxed{\max\{0,\|\widehat e_f(T)\|_\infty-\eta_f(T)\}
\le E_f(T)\le\|\widehat e_f(T)\|_\infty+\eta_f(T).}\tag{40}$$

固定网格的完全离散版本直接用式6的传播矩阵乘积和更新映射二阶导数界。普通粗范数可提供很保守的 $G$；更紧的做法是包围实际变系数传播或一个解析近似传播的缺陷。尚未获得这些包围时，不能将式39中未知的 $\eta_f$ 报成具体精度保证。

## 12 因素与误差作用的对应表

| 因素 | 直接映射对象 | 可以从理论得到的影响 | 需要保留的条件 |
|---|---|---|---|
| $a,p_i,q_i$ | 相位尺度、剖面、残差、传播算子 | 单孤子按式13至18；多孤子按式19和20 | 正则分支与谱极点距离；区分固定初态和固定谱 |
| 权重与初相位 | 过渡位置、重叠、边界距离 | 全空间平移不改变单孤子残差范数；有限域改变注入 | 边界、节点及评价窗口固定方式 |
| 孤子数与 $A_{ij}$ | 对数导数的混合累积量 | 改变残差形状及相互作用区 | 正系数或明确的非零tau下界 |
| SD、SDR、FD | 缺陷及原生演化和重构 | SD/FD的 $h^2$ 源不同；SDR/SD额外有乘积与时间曲率项 | 共同物理初边值和规范 |
| $\alpha,\beta$ | 两个可调源方向 | 式37给有符号线性响应，可做系数投影 | 常数随 $h\to0$ 有界；同步改重构 |
| $h$ | $h^2$ 注入及 $h^4$ 余项 | 缩小纯y源和余项 | 固定物理域、光滑分支、其他项受控 |
| $k$ | $k^4$ 注入及可表示频率 | 缩小光滑x缺陷，也扩大高频传播范围 | 实际差分谱与传播条件 |
| $\delta$ 与时间法 | 局部更新缺陷与传播乘积 | Euler为一阶、RK4为四阶；系数依赖向量场导数 | $|\delta\lambda|$、稳定区及重构一致性 |
| $T$ | 缺陷累积和传播时长 | 初始为受迫增长，随后由式22和30控制 | 高频与非正规放大；不能默认线性增长 |
| 网格 $X,J,V$ | 几何差分、ALE及节点响应 | 式35和扩展状态式5 | 正Jacobian及网格高阶导数界 |
| 初态、规范和边界 | 初始传播项、边界源及输出条件性 | 同物理初态可消独有初始表示项；闭合影响放大 | 离散提升、零模态、远场延拓相容 |
| 插值与采样指标 | 末端评价误差 | 光滑且网格受控时三次样条为 $k^4$ 级 | 端点条件；评价加密不替代演化网格加密 |
| 算术精度与线性求解 | 初始误差和每步算术缺陷 | 通过同一传播矩阵累积，可能激发增长模态 | 运算误差源界和提升系统条件性 |

若评价点覆盖半径为 $\rho_{\mathcal G}$，在可微误差场和覆盖整个比较域的条件下，采样最大值 $E_{\mathcal G}$ 满足 $E_{\mathcal G}\le E_\infty\le E_{\mathcal G}+\rho_{\mathcal G}\|\nabla e\|_\infty$。仅在离散y层取最大值时，其对象就是该层集合，不能直接作为连续y条带的下界见证之外的等价指标。绝对误差、按场峰值归一化的误差和相位对齐后的误差是不同输出；比较参数或优化双场时，应固定所选权重和输出定义，额外归一化的参数依赖也需进入式38。

## 13 理论闭合与最后的数值验证

本轮已建立因素映射、一般精确误差恒等式、单孤子显式参数剖面和统一残差界、物理Fourier矩阵首项、双参数响应以及条件上下界。完整验证先要求选定一套固定初边值和频率或函数空间，包围所需导数、传播和源余项，再得到A/B/C对应的有符号误差预测及认证余量。连续PDE的一般传播界、当前边界下指定有限时间的最优系数及动网格的耦合传播界仍需分别证明。

最后的数值验证应只检验冻结的理论预测：有限h残差减去首项的余量；实际右端差与式12；共同物理状态下的短时响应；独立改变h、k、时间步后的误差场；参数响应及误差区间。实际终点误差不作为式18、式28和29、式36至38的输入，也不用于倒推源系数。理论解释应先比较完整带符号场，再计算报告使用的最大范数。

## 14 来源与符号核对

现有方程和二阶残差来自 [Report正文](../gsg_project/dlw_report/_src/Report.md)、[修正方程](../dlw_modified_equation_20260926/REPORT.md) 和 [当前二阶系数界](../dlw_h2_bounds_20260930/REPORT.md)。有限维传播与闭合来自 [参数相关理论](../dlw_semidiscrete/numerics/PARAMETRIC_THEORY.md) 和 [误差传播报告](../dlw_advantage_regions_20260926/REPORT.md)。双参数族来自 [替代半离散化](../dlw_semidiscrete/ALTERNATIVE_DISCRETIZATIONS.md)。SDR差分与时间重构的细化承接 [理论误差阶分析会话](chatgpt-conversation://6abc84e1-37dc-83ec-80fb-bd94b5e3c1a6)。

本轮新增的式15至18、式25的原函数、式28和29的物理矩阵，以及式31的时间系数由 [symbolic_checks.py](symbolic_checks.py) 用精确有理恒等式及代数临界点核对；[symbolic_validation.json](symbolic_validation.json)记录40项通过、源码哈希、零PDE模拟。它未认证传播算子、任意参数区域、浮点轨道或Lean命题。
