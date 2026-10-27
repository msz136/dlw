from pathlib import Path
import shutil,re,json
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'samm_three_20261027/narrative_revision'; OUT.mkdir(exist_ok=True)
p=ROOT.parents[1]/'pdf/2hs/main.tex'
if not (OUT/'before_main.tex').exists():
 shutil.copy2(p,OUT/'before_main.tex');shutil.copy2(p.with_suffix('.pdf'),OUT/'before_main.pdf')
t=(OUT/'before_main.tex').read_text(encoding='utf-8');old=t
def replace(a,b):
 global t
 assert a in t,a[:90]
 t=t.replace(a,b,1)

# Integrate the analytical diagnostic into the case it concerns.
st=t.index(r'\subsection*{5.4. What the density comparison reveals}')
en=t.index(r'\FloatBarrier'+'\n'+r'\section*{6. Conclusions}',st)
block=t[st:en]
diagnostic=next(x for x in block.split('\n\n') if x.startswith('The field equations'))
refinement=next(x for x in block.split('\n\n') if x.startswith('Refinement provides'))
t=t[:st]+t[en:]
anchor='The two fields respond differently even for this single smooth wave.'
replace(anchor,anchor+'\n\n'+diagnostic.replace('The field equations also identify how to investigate these coefficients.','The different field responses can be examined through their numerical evolution equations.').replace('A separate initial-grid diagnostic illustrates the distinction.','To examine the role of the initial mesh, we also apply the velocity recovery separately from time evolution.'))
anchor='These checks accompany the terminal comparisons for all four mesh choices.'
replace(anchor,anchor+'\n\n'+refinement.replace('Refinement provides a second observation. Upon refinement','Upon refinement')+'\n\n'+r'''Across the two profiles, \(R_m\) gives the smallest velocity errors among the three moving meshes and improves the density error relative to fixed FD. The stronger concentration under \(R_2\) gives the smallest single-wave density error, but its larger velocity errors persist under refinement. The mesh choice therefore affects the two components through different error coefficients. For these waves, the curvature--mass ratio provides the most balanced allocation, while the gradient-sensitive density places greater resolution in selected regions at the expense of accuracy elsewhere in the coupled calculation.''')

# Abstract and introduction: state the insight at the scope supported by the tests.
replace('Comparisons of the three resulting self-adaptive meshes show that the curvature--mass ratio improves density accuracy in both soliton tests and velocity accuracy for the two-wave profile, while the gradient-sensitive density redistributes accuracy between the fields.',
'The three meshes retain approximately second-order refinement with different fieldwise error coefficients. The curvature--mass ratio improves density accuracy in both soliton tests and velocity accuracy for the two-wave profile; the gradient-sensitive density further reduces the single-wave density error while increasing the velocity error.')
replace('This observation motivates examining how the choice of conserved density affects the accuracy of the two fields.',
'This observation motivates examining how the choice of conserved density affects the accuracy of the two fields. A density involving curvature or density gradients can assign resolution to different parts of the same wave. The accompanying flux also changes the node motion, so its numerical effect involves both the initial allocation and the subsequent coupled evolution.')
replace('The resulting comparisons show how knowledge of the solution structure can inform both error assessment and a practical improvement in resolution.',
'These meshes retain a common second-order refinement trend while producing different errors in velocity and density. The curvature--mass ratio gives the most balanced results in the two tests, and the gradient-sensitive choice improves the single-wave density error further at a cost in velocity accuracy. This identifies the local choice of conserved coordinate as a way to influence the error coefficients of the coupled computation.')

# Section 3: clarify why variables and comparisons are chosen.
replace('We evolve the fields through either a moving physical mesh or a fixed physical grid. The moving formulations use velocity jumps and cell widths as their state variables, so that field reconstruction and node motion are performed at every stage of the time integrator. The fixed-grid formulation instead evolves a differentiated velocity variable and reconstructs the velocity by solving a discrete Poisson equation.',
r'''We formulate the numerical evolution so that the analytical relations between fields and coordinates remain explicit. On a moving mesh, velocity jumps and cell widths determine both the field reconstruction and the motion of the physical nodes. On a fixed grid, the differentiated velocity variable \(m=u_{xx}+2\) evolves with the density, and a discrete boundary-value problem recovers the velocity. These choices turn the wave equations into finite-dimensional evolutions while retaining the reconstruction needed to compare their physical fields.

The two moving formulations provide a particularly useful comparison because they share the same reconstruction and node velocity. Their slope equations can be compared at an identical state, exposing the finite-spacing correction introduced by the integrable lattice. Fixed FD supplies a centered approximation in physical coordinates. We specify each evolution and its boundary data before applying common time integrators, so that the experiments can distinguish the spatial formulation from its temporal approximation.''')
replace(r'Define \(v_k=u_k-u_{k-1}\)',r'''In the reciprocal coordinate, each cell carries the prescribed mass \(a\). Its width therefore determines its mean density, and the velocity difference between its endpoints determines the rate at which that width changes. This suggests using the two cell quantities as the evolving variables. Define \(v_k=u_k-u_{k-1}\)''')
replace('This supplies a concrete connection between the finite-lattice model and the spatial errors examined below.',
'It vanishes at the unit-density background and contributes inside a nonuniform wave. Equation (10) therefore identifies where the leading correction enters the evolution and how it scales with reciprocal spacing. The continuous-reference experiments examine the resulting field errors, including their accumulation through the reconstruction.')
replace(r'On a uniform physical grid, introduce \(m=u_{xx}+2\). Differentiating the first equation in (1) yields',
r'''A fixed physical grid gives a complementary representation in which the positions are prescribed throughout the computation. We introduce \(m=u_{xx}+2\) to obtain a local evolution equation coupled to the transported density. Differentiating the first equation in (1) yields''')
replace('We refer to this formulation as fixed FD.',
'We refer to this formulation as fixed FD. The boundary-value recovery couples the velocity across the interval, while the right-hand sides advance the local values of curvature and density. This distinction is useful when interpreting the different error profiles of the two physical fields.')
replace('Spatial comparisons begin with the continuous exact fields at',
'The choice of initial and boundary data follows the reference solution used in each experiment. To measure approximation of the continuous wave, we initialize its physical fields and supply its boundary values throughout the evolution. To measure time-integration error, we use an exact trajectory of the finite lattice. This second choice fixes the spatial model while the time step is varied.\n\nSpatial comparisons begin with the continuous exact fields at')
replace('The three methods have global orders one, four and two, respectively, for a smooth finite-dimensional evolution on a fixed interval with the usual bounded-derivative assumptions.',
'The three methods have global orders one, four and two, respectively, for a smooth finite-dimensional evolution on a fixed interval with the usual bounded-derivative assumptions. Their different orders allow the exact lattice trajectory to serve as a temporal refinement test. In the continuous-reference experiments, the time step is instead chosen small enough that halving it has little effect on the measured spatial errors.')

