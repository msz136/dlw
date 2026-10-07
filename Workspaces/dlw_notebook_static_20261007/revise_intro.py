"""Revise the report introduction while retaining executed numerical cells."""
from pathlib import Path
import hashlib
import json
import shutil
import nbformat

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROJECT = ROOT/'Workspaces/notebook_reports_20261006'
NOTEBOOK = ROOT/'notebook/DLW数值分析report.ipynb'
BUILDER = PROJECT/'build_dlw_numerics_notebook.py'
BACKUP = HERE/'before_intro_revision'
OLD = '以 DLW 单孤子与二孤子的解析解为参照，比较 SD、SD2 与 FD，以及固定网格与动网格。SD 直接推进双线性方程，采用隐式中点；SD2、FD 比较 Euler 与 RK4。'
NEW = '以 DLW 单孤子与二孤子的解析解为参照，采用两种可积半离散方法（SD、SD2）和一种直接差分方法（FD）计算数值解，比较固定网格、动网格及不同时间算法下的误差。'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

paths = [NOTEBOOK, BUILDER, ROOT/'dlw_numerical.html', HERE/'README.md', HERE/'build_static.py',
    HERE/'build_validation.json', HERE/'content_validation.json', HERE/'browser_validation.json']
for path in paths:
    target = BACKUP/path.relative_to(ROOT)
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        shutil.copy2(path, target)
before = nbformat.read(BACKUP/NOTEBOOK.relative_to(ROOT), as_version=4)
after = nbformat.from_dict(json.loads(json.dumps(before)))
title = next(c for c in after.cells if c.id == 'dlw-title')
assert OLD in title.source
title.source = title.source.replace(OLD, NEW, 1)
exact = next(c for c in after.cells if c.id == 'dlw-exact-text')
exact.source = exact.source.replace('1.1　孤子参照', '1.1　孤子精确解', 1).replace(
    '用对数和计算正系数 tau 函数；对数的一阶、二阶导数分别是指数率的加权均值、协方差。',
    r'精确参照由 `Exact` 类按上述孤子公式计算。`tau` 用 `logsumexp` 求 τ 函数的对数及各指数项的归一化权重；`mean`、`cov` 分别计算 $\partial_x\log\tau$ 和 $\partial_x\partial_y\log\tau$，`uv` 按上式组合成 $u_*,v_*$。调用 `uv(js, x, t)`，得到各 $y_j$ 层、$x$ 点和 $t$ 时刻的精确参照值。', 1)
assert [c for c in before.cells if c.cell_type=='code'] == [c for c in after.cells if c.cell_type=='code']
assert all(a == b for a,b in zip(before.cells, after.cells) if a.id not in ('dlw-title','dlw-exact-text'))
source = BUILDER.read_text('utf-8')
assert NEW in source and exact.source in source
nbformat.validate(after)
nbformat.write(after, NOTEBOOK)
evidence = dict(success=True, date='2026-10-07', old_intro=OLD, new_intro=NEW,
    changed_cells=['dlw-title','dlw-exact-text'], all_other_cells_unchanged=True,
    exact_solution_methods=['Exact.tau','Exact.mean','Exact.cov','Exact.uv'],
    html_core_excerpt='Exact.tau through Exact.uv',
    code_cells_unchanged=True, execution_counts_and_saved_outputs_unchanged=True,
    numerical_reexecution=False,
    original_notebook_sha256=sha(BACKUP/NOTEBOOK.relative_to(ROOT)),
    notebook_sha256=sha(NOTEBOOK), builder_sha256=sha(BUILDER),
    numerical_execution_evidence='Workspaces/notebook_reports_20261006/dlw_execution_validation.json',
    numerical_execution_evidence_sha256=sha(PROJECT/'dlw_execution_validation.json'),
    code_cell_hashes={c.id:hashlib.sha256(json.dumps(c,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
                      for c in after.cells if c.cell_type=='code'},
    backup=str(BACKUP))
(HERE/'intro_revision.json').write_text(json.dumps(evidence, ensure_ascii=False, indent=2)+'\n',encoding='utf-8')
print(NEW)
