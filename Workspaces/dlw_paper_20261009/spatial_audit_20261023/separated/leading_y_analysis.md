# Table 2: leading initial y-defect coefficients (2026-10-23)

This is an asymptotic derivation with numerical coefficient checks, not an added manuscript theorem. It concerns the analytic-x initial time-derivative defect Y, not exact-lattice field error or evolved field error. Assume smooth continuous DLW fields, exact lower u_t, and interior evaluation away from the ghost boundary. Let [f]=f(x,y,0)-f(x,y0,0), with y0 the first prescribed u node, and H=u^2/2+2au. The continuous first equation gives u_t(y)=u_t(y0)-[H_x]-integral(y0,y) v_xx ds.

Endpoint-SD sums midpoint values of v_xx. FD sums trapezoidal averages. Composite quadrature expansions give

    r_E,u = h^2 [v_xxy]/24 + O(h^4),
    r_FD,u = -h^2 [v_xxy]/12 + O(h^4).

Thus r_FD,u=-2 r_E,u+O(h^4) pointwise on the same u grid. The factor-two norm relation holds in the nondegenerate leading-order regime. Endpoint's first nonlinear flux telescopes exactly here; its second equation's O(h) defect does not enter this initial evaluation of u_t from prescribed exact fields.

For Centered-SD let w=v-u_y and A=w^2/32-w/4. Since delta0 u=u_y+h^2 u_yyy/6+O(h^4), the sum of Delta u + M_-(v-delta0u) equals

    integral v ds + h^2[v_y]/12 - h^2[u_yy]/4 + O(h^4).

The flux adds h^2[A_x], giving

    r_C,u = h^2[-v_xxy/12 + u_xxyy/4 - A_x] + O(h^4).

The brackets apply to the whole expression, retaining lower-boundary contributions. These terms have wave-dependent magnitudes; second-order consistency does not constrain their coefficient to be smaller than Endpoint or FD.

For the v component, at interior nodes the lower integration constant differentiates out. Using the continuous equations to simplify time derivatives yields

    r_FD,v = -h^2 u_xxyyy/6 + O(h^4),
    r_C,v = h^2 (u_xxyyy/12 - v_xxyy/4 - (u_y*u_yy)_x/2 - A_xy) + O(h^4).

Here A_xy = w_y*w_x/16 + (w/16-1/4)*w_xy. Endpoint has r_E,v = -h/4 (v^2-u_y^2-8v)_x + O(h^2), consistent with the sign reversal between equation residual and numerical RHS defect in manuscript equation(51).

## Numerical checks

`explain_u.py` evaluates mixed log-tau derivatives analytically through normalized bivariate Taylor recurrences of exponential sums. No finite-difference fitting of coefficients is used. `u_leading_coefficients.json` compares h^2 coefficient maxima with measured u defects for all three h values; `v_leading_coefficients.json` compares Centered/FD v at h=.025.

At h=.025, max relative mismatch between predicted and measured maxima is 5.782e-5 for u (<.006%), and 3.409e-4 for v (<.035%). These are differences of maximum norms, not uniform relative errors at every spatial point.

At h=.025, ratios FD_u/Endpoint_u are 1.9999913,1.9999907,1.9999906,1.9999792 for A–D. Centered_u/Endpoint_u ratios are 6.67450,15.09914,12.32691,6.50887. The predicted v coefficients reproduce Centered below FD in A/D, and FD below Centered in B/C.

The conclusion is component-specific: the Endpoint initial u advantage over FD follows from midpoint/trapezoidal coefficients; the Centered/FD rankings depend on wave derivatives. These statements do not rank finite-time field errors, where the coupled v evolution also affects u. Manuscript HTML unchanged in this analysis turn.
