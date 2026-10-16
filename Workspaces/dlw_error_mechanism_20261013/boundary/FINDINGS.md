# y-domain intervention: a large change of the u error field with almost unchanged RMS

The preregistered follow-up used the original A solver, h=dx=.1,
RK4 dt=.0001 and T=.01. The only changed configuration entry was yhalf,
from 10 to 20. This expands both y endpoints, moving the prescribed lower
trace used to reconstruct u. Lx=20 and the physical observation window
|x|<=5, |y|<5 were held fixed. The 100 by 101 target grid, all 21 times,
and all exact reference values are bitwise identical to the archived run.
Initial field errors remain below 2.5e-15.

## Terminal measurements

| Method | Field | Original RMS | Expanded-y RMS | Difference RMS / original RMS | y-constant squared fraction of difference |
|---|---|---:|---:|---:|---:|
| PE/SD | u | 1.45979634e-4 | 1.44779200e-4 | 0.986099 | 0.998806 |
| FD | u | 9.97199227e-5 | 9.95272453e-5 | 0.991185 | 0.998093 |
| PE/SD | v | 3.21963199e-4 | 3.21810390e-4 | 0.037137 | 0.997491 |
| FD | v | 2.85695125e-4 | 2.85558066e-4 | 0.030987 | 0.997152 |

For delta_error = new_error - archived_error, the last column is exactly

    mean_x(mean_y(delta_error)^2) / mean_xy(delta_error^2).

This is the orthogonal projection onto fields independent of y, replicated
over all y rows. It measures the fraction of squared difference explained
by vertical x-dependent bands; it is not a fraction of the entire original
error and is not an additive source share.

## Interpretation

1. The independent initial-source calculation predicted a y-independent
   change of the u defect when the y reconstruction boundary moves. The
   actual full evolution verifies that directional prediction: more than
   99.8% of the u difference energy remains in that subspace at T=.01.
   Exact constancy is not claimed; the remaining u RMS is 4.98e-6 for SD
   and 4.32e-6 for FD.
2. The u difference is as large as almost the entire original error norm,
   even though the total RMS changes by less than 1%. Thus a norm-only
   buffer check would miss a major change of error location and pattern.
   Expansion does not significantly improve this A error norm.
3. The initial v source is unchanged in the common interior, while a small
   v difference develops during evolution (3.1% to 3.7% of the old error).
   It is also predominantly y-constant. The evolving coupling and closures
   must be retained in any detailed propagation explanation.
4. The controlled outcome concerns the actual y-domain/closure intervention.
   Expanding yhalf moves both endpoints; the full-time outcome is not an
   experiment changing only the lower boundary, and it does not prove all
   observed vertical bands have a single source. The source identity
   specifically locates its initial u contribution in cumulative recovery
   from the prescribed lower trace.
5. These outcomes apply to A at the stated short time. They do not establish
   an abstract accuracy benefit or penalty of integrability.

## Reproduction and retained data

Run `python boundary_followup.py --kind SD` and `--kind FD`.
The protocol was saved before either run. Separate validation JSON records
contain input hashes, exact grid/reference equality and initial errors.
Each NPZ retains all 21 physical field snapshots, exact references and
signed differences; CSVs contain all measured norm/projection time series.
