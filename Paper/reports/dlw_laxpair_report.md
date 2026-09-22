# Lax pair / linear problem of the (2+1)-dimensional dispersive long wave (DLW) system

**Method note.** Every formula below was read out of a fetched document (arXiv PDF/HTML, journal
open-access PDF, publisher abstract API). Nothing is reconstructed from memory. Normalizations differ
between sources; I flag every place where I could not verify that two printed forms are the same system.
All formulas below are quoted as printed (LaTeX transcription of the printed symbols).

---

## 0. The equation as actually printed (four independent sources)

| # | System as printed | URL |
|---|---|---|
| a | `u_{yt} + h_{xx} + (1/2)(u^2)_{xy} = 0`,  `h_t + (uh + u + u_{xy})_x = 0` — "which were first obtained by Boiti et al [1] as a compatibility condition for a "weak" Lax pair" | https://arxiv.org/abs/math/9804162 |
| b | `u_{yt} + v_{xx} + (1/2)(u^2)_{xy} = 0`,  `v_t + (uv + u + u_{xy})_x = 0` — "该系统是由 Boiti 等人首先提出的，它是由一个弱 Lax 对的相容性条件而得到的" ("first proposed by Boiti et al., obtained from the compatibility condition of a weak Lax pair") | https://nshu.hainanu.edu.cn/cn/article/pdf/preview/10.15886/j.cnki.hdxbzkb.2008.03.001.pdf |
| c | `u_{yt} + \eta_{xx} + u_x u_y + u u_{xy} = 0`,  `\eta_t + u_x + \eta u_x + u \eta_x + u_{xxy} = 0` — "Equations (1) are firstly obtained by Boiti et al.[1] as a compatibility condition for a "weak" Lax pair." | https://ctp.itp.ac.cn/EN/article/downloadArticleFile.do?attachType=PDF&id=9298 |
| d | `u_{yt} + (v_x + u u_y)_x = 0`,  `v_t + (uv - u_{xy})_x = 0` — "The DLWEs were initially introduced by Boiti in 1987 as a compatibility condition for a weak Lax pair [8]." | https://arxiv.org/abs/2410.20059 |

Form (b) has **exactly your second equation** (`v_t + (uv + u + u_{xy})_x = 0`). Your first equation
`u_t + v_x + (1/2)(u^2)_y = 0` is the once-`x`-integrated form of form (a)/(b) (note `(1/2)(u^2)_{xy} = ((1/2)(u^2)_y)_x`).
**UNCERTAIN:** whether Sheng & Yu print the first equation integrated or differentiated — I could not read
Sheng & Yu's text (paywalled, see §5).

---

## 1. The Lax pair(s)

### (A) Explicit spectral problem with explicit `\lambda`, plus a 2×2 matrix form — *best match to the request*
Gordoa, Joshi & Pickering, *On a Generalized 2+1 Dispersive Water Wave Hierarchy*,
Publ. RIMS **37** (2001) 327–347 (open access, J-STAGE).
URL: https://www.jstage.jst.go.jp/article/kyotoms1969/37/3/37_3_327/_pdf

System (1): `u_t = R u_\tau + G`, `u = (u,v)^T`, `G = (g,0)^T`; recursion operator (2)
```
R = (1/2) [ [ \partial_x u \partial_x^{-1} - \partial_x ,  2 ],
             [ 2v + v_x \partial_x^{-1} u + \partial_x ,  0 ] ]
```
with `R = B_2 B_1^{-1}` (3), `B_2 = (1/2)[[2\partial_x, \partial_x u - \partial_x^2],[u\partial_x+\partial_x^2, v\partial_x+\partial_x v]]` (4),
`B_1 = [[0,\partial_x],[\partial_x,0]]` (5).

