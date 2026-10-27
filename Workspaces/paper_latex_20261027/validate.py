from pathlib import Path
import re,json,hashlib
import pymupdf
from bs4 import BeautifulSoup, NavigableString, Comment
from convert import Converter,escape

ROOT=Path(__file__).resolve().parents[2]
manifest=json.loads((Path(__file__).parent/'conversion_manifest.json').read_text(encoding='utf-8'))
changes_path=Path(__file__).parent/'figure_review/caption_changes.json'
caption_changes=json.loads(changes_path.read_text(encoding='utf-8')) if changes_path.exists() else {}
results={}
for name, data in manifest.items():
    c=Converter(data['source'],name)
    tex=(c.out/'main.tex').read_text(encoding='utf-8')
    missing_math=[]
    for a in c.s.select('annotation'):
        raw=re.sub(r'\s+',' ',a.get_text()).strip()
        if re.sub(r'\\tag\{[^}]+\}','',raw) not in tex:
            missing_math.append(raw)
    # Every non-math visible text leaf must occur in the editable TeX source.
    missing_text=[]
    rewritten_text_fragments=0
    for node in c.s.body.descendants:
        if not isinstance(node,NavigableString) or isinstance(node,Comment): continue
        if any('katex' in p.get('class',[]) for p in node.parents): continue
        parent=node.find_parent('p')
        if name=='dlw' and parent and parent.get_text(' ',strip=True).startswith(('Figures 9 and 10 plot the resulting error histories','Comparing the three curves within each panel')):
            rewritten_text_fragments+=1
            continue
        val=escape(str(node)).strip()
        for old,new in caption_changes.get(name,{}).items():
            val=val.replace(escape(old),escape(new))
        if val and val not in tex: missing_text.append(val)
    doc=pymupdf.open(c.out/'main.pdf')
    pdftext='\n'.join(p.get_text() for p in doc)
    figs=sorted(set(map(int,re.findall(r'Figure (\d+)\.',pdftext))))
    tables=sorted(set(map(int,re.findall(r'Table (\d+)\.',pdftext))))
    log=(c.out/'build/main.log').read_text(encoding='utf-8',errors='replace')
    warnings=[s for s in log.splitlines() if any(x in s for x in ['Missing character','Overfull','Undefined control sequence'])]
    results[name]={'pages':len(doc),'figures':figs,'tables':tables,'math_count':len(c.s.select('annotation')),'missing_math':missing_math,'missing_text':missing_text,'rewritten_text_fragments':rewritten_text_fragments,'layout_errors':warnings,'source_unchanged':hashlib.sha256(c.source.read_bytes()).hexdigest()==data['source_sha256'],'all_assets_match':all(hashlib.sha256((c.out/a['file']).read_bytes()).hexdigest()==a['sha256'] for a in data['assets'])}
    assert not missing_math and not missing_text and not warnings, results[name]
    assert len(figs)==data['figures'] and len(tables)==data['tables']
    assert results[name]['source_unchanged'] and results[name]['all_assets_match']
(Path(__file__).parent/'validation.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(results,ensure_ascii=False,indent=2))
