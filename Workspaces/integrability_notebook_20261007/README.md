# 一般周期 DLW 刘维尔可积性 Notebook

日期：2026-10-07。用户交付为 `C:\Users\msz\aca\notebook\DLW刘维尔可积性report.ipynb`，本目录同名文件保存生成时的项目镜像。用户重新运行并保存后，交付文件的输出与哈希可能改变。

## 正文精简（2026-10-07）

删除用户列出的防御性叙述，并逐段清理类似的前提自证与范围否定。开头仅留数学概述；正文直接解释条件、公式和关键 Lean 结论，结尾结束于式（19）。16 个 Markdown 单元经独立语言审阅，14 个正文单元修改。19 个编号公式、15 个完整代码单元对象、执行计数、元数据与保存输出逐项保持。生成器与交付正文一致。

当前交付 SHA-256：`62c3cd956a6c0747c308c5115bd6276228804fa878d2f4372246903de37cbd6e`。本轮只改正文，当前保存输出沿用此前真实执行；此前来源、执行与浏览器登记保留为历史记录。本轮快照、源文稿与保留性检查见 `prose_revision/`，具体哈希见 `prose_revision/validation.json`。

## 内容与已证范围

笔记本共有 31 个单元，15 个代码单元（1 个 Python 准备、14 个 Lean 单元），按照条件与周期格点、自由坐标及重构、原物理方程、谱基础、Cₙ/H₀/K/P、约化括号、守恒、对易、Fourier 频率、Jacobian 子式、泛型独立与最终定理排列。19 个编号公式与关键 Lean 定义和命题逐项对应，长证明保留在原库。

沿给定光滑原 PDE 解证明普通时间导数为零；在约化泊松括号下证明谱量与物理族对易；构造有限 Fourier 切片的非零 Jacobian 子式，并证明物理族每个有限前缀各自有开稠密独立集。最终定理显式保留 `FactorSpectralFoundation` 的正规 PDO 表示、形式逆元以及周期迹／Adler 基础接口。目标守恒、对易和独立性没有作为输入。完整定义及此前研究范围继续以 `Workspaces\dlw_integrability_lean_20261006\LEAN_PROOF_REPORT.md` 为准；该报告与证明源未改。

## 实际执行证据

