"""Export the theory manuscript as a self-contained HTML reading copy.

Uses Python Markdown when available, otherwise Pandoc. Existing embedded KaTeX
assets can be reused, so editorial rebuilds also work in a small cloud checkout.
"""
from pathlib import Path
import base64, html, json, os, re, shutil, subprocess, sys
from fontTools import subset
from fontTools.ttLib import TTFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
source = (HERE / 'paper.src.md').read_text(encoding='utf-8')
formulas = []
def store_math(match):
    display = match.group().startswith('$$')
    tex = match.group()[2:-2] if display else match.group()[1:-1]
    i = len(formulas)
    formulas.append({'tex': tex, 'display': display})
    return f'MATHPLACEHOLDER{i}END'
text = re.sub(r'\$\$[\s\S]*?\$\$|(?<!\$)\$(?!\$)[^\n$]+\$', store_math, source)
try:
    import markdown
    body = markdown.markdown(text, extensions=['tables'])
except ImportError:
    pandoc = shutil.which('pandoc')
    if not pandoc:
        raise RuntimeError('Install Python Markdown or Pandoc to export the manuscript.')
    body = subprocess.run([pandoc, '-f', 'markdown+raw_html', '-t', 'html5'],
                          input=text, text=True, encoding='utf-8', check=True,
                          stdout=subprocess.PIPE).stdout
(HERE / 'formulas.json').write_text(json.dumps(formulas, ensure_ascii=False), encoding='utf-8')
subprocess.run([os.environ.get('NODE', 'node'), str(HERE / 'render_math.cjs')], check=True)
rendered = json.loads((HERE / 'rendered_math.json').read_text(encoding='utf-8'))
body = re.sub(r'MATHPLACEHOLDER(\d+)END', lambda m: rendered[int(m[1])], body)

assets = ROOT / 'Workspaces/gsg_project/dlw_report/_assets/package/dist'
css_path = assets / 'katex.css'
if css_path.exists():
    kcss = css_path.read_text(encoding='utf-8')
    kcss = re.sub(r'src: (url\([^)]*\.woff2\) format\("woff2"\))[^;]*;', r'src: \1;', kcss)
    def font_url(match):
        value = match[1].strip('"\'')
        if value.startswith('data:'):
            return match[0]
        return 'url(data:font/woff2;base64,' + base64.b64encode((assets / value).read_bytes()).decode() + ')'
    kcss = re.sub(r'url\(([^)]+)\)', font_url, kcss)
else:
    previous = (ROOT / 'report/dlw_theory.html').read_text(encoding='utf-8')
    style = re.search(r'<style>([\s\S]*?)</style>', previous)[1]
    kcss = style.split('@font-face{font-family:PaperSerif;')[0]
    if 'KaTeX_Main' not in kcss:
        raise RuntimeError('The existing HTML does not contain embedded KaTeX styles.')

font_path = os.environ.get('DLW_PAPER_FONT')
if not font_path:
    candidates = ['C:/Windows/Fonts/NotoSerifSC-VF.ttf',
                  '/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc']
    font_path = next((p for p in candidates if Path(p).is_file()), None)
if font_path:
    font = TTFont(font_path, fontNumber=2) if font_path.lower().endswith('.ttc') else TTFont(font_path)
    if 'fvar' in font:
        from fontTools.varLib.instancer import instantiateVariableFont
        font = instantiateVariableFont(font, {'wght': 400}, inplace=True)
    options = subset.Options()
    sub = subset.Subsetter(options=options)
    sub.populate(text=source)
    sub.subset(font)
    font.flavor = 'woff'
    font.save(HERE / 'paper-serif.woff')
font_file = HERE / 'paper-serif.woff'
fontcss = ''
if font_file.exists():
    fontcss = "@font-face{font-family:PaperSerif;src:url(data:font/woff;base64," + base64.b64encode(font_file.read_bytes()).decode() + ") format('woff');font-weight:400;font-style:normal;font-display:block}"
css = kcss + fontcss + '''
*{box-sizing:border-box}html,body{margin:0;background:#fff;color:#000}
body{font-family:KaTeX_Main,PaperSerif,"Noto Serif CJK SC","Songti SC",SimSun,serif;font-size:16px;line-height:1.9;font-weight:400}
main{width:100%;max-width:960px;margin:0 auto;padding:58px 48px 88px}
h1{font-family:PaperSerif,serif;font-size:25px;line-height:1.65;font-weight:600;text-align:center;margin:0 0 28px;letter-spacing:.035em}
h2{font-size:19px;line-height:1.65;margin:32px 0 14px;font-weight:600}
h3{font-size:16px;line-height:1.7;margin:23px 0 10px;font-weight:600}
p{margin:11px 0;text-align:justify;overflow-wrap:break-word}
.abstract{font-size:14px;line-height:1.85;margin:0 26px 26px;text-align:justify}
.abstract-label{font-weight:600;margin-right:1em}
strong{font-weight:600}.eq{display:block;overflow-x:auto;overflow-y:hidden;padding:9px 1px;margin:5px 0}
.katex{font-size:1.04em}.katex-display{margin:.65em 0}.katex-display>.katex{white-space:nowrap}
a{color:#222;text-decoration-thickness:1px;text-underline-offset:.16em}
@media(max-width:650px){main{padding:28px 18px 50px}body{font-size:15px}h1{font-size:21px}.abstract{margin:0 3px 24px}h2{font-size:18px}}
@page{size:A4;margin:20mm 18mm}
@media print{body{font-size:10.5pt;line-height:1.7}main{max-width:none;padding:0 3px}h1{font-size:16pt}h2{font-size:12pt;break-after:avoid}.eq{overflow:visible;break-inside:avoid}p{orphans:3;widows:3}.abstract{font-size:9.5pt}}
'''
title = next(line[2:].strip() for line in source.splitlines() if line.startswith('# '))
dest = HERE / 'preview.html' if '--preview' in sys.argv or '--input' in sys.argv else ROOT / 'report/dlw_theory.html'
dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_text('<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + html.escape(title) + '</title><style>' + css + '</style></head><body><main>' + body + '</main></body></html>', encoding='utf-8')
print('Offline HTML:', dest, 'formulas:', len(formulas))
