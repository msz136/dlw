"""Exact linear finite-h constant-background controls, using actual native sites."""
from pathlib import Path
import csv
import json
import numpy as np

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[1] / 'perturbation_pilot/four_case_kappa_pi_over_2'
T = .01
rows = []
for case in ['A', 'D', 'Gaussian', 'Sinusoidal']:
    z = np.load(BASE / (case + '.npz'))
    x, y, yv = z['x'], z['y'], z['yv']
    rec = json.loads((BASE / (case + '.json')).read_text())
    h, dx = rec['h'], rec['dx']
    if case in ['A', 'D']:
        R = 5 if case == 'A' else 30
        mx, mu, mv = abs(x) <= R, abs(y) < R, abs(yv) < R
    else:
        mx = np.ones_like(x, dtype=bool)
        mu, mv = abs(y) <= 1.8 + 1e-12, abs(yv) <= 1.8 + 1e-12
    phi = np.sin(np.pi*(y-y[0])/(y[-1]-y[0]))**2
    phi[0] = phi[-1] = 0
    phiv = np.sin(np.pi*(yv-y[0])/(y[-1]-y[0]))**2
    dphi = np.diff(phi)/h
    iphi = np.r_[0, h*np.cumsum(phiv)]
    for kfactor in [1, 2, 4]:
        kappa = np.pi/2*kfactor
        theta = kappa*kappa*T
        C, S = np.cosh(theta), np.sinh(theta)
        phase = np.cos(kappa*(x-4*T))
        native_factor = float(abs(phase[mx]).max())
        for component in ['u', 'v']:
            if component == 'u':
                up, vp = C*phi, S*dphi
                g2 = np.sqrt(C*C + S*S*np.sum(dphi[mv]**2)/np.sum(phi[mu]**2))
            else:
                up, vp = S*iphi, C*phiv
                g2 = np.sqrt(C*C + S*S*np.sum(iphi[mu]**2)/np.sum(phiv[mv]**2))
            rows.append(dict(case=case,component=component,kappa_factor_of_pi_over_2=kfactor,
                kappa=float(kappa),T=T,theta=float(theta),cosh=float(C),sinh=float(S),
                native_x_peak_factor=native_factor,
                terminal_u_over_epsilon=float(abs(up[mu]).max()*native_factor),
                terminal_v_over_epsilon=float(abs(vp[mv]).max()*native_factor),
                pair_L2_gain=float(g2)))

for case, expected in [('A', .222478086), ('D', .971576991)]:
    r = next(x for x in rows if x['case']==case and x['component']=='v' and x['kappa_factor_of_pi_over_2']==1)
    assert abs(r['terminal_u_over_epsilon'] - expected) < 1e-9
out = dict(scope='Exact constant-(u,v)=(0,4) semidiscrete linearized response; native x maxima and continuous-time Fourier phase; no PDE error certificate',
           h=.1,dx=.1,rows=rows)
(HERE/'constant_response.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
with (HERE/'constant_response.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print(json.dumps(rows,indent=2))
