"""Build the dedicated, self-contained paper from its local HTML source."""
from pathlib import Path
import base64
import hashlib
import json
import re

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
DIST=ROOT/"Workspaces/gsg_project/dlw_report/_assets/package/dist"
data=json.loads((HERE/"verification.json").read_text(encoding="utf-8"))
page=(HERE/"report.src.html").read_text(encoding="utf-8")

def fmt(value):
    return f"{float(value):.7g}" if value is not None else "—"

rows=[]
for row in data["asymptotic_constants"]:
    rows.append("<tr>"+"".join(f"<td>{v}</td>" for v in
        [row["n"],fmt(row["space_ratio"]),fmt(row["Euler_ratio"]),
         fmt(row["RK4_ratio"]),fmt(row["gamma_minus_center"])])+"</tr>")
page=page.replace("@@ASYMPTOTIC_ROWS@@","\n".join(rows))
rows=[]
for row in data["gaussian_operator"]:
    rows.append("<tr>"+"".join(f"<td>{v}</td>" for v in
        [row["N"],fmt(row["operator_error"]),fmt(row["error_over_k4"]),
         fmt(row["refinement_ratio"])])+"</tr>")
page=page.replace("@@GAUSSIAN_ROWS@@","\n".join(rows))
rows=[]
bands=data["bandwidth_witnesses"]
for left,right in zip(bands[:4],bands[4:]):
    rows.append("<tr>"+"".join(f"<td>{v}</td>" for v in
        [left["log2_N"],left["K"],fmt(left["log_error"]),right["K"],
         fmt(right["log_error"])])+"</tr>")
page=page.replace("@@BANDWIDTH_ROWS@@","\n".join(rows))

equations=[]
def tag(match):
    equations.append(match[0])
    return match[0][:-2]+rf"\tag{{{len(equations)}}}"+ "$$"
main_start=page.index("<main>")+len("<main>")
main_end=page.index("</main>")
page=page[:main_start]+re.sub(r"\$\$[\s\S]*?\$\$",tag,page[main_start:main_end])+page[main_end:]

css=(DIST/"katex.min.css").read_text(encoding="utf-8")
fonts=[]
def embed(match):
    name=match[1]
    path=DIST/"fonts"/name
    mime={".woff2":"font/woff2",".woff":"font/woff",".ttf":"font/ttf"}[path.suffix]
    fonts.append(name)
    return "url(data:"+mime+";base64,"+base64.b64encode(path.read_bytes()).decode()+")"
css=re.sub(r'url\((?:"|\'|)?fonts/([^)"\']+)(?:"|\'|)?\)',embed,css)
js=(DIST/"katex.min.js").read_text(encoding="utf-8")+"\n"+(DIST/"contrib/auto-render.min.js").read_text(encoding="utf-8")
page=page.replace("@@KATEX_CSS@@",css).replace("@@KATEX_JS@@",js)
if "@@" in page:
    raise ValueError("Unresolved placeholder")
page=page.replace('href="Workspaces/', 'href="../../Workspaces/')
output=HERE/"report.html"
output.write_text(page,encoding="utf-8")
manifest={"output":str(output),"sha256":hashlib.sha256(output.read_bytes()).hexdigest(),
          "source_sha256":hashlib.sha256((HERE/"report.src.html").read_bytes()).hexdigest(),
          "prediction_sha256":data["prediction_sha256"],"equation_count":len(equations),
          "fonts_embedded":len(fonts),"equations":equations}
(HERE/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({k:v for k,v in manifest.items() if k!="equations"},ensure_ascii=False))
