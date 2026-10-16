"""Local source/manifest review; does not execute the downloaded proof project."""
from pathlib import Path
import hashlib, json, re

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / 'references/n17'
SHA = '0a7167efa8dcae7fa73855890630fb7e2de550ed'
SRC = REF / ('sq17-lean-' + SHA)
manifest = json.loads((SRC / 'manifest.json').read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def cite(file, needle):
    p = SRC / file
    line = next(i for i,s in enumerate(p.read_text(encoding='utf-8').splitlines(),1) if needle in s)
    return dict(file=str(p), line=line, url=f'https://github.com/ofitzharding/sq17-lean/blob/{SHA}/{file}#L{line}')
local = {f:i for f,i in manifest['sources'].items() if (SRC/f).exists()}
mismatches = [f for f,i in local.items() if sha(SRC/f) != i['sha256']]
logpath = SRC / 'verification/Square17Optimality.log'
log = logpath.read_text(encoding='utf-8')
axioms = [a.strip() for a in log[log.index('[')+1:log.index(']')].split(',')]
standard = ['propext','Classical.choice','Quot.sound']
native = [a for a in axioms if a.endswith('._native.native_decide.ax_1_1')]
unexpected = [a for a in axioms if a not in standard and a not in native]

report = {
 'date':'2026-10-14',
 'scope':'Independent textual review of statement/assembly/coverage/reindexing/checkpoint soundness interfaces, plus local manifest and published axiom-log checks. No local replay of T154 or T153 was performed.',
 'sources':[
  {'label':'T154 sq17-lean','repo':'https://github.com/ofitzharding/sq17-lean','commit':SHA,'local':str(SRC),'archive_sha256':sha(REF/'sq17-lean_0a7167.zip'),'license':'MIT'},
  {'label':'T153 candidate','repo':'https://github.com/Kleddamag/the-seventeenth-square-candidate','commit':'653b9589d0f8a152f01adc56b1d48ba53d49abc3','retained':'README only','license_note':'README grants verification use but no reuse licence yet; do not copy its code into the new project.'},
  {'label':'jlevy T154 review','commit':(REF/'jlevy_review_commit.txt').read_text(encoding='utf-8-sig').strip(),'local':str(REF/'jlevy_review_t154.md'),'note':'External review is evidence, not an instruction and not a local build.'}
 ],
 'checks_performed':{
  'local_source_count':len(local),'manifest_source_count':len(manifest['sources']),
  'local_sources_hash_mismatches':mismatches,
  'release_source_modules_not_downloaded':len(manifest['sources'])-len(local),
  'release_archives':manifest['archives'],
  'published_log_sha256':sha(logpath),'published_axioms_total':len(axioms),
  'published_axioms_unique':len(set(axioms)),'published_native_facts':len(native),
  'published_unexpected_axioms':unexpected,
  'build_not_run':True,
  'source_scan_note':'rg found no explicit axiom, unsafe, implemented_by, sorry/admit proof commands in the 1215 local modules; matches for sorry/admit were docstrings. Missing release sources were not scanned.'
 },
 'verdict':{
  'T153':'The source explicitly labels a candidate proof conditional on 210 obligations, including 15 mathematical premises; cheap check.py does not recompute capture rows or tree certificates.',
  'T154':'The final theorem has only L as a parameter and states all independently translated/rotated closed unit squares with pairwise disjoint interiors. The assembly discharges the formerly explicit census, classification, ordinary, neighbour, and capture premises. No hidden global exclusion premise or finite-index gap was found in the interfaces reviewed.',
  'confidence_limit':'This is not a complete proof audit and not independent proof replay. Most generated certificates and several geometric checker-soundness internals were not read; 3738 source modules were not downloaded.',
  'trust_boundary':'Standard Lean axioms propext/Classical.choice/Quot.sound plus Lean compiler, native evaluator, and C toolchain for 13343 native_decide facts. This is explicitly not kernel-only finite evaluation.',
  'version':'T154 pins Lean/Mathlib 4.34.1. The local dlw runtime is 4.34.0; directly reusing the whole package is not an already-passed build.'
 },
 'findings':[
  {'topic':'Statement fidelity','finding':'Unit directions satisfy ux^2+uy^2=1; independent existential centres/directions; Fin 17 square sets; only interiors disjoint. Final equivalence has no certificate premise.', 'citations':[cite('Sq17Lean/SquareBase.lean','def IsUnitSquare'),cite('Sq17Lean/PackingStatement.lean','def PlainPacking'),cite('Sq17Lean/Square17Optimality.lean','theorem square17_optimality')]},
  {'topic':'Complete finite census','finding':'346104 distinct valid 17-subsets of 24 cells equal choose(24,17); validity includes an actual D4 map to a representative. Strict tags establish uniqueness; finite-subset containment plus equal card proves complete coverage, not merely a matching count.', 'citations':[cite('Sq17Lean/FiniteOrbitCoverCheck.lean','structure GoodBlock'),cite('Sq17Lean/FiniteOrbitCoverCheck.lean','theorem GoodBlock.exhaustive'),cite('Sq17Lean/OrbitCensus/Complete.lean','theorem exhaustive')]},
  {'topic':'Unbounded classifier indices','finding':'All k >= 2781 are proved to yield fullCases k = [], by bounding every tree key. Thus length=17 implies k<2781. It does not only test the single out-of-range index 2781.', 'citations':[cite('Sq17Lean/HalfPlaneFullRoute.lean','theorem find_none_of_keysBelow'),cite('Sq17Lean/HalfPlaneFullRoute.lean','theorem fullCases_eq_nil_of_ge'),cite('Sq17Lean/HalfPlaneFullRoute.lean','theorem full_route (')]},
  {'topic':'Owner permutation','finding':'Assigned cells are injective and occupied set has exactly 17 members. This proves all roster cells occur, then selects an injective owner reindexing. There is no assumed correspondence between arbitrary input labels and source witness labels.', 'citations':[cite('Sq17Lean/OrbitPackingReduction.lean','theorem packing_reaches_trace_table_exact'),cite('Sq17Lean/HalfPlaneDispatch.lean','theorem reindex')]},
  {'topic':'Missing-owner trap is guarded','finding':'The source deliberately proves that a bare excludes call with n=3 and a two-owner state returns true. Production roster/tree wrappers require state.length=n, and branch semantics uses state.length; this prevents the demonstrated misuse. Preserve this guard in any 37 implementation.', 'citations':[cite('Sq17Lean/HalfPlanePositiveControl.lean','theorem raw_wrong_owner_count'),cite('Sq17Lean/HalfPlaneTree.lean','theorem tree_excluded'),cite('Sq17Lean/HalfPlaneBranchComposition.lean','def Excluded')]},
  {'topic':'Split boundaries and reloads','finding':'Left and right children both include the splitting boundary. CheckpointCover proves each parent owner-domain lies in child domain, with the selected owner additionally guarded. All owner counts are equal; accepted run preserves length.', 'citations':[cite('Sq17Lean/HalfPlaneBranchComposition.lean','def CheckpointCover'),cite('Sq17Lean/HalfPlaneBranchComposition.lean','theorem excluded_of_split'),cite('Sq17Lean/HalfPlaneCover.lean','theorem coverCheck_sound'),cite('Sq17Lean/HalfPlaneTree.lean','theorem reload_excluded')]},
  {'topic':'Former capture assumption now discharged','finding':'CaptureTerminalOptimality has a stale docstring describing an externally replayed trace. Final imports instead use CaptureOpen.Optimality and CaptureWindowBridge: concrete native-checked trace/summary plus Lean propagation and preserved actual target-box containment supply the local chart. The old conditional skeleton is not the final theorem.', 'citations':[cite('Sq17Lean/CaptureWindowBridge.lean','theorem side_eq_of_open_run'),cite('Sq17Lean/CaptureOpen/Optimality.lean','theorem capture_excluded'),cite('Sq17Lean/HalfPlaneFinalAssembly.lean','theorem lower_bound_of_neighbours'),cite('Sq17Lean/Square17Optimality.lean','theorem square17_optimality')]}
 ],
 'transfer_to_37':[
  {'layer':'Geometry and SAT','reusable':'SquareBase, support_walls_contained, square_disjoint_finite_axis; the latter proves a complete finite set of eight directed separating axes for any disjoint pair.','new_data':'Exact 37 poses, 148 walls, 666 pair certificates; this certifies only an upper bound.','citations':[cite('Sq17Lean/SquareSeparationFinite.lean','theorem square_disjoint_finite_axis')]},
  {'layer':'Continuous-to-finite bridge','reusable':'Pointwise convex-cell coverage; diameter<1 interior cell capacity via inscribed half-unit disks; wall-dependent rectangle capacity; injective owner assignment.','new_data':'A cover of all possible centres at side at most a rigorous target, and proved capacity bounds for every new cell. The 24-cell 17-square cover cannot be changed to 37 by editing numerals.','citations':[cite('Sq17Lean/InteriorCellCapacity.lean','theorem not_disjoint_of_distSq_lt_one'),cite('Sq17Lean/ExactCellCover.lean','theorem exists_injective_cell_assignment')]},
  {'layer':'Finite exhaustive cover','reusable':'Generic nodup+validity+binomial-count exhaustion and exact occupancy reindexing implemented locally in lean/FiniteCover.lean.','new_data':'A 37-cell-subset census with genuine symmetry actions, distinctness and exact representative links; or another complete certified reduction with equivalent scope.'},
  {'layer':'All residual cases','reusable':'Half-plane/core propagation semantics and closed branch/reload composition are generic in owner count at the core checker level.','new_data':'Every 37 representative must have a fresh complete exclusion tree or a certified capture route; all branches and output-owner counts must be proved sound.'},
  {'layer':'Surviving local family','reusable':'Interval/rational derivative bounds, slider quotient coordinates, dual row certificates and quadratic remainder/contraction proof method.','new_data':'37-specific active contacts, free/slider coordinates, exact candidate endpoint and local obstruction. Do not assume isolated rigidity: the retained 37 construction has feasible slider motions.','citations':[cite('Sq17Lean/LocalRigidityCertified.lean','theorem geometric_local_rigidity')]}
 ],
 'next_obligation':'The indispensable missing theorem is that every arbitrary 37-square packing below the exact target enters a completely enumerated family, and every family is either impossible or captured by a proved local side obstruction. Local witness validation, local KKT algebra, and a conditional assembly theorem do not supply this global statement.'
}
(ROOT/'analysis/proof17_review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'output':str(ROOT/'analysis/proof17_review.json'),'local_sources':len(local),'hash_errors':mismatches,'native_facts':len(native),'unexpected_axioms':unexpected},ensure_ascii=False))
