"""Generate a paper-style derivation template using local KaTeX assets."""
from pathlib import Path
from urllib.parse import urlsplit
import hashlib
import html
import json
import re
import markdown
from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = HERE / "_src/equations_and_estimates.md"
source = SOURCE.read_text(encoding="utf-8")
formulas = []
equation_count = 0


def protect(match):
    global equation_count
    value = match[0]
    display = value.startswith("$$")
    if display:
        equation_count += 1
        value = value[:-2].rstrip() + rf"\tag{{{equation_count}}}" + "\n$$"
    formulas.append({"text": value, "display": display})
    return f"MATHPLACEHOLDER{len(formulas)-1}END"


protected = re.sub(r"\$\$[\s\S]*?\$\$|\$[^$\n]+\$", protect, source)
if "$" in protected:
    raise ValueError("Unmatched math delimiter")
body = markdown.markdown(protected, extensions=["tables", "md_in_html"])
for i, entry in enumerate(formulas):
    body = body.replace(f"MATHPLACEHOLDER{i}END",
                        html.escape(entry["text"], quote=False))
soup = BeautifulSoup(body, "html.parser")
toc_items = []
for i, heading in enumerate(soup.find_all("h2"), 1):
    heading["id"] = f"section-{i}"
    toc_items.append(f'<li><a href="#section-{i}">{html.escape(heading.get_text())}</a></li>')
for i, table in enumerate(soup.find_all("table"), 1):
    wrapper = soup.new_tag("div", attrs={
        "class": "table-wrap", "tabindex": "0", "role": "region",
        "aria-label": f"表 {i}，可横向滚动"})
    table.wrap(wrapper)
    for th in table.find_all("th"):
        th["scope"] = "col"
for p in soup.find_all("p"):
    if p.get_text().strip().startswith("$$"):
        p["class"] = ["equation"]
for a in soup.find_all("a", href=True):
    href = a["href"]
    if not urlsplit(href).scheme and not href.startswith("#"):
        target = (SOURCE.parent / href).resolve()
        if not target.is_file():
            raise FileNotFoundError(target)
        a["href"] = '../' + target.relative_to(ROOT).as_posix()

toc = BeautifulSoup(
    '<nav aria-label="文章目录"><details open><summary>目录</summary><ol>'
    + "".join(toc_items) + "</ol></details></nav>", "html.parser")
soup.find("h2").insert_before(toc)
css = """
*{box-sizing:border-box}
html{scroll-padding-top:24px}
body{margin:0;color:#171717;background:#f0efec;font:17px/1.95 "Times New Roman","SimSun",serif}
main{max-width:1040px;margin:36px auto;padding:64px 76px 72px;background:#fff}
h1{font-size:29px;line-height:1.5;letter-spacing:.035em;text-align:center;margin:0 0 8px}
.subtitle{text-align:center!important;text-indent:0!important;color:#666;font-size:15px;margin:0 0 30px}
.abstract{text-indent:0!important;font-size:16px;line-height:1.9;border-top:1px solid #bbb;border-bottom:1px solid #bbb;padding:17px 0;margin:24px 0}
h2{font-size:23px;line-height:1.6;margin:45px 0 19px;break-after:avoid}
h3{font-size:18px;line-height:1.65;margin:28px 0 12px;break-after:avoid}
p{margin:13px 0;text-align:justify;text-indent:2em;overflow-wrap:break-word}
a{color:#254b68;text-decoration-thickness:1px;text-underline-offset:3px}
a:focus-visible,summary:focus-visible,.table-wrap:focus-visible{outline:2px solid #254b68;outline-offset:4px}
nav{font-size:15px;line-height:1.9;margin:26px 0 34px;border-bottom:1px solid #d5d5d5;padding-bottom:20px}
nav summary{cursor:pointer;font-weight:bold;width:max-content}
nav ol{columns:2;column-gap:35px;list-style:none;padding:0;margin:13px 0 0}
nav li{break-inside:avoid;padding:3px 0}
nav a{text-decoration:none}
.equation{text-indent:0;margin:17px 0}
.katex{font-size:1.03em}
.katex-display{overflow-x:auto;overflow-y:hidden;padding:12px 4px;font-size:.96em;margin:.5em 0}
.katex-display>.katex>.katex-html{display:flex;align-items:center;width:max-content;min-width:100%}
.katex-display .formula-body{display:inline-block;margin-inline:auto}
.katex-display>.katex>.katex-html>.katex-tag{position:static;flex:none;margin-left:2em}
.table-wrap{overflow-x:auto;margin:22px 0}
table{width:100%;border-collapse:collapse;font-size:15px;line-height:1.8;border-top:1.5px solid #333;border-bottom:1.5px solid #333;min-width:650px}
th,td{padding:11px 12px;text-align:left;vertical-align:top}
th{border-bottom:1px solid #777;font-weight:bold}
td{border-bottom:1px solid #e4e4e4}
tr:last-child td{border-bottom:0}
.references{margin-top:38px;padding-top:10px;border-top:1px solid #aaa;font-size:14px;line-height:1.9}
.references p{text-indent:0;text-align:left}
@media(max-width:700px){
 body{font-size:16px;line-height:1.85;background:#fff}
 main{margin:0;padding:32px 19px 42px}
 h1{font-size:24px}h2{font-size:20px;margin-top:36px}h3{font-size:17px}
 .subtitle{font-size:13px}.abstract{font-size:15px}
 nav ol{columns:1}.katex-display{font-size:.84em}
}
@media print{
 @page{size:A4;margin:20mm 18mm}
 body{background:white;font-size:10.5pt;line-height:1.75}
 main{max-width:none;margin:0;padding:0}
 h1{font-size:18pt}h2{font-size:14pt}h3{font-size:12pt}
 nav{display:none}.abstract{font-size:10.5pt}.subtitle{font-size:10pt}
 .katex-display{font-size:.84em;overflow:visible}
 .table-wrap{overflow:visible}table{min-width:0;font-size:9pt}
 a{color:inherit;text-decoration:none}
}
"""
page = """<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="从连续与半离散DLW方程推导SD、SDR、FD的误差阶、主系数、参数依赖和误差传播。">
<title>DLW：从初始方程到误差估计</title>
<style>@@KATEX_CSS@@</style><style>""" + css + """</style></head>
<body><main>""" + str(soup) + """</main>
<script>@@KATEX_JS@@</script>
<script>
renderMathInElement(document.querySelector("main"),{
delimiters:[{left:"$$",right:"$$",display:true},{left:"$",right:"$",display:false}],
throwOnError:false,strict:"ignore"});
document.querySelectorAll(".katex-display > .katex > .katex-html").forEach(container=>{
 const tag=container.querySelector(":scope > .katex-tag");
 if(!tag)return;
 const body=document.createElement("span");
 body.className="formula-body";
 Array.from(container.childNodes).filter(node=>node!==tag).forEach(node=>body.appendChild(node));
 container.prepend(body);
});
document.documentElement.dataset.mathReady="true";
</script></body></html>"""
(HERE / "_src/dlw_error_theory.src.html").write_text(page, encoding="utf-8")
(HERE / "html_manifest.json").write_text(json.dumps({
    "source": str(SOURCE), "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    "equations": equation_count, "math_segments": len(formulas),
    "sections": len(toc_items), "formulas": formulas
}, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({"equations": equation_count, "math_segments": len(formulas),
                  "sections": len(toc_items)}, ensure_ascii=False))
