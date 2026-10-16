# Follow-up prediction: remove the helpful x-error cancellation in C

This is an explicitly adaptive follow-up, frozen AFTER the initial source
decomposition and BEFORE its evolution experiment. It is not part of the
original preregistered comparison.

Source data at t=0 show that C's PE u y-model source is larger than FD's, but
points partly against the much larger x-stencil source. At fixed h=.1, reducing
dx reduces the x-stencil source and therefore removes this helpful cancellation.
The independent dx source scan already includes .025. The prediction is that
the actual PE/FD u-error ranking reverses at dx=.025.

Run the original C computational domain (L=80,yhalf=40) and observation window
(|x|<=30, |y|<30), h=.1, T=.001, RK4 dt=.000025. Compare pure PE and FD at
dx=.025, and use the original archived dx=.1 trajectory at t=.001 as baseline.
Use this short T to stay away from the large high-frequency amplification that
can compromise fine-grid long-time results. Do not infer long-time performance.
Repeat the refined PE case with dt=.0000125 as a targeted temporal check.

Prediction outcome is the direction of the u RMS ranking (PE worse at refined
dx), not a fitted numerical coefficient. Separately compare e(T)/T against the
independently derived initial source, reporting its vector discrepancy and
correlation. A failure is to be retained and reported, not followed by a search
for a favorable grid or time.
