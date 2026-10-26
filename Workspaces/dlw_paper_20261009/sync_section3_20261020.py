"""Synchronize approved bilingual discussion, preserving equations and source data."""
from pathlib import Path
import re, json, csv, shutil
from datetime import datetime

P = Path(__file__).resolve().parent
ROOT = P.parents[1]
SOURCE = P / "manuscript.md"
s = SOURCE.read_text(encoding="utf-8")
original = s
backup = P / "discussion_revision_20261020" / datetime.now().strftime("%H%M%S")
backup.mkdir(parents=True, exist_ok=False)
shutil.copy2(SOURCE, backup / "manuscript.md.before")
shutil.copy2(ROOT / "report/dlw_paper_draft.html", backup / "dlw_paper_draft.html.before")

def section(text, lang, key, nextkey):
    start = re.search(r"(?m)^#{2,4} .*?\{#"+lang+"-"+key+r"\}", text).start()
    end = re.search(r"(?m)^#{2,4} .*?\{#"+lang+"-"+nextkey+r"\}", text).start()
    return text[start:end]

def put(lang, key, nextkey, new):
    global s
    old = section(s, lang, key, nextkey)
    s = s.replace(old, new.strip()+"\n\n", 1)

def heading(lang,key,level,title):
    return "#"*level+" "+title+" {#"+lang+"-"+key+"}\n\n"

def fig(file, caption):
    return f'<figure><img src="../Workspaces/dlw_paper_20261009/figures/{file}" alt="{caption}" loading="lazy"><figcaption>{caption}</figcaption></figure>'

def rowfig(kind, row, caption):
    # Render a bounded window of the existing scientific figure; source pixels are unchanged.
    # Row bounds include titles, scientific-notation labels, axes and x labels.
    if kind == "time":
        width, height = 3196, 4677
        bounds = [110, 1260, 2408, 3548, 4677]
    else:
        width, height = 3334, 4224
        bounds = [110, 1130, 2160, 3195, 4224]
    top, bottom = bounds[row:row+2]
    return (
        '<figure class="profile-pair">'
        f'<div style="position:relative;overflow:hidden;aspect-ratio:{width}/{bottom-top}">'
        f'<img src="../Workspaces/dlw_paper_20261009/figures/PE_{kind}_profiles.png" '
        f'alt="{caption}" loading="lazy" style="position:absolute;left:0;top:0;width:100%;max-width:none;'
        f'height:auto;margin:0;transform:translateY(-{100*top/height:.8f}%);">'
        f'</div><figcaption>{caption}</figcaption></figure>'
    )

EN_TIME = r"""
After spatial discretization, we advance the resulting systems in time. For the comparisons between PE, PF and FD, and between fixed and moving meshes, we use the classical fourth-order Runge–Kutta method (RK4) [10]. Keeping the time integrator common allows us to examine the effects of the spatial formulation and mesh choice under the same time-stepping procedure. We then assess the influence of time integration separately by comparing forward Euler, RK4 and Crank–Nicolson (C–N) for PE on a fixed grid.

Let $z$ collect the evolving variables, so that each spatial scheme takes the form $\dot z=\mathcal F(t,z)$. For PE, these variables are $P,W$; for PF, they are the evolving components of $Q,R$; and for FD, they are $P,v$. The physical fields and auxiliary quantities are recovered when evaluating $\mathcal F$, using the reconstruction and boundary relations described above.

For SAMM, we include the node coordinates in the state and advance them together with the field variables. The resulting right-hand side contains both the field equations, with their mesh transport terms, and the node velocities from Section 3.2. This coupling allows changes in the fields to affect the mesh within each time step, while the updated mesh determines where the spatial derivatives are evaluated.

Given $z^n$ at time $t_n$, we compute the RK4 stages as
$$\begin{aligned}
K_1&=\mathcal F(t_n,z^n),\\
K_2&=\mathcal F(t_n+\Delta t/2,z^n+\Delta t K_1/2),\\
K_3&=\mathcal F(t_n+\Delta t/2,z^n+\Delta t K_2/2),\\
K_4&=\mathcal F(t_n+\Delta t,z^n+\Delta t K_3),
\end{aligned}$$
and update
$$z^{n+1}=z^n+\frac{\Delta t}{6}(K_1+2K_2+2K_3+K_4).$$

At each stage, we reconstruct the physical fields and auxiliary quantities from the stage variables and evaluate the prescribed boundary data at the corresponding stage time. For SAMM, the stage node positions determine the mapped spatial operators. The density, flux and node velocity are then evaluated from the same stage fields and mesh. Each call to $\mathcal F$ therefore represents a consistent intermediate state of the coupled system.

To examine the role of the time integrator, we retain the fixed-grid PE spatial discretization and vary only the time-stepping method. Forward Euler uses the current right-hand side,
$$z^{n+1}=z^n+\Delta t\,\mathcal F(t_n,z^n),$$
whereas Crank–Nicolson averages the right-hand sides at the two ends of the step:
$$z^{n+1}=z^n+\frac{\Delta t}{2}\left[\mathcal F(t_n,z^n)+\mathcal F(t_{n+1},z^{n+1})\right].$$
These methods provide first- and second-order temporal approximations, respectively, alongside the fourth-order RK4 method.

For Crank–Nicolson, the new state appears on both sides of the update. We solve the resulting nonlinear equation iteratively, reconstructing the fields and applying the boundary data whenever the right-hand side is evaluated. The iteration is monitored through the residual
$$\mathcal R(z^{n+1})=z^{n+1}-z^n-\frac{\Delta t}{2}\left[\mathcal F(t_n,z^n)+\mathcal F(t_{n+1},z^{n+1})\right].$$
The iteration procedure and stopping criterion are specified in [Appendix F](#en-app-f); the time-integrator comparison is presented in Section 3.5.2.

For all three integrators, we recover $u,v$ from the numerical state at the comparison time and evaluate their errors against the same exact solution. This keeps the assessment in the physical fields while allowing us to examine how the time-stepping method affects the accuracy of the chosen spatial scheme.
"""
ZH_TIME = r"""
完成空间离散后，我们对所得系统进行时间推进。在 PE、PF、FD 的比较以及固定网格与动网格的比较中，统一采用经典四阶 Runge–Kutta 方法（RK4）[10]。保持时间积分器一致，使我们能够在相同的时间推进方式下考察空间表示与网格选择的影响。随后，在固定网格 PE 格式上比较前向 Euler、RK4 与 Crank–Nicolson（C–N），单独考察时间积分的作用。

记 $z$ 为演化变量，则各空间格式写为 $\dot z=\mathcal F(t,z)$。PE 的变量为 $P,W$，PF 的变量为 $Q,R$ 中需要演化的分量，FD 的变量为 $P,v$。每次计算 $\mathcal F$ 时，按照前述重构和边界关系恢复物理场与辅助量。

对于 SAMM，我们将节点坐标纳入状态，与场变量共同推进。相应右端包含带网格输运项的场方程，以及第 3.2 节给出的节点速度。这一耦合使物理场的变化能够在每个时间步内影响网格，而更新后的网格决定空间导数的计算位置。

给定 $t_n$ 时刻的 $z^n$，RK4 各阶段为
$$\begin{aligned}
K_1&=\mathcal F(t_n,z^n),\\
K_2&=\mathcal F(t_n+\Delta t/2,z^n+\Delta t K_1/2),\\
K_3&=\mathcal F(t_n+\Delta t/2,z^n+\Delta t K_2/2),\\
K_4&=\mathcal F(t_n+\Delta t,z^n+\Delta t K_3),
\end{aligned}$$
并更新
$$z^{n+1}=z^n+\frac{\Delta t}{6}(K_1+2K_2+2K_3+K_4).$$

在每个阶段，我们由阶段变量恢复物理场与辅助量，并在对应的阶段时刻计算给定边界数据。对于 SAMM，阶段节点位置决定映射后的空间算子，密度、通量和节点速度则由同一阶段的场与网格计算。因此，每次调用 $\mathcal F$ 都对应耦合系统中一致的中间状态。

为考察时间积分器的作用，我们保持固定网格 PE 空间离散不变，仅改变时间推进方法。前向 Euler 使用当前右端，
$$z^{n+1}=z^n+\Delta t\,\mathcal F(t_n,z^n),$$
而 Crank–Nicolson 对时间步两端的右端取平均：
$$z^{n+1}=z^n+\frac{\Delta t}{2}\left[\mathcal F(t_n,z^n)+\mathcal F(t_{n+1},z^{n+1})\right].$$
这两种方法分别给出一阶和二阶时间近似，与四阶 RK4 一同用于比较。

Crank–Nicolson 的更新式两侧均含有新状态。我们迭代求解所得非线性方程，并在每次计算右端时恢复物理场、施加边界数据。迭代通过残差
$$\mathcal R(z^{n+1})=z^{n+1}-z^n-\frac{\Delta t}{2}\left[\mathcal F(t_n,z^n)+\mathcal F(t_{n+1},z^{n+1})\right]$$
进行监测。迭代过程与停止条件见[附录 F](#zh-app-f)，时间积分器的比较结果见第 3.5.2 节。

对于三种积分器，我们均在比较时刻由数值状态恢复 $u,v$，并相对于同一精确解评价误差。这样便能直接在物理场上考察时间推进方法如何影响所选空间格式的精度。
"""

