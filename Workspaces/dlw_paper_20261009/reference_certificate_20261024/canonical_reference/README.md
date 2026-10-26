# Canonical nonlinear continuum-reference candidates

Date: 2026-10-24. Numerical candidates and diagnostics only. **No proven error bound to an infinite-dimensional continuous DLW solution is supplied by these files: eta_u=null, eta_v=null.** The candidates are materially different from the earlier FD reference with frozen/extrapolated ghost values.

## Exact problem being approximated

Use a=2, x-period 192, -2 <= y <= 2, u(x,-2,t)=0, T=.01. Define e(y)=sin(pi(y+2)/4). The approved Gaussian is the smooth periodic sum G(x)=sum_m exp(-((x+192m)/6)^2), with u0=.05 e G and v0=.03 e G. Sinusoidal data are u0=.03 e cos(pi*x/12), v0=.02 e sin(pi*x/12). The latter have exact period 24; the candidate is computed on that invariant periodic subspace and repeated eight times to period 192. This does not assume uniqueness of the unresolved continuum problem.

The exact nonlinear integral formulation is

    w = v-u_y,
    u_t = -u_xx - (u^2/2+4u)_x - integral_{-2}^y w_xx ds,
    w_t = w_xx - ((u+4)w-4u)_x,
    v = u_y+w.

There is no upper-y ghost, no imposed upper-y value, and no frozen lower w. The lower u is zero; lower w follows its heat-advection equation. Initial w is the prescribed v0 minus the analytical derivative (u0)_y.

## Discretization and output

`solve.py`: Fourier-Galerkin |n|<=M, with quadratic products exactly dealiased by padding to 3M+1 nodes. This finite Fourier projection is explicit, not hidden filtering. Gaussian Fourier coefficients are initialized analytically as 6 sqrt(pi)/192 exp(-9 xi_n^2); sine/cosine modes are initialized exactly up to binary evaluation of amplitudes. The y degree is 16 or 24 on Chebyshev-Lobatto nodes. Integration and differentiation matrices act on that interpolating polynomial. Time integration is RK4. All calculations here use float64.

Each `.npz` contains 11 trajectory snapshots of Fourier coefficients for u,w, y Chebyshev nodes, Fourier indices, final physical u,v on a common 768-by-161 comparison grid (including both y boundaries), and the corresponding coordinates. The coefficients also permit evaluation at arbitrary physical x,y points; the final comparison grid is not the definition of the reference function. All sample differences below are on this grid.

Selected candidate files:

- `Sinusoidal_M32_Y24_dt5.0e-05.npz`
- `Gaussian_M128_Y24_dt5.0e-05.npz`

`validate.py` compares x/y/time refinement, an independent DOP853 time solve, and the physical continuous PDE residual of a cubic-Hermite interpolation of the stored trajectory. Residuals are sampled, not enclosed over the entire space-time cylinder.

`evaluate.py` supplies `evaluate(case,x,y,t=.01)`, returning an array of shape (2,len(y),len(x)) for physical u,v. It evaluates the Fourier/Chebyshev expansions at arbitrary x,y and uses the stored state at each saved time. Intermediate times use cubic-Hermite interpolation; x is periodic, -2<=y<=2 and 0<=t<=.01. The evaluator also carries no error guarantee.

## Results

At T=.01, maxima of absolute values are approximately

| Case | max abs(u) | max abs(v) |
|---|---:|---:|
| Sinusoidal | .0299998967991888 | .0196873401686598 |
| Periodic Gaussian | .0500189675563063 | .0300031144031902 |

The x-cutoff refinements after the apparent resolved range change both fields by <=1.4e-17. Raising y degree 16 to 24 changes u by <=7.7e-17 and v by <=1.6e-15. Halving dt from 1e-4 to 5e-5 changes u by <=4.9e-17 and v by <=3.2e-16. DOP853 at rtol1e-13, atol1e-16 differs by <=3.9e-17 in u and <=2.3e-16 in v. These are observed agreements at float64 precision, **not convergence bounds**.

The exact nonlinear boundary traces p=u_y and b=v from `../BOUNDARY_THEOREM.md` agree with the selected candidates to approximately 9.2e-16 (sinusoid) and 1.3e-15 (Gaussian). This checks the continuum boundary formulation independently of the interior evolution.

Sampled physical residual maxima over 30 interior times are (r1,r2)=(3.34e-13,1.44e-12) for sine and (7.13e-13,3.29e-12) for Gaussian. These include the full physical equations evaluated on the approximate trajectory, not only the projected ODE residual. They still are not uniform residual enclosures. No infinite-frequency stability estimate or existence/uniqueness certificate follows from this diagnostic.

## Reproduce

    python solve.py Sinusoidal 32 24 .00005
    python solve.py Gaussian 128 24 .00005
    python validate.py

All other resolution arguments are recorded in `validation.json` and each individual JSON. No manuscript data or old reference files were overwritten.
