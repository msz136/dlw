from pathlib import Path

hist = Path(r'C:\Users\msz\aca\Workspaces\workspace_catalog_audit_20261013\progress_history\2026-10.md')
entry = '''

## 2026-10-26｜DLW 白描写法第三稿

Abstract、§1 第 3–5 段、§5.2 末两段、§6 改为白描式叙述：只陈述构造、方程形式与各算例中谁在哪个场误差更小，去掉 complementary／strengths／trade-offs／defective／outperform 等评价词（全文检索已无这些词）。摘要补入开头背景句（DLW 为二维非线性浅水波的基本可积模型、离散化下保持可积结构的意义）与结尾综合句（双线性格点对称性与半离散守恒律如何转化为物理场精度），325 词；§1 第 1、2、6 段逐字节保留（含 [6–9]/[11]/[9,12,13]/[14]/[10] 文献句与章节安排）；§5.2 末两段改为表2/表3 的对应关系、u 排序在高斯正弦保持而在孤子翻转的机制、v 四例最小的原因；§6 压成三段，末段升至一般意义。核验：仅 abstract、1、5.2、5、6 变化；28 图 6 表；公式账目 948−45+51=954、0 渲染错误；[1]–[15] 全部被引；§6 三段 398 词；哈希 8b511834…92ad26。证据：Workspaces/dlw_paper_20261009/plain_revision_20261026/（publish/verify、manifest、validation、shot_top.png）。
'''
hist.write_text(hist.read_text(encoding='utf-8').rstrip('\n') + entry, encoding='utf-8')

cn = Path(r'C:\Users\msz\aca\Workspaces\dlw_paper_20261009\frontmatter_v2_20261026\chinese_paraphrase.md')
s = cn.read_text(encoding='utf-8')
new_abs = (
    '## 摘要（2026-10-26 白描版，对应正文 325 词）\n\n'
    '(2+1) 维色散长波（DLW）系统是二维水平非线性浅水波的基本可积模型；在离散化过程中保持其底层的可积结构，'
    '兼具理论与计算两方面的意义。本文研究 DLW 系统的可积半离散化与数值逼近，目标是理解双线性 τ 函数层面的'
    '格点安排如何塑造重构出的物理波场及其数值演化。从 Hirota–Miwa 方程与两时间 Miwa 展开出发，我们离散横向'
    '坐标 y 而保持 x 与 t 连续，导出端点型半离散化（Endpoint-SD）；再通过双线性参数的半步平移与 τ 函数的交错'
    '放置，得到中心型半离散化（Centered-SD）。两种表述都具有显式的正 Gram 行列式解、相容的 Darboux–Lax 表示'
    '与封闭的非线性物理场方程，其双线性一致性分别为一阶与二阶。我们通过单孤子、双孤子、高斯与正弦四类初值的'
    '数值实验考察所得的物理场。在空间层面，Endpoint-SD 给出最小的初始 u_t 缺陷，并在高斯与正弦算例中给出最小的 '
    'u 误差；Centered-SD 则在全部四个算例中给出最小的 v 误差，并在单孤子与双孤子情形中使 u 与 v 的误差都更小。'
    '在前向 Euler、RK4 与 Crank–Nicolson 积分下追踪全程误差历史，可以把由空间离散决定的误差增长速率与由时间'
    '积分格式引入的水平位移分离开来。最后，利用 Centered-SD 系统的半离散守恒律对一组共享的移动 x 节点作等分布，'
    '可降低两个物理分量沿波带的误差。综合起来，这些结果表明：双线性格点的对称性与半离散守恒律如何在高维可积波'
    '的数值计算中直接转化为物理场精度的提升。\n\n'
)
head, rest = s.split('## 摘要', 1)
rest = '## 摘要' + rest
i = rest.index('## 1. 引言')
rest = new_abs + rest[i:]
cn.write_text(head + rest, encoding='utf-8')
print('history chars', len(hist.read_text(encoding='utf-8')))
print('cn chars', len(cn.read_text(encoding='utf-8')))
