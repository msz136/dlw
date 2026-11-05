# Explicit omega reconstruction in Proposition 3.2

2026-11-05. Replaced the recurrence in main-text equation (50) by the exact finite sum omega_k = (-1)^k omega_0 + (1/2) sum_{j=1}^k (-1)^(k-j) [h v_j - u_j + u_{j-1}]. It directly expands the existing backward difference and Appendix B formula (B5). The compatible lower trace remains stated inside the proposition. The k=0 value and cancellation of adjacent sums reproduce omega_k + omega_{k-1} = [h v_k - u_k + u_{k-1}]/2, proving equivalence with the original recurrence.

Adjusted proof/reference wording in Sections 3.2, 3.4, 4.2 and Appendix B so (50) is called the explicit reconstruction, and (76)/(B4) remain its recursive evaluation. Eight associated prose substitutions were synchronized between HTML and TeX. Only display formula 50 changed, all 112 tags and 117 display blocks retained. Two-pass compile has no warnings and 40 pages. Changed PDF pages 9, 10, 11, 12, 14, 34 were rendered and reviewed. Proposition (49)/(50) already spanned P9/P10 in the entry PDF and still does. Browser verification found no KaTeX errors, missing images, equation/tag collisions or document overflow. html-50.png checks the explicit sum. 2HS untouched.

Outputs are C:/Users/msz/aca/pdf/dlw/main.tex, main.pdf, and C:/Users/msz/aca/dlw-paper.html. before/ is the entry snapshot. validation.json and html_validation.json hold checks.
