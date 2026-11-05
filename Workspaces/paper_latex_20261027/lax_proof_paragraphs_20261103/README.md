# DLW Lax presentation, main proof, and semantic paragraphs, 2026-11-03

Current outputs are `C:/Users/msz/aca/dlw-paper.html`, `C:/Users/msz/aca/pdf/dlw/main.tex`, and `C:/Users/msz/aca/pdf/dlw/main.pdf`.

## Literature consulted

- Feng, Maruno and Ohta, *Self-adaptive moving mesh schemes for short pulse type equations and their Lax pairs* (2014). The Method 2 discussion, equations (32)–(36), directly presents the semi-discrete linear problem and its matrices, then explains how compatibility yields the nonlinear system. This supplied an example of a compact, equation-led presentation. https://link.springer.com/article/10.1186/s40736-014-0008-7
- Riaz and Hassan, *Integrable semi-discretization of complex and multi-component coupled dispersionless systems and their solutions* (2019 preprint). Section 2 proceeds from the differential-difference linear problem to the zero-curvature condition and then its component equations. This supported keeping the link to nonlinear dynamics visible. https://arxiv.org/html/1901.05185
- Nijhoff, *Lagrangian 3-form structure for the Darboux system and the KP hierarchy* (2023). Proposition 2.1 and its proof show the cross-differentiation and coefficient comparison in the main text. This supplied a model for retaining the essential compatibility calculation with the result. https://link.springer.com/article/10.1007/s11005-023-01641-7

These sources guided the organization. The DLW identities and proof were derived from the existing manuscript and independently checked. The paper's bibliography entries were preserved.

## Implemented changes

Proposition 3.3 now consists of a short introduction and the two commutator identities (67)–(68). Positivity, smoothness, and the centered lower-trace assumptions appear before the explicit operators. The corresponding linear problems are stated in prose after the proposition.

The main proof restores the common coefficients/operators (69)–(70), the three scalar compatibility relations (71)–(73), the common commutator identity (74), and the endpoint/centered field recovery formulas (75)–(77). It explains coefficient cancellation, preservation of the linear constraint, and recovery of both nonlinear systems. Appendix C now contains the full product-rule expansion and intermediate reconstruction substitutions, followed by the continuum expansions. Repeated explanatory material was condensed.

Paragraph grouping was reviewed by logical stage. New constructions, successive limit steps, new components of proofs, and changes of numerical methods start paragraphs. Definitions, explanations of displayed formulas, and continuing algebra remain in their paragraphs. The selected boundary changes are recorded in `paragraphs.py` and the edit manifest. HTML mirrors these changes. The article's normal 15pt paragraph indentation is retained. A local space reservation keeps the conditions and both continuous-limit systems in Proposition 3.4 together.

Reference-list item spacing was tightened from 3pt to 1.5pt to eliminate a final page containing one bibliography item. This was the only bibliography change. The HTML print rule was adjusted accordingly.

## Verification and final pagination

The final PDF has 40 pages. The explicit operators and Proposition 3.3 are on page 11, its main proof is on page 12, and Proposition 3.4's two continuous-limit systems are together on page 13. Figures 1–2 share page 19 with a full preceding text page. There are 101 main equation numbers, 122 equation numbers including appendices, five unnumbered displays, and 122 rendered display blocks because of the multi-tag align groups.

`validation.json` records preservation of prior mathematics after relocation/renumbering, equivalence of the common commutator form, an independent symbolic verification of the full differential-difference operator expansion and coefficient cancellations, matching HTML/TeX prose and math, unchanged table data/figure/2HS hashes, no compilation issues and no off-page text. `html_validation.json` checks all displays, four aligned groups, 14 loaded figures, and absence of overflow or rendering errors. Full contact sheets and the edited mathematical pages were visually inspected.

Incoming files are in `before/`. `edit.py` replays that snapshot and must not overwrite subsequent edits. Synchronization tools must support native multi-tag `align*` environments. Routine compilation remains `pdf/build.ps1 -Paper dlw`.
