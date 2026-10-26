from pathlib import Path
import re
P=Path(__file__).resolve().parent
s=(P/'manuscript.md').read_text(encoding='utf-8')
def eq(lang,id):
 m=re.search(rf'<a id="{lang}-eq-{id}"></a>\s*\$\$[\s\S]*?\$\$',s)
 assert m,id
 return m[0]
def generate(lang):
 en=lang=='en'; out=[]
 def p(a,b):out.append(a if en else b)
 def e(i):out.append(eq(lang,i))
 p('### 2.5 Continuum limits {#en-limits}','### 2.5 连续极限 {#zh-limits}')
 p(r'''Having established the semi-discrete equations and their exact solutions, we now examine how they approach the continuous DLW system as the lattice spacing tends to zero. We wish to determine how the lattice modifies the exact wave fields and how the continuous equations emerge from the discrete relations. We first derive an expansion of the difference between the semi-discrete and continuous Gram solutions, including its leading coefficients. The second-order convergence of the reconstructed fields then follows directly. We subsequently examine the consistency of the nonlinear equations.

Throughout this subsection, $O_K(h^m)$ denotes a remainder bounded uniformly by $C_Kh^m$ on a compact set $K$, with $C_K$ independent of $h$. We assume sufficient smoothness on an open neighbourhood of $K$. Where derivatives of an expansion are used, the remainder estimate is understood to hold for those derivatives as well.

We begin by comparing corresponding members of the exact solution families. To make this comparison at a common physical position, we extend the lattice τ functions to continuous $y$ and retain the staggered reconstruction. For positive functions $f_h,g_h$, we define''',r'''在建立半离散方程及其精确解之后，我们进一步考察它们在格点间距趋于零时如何逼近连续 DLW 系统。我们希望明确格点如何改变精确波场，以及连续方程如何从离散关系中恢复。首先，我们导出半离散与连续 Gram 解之差的展开，并给出其首项系数；重构物理场的二阶收敛由此直接得到。随后，我们考察非线性方程的相容性。

本小节中，$O_K(h^m)$ 表示在紧集 $K$ 上由 $C_Kh^m$ 一致控制的余项，其中 $C_K$ 与 $h$ 无关。我们假设函数在 $K$ 的一个开邻域内充分光滑。使用展开式的导数时，余项估计也适用于所需导数。

我们首先比较精确解族中相互对应的成员。为在同一物理位置进行比较，我们将格点 τ 函数延拓到连续坐标 $y$，并保留交错重构。对于正函数 $f_h,g_h$，定义''')
 e(47)
 out[-1]=out[-1].replace('u^{[h]}','U_h').replace('v^{[h]}','V_h').replace('\\omega^{[h]}','\\Omega_h').replace('f(y)','f_h(y)').replace('g(y','g_h(y')
 p(r'''Here and below, we suppress the common arguments $x,t$ when displaying shifts in $y$. At $y=(j+\tfrac12)h$, these expressions agree with the lattice reconstruction in (18).

**Theorem 2.7 (Leading error and convergence of the exact wave fields).** Fix the determinant order $N$ and real spectral parameters satisfying, for some $h_0>0$,''',r'''这里及下文在表示 $y$ 方向平移时，省略共同的变量 $x,t$。在 $y=(j+\tfrac12)h$ 处，这些表达式与格点重构公式 (18) 一致。

**定理 2.7（精确波场的误差首项与收敛性）。** 固定行列式阶数 $N$，并选取满足下列条件的实谱参数，其中 $h_0>0$：''')
 e(59)
 p(r'''Let $f,g$ be the continuous Gram τ functions in (5), and let $u,v$ be their physical fields defined by (2). For $0<h\le h_0$, extend the positive lattice factors to real powers and set''',r'''设 $f,g$ 为公式 (5) 中的连续 Gram τ 函数，$u,v$ 为通过公式 (2) 定义的物理场。对于 $0<h\le h_0$，将正格点因子延拓到实数次幂，并令''')
 e(60);out[-1]=out[-1].replace('g^{(h)}','g_h').replace('f^{(h)}','f_h')
 p(r'''Let $U_h,V_h$ be the staggered reconstruction defined above. Write $\alpha=\log f$, $\beta=\log g$, $z_i=p_i-a$ and $w_i=q_i+a$, and define''',r'''设 $U_h,V_h$ 为上述交错重构得到的物理场。记 $\alpha=\log f$、$\beta=\log g$、$z_i=p_i-a$、$w_i=q_i+a$，并定义''')
 out.append(r'''$$c_i=\frac{z_i^{-3}+w_i^{-3}}{12},\qquad d_i=\frac{w_i^{-2}-z_i^{-2}}8,$$

$$\alpha_2=\sum_{i=1}^{N}(yc_i+d_i)\rho_i\partial_{\rho_i}\alpha,\qquad \beta_2=y\sum_{i=1}^{N}c_i\rho_i\partial_{\rho_i}\beta.$$''')
 p('Then, uniformly on every compact set $K$,','则在任意紧集 $K$ 上，一致地有')
 e(201)
 p('Consequently, for sufficiently small $h>0$,','因此，对于充分小的 $h>0$，有')
 e(61);out[-1]=out[-1].replace('u^{(h)}','U_h').replace('v^{(h)}','V_h').replace('u^{(0)}','u').replace('v^{(0)}','v')
 p(r'''The same expansion applies to the physical fields reconstructed through either PE or PF.

**Proof.** We first expand the lattice factors while keeping the spectral parameters fixed:''',r'''这一展开同时适用于通过 PE 与 PF 重构的物理场。

**证明。** 我们保持谱参数固定，首先展开格点因子：''')
 e(62)
 p('For each determinant entry, the coefficient of $y$ in the lattice phase therefore satisfies','对于各行列式元素，格点相位中 $y$ 的系数因而满足')
 e(63)
 p(r'''In $f_h$, the half-grid displacement also combines with the shift of the auxiliary parameter. The resulting amplitude factor is''',r'''在 $f_h$ 中，半格点位移还与辅助参数的平移相结合，得到如下振幅因子：''')
 e(64)
 # Expand the amplitude to the coefficient order required by the theorem.
 out[-1]=out[-1].replace(r'-\frac{z_i}{w_k}+O(h^2)',r'-\frac{z_i}{w_k}\left[1+\frac{h^2}{8}\left(\frac1{w_k^2}-\frac1{z_i^2}\right)+O(h^4)\right]')
 p(r'''Both the phase and the centred amplitude thus differ from their continuous counterparts first at order $h^2$.

To identify the coefficients in the determinants, we use their principal-minor expansions. Each minor uses the same index set $\mathcal I$ for its rows and columns. Its phase correction is $h^2y\sum_{i\in\mathcal I}c_i$, while the additional amplitude correction for $f_h$ is $h^2\sum_{i\in\mathcal I}d_i$. The operator $\rho_i\partial_{\rho_i}$ selects precisely the minors containing the index $i$. Expanding the determinants and then their logarithms gives''',r'''因此，相位与中心化振幅相对于连续形式的差异均从 $h^2$ 阶开始。

为确定行列式中的系数，我们采用主子式展开。每个主子式的行与列使用同一个指标集 $\mathcal I$，其相位修正为 $h^2y\sum_{i\in\mathcal I}c_i$，而 $f_h$ 的额外振幅修正为 $h^2\sum_{i\in\mathcal I}d_i$。算子 $\rho_i\partial_{\rho_i}$ 恰好选出包含指标 $i$ 的主子式。先展开行列式，再展开其对数，得到''')
 out.append(r'''$$\log f_h=\alpha+h^2\alpha_2+O_K(h^4),\qquad \log g_h=\beta+h^2\beta_2+O_K(h^4).$$''')
 p(r'''The stated spectral conditions ensure positivity of the continuous τ functions and their real-exponent extensions. Since $N$ and the spectral parameters are fixed, these expansions hold uniformly on compact sets, together with the derivatives required below.

We next insert the logarithmic expansions into the staggered reconstruction. Symmetric Taylor expansion about the physical position $y$ gives''',r'''所述谱条件保证连续 τ 函数及其实数次幂延拓为正。由于 $N$ 和谱参数保持固定，这些展开连同下面所需的导数在紧集上一致成立。

接下来，我们将对数展开代入交错重构。围绕物理位置 $y$ 作对称 Taylor 展开，得到''')
 out.append(r'''$$U_h=u+h^2\left[2(\alpha_2-\beta_2)_x-\frac14\beta_{xyy}\right]+O_K(h^4).$$''')
 p('For the second field, the corresponding expansions are','对于第二个物理场，相应的展开为')
 out.append(r'''$$\frac4h\Omega_h=4\beta_{xy}+h^2\left[4(\beta_2)_{xy}+\frac16\beta_{xyyy}\right]+O_K(h^4),$$

$$\begin{aligned}\frac{U_h(y+h)-U_h(y-h)}{2h}={}&u_y+h^2\left[2(\alpha_2-\beta_2)_{xy}-\frac14\beta_{xyyy}+\frac16u_{yyy}\right]+O_K(h^4).\end{aligned}$$''')
 p('Adding these expressions, we obtain','将二者相加，得到')
 out.append(r'''$$V_h=v+h^2\left[2(\alpha_2+\beta_2)_{xy}+\frac16u_{yyy}-\frac1{12}\beta_{xyyy}\right]+O_K(h^4).$$''')
 p(r'''Finally, the continuous reconstruction implies $4\beta_{xy}=v-u_y$. Using this identity in the two field expansions gives the stated coefficients $C_U,C_V$. Their boundedness on $K$ yields the second-order convergence estimate. Since PE and PF reconstruct identical fields from the same τ functions, the result holds for both formulations. □

Through this expansion, we can describe how discretization in $y$ changes the reconstructed wave fields at small but finite lattice spacing. The coefficients $C_U$ and $C_V$ determine the leading spatial distribution of the difference in each field. The terms involving $\alpha_2,\beta_2$ arise from changes in the determinant solutions, while the remaining terms come from the staggered reconstruction. Under the stated assumptions, these coefficients are bounded on compact sets. The expansion therefore gives, as a direct consequence, uniform second-order convergence of both reconstructed fields to their continuous DLW counterparts as $h\to0$.

We now turn to the nonlinear equations. To express their continuum limit in the physical variables, we introduce''',r'''最后，连续重构关系给出 $4\beta_{xy}=v-u_y$。在两个物理场展开中使用这一恒等式，即得所述系数 $C_U,C_V$。它们在 $K$ 上有界，因此得到二阶收敛估计。由于 PE 与 PF 从同一组 τ 函数重构出相同的物理场，结论对两种表示均成立。□

通过这一展开，我们可以描述格点间距较小但非零时，$y$ 方向离散如何改变重构波场。系数 $C_U,C_V$ 分别刻画两个物理场差异首项的空间分布。含 $\alpha_2,\beta_2$ 的项来自行列式解本身的变化，其余项则来自交错重构。在所述假设下，这些系数在紧集上有界。因此，这一展开直接蕴含：当 $h\to0$ 时，两个重构物理场均在紧集上以二阶精度一致收敛到相应的连续 DLW 物理场。

现在，我们转向非线性方程。为用物理变量表达其连续极限，我们引入''')
 e(51)
 p('The PE equations then take the form','PE 方程于是写为')
 e(52)
 p(r'''With $\mathcal M_+z_j=(z_{j+1}+z_j)/2$, the identity $\mathcal M_+\delta_-=\delta_0$ shows that the time derivative in $\mathcal M_+E_{1,h,j}+E_{2,h,j}$ is $v_{j,t}$. We therefore compare this combination with the second continuous DLW equation.

**Proposition 2.8 (Consistency of the equations).** Sample sufficiently smooth fields $u,v$ at $y_j=(j+\tfrac12)h$, and define the continuous residuals''',r'''令 $\mathcal M_+z_j=(z_{j+1}+z_j)/2$。恒等式 $\mathcal M_+\delta_-=\delta_0$ 表明，$\mathcal M_+E_{1,h,j}+E_{2,h,j}$ 中的时间导数为 $v_{j,t}$。因此，我们将这一组合与连续 DLW 系统的第二式进行比较。

**命题 2.8（方程的相容性）。** 在 $y_j=(j+\tfrac12)h$ 处对充分光滑的物理场 $u,v$ 取样，并定义连续残差''')
 e(53)
 p('Then, uniformly on compact sets,','则在紧集上一致地有')
 e(54)
 p(r'''**Proof.** We set $m_j=y_j-h/2$. Expanding the difference and averaging operators about their respective centres gives''',r'''**证明。** 记 $m_j=y_j-h/2$。围绕差分与平均算子各自的中心展开，得到''')
 e(55)
 p('Consequently,','因此，')
 e(56)
 p(r'''These expansions also hold after the required differentiation. Substitution into the first residual yields $E_{1,h,j}=\mathcal C_1(x,m_j,t)+O_K(h^2)$.

For the second residual, we write $w=v-u_y$ and obtain''',r'''这些展开在所需的求导后仍成立。代入第一条残差，得到 $E_{1,h,j}=\mathcal C_1(x,m_j,t)+O_K(h^2)$。

对于第二条残差，记 $w=v-u_y$，可得''')
 e(57)
 p('Averaging the first residual about $y_j$ and adding the second gives','将第一条残差关于 $y_j$ 作平均，再与第二条相加，得到')
 e(58)
 p(r'''Here all continuous fields are evaluated at $y_j$. This proves the second assertion. □

The continuum-limit analysis shows that the proposed lattice system retains a quantitative connection with the continuous DLW model. We recover the continuous equations with second-order consistency and, for the exact solution families considered here, obtain uniform second-order convergence of both physical fields on compact sets. At finite lattice spacing, the coefficients $C_U$ and $C_V$ give a more detailed account of this approximation: they describe the leading difference in each field and how that difference varies across the wave profile. We can thus assess the effect of discretizing $y$ directly in the reconstructed physical fields. Since PE and PF yield identical fields from the same τ functions, the error expansion and its coefficients apply to both formulations.''',r'''这里，所有连续物理场均在 $y_j$ 处取值。第二个结论得证。□

连续极限分析表明，所构造的格点系统与连续 DLW 模型保持着可定量描述的联系。我们建立了格点方程对连续方程的二阶相容性，并对本节考察的精确解族，得到了两个物理场在紧集上的二阶一致收敛。在有限格距下，系数 $C_U,C_V$ 进一步刻画了这种逼近：它们描述各物理场差异的首项，以及这一差异在波形中的空间变化。因此，我们能够直接通过重构物理场评估 $y$ 方向离散的影响。由于 PE 与 PF 从同一组 τ 函数得到相同的物理场，上述误差展开及其系数同时适用于两种表示。''')
 (P/f'section25_sync_{lang}.md').write_text('\n\n'.join(out)+'\n',encoding='utf-8')
generate('en');generate('zh')
