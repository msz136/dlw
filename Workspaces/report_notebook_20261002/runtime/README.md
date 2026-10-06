# Report 分段运行服务（agent 文档）

用户入口为工作区根目录 `Report.exe`。启动器自动检查/隐藏启动本服务，再打开 `Report.html`；重复打开复用同一服务。服务只绑定 127.0.0.1，使用本机已安装 Python 和现有 Lean/Mathlib，没有环境安装或公开端口。旧 CMD/PowerShell 入口保留在历史材料中，当前用户流程不使用它们。

## 实际执行与会话

每条路线按 `import → start → endpoint` 三段运行。import 用标准 `_lean_shared/check_lean.py` 重新检查该路线的完整证明库，目标为 ReportNonlinearUW/ReportNonlinearQRM，随后真实编译纯 import 薄单元；它不执行显示的终点 example 调用。start 与 endpoint 各用固定 Lean 编译器只编译当前薄单元，沿用同一会话刚刚检查过的库及前段 .olean。start 完整定义并打印双线性起点 StartPoint，不再做导数/变量定义核对；endpoint 从该起点实际调用原目标、原假设的定理并检查端点公理。

`lean_material/stage_manifest.json` 和 `steps/` 给出六个单元的精确可信源码。浏览器只能选择 route/stage，不提交任意路径/源代码/shell。前后核对原证明闭包 SHA-256、当前显示单元 SHA-256、此前编译产物 SHA-256 与运行配置；变化使会话失效。库检查进程为 0/PASSED、当前单元真实编译为 0/PASSED才可返回 ok；终点仅允许 propext、Classical.choice、Quot.sound。无 sorry/admit/新axiom。数学范围保持每j正实联合解析 F/G、h≠0 和 SemiPair 假设。

## 固定接口

- GET `/Report.html`、`/dlw_error_theory.html`：精确两份本地报告；不任意浏览文件。
- GET `/api/health`：service/version/leanVersion/toolchain/mathlibCommit/pid/port/status/workspace/script/activeJobs。
- GET `/api/lean/cells`：精确分段材料清单。
- POST `/api/lean`：`{route:'uw'|'qrm',stage:'import'|'start'|'endpoint',sessionId:null|32hex,expectedSources:{filename:sha256},expectedCellHash:sha256}`；import 的 sessionId 为 null，后段用前段返回的 sessionId。202 返回 jobId/status/sessionId。
- GET `/api/lean/{jobId}`：真实当前状态、stage/sessionId/completedStages、compilerOutput/log/elapsedSeconds/sourceHashes/returncode/axioms、库 runResult 与当前 cellResult/cellResultPath。compilerOutput 仅含 Lean 原始 stdout/stderr（按读取顺序合并），log 保留内部审计记录；网页直接显示 compilerOutput，不追加完成说明或折叠。
- POST `/api/lean/{jobId}/cancel`：空JSON，终止对应进程树。
- POST `/api/lean/reset`：`{route,sessionId}`，取消该会话正在运行的单元，清空前置完成标记。
- POST `/api/session`：`{action:'open'|'heartbeat'|'close',pageId:UUID}`。各浏览器标签独立lease，页面15秒心跳，关闭发送close。
- POST `/api/stop`：内部维护 `{token,idleOnly:true}`；随机token只在本地状态文件，不暴露到网页。锁内有任务时拒绝空闲升级。

写请求要求同源 Origin、application/json、小body，拒绝跨域、Origin:null、未知Host/路径/额外任意代码字段。一次只允许一个Lean编译任务。file页面不向服务执行POST，用户通过Report.exe进入HTTP页。默认无页面闲置180秒退出；无页面的编译完成后120秒回收，活跃页面或编译不中断。非默认端口用独立状态文件，避免测试覆盖8766凭据。

2.2.0 继续使用固定内部 `--check-library-stream` 子模式调用未修改的标准 checker；只将 Lean 进程真实输出与 checker 审计文本送入不同 JSON 通道。原导入闭包、证明审计及结果文件规则不变。`stepwise_lean.py` 的当前单元输出直接来自 Lean 子进程；原始诊断在编译失败时也直接显示。Windows 服务禁用地址重用，第二实例不得共享已有端口或覆盖其 PID/token 文件。

## 留档与验证

`jobs/{jobId}/job.json`、`cell-result.json`、该session的lib及标准checker的 `.lean-runs/{runId}/result.json/build.log` 均保留，不删除。历史成功作业只是旧日志，不能代替新会话；重置或服务重启后需重新import。

- `stepwise_validation_uw.json`：UW完整三段实际PASSED、前置顺序、缺会话、重置后旧session拒绝。
- `stepwise_validation_final.json`：当前显示单元hash拒绝、lease等最终接口核查（若存在）。
- 上一版 `service_verification_*.json`、`lifecycle_verification_*.json` 留作历史；旧 `verify_service.py`/`verify_lifecycle.py` 针对1.0协议，不作为2.0重新运行入口。
- 当前QRM网页三阶段、顺序/重置核验在上层 `stepwise_lean_ui_validation.json`；单入口/闲置/升级验证在 `package/`。
- 本轮原始编译输出、当前 UW 三阶段和页面布局在上层 `raw_output_validation.json`；真实成功/错误/stderr/Unicode传输验证见 `raw_compiler_validation.json`。六单元仅注释变化的逐行核对在 `lean_material/raw_output_semantic_validation.json`。
