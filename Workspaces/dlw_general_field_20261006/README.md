# 一般周期物理场的守恒层级与泊松结构

本目录对应主报告 [第 13–17 节](../../dlw_liouville_integrability.md#sec-field-theorem)，记录 2026-10-06 的推导与核验。

主要结论是具体守恒族 $\mathcal K,\mathcal P,\mathcal C_3,\mathcal C_5,\ldots$ 的守恒、两两对合和有限前缀泛型独立性。相空间为选定非零格点平均闭合下的一般光滑周期物理场。

## 证明入口

- [守恒族与判断](CONSERVATION_FAMILY_VERDICT.md)
- [一般场主方程与解析边界](RESEARCH_NOTES.md)
- [任意有限周期的矩阵 Lax 表示](GENERAL_PERIOD_MATRIX_LAX.md)
- [任意有限周期的原泊松坐标](GENERAL_PERIOD_FREE_FIELD_POISSON.md)
- [两格点逆变换和局部守恒递推](TWO_SITE_INVERSE_AND_LOCAL_HIERARCHY.md)
- [两格点三 Hamilton 算子与 Lenard 关系](TWO_SITE_POISSON_PENCIL.md)
- [混合时间条件下的一般场解](MIXED_TIME_EXISTENCE.md)

## 复现

依赖 Python、SymPy、NumPy。在本目录运行 `python run_checks.py`。脚本更新 [validation.json](validation.json) 和 `logs/`，记录源码哈希、退出码及软件版本。所有输出路径相对于脚本目录。

共 13 个检查入口：两格点物理方程与规范变换、全周期线性化、混合时间矩阵分解与数值验证、逆 Riccati 变换、六阶局部守恒律和四阶直接 Lenard 核验、完整泊松推前、任意阶生成恒等式、全周期矩阵表示和自由场括号，以及此前的二次谱符号、第五阶 BCH、两格点单值算子核验。

其中 `mixed_time_probe.py` 是数值核验，其余为符号／矩阵代数检查。有限周期数与有限阶数测试对应展开核验；任意周期、任意阶数的依据写在证明文件中。数值漂移结果另见 [mixed_time_probe.json](mixed_time_probe.json)。

本目录为可复核的研究证明草稿。完整谱坐标与全局作用角理论继续作为后续研究内容。
