from pathlib import Path
import re,json
from bs4 import BeautifulSoup

HERE=Path(__file__).resolve().parent

def revise(s):
    def rep(a,b):
        nonlocal s
        assert s.count(a)==1,(a[:90],s.count(a))
        s=s.replace(a,b,1)
    rep('## 2　交错格点双线性系统','## 2　沿 $y$ 方向的半离散双线性系统')
    a=s.index('式（4）表明');b=s.index('令 $G_j$',a)
    s=s[:a]+r'''本文沿 $y$ 方向离散连续 DLW 的双线性方程，保留 $x,t$ 为连续变量。为保持可积结构，采用两组相差半个格距的 τ 函数，并对双线性算子的参数作对称平移。交错布置使同一行列式解同时满足两条相邻格点关系，其精确性将在第 3 节证明。

记 $B_s=D_x^2+D_t+2sD_x$，其中 $D_x,D_t$ 为 Hirota 双线性算子。

'''+s[b:]
    rep('本节给出半离散系统的 Gram 行列式解，并证明所定义的 τ 函数满足式（5）。',
        '本节给出 Gram 行列式解，并证明所定义的 τ 函数满足沿 $y$ 方向的半离散双线性方程。')
    a=s.index('**定理 3.1');b=s.index('引入辅助层 $n$',a)
    s=s[:a]+r'''**定理 3.1（任意有限阶 Gram 精确解）。** 设 $h>0$，$N\ge1$ 为整数，$p_i,q_i,\rho_i,s$ 为实参数。记 $d=h/2$、$\lambda_h(z)=(z+d)/(z-d)$，并假设对所有 $i,k$，有 $p_i+q_k\ne0$、$p_i-a\pm d\ne0$、$q_k+a\pm d\ne0$、$q_k+s\ne0$。

'''+s[b:]
    rep('引入辅助层 $n$ 和参数 $s$，定义 Gram 行列式','对非负整数辅助层 $n$，定义 Gram 行列式')
    rep(r'$\tau_0$ 与 $s$ 无关。对于一般辅助层，要求 $q_k+s\ne0$；涉及负整数层时，还要求 $p_i-s\ne0$。'+'\n\n','')
    rep('以下相邻辅助层恒等式用于验证上述 τ 函数满足的双线性关系。','为证明定理 3.1，先建立以下相邻辅助层恒等式。')
    a=s.index('## 4　');b=s.index('记格点差分和平均算子为',a)
    s=s[:a]+'''## 4　非线性化

本节由半离散双线性方程导出物理场的非线性演化方程。先通过对数变换建立共同的场变量关系，再分别采用差分消势形式（PE）和势函数形式（PF）完成非线性系统的闭合。

### 4.1　物理变量与非线性演化关系

'''+s[b:]
    a=s.index('**定理 4.1');b=s.index('**证明。**',a)
    theorem=s[a:b].strip();s=s[:a]+s[b:].replace('**证明。** 令', '令',1)
    a=s.index('式（26）是两种非线性化的共同起点。');b=s.index('由式（24）、（25）可得',a)
    s=s[:a]+'''式（26）给出共同的非线性演化关系，其中辅助势 $Z_j$ 已由 τ 函数的对数导数定义。以下分别通过格点差分和势函数表示处理 $Z_j$，得到 PE 与 PF 两种形式。

### 4.2　差分消势形式（PE）

差分消势形式（potential-elimination formulation，PE）对第一条演化方程作格点差分，利用 $Z_j$ 的相邻差消去该辅助势。

'''+theorem+'\n\n**证明。** '+s[b:]
    rep('## 5　势函数形式（PF）','### 4.3　势函数形式（PF）')
    rep('并沿用上一节的记号','并沿用本节的记号')
    rep('对严格正的 $F_j,G_j$，定义','设严格正的 $F_j,G_j$ 满足半离散双线性方程，定义')
    rep('本小节建立精确解之间的连续极限：在固定谱参数下，半离散 Gram 解恢复的 $u^{(h)},v^{(h)}$ 一致趋于连续 Gram 解的物理场，误差为 $O(h^2)$。定理同时给出作为极限的连续行列式表达。',
        '本小节证明所构造的半离散精确解本身趋于连续 DLW 解。命题 6.2 对给定的连续 τ 函数建立重构误差估计；这里的 τ 函数则随格距 $h$ 改变，其相位与振幅也随之变化。在固定谱参数下，以下定理证明这一精确解族恢复的 $u^{(h)},v^{(h)}$ 仍以 $O(h^2)$ 一致收敛，并给出其连续行列式极限。')
    rep('$B_j^{-1}$ 在形式伪微分算子代数中定义。相容条件为',r'''$B_j^{-1}$ 在形式伪微分算子代数中定义。格点关系写为 $\psi_{j+1}=T_j\psi_j$。对其求时间导数，并分别代入两层的时间方程，得到

$$\psi_{j+1,t}=(T_{j,t}+T_j\mathscr Q_j)\psi_j,\qquad
\psi_{j+1,t}=\mathscr Q_{j+1}T_j\psi_j.$$

因此，两种计算给出同一时间演化的条件为''')
    rep('为比较这两种演化次序，分别考察一阶算子 $A_j,B_j$ 与时间算子的交织关系。其未抵消的零阶项由以下两个残差表示：',
        '下面计算一阶算子与时间演化算子交换作用次序后产生的差。导数项抵消后，剩余项是乘法算子，其系数记为')
    rep('由系统（46）和关系（47），两项残差均为零。另一方面，乘积法则给出 Darboux 恒等式',
        r'式（52）的第一条右端是 $w_j$ 演化方程的 $h/4$ 倍，故为零；第二条右端则因（47）中 $V_{j,x}$ 的定义而为零。因此两项残差的和与差均为零，即 $\mathcal E_j^\alpha=\mathcal E_j^\eta=0$。这一消去把非线性方程与下面的线性算子关系联系起来。由乘积法则有 Darboux 恒等式')
    rep(r'分别取 $r=\alpha_j,\eta_j$，共同的中间势为 $V_j+2\alpha_{j,x}=V_{j+1}+2\eta_{j,x}$。两条交织关系代入 $T_{j,t}=(B_j^{-1}A_j)_t$，中间势抵消，即得（50）。',r'''令 $L_j=\partial_t+\partial_x^2+V_j$。当式（53）的右端为零时，先作用 $\partial_x-r$ 再作用新的时间算子，与先作用原时间算子再作用 $\partial_x-r$ 得到相同结果；这就是此处的交织关系。

分别取 $r=\alpha_j$ 和 $r=\eta_j$，并使用已证明为零的两项残差。由势差关系，二者具有共同的中间势 $\widetilde V_j=V_j+2\alpha_{j,x}=V_{j+1}+2\eta_{j,x}$。记 $\widetilde L_j=\partial_t+\partial_x^2+\widetilde V_j$，则

$$\widetilde L_jA_j=A_jL_j,\qquad
\widetilde L_jB_j=B_jL_{j+1}.$$

消去共同的 $\widetilde L_j$ 得到 $L_{j+1}B_j^{-1}A_j=B_j^{-1}A_jL_j$，即 $L_{j+1}T_j=T_jL_j$。展开其中的时间导数，恰为相容条件（50）。因此，非线性方程使两项残差为零，进而保证所给 Lax 对相容。''')
    rep(r'将 $x\in[-L/2,L/2)$ 等分为 $N_x$ 个区间，取',
        r'固定网格计算中，将 $x\in[-L/2,L/2)$ 等分为 $N_x$ 个区间，取')
    rep('对 $x$ 的一、二阶导数分别采用中心差分',
        r'自适应计算仅调整 $x$ 节点的位置 $x_i(t)$，从而改变相邻节点间距 $x_{i+1}(t)-x_i(t)$；$y$ 方向格距 $h$、层编号 $j$ 和时间步长 $\Delta t$ 均保持不变。动网格的初始布点由下文的守恒密度等分确定。'+'\n\n在固定均匀网格上，对 $x$ 的一、二阶导数分别采用中心差分')
    rep(r'在均匀计算坐标 $\xi_i=-L/2+i\Delta\xi$ 上写 $x_i(t)=\xi_i+s_i(t)$，令 $J_i=1+D_\xi s_i$。移动节点上的 $x$ 导数由链式法则计算：',r'''物理节点移动后，相邻 $x$ 间距不再相等。为在同一节点编号上计算导数，引入固定均匀的计算坐标 $\xi_i=-L/2+i\Delta\xi$，其中 $\Delta\xi=L/N_x$。写 $x_i(t)=\xi_i+s_i(t)$，$s_i$ 是节点位移，$J_i=1+D_\xi s_i$ 近似坐标映射的伸缩率 $J=x_\xi$。

对于定义在移动节点上的场，链式法则给出 $\partial_x=J^{-1}\partial_\xi$。再作用一次该算子，就会对 $J^{-1}$ 求导，因而

$$\partial_{xx}z=\frac{z_{\xi\xi}}{J^2}-\frac{J_\xi z_\xi}{J^3}.$$

分别以均匀 $\xi$ 网格上的中心差分近似这些导数，得到''')
    a=s.index('## 9　数值结果');b=s.index('## 10　结论',a)
    results=(HERE/'full_comparison_results.md').read_text(encoding='utf-8')
    tabs=re.findall(r'<div class="table-wrap">[\s\S]*?</div>',s[a:b])
    assert len(tabs)==3
    results=results.replace('SPACE_TABLE',tabs[0]).replace('TIME_TABLE',tabs[1])
    raw=json.loads((HERE/'tables.json').read_text(encoding='utf-8'))['mesh_table']
    rows=BeautifulSoup(raw,'html.parser').select('tbody tr')
    values=[[c.get_text(strip=True) for c in r.find_all('td')] for r in rows]
    table='<div class="table-wrap"><table class="comparison paired-errors"><thead><tr><th>算例</th><th>方法</th><th>固定网格：u / v</th><th>动网格：u / v</th></tr></thead><tbody>'
    for c,case in enumerate(['单孤子 A','单孤子 B','二孤子']):
        for m,method in enumerate(['PE','PF','FD']):
            u,v=values[c*6+m*2:c*6+m*2+2]
            table+=f'<tr><th>{case}</th><th>{method}</th><td>{u[0]} / {v[0]}</td><td><strong>{u[1]} / {v[1]}</strong></td></tr>'
    table+='</tbody></table></div>'
    results=results.replace('MESH_TABLE',table)
    for c,case in enumerate('ABC'):
        label=['单孤子 A','单孤子 B','二孤子'][c]
        for offset,kind in enumerate(['fields','errors']):
            n=2*c+offset+1
            what='数值物理场' if kind=='fields' else '绝对误差'
            cap=f'图 {n}　{label}的{what}。左、中、右列依次为 PE、PF、FD；第一、二行为 u 的曲面和等高线，第三、四行为 v 的曲面和等高线。RK4，固定网格，T = 0.01。同一物理量在三种方法间采用共同色阶。'
            if kind=='errors':cap=cap.replace('u 的','u 误差的').replace('v 的','v 误差的')
            fig=f'<figure><a href="../Workspaces/dlw_paper_20261009/figures/{case}_{kind}.png"><img src="../Workspaces/dlw_paper_20261009/figures/{case}_{kind}.png" alt="{label}，PE/PF/FD三列四行{what}对照" loading="lazy"></a><figcaption>{cap}</figcaption></figure>'
            results=results.replace('FIGURE_'+str(n),fig)
    s=s[:a]+results+'\n\n'+s[b:]
    a=s.index('## 附录 A');b=s.index('## 参考文献',a);s=s[:a]+s[b:]
    a=s.index('## 10　结论');b=s.index('## 数据与代码说明',a)
    s=s[:a]+'''## 10　结论

本文沿 $y$ 方向构造了（2+1）维 DLW 方程的半离散双线性系统，并给出任意有限阶的 Gram 行列式解。通过对共同辅助势作格点差分消元和势函数表示，导出 PE 与 PF 两种非线性形式，并建立其 Darboux–Lax 表示。在正则谱参数条件下，半离散方程和物理变量重构均具有二阶一致性，固定谱参数的精确 Gram 解族以 $O(h^2)$ 趋于连续 DLW 解。

基于两种非线性形式给出数值方法，并通过单孤子 A、单孤子 B 和二孤子考察空间离散、时间推进和网格运动的影响。固定网格上，PE、PF 与 FD 的误差排序随算例和物理场变化；RK4 与 C–N 在单孤子 B 和二孤子中的误差接近，且小于 Euler。采用守恒密度驱动的 $x$ 向动网格后，三种方法的两个物理场误差均减小。三种方法并列的物理场与误差图展示了相同计算条件下的波形及其空间偏差。

'''+s[b:]
    s=re.sub(r'(<th\b[^>]*>)([ABC])(</th>)',lambda m:m[1]+{'A':'单孤子 A','B':'单孤子 B','C':'二孤子'}[m[2]]+m[3],s)
    s=s.replace('附录中的误差表','正文中的误差表').replace('正文和正文','正文')
    s=s.replace('正文中的误差表使用这些既有结果。',
        '正文中的误差表使用这些既有结果。三种方法的宽域场图另附[场数据准备程序](../Workspaces/dlw_paper_20261009/prepare_comparison_fields.py)与[绘图程序](../Workspaces/dlw_paper_20261009/plot_comparison_fields.py)。')
    theorem_map={'5.1':'4.2','6.1':'5.1','6.2':'5.2','6.3':'5.3','7.1':'6.1'}
    s=re.sub(r'(命题|定理|引理) (\d+\.\d+)',lambda m:m[1]+' '+theorem_map.get(m[2],m[2]),s)
    s=re.sub(r'^(#{2,3}) (\d+)([.　])',lambda m:m[1]+' '+str(int(m[2])-1 if int(m[2])>=6 else int(m[2]))+m[3],s,flags=re.M)
    def section_ref(m):
        n=int(m[1]);sub=m[2] or ''
        if n==5:return '第 4.3 节'
        return '第 '+str(n-1 if n>=6 else n)+sub+' 节'
    s=re.sub(r'第 (\d+)(\.\d+)? 节',section_ref,s)
    a=s.index('本文的安排如下。');b=s.index('\n\n',a)
    s=s[:a]+'''本文的安排如下。第 1、2 节介绍连续双线性表示及沿 $y$ 方向的半离散化。第 3 节给出 Gram 行列式解及其证明。第 4 节完成非线性化，并分别导出 PE 和 PF 两种形式。第 5 节建立连续极限，第 6 节给出 Lax 表示。第 7 节介绍数值方法，第 8 节给出精确解基准及空间离散、时间算法和固定／动网格比较，展示三组孤子的数值物理场与误差。第 9 节给出结论。'''+s[b:]
    tags=re.findall(r'\\tag\{([^}]+)\}',s);mapping={n:str(i+1) for i,n in enumerate(tags)}
    assert len(tags)==len(mapping)
    s=re.sub(r'\\tag\{([^}]+)\}',lambda m:r'\tag{'+mapping[m[1]]+'}',s)
    s=re.sub(r'（(\d+|E\d+)）',lambda m:'（'+mapping.get(m[1],m[1])+'）',s)
    assert '## 附录' not in s and 'SD2' not in s
    assert 'FIGURE_' not in s and '_TABLE' not in s
    return s
