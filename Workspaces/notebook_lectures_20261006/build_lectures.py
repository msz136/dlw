"""Wrap source-grounded lecture fragments with local typography and math."""
from __future__ import annotations
import base64
import hashlib
import html
import json
from pathlib import Path
import re

from bs4 import BeautifulSoup
import nbformat

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DEST = ROOT / "notebook" / "讲稿"
KATEX = ROOT / "Workspaces" / "gsg_project" / "dlw_report" / "_assets" / "package"
SPECS = {
    "nonlinear": ("非线性化report.ipynb", "nonlinear_body.html", "非线性化讲稿.html"),
    "hs": ("2HS数值分析report.ipynb", "hs_body.html", "2HS数值分析讲稿.html"),
    "dlw": ("DLW数值分析report.ipynb", "dlw_body.html", "DLW数值分析讲稿.html"),
}
FIGURES = {
    "nonlinear": [("error-convergence", 0, "nonlinear-residual-1.png"),
                  ("error-convergence", 1, "nonlinear-residual-2.png")],
    "hs": [("hs-waveforms", 0, "hs-single-waveforms.png"),
           ("hs-two-plots", 0, "hs-two-waveforms.png"),
           ("hs-two-plots", 1, "hs-two-errors.png")],
    "dlw": [("dlw-curves", 0, "dlw-case-A.png"),
            ("dlw-curves", 1, "dlw-case-B.png"),
            ("dlw-curves", 2, "dlw-case-C.png")],
}
CSS = '''html{background:#fff;color:#242424;font-size:17px}
body{max-width:880px;margin:42px auto 76px;padding:0 26px;font-family:Georgia,"Times New Roman","Songti SC","SimSun",serif;line-height:1.85}
nav{font-size:14px;line-height:1.6;border-bottom:1px solid #d9d9d9;padding-bottom:12px;margin-bottom:28px;display:flex;flex-wrap:wrap;gap:8px 22px}
a{color:#264c6b;text-underline-offset:3px}nav a{text-decoration:none}a:hover{text-decoration:underline}
h1{font-size:28px;line-height:1.45;font-weight:600;text-align:center;margin:0 0 22px}
h2{font-size:22px;line-height:1.55;font-weight:600;margin:38px 0 14px;scroll-margin-top:20px}
h3{font-size:18px;margin:24px 0 10px;font-weight:600}
p{margin:12px 0}.lead{margin:18px 0 24px}.show{color:#555;font-size:15px;line-height:1.75;margin:10px 0 18px;padding-left:12px;border-left:2px solid #ddd}
code,pre{font-family:Consolas,"Cascadia Code",monospace}code{font-size:.86em;overflow-wrap:anywhere}
pre{background:#fafafa;border:1px solid #e5e5e5;border-radius:2px;font-size:14px;line-height:1.65;padding:14px 16px;overflow-x:auto;margin:16px 0;tab-size:4;max-width:100%;box-sizing:border-box}
pre code{font-size:inherit;white-space:pre;overflow-wrap:normal}
table{width:100%;border-collapse:collapse;font-size:15px;line-height:1.65;margin:18px 0}th,td{text-align:left;vertical-align:top;padding:10px;border-bottom:1px solid #ddd}th{border-top:1px solid #333;border-bottom:1px solid #333;font-weight:600}.table-wrap{overflow-x:auto}
ul,ol{padding-left:1.5em}li{padding-left:3px;margin:6px 0}
.katex{font-size:1.03em}.katex-display{overflow-x:auto;overflow-y:hidden;padding:6px 2px;margin:20px 0}.katex-display>.katex{min-width:max-content}
figure{margin:25px 0}img{max-width:100%;height:auto;display:block;margin:auto}figcaption{font-size:14px;color:#555;line-height:1.65;margin-top:8px;text-align:left}
footer{border-top:1px solid #ddd;margin-top:36px;padding-top:14px;color:#555;font-size:14px}
@media(max-width:600px){html{font-size:16px}body{margin-top:24px;padding:0 18px}h1{font-size:24px}h2{font-size:20px;margin-top:30px}pre{font-size:12.5px;padding:12px}.show{font-size:14px}table{font-size:14px}th,td{padding:8px}}
@media print{body{max-width:none;margin:0;padding:0;font-size:11pt;line-height:1.65}nav{display:none}h1{font-size:20pt}h2{font-size:15pt;break-after:avoid}h3,.show{break-after:avoid}pre{font-size:9pt;white-space:pre-wrap;overflow:visible}pre code{white-space:pre-wrap}figure,tr{break-inside:avoid}.katex-display{overflow:visible}a{color:inherit}footer{font-size:9pt}}
'''
SCRIPT = r'''document.addEventListener("DOMContentLoaded", () => {
  renderMathInElement(document.querySelector("main"), {
    delimiters: [{left:"$$",right:"$$",display:true},{left:"\\[",right:"\\]",display:true},
                 {left:"\\(",right:"\\)",display:false},{left:"$",right:"$",display:false}],
    throwOnError:false, strict:"ignore", trust:false,
    ignoredTags:["script","noscript","style","textarea","pre","code"]
  });
  document.documentElement.dataset.mathReady = "true";
});'''


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def prepare_assets():
    assets = DEST / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    fonts = assets / "fonts"
    fonts.mkdir(exist_ok=True)
    for filename in ["katex.min.css", "katex.min.js"]:
        (assets / filename).write_bytes((KATEX / "dist" / filename).read_bytes())
    (assets / "auto-render.min.js").write_bytes((KATEX / "dist" / "contrib" / "auto-render.min.js").read_bytes())
    (assets / "KaTeX-LICENSE.txt").write_bytes((KATEX / "LICENSE").read_bytes())
    for path in (KATEX / "dist" / "fonts").iterdir():
        if path.is_file():
            (fonts / path.name).write_bytes(path.read_bytes())
    (assets / "lecture.css").write_text(CSS, encoding="utf-8")
    (assets / "lecture.js").write_text(SCRIPT, encoding="utf-8")
    for key, (notebook_name, _, _) in SPECS.items():
        notebook = nbformat.read(ROOT / "notebook" / notebook_name, 4)
        by_id = {cell.id: cell for cell in notebook.cells}
        for cell_id, number, filename in FIGURES[key]:
            pngs = [output.data["image/png"] for output in by_id[cell_id].outputs
                    if "image/png" in output.get("data", {})]
            (assets / filename).write_bytes(base64.b64decode(pngs[number]))


