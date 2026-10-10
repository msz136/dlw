from pathlib import Path
import hashlib,json,re

HERE=Path(__file__).resolve().parent
before=(HERE/'before_prose_revision/compact_manuscript.md').read_text(encoding='utf-8')
after=(HERE/'compact_manuscript.md').read_text(encoding='utf-8')
def numbered(text):
    result={}
    for block in re.findall(r'\$\$([\s\S]*?)\$\$',text):
        tag=re.search(r'\\tag\{(\d+)\}',block)
        if tag:result[tag[1]]=block
    return result
assert numbered(before)==numbered(after)
assert len(numbered(after))==12
assert len(re.findall(r'^## ',after,re.M))==4
assert r'\gamma' not in after
result={'numbered_formulas_unchanged':12,'sections':4,'scope':'prose and explanatory compatibility calculation','source_sha256':hashlib.sha256(after.encode()).hexdigest()}
(HERE/'prose_revision_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