EN_X = r"""
**Leading x-discretization error.** We examine how centred differences in $x$ affect the approximation of $u_t$ in PE and FD. For the same smooth fields on a fixed finite $y$ interval, with the prescribed lower-boundary rate at $y=b$, both schemes have the leading contribution

<a id="en-eq-203"></a>

$$r^u_{x,m}=(\Delta x)^2B+O\!\left((\Delta x)^4+(\Delta x)^2h^2\right),\qquad m=\mathrm{PE},\mathrm{FD}.\tag{69}$$

The coefficient is

<a id="en-eq-204"></a>

$$\boxed{B=-\frac16\partial_x^3\left[\frac{u(x,y,t)^2-u(x,b,t)^2}{2}+2a\bigl(u(x,y,t)-u(x,b,t)\bigr)\right]-\frac1{12}\partial_x^4\int_b^y v(x,s,t)\,ds.}\tag{70}$$

Thus, $B$ identifies the leading spatial distribution of the error introduced by the common $x$ stencil.

*Derivation.* We begin with the $P$ equations, namely $\dot P=F_P$ in (65) for PE and in (68) for FD. Since $P_r=(u_r-u_{r-1})/h$, summing these equations from the lower layer $\ell$ gives
$$F^u_{m,j}=u_t(x,b,t)+h\sum_{r=\ell+1}^{j}F_{P,m,r}.$$
For FD, the first term telescopes and the second forms a trapezoidal sum:
$$F^u_{\mathrm{FD},j}=u_t(x,b,t)
-D_1\left[\frac{u_j^2-u_\ell^2}{2}+2a(u_j-u_\ell)\right]
-D_2\left[\frac h2\sum_{r=\ell+1}^{j}(v_r+v_{r-1})\right].$$
Applying the centred-difference expansions (63), and replacing the trapezoidal sum by $\int_b^y v\,ds+O(h^2)$, gives the coefficient (70). The corresponding $x$ derivatives of the quadrature remainder are also $O(h^2)$ for the smooth fields considered.

For PE, the same summation gives
$$\begin{aligned}
F^u_{\mathrm{PE},j}={}&u_t(x,b,t)
-D_1\left[\frac{u_j^2-u_\ell^2}{2}+2a(u_j-u_\ell)
+h^2\left(\frac{W_j^2-W_\ell^2}{32}-\frac{W_j-W_\ell}{4}\right)\right]\\
&-D_2\left[u_j-u_\ell+\frac h2\sum_{r=\ell+1}^{j}(W_r+W_{r-1})\right].
\end{aligned}$$
Here $W=v-\delta_0u=v-u_y+O(h^2)$. The integral of $u_y$ cancels the endpoint difference $u_j-u_\ell$, leaving the same integral of $v$ to leading order. The additional flux term carries an explicit factor $h^2$. Applying (63) therefore gives

<a id="en-eq-205"></a>

$$\begin{gathered}
r^u_{x,\mathrm{PE}}=(\Delta x)^2B_{h,\mathrm{PE}}+O((\Delta x)^4),\qquad
r^u_{x,\mathrm{FD}}=(\Delta x)^2B_{h,\mathrm{FD}}+O((\Delta x)^4),\\
B_{h,\mathrm{PE}}=B+O(h^2),\qquad B_{h,\mathrm{FD}}=B+O(h^2),\qquad
B_{h,\mathrm{PE}}-B_{h,\mathrm{FD}}=O(h^2).
\end{gathered}\tag{71}$$

The $O(h^2)$ difference concerns the coefficients multiplying $(\Delta x)^2$, so the difference between these leading $x$-error contributions is $O((\Delta x)^2h^2)$. These expressions provide a common reference for comparing PE and FD when we interpret the numerical results.

These three spatial discretizations are combined with the time integrators in Section 3.3. Their initial and boundary data are specified in Section 3.4.
"""
ZH_X = r"""
**x 向离散误差的首项。** 我们考察 $x$ 向中心差分如何影响 PE 和 FD 对 $u_t$ 的近似。在固定有限 $y$ 区间上的同一光滑场及给定的 $y=b$ 下边界变化率下，两种格式均具有首项贡献

<a id="zh-eq-203"></a>

$$r^u_{x,m}=(\Delta x)^2B+O\!\left((\Delta x)^4+(\Delta x)^2h^2\right),\qquad m=\mathrm{PE},\mathrm{FD}.\tag{69}$$

其系数为

<a id="zh-eq-204"></a>

$$\boxed{B=-\frac16\partial_x^3\left[\frac{u(x,y,t)^2-u(x,b,t)^2}{2}+2a\bigl(u(x,y,t)-u(x,b,t)\bigr)\right]-\frac1{12}\partial_x^4\int_b^y v(x,s,t)\,ds.}\tag{70}$$

因此，$B$ 刻画了共同 $x$ 向差分模板所引入误差的首项空间分布。

*推导。* 我们从 $P$ 方程出发，即 PE 的 (65) 和 FD 的 (68) 中的 $\dot P=F_P$。由 $P_r=(u_r-u_{r-1})/h$，从下边界层 $\ell$ 起累加可得
$$F^u_{m,j}=u_t(x,b,t)+h\sum_{r=\ell+1}^{j}F_{P,m,r}.$$
对于 FD，第一项相消为端点差，第二项形成梯形求和：
$$F^u_{\mathrm{FD},j}=u_t(x,b,t)
-D_1\left[\frac{u_j^2-u_\ell^2}{2}+2a(u_j-u_\ell)\right]
-D_2\left[\frac h2\sum_{r=\ell+1}^{j}(v_r+v_{r-1})\right].$$
应用中心差分展开 (63)，并将梯形和写为 $\int_b^y v\,ds+O(h^2)$，即得到系数 (70)。对于所考虑的光滑场，求积余项相应的 $x$ 导数也为 $O(h^2)$。

对于 PE，同样的累加给出
$$\begin{aligned}
F^u_{\mathrm{PE},j}={}&u_t(x,b,t)
-D_1\left[\frac{u_j^2-u_\ell^2}{2}+2a(u_j-u_\ell)
+h^2\left(\frac{W_j^2-W_\ell^2}{32}-\frac{W_j-W_\ell}{4}\right)\right]\\
&-D_2\left[u_j-u_\ell+\frac h2\sum_{r=\ell+1}^{j}(W_r+W_{r-1})\right].
\end{aligned}$$
其中 $W=v-\delta_0u=v-u_y+O(h^2)$。$u_y$ 的积分抵消端点差 $u_j-u_\ell$，从而在首阶留下相同的 $v$ 积分；额外通量项则显式带有因子 $h^2$。再次应用 (63)，得到

<a id="zh-eq-205"></a>

$$\begin{gathered}
r^u_{x,\mathrm{PE}}=(\Delta x)^2B_{h,\mathrm{PE}}+O((\Delta x)^4),\qquad
r^u_{x,\mathrm{FD}}=(\Delta x)^2B_{h,\mathrm{FD}}+O((\Delta x)^4),\\
B_{h,\mathrm{PE}}=B+O(h^2),\qquad B_{h,\mathrm{FD}}=B+O(h^2),\qquad
B_{h,\mathrm{PE}}-B_{h,\mathrm{FD}}=O(h^2).
\end{gathered}\tag{71}$$

这里的 $O(h^2)$ 差异指乘在 $(\Delta x)^2$ 前的系数差，因此相应 $x$ 向首项误差的差异为 $O((\Delta x)^2h^2)$。这些表达式为后文解释 PE 与 FD 的数值结果提供了共同参照。

上述三种空间格式与第 3.3 节的时间积分器结合使用，初值和边界数据见第 3.4 节。
"""

for lang in ("en","zh"):
    part = section(s,lang,"schemes","samm")
    first = part.index("\n\n")
    p_end = part.index("\n\n", first+2)
    intro = ("For the numerical comparison, we apply the same centred differences in $x$ to PE, PF and a direct finite-difference approximation of the continuous DLW system, denoted by FD. This allows us to examine the different formulations under a common spatial discretization."
             if lang=="en" else "为进行数值比较，我们对 PE、PF 及连续 DLW 系统的直接有限差分近似（记为 FD）统一采用相同的 $x$ 向中心差分。由此，我们在共同的空间离散下考察不同表示的计算表现。")
    part = part[:first+2]+intro+part[p_end:]
    part = part.replace("Writing $k=\\Delta x$, smooth functions satisfy","For smooth functions, the centred differences satisfy")
    part = re.sub(r"记 \$k=\\Delta x\$[^\n]*", "对于光滑函数，中心差分满足", part)
    part = part.replace("k^2","(\\Delta x)^2").replace("k^4","(\\Delta x)^4")
    marker = part.index('<a id="'+lang+'-eq-203">')
    start = part.rfind("**",0,marker)
    start = part.rfind("**",0,start)
    part = part[:start]+(EN_X if lang=="en" else ZH_X)
    put(lang,"schemes","samm",part)
    put(lang,"time","tests",heading(lang,"time",3,"3.3 Time integration" if lang=="en" else "3.3 时间积分")+(EN_TIME if lang=="en" else ZH_TIME))

# Explain the density choice, preserving the numbered conservation and mesh equations.
for lang in ("en","zh"):
    part = section(s,lang,"samm","time")
    pos = part.index('<a id="'+lang+'-eq-96">')
    last = part.rfind("\n\n",0,pos-2)
    before = part[:last]
    explanation = (r"""
To obtain a density that follows the field evolution, we use the conservation form of the $W$ equation,
$$W_t+\bigl[(u+2a)W-4u\bigr]_x-W_{xx}=0.$$
The choice $\rho=1-W/4$ rewrites its nonlinear flux as
$$ (u+2a)W-4u=8a-4(u+2a)\rho.$$
It therefore leads directly to a conservation law for $\rho$, with $\rho=1$ on the zero-field background. We choose the flux to vanish on this background and obtain
""" if lang=="en" else r"""
为了使密度随物理场演化，我们利用 $W$ 方程的守恒形式，
$$W_t+\bigl[(u+2a)W-4u\bigr]_x-W_{xx}=0.$$
取 $\rho=1-W/4$ 后，非线性通量写为
$$ (u+2a)W-4u=8a-4(u+2a)\rho.$$
这一选择直接产生 $\rho$ 的守恒律，且零场背景对应 $\rho=1$。我们将通量归一化为在该背景上为零，从而得到
""")
    part = before+"\n\n"+explanation.strip()+"\n\n"+part[pos:]
    put(lang,"samm","time",part)

