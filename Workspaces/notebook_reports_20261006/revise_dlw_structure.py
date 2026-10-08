"""Arrange the DLW notebook as equations, parameters, and executable scheme cells."""
from pathlib import Path
import ast
import copy
import json
import shutil
import nbformat as nbf

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
NOTEBOOK = ROOT / 'notebook/DLW数值分析report.ipynb'
BACKUP = HERE / 'before_scheme_revision'

TEXT = {
    'spatial-text': r'''## 2　空间离散与边界

$x\in[-20,20)$ 分为 256 份，$\Delta x=40/256=0.15625$；$y\in[-1.5,1.5]$ 分为 24 份，$h=0.125$，场值取各份中点。

记 $\delta_-f_j=(f_j-f_{j-1})/h$、$\delta_0f_j=(f_{j+1}-f_{j-1})/(2h)$、$M_-f_j=(f_j+f_{j-1})/2$。$x$ 向采用三点二阶中心差分；二阶导数与 GSG 对照格式的式 (4.13)–(4.14) 使用相同的三点算子：

$$D_1f_i=\frac{f_{i+1}-f_{i-1}}{2\Delta x},\qquad D_2f_i=\frac{f_{i+1}-2f_i+f_{i-1}}{\Delta x^2}.$$

$y$ 下侧取解析值，上侧虚点取解析背景加扰动的二次外推；SD、FD 的 $x$ 差分按周期延拓，SD2 按端点跃变量延拓。

**对应代码。** 下方定义共用网格、三点差分与场值恢复。''',
    'sd-text': r'''### 2.1　SD

**半离散非线性方程。** 以 $u_j,\omega_j$ 表示第一种非线性形式：

$$\begin{aligned}
\delta_-u_{j,t}
&+\partial_x\delta_-\left[\frac{u_j^2+\omega_j^2}{2}+2au_j-h\omega_j\right]
+\partial_x^2\left(\delta_-u_j+\frac4hM_-\omega_j\right)=0,\\
\omega_{j,t}&+\partial_x[(u_j+2a)\omega_j-hu_j]-\omega_{j,xx}=0.
\end{aligned}$$

$\omega_j=\partial_x(\log G_{j+1}-\log G_j)$，物理场为 $v_j=4\omega_j/h+\delta_0u_j$。取演化变量

$$P_j=\delta_-u_j,\qquad W_j=\frac4h\omega_j=v_j-\delta_0u_j,$$

并记

$$H_j=\frac{u_j^2}{2}+2au_j+h^2\left(\frac{W_j^2}{32}-\frac{W_j}{4}\right).$$

上式成为

$$\begin{aligned}
P_{j,t}&=-\delta_-\partial_xH_j-\partial_x^2(P_j+M_-W_j),\\
W_{j,t}&=-\partial_x[(u_j+2a)W_j-4u_j]+\partial_x^2W_j.
\end{aligned}$$

**离散递推。** 每个时间级先由下侧解析边界恢复

$$u_{j,i}(t)=u_{j_L,i}(t)+h\sum_{k=j_L+1}^{j}P_{k,i}(t),\qquad
v=W+\delta_0u,$$

再计算

$$\begin{aligned}
F_P&=-\delta_-D_1H-D_2(P+M_-W),\\
F_W&=-D_1[(u+2a)W-4u]+D_2W,\\
P^{n+1}&=P^n+\Delta t\,F_P(t_n),\qquad
W^{n+1}=W^n+\Delta t\,F_W(t_n).
\end{aligned}$$

参数：$a=2$、$h=0.125$、$\Delta x=0.15625$、$\Delta t=0.000125$、$T=0.01$。初值为 $P^0=\delta_-u_*(0)$、$W^0=v_*(0)-\delta_0u_*(0)$，$u_{j_L}(t)$ 取解析值。以上为 Euler 更新；同一右端的 RK4 更新见第 3 节。

**对应代码。** `pt`、`wt` 分别是 $F_P,F_W$；`axis=0` 沿 $y$，`d1,d2` 沿 $x$。''',
    'sd2-text': r'''### 2.2　SD2

**原半离散方程。** 以 $Q,R$ 为演化变量：

$$\begin{aligned}
Q_{j,t}&=-Q_{j,xx}-2aQ_{j,x}-\left[(M_j+M_{j+1})_x+\frac{h^2}{4}(Q_j^2R_j^2-1)\right]Q_j,\\
R_{j,t}&=R_{j,xx}-2aR_{j,x}+\left[(M_j+M_{j+1})_x+\frac{h^2}{4}(Q_j^2R_j^2-1)\right]R_j,\\
M_{j+1}-M_j&=h(1-Q_jR_j).
\end{aligned}$$

**离散递推。** 令 $S_j=Q_jR_j$、$G_j=h^2(S_j^2-1)/4$、$m_j=M_{j,x}$，下边界确定 $Q_0,Q_{0,t}$，然后计算

$$\begin{aligned}
m_0&=-\frac{Q_{0,t}+D_2Q_0+2aD_1Q_0}{2Q_0}-\frac{G_0}{2}+\frac h2D_1S_0,\\
m_{j+1}&=m_j-hD_1S_j,\qquad A_j=m_j+m_{j+1},\\
F_Q&=-D_2Q-2aD_1Q-(A+G)Q,\\
F_R&=D_2R-2aD_1R+(A+G)R,\\
Q_j^{n+1}&=Q_j^n+\Delta t\,F_{Q,j}(t_n)\quad(j\ge1),\qquad
R_j^{n+1}=R_j^n+\Delta t\,F_{R,j}(t_n)\quad(j\ge0),\\
u&=2(D_1Q)/Q,\qquad v=4(1-QR)+\delta_0u.
\end{aligned}$$

参数：$a=2$、$h=0.125$、$\Delta x=0.15625$、$\Delta t=0.000125$、$T=0.01$。初值与下边界通过

$$D_1Q_j^0=\tfrac12u_j^0Q_j^0,\qquad Q_{j,0}^0=1,\qquad
R_j^0=\frac{1-(v_j^0-\delta_0u_j^0)/4}{Q_j^0}$$

确定。下边界每个时间级求解 $D_1Q_0(t)=u_{*,0}(t)Q_0(t)/2$、$Q_{0,0}(t)=1$；这里的 $D_1$ 使用代码 `dx` 的端点跃变量修正。内部 $Q$ 与全部 $R$ 按上述右端推进，Euler 与 RK4 共用此右端。

**对应代码。** 先定义初值与下边界的求解，再定义递推；代码中的 `w` 对应 $S$、`H` 对应 $G$、`mx` 对应 $m$。''',
    'fd-text': r'''### 2.3　FD

**原连续方程。**

$$\begin{aligned}
u_{yt}&=-\partial_x[(u+2a)u_y]-v_{xx},\\
v_t&=-\partial_x[(u+2a)v-4u]-u_{xxy}.
\end{aligned}$$

**离散递推。** 取 $P=\delta_-u$，每个时间级由 $u_{j,i}=u_{j-1,i}+hP_{j,i}$ 恢复 $u$，然后计算

$$\begin{aligned}
F_P&=-\delta_-D_1\left(\frac{u^2}{2}+2au\right)-D_2M_-v,\\
F_v&=-D_1[(u+2a)v-4u]-D_2\delta_0u,\\
P^{n+1}&=P^n+\Delta t\,F_P(t_n),\qquad v^{n+1}=v^n+\Delta t\,F_v(t_n).
\end{aligned}$$

参数：$a=2$、$h=0.125$、$\Delta x=0.15625$、$\Delta t=0.000125$、$T=0.01$。初值为 $P^0=\delta_-u_*(0)$、$v^0=v_*(0)$。Euler 与 RK4 共用此右端。

**对应代码。** `fp`、`fv` 分别是 $F_P,F_v$，`uy` 是 $\delta_0u$。''',
    'mesh-text': r'''### 2.4　网格策略

固定网格取 $s=0$、$V=0$。动网格初始节点按 $\bar\rho$ 的累积积分等分，之后使用

$$\begin{aligned}
x_i&=\xi_i+s_i,\qquad J_i=1+D_\xi s_i,\qquad D_1=J^{-1}D_\xi,\\
D_2f&=J^{-2}D_{\xi\xi}f-J^{-3}(D_\xi J)(D_\xi f),\\
\rho_j&=1-(v_j-\delta_0u_j)/4,\qquad
\bar\rho=\frac1{24}\sum_j\rho_j,\\
\bar q&=\frac1{24}\sum_j[(u_j+2a)\rho_j-D_1\rho_j-2a],\qquad
V_i=\frac{\bar q_i-\bar q_0}{\bar\rho_i},\\
\dot x_i&=V_i,\qquad \dot z=\mathcal F(t,z)+VD_1z.
\end{aligned}$$

$D_\xi$、$D_{\xi\xi}$ 为前述三点二阶中心差分，$\Delta\xi=0.15625$；节点与场值同步使用 Euler 或 RK4 更新。''',
}