- 首次独立原生 Python kernel 完整执行全部 15 个代码单元，253.193 秒，全部通过。该次 notebook 与原完整执行记录保存在 `before_conservation_revision\`。
- 随后仅在 `lean-conservation` 里增加 K、P 的显式 `HasDerivAt ... 0 t` 目标。在新内核运行准备、库导入和该守恒单元三个相关单元，35.394 秒，通过；其余 14 个代码单元的源码、输出、执行计数与元数据全部保留。证据为 `conservation_revision_execution_validation.json`、`conservation_revision_validation.json` 和 `conservation_revision.executed.ipynb`。
- `integrability_execution_validation.json` 将首次完整执行与后续局部修订分别登记。当前输出来自这两次真实执行，没有将局部修订写成第二次整本运行。
- `notebook_content_validation.json` 将 14 段 Lean 源码与保存输出逐段对照真实编译 `history.json`，全部匹配，105 模块原库哈希保持。
- `MATHEMATICAL_REVIEW.md`、`mathematical_content_validation.json` 与 `ReviewExamples.lean`／`review_compile.json` 保存只读数学审阅和独立示例编译。
- `runtime_validation.json` 的 8 个用例实际检查前置、导入、代码修改、失败证明、修复以及隔离源／产物变更。隔离副本位于 `runtime_validation_library\`；原库保持。
- `browser_validation.json` 核验正文精简前 notebook 与非线性化定义补充的离线预览，桌面、390px 和打印的公式、源码、输出及资源全部通过；本次没有自动操作 Colab 或 VS Code 的原生界面。PNG 在本目录，预览位于 `preview\`。

此前内容交付 SHA-256（运行保存后可改变）：`1bb3e881c082479dbfa770e5b481a086af404945e238a1a1b36895223c090aed`。

## 运行

在 VS Code 中打开根目录交付 notebook，选择 `C:/Users/msz/aca/Workspaces/report_colab_20261006/.venv/Scripts/python.exe`，按正文顺序点击 ▶。在 Colab 中则上传该文件，双击根 `notebook\启动Colab本地运行时.pyw`，将提供的地址用于“连接到本地运行时”。具体步骤见 `report\notebook_usage.html`。

`integrability_runtime.py` 复用 Lean 4.34.0、对应 Mathlib 与原研究工程 `.lean-runs\20261007_112653_73c4af05\lib\lean` 下已经完整核验的 105 模块编译库。`library_manifest.json` 绑定编译器、Mathlib、原源码及产物身份。只编译正在执行的显示单元，原库有变更则要求重新核验。`proof_cache\` 是运行器接口的空兼容目录，当前不经该目录复用库。没有云端 Lean 安装。

打开 notebook 时会显示文件中保存的编译输出；点击执行后以新的真实输出更新该单元。若修改上游条件或定义，应向下逐段执行。

## 运行器会话修复（2026-10-07）

用户在 `%%lean conditions` 遇到 `Run the Lean library import cell first.`。原实现每次调用 `load_lean()` 都新建运行器，并把 `library_ready` 重置为 false；重新运行 Python 准备单元后，即使刚才的库导入已成功，也会被人工前置检查拦下。

现在 `load_lean()` 在同一内核复用现有同类运行器，并重新注册 `%%lean`，以恢复被其他 notebook 替换的 magic。每个显示 Lean 单元均自带 `import FinalEndpoint`，在独立临时模块中只编译当前代码；取消 `library_ready` 的人工拦截，不执行任何前段单元。每次编译前后仍检查完整 105 模块库的源文件、编译产物及 Lean/Mathlib 身份哈希，失败证明继续报错，源码或产物变更继续拒绝复用。

真实内核回归为 66.237 秒，重现旧版报错后，验证了补丁重载、重复准备、跨 notebook magic 恢复及 conditions 两次独立编译；运行器 8 个用例通过，包括输入编辑、失败恢复和隔离库变更检查。原库、Notebook 正文及代码未由本次登记修改；当前交付哈希只作用户文件快照，不要求与此前保存输出时相同。证据与旧版备份见 `session_fix/`；历史 `registration.json` 保留，本轮登记为 `session_fix/registration.json`。

**应用修复：** 在当前 notebook 中重启内核，再执行首个 Python 准备单元，之后按正文顺序运行 Lean 单元。已打开的 Python 内核缓存了旧版导入，仅修改本地 `.py` 或重跑 `from integrability_runtime import load_lean` 不会自动更新旧实现。

## 生成与登记

- `build_integrability_notebook.py`：权威中文正文、LaTeX 和关键 Lean 单元生成器；`build_integrability_validation.json` 保存初稿来源哈希。
- `execute_notebook.py`：调用既有原生执行器；`finalize_conservation_revision.py` 保留首次完整证据并合并守恒单元局部执行结果。
- `build_preview.py`、`check_preview.cjs`、`verify_notebook.py`：来源、真实输出和浏览器核验。
- `nonlinear_revision\`：非线性化 notebook 式（7）的完整 `reportN1/reportN2` 定义补充、修改前备份及相关四单元实际编译证据，数值未重算。
- `before_records\`：使用说明、根进度、根索引及旧报告核验脚本修改前原件。
- `register_integrability_notebook.py`：合并同专题进度和逐文件索引，生成本次 `registration.json`，保留既有历史登记。

默认运行登记脚本只在项目内准备根记录草稿；确认执行、数学、视觉与交付镜像全部核验通过后，运行 `--register --content notebook_content_validation.json`。本次使用显式绝对路径参数，根记录和交付当前哈希由 `registration.json` 核对。
