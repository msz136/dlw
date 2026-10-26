from pathlib import Path
import re, json
root=Path('review')
original=(root/'manuscript.md').read_text(encoding='utf8')
en,zh=original.split('# （2+1）维色散长波系统的可积半离散化',1)
zh='# （2+1）维色散长波系统的可积半离散化'+zh

def eq(lang,n,tex):
    return f'\n\n<a id="{lang}-eq-{n}"></a>\n\n$$'+tex+f'\\tag{{{n}}}$$\n\n'

def revise(s,l):
    en=l=='en'; app=[]
    def move(start,end,title,replacement):
        nonlocal s
        a=s.index(start); b=s.index(end,a)
        app.append((title,s[a:b].strip()))
        s=s[:a]+replacement+'\n\n'+s[b:]
    # Keep the lemma and its use in the main proof; relocate auxiliary matrix algebra.
    move('**Proof.** Write the nth Gram matrix' if en else '**证明。** 将第 n 层 Gram 矩阵',
         '**Proof of Theorem 2.2.**' if en else '**定理 2.2 的证明。**',
         'B. Adjacent-layer determinant identity' if en else 'B. 相邻层行列式恒等式',
         '**Proof.** The matrix determinant lemma and differentiated rank-one identities give the result; the calculation, including continuation to singular matrices, is given in [Appendix B](#en-app-b). □' if en else '**证明。** 由矩阵行列式引理及秩一恒等式的微分可得结论；包括奇异矩阵延拓在内的计算见[附录 B](#zh-app-b)。□')
    # Full Darboux calculation is retained, with the compatibility argument in the body.
    move('**Proof.** Set\n\n<a id="en-eq-73"' if en else '**证明。** 令\n\n<a id="zh-eq-73"',
         'For τ-function solutions, take' if en else '对于 τ 函数解，可取',
         'C. Darboux operator calculation' if en else 'C. Darboux 算子计算',
         '**Proof.** Factor the lattice transfer as $T_j=\mathscr B_j^{-1}\mathscr A_j$, with $\mathscr A_j=\partial_x-U_j/2-hw_j/8$ and $\mathscr B_j=\partial_x-U_j/2+hw_j/8$. The field equations make both scalar Darboux residuals vanish and give a common intermediate potential, hence $T_{j,t}=H_{j+1}T_j-T_jH_j$. Conversely, the coefficients of orders zero and minus one imply vanishing of both residuals when $w_j\\ne0$. Their sum and difference recover the field equations. The operator identities are recorded in [Appendix C](#en-app-c). □' if en else '**证明。** 将格点转移分解为 $T_j=\mathscr B_j^{-1}\mathscr A_j$，其中 $\mathscr A_j=\partial_x-U_j/2-hw_j/8$、$\mathscr B_j=\partial_x-U_j/2+hw_j/8$。场方程使两个标量 Darboux 残差均为零，并给出共同的中间势，从而 $T_{j,t}=H_{j+1}T_j-T_jH_j$。反之，零阶与负一阶系数在 $w_j\\ne0$ 时迫使两残差为零，其和与差恢复场方程。算子恒等式见[附录 C](#zh-app-c)。□')
    # PE cumulative reconstruction moves, while variables and final evolution remain.
    a=s.index('At each time, the physical fields are reconstructed by' if en else '在每个时刻，通过')
    b=s.index('<a id="'+l+'-eq-90"',a)
    block=s[a:b]
    app.append(('D. Reconstruction and boundary initialization' if en else 'D. 重构与边界初始化',block))
    s=s[:a]+('The lower boundary value fixes u by cumulative summation of P, and $v=W+\delta_0u$; see [Appendix D](#en-app-d). The evolution equations are $\dot P=F_P$, $\dot W=F_W$, with\n\n' if en else '由下边界值及 P 的累积和确定 u，再令 $v=W+\delta_0u$，见[附录 D](#zh-app-d)。演化方程为 $\dot P=F_P$、$\dot W=F_W$，其中\n\n')+s[b:]
    a=s.index('The evolution equations also contain' if en else '恢复。演化方程还包含')
    b=s.index('<a id="'+l+'-eq-94"',a)
    app[-1]=(app[-1][0],app[-1][1]+'\n\n'+s[a:b])
    s=s[:a]+('Here $m_j\simeq M_{j,x}$ is obtained from the lattice constraint and lower boundary data as detailed in Appendix D. The final rates are\n\n' if en else '恢复。其中 $m_j\simeq M_{j,x}$ 由格点约束和下边界数据确定，详见附录 D。最终演化右端为\n\n')+s[b:]
    move('The physical x spacings become nonuniform' if en else '物理节点移动后，',
         '### 3.3 ',
         'E. Derivatives on moving nodes' if en else 'E. 移动节点上的导数',
         'On moving nodes, use the mapped centred operators in [Appendix E](#en-app-e) and evolve $\dot z=F_z+\mathcal V D_1z$ together with (100). The mapping Jacobian must remain positive. The fixed grid has $\mathcal V=0$.' if en else '移动节点上采用[附录 E](#zh-app-e)的映射中心差分，将 $\dot z=F_z+\mathcal V D_1z$ 与 (100) 联立推进，并要求映射 Jacobian 保持正值。固定网格对应 $\mathcal V=0$。')
    # Remove elementary Euler formula; retain C–N implementation in an appendix.
    a=s.index('With $t_n=n' if en else '取 $t_n=n')
    b=s.index('### 3.4 ',a)
    old=s[a:b]
    cn=old[old.index('The Crank–Nicolson' if en else 'Crank–Nicolson'):]
    app.append(('F. Implicit time stepping and comparison' if en else 'F. 隐式时间推进及对照',cn))
    s=s[:a]+('We use the standard Euler and RK4 methods [10]. At every RK4 stage, the fields, auxiliary variables, mesh and boundary values are evaluated at that stage. The C–N iteration and complete time-integrator comparison are given in [Appendix F](#en-app-f).\n\n' if en else '采用标准 Euler 与 RK4 方法 [10]；RK4 每一级均按该级的场、辅助变量、网格及边界数据计算。C–N 迭代及完整的时间积分器比较见[附录 F](#zh-app-f)。\n\n')+s[b:]
    a=s.index('We compare Euler, RK4 and C–N for all four' if en else '我们采用固定网格上的 PE') if en else -1
    if not en:
        a=s.index('\n\n',s.index('{#zh-time-results}'))+2
    b=s.index('#### 3.5.3 ',a)
    app[-1]=(app[-1][0],app[-1][1]+'\n\n'+s[a:b])
    s=s[:a]+('The fixed-grid PE comparison in Appendix F shows that the C–N and RK4 error profiles nearly coincide at the reported step size. Euler has a smaller u maximum error in some cases; such a ranking concerns total error, which also contains spatial and initial-data effects. RK4 is used throughout the mesh comparison.\n\n' if en else '附录 F 的固定网格 PE 对照表明，在所用步长下，C–N 与 RK4 的误差剖面几乎重合。部分算例中 Euler 的 u 最大误差较小；这一排序针对包含空间及初始数据影响的总误差。网格比较统一采用 RK4。\n\n')+s[b:]
    # Exact-family leading term, immediately following the continuum-limit theorem.
    lead=('**Proposition 2.10 (Leading difference of the exact families).** Fix N and the same regular spectral parameters in the continuous and semi-discrete Gram determinants. On a compact set where the τ functions stay away from zero, choose smooth logarithms and write $\\alpha=\log f$, $\\beta=\log g$, $\log f_h=\\alpha+h^2\\alpha_2+O_K(h^4)$ and $\log g_h=\\beta+h^2\\beta_2+O_K(h^4)$, using the extensions (60). At the common physical position $y=(j+\\tfrac12)h$, the reconstructed exact fields satisfy' if en else '**命题 2.10（精确解族之差的首项）。** 固定 N，并在连续与半离散 Gram 行列式中取同一组正则谱参数。在 τ 函数远离零的紧区域上选取光滑对数，记 $\\alpha=\log f$、$\\beta=\log g$，并按 (60) 的延拓写成 $\log f_h=\\alpha+h^2\\alpha_2+O_K(h^4)$、$\log g_h=\\beta+h^2\\beta_2+O_K(h^4)$。在共同物理位置 $y=(j+\\tfrac12)h$，重构的精确场满足')
    lead+=eq(l,201,r'\begin{gathered}U_h-u=h^2C_U+O_K(h^4),\qquad V_h-v=h^2C_V+O_K(h^4),\\ C_U=2\partial_x(\alpha_2-\beta_2)+\frac{u_{yy}-v_y}{16},\qquad C_V=2\partial_{xy}(\alpha_2+\beta_2)+\frac{9u_{yyy}-v_{yy}}{48}.\end{gathered}')
    lead+=('The expansions hold with the derivatives used in reconstruction. Their coefficients and proof are given in [Appendix A](#en-app-a). This is an asymptotic comparison of exact solution families; the two families already differ at the initial time.' if en else '上述展开连同重构所需导数一致成立，系数及证明见[附录 A](#zh-app-a)。这是精确解族的渐近比较；两族在初始时刻已经存在差异。')
    pos=s.index('### 2.6 '); s=s[:pos]+lead+'\n\n'+s[pos:]
    # Central x truncation, right after the actual stencil.
    pos=s.index('In the y direction, we use' if en else '沿 y 方向采用')
    xtext=('Writing $k=\Delta x$, smooth functions satisfy' if en else '记 $k=\Delta x$，对光滑函数有')+eq(l,202,r'D_1f=f_x+\frac{k^2}{6}f_{xxx}+O(k^4),\qquad D_2f=f_{xx}+\frac{k^2}{12}f_{xxxx}+O(k^4).')
    xtext+=('$D_2$ is the independent three-point second derivative, not $D_1^2$.' if en else '$D_2$ 是独立的三点二阶导数模板，不等于 $D_1^2$。')
    s=s[:pos]+xtext+'\n\n'+s[pos:]
    # Finite-h RHS expansion, using the exact cumulative reconstruction.
    pos=s.index('These three spatial discretizations are combined' if en else '上述三种空间离散分别')
    xtext=('**Leading x contribution to the reconstructed u rate.** Let b be the lowest physical y layer, $\Delta_bF=F(y)-F(b)$, and $T_h$ the composite trapezoidal sum from b to y. On a fixed grid define $H=u^2/2+2au$, $W=v-\delta_0u$ and $K(W)=W^2/32-W/4$. Summing the P equation with the prescribed $u_t(b)$ gives' if en else '**重构 u 变化率的 x 方向首项。** 设 b 为最下物理 y 层，$\Delta_bF=F(y)-F(b)$，$T_h$ 为从 b 到 y 的复合梯形和。在固定网格上记 $H=u^2/2+2au$、$W=v-\delta_0u$、$K(W)=W^2/32-W/4$。将 P 方程累加并使用给定的 $u_t(b)$，得到')
    xtext+=eq(l,203,r'\begin{aligned}F^u_{\rm PE}&=u_t(b)-D_1\Delta_b[H+h^2K(W)]-D_2[\Delta_bu+T_hW],\\F^u_{\rm FD}&=u_t(b)-D_1\Delta_bH-D_2T_hv.\end{aligned}')
    xtext+=('Relative to the same y-discrete rates with exact x derivatives, $r^u_{x,m}=k^2B_{h,m}+O(k^4)$ at fixed h, where' if en else '相对于保留同一 y 离散而对 x 精确求导的变化率，固定 h 时有 $r^u_{x,m}=k^2B_{h,m}+O(k^4)$，其中')
    xtext+=eq(l,204,r'\begin{aligned}B_{h,\rm PE}&=-\frac16\partial_{xxx}\Delta_b[H+h^2K(W)]-\frac1{12}\partial_{xxxx}[\Delta_bu+T_hW],\\B_{h,\rm FD}&=-\frac16\partial_{xxx}\Delta_bH-\frac1{12}\partial_{xxxx}T_hv.\end{aligned}')
    xtext+=('For smooth fields, as h also tends to zero, both coefficients approach' if en else '对光滑场，当 h 也趋于零时，二者均趋于')
    xtext+=eq(l,205,r'B=-\frac16\partial_{xxx}\Delta_bH(u)-\frac1{12}\partial_{xxxx}\int_b^y v(x,s,t)\,ds,\qquad r_x^u=k^2B+O(k^4+k^2h^2).')
    xtext+=('These are interior right-hand-side truncation errors with a matched x extension and the prescribed lower boundary. Periodic wrap-around mismatches contribute separately. The calculation concerns u for PE and FD on a fixed grid; PF, v and moving nodes require their own expansions.' if en else '以上为匹配 x 延拓并保留给定下边界时的内部右端截断误差；周期回绕不匹配另有边界贡献。此处只计算固定网格上 PE 与 FD 的 u 变化率，PF、v 及移动节点需另行展开。')
    s=s[:pos]+xtext+'\n\n'+s[pos:]
    # Error interpretation follows the actual norm definition.
    pos=s.index('### 3.5 ')
    err=('To interpret PE and PF errors, let $Z=(u,v)$ be the continuous exact field and $Z_h=(U_h,V_h)$ the semi-discrete exact field with the same spectral parameters, evaluated at the same positions as $Z_{\\rm num}$. Then' if en else '为解释 PE 与 PF 的误差，记连续精确场为 $Z=(u,v)$，同谱参数的半离散精确场为 $Z_h=(U_h,V_h)$，并与 $Z_{\\rm num}$ 在相同位置取值。于是')
    err+=eq(l,206,r'e_{\rm model}=Z_h-Z,\qquad e_{\rm num}=Z_{\rm num}-Z_h,\qquad e_{\rm total}=e_{\rm model}+e_{\rm num}.')
    err+=('Here $e_{\\rm num}$ is the numerical deviation from the semi-discrete exact solution. It includes spatial and time discretization, reconstruction, and initial and boundary mismatches. With the continuous-field initialization used here, $e_{\\rm num}(0)=-h^2C(0)+O(h^4)$, $C=(C_U,C_V)$, at points where the physical initialization is exact; any initialization reconstruction residual is additional. The continuous lower boundary likewise differs from that of the exact semi-discrete family. For a common discrete L² or RMS inner product, without subtracting means,' if en else '其中 $e_{\\rm num}$ 为相对于半离散精确解的数值偏差，包含空间与时间离散、重构以及初值和边界不匹配的影响。本文采用连续场初始化，因此在物理初值精确恢复的点上，$e_{\\rm num}(0)=-h^2C(0)+O(h^4)$，$C=(C_U,C_V)$；初始化中的重构残差需另计。连续下边界与该半离散精确族的边界也存在差异。对同一个离散 L² 或 RMS 内积，不减去均值，有')
    err+=eq(l,207,r'\rho=\frac{\langle e_{\rm model},e_{\rm num}\rangle}{\|e_{\rm model}\|\,\|e_{\rm num}\|},\qquad \|e_{\rm total}\|^2=\|e_{\rm model}\|^2+\|e_{\rm num}\|^2+2\rho\|e_{\rm model}\|\,\|e_{\rm num}\|.')
    err+=('The direction cosine ρ is defined when both norms are nonzero and is not a Pearson correlation. A negative cross term describes cancellation in this inner-product norm. The maximum errors reported below remain total errors and do not obey this squared-norm identity. Right-hand-side truncation coefficients describe instantaneous forcing; their effect on final errors also depends on propagation and the initial and boundary data.' if en else '两范数均非零时方向余弦 ρ 有定义，它不是 Pearson 相关系数。负交叉项说明该内积范数中的抵消。下文保留的最大误差均为总误差，不适用上述平方范数恒等式。右端截断系数描述瞬时误差源，其对终态误差的影响还取决于传播及初边值数据。')
    s=s[:pos]+err+'\n\n'+s[pos:]
    # Exact-family derivation, no fitted quantities.
    ap=('Set $z_i=p_i-a$, $w_i=q_i+a$. The principal-minor expansion pairs every selected row and column with the same index set I. The lattice phase contributes $h^2y\sum_{i\in I}c_i$, and the centred f amplitude in (64) contributes $h^2\sum_{i\in I}d_i$, where' if en else '记 $z_i=p_i-a$、$w_i=q_i+a$。主子式展开中，选取的行、列对应同一指标集 I。格点相位贡献 $h^2y\sum_{i\in I}c_i$，(64) 的居中 f 振幅贡献 $h^2\sum_{i\in I}d_i$，其中')
    ap+=eq(l,208,r'c_i=\frac{z_i^{-3}+w_i^{-3}}{12},\qquad d_i=\frac{w_i^{-2}-z_i^{-2}}8,\qquad \alpha_2=\sum_i(yc_i+d_i)\rho_i\partial_{\rho_i}\alpha,\qquad \beta_2=y\sum_i c_i\rho_i\partial_{\rho_i}\beta.')
    ap+=('Indeed, $\\rho_i\partial_{\\rho_i}$ selects precisely those minors containing i. Expanding the determinant and then its logarithm therefore gives (208) for every fixed N. Symmetric reconstruction at the physical midpoint yields' if en else '算子 $\\rho_i\partial_{\\rho_i}$ 恰好选出含 i 的主子式，故先展开行列式再取对数，即对任意固定 N 得到 (208)。在物理中点作对称重构，得到')
    ap+=eq(l,209,r'\begin{aligned}U_h&=u+h^2\left[2(\alpha_2-\beta_2)_x-\frac14\beta_{xyy}\right]+O_K(h^4),\\V_h&=v+h^2\left[2(\alpha_2+\beta_2)_{xy}+\frac16u_{yyy}-\frac1{12}\beta_{xyyy}\right]+O_K(h^4).\end{aligned}')
    ap+=('Using $4\\beta_{xy}=v-u_y$ gives (201). Fixed regular spectral parameters, nonvanishing τ functions on a neighbourhood of K, and sufficiently small h ensure uniform bounds for the required derivatives and remainders. The positive spectral domain in Theorem 2.8 supplies these conditions; other regular real branches may be used wherever the same bounds hold. No stability estimate for a general initial-value problem is asserted.' if en else '代入 $4\\beta_{xy}=v-u_y$ 即得 (201)。固定正则谱参数、K 邻域上 τ 函数不为零以及充分小的 h，保证所需导数及余项的一致界。定理 2.8 的正谱域提供这些条件；其他正则实分支在具有同样界的区域内也适用。此处未断言一般初值问题的稳定性估计。')
    app.insert(0,('A. Leading exact-family difference' if en else 'A. 精确解族差的首项',ap))
    appendix='\n\n'
    for title,body in app:
        letter=title[0].lower()
        appendix+=f'## {"Appendix " if en else "附录 "}{title} {{#{l}-app-{letter}}}\n\n'+body.strip()+'\n\n'
    # Appendices go before References and preserve all relocated formulas and tables.
    pos=s.index('## References' if en else '## 参考文献')
    s=s[:pos]+appendix+s[pos:]
    s+='\n[10] E. Hairer, S. P. Nørsett, G. Wanner. *Solving Ordinary Differential Equations I: Nonstiff Problems*. 2nd revised ed., Springer, 1993. [Publisher](https://link.springer.com/book/10.1007/978-3-540-78862-1).\n\n'
    # Keep symbolic anchors stable; numbering follows the revised reading order.
    tags=re.findall(r'\\tag\{(\d+)\}',s)
    assert len(tags)==len(set(tags))
    mapping={t:str(i+1) for i,t in enumerate(tags)}
    s=re.sub(r'\\tag\{(\d+)\}',lambda m:r'\tag{'+mapping[m[1]]+'}',s)
    # Textual equation references (not mathematical tuples); link targets keep stable IDs.
    chunks=re.split(r'(\$\$[\s\S]*?\$\$|(?<!\$)\$(?!\$)[^\n$]+\$)',s)
    for i in range(0,len(chunks),2):
        chunks[i]=re.sub(r'(?<![\w\d])\((\d{1,3})\)',lambda m:'('+mapping.get(m[1],m[1])+')',chunks[i])
        chunks[i]=re.sub(r'（(\d{1,3})）',lambda m:'（'+mapping.get(m[1],m[1])+'）',chunks[i])
    (root/f'numbering_{l}.json').write_text(json.dumps(mapping,indent=2),encoding='utf8')
    return ''.join(chunks)

en=revise(en,'en'); zh=revise(zh,'zh')
(root/'revised.md').write_text(en+zh,encoding='utf8')
print('revised characters',len(en+zh))
