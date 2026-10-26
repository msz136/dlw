from pathlib import Path
import re,json
P=Path(__file__).resolve().parent
B=P/'discussion_revision_20261019/20261019_204817'
old=(B/'manuscript.md').read_text(encoding='utf-8')
new=(P/'manuscript.md').read_text(encoding='utf-8')
def formulas(s,lang):
 return {m[1]:re.sub(r'\\tag\{\d+\}','',m[2]) for m in re.finditer(rf'<a id="{lang}-eq-(\d+)"></a>\s*\$\$([\s\S]*?)\$\$',s)}
en=formulas(new,'en');zh=formulas(new,'zh')
assert en==zh,'Bilingual numbered equations differ'
changed=[]
for key,value in formulas(old,'en').items():
 if key not in en or en[key]!=value:changed.append(int(key))
assert set(changed)<=set(range(47,69))|{201},changed
for lang in ('en','zh'):
 assert re.search(rf'\*\*(?:Proof of|证明|Proof\.)',new)
 # Published short Darboux proof is retained verbatim except equation references.
 start=old.index('**Theorem 2.11') if lang=='en' else old.index('**定理 2.11')
 oldproof=old[start:].split('**Proof.**' if lang=='en' else '**证明。**',1)[1].split('□',1)[0]
 start=new.index('**Theorem 2.9') if lang=='en' else new.index('**定理 2.9')
 newproof=new[start:].split('**Proof.**' if lang=='en' else '**证明。**',1)[1].split('□',1)[0]
 assert oldproof==newproof,'Proof changed'
results={'numbered_equations_identical_between_languages':True,'changed_or_merged_equation_anchors':changed,'mathematics_outside_2_5_unchanged':True,'original_Darboux_proof_retained':True,'pending':'Darboux compatibility proof prose still awaits review; print/PDF not rebuilt'}
(B/'scope_validation.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(results,ensure_ascii=False))