# Save intermediate state for subsequent content blocks in this same one-shot script.
def eq(lang, number):
    match = re.search(r'<a id="'+lang+r'-eq-[^"]+"></a>\s*\$\$(?:(?!\$\$)[\s\S])*?\\tag\{'+str(number)+r'\}\$\$',original)
    assert match, (lang,number)
    return match[0]

test_names = ["One soliton (1,2)","One soliton (4,−3)","Two solitons (6,−5; 4,−3)","Two solitons (1,2; 4,−3)"]
zh_names = ["单孤子 (1,2)","单孤子 (4,−3)","二孤子 (6,−5; 4,−3)","二孤子 (1,2; 4,−3)"]
exact_files = ["exact_single_1_2.png","exact_single_4_m3.png","exact_two_soliton.png","exact_two_soliton_mixed.png"]
en_profiles = [
"The first profile is shown below at $t=0$. Both $u_*$ and $v_*$ form a negative trough extending obliquely across the region. Their variation is concentrated across the wave band, giving us a simple setting in which to examine how the methods resolve a localized pulse in each field.",
"With the second parameter choice, the $u_*$ trough is replaced by a positive ridge, while $v_*$ remains negative. The profiles also differ from the first case in amplitude and transverse width. We use this case to extend the comparison to a different pulse shape as well as the opposite polarity of $u_*$.",
"The corresponding profiles are shown below. The two positive ridges in $u_*$ approach one another along different directions and form a higher crest in the interaction region. The accompanying $v_*$ field contains two negative troughs whose shape also changes near their meeting point. This spatial variation allows us to examine the resolution of both the individual wave bands and the region where they interact.",
"In this case, a positive ridge and a deeper negative trough coexist in $u_*$, while the two wave bands in $v_*$ remain negative. The difference in their amplitudes and widths gives the profile a more uneven spatial structure. By including this case, we examine how the methods resolve a smaller positive feature alongside a stronger negative wave and represent their interaction in both physical fields."]
zh_profiles = [
"下图展示第一组解在 $t=0$ 时的波形。$u_*$ 和 $v_*$ 均形成斜穿区域的负向波谷，场的变化主要集中在波带的横向。我们由此从较为简单的波形出发，考察各方法对两个物理场中局部脉冲的分辨能力。",
"采用第二组参数后，$u_*$ 由负向波谷变为正向波脊，而 $v_*$ 仍为负向波谷。与第一组相比，波形的幅值和横向宽度也有所变化。通过这一算例，我们将比较扩展到不同的脉冲形状及相反的 $u_*$ 极性。",
"相应的二孤子波形如下图所示。$u_*$ 中的两条正向波脊沿不同方向接近，并在相互作用区域形成更高的波峰。伴随的 $v_*$ 场包含两条负向波谷，其形状在交汇处附近也发生变化。这种空间变化使我们能够同时考察独立波带及其相互作用区域的分辨情况。",
"最后一组算例中，$u_*$ 同时包含一条正向波脊和一条更深的负向波谷，而 $v_*$ 中的两条波带仍均为负。两者幅值与宽度的差异使波形呈现出更不均匀的空间结构。引入这一算例后，我们可以考察各方法如何在较强负向波的同时分辨较小的正向结构，并在两个物理场中刻画它们的相互作用。"]
for lang in ("en","zh"):
    en=lang=="en"
    profiles=en_profiles if en else zh_profiles
    names=test_names if en else zh_names
    def exactfig(i):
        return fig(exact_files[i],("Exact profiles: " if en else "精确波形：")+names[i]+("; t=0. Left: u; right: v." if en else "；t=0。左：u；右：v。"))
    content=heading(lang,"tests",3,"3.4 Test problems and error measures" if en else "3.4 算例与误差度量")
    content+= (r"""We use four soliton solutions of the continuous DLW system to examine how the numerical methods resolve different wave profiles. We begin with two one-soliton solutions whose $u$ pulses have opposite signs, and then consider two-soliton solutions with different wave orientations and combinations of polarity. This progression allows us to compare the methods on individual waves before examining the more varied spatial structure of interacting waves. In each case, the exact solution supplies the initial and boundary data and provides the reference for measuring errors in both physical fields. Throughout these tests, we take $a=2$, set the determinant coefficients to $\rho_i=1$, and choose zero initial phases.

We examine the solutions over regions containing the principal wave profiles and place the computational boundaries farther out. The regions for the four tests are $[-5,5]^2$, $[-10,10]^2$, $[-30,30]^2$, and $[-30,30]^2$, respectively, and are kept the same across the numerical methods.

**One-soliton solutions.** For the one-soliton tests, we set $N=1$ in the continuous Gram determinant and obtain
""" if en else r"""我们采用连续 DLW 系统的四组孤子解，考察数值方法对不同波形的分辨能力。首先考虑两组 $u$ 脉冲符号相反的单孤子解，再考察具有不同波传播取向与极性组合的二孤子解。这样的安排使我们能够先比较各方法对单个波的计算表现，再考察相互作用波中更为丰富的空间结构。各算例均由精确解提供初值和边界数据，并以其作为两个物理场的误差评价基准。以下统一取 $a=2$、行列式系数 $\rho_i=1$，初相位为零。

我们在包含主要波形的区域内考察这些解，并将计算边界设置在更外侧。四组算例的区域分别为 $[-5,5]^2$、$[-10,10]^2$、$[-30,30]^2$ 和 $[-30,30]^2$，各数值方法均采用相同的区域。

**单孤子解。** 对于单孤子算例，我们在连续 Gram 行列式中取 $N=1$，得到
""")
    content+="\n"+eq(lang,77)+"\n\n"+("where" if en else "其中")+"\n\n"+eq(lang,78)
    content+="\n\n"+("The physical fields then take the explicit form" if en else "相应的物理场具有显式形式")+"\n\n"+eq(lang,79)
    content+="\n\n"+(r"""These expressions guide our choice of parameters. When $p+q>0$ and $c>0$, the signs of the two pulses are determined by $c-1$ and $\ell$, respectively. We therefore choose $(p,q)=(1,2)$ and $(4,-3)$, giving a negative $u$ pulse in the first test and a positive one in the second. The corresponding values are $(c,\ell)=(1/4,-3/4)$ and $(2,-1/2)$, so the $v$ pulse remains negative in both cases.""" if en else r"""这些表达式为参数选择提供了依据。当 $p+q>0$、$c>0$ 时，两个脉冲的符号分别由 $c-1$ 和 $\ell$ 决定。因此，我们选取 $(p,q)=(1,2)$ 和 $(4,-3)$，使第一组算例具有负的 $u$ 脉冲，第二组具有正的 $u$ 脉冲。相应参数分别为 $(c,\ell)=(1/4,-3/4)$ 和 $(2,-1/2)$，因而两组算例的 $v$ 脉冲均为负。""")
    for i in (0,1): content+="\n\n"+profiles[i]+"\n\n"+exactfig(i)
    content+="\n\n"+(r"""**Two-soliton solutions.** We next consider two-soliton solutions to examine how the methods resolve the spatial structure formed by two interacting waves. Setting $N=2$ and expanding the Gram determinant gives""" if en else r"""**二孤子解。** 接下来，我们考虑二孤子解，考察各方法对两个相互作用波所形成空间结构的分辨能力。取 $N=2$ 并展开 Gram 行列式，得到""")
    content+="\n\n"+eq(lang,80)+"\n\n"+("where" if en else "其中")+"\n\n"+eq(lang,81)
    content+="\n\n"+(r"""We obtain the physical fields from $u_*=2\partial_x\log(f_*/g_*)$ and $v_*=2\partial_x\partial_y\log(f_*g_*)$. The mixed term $E_1E_2$ incorporates the interaction between the two waves, with its coefficient determined by their spectral parameters.

In the first test, we choose $(p_1,q_1)=(6,-5)$ and $(p_2,q_2)=(4,-3)$, which gives $c_1=4/3$, $c_2=2$, and $A_{12}=4/3$. The phases $\theta_1=x-11t-y/12$ and $\theta_2=x-7t-y/2$ describe waves with different spatial orientations and propagation rates.""" if en else r"""我们通过 $u_*=2\partial_x\log(f_*/g_*)$ 和 $v_*=2\partial_x\partial_y\log(f_*g_*)$ 恢复物理场。其中，混合项 $E_1E_2$ 纳入两个波之间的相互作用，其系数由谱参数确定。

第一组算例取 $(p_1,q_1)=(6,-5)$、$(p_2,q_2)=(4,-3)$，相应地有 $c_1=4/3$、$c_2=2$、$A_{12}=4/3$。两相位 $\theta_1=x-11t-y/12$ 和 $\theta_2=x-7t-y/2$ 描述具有不同空间取向和传播速率的两个波。""")
    content+="\n\n"+profiles[2]+"\n\n"+exactfig(2)
    content+="\n\n"+(r"""For the second test, we retain $(p_2,q_2)=(4,-3)$ and choose $(p_1,q_1)=(1,2)$, bringing together the two parameter pairs used in the one-soliton tests. Here $c_1=1/4$, $c_2=2$, and $A_{12}=5/4$, with $\theta_1=3x+3t-3y/4$ and $\theta_2=x-7t-y/2$.""" if en else r"""第二组算例保留 $(p_2,q_2)=(4,-3)$，并取 $(p_1,q_1)=(1,2)$，将前面两组单孤子算例采用的参数组合起来。此时 $c_1=1/4$、$c_2=2$、$A_{12}=5/4$，相位为 $\theta_1=3x+3t-3y/4$ 和 $\theta_2=x-7t-y/2$。""")
    content+="\n\n"+profiles[3]+"\n\n"+exactfig(3)
    content+="\n\n"+(r"""**Initial and boundary data.** To compare the three formulations from the same physical initial state, we use the continuous exact fields $u_*,v_*$ to initialize their respective variables. For PE, we set $P^0=\delta_-u_*(0)$ and $W^0=v_*(0)-\delta_0u_*(0)$, while FD uses the same $P^0$, together with $v^0=v_*(0)$. For PF, we determine $Q^0,R^0$ from these physical data and fix the normalization of $Q$ at the leftmost $x$ node. The reconstruction and lower-boundary initialization are described in Appendix D.

During time integration, the continuous exact solution supplies the lower $y$-boundary data and the ghost values of $u$. In the $x$ direction, PE and FD use periodic continuation, whereas PF incorporates the prescribed additive jumps of $Q$ and $R$. These boundary relations are applied when evaluating the right-hand side at each stage of the time integrator.

**Computational settings.** The fixed grids have spacing $\Delta x=h=0.1$. In the SAMM calculations, we keep the same number of nodes and the uniform $y$ spacing $h=0.1$, while allowing the $x$ nodes to follow the transversely averaged conservation density defined in Section 3.2. This lets us examine how redistributing the available nodes affects the accuracy of the computed wave profiles.

All tests start at $t=0$ and advance to $T=0.01$ with $\Delta t=10^{-4}$, giving 100 time steps. We use RK4 for the comparisons of the spatial formulations and meshes; the separate time-integrator comparison retains the fixed-grid PE scheme and the same time step.

**Error measures.** We compare the numerical and exact physical fields at the same spatial locations, using cubic spline interpolation along $x$ for the numerical nodal values. Let $\mathcal G$ denote the common set of comparison points in the region under consideration. The maximum absolute errors at the final time are""" if en else r"""**初值与边界数据。** 为使三种表示从相同的物理初态出发进行比较，我们利用连续精确场 $u_*,v_*$ 初始化各自的变量。PE 取 $P^0=\delta_-u_*(0)$、$W^0=v_*(0)-\delta_0u_*(0)$，而 FD 使用相同的 $P^0$，并取 $v^0=v_*(0)$。对于 PF，我们由这些物理数据确定 $Q^0,R^0$，并在最左侧 $x$ 节点固定 $Q$ 的归一化。具体重构与下边界初始化见附录 D。

时间推进过程中，连续精确解提供 $y$ 下边界数据和 $u$ 的幽灵层值。在 $x$ 方向，PE 与 FD 采用周期延拓，PF 则纳入 $Q、R$ 的给定加性跳跃。在时间积分器的各阶段计算右端项时，均施加相应边界关系。

**计算设置。** 固定网格的间距为 $\Delta x=h=0.1$。在 SAMM 计算中，我们保持相同节点数及均匀的 $y$ 向间距 $h=0.1$，同时让 $x$ 节点按照第 3.2 节定义的横向平均守恒密度调整位置。由此，我们考察在既定节点数下，节点重新分配如何影响波形的计算精度。

所有算例均从 $t=0$ 开始，以 $\Delta t=10^{-4}$ 推进至 $T=0.01$，共计 100 个时间步。空间表示与网格的比较统一采用 RK4；单独的时间积分器比较保持固定网格 PE 格式及相同时间步长。

**误差度量。** 我们在相同空间位置比较数值物理场与精确物理场，并沿 $x$ 方向对数值节点值进行三次样条插值。记 $\mathcal G$ 为所考察区域内的共同取样点集，终止时刻的最大绝对误差为""")
    content+="\n\n"+eq(lang,82)
    content+="\n\n"+(r"""We report the errors in the two fields separately to examine how each responds to the formulation, time integrator, and mesh choice.

For PE and PF, we further interpret the total error through the corresponding semi-discrete exact solution. Writing $Z=(u_*,v_*)$ for the continuous exact field and $Z_h=(U_h,V_h)$ for the semi-discrete exact field with the same spectral parameters, we have""" if en else r"""我们分别报告两个物理场的误差，以考察它们对非线性表示、时间积分器及网格选择的不同响应。

对于 PE 和 PF，我们进一步借助对应的半离散精确解理解总误差的组成。记连续精确场为 $Z=(u_*,v_*)$，具有相同谱参数的半离散精确场为 $Z_h=(U_h,V_h)$，则""")
    content+='\n\n<a id="'+lang+'-eq-206"></a>\n\n'
    content+=r"$$Z_{\mathrm{num}}-Z=\underbrace{Z_h-Z}_{\text{lattice error}}+\underbrace{Z_{\mathrm{num}}-Z_h}_{\text{numerical error}}.\tag{83}$$"
    content+="\n\n"+(r"""Under the assumptions of Section 2.5, the lattice error satisfies $Z_h-Z=h^2C+O(h^4)$, where $C=(C_U,C_V)$. The coefficients derived there describe the leading spatial distribution of the error introduced by discretizing $y$. The remaining contribution includes the effects of the $x$ and time discretizations, field recovery, and initial and boundary data. We use this decomposition in the numerical results below to discuss how the lattice and numerical contributions combine and to interpret the observed errors in both physical fields.""" if en else r"""在第 2.5 节的假设下，格点误差满足 $Z_h-Z=h^2C+O(h^4)$，其中 $C=(C_U,C_V)$。该节导出的系数刻画了离散化 $y$ 所引入误差的首项空间分布。其余贡献包括 $x$ 方向和时间离散、物理场恢复以及初值与边界数据的影响。我们将在下文数值结果中利用这一分解，讨论格点误差与数值误差如何共同作用，并解释两个物理场中观察到的误差表现。""")
    put(lang,"tests","results",content)

