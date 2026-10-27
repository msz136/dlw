# DLW 与 2HS 的 LaTeX 论文

2026-10-27 从根目录 `dlw-paper.html` 与 `2HS paper.html` 转写。

- `dlw/main.tex`、`dlw/main.pdf`、`dlw/images/`：DLW，14 图、8 表。
- `2hs/main.tex`、`2hs/main.pdf`、`2hs/images/`：2HS，10 图、8 表。
- 每篇只有一个正文 TeX 文件，参考文献也在其中；图片全部随目录携带，无须访问原工作目录。
- 公式取自 HTML 的原始 TeX，正文、公式编号、图表编号和参考文献顺序保留。网页目录、下载按钮、打印重复图及资源页脚不进入论文。
- 优先使用对应图的矢量 PDF 原文件，便于放大和打印。

## VS Code

打开 `papers.code-workspace`，打开需要编辑的 `main.tex`，通过 LaTeX Workshop 的 Build 命令（通常 Ctrl+Alt+B）编译。项目已配置 XeLaTeX 连续运行两次，使用本机 MiKTeX，不依赖 latexmk/Perl；不会自动清理文件。

也可以在此目录运行 `powershell -ExecutionPolicy Bypass -File ./build.ps1`；仅编译一篇时追加 `-Paper dlw` 或 `-Paper 2hs`。生成的 `main.pdf` 位于各自正文旁，辅助文件归入 `build/`。

需要 MiKTeX/XeLaTeX 和 Times New Roman 字体（当前 Windows 环境已验证）。Codex 内置编译器的 latexmk 路线因本机缺少 Perl 失败；上面的直接 XeLaTeX 路线已成功生成 PDF。

转换和核验记录：`../Workspaces/paper_latex_20261027/`。之后可直接编辑 TeX；重新运行转换程序会覆盖 TeX，请勿在人工修改后直接重跑转换。


## 2026-10-27 图文修订

DLW 说明按图穿插，分面图允许沿行间空白跨页；Figure 11、12 与其说明和图注紧凑排列。DLW 的交叉虚线只用于曲线重叠处，分开后为实线。2HS 的对数误差图不连接给定的零边界误差，边界单元宽度单独显示。两篇 PDF 的图形均使用 DejaVu Sans 字体。原始 HTML 与数值数据没有更改；正文源和图片已独立保存在各自目录。
