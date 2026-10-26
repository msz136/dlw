"""Outward upper arithmetic for a CONDITIONAL scalar a-posteriori bound.

Inputs must already be proved bounds in one common norm. This module cannot
certify a PDE, a residual enclosure, floating-point solver, or omitted modes.
Decimal.exp is correctly rounded; next_plus supplies a strict upper bound.
"""
from decimal import Decimal, localcontext, ROUND_CEILING, ROUND_FLOOR
import json

def upper_bound(*, initial, residual, linear, quadratic, radius, T, discrepancy, fraction='0.01'):
    with localcontext() as ctx:
        ctx.prec = 80
        ctx.rounding = ROUND_CEILING
        e0, rho, L, B, R, t, D, f = map(Decimal,
            (initial,residual,linear,quadratic,radius,T,discrepancy,fraction))
        if min(e0,rho,L,B,t,D) < 0 or R <= 0 or not (0 < f < 1):
            raise ValueError('Use nonnegative bounds, positive radius, 0<fraction<1.')
        exponent = (L+B*R)*t
        eta = (e0+t*rho)*exponent.exp().next_plus()
        with localcontext() as lower:
            lower.rounding = ROUND_FLOOR
            budget = f*D
            lo = max(Decimal(0), D-eta)
        return dict(eta_upper=str(eta), bootstrap_closes=eta<R,
            relative_budget_met=eta<=budget, radius=str(R),
            error_interval=[str(lo),str(D+eta)], continuum_certified=False,
            status='conditional arithmetic only; analytic/enclosure hypotheses not verified')

if __name__ == '__main__':
    # Arithmetic test, explicitly not DLW evidence.
    r=upper_bound(initial='1e-14',residual='1e-12',linear='1',quadratic='1',
        radius='1e-10',T='.01',discrepancy='1e-8')
    assert r['bootstrap_closes'] and r['relative_budget_met']
    assert not r['continuum_certified']
    print(json.dumps(dict(arithmetic_test_only=r),indent=2))
