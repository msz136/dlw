"""Static page/link/status and KaTeX checks; does not emulate a browser."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
from collections import Counter
import hashlib, json, re, subprocess

root=Path(__file__).resolve().parents[2]
page=root/'lean_verification.html'
class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids=[]; self.links=[]; self.states=[]; self.text=[]; self.skip=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if tag=='a' and 'href' in a: self.links.append(a['href'])
        if tag=='article' and 'data-state' in a: self.states.append(a['data-state'])
        if tag in ('pre','code','script','style'): self.skip+=1
    def handle_endtag(self,tag):
        if tag in ('pre','code','script','style'): self.skip-=1
    def handle_data(self,s):
        if self.skip==0: self.text.append(s)
p=Page(); p.feed(page.read_text(encoding='utf-8'))
assert len(p.ids)==len(set(p.ids))
bad=[]
for link in p.links:
    u=urlsplit(link)
    if u.scheme: continue
    if not u.path and u.fragment:
        if u.fragment not in p.ids: bad.append(link)
    elif u.path and not (root/unquote(u.path)).exists(): bad.append(link)
assert not bad,bad
states=dict(Counter(p.states))
manifest=json.loads((root/'Paper/dlw_semidiscrete/lean_contracts/status.json').read_text(encoding='utf-8'))
expected={'proved':manifest['proved_count']}
if manifest['unproved_count']: expected['pending']=manifest['unproved_count']
assert states==expected and sum(states.values())==32,states
formulas=[a or b for a,b in re.findall(r'\$\$([\s\S]*?)\$\$|\$([^$]*?)\$', ''.join(p.text))]
js="""const fs=require('fs'),katex=require(process.argv[1]);
const formulas=JSON.parse(fs.readFileSync(0,'utf8'));
for(const s of formulas) katex.renderToString(s,{throwOnError:true});
process.stdout.write(JSON.stringify({compiled:formulas.length}));"""
katex=root/'Paper/gsg_project/dlw_report/_assets/package/dist/katex.js'
compiled=subprocess.run(['node','-e',js,str(katex)],input=json.dumps(formulas),text=True,
                        capture_output=True,check=True)
result={'html_sha256':hashlib.sha256(page.read_bytes()).hexdigest(),
        'states':states,'broken_links':bad,'duplicate_ids':[],
        'math':json.loads(compiled.stdout),
        'browser_visual_check':'Not rerun: browser policy blocked file URL. Static parsing and KaTeX compilation only.'}
(root/'Paper/dlw_semidiscrete/lean_contracts/page_validation_current.json').write_text(
    json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
