# 刘维尔可积性研究：可复核材料

正文：[半离散 DLW 的刘维尔可积性研究](../../dlw_liouville_integrability.md)。

这些文件记录构造性数学证明的精确代数检查。有限 N、有限阶检查用于发现符号错误；任意 N、任意阶结论必须阅读正文的一般证明。新括号是明确指定的孤子参数泊松结构，不是原场 J₀ 的继承。

## 运行

需要 Python 3 和 SymPy。使用已有项目环境运行：

```sh
python Workspaces/dlw_liouville_20261005/run_checks.py
```

该脚本会顺序执行七个证书并更新本目录 `validation.json`，记录 Python/SymPy 版本、证书哈希、实际退出码及原始输出。不访问网络，不推送仓库，不修改其他研究文件。

| 文件 | 检查内容 |
|---|---|
| `verify_general_structure.py` | 前四谱系数、Hamilton 识别、谱参数反演、Vandermonde 与子集支持恢复样例 |
| `all_rank_bilinear_certificate.py` | 不依赖矩阵大小的行列式双线性标量恒等式 |
| `moduli_certificate.py` | 谱积分、双孤子独立性、成对散射正则性 |
| `physical_immersion_certificate.py` | 论文双孤子参数到物理取值的精确有理 Jacobian |
| `single_and_casimir_certificate.py` | 单孤子局部物理坐标以及新括号不保留原质量 Casimir 的证据 |
| `cross_n_certificate.py` | 零强度退化、tau 公因子、相容观测量括号限制 |
| `atomic_poisson_certificate.py` | 共同有限原子括号、一般函数 Jacobi 和共同 Hamilton 流 |
| `CROSS_N_GLUING_PROOF.md` | 全 N、全阶的零强度拼接证明草稿 |
| `ATOMIC_POISSON_CONSTRUCTION.md` | 一个不预先指定 N 的共同泊松观测框架 |
| `validation.json` | 本次真实运行记录，不是历史检查的转述 |

本次没有运行 Lean、重新核验整个旧周期层级、证明一般 PDE 适定性或执行时间数值模拟。一般物理模空间和全局分层几何的限定范围见正文。英文补充里的未来工作描述以主报告的精确声明为准。
