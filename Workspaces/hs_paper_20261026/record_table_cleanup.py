from pathlib import Path
root=Path(__file__).resolve().parent;ws=root.parent.parent
note='2026-10-26｜2HS同轮精简：移除时间热图展开区，保留10组曲线图；9张表连续编号1–9并同步正文引用。空间表逐行明确a或Δx；自适应网格表6、7各四项误差最小值加粗。119数学渲染、编号/逻辑列/粗体/链接检查通过；数据未改，旧热图保留。证据：Workspaces/hs_paper_20261026/validation.json。'
with (ws/'Workspaces/workspace_catalog_audit_20261013/progress_history/2026-10.md').open('a',encoding='utf-8') as f:f.write('\n'+note+'\n')
p=ws/'PROGRESS_LOG.md';s=p.read_text(encoding='utf-8')
s=s.replace('新增6组时间误差热图置4.3展开区','时间热图已按用户要求移出正文（资产保留）').replace('现10组主图+2展开补图、9分算例表，101处数学渲染','现10组主图、9张连续编号表（1–9），119处数学渲染')
s=s.replace('下一步按用户节奏继续逐段审稿。','空间表逐行明确a或Δx；网格表6、7的各列较小误差加粗。下一步按用户节奏继续逐段审稿。')
p.write_text(s,encoding='utf-8')
readme=root/'README.md';s=readme.read_text(encoding='utf-8')
s=s.replace('10 numbered main figures and two expandable temporal-error maps (S1/S2), 9 case-separated tables (1, 2a/b, 3a/b, 4a/b, 5a/b)','10 numbered main figures without heatmaps or expandable supplements, 9 case-separated tables numbered consecutively 1–9')
s+='\nTable cleanup: spatial spacing cells explicitly name a or Δx; adaptive-mesh tables 6/7 bold the minimum of each of the four error columns within each case. Removed temporal maps remain on disk.\n'
readme.write_text(s,encoding='utf-8')