**"The system (1) has the Lax pair"** (6)–(8):
```
(6)   \psi_{xx} = [ (\lambda - (1/2)u)^2 + (1/2)u_x - v ] \psi
(7)   \psi_t    = \lambda \psi_\tau + (1/2)(\partial_x^{-1} u_\tau) \psi_x - (1/4) u_\tau \psi
(8)   \lambda_t = \lambda \lambda_\tau + (1/2) g          (non-isospectral: \lambda = \lambda(\tau,t))
```
Explicit **2×2 matrix** linear problem (40)–(41), with F given explicitly at (57):
```
(40)  \Psi_x = F \Psi
(57)  F = [[ -(1/2)(2\lambda-u) ,  1 ],
           [ -v               ,  (1/2)(2\lambda-u) ]]
(41)  (1/2) \sum_{i=0}^{n+1} \lambda^{n+1-i} g_i \Psi_\lambda = H \Psi = (\lambda^n F + G)\Psi
```
Consistency check I performed myself: eliminating `\psi_2` from `\Psi_x=F\Psi` gives back (6) exactly, since
`-[\tfrac12(2\lambda-u)]_x = \tfrac12 u_x`.

**Caveat (UNCERTAIN):** this paper calls the system "dispersive water wave (DWW)" and says its 1+1 limit is the
Broer system (refs [18],[19] = Broer 1975, Kaup 1975); it does *not* cite Boiti and never writes "DLW". The DLW's
1+1 reduction is the same Broer/Kaup (classical Boussinesq) system, so this is the same family — but I did **not**
verify by explicit change of variables that (1)/(6)-(8) is literally the Boiti–Leon–Pempinelli system.

### (B) Gauge-invariant operator Lax pair for the "2DGDLW"
Leble & collaborators, *Gauge-invariant description of (2+1)-dimensional integrable NLEEs*, arXiv:0802.2334 (also 0907.3205).
URL: https://arxiv.org/abs/0802.2334
```
(1.1)  L_1 \psi = ( \partial_{\xi\eta} + u_1 \partial_\xi + v_1 \partial_\eta + u_0 ) \psi = 0
(1.2)  L_2 \psi = ( \partial_t + u_3 \partial_\xi + v_3 \partial_\eta + u_2 \partial_\xi^2 + v_2 \partial_\eta^2
                     + \tilde u_1 \partial_\xi + \tilde v_1 \partial_\eta + v_0 ) \psi = 0
       \xi = x + \sigma y ,  \eta = x - \sigma y ,  \sigma^2 = \pm 1
```
Case (ii) (`u_3=v_3=0`, `u_2=\kappa_1=const`, `v_2=\kappa_2=const`) is stated to lead to "the famous
two-dimensional generalization of dispersive long-wave system"; with `\kappa_2 = 0` the printed system is
```
(1.21)  q_{t\eta} = -\kappa_1 r_{\xi\xi} - (\kappa_1/2)(q^2)_{\xi\eta}
(1.22)  r_{t\xi} = ( -\kappa_1 q r + q + q_{\xi\eta} )_{\xi\xi}
```
Note the `+q` term, which is the signature term of the DLW. **Caveat:** `\lambda` does not appear explicitly in
(1.1)–(1.2); the pair is a Lax/zero-curvature pair without a printed spectral parameter.

### (C) The Boiti-type "weak Lax pair" as quoted by a later paper (for the paper's own "GLDW")
*Miura transformation between two non-linear equations in 2+1 dimensions*, arXiv:solv-int/9803007.
URL: https://arxiv.org/abs/solv-int/9803007
Printed system (2.1), there called GLDW ("In 1987 Boiti et al. [9] proposed a dispersive wave equation in 2+1 dimensions"):
```
(2.1)  0 = u_{ty} + ( \eta_{xy} + 2u u_y )_x
       0 = \eta_{ty} + ( u_{xy} + 2u \eta_y )_x
```
Lax pair exactly as printed:
```
(3.12)  0 = \phi_t - \phi_{xx} + 2u \phi_x
        0 = \phi_{xy} - \partial_x^{-1}( u_y \phi_x ) + (( \eta_y - u_y )/2) \phi
(3.13)  0 = \psi_t - \psi_{xx} + [ \partial_x^{-1} u_t - u_x + u^2 ] \psi
        0 = \psi_{xy} + u \psi_y + (( \eta_y + u_y )/2) \psi
```
with gauge `\phi = e^{\partial_x^{-1} u} \psi`. The paper writes of (3.13): *"This is the form of the Lax pair
obtained by other authors [11], [9]"* — [9] is Boiti, Leon & Pempinelli, Inverse Problems **3** (1987) 371.
The `\partial_x^{-1}` terms are why this is called a *weak* Lax pair.
**Caveat (UNCERTAIN):** (2.1) as printed here carries factors `2` and `\eta_{xy}` that do **not** match forms (a)–(d)
of §0; I did not verify the equivalence.

