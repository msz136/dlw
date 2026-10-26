from pathlib import Path

p = Path(r'C:\Users\msz\aca\Workspaces\dlw_paper_20261009\frontmatter_v2_20261026\chinese_paraphrase.md')
s = p.read_text(encoding='utf-8')

head, rest = s.split('## 摘要', 1)
intro_idx = rest.index('## 1. 引言')
old_abstract_block = rest[:intro_idx]
rest = rest[intro_idx:]

new_abstract = (
    '## 摘要（2026-10-26 平衡版，对应正文 283 词）\n\n'
    '本文研究 (2+1) 维色散长波（DLW）系统的可积半离散化与数值逼近，目的在于理解双线性 τ 函数层面的不同格点安排'
    '如何影响重构出的物理波场。从 Hirota–Miwa 方程与两时间 Miwa 展开出发，我们离散横向坐标 y，同时保持 x 与 t '
    '连续，在同一双线性框架内得到两种互补的半离散表述：一种是由未平移的 Miwa 约化直接得到的端点型表述'
    '（Endpoint-SD），另一种是通过半步参数平移得到的中心交错表述（Centered-SD）。对这两种表述，我们构造显式的 '
    'Gram 行列式解，给出物理场光滑所要求的正性条件，并在导出封闭非线性场方程的同时给出相容的 Darboux–Lax 对。'
    'Endpoint-SD 给出结构紧凑的直接两场系统；Centered-SD 则引入一个辅助对数差分，使两条物理方程都恢复完整的二阶'
    '一致性，并由此提供一个内禀的半离散守恒律。在单孤子、双孤子、高斯与正弦四类初值上的数值实验展示了两种格式'
    '各自的长处：Endpoint-SD 给出最小的初始 u_t 误差，并在光滑的高斯与正弦情形中对第一个场 u 达到最高精度；'
    'Centered-SD 则在全部算例中稳定地改善第二个场 v，并在非线性孤子的传播与相互作用过程中使两个分量的误差都更小。'
    '我们进一步在前向 Euler、RK4 与 Crank–Nicolson 三种时间积分下考察 Centered-SD，通过追踪全程误差历史说明：'
    '按其原生的半离散守恒密度重新分布空间节点，可以系统性地降低两个物理场沿波带的误差。\n\n'
)

rest = rest.replace('## 1. 引言', '## 1. 引言（平衡版之前的版本，待更新）', 1)
rest = rest.replace('## 6. 结论', '## 6. 结论（平衡版之前的版本，待更新）', 1)

note = ('对应 `dlw-paper.html`。摘要为 2026-10-26「表述尺度与立场平衡」版的译文；\n'
        '引言与结论的中文对应平衡版之前的文本，尚未重译。\n'
        '中文为释义，供核对英文表述之用，不是投稿用的第二语言稿。\n\n')

p.write_text(head.split('对应')[0] + note + new_abstract + rest, encoding='utf-8')
print('rewritten; chars', len(p.read_text(encoding='utf-8')))
print(p.read_text(encoding='utf-8')[:700])