en_spatial = [
"For the first one-soliton solution, we observe errors concentrated along the oblique wave band in both fields. Figure 1 shows similar error patterns for PE and FD, with several parallel ridges in the $u$ error and a more pronounced central band in the $v$ error. PF produces larger errors along the same wave structure. Its higher maximum errors in Table 1 therefore reflect an extended band of larger deviations rather than a single isolated peak.",
"The second one-soliton test reveals a more distinct difference between the formulations. In Figure 2, the PE and FD errors remain concentrated near the wave band and have similar spatial shapes. The PF $v$ error extends over a broader portion of the region and remains visibly elevated away from the principal band. We thus see a difference in both the magnitude and spatial extent of the error, accompanying the larger separation between the PF and PE/FD maximum $v$ errors in Table 1.",
"For the first two-soliton solution, the error surfaces follow the two wave branches and develop a pronounced peak near their interaction region. In Figure 3, we find this structure in the $v$ errors of all three methods, whose maximum values are also close. The $u$ errors show a clearer distinction: PF produces a higher peak near the interaction, while PE and FD retain similar distributions with smaller amplitudes. Comparing the two rows makes the field dependence evident—the formulations give closely matched $v$ errors in this case, but differ more substantially in $u$.",
"In the mixed-polarity two-soliton test, the larger errors are concentrated near the stronger negative wave band, while the smaller positive feature is less prominent in the error surfaces. Figure 4 again shows similar distributions for PE and FD, with FD attaining smaller maximum errors in both fields. PF produces a substantially higher error band, particularly in $u$. Alongside the first one-soliton test, this case shows that the larger PF errors persist when the $(1,2)$ wave is incorporated into an interacting solution."]
zh_spatial = [
"对于第一组单孤子解，我们观察到两个物理场的误差均集中在斜向波带附近。图 1 中，PE 与 FD 呈现相近的误差形态：$u$ 误差形成数条平行的脊线，$v$ 误差则表现为更突出的中央波带。PF 沿同一波形结构产生更大的误差。因此，表 1 中 PF 较大的最大误差对应着一段持续分布的较大偏差，而非单个孤立峰值。",
"第二组单孤子更清楚地呈现了不同表示之间的差异。图 2 中，PE 与 FD 的误差仍集中在波带附近，并具有相近的空间形态。PF 的 $v$ 误差则延伸至区域内更广的范围，在远离主要波带的位置仍明显偏高。因此，差异同时体现在误差大小和空间分布范围上，与表 1 中 PF 和 PE、FD 之间更大的 $v$ 最大误差差距相对应。",
"对于第一组二孤子解，误差曲面沿两条波支分布，并在相互作用区域附近形成突出的峰值。图 3 中，三种方法的 $v$ 误差均呈现这一结构，其最大值也彼此接近。$u$ 误差则表现出更明显的区别：PF 在相互作用附近产生更高峰值，而 PE 和 FD 保持相似的分布，幅值较小。对比上下两行可以清楚地看到这种物理场依赖性：各表示的 $v$ 误差较为接近，但在 $u$ 场上存在更明显的差异。",
"在混合极性二孤子算例中，较大误差集中在较强的负向波带附近，较小的正向结构在误差曲面中并不突出。图 4 再次呈现出 PE 与 FD 相近的误差分布，其中 FD 在两个物理场上均取得较小的最大误差。PF 则形成明显更高的误差带，尤其在 $u$ 场中。结合第一组单孤子算例可见，当 $(1,2)$ 波被纳入相互作用解后，PF 误差较大的现象仍然存在。"]
budget=list(csv.DictReader((P/"initial_error_20261020/leading_u.csv").open(encoding="utf-8")))
for lang in ("en","zh"):
    en=lang=="en"
    names=test_names if en else zh_names
    content=heading(lang,"results",3,"3.5 Numerical results" if en else "3.5 数值结果")
    content+=(r"""With these test problems, we examine how the nonlinear formulation, time integrator, and mesh choice affect the accuracy of the two physical fields. We begin by comparing PE, PF, and FD on fixed grids with RK4, using both the maximum errors and their spatial distributions to assess the differences between the formulations. We then retain the PE spatial scheme and compare Euler, RK4, and Crank–Nicolson to examine the influence of time integration. Finally, we compare fixed grids with SAMM under the same RK4 method and node count to assess the benefit of redistributing the mesh. Where relevant, we draw on the analytical error coefficients and the decomposition above to interpret the observed differences. In the tables, $e_u=E_u(T)$ and $e_v=E_v(T)$ denote the maximum absolute errors at the final time.""" if en else r"""通过上述算例，我们考察非线性表示、时间积分器和网格选择如何影响两个物理场的计算精度。首先，在固定网格上统一采用 RK4，对比 PE、PF 和 FD，并结合最大误差及其空间分布分析不同表示之间的差异。随后保持 PE 空间格式不变，比较 Euler、RK4 和 Crank–Nicolson，以考察时间积分的影响。最后，在采用相同 RK4 方法和节点数的条件下，对比固定网格与 SAMM，评价节点重新分配带来的精度改善。在相关结果的讨论中，我们结合解析误差系数与上述误差分解，解释观察到的差异。表中，$e_u=E_u(T)$ 和 $e_v=E_v(T)$ 表示终止时刻的最大绝对误差。""")
    put(lang,"results","spatial-results",content)
    content=heading(lang,"spatial-results",4,"3.5.1 Comparison of spatial discretizations" if en else "3.5.1 空间离散的比较")
    content+=(r"""We first compare PE, PF, and FD under the same grid spacing and time-stepping procedure. Starting from the continuous exact physical fields, we advance all three schemes on fixed grids with RK4 to $T=0.01$. Table 1 reports the maximum absolute errors in $u$ and $v$, allowing us to assess how the choice of formulation affects each field.""" if en else r"""我们首先在相同网格间距和时间推进方法下比较 PE、PF 和 FD。从连续精确物理场出发，三种格式均在固定网格上采用 RK4 推进至 $T=0.01$。表 1 列出 $u$ 和 $v$ 的最大绝对误差，以考察表示方式的选择如何影响各物理场。""")
    old=section(original,lang,"spatial-results","time-results")
    table=re.search(r'<div class="table-wrap">[\s\S]*?</div>',old)[0]
    content+="\n\n"+("**Table 1. Maximum absolute errors $e_u/e_v$ on fixed grids; RK4, $\\Delta x=h=0.1$, $\\Delta t=10^{-4}$, $T=0.01$. Bold values indicate the smallest error in each field.**" if en else "**表 1　固定网格的最大绝对误差 $e_u/e_v$；RK4，$\\Delta x=h=0.1$，$\\Delta t=10^{-4}$，$T=0.01$。粗体标出各物理场的最小误差。**")+"\n\n"+table
    content+="\n\n"+(r"""PE and FD give errors of comparable magnitude across the four tests, with their relative performance depending on the field and wave profile. For the $(4,-3)$ one-soliton solution and the $(6,-5;\,4,-3)$ two-soliton solution, PE gives the smaller $u$ error, while FD gives the smaller $v$ error. In the remaining two tests, FD is more accurate in both fields. Thus, even within the same wave solution, the two physical fields can respond differently to the choice of formulation.

The PF results show a stronger variation between cases. Its errors exceed those of PE and FD in both fields throughout the table, but the size of the difference changes substantially. For the first two-soliton test, its $v$ error is close to those of the other two methods; for the $(4,-3)$ one-soliton test, it is more than an order of magnitude larger. Although PE and PF represent the same semi-discrete system, their different variables and the subsequent numerical operations lead to distinct accuracy after full discretization.

To see where these differences arise in space, we next examine the absolute-error surfaces in Figures 1–4. The columns show PE, PF, and FD from left to right, with the $u$ error in the upper row and the $v$ error in the lower row. For each field, the three methods share the same colour and height scales, so that both the magnitude and spatial distribution of the errors can be compared directly.""" if en else r"""四组算例中，PE 与 FD 的误差处于相近量级，两者的相对表现随物理场和波形变化。对于 $(4,-3)$ 单孤子和 $(6,-5;\,4,-3)$ 二孤子，PE 的 $u$ 误差更小，而 FD 的 $v$ 误差更小。另外两组算例中，FD 对两个物理场均具有更高精度。因此，即使对于同一个波解，两个物理场对表示方式的选择也可能呈现不同响应。

PF 的结果表现出更明显的算例差异。各组算例的两个物理场误差均大于 PE 和 FD，但差距大小变化显著。第一组二孤子中，其 $v$ 误差与另外两种方法接近；而在 $(4,-3)$ 单孤子中，其 $v$ 误差高出一个数量级以上。尽管 PE 和 PF 表示同一个半离散系统，两者采用的变量及后续数值运算不同，使其在完全离散后呈现不同精度。

为了观察这些差异在空间中的分布，我们接下来考察图 1—4 的绝对误差曲面。各列从左至右依次对应 PE、PF 和 FD，上行为 $u$ 误差，下行为 $v$ 误差。同一物理场采用共同色阶和高度范围，以便直接比较误差大小及空间分布。""")
    for i,case in enumerate("ABCD"):
        content+="\n\n"+(en_spatial if en else zh_spatial)[i]+"\n\n"+fig(case+"_errors3d.png",f"Figure {i+1}. {names[i]}: absolute-error surfaces at T=0.01." if en else f"图 {i+1}　{names[i]}：T=0.01 时的绝对误差曲面。")
    content+="\n\n"+(r"""To interpret these spatial comparisons, we return to the two contributions identified in Section 3.4. For PE and PF, the exact semi-discrete fields differ from the continuous fields by $h^2C+O(h^4)$, where $C=(C_U,C_V)$ describes the leading spatial distribution of the lattice error. Since both formulations share the same exact semi-discrete physical fields, this contribution is common to them. Their different errors in Table 1 and Figures 1–4 therefore arise from the numerical contribution: the choice of evolved variables, their subsequent discretization, and the recovery of the physical fields lead to different approximations of the same semi-discrete solution.

To understand the relative performance of PE and FD more quantitatively, we evaluate their spatial truncation errors on the continuous exact fields at $t=0$. For the approximation of $u_t$, the leading error takes the form""" if en else r"""为解释上述空间离散的比较结果，我们回到第 3.4 节区分的两项误差贡献。对于 PE 和 PF，半离散精确场与连续精确场之差为 $h^2C+O(h^4)$，其中 $C=(C_U,C_V)$ 刻画格点误差的首项空间分布。由于两种表示具有相同的半离散精确物理场，这部分贡献也是共同的。因此，表 1 和图 1—4 中两者的误差差异来自数值误差部分：演化变量的选择、后续离散及物理场恢复，使它们对同一半离散解形成不同的数值近似。

为更定量地理解 PE 与 FD 的相对表现，我们将 $t=0$ 的连续精确场代入两种格式，计算其空间截断误差。对于 $u_t$ 的近似，误差首项为""")
    content+=r"""

$$r_m^u=\underbrace{(\Delta x)^2B}_{X}+\underbrace{h^2A_m}_{Y_m}
+O\!\left((\Delta x)^4+(\Delta x)^2h^2+h^4\right),\qquad m=\mathrm{PE},\mathrm{FD}.$$
"""
    content+="\n"+(r"""Here $B$ is the common $x$-discretization coefficient discussed in Section 3.1, while $A_m$ describes the contribution from discretizing $y$. With $[f]_b^y=f(x,y,0)-f(x,b,0)$, the latter coefficients are""" if en else r"""其中 $B$ 是第 3.1 节讨论的共同 $x$ 向离散误差系数，$A_m$ 描述离散化 $y$ 的贡献。记 $[f]_b^y=f(x,y,0)-f(x,b,0)$，则""")
    content+=r"""

$$A_{\mathrm{FD}}=-\frac1{12}\partial_x^2[v_y]_b^y,\qquad
A_{\mathrm{PE}}=A_{\mathrm{FD}}-\partial_x\left[\frac{(v-u_y)^2}{32}-\frac{v-u_y}{4}\right]_b^y+\frac14\partial_x^2[u_{yy}]_b^y.$$
"""
    content+="\n"+(r"""PE therefore changes both the magnitude of the $y$ contribution and its spatial relation to the common $x$ contribution. We measure this relation using the normalized spatial inner product""" if en else r"""因此，PE 不仅改变了 $y$ 向贡献的大小，也改变了它与共同 $x$ 向贡献之间的空间关系。我们利用归一化空间内积衡量这种关系：""")
    content+=r"""

$$\gamma_m=\frac{\langle X,Y_m\rangle}{\|X\|_{\mathrm{RMS}}\|Y_m\|_{\mathrm{RMS}}},
\qquad \langle X,Y_m\rangle=\frac1{|\mathcal G|}\sum_{\mathcal G}XY_m.$$
"""
    content+="\n"+("For nonzero component norms, the resulting identity is" if en else "当分项范数非零时，相应恒等式为")+"\n\n"+f'<a id="{lang}-eq-207"></a>\n\n'
    content+=r"$$\|X+Y_m\|_{\mathrm{RMS}}^2=\|X\|_{\mathrm{RMS}}^2+\|Y_m\|_{\mathrm{RMS}}^2+2\gamma_m\|X\|_{\mathrm{RMS}}\|Y_m\|_{\mathrm{RMS}}.\tag{84}$$"
    content+="\n\n"+(r"""A negative $\gamma_m$ reduces the squared norm through cancellation, whereas a positive value increases it. Table 2 evaluates these leading contributions at $t=0$ with $\Delta x=h=0.1$, using RMS values and inner products on the grid points in the four test regions.""" if en else r"""$\gamma_m<0$ 时，交叉项通过抵消降低合成误差的平方范数；正值则增大这一范数。表 2 给出 $\Delta x=h=0.1$、$t=0$ 时四组算例的首项贡献，RMS 与内积均在相应区域的格点上计算。""")
    content+="\n\n"+("**Table 2. Leading spatial truncation-error contributions to $u_t$ at $t=0$.**" if en else "**表 2　$t=0$ 时 $u_t$ 的空间截断误差首项贡献。**")
    content+="\n\n| "+("Test | Method" if en else "算例 | 方法")+r" | $\|X\|_{\mathrm{RMS}}$ | $\|Y_m\|_{\mathrm{RMS}}$ | $\gamma_m$ | $\|X+Y_m\|_{\mathrm{RMS}}$ |"+"\n|---|---|---:|---:|---:|---:|\n"
    for row in budget:
        i="ABCD".index(row["case"])
        content+=f'| {names[i]} | {row["method"]} | {float(row["rms_x"]):.5e} | {float(row["rms_y"]):.5e} | {float(row["cosine"]):+.4f} | {float(row["rms_sum"]):.5e} |\n'
    content+="\n"+(r"""The leading expressions agree closely with the full spatial residuals, with relative RMS differences of $0.12\%$–$2.12\%$.

This analysis gives a quantitative explanation for the change in relative accuracy between PE and FD. The two methods share the leading $x$-discretization contribution, while their different treatments of $y$ produce different spatial error distributions. For the $(1,2)$ one-soliton and mixed-polarity two-soliton solutions, the FD $y$ contribution reduces the combined spatial residual, whereas the PE contribution increases it. For the other two solutions, this relation is reversed, and PE gives the smaller residual. The resulting ordering agrees with the final maximum $u$ errors in all four tests. We thus relate the observed differences between the two spatial schemes to their $y$-error coefficients evaluated on each wave profile, together with the common error introduced by the $x$ discretization.

Having compared the spatial formulations, we retain PE in the following experiments and examine how its accuracy changes with the time integrator and mesh placement.""" if en else r"""首项表达式与完整空间残差吻合良好，相对 RMS 差异为 $0.12\%$–$2.12\%$。

这一分析为 PE 与 FD 相对精度的变化提供了定量解释。两种方法具有共同的 $x$ 向离散误差首项，而它们对 $y$ 方向的不同处理产生不同的空间误差分布。对于 $(1,2)$ 单孤子和混合极性二孤子，FD 的 $y$ 向贡献减小了合成空间残差，而 PE 的贡献增大残差。另外两组解中，这一关系反转，PE 得到较小残差。由此得到的排序与四组算例中终止时刻的 $u$ 最大误差一致。因此，我们将两种空间格式所呈现的精度差异，具体联系到各自的 $y$ 向误差系数在不同波形上的取值，以及它们与共同 $x$ 向离散误差的叠加结果。

在完成空间表示的比较后，下面的实验保持 PE 不变，考察其精度如何随时间积分器和网格布置而变化。""")
    put(lang,"spatial-results","time-results",content)

