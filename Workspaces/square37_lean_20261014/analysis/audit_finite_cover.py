from pathlib import Path
import hashlib, json, re

root = Path(__file__).resolve().parents[1]
source = root/'lean/FiniteCover.lean'
run = root/'lean/.lean-runs/20261014_155639_bf16da4f'
receipt = json.loads((run/'result.json').read_text(encoding='utf-8'))
log = (run/'build.log').read_text(encoding='utf-8')
actual = hashlib.sha256(source.read_bytes()).hexdigest()
assert receipt['status'] == 'PASSED'
assert receipt['files'][0]['sha256'] == actual
parsed = re.findall(r"'([^']+)' depends on axioms: \[([^]]*)\]", log)
assert len(parsed) == 6
entries = [{'theorem':name,'axioms':[s.strip() for s in axioms.split(',')]} for name,axioms in parsed]
assert all(set(e['axioms']) <= {'propext','Classical.choice','Quot.sound'} for e in entries)
scope = {
'exhaustive_of_nodup_card':'For arbitrary n,m, a list of distinct n-element subsets of Fin m whose length is choose(m,n) contains every n-element subset. Validity, distinctness, and exact length are explicit hypotheses.',
'property_of_complete_census':'Any property verified on every row of such a census holds for every n-element subset. This transfers a provided property; it does not generate row proofs.',
'injective_assignment_of_capacity':'If every indexed owner belongs to at least one cell and no two different owners may belong to the same cell, there is an injective cell assignment. The geometric meaning and capacity proof are explicit external hypotheses.',
'image_eq_of_exact_occupancy':'An injective assignment of n owners with image contained in an n-element occupied set has image equal to that set.',
'equiv_reindex_of_image_eq':'Injective rosters Fin n -> Fin m with equal images can be matched by an actual equivalence Fin n ≃ Fin n. The assigned-injective hypothesis is redundant but retained in the symmetric interface.',
'equiv_reindex_of_exact_occupancy':'An injective assignment filling an n-element occupied set can be permuted to any injective roster with that same image.'}
for entry in entries:
    entry['scope']=scope[entry['theorem'].split('.')[-1]]
    entry['line']=next(i for i,s in enumerate(source.read_text(encoding='utf-8').splitlines(),1) if s.startswith('theorem '+entry['theorem'].split('.')[-1]+' '))
result = {'source':str(source),'sha256':actual,'build_receipt':str(run/'result.json'),
          'status':'PASSED_AND_AXIOM_REPORT_REVIEWED','toolchain':receipt['toolchain'],
          'mathlib_commit':receipt['mathlib_commit'],'theorems':entries,
          'no_native_decide': 'native_decide' not in source.read_text(encoding='utf-8'),
          'scope_limit':'No 37-cell cover, capacity certificate, exhaustive roster list, orbit action, or exclusion tree is supplied or asserted by this module. It is an abstract verified bridge only.',
          'T154_review':str(root/'analysis/proof17_review.json')}
(root/'analysis/finite_cover_trust.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':result['status'],'theorem_count':len(entries),'sha256':actual}))
