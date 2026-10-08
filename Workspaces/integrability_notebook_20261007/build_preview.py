"""Offline reading preview for inspecting notebook equations and outputs."""
from html import escape
import json
from pathlib import Path
import re
import shutil

import markdown
import nbformat

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PREVIEW = HERE / "preview"


def render_markdown(text):
    protected = {}
    def hold(match):
        key = "MATHPLACEHOLDER" + str(len(protected)) + "END"
        content = match.group(0)
        if content.startswith("$$"):
            value = r"\[" + content[2:-2] + r"\]"
        else:
            value = r"\(" + content[1:-1] + r"\)"
        protected[key] = escape(value)
        return key
    text = re.sub(r"\$\$[\s\S]*?\$\$|(?<!\$)\$[^\n$]+\$(?!\$)", hold, text)
    result = markdown.markdown(text, extensions=["tables", "fenced_code"])
    for key, value in protected.items():
        result = result.replace(key, value)
    return result


def render(path, name, ids=None):
    nb = nbformat.read(path, 4)
    body = []
    for cell in nb.cells:
        if ids is not None and cell.id not in ids:
            continue
        if cell.cell_type == "markdown":
            value = render_markdown(cell.source)
        elif cell.cell_type == "code":
            value = '<pre class="source"><code>' + escape(cell.source) + '</code></pre>'
            for output in cell.outputs:
                if output.output_type == "stream":
                    value += '<pre class="output">' + escape(output.text) + '</pre>'
        else:
            continue
        body.append('<section id="' + escape(cell.id) + '">' + value + '</section>')
    html = '''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Notebook 公式与源码预览</title>
<link rel="stylesheet" href="assets/katex.min.css">
<link rel="stylesheet" href="assets/lecture.css">
<style>.output{background:#fff;color:#444;font-size:12px;line-height:1.65}
section{margin:0 0 24px}td code{word-break:break-word}</style>
<script defer src="assets/katex.min.js"></script>
<script defer src="assets/auto-render.min.js"></script>
<script defer src="assets/lecture.js"></script></head><body><main>'''
    target = PREVIEW / name
    target.write_text(html + "\n".join(body) + '</main></body></html>\n', "utf-8")
    return str(target)


def main():
    PREVIEW.mkdir(exist_ok=True)
    shutil.copytree(ROOT / "notebook" / "讲稿" / "assets", PREVIEW / "assets", dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("*.png"))
    paths = [render(HERE / "DLW刘维尔可积性report.ipynb", "integrability.html"),
             render(ROOT / "notebook" / "非线性化report.ipynb", "nonlinear-definitions.html",
                    {"report-text-04", "lean-uw"})]
    (HERE / "preview_paths.json").write_text(json.dumps(paths, ensure_ascii=False, indent=2) + "\n", "utf-8")
    print(json.dumps({"previews": paths}, ensure_ascii=False))


if __name__ == "__main__":
    main()
