"""Diagnose the moving-mesh result against the frozen and uniform members."""
import sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
sys.path.insert(0, str(PROJECT / 'spatial_audit_20261023'))
from run import Model

m = Model('A', 'Centered-SD', .1, .1)
mv = np.load(HERE / 'A_moving_0.0001_spectral.npz')
fr = np.load(HERE / 'A_frozen_0.0001_spectral.npz')
un = np.load(HERE / 'A_uniform_0.0001_spectral.npz')

du = mv['u'] - fr['u']
print('moving-free u: max %.3e at y=%.3f x=%.3f' % (abs(du).max(), m.y[np.unravel_index(abs(du).argmax(), du.shape)[0]], mv['x'][np.unravel_index(abs(du).argmax(), du.shape)[1]]))
print('frozen-uniform u: max %.3e' % abs(fr['u'] - un['u']).max())
print('moving error at T:', mv['v'].shape)

# velocity at the terminal state
grid_x, spacing = mv['x'], mv['spacing']
u, w = mv['z']
h = m.h
def d1(f):
    k = 2 * np.pi * np.fft.rfftfreq(len(grid_x), m.dx if False else (grid_x[-1] - grid_x[0] + spacing[-1]) / len(grid_x))
    return np.fft.irfft(np.fft.rfft(f, axis=-1) * (1j * k), n=len(grid_x), axis=-1)
L = 2 * m.half
xi = mv['xi']; s = grid_x - xi
dk = 2 * np.pi * np.fft.rfftfreq(len(xi), L / len(xi))
m1 = 1j * dk; m1[-1] = 0
dxi = lambda f: np.fft.irfft(np.fft.rfft(f, axis=-1) * m1, n=len(xi), axis=-1)
J = 1 + dxi(s)
D1 = lambda f: dxi(f) / J
rho = 1 - w / 4
rhobar = rho.mean(axis=0)
qbar = ((u + 2 * m.a) * rho - D1(rho) - 2 * m.a).mean(axis=0)
V = (qbar - qbar[0]) / rhobar
print('J range %.6f %.6f ; spacing range %.5f %.5f' % (J.min(), J.max(), spacing.min(), spacing.max()))
print('V range %.4e %.4e' % (V.min(), V.max()))
spec = np.abs(np.fft.rfft(V))
print('V spectrum: low %.3e high %.3e ratio %.3e' % (spec[:5].max(), spec[-20:].max(), spec[-20:].max() / spec.max()))
# location of the u-error maximum for both runs
for name, arr in (('uniform', un), ('frozen', fr), ('moving', mv)):
    e = np.abs(arr['u'] - arr['u_exact'])
    i, j = np.unravel_index(e.argmax(), e.shape)
    print('%-8s max u error %.3e at y=%.2f x=%.3f  (x0=%.3f)' % (name, e.max(), arr['y'][i], arr['x'][j], arr['x0'][j]))
