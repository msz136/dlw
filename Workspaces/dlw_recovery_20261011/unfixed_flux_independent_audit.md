# 未固定通量层级的独立审查

2026-10-11。审查对象：[unfixed_flux_hierarchy_20261011.md](../../刘维尔可积性/research/unfixed_flux_hierarchy_20261011.md)。本次逐式独立重算，未运行该报告脚本，未改共享研究状态。另由 c0_principal_symbol 独立子审复核第 5–8 式。

**结论：第 1–8 式正确。** 覆盖有限 M≥2、周期 x、c≠0、原方程允许的任意光滑 Γ(t)。c 时间守恒来自原方程，Γ 保留自由时间模。中心化谱迹属于每个固定 c 和组件空间均值叶上的同一 Poisson 代数，并沿任意已经存在的物理轨道守恒。不能从形式 residue trace 推出固定周期算子域下的实际谱相同；后文给出其具体 Floquet 扭转。

## 1. 平均兼容和 Hamilton 分解

取原方程格点平均：D²Πw=0；周期边界给 Πw=c(t)。第二式平均为 c_t+DΠ(Uw)=0，空间积分给 c_t=0，进而 DΠ(Uw)=0。因此 Γ(t)=Π(Uw) 可以任意随时间变。p=P0U、s=w−c、z=Π(ps) 时 b=(Γ−z)/c，报告第 1 式确实没有额外函数约束。

Hfull−hM∫Γb 中的 b 部分精确为

\[
\frac c2b^2+bz-\Gamma b=-\frac{(\Gamma-z)^2}{2c}.
\]

由此得到

\[
K_\Gamma=K_0+\frac\Gamma cP-\frac{hML}{2c}\Gamma^2,
\qquad X_{K_\Gamma}=X_{K_0}+\frac\Gamma cX_P,
\quad X_P=-D(p,s).
\]

最后一项只依赖规定的 Γ(t)、原方程守恒的 c，梯度为零。K0 与 P 平移不变而对合，因此沿这些轨道各自守恒；KΓ 的显含时间依赖不能删掉。这确认报告第 2–3 式。

## 2. 与真实解的规范对应

对任意已经存在的 Γ=0 解，令 a'=Γ/c，定义

\[
U(x,t)=U_0(x-a(t),t)+a'(t),\qquad w(x,t)=w_0(x-a(t),t).
\]

