from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parents[2]
P=ROOT/'pdf/2hs';A=Path(__file__).parent/'references_2hs_20261027';A.mkdir(exist_ok=True)
for name in ['main.tex','main.pdf']:
 if not (A/('before_'+name)).exists():shutil.copy2(P/name,A/('before_'+name))
s=(P/'main.tex').read_text(encoding='utf-8')
s=s.replace(' [1]',r' \cite{hori2026}').replace(' [2]',r' \cite{feng2023}')
start=s.index('Nonlinear wave equations offer');end=s.index('The availability of exact solutions',start)
s=s[:start]+r'''Nonlinear wave equations offer a setting in which coherent structures can be followed through both analytical formulas and numerical evolution. The Hunter--Saxton equation originated as an asymptotic model for director-field dynamics in nematic liquid crystals \cite{hunter1991}. Its two-component extension couples a velocity field to a transported density and admits a bilinear description through a hodograph transformation. Lou, Feng and Yao constructed a general multi-soliton solution for the two-component Hunter--Saxton (2HS) equation in this framework \cite{lou2016}. The density therefore has two roles in the computation: it is a physical field to be resolved and a quantity that determines the relation between computational and physical coordinates.

Hori, Tanaka, Maruno and Ohta developed an integrable semi-discretization of the 2HS equation using bilinear equations, determinant solutions and a discrete hodograph transformation \cite{hori2026}. Their construction supplies both a spatial model and exact finite-lattice trajectories. A related numerical approach was developed by Feng, Sheng and Yu for a generalized sine-Gordon equation \cite{feng2023}, where integrable and non-integrable semi-discrete systems generate self-adaptive moving-mesh methods. These constructions give a concrete way to use analytical solution structure in numerical evolution: the field values and the physical node positions evolve together.

Numerical studies of Hunter--Saxton-type equations have also used their geometric and conservation properties to guide discretization. Miyatake, Cohen, Furihata and Matsuo developed multi-symplectic and Hamiltonian-preserving methods for the scalar, modified and two-component equations, with particular attention to the boundary conditions required by the numerical formulations \cite{miyatake2017}. For the scalar Hunter--Saxton equation, Grunert, Nordli and Solem established convergence of a method that combines piecewise-linear projection with evolution along characteristics \cite{grunert2021}. These studies connect preservation of analytical structure with the choice of variables, boundary treatment and approximation of the evolving solution.

Mesh allocation introduces a further choice. In adaptive moving-mesh methods, a monitor function determines how a fixed number of nodes is distributed, and equidistribution provides a systematic rule for that allocation \cite{huang2011}. A reciprocal transformation supplies such a monitor through a conserved density and determines the associated node velocity through its flux. For the smooth 2HS waves studied here, however, the physical density decreases near a velocity peak. Equal density mass then assigns wider cells to this region. This observation motivates examining how the choice of conserved density affects the accuracy of the two fields.

''' +s[end:]
start=s.index(r'\section*{References}')
s=s[:start]+r'''\renewcommand{\refname}{References}
\begin{thebibliography}{9}

\bibitem{hunter1991}
J. K. Hunter and R. Saxton,
Dynamics of director fields,
\textit{SIAM Journal on Applied Mathematics} \textbf{51}(6) (1991), 1498--1521.
\href{https://doi.org/10.1137/0151075}{doi:10.1137/0151075}.

\bibitem{lou2016}
S. Lou, B.-F. Feng and R. Yao,
Multi-soliton solution to the two-component Hunter--Saxton equation,
\textit{Wave Motion} \textbf{65} (2016), 17--28.
\href{https://doi.org/10.1016/j.wavemoti.2016.04.006}{doi:10.1016/j.wavemoti.2016.04.006}.

\bibitem{hori2026}
A. Hori, Y. Tanaka, K.-i. Maruno and Y. Ohta,
An integrable semi-discretization of the two-component Hunter--Saxton equation,
arXiv:2606.18701v2 (2026).
\href{https://arxiv.org/abs/2606.18701v2}{arXiv:2606.18701v2}.

\bibitem{feng2023}
B.-F. Feng, H.-H. Sheng and G.-F. Yu,
Integrable semi-discretizations and self-adaptive moving mesh method for a generalized sine-Gordon equation,
\textit{Numerical Algorithms} \textbf{94} (2023), 351--370.
\href{https://doi.org/10.1007/s11075-023-01504-1}{doi:10.1007/s11075-023-01504-1}.

\bibitem{miyatake2017}
Y. Miyatake, D. Cohen, D. Furihata and T. Matsuo,
Geometric numerical integrators for Hunter--Saxton-like equations,
\textit{Japan Journal of Industrial and Applied Mathematics} \textbf{34} (2017), 441--472.
\href{https://doi.org/10.1007/s13160-017-0252-1}{doi:10.1007/s13160-017-0252-1}.

\bibitem{grunert2021}
K. Grunert, A. Nordli and S. Solem,
Numerical conservative solutions of the Hunter--Saxton equation,
\textit{BIT Numerical Mathematics} \textbf{61} (2021), 441--471.
\href{https://doi.org/10.1007/s10543-020-00835-y}{doi:10.1007/s10543-020-00835-y}.

\bibitem{huang2011}
W. Huang and R. D. Russell,
\textit{Adaptive Moving Mesh Methods},
Applied Mathematical Sciences, vol. 174, Springer, New York, 2011.
\href{https://doi.org/10.1007/978-1-4419-7916-2}{doi:10.1007/978-1-4419-7916-2}.

\end{thebibliography}
\end{document}
'''
(P/'main.tex').write_text(s,encoding='utf-8')
print('Updated Introduction and seven keyed bibliography entries; original sources backed up.')
