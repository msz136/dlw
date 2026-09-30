from pathlib import Path

root = Path(__file__).resolve().parents[2]
index = root / 'FILE_INDEX.md'
text = index.read_text(encoding='utf-8')
if 'Workspaces/adaptive_mesh_research/RECOMMENDATIONS.md' not in text:
    pos = text.index('\n') + 1
    entry = '''
**2HS / DLW 自适应网格守恒密度调研（2026-09-25）：**

- `Workspaces/adaptive_mesh_research/RECOMMENDATIONS.md`（多种守恒密度/监测量、推导、选型理由与时间算法比较计划）
- `Workspaces/adaptive_mesh_research/verify_identities.py`（九条局部守恒恒等式的符号核对）
- `Workspaces/adaptive_mesh_research/identity_checks.json`（九条残差为零；不含演化实验）
- `Workspaces/adaptive_mesh_research/update_research_index.py`（将本轮成果合并到进度与索引）
'''
    text = text[:pos] + entry + text[pos:]
    index.write_text(text, encoding='utf-8')
elif 'Workspaces/adaptive_mesh_research/update_research_index.py' not in text:
    pos = text.index('\n', text.index('Workspaces/adaptive_mesh_research/identity_checks.json'))
    text = text[:pos] + '\n- `Workspaces/adaptive_mesh_research/update_research_index.py`（将本轮成果合并到进度与索引）' + text[pos:]
    index.write_text(text, encoding='utf-8')

log = root / 'PROGRESS_LOG.md'
text = log.read_text(encoding='utf-8')
entry = '> **同专题 2026-09-25（扩展至 2HS / DLW 守恒密度选型）：** [调研建议](Workspaces/adaptive_mesh_research/RECOMMENDATIONS.md)核对 GSG §2/§4，区分原文五格式与后续 RK1/2/4/8 扩展。2HS 列出原质量、常数混合、被动标签加权、带符号能量及双场梯度/曲率监测；DLW 推导连续 r₀=1−v/4、r±=1−(v±uᵧ)/4 与通量，优先现有有限 h 的 r₋=1−(v−δ₀u)/4 共同 x 网格，并说明正性、固定横向权重、二维变换与边界限制。九条局部守恒恒等式经 SymPy 核对残差均为零（identity_checks.json）；新增公式未作 Lean 证明，未跑新的时间演化。已有误差收益仅引用此前报告，不宣称当前所有候选已实现或已保持可积结构。\n\n'
if '同专题 2026-09-25（扩展至 2HS / DLW 守恒密度选型）' not in text:
    marker = '> **2026-09-24（双线性→非线性与 Miura 转化复梳）：**'
    assert marker in text
    text = text.replace(marker, entry + marker, 1)
    log.write_text(text, encoding='utf-8')
text = index.read_text(encoding='utf-8')
if 'Workspaces/adaptive_mesh_research/EXPERIMENT_PROTOCOL.md' not in text:
    pos = text.index('\n', text.index('Workspaces/adaptive_mesh_research/RECOMMENDATIONS.md'))
    entry = '\n- `Workspaces/adaptive_mesh_research/EXPERIMENT_PROTOCOL.md`（v1 实验协议：密度/控制器分离、六阶段对照、确认集与胜负规则）\n- `Workspaces/adaptive_mesh_research/build_experiment_matrix.py`（仅生成计划矩阵，不运行求解器）\n- `Workspaces/adaptive_mesh_research/planned_matrix.json`（456 条计划记录，实际新演化为零，待 E0 与调参）'
    index.write_text(text[:pos]+entry+text[pos:],encoding='utf-8')
text = log.read_text(encoding='utf-8')
if 'EXPERIMENT_PROTOCOL.md' not in text:
    marker = '同专题 2026-09-25（扩展至 2HS / DLW 守恒密度选型）'
    pos = text.index('\n', text.index(marker))
    entry = ' **同日实验设计扩展：** [v1 实验协议](Workspaces/adaptive_mesh_research/EXPERIMENT_PROTOCOL.md)分离密度主效应与原生守恒控制器，规定 E0–E5、共同物理双场误差、失败计数、同精度成本、开发/确认分离及操作性筛选门槛。计划矩阵含 E2 180、dt 控制 60、E3 216，共 456 条且全部 planned；生成器验证唯一 ID 和计数通过，尚未运行新 PDE 演化，尚需统一 HS 重分布/ALE、候选接口、边界和参照控制。最终确认集未生成/未使用，未宣称已选出赢家。'
    log.write_text(text[:pos]+entry+text[pos:],encoding='utf-8')
print('Research index and existing progress topic updated.')
