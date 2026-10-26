"""Rigorous sampled-boundary comparison with an EXACT nonlinear DLW trace.

Arb interval arithmetic verifies explicit rational error brackets. This is a
certificate at the lower boundary only, conditional on a sufficiently regular
continuous solution having that trace; it is NOT a full-domain error upper bound.
"""
from pathlib import Path
import json
import numpy as np
from flint import arb,ctx
HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'spatial_audit_20261023'
ctx.dps=100
pi=arb.pi();t=arb(1)/100;omega=pi/12

def rational_float(f):
    n,d=float(f).as_integer_ratio()
    return arb(n)/d

def exact_v(x):
    return arb(3)/100*pi/4*(omega*(x-4*t)).cos()*(omega*omega*t).sinh()

rows=[]
for tag,low,high in [('ref4','4.2267e-8','4.2270e-8'),('ref8','4.2267e-8','4.2269e-8')]:
    z=np.load(OLD/f'Sinusoidal_FD_short_a2_{tag}.npz')
    errors=[abs(rational_float(v)-exact_v(rational_float(x))) for x,v in zip(z['x'],z['z'][1,0])]
    # All nodes below upper; at least one above lower. Arb comparisons must be
    # determinate and true, not merely overlapping intervals.
    assert all(e<arb(high) for e in errors)
    assert any(e>arb(low) for e in errors)
    rows.append(dict(candidate=tag,scope='max over stored lower-boundary x nodes',
                     rigorous_lower=low,rigorous_upper=high,verified=True,
                     target_upper_1e_10_rejected=True))

lines=(HERE/'Sinusoidal_precision80_dx0.05_dt0.0001.txt').read_text().splitlines()
vals=lines[41*480:41*480+480]
errors=[abs(arb(s)-exact_v(arb(j)/20)) for j,s in enumerate(vals)]
low,high='4.5381e-8','4.5383e-8'
assert all(e<arb(high) for e in errors) and any(e>arb(low) for e in errors)
rows.append(dict(candidate='80 digits, h=.1 dx=.05',scope='max over stored lower-boundary x nodes',
                 rigorous_lower=low,rigorous_upper=high,verified=True))

# A separately defined trace candidate: exact formula rounded to 70 decimal
# significant digits. Verify a small numerical representation error on all nodes.
rounded=[]
for j in range(480):
    x=arb(j)/20
    exact=exact_v(x)
    val=exact.mid().str(70,radius=False)
    rounded.append(val)
    assert abs(arb(val)-exact)<arb('1e-72')
(HERE/'exact_sinusoidal_boundary_T001.txt').write_text('\n'.join(rounded),encoding='utf8')
result=dict(formula='v(x,-2,t)=(.03*pi/4)*cos((pi/12)*(x-4*t))*sinh((pi/12)^2*t)',
    interpretation='exact boundary trace of the full nonlinear PDE; not linearized approximation',
    candidates=rows,exact_trace_representation_error_upper='1e-72',
    trace_representation_scope='480 points x=j/20, t=.01; rounded analytic trace only',
    full_domain_upper=None,continuum_reference_certified=False)
(HERE/'boundary_certificate.json').write_text(json.dumps(result,indent=2),encoding='utf8')
print(json.dumps(result,indent=2))