# Section 4: develop what each experiment answers, without repeating a roadmap.
replace('Exact wave families allow us to examine several sources of numerical error within a common setting.',
'The exact wave families provide two references with different uses. Continuous solutions measure how well a spatial formulation resolves the physical wave, whereas exact finite-lattice solutions measure how accurately a time integrator follows that formulation. We use both references to connect the algebraic correction in Section 3.1 with observable errors, and then perturb the initial velocity to examine the response generated in the density field.')
replace(r'We set \(c=1\), take zero phase constants',
r'''The one-soliton profile provides a single localized structure whose position, width and density depression can be resolved together. The two-soliton profile introduces two regions with different wave heights, testing how the same numerical choices distribute their errors over a more varied solution. Both belong to the exact family in Section 2.2, so their field values and physical coordinates can be evaluated throughout the observation interval.

We set \(c=1\), take zero phase constants''')
replace('The two-soliton experiment samples a short portion of this exact family.',
'The selected interval follows a short portion of the two-soliton trajectory and permits the spatial and temporal refinements to use the same observation times.')
replace(r'\subsubsection*{One-soliton case}',
r'''\subsubsection*{One-soliton case}

Figure 1 shows the localized velocity peak and its associated density depression. The two fields occupy the same wave region but have different shapes, so their errors are recorded separately. The density depression also determines where the natural equal-mass mesh has its wider cells.''')
replace('This decomposition guides the choice of references in the following experiments.',
'The signed terms also distinguish changes in field value from changes in the sampling position. In the spatial comparison we retain their combined effect against the continuous wave. In the temporal comparison the exact lattice state supplies the reference, so the measured discrepancy records the numerical advancement of that state.')
replace('This comparison examines how the two spatial formulations approximate the same continuous wave family.',
'Refining the spatial spacing tests how each formulation approaches the continuous wave. For integrable SD, the phase expansion in (6) and the slope correction in (10) both identify a first-order finite-spacing contribution. The centered fixed-grid differences provide a second-order comparison. We examine whether these distinctions remain visible after the fields and coordinates have evolved, and where the largest discrepancies occur within each profile.')
replace('To isolate temporal accuracy, we fix',
'The spatial tests measure the combined discrepancy from the continuous fields. The exact lattice solution now allows us to hold that spatial model fixed and examine only its numerical advancement. To isolate temporal accuracy, we fix')
replace('For each method, the perturbed solution is compared with its own unperturbed numerical trajectory.',
'For each method, the perturbed solution is compared with its own unperturbed numerical trajectory. Subtracting the two trajectories follows the added disturbance on that numerical background. Because the initial density is unchanged, its subsequent response measures the transfer generated by the coupled evolution; on the moving grids, that transfer also involves the changing cell widths.')

# Conclusion: retain the numerical scope and integrate the recovery observation.
replace('These results show how the local form of a conservation law affects the distribution of numerical accuracy between coupled fields.',
'The isolated initial-grid recovery test also favors the curvature-based meshes for the single wave, although their terminal velocity errors are larger. Initial representation and accumulated evolution thus need to be examined together when selecting a conserved coordinate. The fieldwise comparisons provide this information and identify the curvature--mass ratio as the most balanced choice among the three moving meshes in the present tests.')

def blocks(text,env):return re.findall(r'\\begin\{'+env+r'\}[\s\S]*?\\end\{'+env+r'\}',text)
assert blocks(t,'table')==blocks(old,'table')
assert blocks(t,'figure')==blocks(old,'figure')
assert re.findall(r'^\\paperdisplay.*$',t,re.M)==re.findall(r'^\\paperdisplay.*$',old,re.M)
assert 'What the density comparison reveals' not in t
p.write_text(t,encoding='utf-8')
(OUT/'validation.json').write_text(json.dumps(dict(tables_unchanged=True,figures_unchanged=True,display_equations_unchanged=True,removed_standalone_5_4=True),indent=2))
print('Narrative revised; all figure/table blocks and displayed equations unchanged.')
