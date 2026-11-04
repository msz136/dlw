# DLW reader revision, 2026-11-04

Revised `dlw-paper.html` and `pdf/dlw/main.tex` together.

- Miwa: keep the successive limits, identify auxiliary layer n and physical lattice k before the shift equations, and introduce the rational factor from the continuous transverse exponential.
- Gram: apply Chen et al., arXiv:1709.03781, Lemma 2.1. Appendix A gives the spectral and auxiliary-variable correspondence and the continuous-layer amplitude map. Apply the adjacent-layer identity at sigma=b and b-h; explain the latter as the g_(k-1) pairing.
- Lax: use component operators L and M with existing logarithmic ratios r and q. Expand S_k, Y, A_k and C_k. Explain the Darboux seeds, common transformed time operator, and preservation of L psi=0. Appendix C records the expanded component calculation.
- Renumber equations and references consistently. Numerical text, figures, tables, algorithms, supplementary experiments and 2HS remain unchanged, apart from equation-reference renumbering in DLW.

Verification: `verify.py` compares all numbered HTML/TeX equations and checks exact rational Gram residuals for both pairings on a 2x2 full constant matrix with endpoint, centered and another b value. It symbolically checks the Lax component product rule and its cancellation. `verification.json` records results. `mapping.json` maps previous equation numbers to the new sequence.

The manuscript cites the standard Gram identity; the finite rational checks supplement the parameter correspondence. No numerical experiments were rerun.
