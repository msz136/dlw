"""Merge the verified 2HS figure presentation revision into workspace records."""
from pathlib import Path
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
ROOT = PROJECT.parent.parent
validation = json.loads((HERE/'validation.json').read_text('utf-8'))
execution = json.loads((HERE/'hs_execution_validation.json').read_text('utf-8'))
assert validation['success'] and execution['success']
assert validation['notebook_sha256'] == hashlib.sha256(Path(validation['notebook']).read_bytes()).hexdigest()
for path in (ROOT/'PROGRESS_LOG.md', ROOT/'FILE_INDEX.md', PROJECT/'README.md'):
    backup = HERE/'before_records'/path.name
    backup.parent.mkdir(exist_ok=True)
    if not backup.exists():
        backup.write_bytes(path.read_bytes())

progress = ROOT/'PROGRESS_LOG.md'
source = progress.read_text('utf-8')
start, end = '<!-- HS_FIGURE_PRESENTATION_BEGIN -->', '<!-- HS_FIGURE_PRESENTATION_END -->'
source = re.sub(re.escape(start)+r'.*?'+re.escape(end)+r'\s*', '', source, flags=re.S)
anchor = '> **2026-10-06（非线性化与2HS独立笔记本）：** '
assert source.count(anchor) == 1
note = (start+'**2HS 图字体与端点显示（2026-10-07）：** '
    '五张数值图的文字与数学公式统一为 STIX 衬线字体，原生内核重新执行 16 个代码单元，'
    f'用时 {execution["elapsed_seconds"]} 秒，保存全部新图；'
    '数值演化语句与八个误差范数保持。正文和输出将初始物理区间简写为单孤子约 [-4.8,3.8]、'
    '二孤子约 [-5.7,3.7]，说明端点来自 X=-4,4 的解析坐标映射；底层计算节点保持原精度。'
    '生成器同步采用统一展示设置。实际图文字形、图输出及数值保持核验见 '
    '[展示核验](Workspaces/notebook_reports_20261006/hs_plot_fonts_20261007/validation.json)。'
    '未提交或推送。'+end+' **此前记录：** ')
source = source.replace(anchor, anchor+note, 1)
progress.write_text(source, 'utf-8')

readme = PROJECT/'README.md'
source = readme.read_text('utf-8')
start, end = '<!-- HS_FIGURE_README_BEGIN -->', '<!-- HS_FIGURE_README_END -->'
source = re.sub(re.escape(start)+r'.*?'+re.escape(end)+r'\n*', '', source, flags=re.S)
paragraph = (start+'\n2HS 当前展示（2026-10-07）：五张图统一使用 STIX 数学与文字字体，'
    '单孤子／二孤子的初始物理区间分别简写为约 [-4.8,3.8]／[-5.7,3.7]；'
    '实际节点由原解析坐标映射计算。16 个单元已完整重跑，八个误差范数与此前输出一致。'
    '字体与显示精度源为 `hs_presentation.py`，生成器同步调用；实际字形核对、执行与新图见 '
    '[展示修订](hs_plot_fonts_20261007/validation.json)。\n'+end+'\n\n')
anchor = '本目录维护根目录 `notebook/` 中的三份标准 Jupyter 笔记本。'
assert anchor in source
source = source.replace(anchor, paragraph+anchor, 1)
readme.write_text(source, 'utf-8')

index = ROOT/'FILE_INDEX.md'
source = index.read_text('utf-8')
start, end = '<!-- HS_FIGURE_INDEX_BEGIN -->', '<!-- HS_FIGURE_INDEX_END -->'
source = re.sub(re.escape(start)+r'.*?'+re.escape(end)+r'\n*', '', source, flags=re.S)
files = [ROOT/'notebook/2HS数值分析report.ipynb', PROJECT/'hs_presentation.py',
         PROJECT/'build_hs_notebook.py', PROJECT/'revise_hs_structure.py',
         *sorted(HERE.rglob('*')), Path(execution['backup'])]
links = []
seen = set()
for path in files:
    if not path.is_file():
        continue
    relative = path.relative_to(ROOT).as_posix()
    if relative in seen:
        continue
    seen.add(relative)
    links.append(f'- [{relative}]({relative})')
section = start+'\n**2HS 图字体与端点显示修订（2026-10-07）：**\n\n'+'\n'.join(links)+'\n'+end+'\n\n'
anchor = '<!-- NOTEBOOK_REPORTS_INDEX_BEGIN -->\n'
assert anchor in source
source = source.replace(anchor, anchor+section, 1)
index.write_text(source, 'utf-8')
print('Registered verified 2HS figure revision; no commit or push.')