### (D) "Modified generalized DLW" Lax pair, and a dispersive-wave sub-problem with explicit `\lambda`
Tian, Cheng & Shao, Commun. Theor. Phys. **41** (2004) 807.
URL: https://ctp.itp.ac.cn/EN/Y2004/V41/I06/807
```
(2a)  \phi_t - \phi_{xx} - 2 M_x \phi = 0
(2b)  2 M_y \phi_{xy} - ( M_{xy} + N_y ) \phi_y + 2 M_y^2 \phi = 0
```
and the "long dispersive wave equation" quoted in the same paper with explicit `\lambda`:
```
(uw)_x = V_y ,   \lambda u_t + u_{xx} - 2uV = 0 ,   \lambda w_t + w_{xx} + 2wV = 0
```

### (E) Multifield / Jordan-pair form
*On the relation between multifield and multidimensional integrable equations*, arXiv:nlin/0011039.
URL: https://arxiv.org/abs/nlin/0011039
```
(27)  -\phi_y = \phi_{xx} + 2(\langle \psi_x,\phi\rangle - \langle\psi,\phi\rangle^2)\phi
      \psi_{xz} = \langle\psi,\phi\rangle \psi_z + (\langle\psi_z,\phi\rangle - 1)\psi
      \phi_{xz} = -\langle\psi,\phi\rangle \phi_z - (\langle\psi,\phi_z\rangle + 1)\phi
(28)  u_y = (u_x + u^2 - 2q)_x ,  -v_t = (v_x - 2uv)_x ,  q_z = v_x
      with u = \langle\psi,\phi\rangle, v = \langle\psi_z,\phi\rangle - 1, q = \langle\psi,\phi_x\rangle + u^2
```

---

## 2. Infinite family of conserved densities `\rho_k, \sigma_k` — **NOT FOUND**

I could not find any accessible source that writes out DLW conserved densities `\rho_k` and fluxes `\sigma_k`
explicitly, and I could not read Sheng & Yu (paywalled). Searched: arXiv API (title/abstract/all for both
"dispersive long wave" and "DLW"/"conservation laws"), OpenAlex, Semantic Scholar (incl. all 16+ citing papers
of Sheng & Yu), J-STAGE, CTP/IOP/Chin. Phys. B mirrors, MDPI/Hindawi-style OA venues, zbMATH/ScienceGate pages.

The closest thing I *did* read (Gordoa–Joshi–Pickering, same URL as §1A) is the recursion operator and the
Hamiltonian operators from which such a family is generated (their eqs. (2), (4), (5) quoted in §1A), plus the
statement: *"We note that in fact the DWW hierarchy is tri-Hamiltonian."* The paper does not print the densities.

---

## 3. Standard Lax pair / linear problem of the 2D Toda lattice and of dKP

### 3.1 2D Toda lattice — equation
arXiv:1802.06452 (W. Fu, *Direct linearisation of the discrete-time two-dimensional Toda lattices*), eq. (1.1),
"originally proposed by Mikhailov [18] in 1979":
```
\partial_1 \partial_{-1} \varphi_n = - e^{\varphi_{n+1}-\varphi_n} + e^{\varphi_n-\varphi_{n-1}}
```
and the A_1^{(1)} scalar reductions, eq. (1.3):
```
\partial_1 \partial_{-1} \varphi_0 = e^{2\varphi_0} + e^{-2\varphi_0}   and   \partial_1 \partial_{-1} \varphi_0 = e^{2\varphi_0} - e^{-\varphi_0}
```
URL: https://arxiv.org/abs/1802.06452

