"""Update human-readable indexes from the checked dashboard manifest."""
from pathlib import Path
import json

root=Path(__file__).resolve().parents[2]
here=root/'Paper/dlw_semidiscrete/lean_contracts'
status=json.loads((here/'status.json').read_text(encoding='utf-8'))
assert status['proved_count']==25 and status['typecheck']['source_hashes_verified']
run=status['typecheck']['run_id']
p=here/'README.md'
s=p.read_text(encoding='utf-8')
s=s.replace('用户要求本轮只定义关键起点/终点与派工验收，不实现中间证明。',
            '用户已授权在原冻结接口基础上继续实现证明，并整合数值分析与系统转换。')
s=s.replace('- 本轮未运行数值求解器。',
            '- 数值四项复审修复已运行验收；见 `../numerics/REPORT.md`。形式化证据与数值证据分开记录。')
s=s.replace('## 进度更新（2026-09-22 第三段：23 / 32）','## 当前进度（2026-09-22：25 / 32）')
s=s.replace('**已证明 23 / 32**','**已证明 25 / 32**')
s=s.replace('→ PASSED: 11 local module(s).   退出码 0   (run 20260922_123007_8274bbe0)',
            f'→ PASSED: 15 local module(s).   退出码 0   (run {run})')
s=s.replace('**未证明 8 项**：C07、C08、C09、C16、C17、C18、C22、C23；另有',
            '**未证明 7 项（含 N01）**：C07、C08、C16、C18、C22、C23、N01；其中')
anchor='逐目标 `#print axioms`'
add='''新增已验收包：

| 包 | 目标 | 说明 |
|---|---|---|
| `PkgC17.lean` | C17 | 真实采样恒等式与物理观测点态二阶一致性 |
| `PkgC09Complete.lean` | C09 | 任意 N Gram 的正性、合法性、联合光滑性 |
| `PkgGramBridges.lean` / `Main.lean` | 条件桥 | `C07 → C08`、`C07 → C16` 已证明；不计作 C08/C16 已完成 |
| `PkgRK4.lean` | N01 辅助 | 乘积 jet、复合导数、线性 RHS 精确 RK4 多项式；一般非线性阶条件仍未闭合 |

整体保证的边界及剩余各项的准确缺口见 [INTEGRATION_STATUS.md](INTEGRATION_STATUS.md)。
页面构建器会核对成功整合运行的全依赖源码哈希、目标类型和公理输出，拒绝用旧日志为已修改源码显示绿灯。

'''
assert anchor in s
s=s.replace(anchor,add+anchor,1)
p.write_text(s,encoding='utf-8')
p=root/'AGENTS.md'
s=p.read_text(encoding='utf-8')
banner=f'''\n> **2026-09-22（Lean 继续实施，优先于下方旧完成数）：25 / 32 个冻结目标已证明。** 标准入口整合 `Main.lean` → **PASSED: 15 local module(s)**，退出码 0，run `{run}`。新增 `PkgC09Complete.lean` 完成任意 N Gram 正性/合法性/光滑性 C09；`PkgGramBridges.lean` 与 Main 完成 `C07 → C08`、`C07 → C16` 条件桥，**不把条件桥算作 C08/C16 无条件证明**。`PkgRK4.lean` 完成积函数 jet、复合导数和线性 RHS 的精确四次 RK4 多项式；一般非线性 RK4 的 N01 仍未完成。全部已验收目标只依赖三个标准逻辑公理，冻结 Contracts 哈希不变。\n> **仍未证明 7 项**：C07、C08、C16、C18、C22、C23、N01（Euler/梯形已过）。C22 的紧盒一致估计可以独立推进，不应一概归因于 C07；有限有理样例不证明任意 N。独立页面 [lean_verification.html](lean_verification.html)、[衔接验收记录](Paper/dlw_semidiscrete/lean_contracts/INTEGRATION_STATUS.md)、[机器状态](Paper/dlw_semidiscrete/lean_contracts/status.json) 已同步。页面构建已加入真实成功运行、导入闭包哈希、目标声明和公理输出核对。**尚不能承诺整套推导或数值程序已全部形式化认证。**\n'''
first,rest=s.split('\n',1)
p.write_text(first+'\n'+banner+rest,encoding='utf-8')
print('Indexes synchronized to',run)