time_en=[
"For the $(1,2)$ one-soliton solution, all three methods produce closely matched error profiles. The enlargements reveal a small difference near the peaks: Euler gives a slightly smaller $u$ error and a slightly larger $v$ error, while Crank–Nicolson and RK4 remain nearly indistinguishable.",
"The $(4,-3)$ one-soliton test shows a more visible response to the choice of integrator. Euler changes the shape of the $u$-error profile, although its maximum remains close to those of the other two methods. In $v$, the difference extends across a broad part of the wave profile, where Euler produces a higher error plateau.",
"For the $(6,-5;\\,4,-3)$ two-soliton solution, we also observe a change in the location of the dominant $u$-error peak. Euler gives a smaller error near the RK4 peak shown in the inset, but develops a higher peak elsewhere. Its larger maximum in the table therefore reflects a redistribution of the error along the profile. In $v$, the main peak is higher for Euler, while the RK4 and Crank–Nicolson profiles remain closely matched.",
"The mixed-polarity two-soliton solution returns to the pattern observed in the first test. The three profiles are close over the region, with Euler giving a slightly lower $u$-error peak and a slightly higher $v$-error peak. The agreement between Crank–Nicolson and RK4 again holds throughout the profiles, including the enlarged regions."]
time_zh=[
"对于 $(1,2)$ 单孤子，三种方法的误差剖面十分接近。局部放大显示了峰值附近的细微差异：Euler 的 $u$ 误差略小，$v$ 误差略大，而 Crank–Nicolson 与 RK4 几乎无法区分。",
"$(4,-3)$ 单孤子对积分器选择的响应更明显。Euler 改变了 $u$ 误差剖面的形状，但最大值仍与另外两种方法接近。在 $v$ 场中，差异延伸至波形较宽的部分，Euler 产生了更高的误差平台。",
"对于 $(6,-5;\\,4,-3)$ 二孤子，我们还观察到主导 $u$ 误差峰值位置的变化。Euler 在放大图所示的 RK4 峰值附近给出较小误差，却在其他位置形成更高峰值。因此，表中更大的最大误差体现了误差沿剖面的重新分布。在 $v$ 场中，Euler 的主峰更高，RK4 与 Crank–Nicolson 的剖面则仍十分接近。",
"混合极性二孤子再次呈现第一组算例中的模式。三种剖面在区域内较为接近，Euler 的 $u$ 误差峰值略低，$v$ 误差峰值略高。Crank–Nicolson 与 RK4 在整个剖面中再次保持吻合，包括局部放大的区域。"]
mesh_en=[
"For the $(1,2)$ one-soliton solution, the adaptive mesh lowers the dominant $u$-error peak and reduces the broad elevated portion of the $v$-error profile. The latter improvement extends across much of the wave region, accompanying the largest relative reduction in the table.",
"The $(4,-3)$ one-soliton solution shows a smaller but sustained improvement. SAMM lowers the broad central portions of both error profiles while preserving their overall shape. The reductions in the maximum errors therefore accompany a decrease over an extended part of the region.",
"For the $(6,-5;\\,4,-3)$ two-soliton solution, we observe the clearest reductions near the principal error peaks around the interaction region. The profiles remain close along several of the separated wave branches. This case connects the node-spacing illustration above with the accuracy comparison: the modest redistribution of the shared $x$ mesh is accompanied by reductions of $6.99\\%$ and $5.59\\%$ in the maximum $u$ and $v$ errors, respectively.",
"In the mixed-polarity two-soliton test, SAMM lowers the broad central portions of both profiles. The narrow peak that determines the maximum $u$ error changes less, giving a reduction of $2.73\\%$, while the maximum $v$ error decreases by $5.51\\%$. The spatial profiles thus reveal improvements beyond those summarized by the single largest error."]
mesh_zh=[
"对于 $(1,2)$ 单孤子，自适应网格降低了主导的 $u$ 误差峰值，并减小了 $v$ 误差剖面中较宽的高值区域。后者的改善延伸至波形区域的大部分位置，对应表中最大的相对降幅。",
"$(4,-3)$ 单孤子的改善幅度较小，但分布持续。SAMM 降低了两个误差剖面较宽的中央部分，同时保持整体形态。因此，最大误差的下降也伴随着区域内较大范围的误差减小。",
"对于 $(6,-5;\\,4,-3)$ 二孤子，最明显的下降出现在相互作用区域附近的主要误差峰值处，而若干分离波支上的剖面仍较接近。这将前面的节点间距图与精度比较联系起来：共享 $x$ 网格的适度重新分配，伴随着 $u$、$v$ 最大误差分别下降 $6.99\\%$ 和 $5.59\\%$。",
"混合极性二孤子中，SAMM 降低了两个剖面较宽的中央部分。决定 $u$ 最大误差的窄峰变化较小，降幅为 $2.73\\%$，而 $v$ 最大误差下降 $5.51\\%$。因此，空间剖面展示了单个最大误差指标之外的改善。"]
for lang in ("en","zh"):
    en=lang=="en"
    names=test_names if en else zh_names
    content=heading(lang,"time-results",4,"3.5.2 Time integration of PE" if en else "3.5.2 PE 的时间推进比较")
    content+=(r"""Having examined the spatial discretizations, we now retain the fixed-grid PE scheme and compare forward Euler, RK4, and Crank–Nicolson. All three methods start from the same initial data and advance to $T=0.01$, with $\Delta x=h=0.1$ and $\Delta t=10^{-4}$. We examine both the maximum errors and their spatial profiles to see how changing the time integrator affects the accuracy of each physical field.

The maximum absolute errors are listed in Table 3. Crank–Nicolson and RK4 give closely matched results in all four tests. Euler produces more noticeable differences: it gives a smaller maximum $u$ error for the $(1,2)$ one-soliton and mixed-polarity two-soliton solutions, whereas RK4 gives the smaller $u$ error in the other two tests. For $v$, RK4 gives the smallest maximum error in all four cases.""" if en else r"""在考察空间离散之后，我们保持固定网格 PE 格式不变，比较前向 Euler、RK4 和 Crank–Nicolson。三种方法均从相同初值出发，以 $\Delta x=h=0.1$、$\Delta t=10^{-4}$ 推进至 $T=0.01$。我们同时考察最大误差及其空间剖面，观察改变时间积分器如何影响各物理场的精度。

最大绝对误差列于表 3。四组算例中 Crank–Nicolson 与 RK4 的结果十分接近。Euler 带来的差异更明显：在 $(1,2)$ 单孤子和混合极性二孤子中，它给出较小的 $u$ 最大误差；另外两组中，RK4 的 $u$ 误差更小。对于 $v$，四组算例均由 RK4 取得最小的最大误差。""")
    table=re.search(r'<div class="table-wrap">[\s\S]*?</div>',section(original,lang,"app-f","references"))[0]
    content+="\n\n"+("**Table 3. Maximum absolute errors $e_u/e_v$ for PE with Euler, RK4 and Crank–Nicolson. Fixed grids; $T=0.01$, $\\Delta x=h=0.1$, $\\Delta t=10^{-4}$.**" if en else "**表 3　PE 采用 Euler、RK4 与 Crank–Nicolson 的最大绝对误差 $e_u/e_v$。固定网格；$T=0.01$、$\\Delta x=h=0.1$、$\\Delta t=10^{-4}$。**")+"\n\n"+table
    content+="\n\n"+("We next examine the spatial error profiles" if en else "接下来考察空间误差剖面")
    content+=r"""

$$\varepsilon_u^{(m)}(x)=\max_j|u_m(x,y_j,T)-u_*(x,y_j,T)|,\qquad
\varepsilon_v^{(m)}(x)=\max_j|v_m(x,y_j,T)-v_*(x,y_j,T)|.$$
"""
    content+="\n"+("Here $m$ denotes the time integrator. For each test, we show the two physical fields side by side and include local enlargements near the RK4 error peaks." if en else "其中 $m$ 表示时间积分器。每组算例均将两个物理场并排展示，并在 RK4 误差峰值附近给出局部放大。")
    for i in range(4):
        cap=(f"Figure {5+i}. {names[i]} at T=0.01. Left: u; right: v. Euler: orange; RK4: blue; C–N: purple dashed. Insets enlarge the RK4 peak neighbourhoods." if en else f"图 {5+i}　{names[i]}，T=0.01。左：u；右：v。橙色：Euler；蓝色：RK4；紫色虚线：C–N。插图放大 RK4 峰值附近。")
        content+="\n\n"+(time_en if en else time_zh)[i]+"\n\n"+rowfig("time",i,cap)
    content+="\n\n"+(r"""Across these tests, changing the time integrator affects both the size and location of errors within the spatially discretized solution. Crank–Nicolson and RK4 yield almost the same profiles at the chosen resolution, whereas Euler produces changes that depend on the wave and the physical field. We retain RK4 in the following experiments to examine the effect of mesh adaptation under a common time-stepping procedure.""" if en else r"""这些算例表明，改变时间积分器会影响空间离散解中误差的大小和位置。在所选分辨率下，Crank–Nicolson 与 RK4 给出几乎相同的剖面，而 Euler 引起的变化依赖于波形和物理场。接下来的实验继续采用 RK4，在共同的时间推进方法下考察网格自适应的作用。""")
    put(lang,"time-results","mesh-results",content)
    content=heading(lang,"mesh-results",4,"3.5.3 Numerical performance of the self-adaptive moving mesh method" if en else "3.5.3 自适应动网格方法的数值表现")
    content+=(r"""We now examine whether the conservation-based mesh adaptation introduced in Section 3.2 improves the accuracy of PE with the same number of nodes. Both the fixed-grid and adaptive calculations use RK4, $\Delta t=10^{-4}$, and the uniform $y$ spacing $h=0.1$. For SAMM, the transversely averaged conservation density determines the initial distribution of the $x$ nodes, which subsequently evolve together with the physical fields.

We first illustrate this redistribution using the $(6,-5;\,4,-3)$ two-soliton solution. Figure 9 shows the local node spacing normalized by the uniform spacing $\Delta x=0.1$, plotted at the midpoint of each interval. Values below one indicate a higher concentration of nodes, while values above one indicate wider spacing.""" if en else r"""下面，我们考察第 3.2 节基于守恒律构造的网格自适应，能否在相同节点数下提高 PE 的计算精度。固定网格与自适应计算均采用 RK4、$\Delta t=10^{-4}$ 及均匀的 $y$ 向间距 $h=0.1$。对于 SAMM，横向平均守恒密度确定 $x$ 节点的初始分布，随后节点与物理场共同演化。

我们首先以 $(6,-5;\,4,-3)$ 二孤子说明这种重新分配。图 9 将各区间局部节点间距除以均匀间距 $\Delta x=0.1$，并在区间中点绘制。小于 1 的值表示节点更集中，大于 1 的值表示间距更宽。""")
    content+="\n\n"+fig("SAMM_spacing_C.png","Figure 9. Normalized local x spacing for the (6,−5; 4,−3) two-soliton solution. Grey dashed: adaptive initial mesh; blue: T=0.01; orange dotted: uniform mesh." if en else "图 9　(6,−5; 4,−3) 二孤子的归一化局部 x 间距。灰色虚线：自适应初始网格；蓝色：T=0.01；橙色点线：均匀网格。")
    content+="\n\n"+(r"""The adaptive mesh concentrates nodes in the central part of the region, with the smallest spacing near $x=0$, and compensates with slightly wider intervals farther away. At $T=0.01$, the minimum spacing is approximately $0.09834$, compared with $0.1$ on the uniform grid. The initial and final spacing curves nearly coincide over this short interval, so the displayed distribution is largely established by the initial adaptation and then adjusted during evolution.

To assess the effect on accuracy, we compare the maximum absolute errors in both physical fields. Table 4 also gives the percentage reduction relative to the fixed mesh,""" if en else r"""自适应网格将节点集中在区域中央，最小间距出现在 $x=0$ 附近，并以远处略宽的区间进行补偿。在 $T=0.01$ 时，最小间距约为 $0.09834$，均匀网格间距则为 $0.1$。在这一短时间区间内，初始与最终间距曲线几乎重合，因此所示分布主要由初始自适应建立，并在演化中继续调整。

为评价精度变化，我们比较两个物理场的最大绝对误差。表 4 还给出相对于固定网格的误差下降百分比：""")
    content+=r"""

$$\mathcal R_f=100\left(1-\frac{E_f^{\mathrm{SAMM}}(T)}{E_f^{\mathrm{fixed}}(T)}\right)\%,\qquad f=u,v.$$
"""
    table=re.search(r'<div class="table-wrap">[\s\S]*?</div>',section(original,lang,"mesh-results","conclusion"))[0]
    table=table.replace("</tr></thead>","<th>"+("Reduction: u / v" if en else "降幅：u / v")+"</th></tr></thead>")
    reductions=["9.75% / 18.50%","6.00% / 4.54%","6.99% / 5.59%","2.73% / 5.51%"]
    it=iter(reductions)
    head,body=table.split("<tbody>",1)
    body=re.sub(r"(<tr><th>[\s\S]*?</tr>)",lambda m:m[0].replace("</tr>","<td>"+next(it)+"</td></tr>"),body)
    table=head+"<tbody>"+body
    content+="\n"+("**Table 4. Maximum absolute errors $e_u/e_v$ of PE on fixed and adaptive meshes at $T=0.01$, with the same node count and RK4 integrator.**" if en else "**表 4　PE 在 $T=0.01$ 时固定网格与自适应网格的最大绝对误差 $e_u/e_v$；节点数及 RK4 积分器相同。**")+"\n\n"+table
    content+="\n\n"+(r"""SAMM reduces the maximum errors in both fields for all four tests. The improvement ranges from $2.73\%$ to $9.75\%$ in $u$ and from $4.54\%$ to $18.50\%$ in $v$. To see where these gains occur, we examine the spatial error profiles defined in the preceding subsection.""" if en else r"""SAMM 降低了四组算例中两个物理场的最大误差。$u$ 的改善范围为 $2.73\%$–$9.75\%$，$v$ 为 $4.54\%$–$18.50\%$。为了观察改善出现的位置，我们考察上一小节定义的空间误差剖面。""")
    for i in range(4):
        cap=(f"Figure {10+i}. Fixed-grid and SAMM error profiles for {names[i]} at T=0.01. Left: u; right: v. Orange dashed with open circles: fixed mesh; blue: SAMM." if en else f"图 {10+i}　{names[i]} 在 T=0.01 时的固定网格与 SAMM 误差剖面。左：u；右：v。橙色虚线与空心圆：固定网格；蓝色：SAMM。")
        content+="\n\n"+(mesh_en if en else mesh_zh)[i]+"\n\n"+rowfig("mesh",i,cap)
    content+="\n\n"+(r"""Through these comparisons, we find that the conservation-based density provides a useful basis for allocating the shared $x$ nodes. Although the density is constructed from $W=v-\delta_0u$ and averaged over $y$, the resulting mesh improves the maximum-error accuracy of both physical fields in every test considered. The degree and location of the improvement vary with the wave profile, while the node count and time integrator remain unchanged.""" if en else r"""通过这些比较，我们看到基于守恒律的密度为共享 $x$ 节点的配置提供了有效依据。尽管密度由 $W=v-\delta_0u$ 构造并在 $y$ 方向平均，所得网格仍改善了全部算例中两个物理场的最大误差精度。改善幅度及位置随波形变化，而节点数与时间积分器保持不变。""")
    put(lang,"mesh-results","conclusion",content)

