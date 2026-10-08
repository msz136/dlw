"""Editorial source for the theory-only HTML; never modifies the notebook."""
from pathlib import Path
import re,shutil,json,hashlib
import nbformat
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
backup=HERE/'before_paper_revision'
backup.mkdir(exist_ok=True)
for p in [ROOT/'report/dlw_theory.html',HERE/'export.py',HERE/'README.md',ROOT/'PROGRESS_LOG.md',ROOT/'FILE_INDEX.md']:
    target=backup/p.name
    if not target.exists():shutil.copy2(p,target)
n=nbformat.read(HERE/'before_prose_revision/DLW理论.ipynb',as_version=4)
parts=[]
parts.append(r'''# DLW 方程的半离散化、τ 函数与连续极限

<div class="abstract"><span class="abstract-label">摘要</span> 对 DLW 方程构造交错格点双线性离散，给出任意有限阶的 Gram 行列式解。由秩一更新证明该解满足两条半离散双线性方程，并导出正则非线性解。在固定正实谱参数下，半离散物理场在任意紧区域上以二阶精度趋于连续 DLW 孤子解。</div>

连续变量记为 $(x,y,t)$，离散格点为 $j\in\mathbb Z$，格距为 $h>0$。参数 $a$ 固定，采用 $\lambda=-2$ 的 DLW 归一化。函数均取实解析类；涉及实对数时，τ 函数取正值。''')

def edit(i,replacements=(),stop=None):
    s=n.cells[i].source
    if stop:s=s[:s.index(stop)]
    for a,b in replacements:
        assert a in s,(i,a)
        s=s.replace(a,b)
    parts.append(s.strip())

