# DLW：GSG 三点二阶差分

当前交付为根目录 `notebook/DLW数值分析report.ipynb` 和 `dlw_numerical.html`。固定网格与动网格均采用三点二阶空间差分，表格和曲线由完整执行的 Notebook 生成。

GSG 原文为 Feng、Sheng、Yu，*Integrable semi-discretizations and self-adaptive moving mesh method for a generalized sine-Gordon equation*，Numerical Algorithms 94 (2023), 351–370，[DOI](https://doi.org/10.1007/s11075-023-01504-1)。第 364 页、Scheme 5 的式 (4.13)–(4.14) 使用直接三点二阶导数。原文更新相邻场值差，式中分母为 Δx；对应的二阶导数算子分母为 Δx²。

DLW 的一阶项采用标准三点中心差分，二阶项直接用三点差分：

```text
Dxi(f)[i]  = (f[i+1] - f[i-1]) / (2*dx)
Dxxi(f)[i] = (f[i+1] - 2*f[i] + f[i-1]) / dx**2
J = 1 + Dxi(s)
D1(f) = Dxi(f) / J
D2(f) = Dxxi(f) / J**2 - Dxi(J)*Dxi(f) / J**3
```

动网格二阶公式由坐标变换的链式法则得到。SD 线性矩阵和 SD2 端点跃量延拓使用同一组算子。节点数 256、区域长度 40、y 格距 0.125、dt=0.000125、T=0.01、4001 个评价点保持不变。SD 使用双线性隐式中点，SD2／FD 使用 Euler 或 RK4。

17 个代码单元完整执行，24 组主试验和 12 组附加时间细化完成，输出保存为 6 张表、3 张图。独立固定／动网格制造解检查给出约 2 的空间观测阶；SD 隐式中点时间阶 1.995–2.000，SD2 Euler 时间阶 0.995–1.000。主 HTML 保留七节、五张三线表及三张曲线图。

`result_comparison.json` 逐项列出旧四阶与新二阶的 48 个误差值及比值。`revision_manifest.json` 记录来源、配置、执行、校验与交付 SHA-256。四阶原件保存在上一层 `before_gsg_second_order/`；历史 direct τ 与版式修订记录继续保留。

## 运行与复现

直接在 VS Code 或 Colab 打开 Notebook，选择 Python 内核，从第一个代码单元依次运行。Notebook 自包含，依赖 NumPy、pandas、SciPy、Matplotlib 和 IPython。

工作区根目录的构建、执行与核验命令：

```powershell
$dlwPython = 'C:/Users/msz/aca/Workspaces/report_colab_20261006/.venv/Scripts/python.exe'
$env:OPENBLAS_NUM_THREADS = '1'
$env:OMP_NUM_THREADS = '1'
& $dlwPython -X utf8 Workspaces/notebook_reports_20261006/build_dlw_numerics_notebook.py
& $dlwPython -X utf8 Workspaces/notebook_reports_20261006/execute_dlw_notebook.py
& $dlwPython -X utf8 Workspaces/notebook_reports_20261006/verify_second_order_spatial.py
& $dlwPython -X utf8 Workspaces/notebook_reports_20261006/verify_dlw_tau.py
& $dlwPython -X utf8 Workspaces/notebook_reports_20261006/verify_direct_tau_delivery.py
& $dlwPython -X utf8 Workspaces/dlw_notebook_static_20261007/build_static.py
& $dlwPython -X utf8 Workspaces/dlw_notebook_static_20261007/verify_static.py
& node Workspaces/dlw_notebook_static_20261007/check_static.cjs
& $dlwPython -X utf8 Workspaces/notebook_reports_20261006/gsg_second_order/register_revision.py
```

Python 依赖见 `../requirements_dlw.txt`。执行器在新内核中运行，以 inline 后端保存绘图，并将代码哈希写入结果和执行证据。NumPy 曲线缓存及独立图文件保存在本地；Notebook 和 HTML 内嵌展示所需图像。