### 3.2 2D Toda lattice — explicit difference-equation Lax pair
arXiv:2104.06123 (Yin & Fu, *Linear integral equations and two-dimensional Toda systems*), §3.2 eq. (3.9).
With `\varphi_n \doteq \ln(\tau_{n+1}/\tau_n)` (their `\phi_n`) and `\varphi_n = [u_n(k)]^{(0)}`:
```
\partial_1 \varphi_n = (\partial_1 \ln\tau_{n+1} - \partial_1\ln\tau_n)\varphi_n + \varphi_{n+1} = (\partial_1\phi_n)\varphi_n + \varphi_{n+1}
\partial_{-1}\varphi_n = (\tau_{n+1}\tau_{n-1}/\tau_n^2)\varphi_{n-1} = e^{\phi_n-\phi_{n-1}}\varphi_{n-1}
```
equivalently, with `\Phi = {}^t(\cdots,\varphi_{-1},\varphi_0,\varphi_1,\cdots)`,
```
(3.9)   \partial_1 \Phi = P \Phi ,   \partial_{-1} \Phi = Q \Phi
```
where `P` is the tridiagonal matrix with rows `(\partial_1\phi_i, 1)` and `Q` has rows `(e^{-\theta_i}, 0)`
(`\theta_n = \varphi_{n-1}-\varphi_n`). The paper adds: *"We refer to (3.9) as the Lax pair of the 2DTL of
A_\infty-type (see [5,6,32]), since equation (1.1) arises as the compatibility condition of the equations in (3.9)."*
The spectral parameter appears in the underlying linear integral equation through `\rho(k), \sigma(k')`.
URL: https://arxiv.org/abs/2104.06123

### 3.3 2D Toda lattice — matrix Lax matrices with explicit spectral parameter
arXiv:1908.08725 (Yu, *Rank shift conditions and reductions of 2d-Toda theory*), §2.1–2.2:
```
L_1 = S_1 \Lambda S_1^{-1} ,   L_2 = S_2 \Lambda^{\top} S_2^{-1}     (\Lambda = shift matrix)
L_1 P(x) = x P(x) ,   L_2^{\top} Q(y) = y Q(y)                      (x, y = spectral parameters)
\partial L_1 / \partial t_n = [ L_1 , (L_1^n)_- ] ,   \partial L_2 / \partial s_n = [ L_2 , (L_2^n)_+ ]
wave functions: \Phi_1(t,s;z) = e^{\xi(t,z)} S_1 \chi(z),  \Phi_2(t,s;z) = e^{\xi(s,z^{-1})} S_2 \chi(z^{-1})
```
URL: https://arxiv.org/abs/1908.08725

### 3.4 Discrete 2D Toda lattice — explicit Lax matrices with spectral parameter `k`
arXiv:1802.06452, §4.4 eqs. (4.11a) ("tilde" part) and (4.11b) ("check" part). For `r`-periodic reduction,
`\tilde\varphi = \tilde L \varphi` is the `r\times r` matrix with rows
`(p_1 + u_1 - \tilde u_0,\; 1)`, …, `(p_1 + u_{r-1} - \tilde u_{r-2},\; 1)`, and last row
`(k^r,\; 0,\dots,0,\; p_1 + u_0 - \tilde u_{r-1})`; the "check" matrix has rows
`(1+p_{-1}(u_i - \check u_i),\; p_{-1})` and `* = k^{-r}[1 + p_{-1}(u_0-\check u_0)]` in the bottom-left.
URL: https://arxiv.org/abs/1802.06452

### 3.5 dKP (dispersionless KP) hierarchy — explicit Lax pair, spectral parameter `p`
K. Takasaki, lecture notes (`aa95.pdf`), §3, eqs. (3.7)–(3.12):
```
(3.7)  \hbar\partial_x \to p ,   \hbar^{-1}[A,B] \to \{A,B\}
(3.8)  \{A,B\} = \partial_p A \cdot \partial_x B - \partial_x A \cdot \partial_p B
(3.9)  L = p + \sum_{n=1}^{\infty} u^{(0)}_{n+1} p^{-n} ,   M = \sum_{n=2}^{\infty} n t_n L^{n-1} + x + \sum_{n=1}^{\infty} v^{(0)}_n L^{-n-1}
(3.10) \partial L/\partial t_n = \{B_n, L\} ,   \partial M/\partial t_n = \{B_n, M\}
(3.11) \{L, M\} = 1
(3.12) B_n = ( L^n )_{\ge 0}
"This hierarchy is called the 'dispersionless KP hierarchy' [18]."
(3.13) \hbar \partial\Psi/\partial t_n = B_n \Psi ,   \lambda \Psi = L \Psi ,   \hbar \partial\Psi/\partial\lambda = M \Psi
```
URL: http://www2.yukawa.kyoto-u.ac.jp/~kanehisa.takasaki/res/aa95.pdf

