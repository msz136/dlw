from pathlib import Path
import re,json

HERE=Path(__file__).resolve().parent

def revise(s):
    original=s
    def rep(a,b):
        nonlocal s
        assert s.count(a)==1,(a[:80],s.count(a))
        s=s.replace(a,b,1)
    rep('通过格点差分消去该势，得到 PE 形式；引入势变量 $Q,R,M$ 表示该势，得到 PF 形式。',
        '通过格点差分消去该势，得到差分消势形式（potential-elimination formulation，PE）；引入势变量 $Q,R,M$ 表示该势，得到势函数形式（potential formulation，PF）。')
    a=s.index('**命题 1.1');b=s.index('## 2　',a)
    s=s[:a]+'上述因变量变换及连续双线性表示采用 Sheng 和 Yu [1，第 2 节，式 (5)—(7)] 的结果。在 τ 函数严格为正的区域内，满足（3）的 $f,g$ 通过（2）给出连续 DLW 系统（1）的解。\n\n'+s[b:]
    s=s.replace('再由命题 1.1，得到','再由文献 [1] 的双线性变换，得到')
    rep('因此，将 $f$ 放在两个相邻 $g$ 格点的中间','将 $f$ 放在两个相邻 $g$ 格点的中间')
    a=s.index('为考察式（5）的连续极限');b=s.index('**命题 2.1',a)
    definitions=s[a:b].replace('为考察式（5）的连续极限，在固定坐标 $y$ 处记','在固定坐标 $y$ 处记').strip()
    s=s[:a]+s[b:]
    rep('**命题 2.1（双线性二阶一致性）。** 设 $f,g$ 在紧集 $K$ 的某个开邻域内实解析。对充分小的 $h>0$，有',
        '**命题 2.1（双线性二阶一致性）。** 设 $f,g$ 在紧集 $K$ 的某个开邻域内实解析。'+definitions+'\n\n则对充分小的 $h>0$，有')
    # Merge construction and verification. State the determinant inside its theorem.
    a=s.index('## 3　');b=s.index('## 4　',a);c=s.index('## 5　',b)
    construct=s[a:b];verify=s[b:c]
    defs=construct[construct.index('设 $N'):].strip().replace('设 $N\\ge1$ 为整数，', '设 $h>0$，$N\\ge1$ 为整数，', 1)
    lemma=verify[verify.index('**引理 4.1'):verify.index('**定理 4.2')]
    proof=verify[verify.index('**证明。**',verify.index('**定理 4.2')):]
    merged='''## 3　Gram 行列式解及其双线性恒等式

本节给出半离散系统的 Gram 行列式解，并证明所定义的 τ 函数满足式（5）。这一结论将行列式构造与半离散方程联系起来，为后续物理场重构和精确解的连续极限提供依据。

**定理 4.2（任意有限阶 Gram 精确解）。** '''+defs+'''

则由（8）、（9）定义的 $F_j,G_j$ 对所有 $x,t\\in\\mathbb R$ 和 $j\\in\\mathbb Z$ 满足半离散双线性系统（5）。

以下相邻辅助层恒等式用于验证上述 τ 函数满足的双线性关系。

'''+lemma+proof.replace('**证明。**','**定理 4.2 的证明。**',1)
    s=s[:a]+merged+s[c:]
    a=s.index('### 5.1　解的正则性');b=s.index('### 5.2　PE 形式的推导',a)
    regular=s[a:b].replace('### 5.1　解的正则性','### 3.1　正则谱参数')
    s=s[:a]+s[b:]
    a=s.index('## 5　');b=s.index('### 5.2　',a)
    s=s[:a]+regular+'## 5　差分消势形式（PE）\n\n差分消势形式（potential-elimination formulation，PE）通过格点差分消去辅助势，得到物理场的闭合半离散系统。以下由双线性方程的和与差导出这一表示；对同一辅助势的势函数处理见第 6 节。\n\n'+s[b:]
    a=s.index('### 5.2　PE 形式的推导');b=s.index('记格点差分和平均算子为',a)
    s=s[:a]+s[b:]
    rep('## 6　PF 形式','## 6　势函数形式（PF）')
    rep('PF 路线保留式（26）中的辅助势，以整数格点上的势函数表示它。',
        '势函数形式（potential formulation，PF）保留式（26）中的辅助势，以整数格点上的势函数表示它。')
    rep('连续极限需要处理三个相互衔接的问题。首先，将光滑物理场代入半离散方程，比较其残差与连续 DLW 方程；其次，检验交错 τ 重构是否保持物理变量的二阶精度；最后，对随 $h$ 变化的精确 Gram 解族证明同样的二阶收敛。前两步给出局部展开，第三步将展开用于实际解族。所有估计均在固定紧集上进行。',
        '本节建立半离散系统与连续 DLW 系统在 $h\\to0$ 时的对应关系：半离散方程以二阶精度恢复连续方程，交错重构趋于连续物理变量，固定谱参数的精确 Gram 解族也以 $O(h^2)$ 收敛到连续解。以下估计均在固定紧集上成立。')
    rep('第一条非线性方程含后向差分，其自然评价点位于相邻物理层的中间；第二条方程含中心差分，评价点仍位于物理层。分别围绕这两个位置展开，可保留交错离散的对称性。',
        '本小节证明 PE 系统在 $h\\to0$ 时恢复连续 DLW 方程。具体地，在各自的空间评价点上，半离散方程与连续方程的左端相差 $O(h^2)$；当物理场满足连续方程时，其格点采样代入半离散方程所得残差也为 $O(h^2)$。')
    rep('方程的一致性之外，还需检查变量变换本身。这里先固定一对连续 τ 函数，只考察半格点平均和中心差商引入的误差。这一结果将在下一节用于随格距变化的 τ 解族。',
        '本小节证明交错格点上的物理变量定义与连续变换（2）具有相同极限，并给出两者之间的二阶误差估计。')
    a=s.index('对于连续正 τ 函数 $f,g$');b=s.index('**命题 7.2',a)
    defs=s[a:b].replace('对于连续正 τ 函数 $f,g$，在物理位置 $y$ 定义交错重构','在物理位置 $y$ 定义交错重构').strip()
    s=s[:a]+s[b:]
    rep('**命题 7.2（重构的二阶精度）。** 设 $f,g$ 在紧集 $K$ 的某个开邻域内严格为正且实解析。则',
        '**命题 7.2（重构的二阶精度）。** 设 $f,g$ 在紧集 $K$ 的某个开邻域内严格为正且实解析。'+defs+'\n\n则')
    rep('精确半离散 τ 函数的格点相位和振幅均依赖 $h$。因此，需要先在同一连续坐标下比较离散与连续行列式，再将估计传递给物理场。下面固定谱数据，通过正实指数插值把格点解延伸到连续 $y$ 坐标。',
        '本小节建立精确解之间的连续极限：在固定谱参数下，半离散 Gram 解恢复的 $u^{(h)},v^{(h)}$ 一致趋于连续 Gram 解的物理场，误差为 $O(h^2)$。定理同时给出作为极限的连续行列式表达。')
    a=s.index('固定 $N$ 及谱参数，设存在');b=s.index('**定理 7.3',a)
    defs=s[a:b].strip();s=s[:a]+s[b:]
    rep('**定理 7.3（精确 Gram 解族的一致二阶极限）。** 在上述固定谱参数条件下，',
        '**定理 7.3（精确 Gram 解族的一致二阶极限）。** '+defs+'\n\n在上述条件下，')
    rep('本节给出连接格点移位与时间演化的辅助线性问题，并检验两种操作的相容性。先在 PE 变量中构造一阶格点关系和二阶时间方程，再通过第 6 节的变量变换得到 PF 表示。证明的关键是将相容条件化为两项标量残差，其和与差分别对应非线性演化关系。',
        '为刻画半离散系统的可积结构，本节给出 PE 与 PF 两种形式的 Lax 表示。其相容条件恢复相应的非线性演化关系，从而将所构造的半离散方程与辅助线性系统联系起来。')
    rep('格点关系描述辅助函数从 $j$ 到 $j+1$ 的变化，时间方程规定每一层的演化。要求先移位后演化与先演化后移位给出相同结果，便得到相容条件。取辅助函数', '取辅助函数')
    rep('前述构造给出了沿 $y$ 方向离散、在 $x,t$ 方向连续的非线性系统。数值计算以 PE 的 $P,W$ 或 PF 的 $Q,R$ 为演化变量，通过相应重构得到 $u,v$。本节依次说明空间差分、网格运动和时间推进，并给出连续 DLW 方程的直接差分格式（FD）作为比较对象。三种格式均以连续解析解确定初始物理场与边界数据。',
        '前述构造给出了沿 $y$ 方向离散、在 $x,t$ 方向连续的非线性系统。本节将两种非线性表示用于数值计算：PE 推进 $P,W$，PF 推进 $Q,R$，再分别恢复物理场 $u,v$。连续 DLW 方程的直接差分方法（FD）作为比较对象，三种方法均以连续解析解确定初始物理场与边界数据。\n\n计算采用三点中心差分处理 $x$ 导数，并分别在固定网格与守恒密度驱动的动网格上推进。时间方向采用 Euler、RK4 和 Crank–Nicolson（C–N）算法。下文先给出各空间离散方法的演化变量及更新关系，再说明网格运动和时间积分；数值结果分别比较空间离散方法、时间算法与网格选择对误差的影响。')
    rep('$y$ 方向的 $\\delta_-,\\delta_0,M_-$ 仍表示第 5 节定义的差分与平均。',r'''沿 $y$ 方向采用后向差分、中心差分及相邻层平均：

$$\delta_-z_{j,i}=\frac{z_{j,i}-z_{j-1,i}}h,\qquad
\delta_0z_{j,i}=\frac{z_{j+1,i}-z_{j-1,i}}{2h},\qquad
M_-z_{j,i}=\frac{z_{j,i}+z_{j-1,i}}2.$$

这些算子仅作用于层编号 $j$；$D_1,D_2$ 作用于 $x$ 节点编号 $i$。''')
    rep('$u^n$ 仍由（58）的第一式恢复，随后计算',r'''由下侧边界恢复 $u^n$：

$$u_{j,i}^n=u_{j_L,i}^n+h\sum_{k=j_L+1}^{j}P_{k,i}^n.$$

其中 $u_{j_L,i}^n$ 为解析边界值。随后计算''')
    rep('对于本文的 DLW 系统，网格运动由 PE 方程中的守恒关系确定。令',
        '对于本文的 DLW 系统，选取 $\\rho_j=1-W_j/4$ 为驱动网格运动的守恒密度。这一选择将场变量的演化与节点分配联系起来；在 PF 中，同一密度为 $Q_jR_j$。相应的密度与通量为')
    rep('例如，FD 格式中的 $v$ 方程写为','FD 格式中的 $v$ 方程写为')
    rep('数值比较围绕两个问题展开：PE、PF 与直接差分格式在同一网格上的误差有何差异，以及移动网格能带来多大的精度改善。先固定时间算法比较三种空间格式，再考察节点运动的影响。随后以 PF 的单孤子和二孤子结果展示波形及误差的空间分布。',
        '本节比较空间离散方法、时间积分算法和网格选择对计算误差的影响。首先在固定网格上比较 PE、PF 与 FD，随后比较 Euler、RK4 和 C–N 三种时间算法，再考察动网格带来的误差变化。最后以 PF 的单孤子和二孤子结果展示波形及误差的空间分布。')
    rep('表 1 分别列出两个物理场的误差；将 $u,v$ 分开，是因为三种格式对两个场的重构方式不同，精度排序也可能不同。','表 1 列出三种方法的 $u,v$ 误差。')
    # Return the full time comparison to the main results, with its interpretation.
    a=s.index('时间算法的完整比较见附录表 A1。');b=s.index('### 10.3',a)
    commentary=s[a:b].replace('时间算法的完整比较见附录表 A1。','').strip()
    s=s[:a]+s[b:]
    a=s.index('### A.1　时间算法');b=s.index('### A.2',a)
    block=s[a:b];table=re.search(r'<div class="table-wrap">[\s\S]*?</div>',block)[0]
    s=s[:a]+s[b:]
    section='''### 10.3　时间算法比较

在相同的固定网格、时间步长和终止时刻下，分别采用 Euler、RK4 和 C–N 推进三种空间离散方法。表 2 给出各算法在两个物理场上的最大绝对误差。

**表 2　固定网格上不同时间算法的最大绝对误差。每行最小值加粗。**

'''+table+'\n\n'+commentary+'\n\n'
    # Shift result subsection and table numbering without touching equations.
    for old,new in [('### 10.5','### 10.6'),('### 10.4','### 10.5'),('### 10.3','### 10.4')]:s=s.replace(old,new)
    s=s.replace('第 10.4 节','第 10.5 节')
    s=s.replace('表 2','表 3').replace('表 1、2','表 1、3')
    s=s.replace('### 10.4　动网格',section+'### 10.4　动网格',1)
    s=s.replace('## 附录 A　完整误差比较','## 附录 A　固定网格与动网格的原始误差')
    s=s.replace('### A.2　固定网格与动网格\n\n','').replace('表 A2','表 A1')
    s=s.replace('第 10.3 节误差比','第 10.4 节误差比')
    # Common terminology: formulations remain "形式"; discretizations are methods.
    s=s.replace('格式','方法')
    # Renumber theorem references after merging sections and moving regularity.
    names={'4.2':'3.1','4.1':'3.2','5.1':'3.3','5.2':'4.1','6.1':'5.1','7.1':'6.1','7.2':'6.2','7.3':'6.3','8.1':'7.1'}
    s=re.sub(r'(命题|定理|引理) (\d+\.\d+)',lambda m:m[1]+' '+names.get(m[2],m[2]),s)
    # Old sections 5..11 shift one number after the merger. 3.1 regularity stays.
    s=re.sub(r'^(#{2,3}) (\d+)([.　])',lambda m:m[1]+' '+str(int(m[2])-1 if int(m[2])>=5 else int(m[2]))+m[3],s,flags=re.M)
    s=re.sub(r'第 (\d+)(\.\d+)? 节',lambda m:'第 '+str(int(m[1])-1 if int(m[1])>=5 else int(m[1]))+(m[2] or '')+' 节',s)
    a=s.index('本文的安排如下。');b=s.index('\n\n',a)
    s=s[:a]+'''本文的安排如下。第 1、2 节介绍连续双线性表示及其半离散化。第 3 节给出 Gram 行列式解、双线性恒等式及正则谱参数。第 4、5 节分别推导差分消势形式（PE）和势函数形式（PF），第 6 节建立连续极限，第 7 节给出 Lax 表示。第 8 节介绍数值方法，第 9 节比较空间离散方法、时间算法与固定／动网格结果，并展示孤子波形。第 10 节给出结论。附录收录网格比较的原始误差和补充算例图。'''+s[b:]
    assert '命题 1.1' not in s
    assert len(re.findall(r'\\tag\{',s))==74
    # All numbered equations and all numeric tables remain intact (only moved).
    def numbered(t):return {re.search(r'\\tag\{(\d+)\}',f)[1]:f for f in re.findall(r'\$\$[\s\S]*?\$\$',t) if '\\tag{' in f}
    assert numbered(original)==numbered(s)
    (HERE/'structure_revision_validation.json').write_text(json.dumps({'numbered_equations_unchanged':74,'continuous_bilinear_proof_replaced_by_reference':True,'gram_sections_merged':True,'parallel_PE_PF_sections':[4,5],'time_comparison_in_main_text':'9.3','experiments_rerun':False},ensure_ascii=False,indent=2),encoding='utf-8')
    return s

