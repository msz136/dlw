"""Merge this synthesis into the existing research project records."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
progress = ROOT / 'PROGRESS_LOG.md'
text = progress.read_text(encoding='utf-8')
prefix = '> **2026-10-13（DLW 两阶段并行研究与方向评议）：**'
addition = (' **成果摘要与机制说明：** 按用户要求整理六项独立成果摘要与一份综合摘要，'
            '新增 [DLW研究摘要与误差机制](report/dlw_research_abstracts_20261013.html)，'
            '源与生成器在 `Workspaces/dlw_stage2_20261013/abstracts/`。主线明确为'
            '“结构缺陷—谱量变化—轨道与相位误差”；分别解释已证的残差到谱漂移恒等式、'
            '行波族内action偏差与相位剪切，以及尚需证明的谱量反演、族外误差控制和跨模型对应。'
            '区分半离散模型、x网格实现及时间积分，明确同h谱差守恒不等于连续—半离散误差守恒。'
            '正文含原数值证据与条件性二次相位累积界；未开展新实验，未声称普遍精度优势、'
            '一般场长期误差界或原创性确认。7份摘要、70处严格离线数学与18个本地链接核验通过。')
assert text.count(prefix) == 1
if 'report/dlw_research_abstracts_20261013.html' not in text:
    start = text.index(prefix)
    stop = text.find('\n\n', start)
    assert stop != -1
    old = text[start:stop]
    merged = prefix + addition + old[len(prefix):]
    remainder = (text[:start] + text[stop + 2:]).lstrip('\n')
    progress.write_text(merged + '\n\n' + remainder, encoding='utf-8')

index = ROOT / 'FILE_INDEX.md'
text = index.read_text(encoding='utf-8')
old = '| 合法约化、保辛与误差 Lax | M=2 行波约化、时间映射辛缺陷与误差结构桥 |'
new = '| 合法约化、保辛与误差 Lax | M=2 行波约化、时间映射辛缺陷与误差结构桥；六项成果摘要及相位误差机制 |'
if old in text:
    assert text.count(old) == 1
    index.write_text(text.replace(old, new), encoding='utf-8')
else:
    assert new in text
print('Updated the existing DLW project and progress entry.')
