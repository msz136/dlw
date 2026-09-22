"""Publish only actually passed fixed-grid time-convergence measurements."""
from pathlib import Path
import json

root=Path(__file__).resolve().parents[2]
num=root/'Paper/dlw_semidiscrete/numerics'
data=json.loads((num/'out/e2_e3_self_convergence.json').read_text(encoding='utf-8'))
assert data['passed'] and len(data['studies'])==6
rows=[]
for r in data['studies']:
    p=r['successive_differences'][-1]['orders']
    rows.append(f"| {r['h']} | {r['method']} | {p['P']:.4f} | {p['W']:.4f} | {p['u']:.4f} | {p['v']:.4f} |")
table='\n'.join(['| h | 方法 | P 阶 | W 阶 | u 阶 | v 阶 |','|---|---|---:|---:|---:|---:|',*rows])
section='''### 补充：同网格时间自收敛已实际完成

固定 nx=256、L=60、开链 j=−12..12、T=0.05 和相同解析初态/时变边界。
每种方法分别取 n=4,8,16,32,64 步，比较相邻 n 与 2n 的最终数值解，
计算 p=log₂(‖U_n−U_2n‖∞/‖U_2n−U_4n‖∞)。不减解析解，因此没有把空间误差地板算入时间误差。
检查全部演化分量 P/W 与重构分量 u/v；30 次推进均到达目标时间且无拒绝/非有限值。
下表为最后三个网格 n=16,32,64 的观测阶，完整加密历史保留在 JSON 中。

'''+table+'''

六组都通过事先指定的末级观测阶与理论阶相差小于 0.35 的检查。
Euler 的粗步长尚处于渐近区前段，不能把末级值四舍五入后说成精确一阶。
这些结果支持当前有限维、短时间、指定数据上的 1/4/2 阶时间行为，不证明非线性长期稳定或一般初值收敛。
梯形法各步还须满足求解器残差容差；本实验使用 tol=1e-14、maxit=100。

![E2/E3 同网格时间自收敛](figures/fig4_e2_e3_time_order.png)

数据与执行源码哈希：`out/e2_e3_self_convergence.json`；完整日志：`out/e2_e3_self_convergence_log.txt`。
复现：`python -u run_all.py e2e3time`。

'''
p=num/'REPORT.md'
s=p.read_text(encoding='utf-8')
s=s.replace('Lean 未更改。','Lean 的后续证明与独立验收页面已同步，见 [系统—数值—Lean 衔接记录](../lean_contracts/INTEGRATION_STATUS.md)；数值运行本身不等于形式化认证。')
s=s.replace('E2/E3 时间自收敛属于后续实验范围。','E2/E3 自身的时间阶已由下述独立同网格实验补充验收。')
s=s.replace('仍可进一步开展 E2/E3 时间自收敛、求解器的两孤子散射、','仍可进一步开展求解器的两孤子散射、')
s=s.replace('## E4：解析两孤子相移',section+'## E4：解析两孤子相移')
s=s.replace('python -u run_all.py e1 e6 e2e3 e5 e7','python -u run_all.py e1 e6 e2e3 e2e3time e5 e7')
p.write_text(s,encoding='utf-8')
p=num/'README.md'
s=p.read_text(encoding='utf-8').replace('python -u run_all.py e1 e6 e2e3 e5 e7','python -u run_all.py e1 e6 e2e3 e2e3time e5 e7')
s=s.replace('E2/E3 自身时间阶尚未由自收敛测出；E7 四阶不可代替它。',
            'E2/E3 已新增六组同网格时间自收敛，分别支持 Euler/RK4/梯形的 1/4/2 阶行为（详见报告中的实际数值）；数据与源码哈希在 `out/e2_e3_self_convergence.json`。')
p.write_text(s,encoding='utf-8')
p=root/'Paper/dlw_semidiscrete/lean_contracts/build_dashboard.py'
s=p.read_text(encoding='utf-8').replace('40 项回归和 13 项产物检查','40 项回归和 17 项产物检查')
s=s.replace('E2/E3 自身时间自收敛、求解器两孤子散射、非线性长期稳定仍未验收。',
            'E2/E3 已补齐六组同网格时间自收敛，支持当前算例下 Euler/RK4/梯形的 1/4/2 阶；30 次推进均完成。求解器两孤子散射、非线性长期稳定仍未验收。')
p.write_text(s,encoding='utf-8')
p=root/'Paper/dlw_semidiscrete/lean_contracts/INTEGRATION_STATUS.md'
s=p.read_text(encoding='utf-8').replace('40 项回归、13 项产物检查通过','40 项回归、17 项产物检查通过')
s=s.replace('也未完成 E2/E3 自身时间自收敛、求解器两孤子散射和非线性长期稳定验收。',
            'E2/E3 已另完成六组同网格时间自收敛（30 次推进），支持当前算例的 1/4/2 阶时间行为；求解器两孤子散射和非线性长期稳定仍未验收。')
p.write_text(s,encoding='utf-8')
p=root/'AGENTS.md'
s=p.read_text(encoding='utf-8')
first,rest=s.split('\n',1)
banner='''
> **2026-09-22（数值继续实施）：E2/E3 自身时间自收敛已补齐。** 两个 h（1/4、1/8）× Euler/RK4/梯形，固定 nx=256、T=0.05、相同初态与时变边界，n=4/8/16/32/64 共 30 次推进完成。比较相邻时间网格的 P/W/u/v，六组末级观测阶通过与 1/4/2 相差小于 0.35 的验收；原先“E2/E3 自身时间阶未测出”的记录已成为历史。真实末级阶见 [数值报告](Paper/dlw_semidiscrete/numerics/REPORT.md)，不能把有限观测当作阶数定理。日志与源码哈希 `out/e2_e3_self_convergence*.{txt,json}`；复现 `python -u run_all.py e2e3time`。最终 **40 项回归 + 17 项产物检查**。求解器散射、非线性长期稳定与程序级 Lean 认证仍未完成。
'''
p.write_text(first+'\n'+banner+rest,encoding='utf-8')
print(table)