SD = '''class SDModel(PhysicalModel):
    def rhs(self, t, z):
        p, w = self.unpack(z)
        u = self.recover_u(p, t)
        gl, gr = ghost_u(self.G, self.js, self.X.x, t, u)
        v = w+delta0(u, (gl, gr), self.h)
        d1, d2, h, a = self.X.d1, self.X.d2, self.h, self.a
        H = u*u/2+2*a*u+h*h*(w*w/32-w/4)
        pe = np.vstack(((u[0]-gl)/h, p, (gr-u[-1])/h))
        lap = (pe[2:]-2*pe[1:-1]+pe[:-2])/(h*h)
        fp = -np.diff(d1(H), axis=0)/h-d2((v[1:]+v[:-1])/2-h*h*lap/4)
        fw = -d1((u+2*a)*w-4*u)+d2(w)
        return self.pack(fp, fw)
'''

FD = '''class FDModel(PhysicalModel):
    def rhs(self, t, z):
        p, v = self.unpack(z)
        u = self.recover_u(p, t)
        ghosts = ghost_u(self.G, self.js, self.X.x, t, u)
        uy = delta0(u, ghosts, self.h)
        d1, d2, h, a = self.X.d1, self.X.d2, self.h, self.a
        fp = -np.diff(d1(u*u/2+2*a*u), axis=0)/h-d2((v[1:]+v[:-1])/2)
        fv = -d1((u+2*a)*v)-d2(uy)+4*d1(u)
        return self.pack(fp, fv)
'''