def build():
    prepare_assets()
    nav = '<nav aria-label="讲稿与笔记本">' + "".join(
        f'<a href="{html.escape(filename)}">{html.escape(filename[:-5])}</a>'
        for _, _, filename in SPECS.values()
    ) + '</nav>'
    reports = []
    for key, (notebook_name, body_name, filename) in SPECS.items():
        body = (HERE / body_name).read_text("utf-8")
        soup = BeautifulSoup(body, "html.parser")
        assert soup.find("h1")
        title_heading = soup.find("h1")
        title = title_heading.get_text()
        title_heading.extract()
        assert not soup.find_all(["script", "style"])
        for index, heading in enumerate(soup.find_all("h2"), 1):
            if not heading.get("id"):
                heading["id"] = f"section-{index}"
        for table in soup.find_all("table"):
            wrapper = soup.new_tag("div", attrs={"class": "table-wrap"})
            table.wrap(wrapper)
        source_link = f'<p class="show">配合 <a href="../{html.escape(notebook_name)}">{html.escape(notebook_name)}</a> 阅读；演示时将讲稿与笔记本并排打开，按各节提示展示公式、代码和输出。</p>'
        result = f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} · 讲稿</title><meta name="description" content="{html.escape(notebook_name)} 的演示讲稿：公式、关键代码与结果对应。">
<link rel="stylesheet" href="assets/katex.min.css"><link rel="stylesheet" href="assets/lecture.css">
<script defer src="assets/katex.min.js"></script><script defer src="assets/auto-render.min.js"></script><script defer src="assets/lecture.js"></script></head>
<body>{nav}<main>{title_heading}{source_link}{soup}</main><footer>讲解顺序与对应代码以当前笔记本为准。<a href="../../report/notebook_usage.html">笔记本使用说明</a></footer></body></html>'''
        path = DEST / filename
        path.write_text(result, encoding="utf-8")
        notebook_path = ROOT / "notebook" / notebook_name
        reports.append({"lecture": str(path), "sha256": sha(path.read_bytes()),
                        "notebook": str(notebook_path), "notebook_sha256": sha(notebook_path.read_bytes()),
                        "body": str(HERE / body_name), "sections": len(soup.find_all("h2")),
                        "code_excerpts": len(soup.select("pre[data-cell]"))})
    manifest = {"success": True, "reports": reports,
                "math_resources": "KaTeX 0.18.7 copied from the existing local report assets",
                "figures": "Unmodified PNG outputs extracted from the delivered notebooks"}
    (HERE / "build_validation.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    return manifest


if __name__ == "__main__":
    print(json.dumps(build(), ensure_ascii=False, indent=2))
