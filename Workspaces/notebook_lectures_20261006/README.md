# 三份笔记本的配套讲稿

交付在 `C:\Users\msz\aca\notebook\讲稿\`：`非线性化讲稿.html`、`2HS数值分析讲稿.html`、`DLW数值分析讲稿.html`。三份页面分别配合同名专题的 `report.ipynb` 演示；数学、代码与结果说明的权威正文为本目录的 `nonlinear_body.html`、`hs_body.html`、`dlw_body.html`。

## 构建与核验

从 `C:\Users\msz\aca` 的 PowerShell 执行：

```powershell
$lecturePython = 'C:\Users\msz\aca\Workspaces\report_colab_20261006\.venv\Scripts\python.exe'
& $lecturePython -X utf8 Workspaces/notebook_lectures_20261006/build_lectures.py
& $lecturePython -X utf8 Workspaces/notebook_lectures_20261006/verify_lecture_content.py
& 'C:\Program Files\nodejs\node.exe' Workspaces/notebook_lectures_20261006/check_lectures.cjs
```

`build_lectures.py` 包装三份正文，复制已有本地 KaTeX 0.18.7、字体及许可证，从笔记本已保存输出提取原 PNG 图；它不推进 PDE 或重新编译 Lean。`verify_lecture_content.py` 对照当前笔记本检查全部代码单元覆盖、真实连续源码摘录（每块不超过 12 行）、本地链接与非线性化原公式（1）—（22）。`check_lectures.cjs` 用真实无头 Edge 检查本地文件的桌面、390px 窄屏、打印视图、公式、图像、锚点和资源请求。

核验入口会更新各自的当前证据 JSON；修改正文后先保留旧证据，再构建和核验。页面资源留在交付的 `assets/` 中，打开时不需要远程请求。

## 本轮证据

- `build_validation.json`：三份交付及其当前笔记本哈希；12／7／12 节，21／16／20 个关键代码摘录。
- `content_validation.json`：覆盖非线性化 14、2HS 13、DLW 15 个代码单元，共 42 个；57 个摘录均来自对应源码的连续片段。
- `browser_validation.json`：三份页面的桌面、窄屏及打印检查全部通过；无公式错误、原始公式残留、页面溢出、坏图、失效锚点或远程请求。窄屏长源码块可在自身区域横向滚动。
- `lecture_1_*`、`lecture_2_*`、`lecture_3_*`：三份页面的 1440px、390px 与桌面公式／代码段截图；顺序为非线性化、2HS、DLW。
- `hs_reference_correction.json` 与 `fix_hs_reference.py`：只把 2HS 的 `hs-time-model` Markdown 引用“式（4）或（28）”改为“式（4）或（6）”；所有代码源、执行计数与实际输出的摘要不变。修改前笔记本及执行证据在 `before_reference_fix/`。校正已完成，不需要重复运行修正器。

三份讲稿的数值内容来自笔记本已保存的真实结果；本轮新增正文和页面核验，没有重跑数值轨道。非线性化的纵向截断残差与另外两份讲稿的有限时间场误差分别解释。

## 登记

`register_lectures.py` 首次运行时先保存根目录 `PROGRESS_LOG.md`、`FILE_INDEX.md` 到 `before_records/`，合并两个既有专题进度条目，并在独立笔记本索引前插入 `NOTEBOOK_LECTURES_INDEX_BEGIN/END` 块。`registration.json` 记录交付、资源、当前来源及证据哈希，以及记录修改前后的哈希；既有其他项目的 registration 保持原样。

```powershell
& $lecturePython -X utf8 Workspaces/notebook_lectures_20261006/register_lectures.py
& $lecturePython -X utf8 Workspaces/notebook_lectures_20261006/register_lectures.py --verify
```

登记已存在时默认命令也只核对当前文件；它不覆盖历史登记。`--verify` 检查登记的文件存在且 SHA-256 未变。之后若继续改正文或记录，应另存新的登记证据，不改写本轮 `registration.json`。
