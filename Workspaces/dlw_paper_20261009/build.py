"""Build the English-then-Chinese paper from the single manuscript source."""
from pathlib import Path
import html,json,re,subprocess
try:
 import markdown
except ImportError:
 markdown=None
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
dest=ROOT/'report/dlw_paper_draft.html'
source=(HERE/'manuscript.md').read_text(encoding='utf-8')
oldpage=dest.read_text(encoding='utf-8')
css='\n'.join(re.findall(r'<style[^>]*>([\s\S]*?)</style>',oldpage))
formulas=[]
def slot(m):
 display=m[0].startswith('$$')
 formulas.append({'tex':m[0][2:-2] if display else m[0][1:-1],'display':display})
 return f'MATHSLOT{len(formulas)-1}END'
text=re.sub(r'\$\$[\s\S]*?\$\$|(?<!\$)\$(?!\$)[^\n$]+\$',slot,source)
# Each language is an independent article; equation anchors are language-prefixed.
text=re.sub(r'^<nav>.*?</nav>\s*','',text)
parts=re.split(r'(?m)(?=^# .*\{#zh-title\}\s*$)',text,maxsplit=1)
assert len(parts)==2,'Expected English manuscript followed by Chinese manuscript'
def markdown_html(text):
 if markdown is not None:
  return markdown.markdown(text,extensions=['tables','attr_list'])
 return subprocess.run(['pandoc','-f','markdown+raw_html+header_attributes','-t','html','--wrap=none'],input=text,text=True,capture_output=True,check=True).stdout
bodies=[markdown_html(p) for p in parts]
(HERE/'formulas.json').write_text(json.dumps(formulas,ensure_ascii=False),encoding='utf-8')
subprocess.run(['node',str(HERE/'render.cjs')],check=True)
rendered=json.loads((HERE/'rendered.json').read_text(encoding='utf-8'))
def render(s):
 s=re.sub(r'MATHSLOT(\d+)END',lambda m:rendered[int(m[1])],s)
 return re.sub(r'<p>(<div class="eq">[\s\S]*?</div>)</p>',r'\1',s)
body='<article lang="en" id="english">'+render(bodies[0])+'</article><article lang="zh-CN" id="chinese">'+render(bodies[1])+'</article>'
page='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DLW paper — English and Chinese</title><style>'+css+'</style></head><body><div class="language-nav"><a href="#en-title">English manuscript</a><a href="#zh-title">中文全文</a></div><main>'+body+'</main></body></html>'
tags=[int(n) for f in formulas for n in re.findall(r'\\tag\{(\d+)\}',f['tex'])]
assert len(tags)%2==0
n=len(tags)//2
assert tags==list(range(1,n+1))*2
assert 'MATHSLOT' not in page
ids=re.findall(r'\bid="([^"]+)"',page)
assert len(ids)==len(set(ids)),'Duplicate HTML IDs'
assert all(a[1:] in ids for a in re.findall(r'href="(#[^"]+)"',page))
missing=sorted({a for a in re.findall(r'(?:href|src)="([^"#]+)"',page) if not a.startswith(('https://','http://','data:')) and not (dest.parent/a).exists()})
dest.write_text(page,encoding='utf-8')
result={'languages':['en','zh-CN'],'equations_per_language':n,'math_items':len(formulas),'katex_strict':True,'unique_ids':True,'internal_links_valid':True,'missing_local_assets':missing,'visual_review':'not performed by this build script'}
(HERE/'build_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