EN_CONCLUSION=r"""
In this work, we have connected the construction of an integrable semi-discrete DLW system with an analysis of its numerical approximation. Starting from the continuous bilinear equations, we introduced a staggered lattice in $y$, coupled to shifts of the bilinear operator parameter, while keeping $x$ and $t$ continuous. The resulting system retains Gram determinant solutions of arbitrary finite order. From this construction, eliminating or retaining the auxiliary potential leads to the PE and PF formulations, for which we established Darboux–Lax representations and their compatibility with the nonlinear equations.

The explicit solutions also allow us to follow how the discrete wave fields approach their continuous counterparts. Under the stated regularity and positivity assumptions, we proved second-order convergence of these fields, alongside second-order consistency of the equations. By deriving the leading error coefficients, we further identified the spatial changes introduced by the lattice. These coefficients give a concrete connection between the analytical construction and the errors examined in the numerical experiments.

When the remaining variables are discretized, the choice of nonlinear formulation becomes consequential. Although PE and PF describe the same exact semi-discrete physical fields, their numerical implementations give different error magnitudes and distributions, with PE attaining smaller maximum errors in both fields throughout the four tests. The comparison with FD presents a more varied picture: the relative accuracy changes with the wave profile and the physical field. For $u$, our analysis relates this variation to the different $y$-error coefficients acting together with a common leading $x$-discretization contribution. Evaluating these contributions at $t=0$ gives the same PE–FD ordering as the final maximum $u$ errors in all four cases. This agreement helps explain how the different spatial discretizations produce the observed accuracy, beyond a comparison of their formal orders.

With PE as the spatial formulation, we then examined how time integration and node placement affect the computation. At the tested resolution, Crank–Nicolson and RK4 give nearly coincident error profiles, while Euler produces changes that depend on the wave and the field. Mesh adaptation offers a further way to improve the approximation within the same formulation. Using the semi-discrete conservation law, we constructed a shared adaptive $x$ mesh that evolves with the fields while retaining a uniform $y$ lattice. With the node count and RK4 integrator unchanged, the adaptive mesh reduces the maximum errors in both fields across all four tests, by $2.73\%$–$9.75\%$ in $u$ and $4.54\%$–$18.50\%$ in $v$. In this way, the conservation law obtained from the semi-discrete system also guides the allocation of numerical resolution, improving the computed wave profiles with the available nodes.

Our work illustrates how the analytical structure of a semi-discrete system can inform both the interpretation and the design of its numerical approximation. The exact solutions let us follow the changes introduced by the lattice, while the error coefficients help explain why different discretizations perform differently on the same waves. The conservation law, in turn, provides a way to use this structure in allocating the computational nodes. By bringing these aspects together, we move from constructing a discrete equation with explicit solutions to understanding how its formulation and implementation shape the accuracy of the computed fields. This connection offers a basis for further developments in which analytical properties guide the choices made in numerical computation.
"""
ZH_CONCLUSION=r"""
本文将可积半离散 DLW 系统的构造与其数值近似分析联系起来。我们从连续双线性方程出发，在 $y$ 方向引入交错格点，并将其与双线性算子参数的平移结合，同时保持 $x$ 和 $t$ 连续。所得系统保留了任意有限阶的 Gram 行列式解。在这一构造的基础上，消去或保留辅助势分别得到 PE 和 PF 表示，我们进一步建立了它们的 Darboux–Lax 表示及其与非线性方程的相容性。

显式解也使我们能够具体考察离散波场如何趋近于相应的连续波场。在所述正则性和正性假设下，我们证明了这些物理场的二阶收敛性，以及方程的二阶相容性。通过推导误差首项系数，我们进一步刻画了格点引入的空间变化。这些系数在解析构造与数值实验所考察的误差之间建立了具体联系。

当其余变量进一步离散化时，非线性表示的选择开始影响计算结果。尽管 PE 和 PF 描述相同的半离散精确物理场，它们的数值实现仍产生不同的误差大小和分布，且四组算例中 PE 在两个物理场上均取得较小的最大误差。与 FD 的比较则呈现出更丰富的情况：相对精度随波形和物理场而改变。对于 $u$，我们的分析将这种变化联系到不同的 $y$ 向误差系数，以及它们与共同的 $x$ 向离散误差首项的作用。在 $t=0$ 处计算这些贡献，得到的 PE–FD 排序与四组算例终止时刻的 $u$ 最大误差排序一致。这种吻合使我们能够超出形式误差阶的比较，进一步解释不同空间离散为何呈现出所观察到的精度。

在采用 PE 空间表示的基础上，我们随后考察了时间积分和节点配置对计算的影响。在所测试的分辨率下，Crank–Nicolson 与 RK4 给出几乎重合的误差剖面，而 Euler 引起的变化则依赖于波形和物理场。网格自适应为同一表示下的精度改善提供了另一条途径。利用半离散系统的守恒律，我们构造了与物理场共同演化的共享自适应 $x$ 网格，同时保持 $y$ 向格点均匀。在节点数和 RK4 积分器均不变的条件下，自适应网格降低了四组算例中两个物理场的最大误差，其中 $u$ 的降幅为 $2.73\%$–$9.75\%$，$v$ 的降幅为 $4.54\%$–$18.50\%$。由此，从半离散系统得到的守恒律也用于指导数值分辨率的分配，使既有节点能够更准确地描述波形。

我们的工作展示了半离散系统的解析结构如何同时参与数值近似的解释与设计。精确解使我们能够追踪格点引入的变化，误差系数帮助解释不同离散方法为何在同一波形上表现不同，而守恒律则提供了利用这些结构配置计算节点的途径。通过将这些方面联系起来，我们的研究从构造具有显式解的离散方程，进一步走向理解其表示方式与数值实现如何影响物理场的计算精度。这种联系也为后续研究提供了基础，使解析性质能够具体地指导数值计算中的方法选择。
"""
for lang in ("en","zh"):
    en=lang=="en"
    put(lang,"conclusion","app-a",heading(lang,"conclusion",2,"4. Conclusion" if en else "4. 结论")+(EN_CONCLUSION if en else ZH_CONCLUSION))
    content=heading(lang,"app-f",2,"Appendix F. Implicit time stepping" if en else "附录 F. 隐式时间推进")
    content+=("The Crank–Nicolson method averages the rates at adjacent time levels:" if en else "Crank–Nicolson 方法对相邻时间层的变化率取平均：")+"\n\n"+eq(lang,111)
    content+="\n\n"+(r"""For the fixed-grid PE calculation, $z$ collects $P,W$. We begin with the forward Euler predictor $z^{(0)}=z^n+\Delta t\,\mathcal F(t_n,z^n)$ and use the residual correction
$$z^{(r+1)}=z^{(r)}-\mathcal R(z^{(r)}),$$
where $\mathcal R$ is the nonlinear residual defined in Section 3.3. At each evaluation, the physical fields are recovered and the boundary data are applied at the corresponding time. We accept the iterate when
$$\|\mathcal R(z^{(r)})\|_\infty\le 10^{-12}+10^{-11}\max(1,\|z^n\|_\infty).$$
The iteration is allowed up to 80 residual evaluations. The numerical comparison with Euler and RK4, including the error table and spatial profiles, is presented in [Section 3.5.2](#en-time-results).""" if en else r"""对于固定网格 PE 计算，$z$ 包含 $P,W$。我们以 Euler 预测值 $z^{(0)}=z^n+\Delta t\,\mathcal F(t_n,z^n)$ 为初值，采用残差修正
$$z^{(r+1)}=z^{(r)}-\mathcal R(z^{(r)}),$$
其中 $\mathcal R$ 为第 3.3 节定义的非线性残差。每次求值时恢复物理场，并在相应时刻施加边界数据。当
$$\|\mathcal R(z^{(r)})\|_\infty\le 10^{-12}+10^{-11}\max(1,\|z^n\|_\infty)$$
时接受该迭代值，最多允许 80 次残差求值。与 Euler 和 RK4 的数值比较，包括误差表及空间剖面，见[第 3.5.2 节](#zh-time-results)。""")
    put(lang,"app-f","references",content)

