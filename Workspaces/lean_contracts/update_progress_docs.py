"""Synchronize the continued proof work without changing frozen contracts."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
p = ROOT/'Paper/dlw_semidiscrete/lean_contracts/build_dashboard.py'
s = p.read_text(encoding='utf-8')
replacements = {
    '<b>命题为真</b>，缺的是形式化机器而非数学事实。':
    '这些有限参数样例通过精确检查，<b>不构成任意 N 命题的证明</b>；任意 N 的行列式恒等式仍待形式化。',
    '数学报告已有证明，未找到完整 Lean 端点。':
    'PkgC09Complete.lean 已完成完整 Lean 端点；原 PkgC09.lean 草稿保留但不导入。',
    '完整 Lean 端点未找到。': '已由 PkgLattice.lean 的 c19_proved 完成。',
    '本轮新接口另有“类型检查尚未完成”的状态，不会显示成绿色。':
    '32 个接口均已类型检查；有目标定义不等于有目标证明。',
    'PASSED: 12 local module(s).': 'PASSED: @@MODULECOUNT@@ local module(s).',
    '一次性导入 Contracts、PkgTrivial、PkgGramEntry、PkgQuotientRate、PkgContinuous、PkgLattice、PkgNumeric 并逐个':
    '一次性导入全部已验收证明包，并逐个',
    '本轮没有数值运行记录、区间证书或求解器实现，因此实验状态全部保留“未验收”。Lean 证明不会凭空证明尚未运行的实验达标。':
    '数值实现与实验已运行，四项复审修正已有 <b>40 项回归和 13 项产物检查</b>。'
    '见 <a href="Paper/dlw_semidiscrete/numerics/REPORT.md">数值结果报告</a>、'
    '<a href="Workspaces/numerics_review_20260922/RESOLUTION.md">修复验收</a>及 '
    '<a href="Paper/dlw_semidiscrete/numerics/out/final_validation_manifest.json">运行证据与哈希</a>。'
    'E6 已改用实际开链线性化，检验 RHS 导数、本征模增长和形状；E1 固定窗口与端点权重已修；'
    'E5 格点和初始时刻已修；E7 实时执行当前代码得接近四阶。'
    '<b>这些是数值验收，不是 N04 区间证书，也不是全部求解器已被 Lean 认证。</b>'
    'E2/E3 自身时间自收敛、求解器两孤子散射、非线性长期稳定仍未验收。',
}
for old,new in replacements.items():
    assert old in s, old
    s=s.replace(old,new)
s=s.replace("'@@MATCHES@@':str(", "'@@MODULECOUNT@@':str(module_count),'@@MATCHES@@':str(")
anchor='<h2 id="definitions">'
addition='''<div class="callout"><b>本轮新闭合与仍有条件的连接：</b>
<code>c09_proved : C09</code> 已证明任意 N 的正性、合法性和光滑性。
<code>c08_of_c07 : C07 → C08</code> 与 <code>c16_of_c07 : C07 → C16</code>
也已通过 Lean，说明有限 h 双线性对与非线性精确解只剩 C07 这一条核心前提。
它们不计作 C08/C16 的无条件证明。C22 是解族紧盒一致误差，不能只因 C07 缺失就断言不可推进。
完整验收路线与剩余目标见 <a href="Paper/dlw_semidiscrete/lean_contracts/INTEGRATION_STATUS.md">系统—数值—Lean 衔接记录</a>。</div>

'''
assert anchor in s
s=s.replace(anchor,addition+anchor)
p.write_text(s,encoding='utf-8')

# Correct a historical overstatement in the index as well as the current README.
for rel in ['AGENTS.md','Paper/dlw_semidiscrete/lean_contracts/README.md']:
    p=ROOT/rel
    s=p.read_text(encoding='utf-8')
    s=s.replace('→ 命题**为真**；缺的是形式化机器',
                '→ **仅这些有限样例精确通过，不能推出任意 N 命题为真**；仍缺形式化机器')
    s=s.replace('**命题为真**；缺的是形式化机器：',
                '**这些有限样例通过，但不构成任意 N 命题的证明**；仍缺形式化机器：')
    p.write_text(s,encoding='utf-8')
print('Updated dashboard wording and corrected finite-sample claim.')
