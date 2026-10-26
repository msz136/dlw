from pathlib import Path
import re,json,subprocess,markdown
r=Path('review');source=(r/'revised.md').read_text(encoding='utf8'); old=(r/'original.html').read_text(encoding='utf8')
css='\n'.join(re.findall(r'<style[^>]*>([\s\S]*?)</style>',old));formulas=[]
def slot(m):
 d=m[0].startswith('$$');formulas.append({'tex':m[0][2:-2] if d else m[0][1:-1],'display':d});return f'MATHSLOT{len(formulas)-1}END'
text=re.sub(r'\$\$[\s\S]*?\$\$|(?<!\$)\$(?!\$)[^\n$]+\$',slot,source)
text=re.sub(r'^<nav>.*?</nav>\s*','',text)
parts=re.split(r'(?m)(?=^# .*\{#zh-title\}\s*$)',text,maxsplit=1); assert len(parts)==2
(r/'formulas.json').write_text(json.dumps(formulas,ensure_ascii=False),encoding='utf8')
subprocess.run(['node','render_review.cjs'],check=True)
rendered=json.loads((r/'rendered.json').read_text(encoding='utf8'))
def render(t):
 t=markdown.markdown(t,extensions=['tables','attr_list']);t=re.sub(r'MATHSLOT(\d+)END',lambda m:rendered[int(m[1])],t)
 return re.sub(r'<p>(<div class="eq">[\s\S]*?</div>)</p>',r'\1',t)
body='<article lang="en" id="english">'+render(parts[0])+'</article><article lang="zh-CN" id="chinese">'+render(parts[1])+'</article>'
page=old[:old.index('<main>')]+'<main>'+body+'</main></body></html>'
(r/'dlw_paper_draft.html').write_text(page,encoding='utf8')
print('built',len(formulas),'math items',len(page),'characters')
