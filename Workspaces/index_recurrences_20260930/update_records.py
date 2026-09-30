from pathlib import Path

root=Path(__file__).resolve().parents[2]
log=root/'PROGRESS_LOG.md'
text=log.read_text(encoding='utf-8')
marker='2026-09-30（Index方法递推）'
if marker not in text:
    entry='**'+marker+'：** 按用户要求参照Report的论文措辞，在首页第2节补SD的P/W、SD2的Q/R及M_x逐层恢复、FD的P/v演化方程与实际空间右端；统一列Euler/RK4更新和已有动网格节点更新，不使用代码块或约定/边界说明。源文件_src/index.md经generate_index_report.py及build_html.ps1生成根index.html，同文副本同步；公式连续编号(1)–(16)。桌面1280与窄屏390检查96数学、无公式错误/页面溢出，桌面公式无滚动，原5表逐项不变。备份及页面记录在[递推式补充记录](Workspaces/index_recurrences_20260930/validation.json)，未新增数值演化。 '
    assert '> **' in text
    text=text.replace('> **','> '+entry+'**',1)
    log.write_text(text,encoding='utf-8')

index=root/'FILE_INDEX.md'
text=index.read_text(encoding='utf-8')
record='- `Workspaces/index_recurrences_20260930/check_page.cjs`、`validation.json`、`recurrences_desktop.png`、`sd2_desktop.png`、`recurrences_mobile.png`（首页SD/SD2/FD递推式、连续编号与宽窄屏检查）；`before/`（修改前正文、模板、页面及同文副本）'
if 'Workspaces/index_recurrences_20260930/check_page.cjs' not in text:
    anchor='- `Workspaces/gsg_project/dlw_report/_src/index.md`、`_src/index.src.html`、`generate_index_report.py`（当前正文与生成入口）'
    assert anchor in text
    text=text.replace(anchor,anchor+'\n'+record,1)
    index.write_text(text,encoding='utf-8')
print('Progress and file index updated.')