s=s.replace("$Q、R$","$Q,R$")
# Align the introductory roadmap with the approved terminology.
s=s.replace("in the reconstructed $u$ evolution","in the approximation of $u_t$")
# Keep all equation identifiers stable and ensure the only removed tag was relocated.
tags=re.findall(r"\\tag\{(\d+)\}",s)
assert tags==[str(i) for i in range(1,112)]*2, tags
# Intro and theoretical section must be unchanged apart from roadmap terminology.
for lang in ("en","zh"):
    start=original.index("{#"+lang+"-numerics}")
    # Compare through the heading prefix; the source before Section 3 is untouched.
    old_prefix=original[:start] if lang=="en" else original[original.index("{#zh-title}"):start]
    new_start=s.index("{#"+lang+"-numerics}")
    new_prefix=s[:new_start] if lang=="en" else s[s.index("{#zh-title}"):new_start]
    assert old_prefix.replace("in the reconstructed $u$ evolution","in the approximation of $u_t$")==new_prefix
SOURCE.write_text(s,encoding="utf-8")
(backup/"receipt.json").write_text(json.dumps({"scope":"Approved Section 3 and conclusion; Appendix F comparison moved to body",
    "equations_per_language":111,"backup":str(backup),"figure_split":"HTML viewports of unchanged original scientific images",
    "conclusion":"Original significance paragraph restored; two later additions excluded"},indent=2),encoding="utf-8")
print(str(backup))
