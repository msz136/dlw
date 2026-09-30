"""Build a standalone illustrated HTML report from GSG_STYLE_REPORT.md.

The HTML is generated; edit the Markdown source and rerun this script.
"""
import base64
import html
import re
from pathlib import Path
import markdown

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'GSG_STYLE_REPORT.md'
TARGET=ROOT/'GSG_STYLE_REPORT.html'
DIST=ROOT.parent/'gsg_project'/'dlw_report'/'_assets'/'package'/'dist'

source=SOURCE.read_text(encoding='utf-8')
math=[]
def placeholder(match,display):
    key=f'MATHTOKEN{len(math):05d}END'
    math.append((key,match.group(1),display))
    return key
source=re.sub(r'\$\$([\s\S]*?)\$\$',lambda m:placeholder(m,True),source)
source=re.sub(r'(?<!\$)\$([^$\n]+)\$(?!\$)',lambda m:placeholder(m,False),source)
body=markdown.markdown(source,extensions=['tables','fenced_code','toc'])
for key,tex,display in math:
    tag='div' if display else 'span'
    fragment=f'<{tag} class="math-{"display" if display else "inline"}" data-tex="{html.escape(tex.strip().replace(chr(13),""),quote=True)}"></{tag}>'
    if display:
        body=body.replace(f'<p>{key}</p>',fragment)
    body=body.replace(key,fragment)

def inline_png(match):
    path=ROOT/match.group(1)
    content=base64.b64encode(path.read_bytes()).decode('ascii')
    return f'src="data:image/png;base64,{content}"'
body=re.sub(r'src="(out/figures/[^"]+\.png)"',inline_png,body)

css=(DIST/'katex.min.css').read_text(encoding='utf-8')
def inline_font(match):
    name=match.group(1).strip('"\' ')
    path=DIST/name
    if not path.is_file(): return match.group(0)
    extension=path.suffix.lstrip('.')
    mime='font/woff2' if extension=='woff2' else 'font/woff' if extension=='woff' else 'font/ttf'
    payload=base64.b64encode(path.read_bytes()).decode('ascii')
    return f'url(data:{mime};base64,{payload})'
css=re.sub(r'url\(([^)]+)\)',inline_font,css)
js=(DIST/'katex.min.js').read_text(encoding='utf-8')

page=f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>2-HS 的 GSG 式数值研究</title>
<style>{css}</style>
<style>
:root{{color-scheme:light}} body{{font-family:system-ui,-apple-system,"Segoe UI",sans-serif;color:#18212b;background:#f7f9fc;margin:0;line-height:1.7}}
main{{max-width:1060px;margin:0 auto;padding:36px 30px 80px;background:white;box-shadow:0 0 28px #d8e0e8}}
h1,h2,h3{{line-height:1.25;color:#102941;scroll-margin-top:16px}} h1{{font-size:2.05rem}} h2{{margin-top:2.3rem;border-bottom:1px solid #d9e2eb;padding-bottom:.35rem}} h3{{margin-top:1.5rem}}
p,li{{max-width:85ch}} table{{border-collapse:collapse;width:100%;font-size:.94rem;margin:1rem 0 1.6rem}}
th,td{{border:1px solid #d7e0e8;padding:7px 9px;vertical-align:top}} th{{background:#edf4f9;text-align:left}} tr:nth-child(even){{background:#fafcff}}
img{{max-width:100%;height:auto;display:block;margin:1.3rem auto .3rem}} img+p{{font-size:.92rem;color:#52677c}}
.math-display{{overflow-x:auto;text-align:center;margin:1rem 0}} .math-inline{{white-space:nowrap}}
pre{{overflow-x:auto;background:#eef3f8;padding:14px;border-radius:6px}} code{{font-family:ui-monospace,Consolas,monospace}} a{{color:#126293}}
@media(max-width:700px){{main{{padding:20px 13px}}table{{display:block;overflow-x:auto}}h1{{font-size:1.6rem}}}}
</style></head><body><main>{body}</main><script>{js}</script>
<script>document.querySelectorAll('[data-tex]').forEach(el=>{{try{{katex.render(el.getAttribute('data-tex'),el,{{displayMode:el.classList.contains('math-display'),throwOnError:true,strict:'ignore'}})}}catch(e){{el.classList.add('math-error');el.textContent=e.message}}}});</script>
</body></html>'''
TARGET.write_text(page,encoding='utf-8')
print(f'Built {TARGET} ({TARGET.stat().st_size:,} bytes, {len(math)} math expressions)')
