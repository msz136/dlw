# Introduction revision — 2026-10-19

Scope: English-first expansion of the main Draft introduction; Chinese translation follows its argument. Abstracts, Sections 2–4, appendices, formulas and numerical results are retained. Bibliography grows from 10 to 16 entries; existing reference numbers remain stable.

## Evidence and use

| Source | Evidence inspected | Use in introduction |
| --- | --- | --- |
| [1] Boiti–Leon–Pempinelli (1987), https://doi.org/10.1088/0266-5611/3/3/007 | Publisher abstract reproduced at https://inspirehep.net/literature/21032; publisher fetch unavailable | Spectral origin, Bäcklund transformation and superposition; no unverified physical derivation attributed to the original paper. |
| [2] Wang–Zhou–Li (1998), https://arxiv.org/abs/math/9804162 | Author preprint record | Nonlinear transformation approach. |
| [3] Sun et al. (2010), https://epubs.siam.org/doi/10.1137/090774847 | Publisher search record/abstract | Bilinear auto-Bäcklund transformation and generalized Bell polynomials. |
| [4] Hu–Xu–Yu (2016), https://www.sciencedirect.com/science/article/pii/S0893965916301975 | Publisher abstract | Grammian/Wronskian solutions, Sato/Hirota framework, Boussinesq–Burgers reduction. |
| [5] Sheng–Yu (2022), https://www.sciencedirect.com/science/article/abs/pii/S0167278921002773 | Indexed publisher abstract and excerpts; direct fetch blocked; checked against manuscript Section 2 | Continuous determinant starting point and wave families; connection to sinh-Gordon kept qualitative. |
| [6] Hu–Yu (2007), https://doi.org/10.1088/1751-8113/40/42/S10 | Existing bibliography; author-uploaded abstract and cross-reference in https://link.springer.com/article/10.1007/s44198-023-00147-z; direct publisher fetch failed | Existing sinh-Gordon discretizations; no new detailed equivalence claim. |
| [7] Zhang et al. (2015), https://arxiv.org/abs/1411.0476 | Author preprint abstract | Compatibility-based bilinear discretization, Lax pairs and continuum limits. |
| [8] Yu–Xu (2015), https://doi.org/10.1103/PhysRevE.91.062902 | Publisher abstract | Neighboring multidimensional differential-difference construction. |
| [9] Feng–Sheng–Yu (2023), https://link.springer.com/article/10.1007/s11075-023-01504-1 | Publisher abstract | Generalized sine-Gordon discretizations and moving mesh lineage. |
| [11] Maltseva–Popovych (2024), https://arxiv.org/html/2103.08734v4 | Author full text, introduction and equivalent forms; publication metadata confirmed on author's https://www.imath.kiev.ua/~rop/ | Modern structural work; variable conventions. |
| [12] Tian et al. (2015), https://www.atlantis-press.com/article/125950664.pdf | Publisher full text, Section 4, Eq. (4.1) | Existing discrete DLW terminology. The equation is u_(n,y)=v_n-v_(n+1), v_(n,x)=v_n(u_n-u_(n-1)); no equivalence/non-equivalence theorem to our lattice is claimed. Use journal year 2015, not migrated website date 2021. |
| [13] Feng–Maruno–Ohta (2010), https://arxiv.org/abs/0905.2693 | Author abstract; journal details checked at https://waseda.elsevierpure.com/en/publications/a-self-adaptive-moving-mesh-method-for-the-camassa-holm-equation/ | Earlier Camassa–Holm moving-mesh work. |
| [14] Feng–Maruno–Ohta (2014), https://link.springer.com/article/10.1186/s40736-014-0008-7 | Publisher full text, abstract and Background | Conservation density, mesh intervals, reciprocal transformations and Lax structure. |
| [15] Huang–Russell (2011), https://link.springer.com/book/10.1007/978-1-4419-7916-2 | Publisher book description | General moving-mesh context. |
| [16] Hirota (2004), https://www.cambridge.org/core/books/direct-method-in-soliton-theory/050807AC4384D7A6101E186FEDC176F4 | Publisher description and front matter | Bilinear/determinant methodology. |

## Research decisions

- Searches covered DLW semi-discretization, determinant solutions, the spectral origin, BLP symmetries, sinh-Gordon discretizations, and integrable moving meshes. This is targeted contextual research, not an exhaustive novelty certification.
- An–Guo, https://arxiv.org/html/2410.20059v1 (published under https://doi.org/10.1016/j.physd.2025.134602), was also inspected. Its Eq. (1.1) has a different displayed mixed-derivative sign and background convention from our Eq. (1). It was not inserted as a direct extension of our exact solution family: such an attribution requires an explicit equivalence check. No claim is made that the present introduction exhausts work through 2025/2026.
- Removed unsupported blanket absence of a discrete DLW counterpart; stated the concrete construction and analysis undertaken here. A relation to prior lattices remains a possible later research question, not a result of this revision.
- Removed universal assertions that all waves are oblique bands, that orientation and speed are independently selectable without restrictions, and that exact discrete solutions are indispensable for all numerical validation. The two exact references now have distinct, accurately stated roles.
- Contribution (iii) clarifies that “two exact families” means continuous versus semi-discrete, not PE versus PF. The compact-set and regular-parameter scope follows Section 2.5; no general initial-value numerical convergence theorem is claimed.
- The shared-node averaging argument follows Section 3.2. Integrability of the semi-discrete model is not asserted for the fully discrete time integrator or for the whole mesh algorithm.

## Files and verification

`before_manuscript.md` and `before_draft.html` preserve the previous version. `introduction_en.md` and `introduction_zh.md` hold the replacement sections. `revise.py` applies the narrowly scoped edit and checks untouched abstracts/body, complete citations and word counts. Rebuild uses the project's existing `build.py`; its validation checks math rendering, equation sequence, anchor uniqueness and local assets. Printed versions and PDFs are outside this revision.
