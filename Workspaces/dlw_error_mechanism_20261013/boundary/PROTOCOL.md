# Follow-up prediction: moving the lower y reconstruction boundary

Frozen before running the new trajectories, 2026-10-13.

The independently computed source budget predicts that extending the A y
domain from yhalf=10 to 20, with all other settings unchanged, changes the
initial u error source by a vector constant in y on the common observation
window. The initial v source is unchanged to rounding. This reflects the
prescribed lower trace used in cumulative y reconstruction. It does not
predict that the evolved difference remains exactly constant in y.

Run the original SD/PE and FD models from the common continuous physical
initial condition: h=dx=.1, Lx=20, T=.01, RK4 dt=.0001, unchanged original
closures. The only intervention is yhalf=20. Compare to the archived original
yhalf=10 trajectories on exactly the same native observation grid
|x|<=5 and |y|<5 (100 by 101). No interpolation, fitted terminal data, or
replacement observation window is permitted.

At all 21 archived times, report the new and original physical-field RMS,
the norm of their signed error difference relative to the original error,
and the orthogonal projection of that difference onto fields constant in y:

    fraction = mean_x(mean_y(delta_error)^2) / mean_xy(delta_error^2).

This is a squared-norm explanatory fraction, not the ratio of amplitudes.
Verify identical x/y/t coordinates and identical exact references before
comparing. Record roundoff-level initial mismatch separately. The result
tests the propagation of an already identified closure-related source and
does not isolate a general treatment called integrability.
