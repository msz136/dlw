"""Synchronize the review artifacts only after an exact-source 32-target Main pass."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
PROOFS = ROOT / 'Workspaces/lean_contracts/proofs'
DOCS = ROOT / 'Paper/dlw_semidiscrete/lean_contracts'
FROZEN = 'e70876c538d52939b030e7813a6b1c60917a79e56e28b29146d22df8da98d656'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
candidates = []
for p in sorted((PROOFS / '.lean-runs').glob('*/result.json'), reverse=True):
    r = json.loads(p.read_text(encoding='utf-8-sig'))
    if r.get('status') == 'PASSED' and Path(r.get('target', '')).name == 'Main.lean':
        candidates.append((p, r))
assert candidates
rp, run = candidates[0]
log = (rp.parent / 'build.log').read_text(encoding='utf-8-sig')
for f in run['files']:
    assert f['passed'] and f['exit_code'] == 0 and sha(Path(f['file'])) == f['sha256'], f['file']
assert sha(PROOFS/'Contracts.lean') == sha(DOCS/'Contracts.lean') == FROZEN
targets = [f'c{i:02}_proved' for i in range(1, 26)] + [f'n{i:02}_proved' for i in range(1, 8)]
for name in targets:
    m = re.search(r"'DLWContract\."+name+r"' depends on axioms: \[([^\]]*)\]", log)
    assert m, name
    assert set(x.strip() for x in m[1].split(',') if x.strip()) <= {'propext','Classical.choice','Quot.sound'}, name

rid = run['run_id']
count = len(run['files'])
builder = DOCS/'build_dashboard.py'
s = builder.read_text(encoding='utf-8')
if " 'C22':('PkgC22Complete.lean'" not in s:
    s = s.replace('PROVEN={', "PROVEN={\n 'C22':('PkgC22Complete.lean','c22_proved','将实际 Gram 插值改写为正的偶解析延拓；u 的一阶误差导数为零，h·v 的误差前三阶 jet 为零。紧性给出统一步长和导数界，分别得到一致二阶/三阶余项，再除 h，严格完成任意固定物理盒上的 u/v 二阶界。'),", 1)
s = s.replace('，其余 @@UNPROVEDCOUNT@@ 项仍未证明，逐条列出原因。', '。冻结的 32 个目标已全部完成；接口之外的研究任务另列，不计入完成率。')
s = s.replace('C22 的紧盒一致误差和 C23 的连续方程仍分别核验。', 'C22 的紧盒一致误差和 C23 的连续 Gram 方程也已完整验收。')
s = s.replace('核心分析缺口；不是一般初值收敛定理。', '已由解析延拓、奇偶性和紧集统一 Taylor 界完成；不是一般初值收敛定理。')
s = s.replace('当前端点待证明。', '本冻结端点已由所列证明包完成。')
s = s.replace('有符号计算证据；本实际函数 Lean 目标待证明。', '符号计算只作辅助；实际函数的冻结目标已由 Lean 证明。')
s = s.replace('仍未证明的 @@UNPROVEDCOUNT@@ 项保持橙色，逐条列出原因。', '32 个冻结目标均有完整证明；第 7 节列出的扩展仍未证明，不以完成率掩盖。')
builder.write_text(s, encoding='utf-8')

readme = DOCS/'README.md'
s = readme.read_text(encoding='utf-8')
s = s.replace('30 / 32', '32 / 32').replace('20260922_212234_3a4b6e8e', rid)
s = s.replace('PASSED: 25 local module(s).', f'PASSED: {count} local module(s).')
s = s.replace('**未证明 2 项**：C22、C23。', '**冻结的 32 项全部已证明**，没有剩余未证明目标。C22 完成任意固定物理盒上一致二阶极限；C23 完成连续 Gram 的两条双线性方程。')
s = s.replace('已导出无条件的 C08/C16', '已按冻结原始假设导出 C08/C16')
anchor = '整体保证的边界及剩余各项的准确缺口见'
s = s.replace(anchor, '整体保证的边界及接口外任务见')
note = '\n新增 `PkgC22Complete.lean`、`PkgC23Complete.lean`：一致二阶极限和连续 Gram 起点均已闭合。关键中间结论、对应模块和适用范围见 [C22_C23_PROOF_NOTES.md](C22_C23_PROOF_NOTES.md)。\n'
if '新增 `PkgC22Complete.lean`' not in s:
    s = s.replace('逐目标 `#print axioms`', note+'\n逐目标 `#print axioms`', 1)
readme.write_text(s, encoding='utf-8')

integration = f'''# 系统转换、数值分析与 Lean 的衔接验收

2026-09-22：**32 / 32 个冻结 Lean 目标全部完成**。C01–C25、N01–N07 均以原目标类型导出，未改冻结定义，未增加前提。

入口：[独立核验页面](../../../lean_verification.html) · [机器状态](status.json) · [关键证明结构](C22_C23_PROOF_NOTES.md) · [数值报告](../numerics/REPORT.md)。

## 完整入口证据

`Workspaces/lean_contracts/proofs/Main.lean`：退出码 0，**PASSED: {count} local module(s).**，run **{rid}**。

[result.json](../../../Workspaces/lean_contracts/proofs/.lean-runs/{rid}/result.json) · [build.log](../../../Workspaces/lean_contracts/proofs/.lean-runs/{rid}/build.log)。

全导入链当前源码 SHA-256 与通过记录逐一吻合。全部 32 个终点的公理依赖仅为 `propext / Classical.choice / Quot.sound`，没有 `sorryAx` 或新增公理。两份冻结 Contracts 的 SHA-256 均为 `{FROZEN}`。

## 系统之间已经接通的保证

| 路线 | 形式化保证 | 适用边界 |
|---|---|---|
| 连续 Gram → 连续双线性 → 连续非线性 DLW | C23、C01、C02：真实行列式、导数、对数变换及混合偏导 | 固定 PositiveData；连续物理方程为 λ=−2 |
| 连续结构 → 半离散构造 | C03–C08、C11：模板偏移、实际矩阵元、任意 N 双线性链、两壁精确方程与算子一致性 | 指定模板内构造；并非任意连续解的采样都满足有限 h 方程 |
| 半离散双线性 → 半离散非线性 | C13–C16：商恒等式、精确残差关系、前向解映射、Gram 精确解 | C14 不预设方程成立；一般反向局部重构不在本接口中 |
| 正性与连续极限 | C09、C12、C17、C18、C22、C24：无零点、速率和观测二阶、非线性一致性、实际解族紧盒一致二阶界、插值对应 | C22 常数与趋零 h 无关，允许依赖数据与固定物理盒；不是一般初值求解器收敛 |
| 其他系统性质 | C10、C19–C21、C25：相互作用系数、局部守恒身份式、周期平均约束、真实零背景线性化 | 不自动给出峰位散射、积分边界、平均模态演化或非线性稳定 |
| 数值方法基础 | N01–N07：Euler/非线性时变 RK4/梯形局部阶，以及误差、重构、增长工具 | 须另接实际离散 RHS、边界和浮点程序；不代表程序已被 Lean 全面认证 |

## 本次补齐的最后两项

- **C23**：连续 y 流通过行列式换序接入 C07，再沿合法辅助参数曲线求导，证明 Bₐ(τ₁ᵧ,τ₀)=2Dₓ。与第一式的 y 导数组合得到完整 ContinuousPair。任意 N，没有 Reservoir 或额外可逆性前提。
- **C22**：实际插值改写为正的偶解析延拓；u 的误差为一致 O(h²)，h·v 的误差为一致 O(h³)，除 h 得 v 的一致 O(h²)。紧性提供共同步长及统一导数界，保留 F 的半格位置。

具体起点、终点与中间模块见 [C22/C23 证明结构](C22_C23_PROOF_NOTES.md)。此前 N01、C18、C07/C08/C09/C16 均继续包含在完整入口中。旧条件桥 `c08_of_c07`、`c16_of_c07` 保留为辅助工具；最终终点已经接入真实证明。

## 正则性与未覆盖的研究任务

冻结接口中的 `ContDiff ℝ ⊤` 在当前 Mathlib（ℕ∞ω）表示解析阶 ω，强于普通 C∞。所有证明按冻结假设验收，没有暗中扩大适用范围。

32 项之外的一般反向局部重构、IST/谱分析、复参数、真实峰位渐近相移、积分边界与求解器浮点认证仍未证明。完整列表在独立页面第 7 节。这些任务不属于本次冻结目标完成率。

## 数值证据保持独立

四项复审修复及 E2/E3 时间自收敛已完成：[RESOLUTION.md](../../../Workspaces/numerics_review_20260922/RESOLUTION.md)、[final_validation_manifest.json](../numerics/out/final_validation_manifest.json)。此前 **40 项回归 + 17 项产物检查**通过；E2/E3 六组研究共 30 次推进，支持当前算例中 Euler/RK4/梯形的 1/4/2 阶。

E1 的固定区域二阶数值观测现在有 C22 的精确解族定理支撑。E6 是实际开链零背景线性化的浮点谱、RHS 导数和本征模核对；线性范数界不能代替非线性长期稳定。E5 的短时积分漂移是轨道诊断。N04 是以区间包含为前提的证书规则；本次没有为实验数据补出 Lean 区间包含证明，也没有验收求解器两孤子散射或非线性长期稳定。
'''
(DOCS/'INTEGRATION_STATUS.md').write_text(integration, encoding='utf-8')

agents = ROOT/'AGENTS.md'
s = agents.read_text(encoding='utf-8')
banner = f'''> **2026-09-22（最新完整验收，优先于下方历史记录）：32 / 32 个冻结 Lean 目标全部完成。** `Main.lean` → **PASSED: {count} local module(s)**，退出码 0，run `{rid}`。最后补齐 C22（实际 Gram 物理场的紧盒一致二阶极限）和 C23（任意 N 连续 Gram 双线性对）。全部终点仅依赖 `propext / Classical.choice / Quot.sound`；两个 Contracts 哈希不变，完整导入链源码哈希逐一核对。
> 独立页面 [lean_verification.html](lean_verification.html)、[衔接验收](Paper/dlw_semidiscrete/lean_contracts/INTEGRATION_STATUS.md)、[机器状态](Paper/dlw_semidiscrete/lean_contracts/status.json)、[C22/C23 关键证明](Paper/dlw_semidiscrete/lean_contracts/C22_C23_PROOF_NOTES.md) 已同步。数值部分保持此前 40 项回归 + 17 项产物检查和 E2/E3 六组自收敛的验收。**完成范围为 C01–C25、N01–N07；并不包含一般反向重构、IST、浮点求解器认证、求解器散射或非线性长期稳定。** 冻结 `ContDiff ℝ ⊤` 表示解析阶 ω，不能解释为仅 C∞。下方旧的未完成计数保留作历史记录。

'''
if banner not in s:
    first, rest = s.split('\n', 1)
    agents.write_text(first+'\n\n'+banner+rest.lstrip('\n'), encoding='utf-8')

subprocess.run([sys.executable, str(builder)], cwd=ROOT, check=True)
subprocess.run([sys.executable, str(ROOT/'Workspaces/lean_contracts/validate_dashboard.py')], cwd=ROOT, check=True)
print(json.dumps({'run_id':rid,'modules':count,'targets':len(targets),'frozen_sha256':FROZEN}, ensure_ascii=False))
