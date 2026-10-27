from pathlib import Path
root=Path(__file__).resolve().parent
p=root/'manuscript.html';s=p.read_text(encoding='utf-8')
(root/'manuscript_before_case_layout.html').write_text(s,encoding='utf-8')
start=s.index('<p>The density conservation law establishes the natural moving mesh')
end=s.index('</section>',start)
s=s[:start]+r'''<p>A moving mesh needs a rule that specifies both its velocity and the quantity carried by each cell. Here the physical density supplies such a rule through its conservation equation. If the endpoints of a cell move with velocity \\(-u\\), differentiation of its mass gives</p>
\\[\frac{d}{dT}\int_{x_{k-1}(T)}^{x_k(T)}\rho(x,T)\,dx=[u\rho]_{x_{k-1}}^{x_k}+\rho(x_k,T)\dot x_k-\rho(x_{k-1},T)\dot x_{k-1}=0.\\]
<p>The flux through the moving endpoints therefore cancels the change of mass inside the cell. For positive density, the accumulated mass defines a monotone coordinate \\(X\\), and the conserved cell mass is \\(a_k=X_k-X_{k-1}\\). Representing the density by its cell mean gives \\(\rho_k=a_k/d_k\\). This explains the choice of density in the natural mesh: it is the conserved physical mass associated with the same velocity that moves the nodes.</p>
<p>Equal masses \\(a_k=a\\) give uniform reciprocal labels. In the present soliton profiles, the density decreases near a velocity peak, so carrying the same mass requires a wider cell there. To increase resolution where either field has appreciable curvature, we choose a nonuniform initial distribution of these labels. Piecewise-linear interpolation has a local error proportional to the field curvature and the square of the cell width, which motivates using both curvatures in the initial monitor</p>
\\[M(X)=1+\frac\gamma2\left(\frac{|u_{xx}(x(X,0),0)|}{\max|u_{xx}|}+\frac{|\rho_{xx}(x(X,0),0)|}{\max|\rho_{xx}|}\right),\qquad \int_{-4}^{X_k}M(X)\,dX=\frac{k}{N-1}\int_{-4}^4M(X)\,dX.\tag{15}\\]
<p>The constant term keeps the monitor positive and allocates nodes to the background. Normalization allows the two fields to contribute on comparable scales, while \\(\gamma\\) controls the additional concentration. Each chosen mass \\(a_k\\) is then held fixed as the direct moving FD equations evolve the cell widths. The monitor sets the initial resolution; the conservation law and the computed velocity determine its subsequent motion. Our mesh experiment holds the FD formulation fixed and compares \\(\gamma=0\\) with \\(\gamma=2\\).</p>
'''.replace('\\\\','\\')+s[end:]
s=s.replace('Figures 1 and 2 show the initial physical fields and their continuous space–time evolution.','Figures 1 and 2 show the exact physical fields at the midpoint of the observation interval, \\(T=0.125\\).')
start=s.index('<p>The natural grid allocates equal density mass to every cell.')
end=s.index('<h3 id="s45">',start)
s=s[:start]+r'''<p>We now hold the direct moving FD equations fixed and ask how their accuracy changes when the initial nodes are redistributed. This comparison uses the same fields, reciprocal endpoints, boundary data, 201 nodes, RK4 step \\(\Delta T=5\times10^{-4}\\), and terminal time \\(T=0.25\\). Only the initial label allocation changes, from uniform labels to the curvature-adapted labels in (15). Both meshes subsequently move with the computed velocity.</p>
<p>The experiment distinguishes the natural equal-mass allocation from an allocation designed to resolve curvature. We report errors at the native nodes and cells, and also after reconstructing the fields at 2,001 common physical points in \\([-2.5,2.5]\\). The latter comparison uses piecewise-linear interpolation of nodal velocity and cell-center density against continuous point values.</p>
{{FIG_MESH_EVOLUTION}}
<p>Across these cases, the conservation law supplies the relation between cell mass, density and width, while the monitor supplies a separate choice of initial resolution. The improvements at common physical points show how that choice affects the reconstructed wave profiles. This provides a practical use of the conserved coordinate: it supports a controlled redistribution of the initial nodes followed by a consistent coupled evolution of the fields and mesh.</p>
'''.replace('\\\\','\\')+s[end:]
s=s.replace('{{TABLE_SPATIAL}}','').replace('{{TABLE_TIME}}','').replace('{{TABLE_RESPONSE}}','')
s=s.replace('Table 2','Tables 2a and 2b').replace('Table 3','Tables 3a and 3b').replace('Table 5','Tables 4a and 4b')
s=s.replace('Figures 10 and 11','Figures 9 and 10')
s=s.replace('The snapshot and evolution experiments','The evolution experiments')
p.write_text(s,encoding='utf-8')
print('Source reorganized')
