# Report 单一入口

`Report.exe` 是 Windows GUI 程序；复制到工作区根目录，双击即检查或启动隐藏的本地报告服务，等待正确版本就绪后在默认浏览器打开 `Report.html`。已启动时复用同一服务。无终端窗口，无启动/停止 CMD 用户入口。

这是现有工作区的单一入口封装。报告源码、Python、Lean 与 Mathlib 仍来自本机现有环境；仅把 EXE 复制到其他机器并不构成可移植独立安装包。EXE 不内嵌 HTML，后续更新同一个 `Report.html` 立即生效。

源码 `ReportLauncher.cs`；构建 `build-launcher.ps1` 使用已有 .NET Framework 4 编译器，不安装依赖。EXE 内嵌的 Python bootstrap 把服务输出直接记录到 `package/logs/`；启动器退出后日志句柄由 Python 服务持有。启动由工作区/端口命名的 mutex 串行化，并校验 service、源码 VERSION、工作区路径（服务提供时）和 ready 状态。启动失败才显示 GUI 提示。

服务升级时，仅当健康信息与本目录 state 的工作区、脚本、PID、端口、版本全部一致，且 `activeJobs=0`，才用 `idleOnly:true` 发起安全关闭再启动新版。服务在锁内再次拒绝活动任务；未知旧协议、外部服务或正在计算的服务均保留，不强制终止。首次从 1.0.0 迁移由本次维护工作关闭已确认空闲的旧服务。

内部验证参数：`--no-open --port 8767`，不会启动默认浏览器。`--idle-seconds N` 仅在服务支持同名参数后用于生命周期测试。实际用户双击无需参数。

服务关闭采用页面 lease 与闲置回收；具体期限与执行中任务行为由 `runtime/report_server.py` 负责。EXE 不保持后台驻留进程，不强制终止其他程序，不更改防火墙或全局设置。

## 验证

- `verification_20261002_125350_504.json`：两次并发启动仅新建一个服务，复用同一 PID；PE subsystem 2；Python 及其隐藏 conhost 无可见主窗口；没有 CMD/PowerShell 子进程；测试端口 8767 服务自行闲置退出。
- `upgrade_verification_20261002_125409_661959.json`：仅在 `package/upgrade_fixture_*` 隔离目录模拟源码从 2.0.0 更新到 2.0.1。活动任务协议状态为 1 时保留旧服务和 PID，中文提示完整；空闲后使用 `idleOnly` 平滑换版，新版服务自行退出。活动任务来自测试夹具，未声称运行科学证明。
- 默认浏览器打开路径使用系统 `Process.Start(URL)`；以上自动验证使用 `--no-open`，没有改变用户浏览器状态。最终从根入口双击即可走正常打开路径。

最新构建 `build.json`：18,432 bytes，SHA-256 `49407fc4ae6308cc977b882aea2f5795c08adad8a432708736aa05b609a3b503`。构建显式按 UTF-8 读取源码，GUI 中文提示由换版测试按原文断言。
