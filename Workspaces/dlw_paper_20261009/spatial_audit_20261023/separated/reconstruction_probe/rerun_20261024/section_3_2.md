### 3.2 The centered semi-discretization (Centered-SD)

We introduce the physical fields through the symmetric pairings of the centered bilinear lattice. As in the Endpoint-SD construction, taking logarithms turns the bilinear equations into relations that can be subtracted and added. The second field is then defined by a lattice difference of the logarithmic potential.

The centered pairings are
\[
B_{a+h/2}f_k\cdot g_k=0,\qquad B_{a-h/2}f_k\cdot g_{k-1}=0,\qquad B_c=D_x^2+D_t+2cD_x.\tag{32}
\]
Here \(f_k\) is located at \(y_k=(k-1/2)h\), between \(g_{k-1}\) and \(g_k\). Define
\[
u_k=\partial_x\log\frac{f_k^2}{g_{k-1}g_k},\qquad Z_k=\partial_x\log(f_k^2g_{k-1}g_k),\qquad v_k=\Delta_hZ_k.\tag{33}
\]
These definitions follow the continuous fields \(u=2\partial_x\log(f/g)\) and \(v=2\partial_{xy}\log(fg)\). The field \(u_k\) is nodal, while \(v_k\) lies at the edge midpoint \(y_k-h/2\). Write \(\Delta_hq_k=(q_k-q_{k-1})/h\) and \(H(u)=u^2/2+2au\).

For a specified lower trace \(b(x,t)\), define the reconstruction \(\Omega_k[u,v;b]\) by
\[
\Omega_0[u,v;b]=b,\qquad \Omega_k[u,v;b]=\frac h2(v_k-\Delta_hu_k)-\Omega_{k-1}[u,v;b],\quad k=1,\ldots,N.\tag{34}
\]
On a finite lattice, this recurrence uniquely determines the reconstruction from the fields and the lower trace. We suppress the dependence on b below and write \(\Omega_k[u,v]\).

**Proposition 3.2 (Natural physical-field formulation of Centered-SD).** Let \(f_k,g_k\) be positive, sufficiently smooth solutions of (32). For the fields defined in (33), choose the compatible lower trace \(b=\partial_x\log(g_0/g_{-1})\). Then, for \(k=1,\ldots,N\), the physical fields satisfy
\[
\begin{aligned}
\Delta_hu_{k,t}
&=-\partial_x\Delta_h\left[H(u_k)+\frac{\Omega_k[u,v]^2}{2}-h\Omega_k[u,v]\right]-v_{k,xx},\\[2mm]
v_{k,t}
&=-\partial_x^2\Delta_hu_k\\
&\quad-\partial_x\Bigg\{\Delta_h\left[H(u_k)+\frac{\Omega_k[u,v]^2}{2}-h\Omega_k[u,v]\right]\\
&\hspace{22mm}+\frac2h\left[(u_k+2a)\Omega_k[u,v]+(u_{k-1}+2a)\Omega_{k-1}[u,v]-h(u_k+u_{k-1})\right]\Bigg\}.
\end{aligned}\tag{35}
\]

