**工作区**：`C:\Users\msz\aca`
**做什么**：2HS,DLW的数值分析
**东西放哪**：论文、文献、原文 → `Paper\`；代码、实验、报告、网页源码 → `Workspaces\`。
**进度记哪**：一律写 [`PROGRESS_LOG.md`](PROGRESS_LOG.md)（最新在上）。**本文件只放索引与约定，不记进度。**
**项目与探索支线索引**：[`FILE_INDEX.md`](FILE_INDEX.md)（按项目登记，不逐文件展开）。
## 目录
```
C:\Users\msz\aca\
├── AGENTS.md / PROGRESS_LOG.md / FILE_INDEX.md   入口 / 进度档 / 项目与支线索引
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

4. **登记以项目／独立探索支线为单位**：`FILE_INDEX.md` 只登记名称、问题范围、主要入口与所属目录；同题续推更新原项，同一目录内的新独立问题增加支线。代码、证明、实验数据、图、日志、核验、备份均归所属项目，不逐文件追加，也不把缓存／运行目录生成到总索引。必要的细清单只放项目内部。
5. **按需读取**：先从项目索引定位相关项目，再读该项目入口和相关进度条目；不要默认加载整份进度档、历史逐文件台账或遍历全部产物。历史台账仅供具体追溯，不再作为当前登记入口。