### 3.6 Dispersionless (Hamiltonian-vector-field) Lax pair with **explicit `\lambda`**, incl. the dKP equation
Rom. Rep. Phys. (2025), *The integrable hierarchy and the nonlinear Riemann–Hilbert problem associated with one
typical Einstein–Weyl physico-geometric dispersionless system*, §2 eqs. (1)–(7). The paper prints the dKP equation
in its introduction as `u_{xt} - (uu_x)_x - u_{yy} = 0`, and gives
```
(2)  L_1 = \partial_t - \{H_1,\cdot\} = \partial_y - \lambda \partial_x + 2u_x \lambda \partial_\lambda
(3)  L_2 = \partial_y - \{H_2,\cdot\} = \partial_t + ( (1/2)\lambda^2 + u\lambda ) \partial_x
                                       - ( u_x \lambda + u_y + 2u u_x ) \lambda \partial_\lambda
(4)  H_1 = \lambda + 2u
(5)  H_2 = -( (1/4)\lambda^2 + u\lambda + u^2 + \partial_x^{-1} u_y )
(6)  [L_1, L_2] = 0
(7)  \partial H_1/\partial y - \partial H_2/\partial t + \{H_1,H_2\} = 0
     \{A,B\} = \lambda (\partial_\lambda A)(\partial_x B) - \lambda (\partial_x A)(\partial_\lambda B)
```
URL: https://rrp.nipne.ro/IP/AP818.pdf

---

## 4. Discrete / semi-discrete DLW and (2+1)-dimensional sinh-Gordon

### 4.1 Hu & Yu, J. Phys. A **40** (2007) 12645 — *Integrable discretizations of the (2+1)-dimensional sinh-Gordon equation*
- DOI: https://doi.org/10.1088/1751-8113/40/42/s10 — **paywalled**; IOPscience serves a "Radware Bot Manager
  Captcha" to automated fetches, so I could not read the body text.
- **No arXiv preprint exists.** I queried the arXiv API for `au:"Hu_Xing-Biao"` (list returned, 2002–2024) and
  `au:"Yu_Guo-Fu"` (2007–2026) and for `all:"sinh-Gordon" AND all:"discretization"`; the 2007 J. Phys. A paper is
  not among them.
- **Abstract (verbatim, publisher abstract retrieved via the OpenAlex API):**
  *"In this paper, we propose two semi-discrete equations and one fully discrete equation and study them by
  Hirota's bilinear method. These equations have continuum limits into a system which admits the (2+1)-dimensional
  generalization of the sinh-Gordon equation. As a result, two integrable semi-discrete versions and one fully
  discrete version for the sinh-Gordon equation are found. Backlund transformations, nonlinear superposition
  formulae, determinant solution and Lax pairs for these discrete versions are presented."*
