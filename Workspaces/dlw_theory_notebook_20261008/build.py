from pathlib import Path
from copy import deepcopy
import re, html, json
import nbformat as nb

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
old=nb.read(HERE/'before/非线性化report.ipynb',as_version=4)
cells=[]
def md(s): cells.append(nb.v4.new_markdown_cell(s.strip()))
def code(s): cells.append(nb.v4.new_code_cell(s.strip()))
def lean(route,s): code('%%lean '+route+' import\n'+s.strip())

md(r'''# DLW 理论

从连续 DLW 方程出发，引入 τ 函数与双线性表示，构造交错格点上的半离散双线性方程，证明其任意 $N$ 孤子行列式解，并建立半离散物理场到连续解的二阶极限。

全文围绕七项结论展开：连续双线性表示、半离散构造、孤子展开、Gram 解的精确性、非线性解重构、方程的连续极限，以及精确解族的连续极限。每项核心结论后附可运行的 Lean 证明单元。

连续变量为 $(x,y,t)$；离散后保留 $(x,t)$，用 $j\in\mathbb Z$ 标记 $y$ 方向格点，格距为 $h>0$。以下使用原 DLW 的 $\lambda=-2$ 归一化与固定参数 $a$。''')
md('''**运行证明。** 在 Colab 中连接现有本地运行时，或使用本地 Jupyter 内核，然后依次运行代码单元。下列入口读取工作区内的 Lean 4.34.0、Mathlib 和证明源码。已保存的输出供直接阅读；重新运行会检查对应的实际 Lean 代码。''')
code('''from pathlib import Path
import sys

workspace = Path("C:/Users/msz/aca")
sys.path.insert(0, str(workspace / "Workspaces/dlw_theory_notebook_20261008"))
from theory_runtime import load_theory
lean_session = load_theory()
print("DLW 理论：Lean 证明环境已载入。")''')

md(r'''## 1　连续 DLW 与双线性表示

连续非线性方程为

$$\begin{aligned}
u_{yt}+v_{xx}+[(u+2a)u_y]_x&=0,\\
v_t+u_{xxy}+[(u+2a)v-4u]_x&=0.
\end{aligned}\tag{C1}$$

引入正的 τ 函数 $f(x,y,t),g(x,y,t)$，令

$$u=2\partial_x\log\frac fg,\qquad v=2\partial_x\partial_y\log(fg).\tag{C2}$$

记 $B_a=D_x^2+D_t+2aD_x$，对应的连续双线性对为

$$B_af\cdot g=0,\qquad(D_yB_a-4D_x)f\cdot g=0.\tag{C3}$$

Hirota 算子采用 $D_xf\cdot g=f_xg-fg_x$，$D_x^2f\cdot g=f_{xx}g-2f_xg_x+fg_{xx}$。特别地，

$$D_yB_af\cdot g=B_af_y\cdot g-B_af\cdot g_y,$$
$$\partial_y(B_af\cdot g)=B_af_y\cdot g+B_af\cdot g_y.$$

因此，在第一条双线性方程成立时，第二条等价于

$$B_af\cdot g_y+2D_xf\cdot g=0.\tag{C4}$$

**定理 1（连续双线性表示）。** 正实解析函数 $f,g$ 满足（C3）时，由（C2）构造的 $u,v$ 满足（C1）。

令 $A=\log(fg)$、$B=\log(f/g)$。第一条归一化双线性残差为

$$R=A_{xx}+B_x^2+B_t+2aB_x.$$

再令

$$S=A_{xxy}-B_{xxy}-A_{yt}+B_{yt}-2B_x(A_{xy}-B_{xy})-2a(A_{xy}-B_{xy})+4B_x.$$

直接微分得

$$\frac{2B_af\cdot g_y+4D_xf\cdot g}{fg}=(A_y-B_y)R+S.$$

因此（C3）—（C4）给出 $R=S=0$。代入 $u=2B_x$、$v=2A_{xy}$ 后，两条非线性残差恰为

$$\mathcal C_1=2R_{xy},\qquad\mathcal C_2=2R_{xy}-2S_x,$$

故均为零。下面的 `continuous_DLW` 明确列出正性、实解析性和双线性假设，并证明两条非线性方程；`c01_proved` 检查（C3）第二式与（C4）的等价性。

这里证明的是双线性表示产生 DLW 解；从任意 DLW 场反向恢复 τ 函数还涉及积分条件。''')
lean('continuous',r'''import PkgC02
import PkgContinuous
noncomputable section
open DLWContract

theorem continuous_Hirota_bridge : C01 := c01_proved

theorem continuous_DLW (a : ℝ) (f g : XYT)
    (hf : Smooth3 f) (hg : Smooth3 g)
    (hfp : Positive3 f) (hgp : Positive3 g)
    (hbil : ContinuousPair a f g) :
    c1 a (cu f g) (cv f g) = 0 ∧
    c2 a (cu f g) (cv f g) = 0 :=
  c02_proved a f g hf hg hfp hgp hbil

#print ContinuousPair
#print continuous_DLW
#print axioms continuous_Hirota_bridge
#print axioms continuous_DLW''')

