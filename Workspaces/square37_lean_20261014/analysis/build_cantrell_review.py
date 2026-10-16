from pathlib import Path
import hashlib,json

root=Path(__file__).resolve().parents[1]
def source_record(name):
    p=root/'lean'/name
    return {'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def line(name,text):
    return next(i for i,s in enumerate((root/'lean'/name).read_text(encoding='utf-8').splitlines(),1) if text in s)
data={
 'date':'2026-10-14',
 'reviewer':'proof17_review subagent',
 'scope':'Independent reading of root-authored CantrellAlgebra and CantrellSupports; subsequent conjugate-factor repair in Algebra and new Angle module were authored by this reviewer, so those additions are not independently reviewed by their author.',
 'sources':[source_record('CantrellAlgebra.lean'),source_record('CantrellSupports.lean')],
 'findings':[
  {'topic':'Root isolation','status':'correct stated scope','detail':'The polynomial has a unique root in [6.59861960924436,6.59861960924437]. The shifted derivative is strictly negative throughout [0,1], which contains the shifted isolating interval. No global packing conclusion is in this theorem.','file':'CantrellAlgebra.lean','line':line('CantrellAlgebra.lean','theorem isolated_root_exists_unique')},
  {'topic':'Conjugate factor','status':'gap in original identification repaired','detail':'Originally only quartic-root implies degree-eight-root was proved. A degree-eight root does not automatically solve the intended radical quartic. Added exact positivity of the conjugate factor throughout the interval and proved candidateSide_quartic. Its new successful build is 20261014_160506_be2ba390; no native/sorry assumptions.','file':'CantrellAlgebra.lean','line':line('CantrellAlgebra.lean','theorem candidateSide_quartic')},
  {'topic':'First chain','status':'algebra checked','detail':'Four directed gaps telescope to 3+c+s. Coordinate constraints give x31−x6≤L−4 and y6−y31≤L−3. For nonnegative c,s their weighted sum yields exactly 3+4c+5s≤(c+s)L. All assumptions are explicit.','file':'CantrellSupports.lean','line':line('CantrellSupports.lean','theorem first_chain_bound')},
  {'topic':'Braces','status':'algebra checked','detail':'Left projections U≥c+3s+3/2−sL and V≥s+2c+3/2 are weighted by c−s and c+s. Under 0≤s≤c and c²+s²=1 this gives x13+y13≥3+3c+s(c−s)(5−L). Explicit reflection gives the corresponding upper bound for x22+y22; two central support gaps give the second inequality.','file':'CantrellSupports.lean','line':line('CantrellSupports.lean','theorem central_brace_bound')},
  {'topic':'Reflection labels','status':'no defect found','detail':'rightLabels is not a permutation of all naturals, but the theorem makes no such claim: it substitutes only the five LeftBrace labels, mapped to five distinct relevant labels. It does not silently assume that the original 37-square packing is symmetric.','file':'CantrellSupports.lean','line':line('CantrellSupports.lean','def RightBrace')},
  {'topic':'Resultant and equality','status':'correct implication','detail':'Two exact support equalities and the unit-direction equation yield two quadratic equations. The resultant identity and nonzero 24−16sqrt(2) imply the selected quartic vanishes. The interval hypothesis then identifies the root. This does not convert support inequalities into equalities or establish a minimax bound by itself.','file':'CantrellSupports.lean','line':line('CantrellSupports.lean','theorem support_equalities_identify_candidate')}
 ],
 'remaining_for_global_37':'A theorem reducing every arbitrary packing below candidateSide to these same labelled common-angle directed support assumptions, or an exhaustive alternative-family elimination. None of Algebra, Supports, FiniteCover, or an angle minimax theorem supplies it.',
 'remaining_for_exact_attainment':'A full 37-square layout at the exact algebraic side still needs its own containment and 666-pair disjointness proof. A rational packing at a slightly larger side only proves that larger upper bound.',
 'finite_cover_audit':str(root/'analysis/finite_cover_trust.json'),
 'T154_audit':str(root/'analysis/proof17_review.json')
}
(root/'analysis/cantrell_support_review.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(root/'analysis/cantrell_support_review.json')
