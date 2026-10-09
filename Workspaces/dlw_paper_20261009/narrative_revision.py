"""Paper narrative and results organization; reuse all stored numerical evidence."""
from pathlib import Path
import re, json
from bs4 import BeautifulSoup
from methods_revision import clean_table

HERE = Path(__file__).resolve().parent

def revise(source):
    original_display = re.findall(r'\$\$[\s\S]*?\$\$', source)
    changes = []
    def replace(old, new):
        nonlocal source
        assert source.count(old) == 1, (old[:100], source.count(old))
        source = source.replace(old, new, 1)
        changes.append({'before': old, 'after': new})
    def after(anchor, prose):
        replace(anchor, anchor + '\n\n' + prose)

    replace('通过与解析解及直接差分方法比较，考察两种非线性形式的误差以及网格移动对计算精度的影响。',
        '固定网格计算中，三种格式的误差排序随算例和物理场变化；在所考察的单孤子与二孤子算例中，动网格均降低了两个物理场的误差。')
    replace('Hirota 双线性方法为构造非线性可积方程的行列式解及其离散形式提供了有效途径。',
        '色散长波（DLW）方程描述具有有限水深的宽水道或开阔水域中的长波运动，其中两个物理场分别对应水平速度与相对静水面的波高 [1]。其孤子解为研究波形及相互作用提供了解析模型，也为检验数值方法提供了明确的参照。Hirota 双线性方法通过因变量变换，将非线性方程转化为适合行列式构造的双线性关系。')
    after('本文以该双线性表示为基础，研究 DLW 系统的半离散化。',
        '本文关注的离散化需要同时连接解的构造与物理场的演化。一方面，离散后的双线性方程应保留可直接验证的行列式解；另一方面，通过该解恢复的物理场应在格距趋于零时回到连续 DLW 解。这两个要求分别涉及离散恒等式与连续极限，也是下文组织理论推导的依据。')
    replace('第 9 节比较两种形式与直接差分方法的数值结果，第 10 节给出结论。',
        '第 9 节给出空间差分、动网格与时间推进方法，第 10 节按格式比较、网格改善和孤子波形组织数值结果，第 11 节给出结论。附录收录完整误差表和补充算例图。')
    after('## 1　连续 DLW 方程的双线性表示',
        '先给出连续方程与 τ 函数之间的对应关系。它既确定半离散系统应恢复的极限方程，也确定后续比较解时所采用的物理变量。')
    replace('由于\n\n$$D_yB_af', '为使第二条双线性关系便于沿 $y$ 方向离散，先将其中的 $y$ 导数集中到第二个因子上。利用\n\n$$D_yB_af')
    after('**命题 1.1（双线性表示与物理场）。** 设 $f,g$ 在开区域内严格为正且实解析，并满足（3）。则由（2）定义的 $u,v$ 满足（1）。',
        '证明中先从第一条双线性关系得到 $u$ 的演化关系，再借助组合 $v-u_y$ 恢复第二条方程。该组合在半离散情形中将对应后文的变量 $W_j$。')
    after('## 2　交错格点双线性系统',
        '式（4）表明，连续双线性对可由同一算子作用于 $g$ 及其 $y$ 导数来描述。因此，将 $f$ 放在两个相邻 $g$ 格点的中间，并同时对算子参数作对称平移，可以使两条离散关系的平均与差商分别对应连续双线性对。')
    after('## 3　Gram 行列式解',
        '接下来构造式（5）的精确解。保留连续解在 $x,t$ 方向的指数因子，以有理格点乘子的幂表示 $y$ 方向的依赖。辅助层的相邻关系用于证明双线性恒等式，格点乘子则把这一层间关系连接到相邻空间格点。')
    replace('本节证明式（9）满足半离散双线性方程（5）。首先建立相邻辅助层之间的双线性恒等式。',
        '证明分为两步。首先固定空间格点，利用相邻辅助层之间的秩一更新得到算子 $B_s$ 的双线性恒等式。随后利用格点乘子与参数平移的关系，将同一恒等式分别用于 $G_j$ 和 $G_{j+1}$，从而得到式（5）的两条方程。')
    replace('**证明。** 将第 $n$ 层矩阵写为',
        '**证明。** 将矩阵元的行参数与列参数分开，使求导和辅助层移位都能写成低秩矩阵关系。将第 $n$ 层矩阵写为')
    after('式（13）的最后一式由矩阵行列式引理得到。由 Jacobi 微分公式，有 $\\kappa=\\tau_{n,x}/\\tau_n$。再令',
        '这里的 $\\psi$ 是相邻两个行列式的比值，$\\kappa$ 是第 $n$ 层行列式的对数导数。只需建立这两个标量之间的微分关系，即可通过双线性算子的展开恢复所需恒等式。为收集求导产生的项，记')
    # Avoid the dangling "再令" left by the explanatory insertion.
    replace('由 Jacobi 微分公式，有 $\\kappa=\\tau_{n,x}/\\tau_n$。再令',
        '由 Jacobi 微分公式，有 $\\kappa=\\tau_{n,x}/\\tau_n$。')
    replace('即（15）的第二式。对该式再求一次 $x$ 导数，并代入其余三式，得到',
        '即（15）的第二式。接下来的消元将消去 $\\eta_1,\\eta_2$，使结果仅含 $\\zeta$ 与 $\\kappa_x$。为此，对该式再求一次 $x$ 导数，并代入其余三式，得到')
    replace('**证明。** 在（10）中取 $n=0$、$s=a-d$，得到（5）的第一条方程。对于第二条，逐矩阵元有',
        '**证明。** 第一条方程直接来自相邻层恒等式：在（10）中取 $n=0$、$s=a-d$ 即可。第二条涉及格点 $j+1$，需要先将 $F_j$ 改写为该格点上参数为 $a+d$ 的第一层。逐矩阵元有')
    after('## 5　正则性与 PE 形式',
        '由双线性解转向非线性物理场时，需要对 τ 函数取对数。以下先确定使这一变换保持正则的谱参数条件，再从双线性方程的和与差导出演化关系。PE 形式通过对辅助势作格点差分完成闭合。')
    after('### 5.2　PE 形式的推导',
        '交错格点上，两侧 τ 函数对数差的平均给出 $u_j$，相邻 $G$ 层的对数差则给出 $\\omega_j$。为与连续变量 $v$ 对应，再将 $\\omega_j$ 与 $u_j$ 的中心差分组合。下面先固定这些变量及差分记号。')
    replace('两侧对数差的 $x$ 导数分别为 $(u_j+\\omega_j)/2$ 和 $(u_j-\\omega_j)/2$。再记',
        '两侧对数差的 $x$ 导数分别为 $(u_j+\\omega_j)/2$ 和 $(u_j-\\omega_j)/2$，因此式（23）的平方项可由 $u_j,\\omega_j$ 表示。两式相加时还会出现对数和的导数，将其记为辅助势')
    replace('为消去式（26）中的辅助势 $Z_j$，由式（24）、（25）可得',
        '式（26）是两种非线性化的共同起点。其中 $\\omega_j$ 的演化已由 $u_j,\\omega_j$ 决定，第一式还含辅助势 $Z_j$。在 PE 路线中，对第一式作格点差分；这一操作之所以能闭合，是因为 $Z_j$ 的相邻差已由物理变量确定。由式（24）、（25）可得')
    replace('本节通过引入势函数，将式（26）化为另一种非线性形式。',
        'PF 路线保留式（26）中的辅助势，以整数格点上的势函数表示它。这样可以直接推进势变量，并由对数导数和乘积恢复物理场。PE 与 PF 的区别由此归结为对同一 $Z_j$ 的不同处理。')
    replace('进一步引入因变量变换\n\n$$Q_j=',
        '第一条方程中同时出现 $u_{j,x}$ 与 $u_j^2/2$。取 $u_j$ 为一个函数的对数导数，可将这两个项合并为该函数的二阶导数与自身之比。相应地引入\n\n$$Q_j=')
    replace('再定义\n\n$$R_j=',
        '为将 $\\omega_j$ 的演化也写成势变量的方程，将 $1-\\omega_j/h$ 分解为 $Q_jR_j$。其中 $Q_j$ 已由 τ 函数确定，因而定义\n\n$$R_j=')
    replace('代入式（37）的第一式，得到 PF 系统',
        '此时第一组括号已由 $Q_j$ 方程确定，消去它便得到 $R_j$ 的演化方程。两条演化方程与 $M_j$ 的格点约束合在一起，构成 PF 系统')
    replace('下面分别考察非线性方程、物理变量变换及 Gram 解族的连续极限。所有估计均在固定紧集上进行。',
        '连续极限需要处理三个相互衔接的问题。首先，将光滑物理场代入半离散方程，比较其残差与连续 DLW 方程；其次，检验交错 τ 重构是否保持物理变量的二阶精度；最后，对随 $h$ 变化的精确 Gram 解族证明同样的二阶收敛。前两步给出局部展开，第三步将展开用于实际解族。所有估计均在固定紧集上进行。')
    after('### 7.1　非线性方程的一致性',
        '第一条非线性方程含后向差分，其自然评价点位于相邻物理层的中间；第二条方程含中心差分，评价点仍位于物理层。分别围绕这两个位置展开，可保留交错离散的对称性。')
    replace('即（42）的第一式。第二条中的通量满足',
        '即（42）的第一式。对于第二条方程，关键是来自中心差分的 $(u+2a)u_y$ 与 $W$ 中的 $-u_y$ 相互抵消，使极限通量恢复为连续方程的通量。具体地，')
    after('### 7.2　物理变量重构的一致性',
        '方程的一致性之外，还需检查变量变换本身。这里先固定一对连续 τ 函数，只考察半格点平均和中心差商引入的误差。这一结果将在下一节用于随格距变化的 τ 解族。')
    after('### 7.3　固定谱参数的 Gram 解族',
        '精确半离散 τ 函数的格点相位和振幅均依赖 $h$。因此，需要先在同一连续坐标下比较离散与连续行列式，再将估计传递给物理场。下面固定谱数据，通过正实指数插值把格点解延伸到连续 $y$ 坐标。')
    replace('**证明。** 记 $z_i=p_i-a<0$、$w_k=q_k+a>0$。',
        '**证明。** 先分别估计矩阵元的相位和振幅，再利用有限阶行列式及对数变换传递误差。记 $z_i=p_i-a<0$、$w_k=q_k+a>0$。')
    replace('对 $f^{(h)}$，半格移位后的矩阵元振幅因子为',
        '对 $f^{(h)}$，辅助层参数的平移与物理位置的半格移位同时作用于振幅。将两者合并后，一阶误差消去，矩阵元振幅因子为')
    after('## 8　两种非线性形式的 Lax 表示',
        '本节给出连接格点移位与时间演化的辅助线性问题，并检验两种操作的相容性。先在 PE 变量中构造一阶格点关系和二阶时间方程，再通过第 6 节的变量变换得到 PF 表示。证明的关键是将相容条件化为两项标量残差，其和与差分别对应非线性演化关系。')
    replace('取辅助函数 $\\psi_j$，定义',
        '格点关系描述辅助函数从 $j$ 到 $j+1$ 的变化，时间方程规定每一层的演化。要求先移位后演化与先演化后移位给出相同结果，便得到相容条件。取辅助函数 $\\psi_j$，定义')
    replace('定义残差\n\n$$\\begin{aligned}\n\\mathcal E_j',
        '为比较这两种演化次序，分别考察一阶算子 $A_j,B_j$ 与时间算子的交织关系。其未抵消的零阶项由以下两个残差表示：\n\n$$\\begin{aligned}\n\\mathcal E_j')
    replace('在 PF 中，$U_j=',
        'PE 与 PF 对应同一组物理场，因此可将前述线性问题直接写成势变量形式。在 PF 中，$U_j=')

    # Separate methods from results. Keep all displayed equations byte-for-byte.
    replace('## 9　数值方法与数值结果','## 9　数值方法')
    replace('本节基于 PE 和 PF 两种非线性形式构造数值格式，并与连续 DLW 方程的直接差分格式（FD）比较。以单孤子和二孤子解析解为参照，考察不同时间算法以及固定、动网格下的数值误差。',
        '前述构造给出了沿 $y$ 方向离散、在 $x,t$ 方向连续的非线性系统。数值计算以 PE 的 $P,W$ 或 PF 的 $Q,R$ 为演化变量，通过相应重构得到 $u,v$。本节依次说明空间差分、网格运动和时间推进，并给出连续 DLW 方程的直接差分格式（FD）作为比较对象。三种格式均以连续解析解确定初始物理场与边界数据。')
    start=source.index('### 9.4　')
    end=source.index('## 10　结论')
    old=source[start:end]
    figures=re.findall(r'<figure>[\s\S]*?</figure>',old)
    assert len(figures)==6
    setup=old[:old.index('**表 1')].replace('### 9.4　参数设置与误差比较','### 10.1　算例与误差度量')
    # Reuse the existing error definition and experiment parameters exactly.
    tables=json.loads((HERE/'tables.json').read_text(encoding='utf-8'))
    rawmesh=BeautifulSoup(tables['mesh_table'],'html.parser')
    vals=[[float(x.get_text()) for x in row.find_all('td')] for row in rawmesh.select('tbody tr')]
    assert len(vals)==18 and all(len(v)==2 for v in vals)
    ratios={}
    for c,case in enumerate('ABC'):
        for m,method in enumerate(['PE','PF','FD']):
            for f,field in enumerate(['u','v']):
                fixed,moving=vals[c*6+m*2+f]
                ratios[case,field,method]=moving/fixed
    ratiohtml='<div class="table-wrap"><table class="comparison"><thead><tr>'+''.join('<th scope="col">'+x+'</th>' for x in ['算例','场','PE','PF','FD'])+'</tr></thead><tbody>'
    for case in 'ABC':
        for field in ['u','v']:
            row=[ratios[case,field,m] for m in ['PE','PF','FD']]
            ratiohtml+=f'<tr><th scope="row">{case}</th><th scope="row">{field}</th>'+''.join('<td>'+('<strong>'+f'{v:.3f}'+'</strong>' if v==min(row) else f'{v:.3f}')+'</td>' for v in row)+'</tr>'
    ratiohtml+='</tbody></table></div>'
    results=(HERE/'results_revised.md').read_text(encoding='utf-8')
    results=results.replace('EXPERIMENT_SETUP',setup)
    results=results.replace('SPACE_TABLE',clean_table(tables['space_table'],['算例','场','PE','PF','FD']))
    results=results.replace('RATIO_TABLE',ratiohtml)
    results=results.replace('TIME_TABLE',clean_table(tables['time_table'],['算例','格式','场','Euler','RK4','C–N']))
    results=results.replace('MESH_TABLE',clean_table(tables['mesh_table'],['算例','格式','场','固定网格','动网格']))
    for i,label in [(1,'1'),(2,'2'),(5,'3'),(6,'4'),(3,'B1'),(4,'B2')]:
        fig=re.sub(r'图 \d+　','图 '+label+'　',figures[i-1])
        results=results.replace('FIGURE_'+str(i),fig)
    results,appendices=results.split('<!-- APPENDICES -->')
    source=source[:start]+results+'\n\n'+source[end:]
    replace('## 10　结论','## 11　结论')
    replace('固定网格上的精度排序随算例及物理场变化；在所考察的算例中，动网格均降低了两个物理场的误差。',
        '固定网格比较中，PE、PF 与 FD 的误差排序随算例和物理场变化。采用同一密度驱动的动网格后，所考察的十八组场误差均减小，误差约为固定网格结果的 0.332 至 0.838。单孤子和二孤子图进一步给出数值波形与解析等高线的对应，以及误差在空间中的分布。')
    availability='''## 数据与代码说明

本文的理论推导与数值计算材料分别收录于随稿文件 [DLW理论.ipynb](../notebook/DLW理论.ipynb) 和 [DLW数值分析report.ipynb](../notebook/DLW数值分析report.ipynb)。数值文件包含算例参数、可执行计算代码及保存的图表输出；正文和附录中的误差表使用这些既有结果。

'''
    replace('## 参考文献',availability+appendices+'\n\n## 参考文献')
    assert original_display==re.findall(r'\$\$[\s\S]*?\$\$',source), 'displayed equations changed'
    assert len(re.findall(r'<figure>',source))==6
    (HERE/'narrative_changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2),encoding='utf-8')
    (HERE/'results_reorganization.json').write_text(json.dumps({
        'displayed_equations_unchanged':True,'displayed_equations':len(original_display),
        'main_comparison_tables':2,'appendix_comparison_tables':2,
        'main_figures':[1,2,5,6],'appendix_figures':[3,4],
        'ratios_from_saved_mesh_table':{'/'.join(k):v for k,v in ratios.items()},
        'experiments_rerun':False},ensure_ascii=False,indent=2),encoding='utf-8')
    return source