md(r'''## 2　交错格点与半离散双线性方程

将 $G_j$ 放在 $y=jh$，将 $F_j$ 放在 $y=(j+\tfrac12)h$，构造

$$\boxed{B_{a-h/2}F_j\cdot G_j=0,\qquad B_{a+h/2}F_j\cdot G_{j+1}=0.}\tag{S1}$$

固定物理位置 $y$，记

$$\mathcal B_h^- = B_{a-h/2}f(x,y,t)\cdot g(x,y-h/2,t),$$
$$\mathcal B_h^+ = B_{a+h/2}f(x,y,t)\cdot g(x,y+h/2,t).$$

**定理 2（二阶双线性一致性）。** 对实解析 $f,g$，在固定 $(x,y,t)$ 处有

$$\frac{\mathcal B_h^++\mathcal B_h^-}{2}=B_af\cdot g+O(h^2),$$
$$\frac{\mathcal B_h^+-\mathcal B_h^-}{h}=B_af\cdot g_y+2D_xf\cdot g+O(h^2).\tag{S2}$$

证明取 $\Phi(s)=B_{a+s}f(x,y,t)\cdot g(x,y+s,t)$。对称和保留 $\Phi(0)$，对称差商保留 $\Phi'(0)$，奇偶项分别消去。结合定理 1 的算子关系，极限就是（C3）。

（S1）是保持该连续极限的离散构造；连续解的直接格点采样一般不精确满足有限 $h$ 的方程。下一节给出有限 $h$ 的精确解。

Lean 中 `PowBound 2 e` 表示存在 $C\ge0,\varepsilon>0$，使 $0<|h|<\varepsilon$ 时 $|e(h)|\le C|h|^2$。''')
lean('walls',r'''import PkgC11
noncomputable section
open DLWContract

theorem bilinear_continuum_limit (a : ℝ) (f g : XYT)
    (hf : Smooth3 f) (hg : Smooth3 g) (x y t : ℝ) :
    PowBound 2 (fun h =>
      (wallPlus a h y f g x t + wallMinus a h y f g x t)/2 - cbil a f g x y t) ∧
    PowBound 2 (fun h =>
      (wallPlus a h y f g x t - wallMinus a h y f g x t)/h -
      (cbil a f (sy g) x y t + 2*chx f g x y t)) :=
  c11_proved a f g hf hg x y t

#print PowBound
#print axioms bilinear_continuum_limit''')

# Incorporate the mathematical exposition from the verified tau report.
tau=(ROOT/'Workspaces/dlw_tau_proof_20261008/report.src.html').read_text(encoding='utf-8')
def convert(s):
    s=re.sub(r'@@M ([\s\S]*?) @@',lambda m:'\n\n$$'+m[1]+'$$\n\n',s)
    s=re.sub(r'<h2>.*?</h2>','',s)
    s=s.replace('<p>','\n\n').replace('</p>','\n\n').replace('<strong>','**').replace('</strong>','**')
    s=html.unescape(s)
    s=re.sub(r'\\tag\{(\d+)\}',r'\\tag{T\1}',s)
    s=re.sub(r'（(\d+)）',r'（T\1）',s)
    return s.strip()
md('## 3　τ 函数：单孤子、双孤子与任意 N\n\n记 $d=h/2$。\n\n'+convert(tau[tau.index('<h2>2.'):tau.index('<h2>4.')]))
md('### 行列式表示与展开\n\n'+convert(tau[tau.index('<h2>4.'):tau.index('<h2>5.')])+r'''

**定理 3（双孤子展开）。** 二阶 Gram 行列式的归一化相互作用系数是 $A_{12}$，它不含 $h$。下面将此展开作为精确函数恒等式检查。''')
lean('interaction',r'''import PkgGramEntry
noncomputable section
open DLWContract

theorem two_soliton_expansion (D : Data 2) (h s : ℝ)
    (hD : Admissible D h) (hs : LayerOK D s) (n j : ℤ) (x t : ℝ) :
    let e₀ := entry D h s n j 0 0 x t - 1
    let e₁ := entry D h s n j 1 1 x t - 1
    tau D h s n j x t = 1 + e₀ + e₁ +
      interaction (D.p 0) (D.p 1) (D.q 0) (D.q 1)*e₀*e₁ :=
  c10_proved D h s hD hs n j x t

#print tau
#print interaction
#print axioms two_soliton_expansion''')

