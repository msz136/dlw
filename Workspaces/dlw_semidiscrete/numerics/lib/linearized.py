"""Zero-background linearisation with fixed zero base, ghosts and outer P.

Periodic fourth-order x stencil; finite open j chain. Spectral abscissae
are modal growth rates, not norm bounds for nonnormal or nonlinear flows.
"""
import numpy as np


def effective_k(theta, dx):
    return (8*np.sin(theta*dx)-np.sin(2*theta*dx))/(6*dx)


def open_block(k, jL=-12, jR=12, h=.25, a=4.):
    n = jR-jL+1
    R = np.zeros((n, n-1))
    for i in range(1, n):
        R[i, :i] = h
    B = np.zeros((n, n))
    for i in range(n):
        if i+1 < n: B[i, i+1] = 1/(2*h)
        if i > 0: B[i, i-1] = -1/(2*h)
    D = (np.eye(n)[1:]-np.eye(n)[:-1])/h
    M = (np.eye(n)[1:]+np.eye(n)[:-1])/2
    Lap = (-2*np.eye(n-1)+np.eye(n-1,k=1)+np.eye(n-1,k=-1))/h**2
    return np.block([
        [-2j*a*k*D@R+k*k*(M@B@R-h*h*Lap/4),
         1j*k*h*h*D/4+k*k*M],
        [4j*k*R, (-2j*a*k-k*k)*np.eye(n)]])


def spectral_max(nx, L=60., h=.25, jL=-12, jR=12):
    # Negative modes are conjugates, so the half spectrum suffices.
    theta = 2*np.pi*np.arange(nx//2+1)/L
    ks = effective_k(theta, L/nx)
    blocks = [open_block(k,jL,jR,h) for k in ks]
    rates = [float(np.linalg.eigvals(B).real.max()) for B in blocks]
    # A separate Euclidean logarithmic norm controls transient growth of the
    # linear system even when eigenvectors are badly conditioned.
    mu = max(float(np.linalg.eigvalsh((B+B.conj().T)/2).max()) for B in blocks)
    idx = int(np.argmax(rates))
    return {'g_max_discrete': rates[idx], 'mode':idx,
            'k_at_gmax':float(ks[idx]), 'max_Keff':float(max(abs(ks))),
            'linear_log_norm':mu}
