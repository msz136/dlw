from pathlib import Path
import json
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
s=json.loads((HERE/'out/summary.json').read_text(encoding='utf-8'))
assert s['scan_count']==324 and s['linear_response_count']==24 and s['readback_error']==0
addition=' **同日优势邻域与传播机制探索：** [新推导](Workspaces/dlw_advantage_regions_20260926/REPORT.md)围绕P2/P6各做a,p,q±.1的3³邻域、2网格、3方案，共324条Euler轨道；P6盒[3.9,4.1]×[.9,1.1]×[2.9,3.1]原式/共用系数两网格均27/27双场胜FD，细x最坏比原式.782/.788、共用.619/.785。P2细x则原式24/27、共用18/27，不能泛化整个盒。新增精确二次误差递推与y/x/Euler三源传播分解，24个无拟合线性预测的误差场相对偏差≤.012985%，32个SD/FD场排名全一致；P6粗x峰值的y响应由FD正叠加变为原式负抵消，定量解释收益及系数排名随分辨率变化。给出严格中心余量＋Lipschitz常数的条件邻域半径，以及初始物理误差速度的充分短时判据；P6细x原式初始比.958/.849，尚未认证具体时间阈值或全盒半径。零背景精确x/t的线性振荡模态推得原式二阶频率误差优势带−4<ξη<−2，参数族判据|C_SD|+4|cξ|sqrt(−D0)<|C_FD|；显式矩阵反例说明频率优势不等于双场优势。12符号＋8Jacobian/解析x核验通过；348个NPZ哈希与误差回读通过，评价加密≤.8485%且216个双场分类无翻转。输出两张PNG/PDF科学图、全部失败点与CSV；候选盒为采样证据，未做区间认证、长期或统计声明。'
p=ROOT/'PROGRESS_LOG.md';t=p.read_text(encoding='utf-8')
if '**同日优势邻域与传播机制探索：**' not in t:
    start=t.index('> **2026-09-26（双线性→非线性与 Miura 转化复梳）');end=t.index('\n\n',start)
    p.write_text(t[:end]+addition+t[end:],encoding='utf-8')
p=ROOT/'FILE_INDEX.md';t=p.read_text(encoding='utf-8')
needle='- `Workspaces/dlw_coefficient_euler_20260926/out/`（三份冻结JSON、481条物理场NPZ、errors.csv、summary.json、tables.md），`pilot_v1/`（4条先导与当时源码）'
entries='''
- [DLW 优势邻域与误差传播](Workspaces/dlw_advantage_regions_20260926/REPORT.md)（P2/P6参数盒、精确误差递推、三源传播、条件邻域半径与线性振荡频带定理）
- `Workspaces/dlw_advantage_regions_20260926/derive.py`、`symbolic.json`（12个色散/系数符号恒等式）；`error_model.py`、`validate.py`、`validation.json`（精确Jacobian、二次余项、解析x导数，8项检查）
- `Workspaces/dlw_advantage_regions_20260926/scan.py`、`propagate.py`、`initial_defect.py`（324邻域轨道、24无拟合误差预测与初始误差速度判据）
- `Workspaces/dlw_advantage_regions_20260926/out/`（冻结计划、348个场NPZ、neighborhood_ratios.csv、预测分量、全部失败点/分类与哈希审计）
- `Workspaces/dlw_advantage_regions_20260926/summarize.py`、`plot.py`、`make_report.py`、`finish_docs.py`（数据审计/科学图/报告/索引生成）；`dispersion_advantage.png/pdf`、`p6_error_sources.png/pdf`（频率判据和误差抵消图）'''
if 'DLW 优势邻域与误差传播' not in t:
    assert needle in t;t=t.replace(needle,needle+entries,1);p.write_text(t,encoding='utf-8')
print('Progress and index merged into existing DLW topic')
