**工作区**：`C:\Users\msz\aca`
**做什么**：2HS,DLW的数值分析
**东西放哪**：论文、文献、原文 → `Paper\`；代码、实验、报告、网页源码 → `Workspaces\`。
**进度记哪**：一律写 [`PROGRESS_LOG.md`](PROGRESS_LOG.md)（最新在上）。**本文件只放索引与约定，不记进度。**
**逐文件索引**：[`FILE_INDEX.md`](FILE_INDEX.md)。
## 目录
```
C:\Users\msz\aca\
├── AGENTS.md / PROGRESS_LOG.md / FILE_INDEX.md   入口 / 进度档 / 逐文件索引
├── theory_results.html / dlw_numerical.html / Report.html / dlw_hamilton.html / dlw_integrability.html   主入口
├── report\                 其余用户专题 HTML 报告
├── Paper\                  论文、文献、原文：refs\ sources\ reports\
├── Workspaces\             所有项目工作
├── Trash\                  废弃物只移到这里，不删除
├── lean-toda\              既有 Lean 工程（原地不动）
└── _lean_shared\           共享 Lean 4.34.0 + Mathlib 环境（原地不动）
```
## 约定

1. **不删除任何东西**：禁用 `rm` / `Remove-Item` / `del` / `os.remove` / `shutil.rmtree`。
   不要的文件只 `Move-Item` 进 `Trash\`
2. **进度写 `PROGRESS_LOG.md`，不写本文件**；同专题的新进展要**合并**进旧条目，不要无限追加。
3. 你可以撰写md和html来进行报告工作，如果你有什么非常希望用户阅读的，请撰写html而不是md，并放在 `report\` 下（主目录保留 theory_results.html、dlw_numerical.html、Report.html、dlw_hamilton.html、dlw_integrability.html），且提醒用户，当你撰写html时，请保持措辞简洁干净，只叙述关键部分，不要包含进工程约定/边界等低价值细节，请使用paper级的撰写风格；md文档通常用于agent阅读，因此没有此限制，你可以随意发挥

