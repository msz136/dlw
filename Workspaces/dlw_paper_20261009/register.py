from pathlib import Path
import re, shutil, json, hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
backup=HERE/'registration_before'
backup.mkdir(exist_ok=True)
for name in ('PROGRESS_LOG.md','FILE_INDEX.md'):
    if not (backup/name).exists():shutil.copy2(ROOT/name,backup/name)
progress='''<!-- DLW_PAPER_DRAFT_BEGIN -->
> **2026-10-09：DLW 理论—数值论文初稿。** 新增 [论文阅读版](report/dlw_paper_draft.html)，按连续 DLW、交错双线性化、任意 N Gram 证明、SD、二阶连续极限、SD2、两种形式的 Lax 表示、数值实现与实验、结论及四篇参考文献整合；68个编号公式、4张结果表及参数表、6张既有数值图。补写固定 x 网格三点差分和动网格 Jacobian 公式，说明 x/t 数值离散与 y 半离散结构的区别、势变量时间规范及 Lax 反向非退化条件。用户要求节省用量、仅撰写排版后未再重算；此前已完成36组主试验和12组Euler细化，108个主表数值与保存精度一致。实验、原Notebook和原报告均未修改；图直接取原Notebook保存输出。初稿保留短时范围、高频分支及CN容差对阶检验的影响。源码与排版记录见 `Workspaces/dlw_paper_20261009/`。
<!-- DLW_PAPER_DRAFT_END -->

'''
p=ROOT/'PROGRESS_LOG.md'; old=p.read_text(encoding='utf-8')
old=re.sub(r'<!-- DLW_PAPER_DRAFT_BEGIN -->[\s\S]*?<!-- DLW_PAPER_DRAFT_END -->\s*','',old)
p.write_text(progress+old,encoding='utf-8')
entries=['<!-- DLW_PAPER_DRAFT_INDEX_BEGIN -->','**DLW 论文初稿（2026-10-09）：**','', '- [report/dlw_paper_draft.html](report/dlw_paper_draft.html)：完整离线HTML论文阅读版。']
for f in sorted(HERE.iterdir()):
    if f.is_file():
        rel=f.relative_to(ROOT).as_posix()
        entries.append(f'- [{rel}]({rel})：'+({'manuscript.md':'合并正文源。','lax_bridge.md':'Lax 对及势规范正文。','numerics.md':'数值方法与实验正文。','assemble.py':'论文结构整合与编号。','reproduce.py':'用户要求停止重算前的复现入口。','numerical_validation.json':'既有数值复核与保存输出来源。','build.py':'离线HTML构建。','layout.cjs':'阅读版排版检查。'}.get(f.name,'论文构建、图片或排版记录。')))
entries+=['- `Workspaces/dlw_paper_20261009/registration_before/`：登记前进度与索引备份。','<!-- DLW_PAPER_DRAFT_INDEX_END -->','','']
p=ROOT/'FILE_INDEX.md';old=p.read_text(encoding='utf-8')
old=re.sub(r'<!-- DLW_PAPER_DRAFT_INDEX_BEGIN -->[\s\S]*?<!-- DLW_PAPER_DRAFT_INDEX_END -->\s*','',old)
p.write_text('\n'.join(entries)+old,encoding='utf-8')
print('Paper draft registered.')