proof=convert(tau[tau.index('<h2>5.'):tau.index('<h2>7.')])
proof=proof.replace('原半离散双线性方程（T1）','原半离散双线性方程（S1）')
md('## 4　任意 N 的 τ 函数满足半离散方程\n\n**定理 4（Gram 精确解）。** 在所有谱分母非零的条件下，（T10）—（T11）满足（S1）。\n\n'+proof)
md('''下面展开任意 N 双线性链的 Lean 证明主体。`matrix_x`、`matrix_xx`、`matrix_t` 是实际 Gram 矩阵的导数；`matrix_shift` 和 `rank_one` 是秩一更新关系。行列式微分与 Plücker 恒等式由 `bil_det_of_jets` 合并。最后以这一条已证明的链推出两条半离散方程。''')
gram=(HERE/'proofs/PkgC07Complete.lean').read_text(encoding='utf-8')
body=gram[gram.index('theorem c07_proved'):gram.index('#print axioms')]
body=body.replace('theorem c07_proved','theorem theory_gram_chain',1)
lean('gram','''import PkgGramComplete
noncomputable section
open scoped BigOperators Matrix
namespace DLWContract
open GramActual

'''+body+'''
theorem theory_exact_tau (N : ℕ) (D : Data N) (h : ℝ)
    (hD : Admissible D h) : SemiPair D.a h (F D h) (G D h) :=
  c08_of_c07 theory_gram_chain N D h hD

#print SemiPair
#print axioms theory_gram_chain
#print axioms theory_exact_tau
end DLWContract''')

md(r'''## 5　正则性与半离散非线性解

**定理 5（正则物理解）。** 假设

$$h>0,\qquad0<p_1<\cdots<p_N<a-h/2,\qquad0<q_1<\cdots<q_N,\qquad\rho_i>0.$$

则子集展开的每一项均为正，常数项为 1，所以 $F_j,G_j>0$。对数导数无奇点，定义

$$u_j=\partial_x\log\frac{F_j^2}{G_jG_{j+1}},\qquad
v_j=\frac4h\partial_x\log\frac{G_{j+1}}{G_j}+\delta_0u_j.$$

这些场满足下文（N8）的两条半离散非线性方程。下面先核验正则性与解的终点，再展开从双线性方程消去辅助势的推导。''')
lean('regular',r'''import PkgGramComplete
noncomputable section
open DLWContract

theorem regular_tau (N : ℕ) (D : Data N) (h : ℝ)
    (hD : PositiveData D h) :
    Admissible D h ∧ PositiveL (F D h) ∧ PositiveL (G D h) ∧
    SmoothL (F D h) ∧ SmoothL (G D h) :=
  c09_proved N D h hD

theorem exact_nonlinear_solution (N : ℕ) (D : Data N) (h : ℝ)
    (hD : PositiveData D h) :
    NonlinearPair D.a h (physU (F D h) (G D h)) (physV h (F D h) (G D h)) :=
  c16_proved N D h hD

#print PositiveData
#print axioms regular_tau
#print axioms exact_nonlinear_solution''')

def oldcell(i):
    c=deepcopy(old.cells[i])
    c.id=f'preserved-{i}'
    if c.cell_type=='code':
        c.outputs=[];c.execution_count=None
    else:
        c.source=re.sub(r'\\tag\{(\d+)\}',r'\\tag{N\1}',c.source)
        c.source=re.sub(r'（(\d+)）',r'（N\1）',c.source)
        c.source=c.source.replace('### 1.2','### 8.1').replace('### 1.3','### 8.2')
    cells.append(c)
md('### 5.1　消去辅助势的非线性化\n\n以下保留原 Notebook 中的两场推导，并将本节公式编号记为 N1—N9。')
for i in (3,4,5,6,7): oldcell(i)