def build_spatial_cells(codes):
    cells = []
    def md(name):
        cells.append(nbf.v4.new_markdown_cell(TEXT[name].strip(), id='dlw-'+name))
    def code(name):
        cells.append(nbf.v4.new_code_cell(codes[name].strip(), id='dlw-'+name))
    md('spatial-text')
    code('spatial')
    code('sd_fd')
    md('sd-text')
    code('sd')
    md('sd2-text')
    code('sd2_lift')
    code('sd2_evolution')
    md('fd-text')
    code('fd')
    md('mesh-text')
    code('mesh')
    return cells

def revise():
    BACKUP.mkdir(exist_ok=True)
    sources = ['build_dlw_numerics_notebook.py', 'dlw_numeric_cells.py', 'verify_dlw_models.py']
    for path in [NOTEBOOK, *(HERE / name for name in sources)]:
        backup = BACKUP / path.name
        if not backup.exists():
            shutil.copy2(path, backup)

    # Preserve the original arithmetic; only place each RHS in its own visible class.
    source = HERE / 'dlw_numeric_cells.py'
    text = source.read_text(encoding='utf-8')
    ns = {}
    exec(compile(text, str(source), 'exec'), ns)
    codes = ns['CELLS']
    base = codes['sd_fd'].split('\n    def rhs(self, t, z):')[0] + '\n'
    old = "CELLS['sd_fd'] = r'''" + codes['sd_fd'] + "'''"
    new = "CELLS['sd_fd'] = r'''" + base + "'''"
    if "CELLS['sd']" not in text:
        text = text.replace(old, new)
        text += "\nCELLS['sd'] = r'''" + SD + "'''\n"
        text += "\nCELLS['fd'] = r'''" + FD + "'''\n"
    text = text.replace("else PhysicalModel(case, model, config)",
                        "else (SDModel if model == 'SD' else FDModel)(case, model, config)")
    ast.parse(text)
    source.write_text(text, encoding='utf-8')
    ns = {}
    exec(compile(text, str(source), 'exec'), ns)
    codes = ns['CELLS']

    builder = HERE / 'build_dlw_numerics_notebook.py'
    text = builder.read_text(encoding='utf-8')
    if 'from revise_dlw_structure import build_spatial_cells' not in text:
        text = text.replace('from dlw_numeric_cells import CELLS',
                            'from dlw_numeric_cells import CELLS\nfrom revise_dlw_structure import build_spatial_cells')
        start = text.index("    md('spatial-text'")
        end = text.index("    md('time-text'", start)
        text = text[:start] + '    cells.extend(build_spatial_cells(CELLS))\n' + text[end:]
        builder.write_text(text, encoding='utf-8')

    verifier = HERE / 'verify_dlw_models.py'
    text = verifier.read_text(encoding='utf-8')
    text = text.replace("'sd_fd', 'sd2_lift'", "'sd_fd', 'sd', 'fd', 'sd2_lift'")
    verifier.write_text(text, encoding='utf-8')

    nb = nbf.read(NOTEBOOK, as_version=4)
    original = {c.id: c for c in nb.cells}
    start = next(i for i, c in enumerate(nb.cells) if c.id == 'dlw-spatial-text')
    end = next(i for i, c in enumerate(nb.cells) if c.id == 'dlw-time-text')
    replacement = build_spatial_cells(codes)
    for cell in replacement:
        prior = original.get(cell.id)
        if prior is not None and cell.cell_type == 'code':
            cell.outputs = copy.deepcopy(prior.outputs)
            cell.execution_count = prior.execution_count
            cell.metadata = copy.deepcopy(prior.metadata)
    nb.cells = nb.cells[:start] + replacement + nb.cells[end:]
    # The experiment design states x/y subdivision in section 2 instead of twice.
    nb.cells[2].source = r'''## 1　模型与实验设计

连续 DLW 方程为

$$\begin{aligned}
u_{yt}&=-\partial_x[(u+2a)u_y]-v_{xx},\\
v_t&=-\partial_x[(u+2a)v-4u]-u_{xxy}.
\end{aligned}$$

采用 Sheng–Yu 原文的三组孤子参数，$a=2$、$c_i=1$，初相位为零。A、B 分别对应图 1(a)、1(b)，C 对应图 3；具体 $p_i,q_i$ 如下表。取 $\Delta t=0.000125$、$T=0.01$。'''
    # Keep generator and delivered prose identical.
    text = builder.read_text(encoding='utf-8')
    start = text.index("    md('design', r'''")
    end = text.index("    code('config')", start)
    text = text[:start] + "    md('design', r'''" + nb.cells[2].source + "''')\n" + text[end:]
    ast.parse(text)
    builder.write_text(text, encoding='utf-8')
    for c in nb.cells:
        if c.cell_type == 'code':
            ast.parse(c.source)
    nbf.validate(nb)
    nbf.write(nb, NOTEBOOK)
    print(json.dumps({'notebook': str(NOTEBOOK), 'cells': len(nb.cells),
                      'sections': ['2.1 SD', '2.2 SD2', '2.3 FD', '2.4 网格策略'],
                      'backup': str(BACKUP)}, ensure_ascii=False))

if __name__ == '__main__':
    revise()