edit(3,[
('连续非线性方程为','考虑连续 DLW 方程'),
('特别地，','由乘积法则，'),
('令 $A=\\log(fg)$、$B=\\log(f/g)$。第一条归一化双线性残差为','证明。令 $A=\\log(fg)$、$B=\\log(f/g)$，并记'),
('因此（C3）—（C4）给出','由（C3）和（C4）得'),
('故均为零。下面的 `continuous_DLW` 明确列出正性、实解析性和双线性假设，并证明两条非线性方程；`c01_proved` 检查（C3）第二式与（C4）的等价性。','故两式均为零。□'),
('这里证明的是双线性表示产生 DLW 解；从任意 DLW 场反向恢复 τ 函数还涉及积分条件。','')])
edit(5,[
('证明取','证明。取'),
('结合定理 1 的算子关系，极限就是（C3）。','由（C4），两式的极限构成（C3）。□'),
('（S1）是保持该连续极限的离散构造；连续解的直接格点采样一般不精确满足有限 $h$ 的方程。下一节给出有限 $h$ 的精确解。','这里的 $O(h^2)$ 指存在 $C\\ge0$、$\\varepsilon>0$，使 $0<h<\\varepsilon$ 时余项的绝对值不超过 $Ch^2$。')],stop='Lean 中')
edit(7,[
('## 3　τ 函数：单孤子、双孤子与任意 N','## 3　孤子解与 Gram 行列式'),
('取常数 pᵢ、qᵢ、ρᵢ，定义','取常数 $p_i,q_i,\\rho_i$，定义'),
('**单孤子。**只有一个指数项时，解为','当 $N=1$ 时，'),
('**双孤子。**两个指数项通过系数 A₁₂ 耦合：','当 $N=2$ 时，'),
('**一般 N 孤子。**对指标集的所有子集求和，空乘积约定为 1：','一般 $N$ 的解写为子集之和，空乘积取 1：'),
('G 的下一格点值由每个 Eᵢ 替换为 χᵢEᵢ 得到。式（T7）是一个精确解族；参数固定后确定一个解，不是一般初值问题的通解。','$G_{j+1}$ 由 $E_i\\mapsto\\chi_iE_i$ 得到。'),
('记 K=p+q、Ω=q²−p²，Eₓ=KE、Eₜ=ΩE。常数项及 E² 项在双线性算子中相消，剩下','单孤子可直接验证。记 $K=p+q$、$\\Omega=q^2-p^2$，则 $E_x=KE$、$E_t=\\Omega E$。双线性残差中的常数项和 $E^2$ 项相消，得到'),
('第一条方程取 s=a−d、α=γ、β=1，方括号为零。第二条取 s=a+d、α=γ、β=χ，并用','第一条方程取 $s=a-d$、$\\alpha=\\gamma$、$\\beta=1$，方括号为零。第二条取 $s=a+d$、$\\alpha=\\gamma$、$\\beta=\\chi$，利用'),
('因此式（T5）逐项满足两条方程。下面证明相互作用项加入后，结论对任意 N 仍成立。','两条方程均成立。')])
edit(8,[
('引入辅助层参数 s 和层编号 n，定义','引入参数 $s$ 和层编号 $n$，定义'),
('这里 τ₀ 与 s 无关。主子式展开 det(I+K)=Σ det K[I,I]，结合 Cauchy 行列式公式','$\\tau_0$ 与 $s$ 无关。由主子式展开 $\\det(I+K)=\\sum_I\\det K[I,I]$ 和 Cauchy 行列式公式'),
('立即给出式（T7）。证明原方程只需 n=0、1；若推广到任意整数 n，则还要求幂的底数非零。其余谱参数也须避开所列分母及格点乘子的零点。','得到（T7）。以下谱参数均避开分母和格点乘子的零点；当 $n$ 取任意整数时，另要求 $p_i-s$ 与 $q_k+s$ 非零。'),
('**定理 3（双孤子展开）。** 二阶 Gram 行列式的归一化相互作用系数是 $A_{12}$，它不含 $h$。下面将此展开作为精确函数恒等式检查。','**推论 3（双孤子系数）。** 二阶行列式展开为（T6），其归一化相互作用系数 $A_{12}$ 与格距 $h$ 无关。')])
edit(10,[
('## 4　任意 N 的 τ 函数满足半离散方程','## 4　Gram 解的双线性恒等式'),
('**定理 4（Gram 精确解）。** 在所有谱分母非零的条件下，（T10）—（T11）满足（S1）。','**定理 4（Gram 解）。** 在第 3 节的谱参数条件下，由（T10）和（T11）定义的 $F_j,G_j$ 满足（S1）。'),
('**引理。**式（T10）满足','先证明固定 $s$ 的双线性链：'),
('证明。固定 j、s、n，把矩阵写为 Mᵢₖ=δᵢₖ+rᵢcₖ/(pᵢ+qₖ)，其中','证明。固定 $j,s,n$，将矩阵写成 $M_{ik}=\\delta_{ik}+r_ic_k/(p_i+q_k)$，其中'),
('令 P=diag(pᵢ)、Q=diag(qᵢ)、b=(Q+sI)⁻¹c。由定义直接得到','令 $P=\\operatorname{diag}(p_i)$、$Q=\\operatorname{diag}(q_i)$、$b=(Q+sI)^{-1}c$。由定义得'),
('最后一个等式来自 −(pᵢ−s)/(qₖ+s)−1=−(pᵢ+qₖ)/(qₖ+s)。在 M 可逆处记','最后一式由 $-(p_i-s)/(q_k+s)-1=-(p_i+q_k)/(q_k+s)$ 得到。在 $M$ 可逆处记'),
('最后一步是矩阵行列式引理。Jacobi 微分公式给出 κ=(log τₙ)ₓ；亦可将其理解为 τₙ,ₓ/τₙ，无需选择复对数分支。再定义','矩阵行列式引理给出 $\\psi=1-\\zeta$。由 Jacobi 微分公式，$\\kappa=\\tau_{n,x}/\\tau_n$。再记'),
('使用 Hₓ=−HMₓH、Hₜ=−HMₜH，逐项求导得到','利用 $H_x=-HM_xH$ 和 $H_t=-HM_tH$ 求导，得'),
('例如 zₓ=HPr−κz，故 ζₓ=(c−sb)ᵀz+bᵀ(HPr−κz)，即第二式。再微分第二式，并代入其余三式：','其中 $z_x=HPr-\\kappa z$，故 $\\zeta_x=(c-sb)^{\\mathsf T}z+b^{\\mathsf T}(HPr-\\kappa z)$。对第二式再求一次导数，代入其余三式：'),
('由于 ψ=1−ζ，因此','代入 $\\psi=1-\\zeta$，得'),
('另一方面，对任意 f=ψg，有直接展开恒等式','对任意 $f=\\psi g$，双线性算子的展开给出'),
('取 g=τₙ、f=τₙ₊₁，式（T20）即证明（T13）。为去掉 M 可逆的临时条件，把全部 ρᵢ 同乘一个参数 ε；在 ε=0 时 M=I，故恒等式在 ε=0 的邻域成立。原双线性残差是 ε 的多项式，因此对所有 ε 恒为零；取 ε=1 即覆盖 τₙ 的零点。引理得证。','取 $g=\\tau_n$、$f=\\tau_{n+1}$，由（T20）得（T13）。将全部 $\\rho_i$ 替换为 $\\varepsilon\\rho_i$，则 $\\varepsilon=0$ 时 $M=I$，上述恒等式在零点邻域成立。双线性残差是 $\\varepsilon$ 的多项式，因而恒为零。取 $\\varepsilon=1$，结论也适用于 $M$ 不可逆的点。'),
('在式（T13）中取 n=0、s=a−d，立即得到第一条方程。第二条来自逐矩阵元恒等式：','在（T13）中取 $n=0$、$s=a-d$，得到（S1）的第一条方程。又有逐矩阵元恒等式'),
('因此，在行列式层面精确地有','故'),
('再在式（T13）中取 n=0、s=a+d，并把 j 换为 j+1，即得','在（T13）中取 $n=0$、$s=a+d$，并将 $j$ 换为 $j+1$，得'),
('式（T7）或等价的式（T10）—（T11）因而满足原半离散双线性方程（S1），对每个有限 N、所有 x、t 及整数 j 成立。','两条方程对任意有限 $N$、实数 $x,t$ 及整数 $j$ 成立。□')])
edit(13,[('## 5　正则性与半离散非线性解','## 5　正则性与非线性化'),('这些场满足下文（N8）的两条半离散非线性方程。下面先核验正则性与解的终点，再展开从双线性方程消去辅助势的推导。','由下述消元，它们满足（N8）。')])
parts.append('### 5.1　辅助势的消去')
edit(19,[
('其中 $D$ 为 Hirota 双线性算子，$F_j$ 与 $G_j$ 分别位于 $y=(j+\\tfrac12)h$ 和 $y=jh$，$h\\ne0$。在 $F_j,G_j$ 非零的区域内，令','证明。令'),
('将式（N1）除以相应的 $\\tau$ 函数乘积，得到','将（S1）除以相应的 τ 函数乘积，得')],stop='上述消元在有限')
# This truncation omits the repeated continuous system N9; it is already C1.
parts[-1]+='\n\n消元对每个有限 $h>0$ 成立。□'
edit(21,[
('第一式的后向差分与相邻平均以 $y-h/2$ 为中心；第二式以 $y$ 为中心。保留这些评价位置后，两式均为二阶一致。','证明。第一式的后向差分与相邻平均以 $y-h/2$ 为中心，第二式以 $y$ 为中心。分别在这些位置作 Taylor 展开，奇次余项相消，得到（L1）。'),
('其证明分别来自 $g(y-h/2)$ 与 $g(y+h/2)$ 的对称 Taylor 展开，以及中心差商展开。下面 `C17` 同时包含采样与重构的精确对齐、重构误差的二阶界；`nonlinear_continuum_limit` 则明确展示（L1）。','对 $g(y-h/2)$ 和 $g(y+h/2)$ 作对称展开，并使用中心差商的二阶精度，得（L2）。□')])
edit(23,[
('固定谱参数，令 $P_i=p_i-a$、$Q_k=q_k+a$。格点相位的关键展开为',r'固定谱参数，令 $P_i=p_i-a$、$Q_k=q_k+a$，并记 $\chi_{ik}=\lambda_h(P_i)\lambda_h(Q_k)$、$\gamma_{ik}(s)=-(p_i-s)/(q_k+s)$。格点相位满足'),
('连续 Gram 函数因而为','连续 Gram 函数为'),
('为了在固定物理坐标比较不同格距的解，使用与格点完全一致的插值','在固定物理坐标下定义插值'),
('F 的半格偏移不可省略。在正实参数区域，每个矩阵元的 F 振幅满足','在正实参数区域，$F$ 的半格偏移使矩阵元的振幅满足'),
('它与（L3）均为 h 的偶函数延拓。行列式、对数及所需导数在紧区域上保持正则；对称重构使物理场的一阶项消失。','该振幅和（L3）均可在 $h=0$ 附近延拓为偶解析函数。'),
('固定任意有限 N 和满足定理 5 在某个 $h_0>0$ 处条件的谱数据。','固定任意有限 $N$，并假设谱数据在某个 $h_0>0$ 处满足定理 5 的条件。')],stop='Lean 的')
parts[-1]+=r'''

证明。由（L3）和（L6），有限 $h$ 的矩阵元及其所需导数在 $h=0$ 附近解析，且关于 $h$ 为偶函数。正性使极限行列式在每个紧区域上有正下界，故其对数导数也在该区域上解析。将（L7）中的中心差商延拓到 $h=0$，得到 $u^{(0)},v^{(0)}$；关于 $h$ 的一阶导数为零。对二阶余项在紧区域上取一致上界，分别得到两个场的 $O(h^2)$ 界，相加即得（L8）。

上述解析延拓同时允许在双线性方程的对称和及差商中取极限。由（S2），$f^{(0)},g^{(0)}$ 满足（C3），再由定理 1 得连续 DLW 方程。□'''
parts.append('## 附录　保留势的非线性表示')
edit(29,[('### 8.2　势差的乘积分解','### 势差的乘积分解'),('固定对数分支，定义中心比值','定义中心比值')],stop='沿用相同的正则性')

source='\n\n'.join(parts)
source=re.sub(r'\n{3,}','\n\n',source)
source=source.replace('（T10）—（T11）','（T10）和（T11）')
tags=re.findall(r'\\tag\{([^}]+)\}',source)
assert len(tags)==len(set(tags))
mapping={v:str(i+1) for i,v in enumerate(tags)}
source=re.sub(r'\\tag\{([^}]+)\}',lambda m:r'\tag{'+mapping[m[1]]+'}',source)
source=re.sub(r'（([A-Z]\d+)）',lambda m:'（'+mapping[m[1]]+'）',source)
assert not re.search(r'Lean|Notebook|Colab|`|—|–|StartPoint|代码|运行时',source)
(HERE/'paper.src.md').write_text(source,encoding='utf-8')
(HERE/'paper_revision.json').write_text(json.dumps({'notebook_sha256':hashlib.sha256((ROOT/'notebook/DLW理论.ipynb').read_bytes()).hexdigest(),'equation_map':mapping,'equations':len(tags),'removed_repeated_equations':['N1','N9'],'source':'paper.src.md'},ensure_ascii=False,indent=2),encoding='utf-8')
print('Paper source:',len(tags),'numbered equations')
