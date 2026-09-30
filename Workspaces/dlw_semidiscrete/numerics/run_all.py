# -*- coding: utf-8 -*-
"""Run every DLW semi-discrete numerical experiment in order and collect the
JSON artifacts into out/.

Usage:  python -u run_all.py [e0 e1 e2 ...]
        (no arguments = run all)
"""

import sys, os, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
EXPDIR = os.path.join(HERE, "experiments")
EXPS = [
    ("e0", "e0_benchmark.py", "exact bilinear residual benchmark"),
    ("e1", "e1_continuum.py", "continuum-limit order test"),
    ("n1n2", "verify_n1n2.py", "exact Gram fields satisfy (N1)(N2)"),
    ("space", "space_error.py", "pure spatial RHS error order"),
    ("e6", "e6_growth.py", "high-wavenumber growth (report eq. (S))"),
    ("e2e3", "e2_e3_solver.py", "time integration, time/space order"),
    ("e2e3time", "e2_e3_self_convergence.py", "same-grid Euler/RK4/trapezoid time self-convergence"),
    ("e4", "e4_twosoliton.py", "two-soliton phase shift"),
    ("e5", "e5_conservation.py", "local conservation balance"),
    ("e7", "e7_fd_baseline.py", "conventional FD baseline"),
    ("dynamics", "dynamics_study.py", "matched dynamics, model comparison and trajectory sensitivity"),
    ("controls", "dynamics_controls.py", "common early-time error decomposition"),
    ("cost", "dynamics_cost.py", "sequential repeated timing comparison"),
    ("dynamicsreport", "dynamics_report.py", "research narrative and figures from measurements"),
]
want = [a.lower() for a in sys.argv[1:]]
fail = []
for key, script, desc in EXPS:
    if want and key not in want:
        continue
    path = os.path.join(EXPDIR, script)
    print("=" * 78)
    print(f"RUN  {key:6s}  {desc}")
    print(f"     experiments/{script}")
    print("=" * 78)
    t0 = time.time()
    r = subprocess.run([sys.executable, "-u", path], cwd=EXPDIR)
    dt = time.time() - t0
    status = "ok" if r.returncode == 0 else f"FAILED (exit {r.returncode})"
    print(f"--- {key}: {status}   ({dt:.1f}s)\n")
    if r.returncode != 0:
        fail.append(key)

print("=" * 78)
if fail:
    print(f"FAILED: {', '.join(fail)}")
    sys.exit(1)
print("all experiments completed")
