from pathlib import Path
import re,json
P=Path(__file__).resolve().parents[1]
s=(P/"manuscript.md").read_text(encoding="utf-8")
old=(P/"discussion_revision_20261020/133537/manuscript.md.before").read_text(encoding="utf-8")
math=re.findall(r"\$\$([\s\S]*?)\$\$",s)
numbered=[x for x in math if r"\tag{" in x]
assert len(numbered)==222,len(numbered)
diff=[i+1 for i,(a,b) in enumerate(zip(numbered[:111],numbered[111:])) if a!=b]
assert not diff,diff
for lang in ("en","zh"):
    oldids=set(re.findall(r'id="('+lang+r'-[^"]+)"',old))
    newids=set(re.findall(r'id="('+lang+r'-[^"]+)"',s))
    assert oldids <= newids,oldids-newids
assert "5.359819e-05" in s
assert "5.394819" not in s
assert "In particular, the spatial error coefficients can help identify" not in s
assert "It also suggests a direction for extending the present work" not in s
assert "[Insert" not in s
for lang in ("en","zh"):
    a=s.index("{#"+lang+"-app-f}")
    b=s.index("{#"+lang+"-references}",a)
    assert "<table" not in s[a:b]
    assert "PE_time_profiles" not in s[a:b]
result={"numbered_equations_identical_across_languages":True,"all_equation_anchors_preserved":True,
        "comparison_tables_moved_out_of_appendix":True,"reverted_conclusion_confirmed":True,
        "CN_case_C_v":5.359819e-5}
(P/"discussion_revision_20261020/content_validation.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
print(result)
