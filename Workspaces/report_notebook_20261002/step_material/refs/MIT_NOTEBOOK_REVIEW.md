# MIT 原 notebook 的实际单元节奏

已读取公开 GitHub raw 源文件并保存在本目录，两份共含 65 个 cell。来源、SHA-256 与逐 cell 内容摘要见 `notebook_structure.json`。源文件是上游 master 的当前快照，供本次结构审查；本页运行不访问这些链接。

## 01_reflected_inertia.ipynb

来源：<https://raw.githubusercontent.com/RussTedrake/manipulation/master/book/robot/exercises/01_reflected_inertia.ipynb>

共 31 个 cell：14 个代码、17 个叙述。其执行安排实际为：

1. cell 1 检查 Colab 环境并按需安装；cell 2 导入 numpy、绘图、Drake 和课程支持包。
2. cell 3—4 先说明问题与摆的动力学；cell 5 用 8 行代码定义 `pendulum_dynamics`。
3. cell 6 说明状态/输入/输出；cell 7 建立符号状态、参数与系统；cell 9 单独创建并打印 context。
4. cell 10—13 给出电机/齿轮箱推导任务、留待填写的动力学函数和独立 grader 调用。函数定义与验证调用分开。
5. cell 14—15 专门设置电机与齿轮比参数。
6. cell 16—17 解释控制图并用 41 行定义 `BuildAndSimulate`。它创建系统、控制器、logger、context 后返回 simulator 与日志；此定义内没有推进时间。
7. cell 19 单独调用构建函数，显示系统连接。cell 20—21 才指定参考角、增益与齿轮比，初始化 simulator，调用 `AdvanceTo`，再取样与画图。
8. cell 23 运行一组目标角；cell 25—28 另做高齿轮比的对照；末尾用叙述问题引导读图与解释机制。

它没有把每个长函数都缩到同一长度，也没有强制计算和画图必须分成不同 cell。可以迁移的关键是：准备/import 在前，命名对象保存在会话中，随后每个短调用直接使用那些对象；定义与真正推进有清楚的运行时边界。

## 02_hardware_station_io.ipynb

来源：<https://raw.githubusercontent.com/RussTedrake/manipulation/master/book/robot/exercises/02_hardware_station_io.ipynb>

共 34 个 cell：14 个代码、20 个叙述。其执行安排实际为：

1. cell 1 为 Colab 环境准备，cell 2 导入，cell 3 单独启动 Meshcat。
2. cell 4 解释 station 的输入/输出；cell 5 用 17 行定义场景、创建 station。
3. cell 6 解释 context；cell 7 用 4 行创建 station context、取得 plant 和 plant context。
4. cell 9 单独画系统图。cell 10 解释一次具体写入与读取；cell 11 用 7 行设置关节位置，直接 `GetOutputPort(...).Eval(context)` 读出测量值。
5. cell 14 演示命名视图，cell 16 独立读取 plant 状态。
6. cell 18—23 设置速度，给出待填写的 `get_velocity`，再独立调用 grader。
7. cell 24—27 区分命令与测量，并用两个具体代码 cell 设置前馈力矩、读取实际命令，随后解释差异。

这份 notebook 的重点是一个操作对应一个可读结果。上下文不是对前面所有代码的重放，而是已有对象的当前状态；后续 cell 直接消费先前创建的对象。

## 对本报告的迁移

- 保留短说明、当前可见代码、Run、紧邻结果的正文节奏，按数学概念拆分。
- 本页数值侧实际执行 JavaScript，准备段确认原生 Math/Float64Array 并建立共享对象；不模拟 Python import 或声称执行 Drake。
- `lab.hs` 与 `lab.dlw` 保存已运行的函数和数据。每个 AsyncFunction 只执行当前一段。
- 2HS 的空间格式定义、RK4 定义、实际演化、终点误差分开；演化完成前，误差段不能画出结果。
- DLW 的解析剖面、主系数、有限格距残差定义分开；主系数表与减半格距图由各自的调用段产生。
- 两份原参考都采用真实 Python/Jupyter 的持久会话；本页采用显式共享对象提供相同的前后段消费关系，语言与运行环境如实标注。
