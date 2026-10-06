# 2026-10-02 Lax 审计实际运行输出

以下逐行复制本次工具返回的标准输出；四项进程均返回退出码0。运行时使用 `python -B`，没有生成字节码缓存。
输入来源哈希见 `lax_source_hashes.json`。没有重新跑原有 PDE 或 Lean。

## verify_integrability_structure.py

```text
PASS: exact 2D Toda identities, 45 cases, N=1..5
PASS: Darboux operator identity on arbitrary wave function
PASS: both Darboux links have the same intermediate potential
PASS: Darboux shift coefficients expressed in physical fields
PASS: physical-field reconstruction of heat potentials
PASS: structural entry identity and exact soliton mass factor
PASS: normalized pair interaction is independent of h and tau shift
PASS: old transfer identification fails; scalar= 4/3 Mobius composition= 25/19
PASS: dispersion (sigma+2a*i*k)^2=k^4+4*k^3*C/K-h^2*k^2
PASS: all-N Gram determinant lemma scalar cancellation
ALL STRUCTURAL CHECKS PASSED
```

## verify_s_spectral.py

```text
PASS: heat and lattice spectral wave, N= 1
PASS: heat and lattice spectral wave, N= 2
PASS: heat and lattice spectral wave, N= 3
PASS: heat and lattice spectral wave, N= 4
PASS: heat and lattice spectral wave, N= 5
PASS: rank-one lattice update and spectral partial fractions
PASS: all-N Woodbury wave update
PASS: all-N spectral lattice compatibility scalar cancellation
PASS: normalized soliton transmission depends nontrivially on z
ALL SPECTRAL CHECKS PASSED; 180 exact parameter/step/site/spectral cases
```

## verify_nonlinear_closure.py

```text
PASS: averaged potential identity
PASS: potential difference identity
PASS: lower-wall Miura Riccati residual
PASS: upper-wall Miura Riccati residual
PASS: wall midpoint slope
PASS: wall jump slope
PASS: wall quadratic sum
PASS: wall drift sum
PASS: Q elimination identity
PASS: short u,w first residual
PASS: short u,w and u,v first equations agree
PASS: first closed residual
PASS: second closed residual
PASS: original-variable first equation
PASS: original-variable second equation
PASS: first continuum equation
PASS: first equation centered at y-h/2
PASS: second continuum equation
PASS: second equation has no first-order error
PASS: u physical limit
PASS: v physical limit
PASS: u definition is second order
PASS: v definition is second order
PASS: u second-order coefficient
PASS: v second-order coefficient
Exact h scan (h, error1/h^2, error2/h^2), point (1, 2, 3) : [('1/4', '106933/2048', '556229/2048'), ('1/8', '2043773/32768', '8886557/32768'), ('1/16', '35419453/524288', '142132349/524288'), ('1/32', '588682109/8388608', '2273907197/8388608'), ('1/64', '9595538173/134217728', '36381673469/134217728')]
Exact h scan (h, error1/h^2, error2/h^2), point (2, 3, 1) : [('1/4', '270695/1024', '301163/256'), ('1/8', '2465075/8192', '1202747/1024'), ('1/16', '20948363/65536', '4809083/4096'), ('1/32', '172558139/524288', '19234427/16384'), ('1/64', '1400471195/4194304', '76935803/65536')]
Exact h scan (h, error1/h^2, error2/h^2), point (3, 1, 2) : [('1/4', '6751/256', '165357/1024'), ('1/8', '582575/16384', '2629041/16384'), ('1/16', '10586557/262144', '41998017/262144'), ('1/32', '179763449/4194304', '671701761/4194304'), ('1/64', '2960287729/67108864', '10746162177/67108864')]
PASS: true continuous Hirota (6), (7), and B(f,g_y)+2Dx(f,g), symbolic N=1
PASS: Miura paper GLDW first equation equals continuous DLW
PASS: Miura paper GLDW second equation equals continuous DLW
PASS: Miura m Riccati residual equals normalized bilinear residual
PASS: Miura m-hat Riccati residual equals normalized bilinear residual
ALL SYMBOLIC CHECKS PASSED
```

## lax_audit_checks.py

```text
PASS: Darboux_difference
PASS: Darboux_sum
PASS: old_scalar_zero_curvature
PASS: bare_pair_degenerate_counterexample
ALL INDEPENDENT LAX AUDIT CHECKS PASSED
```

`W=4` 反例只针对“约化成 (L=1) 后，裸零曲率自动等价完整 SD”这一过度推论。
它不否定非退化 (W-4) 分支上的谱表示，也不否定整体可积性。