md(r'''## 6　半离散方程的连续极限

**定理 6（二阶非线性一致性）。** 对固定实解析场 $u(x,y,t),v(x,y,t)$，令 $u_j=u(x,y+jh,t)$、$v_j=v(x,y+jh,t)$。以 $\mathcal N_{1,h},\mathcal N_{2,h}$ 表示（N8）的两条残差，以 $\mathcal C_1,\mathcal C_2$ 表示（C1）的残差，则

$$\mathcal N_{1,h}(0,x,t)=\mathcal C_1(x,y-h/2,t)+O(h^2),$$
$$\mathcal N_{2,h}(0,x,t)=\mathcal C_2(x,y,t)+O(h^2).\tag{L1}$$

第一式的后向差分与相邻平均以 $y-h/2$ 为中心；第二式以 $y$ 为中心。保留这些评价位置后，两式均为二阶一致。

同时，将连续 τ 函数按 F、G 的交错位置采样，物理变量的重构满足

$$u^{[h]}=2(\log(f/g))_x+O(h^2),\qquad v^{[h]}=2(\log(fg))_{xy}+O(h^2).\tag{L2}$$

其证明分别来自 $g(y-h/2)$ 与 $g(y+h/2)$ 的对称 Taylor 展开，以及中心差商展开。下面 `C17` 同时包含采样与重构的精确对齐、重构误差的二阶界；`nonlinear_continuum_limit` 则明确展示（L1）。''')
lean('limit',r'''import PkgC17
import PkgC18Complete
noncomputable section
open DLWContract

theorem physical_reconstruction_limit : C17 := c17_proved

theorem nonlinear_continuum_limit (a : ℝ) (u v : XYT)
    (hu : Smooth3 u) (hv : Smooth3 v) (x y t : ℝ) :
    PowBound 2 (fun h =>
      n1 a h (localSamples y h u) (localSamples y h v) 0 x t - c1 a u v x (y-h/2) t) ∧
    PowBound 2 (fun h =>
      n2 a h (localSamples y h u) (localSamples y h v) 0 x t - c2 a u v x y t) :=
  c18_proved a u v hu hv x y t

#print C17
#print axioms physical_reconstruction_limit
#print axioms nonlinear_continuum_limit''')

md(r'''## 7　精确孤子解的连续极限

固定谱参数，令 $P_i=p_i-a$、$Q_k=q_k+a$。格点相位的关键展开为

$$\frac1h\log\lambda_h(z)=\frac1z+\frac{h^2}{12z^3}+O(h^4),$$
$$\frac1h\log\chi_{ik}=\frac1{P_i}+\frac1{Q_k}+O(h^2).\tag{L3}$$

连续 Gram 函数因而为

$$\tau_n^{(0)}(x,y,t)=\det\left[\delta_{ik}+\frac{\rho_i}{p_i+q_k}
\left(-\frac{p_i-a}{q_k+a}\right)^n
\exp\left((p_i+q_k)x+(q_k^2-p_i^2)t+y\left(\frac1{P_i}+\frac1{Q_k}\right)\right)\right].\tag{L4}$$

令 $f^{(0)}=\tau_1^{(0)}$、$g^{(0)}=\tau_0^{(0)}$。它们满足（C3），所以由（C2）给出的 $u^{(0)},v^{(0)}$ 满足连续 DLW。

为了在固定物理坐标比较不同格距的解，使用与格点完全一致的插值

$$f^{(h)}=\det\left[\delta_{ik}+\frac{\rho_i}{p_i+q_k}\gamma_{ik}(a-h/2)
e^{(p_i+q_k)x+(q_k^2-p_i^2)t+(y/h-1/2)\log\chi_{ik}}\right],$$
$$g^{(h)}=\det\left[\delta_{ik}+\frac{\rho_i}{p_i+q_k}
e^{(p_i+q_k)x+(q_k^2-p_i^2)t+(y/h)\log\chi_{ik}}\right].\tag{L5}$$

于是 $f^{(h)}(x,(j+1/2)h,t)=F_j(x,t)$，$g^{(h)}(x,jh,t)=G_j(x,t)$。F 的半格偏移不可省略。在正实参数区域，每个矩阵元的 F 振幅满足

$$\gamma_{ik}(a-h/2)\chi_{ik}^{-1/2}
=\sqrt{\frac{P_i^2-h^2/4}{Q_k^2-h^2/4}}
=-\frac{P_i}{Q_k}+O(h^2).\tag{L6}$$

它与（L3）均为 h 的偶函数延拓。行列式、对数及所需导数在紧区域上保持正则；对称重构使物理场的一阶项消失。

定义

$$u^{(h)}=\partial_x\bigl[2\log f^{(h)}(y)-\log g^{(h)}(y-h/2)-\log g^{(h)}(y+h/2)\bigr],$$
$$v^{(h)}=\frac4h\partial_x\bigl[\log g^{(h)}(y+h/2)-\log g^{(h)}(y-h/2)\bigr]
+\frac{u^{(h)}(y+h)-u^{(h)}(y-h)}{2h}.\tag{L7}$$

**定理 7（精确解族的一致二阶极限）。** 固定任意有限 N 和满足定理 5 在某个 $h_0>0$ 处条件的谱数据。对任意 $R>0$，存在 $C_R\ge0$ 与 $\varepsilon_R>0$，使 $0<h<\varepsilon_R$ 时

$$\sup_{|x|,|y|,|t|\le R}\left(|u^{(h)}-u^{(0)}|+|v^{(h)}-v^{(0)}|\right)\le C_Rh^2.\tag{L8}$$

Lean 的 `UniformBoxO2` 分别给出两个场的紧盒界；将两个常数相加、邻域半径取最小，即得（L8）。`continuous_Gram_pair` 证明极限 τ 满足连续双线性对，`exact_solution_limit` 检查实际有限 h Gram 场到连续物理场的收敛，不以残差一致性代替解的收敛。''')
lean('solutionlimit',r'''import PkgC22Complete
import PkgC23Complete
import PkgQuotientRate
noncomputable section
open DLWContract

theorem lattice_phase_limit : C12 := c12_proved
theorem exact_lattice_interpolation : C24 := c24_proved

theorem continuous_Gram_pair (N : ℕ) (D : Data N) (h₀ : ℝ)
    (hD : PositiveData D h₀) :
    ContinuousPair D.a (tau0 D 1) (tau0 D 0) :=
  c23_proved N D h₀ hD

theorem exact_solution_limit (N : ℕ) (D : Data N) (h₀ : ℝ)
    (hD : PositiveData D h₀) :
    UniformBoxO2 (fun h =>
      interpU h (tauI D h (D.a-h/2) 1 (1/2)) (tauI D h D.a 0 0) -
      cu (tau0 D 1) (tau0 D 0)) ∧
    UniformBoxO2 (fun h =>
      interpV h (tauI D h (D.a-h/2) 1 (1/2)) (tauI D h D.a 0 0) -
      cv (tau0 D 1) (tau0 D 0)) :=
  c22_proved N D h₀ hD

#print UniformBoxO2
#print axioms lattice_phase_limit
#print axioms exact_lattice_interpolation
#print axioms continuous_Gram_pair
#print axioms exact_solution_limit''')

