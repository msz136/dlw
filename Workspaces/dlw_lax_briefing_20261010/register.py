from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
backup = HERE / 'registration_before'
backup.mkdir(exist_ok=True)
for name in ['PROGRESS_LOG.md', 'FILE_INDEX.md']:
    dest = backup / name
    if not dest.exists():
        dest.write_bytes((ROOT / name).read_bytes())
progress = ROOT / 'PROGRESS_LOG.md'
text = progress.read_text(encoding='utf-8')
marker = '> **2026-10-09（半离散 DLW 的 Lax 推导）：**'
addition = ' **2026-10-10 专题汇报整理：** 新增 [半离散 Lax 专题汇报](report/dlw_lax_briefing.html)，集中原方程、辅助热势、格点／时间线性对、Darboux相容性正反向证明，并补齐τ双线性与PF代入公式。统一时间算子为𝒬以区别PF变量Q；说明逐点w≠0、退化反例及PF时间归一化。16个编号公式、104处严格离线渲染，7项局部符号检查通过；1440/390px及打印布局通过，桌面已目视检查。未重跑PDE或Lean。正文、构建与验证见 Workspaces/dlw_lax_briefing_20261010/。'
assert marker in text
line = next(line for line in text.splitlines() if line.startswith(marker))
if 'report/dlw_lax_briefing.html' not in line:
    text = text.replace(line, line + addition, 1)
progress.write_text(text, encoding='utf-8')
index = ROOT / 'FILE_INDEX.md'
text = index.read_text(encoding='utf-8')
marker = '<!-- DLW_LAX_BRIEFING_BEGIN -->'
if marker not in text:
    files = sorted(p for p in HERE.rglob('*') if p.is_file())
    files += [ROOT / 'report/dlw_lax_briefing.html']
    block = marker + '\n## 半离散 DLW 的 Lax 专题汇报（2026-10-10）\n\n'
    block += '\n'.join(f'- [{p.relative_to(ROOT).as_posix()}]({p.relative_to(ROOT).as_posix()})' for p in files)
    block += '\n<!-- DLW_LAX_BRIEFING_END -->\n\n'
    text = block + text
index.write_text(text, encoding='utf-8')
print(json.dumps({'progress':'merged into existing Lax entry','index':'registered','backups':str(backup)}, ensure_ascii=False))