**Proof.** Set \(r_k=\log(f_k/g_k)\), \(R_k=\log(f_k/g_{k-1})\), \(s_k=\log(f_kg_k)\), and \(Q_k=\log(f_kg_{k-1})\). The first equation in (32) pairs \(f_k\) with \(g_k\), whereas the second pairs \(f_k\) with \(g_{k-1}\). We refer to these as the same-site and cross-site relations, respectively; these names describe the lattice indices in each pairing. Dividing by the corresponding products, using \((D_x^2f\cdot g)/(fg)=(\log fg)_{xx}+[(\log(f/g))_x]^2\), gives
\[
\begin{aligned}
s_{k,xx}+r_{k,x}^2+r_{k,t}+(2a+h)r_{k,x}&=0,\\
Q_{k,xx}+R_{k,x}^2+R_{k,t}+(2a-h)R_{k,x}&=0.
\end{aligned}\tag{36}
\]
We have now rewritten the two bilinear equations as two logarithmic relations. Subtracting the first relation in (36) from the second gives
\[
0=(Q_k-s_k)_{xx}+(R_{k,x}^2-r_{k,x}^2)+(R_k-r_k)_t+2a(R_k-r_k)_x-h(R_k+r_k)_x.
\]
The definitions imply \(Q_k-s_k=-(R_k-r_k)\). Introduce \(\omega_k=(R_k-r_k)_x\). Since \(u_k=(R_k+r_k)_x\), the second-derivative term is \(-\omega_{k,x}\), while the difference of squares is \(u_k\omega_k\). The subtraction therefore reduces to
\[
(R_k-r_k)_t-\omega_{k,x}+(u_k+2a)\omega_k-hu_k=0.
\]
Differentiating in x gives
\[
\omega_{k,t}=\omega_{k,xx}-\partial_x[(u_k+2a)\omega_k-hu_k].\tag{37}
\]
This is one evolution equation, for the difference between the two logarithmic derivatives. We next return to (36) and add its two relations:
\[
0=(s_k+Q_k)_{xx}+r_{k,x}^2+R_{k,x}^2+(r_k+R_k)_t+2a(r_k+R_k)_x-h(R_k-r_k)_x.
\]
From \(r_{k,x}=(u_k-\omega_k)/2\) and \(R_{k,x}=(u_k+\omega_k)/2\), the sum of squares is \((u_k^2+\omega_k^2)/2\). Substituting and differentiating in x yields
\[
u_{k,t}=-\partial_x\left[H(u_k)+\frac{\omega_k^2}{2}-h\omega_k\right]-Z_{k,xx}.\tag{38}
\]
At this stage, the two relations obtained from the bilinear system are
\[
\begin{aligned}
\omega_{k,t}&=\omega_{k,xx}-\partial_x[(u_k+2a)\omega_k-hu_k],\\
u_{k,t}&=-\partial_x[H(u_k)+\omega_k^2/2-h\omega_k]-Z_{k,xx}.
\end{aligned}
\]
The first involves \(u_k,\omega_k\); the second also contains the logarithmic potential \(Z_k\). Taking a lattice difference of the second relation and using \(v_k=\Delta_hZ_k\), the pair becomes
\[
\begin{aligned}
\omega_{k,t}&=\omega_{k,xx}-\partial_x[(u_k+2a)\omega_k-hu_k],\\
\Delta_hu_{k,t}&=-\partial_x\Delta_h[H(u_k)+\omega_k^2/2-h\omega_k]-v_{k,xx}.
\end{aligned}
\]
The potential has been replaced by v. The auxiliary quantity \(\omega\) remains, and we still need the evolution equation for v.

The field definitions provide the relation needed to continue. They give \(Z_k-u_k=2\partial_x\log(g_{k-1}g_k)\), and hence
\[
v_k-\Delta_hu_k=\frac2h\partial_x\log\frac{g_k}{g_{k-2}}=\frac2h(\omega_k+\omega_{k-1}).\tag{39}
\]
With \(\omega_0=b\), this is precisely the recurrence (34), so \(\omega_k=\Omega_k[u,v]\).

We now have equations for \(\omega_{k,t}\) and \(\Delta_hu_{k,t}\), together with a relation expressing v through u and \(\omega\). Differentiating (39) in time gives
\[
v_{k,t}=\Delta_hu_{k,t}+\frac2h(\omega_{k,t}+\omega_{k-1,t}).
\]
Both terms on the right are supplied by the preceding pair. Substituting them, the second x derivatives combine by (39) as
\[
-v_{k,xx}+\frac2h(\omega_{k,xx}+\omega_{k-1,xx})=-\partial_x^2\Delta_hu_k.
\]
The resulting physical-field equations are
\[
\begin{aligned}
\Delta_hu_{k,t}&=-\partial_x\Delta_h[H(u_k)+\omega_k^2/2-h\omega_k]-v_{k,xx},\\[2mm]
v_{k,t}&=-\partial_x^2\Delta_hu_k\\
&\quad-\partial_x\Bigg\{\Delta_h[H(u_k)+\omega_k^2/2-h\omega_k]\\
&\hspace{22mm}+\frac2h[(u_k+2a)\omega_k+(u_{k-1}+2a)\omega_{k-1}-h(u_k+u_{k-1})]\Bigg\}.
\end{aligned}
\]
Replacing \(\omega\) by the reconstruction (34) gives the two equations in (35). ∎
