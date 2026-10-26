"""Add the four selected transparent surfaces next to existing paper figures.

Changes only Section 5.2 in the manuscript and its numerical mirror. Existing
figures and numerical data remain in place. The figure gallery is synchronized.
"""
from pathlib import Path
import hashlib, json, re, shutil, sys
from bs4 import BeautifulSoup

HERE=Path(__file__).resolve().parent
PROJECT=HERE.parent
ROOT=PROJECT.parents[2]
sys.path.insert(0,str(PROJECT))
from validate_publication import raw_section

PAPER=ROOT/'dlw-paper.html'
DRAFT=ROOT/'report/dlw_numerical_text_20261025.html'
GALLERY=ROOT/'report/dlw_uv_figure_choices_20261025.html'
PREFIX='Workspaces/dlw_paper_20261009/spatial_ad_uv_20261025/surface_only_20261025/figures/'
CASES=['A','D','Gaussian','Sinusoidal']
texts={p:p.read_text(encoding='utf-8') for p in [PAPER,DRAFT,GALLERY]}
assert 'data-view="surface"' not in texts[PAPER], 'Surfaces already inserted; edit in place.'
backup=HERE/'before_paper_insertion'
backup.mkdir(exist_ok=True)
for path in [PAPER,DRAFT,GALLERY,PROJECT/'section-5.2.html',PROJECT/'publication.json',PROJECT/'publication_validation.json']:
    if path.exists():
        dest=backup/path.name
        assert not dest.exists(), ('Existing backup',dest)
        shutil.copy2(path,dest)

old=raw_section(texts[PAPER],'section-5.2')
figures=list(re.finditer(r'<figure\b[^>]*>.*?</figure>',old,re.S))
assert len(figures)==12
new_figures={}
counter=8

def renumber(block,number):
    block=re.sub(r'id="figure-\d+"',f'id="figure-{number}"',block,count=1)
    return re.sub(r'<strong>Figure \d+\.</strong>',f'<strong>Figure {number}.</strong>',block,count=1)

def replace_figure(match):
    global counter
    block=match.group()
    parsed=BeautifulSoup(block,'html.parser').figure
    case,view=parsed['data-case'],parsed['data-view']
    counter+=1
    block=renumber(block,counter)
    new_figures[(case,view)]=block
    if view!='overlay':return block
    surface=block.replace('data-view="overlay"','data-view="surface"',1)
    surface=re.sub(r'src="[^"]+"',f'src="{PREFIX}plain_{case}.png"',surface,count=1)
    surface=surface.replace('terminal physical-field overlay comparison','terminal absolute physical-field error surfaces')
    surface=surface.replace('The three spatial formulations on common three-dimensional axes at','Absolute physical-field errors at',1)
    surface=surface.replace('Transparent surfaces and colored wireframes retain the same physical coordinates and linear height scale.','The three methods share the same spatial coordinates and linear height scale within each panel.',1)
    surface=re.sub(r' <a class="export"[^>]*>PDF</a>','',surface)
    counter+=1
    surface=renumber(surface,counter)
    new_figures[(case,'surface')]=surface
    return block+'\n'+surface

updated=re.sub(r'<figure\b[^>]*>.*?</figure>',replace_figure,old,flags=re.S)
assert counter==24
updated=updated.replace('The heatmaps locate the errors in the plane. The separate and overlaid three-dimensional views show the same absolute error fields as surface heights, using a common linear height scale for each component.','The heatmaps locate the errors in the plane, while the surface heights show their magnitude on a common linear scale for each physical component.')
paper=texts[PAPER].replace(old,updated,1)
old_draft=raw_section(texts[DRAFT],'section-5.2')
draft_section=updated.replace('src="Workspaces/','src="../Workspaces/').replace('href="Workspaces/','href="../Workspaces/')
draft=texts[DRAFT].replace(old_draft,draft_section,1)

gallery=texts[GALLERY]
for case in CASES:
    for view in ['heatmap','separate','overlay']:
        pattern=r'<figure\b[^>]*\bid="choice-'+view+'-'+case+r'"[^>]*>.*?</figure>'
        found=re.search(pattern,gallery,re.S)
        assert found,(case,view)
        def gallery_figure(v):
            f=new_figures[(case,v)]
            f=re.sub(r'id="figure-\d+"',f'id="choice-{v}-{case}"',f,count=1)
            return f.replace('src="Workspaces/','src="../Workspaces/').replace('href="Workspaces/','href="../Workspaces/')
        replacement=gallery_figure(view)
        if view=='overlay':replacement+='<h3>Physical-field error surfaces</h3>'+gallery_figure('surface')
        gallery=gallery[:found.start()]+replacement+gallery[found.end():]

assert paper.replace(updated,'__SECTION__',1)==texts[PAPER].replace(old,'__SECTION__',1)
for path in texts:
    assert path.read_text(encoding='utf-8')==texts[path],('Concurrent edit',path)
for path,text in [(PAPER,paper),(DRAFT,draft),(GALLERY,gallery),(PROJECT/'section-5.2.html',updated)]:
    path.write_text(text,encoding='utf-8')
record=json.loads((PROJECT/'publication.json').read_text(encoding='utf-8'))
record.update(paper_sha256=hashlib.sha256(PAPER.read_bytes()).hexdigest(),surface_only_3d_groups=4,total_figure_groups=24,current_additive_publisher='surface_only_20261025/insert_into_paper.py')
(PROJECT/'publication.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
out=dict(paper_sha256=record['paper_sha256'],previous_paper_sha256=hashlib.sha256((backup/PAPER.name).read_bytes()).hexdigest(),added_cases=CASES,added_figure_numbers=[12,16,20,24],existing_figures_retained=True,only_main_section_changed='section-5.2',figure_count=24,source_manifest_sha256=hashlib.sha256((HERE/'manifest.json').read_bytes()).hexdigest(),artifacts={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [PAPER,DRAFT,GALLERY]})
(HERE/'publication.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
