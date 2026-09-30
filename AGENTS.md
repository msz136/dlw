# AGENTS.md — 工作区入口

**工作区**：`C:\Users\msz\aca`
**做什么**：把 Feng–Sheng–Yu 的 GSG 半离散化方法移植到 Sheng–Yu 的 (2+1) 维 DLW 系统，
给出离散双线性方程与孤子结构，并判断这个离散系统本身有没有可积结构。
**东西放哪**：论文、文献、原文 → `Paper\`；代码、实验、报告、网页源码 → `Workspaces\`。
**进度记哪**：一律写 [`PROGRESS_LOG.md`](PROGRESS_LOG.md)（最新在上）。**本文件只放索引与约定，不记进度。**
**逐文件索引**：[`FILE_INDEX.md`](FILE_INDEX.md)。

## 目录

```
C:\Users\msz\aca\
├── AGENTS.md / PROGRESS_LOG.md / FILE_INDEX.md   入口 / 进度档 / 逐文件索引
├── index.html              论文式报告（生成物，1.89 MB，自包含）
├── numerical_analysis.html 数值总报告（生成物）
├── lean_verification.html  Lean 核验页（生成物）
├── Paper\                  论文、文献、原文：refs\ sources\ reports\
├── Workspaces\             所有项目工作：dlw_semidiscrete\ gsg_project\ lean_contracts\
│                           expression_*\ analysis_*\ numerics_*\
├── Trash\                  废弃物只移到这里，不删除
├── lean-toda\              既有 Lean 工程（原地不动）
└── _lean_shared\           共享 Lean 4.34.0 + Mathlib 环境（原地不动）
```

## 约定

1. **不删除任何东西**：禁用 `rm` / `Remove-Item` / `del` / `os.remove` / `shutil.rmtree`。
   不要的文件只 `Move-Item` 进 `Trash\`
2. **Lean 部分原地不动**：`lean-toda\`、`_lean_shared\`、`Paper\dlw_semidiscrete\lean_contracts\`、
   `Paper\gsg_project\lax\lean\`、`Workspaces\lean_contracts\`。验证只走 `_lean_shared\Check-Lean.ps1`
   （返回码 0 **且** 输出 `PASSED` 才算过；`sorry`/`admit`/新 `axiom` 一律拒绝）。
3. **三个 HTML 都是生成物，不要手改**：改 `_src\*.src.html` 后跑 `build_html.ps1`（数值页另走
   `sync_numerical_results.py`）。数学段里的 `<`/`>` 要写成 `&lt;`/`&gt;`，否则公式整段不渲染。
4. **进度写 `PROGRESS_LOG.md`，不写本文件**；同专题的新进展要**合并**进旧条目，不要无限追加。

