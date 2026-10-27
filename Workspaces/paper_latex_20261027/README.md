# HTML 论文转 LaTeX / PDF（2026-10-27）

用户指定成品目录为根目录 `pdf/`。两套独立源文件是 `pdf/dlw/main.tex` 和 `pdf/2hs/main.tex`，图片均在各自 `images/`，已用本机 MiKTeX XeLaTeX 编译两遍。DLW 39 页（14 图、8 表），2HS 15 页（10 图、8 表）。每篇的参考文献直接包含在唯一的正文 TeX 文件中。

## 转换范围

来源为根目录 `dlw-paper.html` 和实际文件名 `2HS paper.html`。使用 KaTeX annotation 中的原始 TeX；删除网页导航、资源页脚、PDF 下载按钮和打印专用重复面板。保留正文、数学内容及原有编号。图片使用同图对应矢量 PDF 文件，复制后采用短文件名。表格转为可编辑 LaTeX 三线表；DLW Table 8 使用自然列宽，避免拆开科学计数法。

## 证据与限制

- `conversion_manifest.json`：原文 SHA256、图片来源与副本 SHA256、图表及公式数量。
- `validation.json`：逐个核对原始公式与未改写的非数学可见文本均在 TeX 内（Figure 9/10 的两段说明按分图顺序改写并另存原文）；PDF 有全部图表编号；编译无缺字、无越界；原 HTML 未变更。
- `preview/`：全篇页面缩略图，以及 Poppler 渲染的长公式页、高精度表格页；已目视检查。最新 Table 8 见 `dlw-table8-final.png`。
- 核验是转换完整性与排版核验，不是新增的数学证明或数值结果认证。
- `pdf/build.ps1` 已实际运行，全部编译成功。VS Code 的独立 `pdf/papers.code-workspace` 配置直接调用 XeLaTeX 两遍；已确认安装 LaTeX Workshop。未改全局 VS Code 设置。
- Codex 内置预览编译尝试未成功：latexmk 缺 Perl，备用编译器资源下载失败/超时。该问题不影响已生成的 PDF 和直接 XeLaTeX 编译。

后续直接编辑 TeX 即可。`convert.py` 为本轮转换程序；重新运行会覆盖人工编辑后的正文。`validate.py` 对照当前原 HTML 和转换清单检查；原 HTML 或 TeX 后续独立修改后应相应调整核验范围。


## 用户反馈后的图与分页修复（2026-10-27）

- DLW 图 9、10、13、14：读取原始时间序列，重合处交叉虚线，分开后恢复实线。图 13、14(d) 的少量分叉由原始数值差异产生，未移动曲线或篡改数据。图 1–14 均逐张检查。
- 2HS 图 3、4：给定边界误差为零，不参与对数误差线的连接；所有节点严格递增。图 7、8 的边界单元宽度单独以空心点表示，其他内部真实误差尖谷保留。图 1–10 均检查。
- DLW 图文穿插，图 1–10、13–14 沿无绘制内容的白边裁成两行，5–8 则裁成四行，允许跨页；图注与最后一行保持同页。图 11、12 缩至版心宽 85%，与说明及图注同页；39 页、14 图、8 表。2HS 15 页、10 图、8 表。
- 两文图字体均为 DejaVu Sans，正文为 Times New Roman。源图保持矢量；图形数据不重算、不平滑，重叠渲染只变线型。原始 HTML 保持不变。
- 核验：`figure_review/redraw_validation.json`（轨迹和节点）、`figure_review/pagination_cuts.json`（分行白边）、`figure_review/font_validation.json`（24 图字体）、`validation.json`（编译和图表完整性）；最终分页页面在 `figure_review/final-layout-*`、`figure11-adjusted.png`、`figure12-adjusted.png`。重绘前文件和分页调整前版本保留在 `figure_review/before/`、`before_pagination/`。

## 2HS 引言与参考文献（2026-10-27）

直接编辑 `pdf/2hs/main.tex`，引用从2条增至7条，补充HS来源、2HS精确解、几何积分、标量HS收敛及动网格背景。原有GSG题名与作者规范化，正文统一使用cite。双遍编译16页，无未解析引用、缺字或越界；第2–4节除引用键外未改。桌面PDF同步。来源与核验见 `references_2hs_20261027/sources.md`、`validation.json`；该目录保留修改前版本。
