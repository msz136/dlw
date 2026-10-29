# DLW Miwa and unified Gram presentation revision

Base: `1fff1d2c8d439c91195fca4f744eb8e173179b54` (2026-10-29).

Section 2.2 now follows the three tau products through explicit F/G shifts, common-centre Hirota exponentials, and homogeneous cancellation before deriving the bilinear relation. It then gives the common lattice with free b, a unified Gram family, the adjacent-layer lemma with its complete rank-one-update proof, and the proof of the two pairings.

Section 2.3 specializes b=a and b=a+h/2 to Endpoint-SD and Centered-SD, respectively, with their explicit determinant formulas, placements, consistency arguments, and positivity class. Former Section 2.4 is absorbed. HTML navigation and the section overview are synchronized. Main equations are numbered (1)–(133); main-text and appendix references follow their original mathematical targets.

Proof source: `Workspaces/dlw_paper_20261009/manuscript.md`, Appendix B, and the adjacent-layer lemma in its Section 2.3. The older rank-one calculation and scalar elimination are retained. Notation is adapted to the current lattice by p_i=z_i+b, q_j=w_j-b and the inverse auxiliary layer ell=-1. For the current arbitrary constant matrix C, the singular-matrix continuation uses C+epsilon I instead of scaling amplitudes from an identity background. The new proof replaces the recent proof by coefficient extraction from the fully discrete Gram family.

Verification: exact coefficient algebra and adjacent-layer elimination; exact N=2 tests with non-diagonal C at multiple lattice sites; identical common numbered formulas in HTML/TeX; unchanged Section 3 onward apart from references. Section 2.2–2.3 compiled twice and all six local validation pages were inspected. Local preview uses Liberation Serif because Times New Roman is unavailable; the committed TeX font setting remains unchanged. The full-paper PDF was not rebuilt. Exact small-N tests supplement, rather than replace, the arbitrary-N proof. See `validation_final.json`.