md('## 8　补充：保留势的非线性表示\n\n保留原报告的 Q、R、M 路线。这一表示从相同的半离散双线性对出发，保留辅助势，给出相容的乘积分解与物理变量重构。')
for i in (9,10,11,12,13,14): oldcell(i)
md('''### 证明对应

| 正文结论 | Lean 核心定理 |
|---|---|
| 连续双线性对产生 DLW 解 | `c01_proved`、`c02_proved` |
| 半离散双线性对的二阶极限 | `c11_proved` |
| 双孤子展开 | `c10_proved` |
| 任意 N Gram 精确解 | `theory_gram_chain`、`theory_exact_tau` |
| 正 τ 与半离散非线性解 | `c09_proved`、`c14_proved`、`c15_proved`、`c16_proved` |
| 非线性方程及重构的二阶一致性 | `c17_proved`、`c18_proved` |
| 精确解族在紧区域上的二阶极限 | `c12_proved`、`c22_proved`、`c23_proved`、`c24_proved` |
| Q、R、M 表示 | `semiPair_implies_report21`、`report22` |

代码中的 `Smooth3`、`SmoothL` 使用当前 Lean 库的实解析假设；Gram 指数行列式满足这些假设。每个定理后的 `#print axioms` 输出其基础公理依赖。''')

for i,c in enumerate(cells):
    if not c.id.startswith('preserved-'): c.id=f'theory-{i:02d}'
from notebook_prose import revise
cells=revise(cells)
from focus_theory import focus
cells=focus(cells)
notebook=nb.v4.new_notebook(cells=cells,metadata=deepcopy(old.metadata))
notebook.metadata['title']='DLW 理论'
notebook.metadata.setdefault('colab',{})['name']='DLW理论.ipynb'
notebook.metadata['report_history']={k:notebook.metadata.pop(k) for k in ('report_conversion','report_split') if k in notebook.metadata}
notebook.metadata['report_theory']={'title':'DLW 理论','scope':'Continuous DLW, exact semidiscrete Gram tau, nonlinear reconstruction and continuum limits','builder':'Workspaces/dlw_theory_notebook_20261008/build.py'}
nb.validate(notebook)
dest=HERE/'DLW理论.input.ipynb'
nb.write(notebook,dest)
(HERE/'build_validation.json').write_text(json.dumps({'cells':len(cells),'code_cells':sum(c.cell_type=='code' for c in cells),'numerical_cells':0,'original_nonlinear_cells_preserved':[3,4,5,6,7,9,10,11,12,13,14]},ensure_ascii=False,indent=2),encoding='utf-8')
print(dest)
