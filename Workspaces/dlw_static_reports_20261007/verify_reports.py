"""Verify regrouping against the pre-revision HTML and current workspace inputs."""
import hashlib
import json
import re
from bs4 import BeautifulSoup
import restructure_integrability as build


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify():
    before=BeautifulSoup(build.BEFORE.read_text('utf-8'),'html.parser')
    soup=BeautifulSoup(build.DEST.read_text('utf-8'),'html.parser')
    assert soup.h1.get_text()==before.h1.get_text()
    assert soup.style.get_text()==before.style.get_text()+build.FLOW_CSS
    assert [h.get_text() for h in soup.select('h2')]==[f'{i}. {title}' for i,(title,_) in enumerate(build.GROUPS,1)]
    assert len(soup.select('main>section.theory-stage'))==5
    assert not soup.select('h3,h4')
    expected_cells=['intro']+[cid for _,cids in build.GROUPS for cid in cids]
    assert [node['data-cell'] for node in soup.select('[data-cell]')]==expected_cells
    for stage,(_,cids) in zip(soup.select('.theory-stage'),build.GROUPS):
        assert [node['data-cell'] for node in stage.select(':scope > [data-cell]')]==cids
    actual_math=[str(node) for node in soup.select('[data-formula]')]
    previous_math=[str(node) for node in before.select('[data-formula]')]
    assert actual_math==previous_math
    tex=[node.select_one('annotation').get_text() for node in soup.select('[data-formula]')]
    tags=set(re.findall(r'\\tag\{(\d+)\}','\n'.join(tex)))
    assert tags=={str(i) for i in range(1,20)}
    changed_paragraphs={('intro',0),('coordinates-text',0),('start-text',0),('foundation-text',0),
                        ('energy-text',0),('bracket-text',0),('generic-text',0),('frequency-text',5)}
    actual_changes=set()
    paragraph_count=0
    for cid in expected_cells:
        current=soup.find(attrs={'data-cell':cid})
        previous=before.find(attrs={'data-cell':cid})
        new_paras=current.select('p')
        old_paras=previous.select('p')
        assert len(new_paras)==len(old_paras),cid
        for index,(new,old) in enumerate(zip(new_paras,old_paras)):
            paragraph_count+=1
            if str(new)!=str(old):
                actual_changes.add((cid,index))
                assert (cid,index) in changed_paragraphs,(cid,index)
    assert actual_changes==changed_paragraphs,actual_changes
    assert soup.select_one('#intro > p').get_text()==build.INTRO
    assert len(soup.select('#intro>p'))==1
    assert len(soup.select('pre'))==len(soup.select('code'))==1
    assert soup.select_one('pre code').get_text()==before.select_one('pre code').get_text()
    assert len(soup.select_one('pre code').get_text().splitlines())==4
    assert not soup.select('script,button,input,textarea,iframe,details,summary,.output,.compiler-output')
    assert not soup.select('[href]:not([href^="#"]),[src]:not([src^="data:"])')
    prose=BeautifulSoup(str(soup.main),'html.parser')
    for node in prose.select('[data-formula],pre'): node.decompose()
    assert not re.search(r'第\s*6\s*节',prose.get_text())
    assert '假设每个闭合场都存在' in soup.select_one('#foundation-text').get_text()
    assert '基础成立时' in soup.select_one('#endpoint-text').get_text()
    inputs=json.loads((build.HERE/'before_flow/input_hashes.json').read_text('utf-8'))
    for name,expected in inputs['notebooks_and_numerical'].items():
        assert sha(build.ROOT/name)==expected,name
    assert sha(build.BEFORE)==inputs['report_before_sha256']
    result={'success':True,'major_sections':5,'flow':[title for title,_ in build.GROUPS],
            'all_rendered_mathematical_expressions_exact':True,'numbered_equations':sorted(map(int,tags)),
            'paragraphs':paragraph_count,'only_transitions_reworded':True,
            'changed_paragraphs':sorted([list(x) for x in actual_changes]),
            'code_excerpts':1,'visible_code_lines':4,'math_expressions':len(tex),
            'implementation_prose_absent':True,'appendix_absent':True,
            'explicit_foundation_preserved':True,'font_styles_preserved':True,
            'notebooks_and_numerical_unchanged':True,
            'delivery_sha256':sha(build.DEST),'inputs':inputs['notebooks_and_numerical']}
    (build.HERE/'content_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':
    verify()
