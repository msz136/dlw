from pathlib import Path
root=Path(__file__).resolve().parents[2]/'Workspaces/dlw_semidiscrete/numerics'
def edit(name,fn):
    p=root/name;p.write_text(fn(p.read_text(encoding='utf-8')),encoding='utf-8')
def e1(s):
    a=s.index('       "l2_definition":'); b=s.index('       "y_window":',a)
    s=s[:a]+'       "l2_definition": "sqrt(dx * h * weighted_sum): trapezoid x endpoints, midpoint y",\n'+s[b:]
    a=s.index('    """E_inf and');b=s.index('\n\n# ---',a)
    s=s[:a]+'''    """Finite x interval: trapezoid endpoints; midpoint lattice y weights."""
    weights = np.ones(len(xs)); weights[[0,-1]] = .5
    dx = xs[1]-xs[0]
    return (np.max(np.abs(eu)), np.max(np.abs(ev)),
            np.sqrt(dx*h*np.sum(weights*eu**2)),
            np.sqrt(dx*h*np.sum(weights*ev**2)))
'''+s[b:];return s
edit('experiments/e1_continuum.py',e1)
def e5(s):
    a=s.index('def integrate_full(');b=s.index('print(f"    grid',a)
    s=s[:a]+s[b:]
    s=s.replace('k = MID - (J_L + 1)', 'k = MID - J_L')
    s=s.replace('# index of site MID inside P\'s range','# index in u and W (both start at J_L)')
    s=s.replace('np.array([rhs.b_fun(t)])','rhs.b_fun(t)')
    s=s.replace('    Pout, Wout, info = integrate(rhs,', '    rec(0.0, P0, W0)\n    Pout, Wout, info = integrate(rhs,')
    s=s.replace('    return cap, info, Pout','    assert info["stopped"] is None and abs(info["final_t"]-T)<1e-12\n    assert np.all(np.isfinite(Pout)) and np.all(np.isfinite(Wout))\n    return cap, info, Pout')
    s=s.replace('np.trapezoid(c[2], Xg.x)','Xg.dx*np.sum(c[2])').replace('np.trapezoid(c[3], Xg.x)','Xg.dx*np.sum(c[3])')
    s=s.replace('"site": int(MID),','"site": int(MID), "initial_t": cap[0][0], "final_t": info["final_t"],\n         "stopped": info["stopped"], "quadrature": "periodic dx sum",')
    s=s.replace('    These drifts include the effect of the open-chain boundary fluxes,','    These are periodic x-integrals at a fixed interior lattice site,').replace('    so they are NOT pure invariant errors; they are reported as measured.','    measured from t=0; conservation alone does not establish solution accuracy.')
    return s
edit('experiments/e5_conservation.py',e5)
def e23(s):
    a=s.index('def gmax_discrete(');b=s.index('\n\ndef budget(',a)
    s=s[:a]+'''from functools import lru_cache
from linearized import spectral_max

@lru_cache(None)
def gmax_discrete(nx, h=1/4, Lg=L):
    """Zero-background fixed-boundary open-chain spectral abscissa."""
    return spectral_max(nx,Lg,h,J_L,J_R)["g_max_discrete"]
'''+s[b:]
    s=s.replace('actual discrete-operator spectrum','zero-background open-chain modal spectrum')
    s=s.replace('window chosen from BOTH budgets','heuristic modal time scales (not nonlinear stability bounds) from BOTH budgets')
    return s
edit('experiments/e2_e3_solver.py',e23)
