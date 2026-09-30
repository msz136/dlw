"""Build a small Markdown handoff and compact, wide CSVs. No HTML writes."""
import csv
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
OUT=HERE/'out'

def main():
    s=json.loads((OUT/'summary.json').read_text())
    for name in ('html_cells','expanded_cells'):
        with (OUT/f'{name}.csv').open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
        groups={}
        for r in rows:
            cols=('section','table','p','t','method','N','dt','evaluation_points')
            key=tuple(r[k] for k in cols)
            group=groups.setdefault(key,{**{k:r[k] for k in cols},**{f'S{i}':'—' for i in range(1,7)}})
            group[r['scheme']]=r['display']
        with (OUT/f'{name}_wide.csv').open('w',encoding='utf-8-sig',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(next(iter(groups.values()))));w.writeheader();w.writerows(groups.values())
    failures=s['html_rounding_checks']-s['html_rounding_passes']
    report=f'''# 2HS 表格数据交接 · 2026-09-27

**完成范围：S5/S6 已补齐；S1–S4 尚未定义对应离散系统，不能填数。因此没有完成用户要求的全部六组合。未制作或修改 HTML。**

## 数据与对应关系

- `out/html_cells.csv`：逐格对应当前根页面 §2.1/§2.2 的 8 张表，408 个双场单元格；136 格有数值，272 格为 `model_not_constructed`。`table` 使用 BeautifulSoup 全页 table 的 **0 起始序号**（5–8、11–14），同时提供 section/p/t/method/方案，避免只靠序号定位。
- `out/expanded_cells.csv`：扩展到整数 **p=3,…,22，共20个参数**，四时间算法、两时刻、两套分辨率；640 个有效双场数值单元格。当前页面原表是13个p，并非22个。所有 S1–S4 仍留空。
- 对应 `*_wide.csv`：一行一个 p/时间/方法/配置，S1–S6 为列，S5/S6 格内为 **u误差 / rho误差**；可直接供表格生成 Agent 使用。
- `out/time_half_cells.csv`：p=5、12、22 的减半步长对照（96个双场单元格）。
- `out/results.json`、`out/all_errors.csv`：完整精度、8001/16001/32001 评价、轨道路径与哈希；`out/plan.json` 保存配置、HTML和求解器/来源哈希。轨道有新生成与引用既有文件两种，不应只复制本目录后假定所有旧轨道仍可访问。

## 固定口径

| 用途 | N（区间数） | dt | 输出时刻 | 填表评价点 |
|---|---:|---:|---|---:|
| §2.1及其四方法扩展 | 400 | .003125 | .25、.5 | 16001 |
| §2.2及其20参数扩展 | 200 | .0125 | .25、.5 | 8001 |

每套均含 Euler、Heun、RK4、固定步长12级DOP853八阶主公式。S5=`difference_rm`，S6=`difference_fixed`。固定 c=1、同一连续单孤子初值，物理计算区间[-4,4]，解析边界；m初值为离散二阶导数 u 加2。S5初始按Rm等分，之后场和内部节点每个时间级耦合推进，两端固定；S6始终均匀固定。误差为线性重构后在共同物理区间[-2,2]的采样最大绝对误差，包含空间、时间、重构误差，不是严格连续上确界或单独时间误差。rho仍是物理未知量，不作为选点候选。

## 本次核对

- {s['runs']} 条演化配置全部成功：{s['new_runs']} 条新算，{s['reused_runs']} 条按参数/求解器哈希匹配复用。320条主配置，48条减半步长控制；每条输出两个目标时刻。
- 所有保存场重新读回，用单调反演连续解析解重新计量；检查有限值、节点单调、网格/密度正性及轨道哈希。复用有原轨道哈希时逐项核对；早期没有哈希的文件本次建立哈希，并追溯来源JSON。
- 页面已有272个单场显示值中，{s['html_rounding_passes']}/{s['html_rounding_checks']} 在原显示精度内一致；差异数 {failures}，详见 `html_rounding_checks.csv`。
- 16001→32001评价加密，全部配置最大相对误差变化 {100*s['max_relative_eval16001_to32001']:.3f}%。注意这不保证8001点评价同样精确，填表仍保留原页面口径。
- 代表参数减半步长后，S5/S6的单场优劣有 {len(s['time_half_ranking_flips'])} 次翻转（明细在summary.json）。不把同一轨道的多时刻/多算法结果称作独立统计样本，也不据此宣布普适排名。

## S1–S4：交接时必须保留的限制

原可积系统要求 d_dot=-Delta u，几何恒等式要求 d_dot=Delta V；所以保持原式只能取 V=-u+b(t)。Rm速度和固定速度一般均不满足。这不是缺一个运行开关，而是缺四个新系统的方程及可积性论证。旧原生质量网格上的原/校准可积结果不能填进这些格子，插值也不能替代新网格上的演化。详见短推导 `MODEL_GAP.md`。本次没有假造新的可积系统或将失败/未定义项写成零。

复现：在工作区根目录运行 `python Workspaces/hs_table_data_20260927/run_tables.py`，再运行同目录 `make_handoff.py`。实验驱动可续跑，旧求解器与旧结果未改动。
'''
    (HERE/'HANDOFF.md').write_text(report,encoding='utf-8')

if __name__=='__main__':main()
