from pathlib import Path

p = Path(r'C:\Users\msz\aca\Workspaces\workspace_catalog_audit_20261013\progress_history\2026-10.md')
entry = '''

## 2026-10-26｜DLW 表述尺度与立场平衡改写

按用户提供的平衡版文本替换四处：Abstract（283 词）、§1 Introduction（6 段）、§5.2 末两段、§6 Conclusions（4 段）。叙事由"Endpoint-SD 有缺陷"改为"同源互补"：Endpoint-SD 直接紧凑、无需辅助变量、初始 u_t 缺陷四例最小、Gaussian/正弦的 u 场最准；Centered-SD 以对称交错恢复两方程二阶一致、v 场四例全胜、孤子演化中 u 亦更准。结论压缩为三点直观认识（空间安排、时间积分与误差历史、守恒密度引导网格），删除对 4.4/5.5、线性化稳定性与受扰初值的全部提及。引用再对齐：§1 第 1 段补 [1–4]，Sheng–Yu 记 [5]，Miwa 展开记 [15]（原文 [2,15] 中 [2] 为 Wang–Zhou–Li，与 Miwa 无关），第 2 段 [6–9]/[11]/[9,12,13]/[14]/[10] 原样保留，[1]–[15] 全部仍被引。核验：仅 abstract、1、5.2、5、6 变化；28 图 6 表；公式账目 974−75+49=948、渲染 0 错误；全文无 degrades/defective/contaminated/fragile 等措辞；哈希 1d84f50a…e711cb。证据：Workspaces/dlw_paper_20261009/balance_revision_20261026/（publish/verify、manifest、validation、shot_top.png）。
'''
p.write_text(p.read_text(encoding='utf-8').rstrip('\n') + entry, encoding='utf-8')
print('history chars:', len(p.read_text(encoding='utf-8')))
print('progress log chars:', len(Path(r'C:\Users\msz\aca\PROGRESS_LOG.md').read_text(encoding='utf-8')))