第一式内 U_t+D(U²/2) 的两个 a' U0,x 项抵消，余下公共 a'' 被 δ_- 消去；第二式时间链法则产生 −a'w0,x，恰与乘积通量的额外 −D(a'w0) 相同。平均通量为 Γ0+ca'=Γ。反向变换给逆映射。这是已有实际轨道之间的双射，无需声称开放 Sobolev 初值空间适定。

p,s 的组件空间均值沿此变换保持；原 U 的组件空间均值增加 a'，所以不要把固定 p,s 的均值叶误写成固定原 U 均值的叶。报告当前措辞是正确的。

## 3. 周期 PDO 自同构：不需把 e^(fx) 当周期函数

令 f=Γ/(2c)，空间恒定。定义周期形式 PDO 代数上的

\[
S_f\!\left(\sum_m a_m(x)D^m\right)
=\sum_m a_m(x)(D-f)^m.
\]

由于 (D−f)a=a(D−f)+a_x，它保乘法；非负整幂仍是微分算子，负幂仍负阶，所以保正部。对每个负阶项，只有原 D^−1 项能贡献新的 D^−1，故 res S_f A=res A 逐点成立。S_f 可用 e^(fx) A e^(−fx) 表示，但不需要把 e^(fx) 本身当作圆周上的周期算子。

在同一 p,s,c 状态，UΓ=U0+2f，因此 MΓ=S_f M0，LΓ=f+S_f L0，正是报告第 5 式。这是合法的周期系数形式 PDO 身份。

## 4. 中心化迹与二项式漂移

定义 CnΓ=Tr LΓ^n/n、Ĉn=Tr(LΓ−f)^n/n。由上一逐点 residue 身份，Ĉn=Cn0。二项式系数为

\[
\frac1n\binom nr\operatorname{Tr}L_\Gamma^r
=\binom{n-1}{r-1}C_r^\Gamma.
\]

所以

\[
\widehat C_n=\sum_{r=1}^n\binom{n-1}{r-1}(-f)^{n-r}C_r^\Gamma,
\quad
C_n^\Gamma=\sum_{r=1}^n\binom{n-1}{r-1}f^{n-r}\widehat C_r.
\]

r=0 的项因 Tr I=0 消失。若 Ĉr 沿轨道守恒，微分即给 C1Γ,t=0、CnΓ,t=(n−1)f' C_(n−1)Γ。第 6–7 式的符号和归一化全部正确。

Ĉn 是 p,s,c 的时间无关场泛函。Γ 可以由即时物理场的平均通量计算后消去；因此不会把规定 Γ(t) 的外部时间参数误计为新独立积分。旧对合与有限块独立性仍需旧固定规范证明支持；新的二项式身份本身不替代那些证明。

## 5. 非自治 Lax 身份的独立推导

由 KΓ 分解，在即时 p,s 状态计算的 L0 满足

\[
L_{0,t}=[-(L_0^2)_+-2fD,L_0].
\]

又有 ∂f S_f A=[x,S_f A]。于是 LΓ=f+S_fL0 的时间微分多出 f'([x,LΓ]+I)。共轭生成元精确为

\[
-S_f((L_0^2)_+)-2fS_fD
=-((L_\Gamma-f)^2)_+-2f(D-f)
=-(L_\Gamma^2)_++f^2.
\]

最后 f² 为标量，不贡献交换子。得到

\[
L_{\Gamma,t}=[-(L_\Gamma^2)_+,L_\Gamma]
+f'([x,L_\Gamma]+I).
\]

因为 LΓ=D+Σ_(r≥1)ℓrD^−r，

\[
[x,L_\Gamma]+I=\sum_{r\ge1}r\ell_rD^{-r-1},
\]

它是从 D^−2 开始的周期负阶算子。这里没有在非周期 x 上使用 trace 循环性。

## 6. 从第 8 式直接再次核对漂移与守恒

对任意形式 PDO A=Σ a_mD^m，

\[
[x,A]=-\sum_m m a_mD^{m-1},\qquad\operatorname{res}[x,A]=0
\]

逐点成立：唯一可能的 D^−1 项来自 m=0，系数却为零。[x,LΓ] 本身有周期系数，所以可以只对周期因子 LΓ 与 [x,LΓ] 循环，得到

\[
\operatorname{Tr}L_\Gamma^{n-1}[x,L_\Gamma]
=\frac1n\operatorname{Tr}[x,L_\Gamma^n]=0.
\]

第 8 式因此直接给 CnΓ,t=f'Tr LΓ^(n−1)=(n−1)f' C_(n−1)Γ；n=1 的 Tr I=0。这是一条独立于二项式展开的一致性检查，合法性不依赖把 x 循环移到 trace 中。

同样取 H=LΓ−f，则 H_t=[−(LΓ²)_+,H]+f'[x,H]。上述周期因子计算给 Ĉn,t=0，直接验证中心化守恒。

## 7. 与真实 Floquet 数据的界限

第 5 式是形式 residue 的规范关系，不能写成“同一固定周期域的谱相同”。对相应标量微分 pencil 的 Bloch 波，若 ψ0(x+L)=ρ0ψ0(x)，则 ψΓ=e^(fx)ψ0 满足

\[
\rho_\Gamma=e^{fL}\rho_0.
\]

若 L0ψ0=λ0ψ0，则 LΓψΓ=(λ0+f)ψΓ。规范到 Γ=0 时，应同时中心化 λΓ−f 与 e^(−fL)ρΓ。实际空间平移只改变 monodromy 的起点共轭，不增加这项倍子扭转。

因此报告不需要公式修正；接续完整 Floquet 逆谱时，需要明确记录这个扭转。否则中心化 trace 不变会被错误升级为固定周期边界的实际等谱定理。

## 8. c=Γ=0、order−3 新层级的 cotangent 审查要点

与 singular_zero_flux 代理通信后，已取得其候选 regular stage：q=0、χ=κ≠0，主/次非零空间模约束矩阵的交叉块 K=−3κD，可逆；a3=hMχ/16+3hMq_x/16−hMbq/8 点态给 stage a3=hMκ/16=−H0/(8L)。该候选的原方程一致性与全 M χ_t 公式由对方独立负责，本节不重跑其脚本。

在这些身份成立且约束构成正则 Poisson/Dirac stage 的前提下，order−3 root 的全阶对合逻辑可以成立，必须写足以下步骤：

1. 冻结数值 a3*，在合法 stage 定义 L=[a3*(P−I)^−1]^(1/3)。迹微分的受限 cotangent 代表为 Xn=−nL^(n+3)/(3a3*)，且 [Xn,P]=0。
2. 显式 extension 以 Ptilde=P−a1D^−1−a2D^−2 处理 ambient 阶数跳变。其梯度与 Tr(XnδP) 相差 da1、da2 conormal。不能把 extension 的实际 ambient 场无检验地等同 Xn 的 Adler 场；约束 Dirac 投影消去这些 conormal 后才允许选择 Xn 代表。
3. 在 a1=a2=0、P−I order−3 上，Adler 场为 −[(PXn)_−,P−I]/8，阶数至多 −5，因为两个负阶 scalar 首系数对易。因此 a1,…,a4 点态保持。须再用 a3 与 χ 的完整局部身份，才可推得 χ 的次约束切向性。
4. Xn 的场切向全部约束，使其 Dirac 修正为零；两个迹的括号由 commuting trace 代表计算为零。
5. 实际归一化 a3=−H0/(8L) 随状态变化，另外给 nFn da3/(3a3)。a3 不能被当 Casimir。冻结迹与 H0 的 ambient 配对为零（Hfull=−8TrD²(P−I)），且冻结迹 stage 切向，所以 Dirac 配对仍为零；这才保证实际归一化后的各 Fn 仍对合。
6. q 的全空间均值也取零时，剩余平移 moment-map level 必须在正则自由/局部自由层约化。κ≠0 本身不保证平移自由：常场可能是固定点，其动量 level 在固定组件均值叶中可能奇异。不能把这个全局零模问题藏在非零模 Dirac 逆里。

本节是有条件的 stage cotangent 核验，未独立认证对方尚在撰写的 χ_t、κ 强制守恒和全部交叉 bracket 公式，也未声称该奇异分支的非线性实际共同流、谱独立性或 Liouville 完备性。若前置 regular stage 身份无法完成，order−3 root 的 ambient commuting 代表单独不足以证明物理对合。

## 9. 第二位审阅与交付范围

c0_principal_symbol 第二位独立子审确认第 5–8 式正确，并独立给出 S_f 自同构解释、res[x,A]=0 和真实 Floquet 扭转的限定。它未修改文件、未运行旧脚本。

本次未发现未固定通量报告的公式错误。建议保留现有“实际已有轨道对应”的范围，并在接 Floquet 逆谱时加入第 7 节的双中心化说明。本次没有新数值证书；独立证据为上述逐式全阶推导和第二位审阅。