- The abstract confirms a Lax pair **exists** but does **not** print it. I found no citing paper that quotes it
  (I checked the 16+ citing works returned by the Semantic Scholar API for Sheng & Yu, and the JNMP 2023
  (2+1)-sinh-Gordon paper's reference list, which cites Hu & Yu as ref. [20] without reproducing the Lax pair).
  → **The discrete (2+1) sinh-Gordon Lax pair of Hu & Yu (2007) is UNKNOWN to me.**

### 4.2 Discrete 2+1 sinh-Gordon with explicit Lax matrices and spectral parameter (accessible substitute)
arXiv:1802.06452 §4.5, A_1^{(1)} reduction of the discrete-time 2DTL:
```
p_1 p_{-1} \exp(\tilde{\check\phi}_0 - \check\phi_0) - \exp(\tilde\phi_0 - \phi_0) = \exp(\tilde\phi_0 + \tilde{\check\phi}_0) - \exp(-\phi_0 - \check\phi_0)
```
stated to be "the discrete analogue of the continuous-time sinh–Gordon equation", and the discrete sine–Gordon
```
p_1 p_{-1} \sin(\vartheta_0 + \tilde{\check\vartheta}_0 - \tilde\vartheta_0 - \check\vartheta_0) = \sin(\vartheta_0 + \tilde\vartheta_0 + \check\vartheta_0 + \tilde{\check\vartheta}_0)
```
under `\phi_0 = 2i\vartheta_0`. Its Lax pair is the `r = 2` case of (4.11a)/(4.11b) in §3.4 (2×2 matrices, explicit
spectral parameter `k`, lattice parameters `p_1, p_{-1}`). URL: https://arxiv.org/abs/1802.06452

### 4.3 Continuous (2+1)-dimensional sinh-Gordon
JNMP **30** (2023) 1621–1640, *General Soliton and (Semi-)Rational Solutions of a (2+1)-Dimensional Sinh-Gordon
Equation* (open access). Verbatim: *"In 1987, the sinh-Gordon equation, q_{xt} + sinh q = 0, was extended to
(2+1)-dimension by the inverse spectral transform [17]. The extended (2+1)-dimensional sinh-Gordon equation reads
[their eq. (1)]"* — the printed eq. (1) uses two nested `\int_{-\infty}^{x}` terms and came out too garbled in
PDF text extraction for me to transcribe reliably, so **I do not quote it**. This paper prints **no Lax pair**.
URL: https://link.springer.com/content/pdf/10.1007/s44198-023-00147-z.pdf

### 4.4 Discrete / semi-discrete DLW
**Nothing found.** No discrete or semi-discrete version of the Boiti–Leon–Pempinelli DLW, and no Lax pair for one,
turned up in any of the searches above.

---

## 5. Is DLW regarded as strongly / completely integrable?

**No source I read calls DLW "strongly integrable".** The literature consistently says:

- It **is Lax / IST integrable** (it is the compatibility condition of Boiti et al.'s *weak* Lax pair):
  https://arxiv.org/abs/math/9804162 , https://arxiv.org/abs/2410.20059 ,
  https://ctp.itp.ac.cn/EN/article/downloadArticleFile.do?attachType=PDF&id=9298
- It has an **infinite-dimensional Kac–Moody–Virasoro symmetry algebra** (Paquin & Winternitz) and a larger
  `W_\infty` symmetry. Verbatim: *"The infinite dimensional Kac-Moody-Virasoro type symmetry structure of the model
  is revealed by Paquin and Winternitz[10]. The more general W_\infty symmetry is given in[11]."*
  https://arxiv.org/abs/nlin/0107027
- It **FAILS the Painlevé test**, in both the WTC and the ARS senses. Verbatim: *"It is proven that[12] the 2DDLWE
  system is fails in passing the Painlevé test both at the WTC's (Weiss-Tabor-Carnevale) meaning and at the ARS's
  (Ablowitz-Ramani-Segur) meaning."* (https://arxiv.org/abs/nlin/0107027); and *"Though the model equation system is
  Lax or IST integrable, it does not pass the Painlevé test.[9]"*
  (https://ctp.itp.ac.cn/EN/article/downloadArticleFile.do?attachType=PDF&id=9298); and *"Sen-yue Lou [3] showed that
  eqs. (1.1) and (1.2) do not pass the Painlevé test, both in the ARS algorithm and in the WTC approach."*
  (https://arxiv.org/abs/math/9804162)

So: **Lax/IST integrable with infinite-dimensional symmetry, but not Painlevé-integrable** — i.e. not
"completely integrable" in the strong (Painlevé) sense, while still being an integrable system in the Lax sense.

---

## 6. What I could not find

1. The explicit DLW Lax pair in Sheng & Yu's own normalization. Sheng & Yu, Physica D **432** (2022) 133140
   (= *Solitons, breathers and rational solutions for a (2+1)-dimensional dispersive long wave system*,
   DOI 10.1016/j.physd.2021.133140) is paywalled; ScienceDirect returned HTTP 403, ResearchGate/scilit/ouci were
   unreachable, and there is **no arXiv preprint** (checked arXiv API for `au:"Yu_Guo-Fu"`, 2012–2026). Its
   abstract is elided by the publisher in both the Semantic Scholar and OpenAlex APIs.
2. The infinite family of conserved densities `\rho_k, \sigma_k` for DLW — no source prints them.
3. The Boiti–Leon–Pempinelli 1987 paper itself (Inverse Problems **3** 371). IOPscience serves a bot captcha for
   the PDF (only the abstract page was readable, and it does not print the Lax pair). Its Lax pair is only
   available to me second-hand, via §1C.
4. Any preprint/arXiv version of Hu & Yu (2007), and any citing paper that quotes its discrete Lax pair.
5. Any discrete or semi-discrete DLW.

**Reproducibility note:** downloaded/extracted source files are in `C:\Users\msz\学术内容\Paper\refs\`
(PDFs + `pdftotext` output) if you want to re-check any transcription.
