"""Which direction limits the fixed-grid Centered-SD error? Fourier x, same y closure."""
import sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
sys.path.insert(0, str(PROJECT / 'spatial_audit_20261023'))
import run as audit

audit.HALF_WIDTHS = audit.HALF_WIDTHS
DT, TEND = 1e-4, 0.01


def measure(m, z, t=TEND):
    errs = []
    for j, yy in enumerate((m.y, m.yv)):
        mask = abs(yy) < audit.HALF_WIDTHS[m.case]
        xx = abs(m.x) <= audit.HALF_WIDTHS[m.case]
        num = z[j][mask][:, xx]
        ref = m.profile(yy[mask], t, m.x[xx])[j]
        errs.append(float(abs(num - ref).max()))
    return errs


for case in ('A', 'D'):
    for dx, h in ((.1, .1), (.1, .05), (.05, .1), (.05, .05)):
        m = audit.Model(case, 'Centered-SD', dx, h)
        z = m.initial()
        with np.errstate(over='ignore', invalid='ignore'):
            for i in range(round(TEND / DT)):
                z = audit.step(m, i * DT, z, DT)
        print(case, 'dx=%.2f h=%.2f nx=%d ny=%d  Eu=%.4e Ev=%.4e' % (dx, h, m.nx, len(m.y), *measure(m, z)), flush=True)
