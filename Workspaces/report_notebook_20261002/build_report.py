"""Add executable cells to the preserved Report, retaining its original typography."""
from pathlib import Path
import argparse
import hashlib
import html
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROOF_EXCERPTS = []


def esc(value):
    return html.escape(str(value), quote=True)


def lean_markup(code):
    tokens = re.compile(r'(?P<comment>--[^\n]*|/-[\s\S]*?-/)|(?P<string>"(?:\\.|[^"\\])*")|(?P<keyword>\b(?:import|open|namespace|noncomputable|section|end|def|abbrev|theorem|example|by|exact|intro|rw|simp|simpa|have|let|fun|if|then|else|where|class|instance|structure)\b|#[a-z_]+)|(?P<number>\b\d+(?:\.\d+)?\b)')
    parts, previous = [], 0
    for token in tokens.finditer(code):
        parts.append(esc(code[previous:token.start()]))
        parts.append(f'<span class="syntax-{token.lastgroup}">{esc(token.group())}</span>')
        previous = token.end()
    parts.append(esc(code[previous:]))
    return ''.join(parts)


def play_button():
    return '<button type="button" class="play-button" data-run aria-label="运行此代码块" title="运行此代码块"><span aria-hidden="true">▶</span></button>'


def lean_cell(case, stage, title, extra="", introduction=""):
    route=case["route"]
    meta=case["_stages"][stage]
    cell_id=f"lean-{route}" if stage=="endpoint" else f"lean-{route}-{stage}"
    code=meta.get("source") or meta.get("code") or meta.get("fullSource")
    if not code:raise ValueError(f"Missing exact Lean cell source: {route}/{stage}")
    source_path = HERE / "lean_material/steps" / meta["filename"]
    if source_path.read_text(encoding="utf-8") != code or hashlib.sha256(source_path.read_bytes()).hexdigest() != meta["sha256"]:
        raise ValueError(f"Lean cell source/hash mismatch: {source_path}")
    return (f'<section class="code-cell" id="{cell_id}" data-kind="lean" data-route="{route}" data-stage="{stage}">'
            f'<p class="cell-title visually-hidden">{esc(title)}</p>'
            f'<p class="cell-lead">{esc(meta["lead"])}</p>'
            + introduction +
            f'<pre class="lean-source" aria-label="{esc(title)}">{lean_markup(code)}</pre>'
            + '<div class="cell-toolbar">' + play_button() + '<span class="cell-status" role="status">尚未运行</span></div>'
            + '<div class="cell-output" aria-live="polite"></div>' + extra + '</section>')


def lean_import(case):
    return lean_cell(case,"import","1　Import：载入本路线的证明库")


def lean_start(case):
    note = ('<p class="notebook-note proof-start-note"><code>def StartPoint</code> 写出式（1）的两条双线性假设；'
            '<code>#print StartPoint</code> 将这一定义输出。起点到终点的证明在后面的终点代码块中调用。</p>'
            '<p class="notebook-note proof-start-note"><code>namespace</code> 组织名称，<code>section</code> 管理作用域，'
            '<code>noncomputable section</code> 允许使用精确实数函数；这些声明负责组织代码。</p>')
    return lean_cell(case,"start","2　理论的双线性起点",note)


def proof_excerpt(case, filename, declaration):
    source = next(item for item in case["sources"] if Path(item["path"]).name == filename)
    path = Path(source["path"])
    if hashlib.sha256(path.read_bytes()).hexdigest() != source["sha256"]:
        raise ValueError(f"Displayed source hash mismatch: {path}")
    text = path.read_text(encoding="utf-8")
    match = re.search(r"(?ms)^(?:def|lemma|theorem) " + re.escape(declaration)
                      + r"\b.*?(?=\n\n|\n(?:def|lemma|theorem|abbrev|end|#print)\b|\Z)", text)
    if not match:
        raise ValueError(f"Missing proof declaration: {filename}/{declaration}")
    code = match.group().rstrip()
    PROOF_EXCERPTS.append({"route":case["route"], "file":filename, "declaration":declaration,
                           "sourceSha256":source["sha256"], "firstLine":text[:match.start()].count("\n")+1,
                           "lines":len(code.splitlines()), "excerptSha256":hashlib.sha256(code.encode()).hexdigest()})
    return code


def proof_panel(case):
    if case["route"] == "uw":
        groups = [
            ("式（7）的残差与 v 的重构", "ReportNonlinearUW.lean",
             ["fluxUW", "fluxOmega", "reportN1", "reportN2", "vFromOmega"]),
            ("式（8）：NonlinearPair 表示两条残差均为零", "Contracts.lean", ["NonlinearPair"]),
            ("核心恒等式的声明：由 c14_proved 证明", "Contracts.lean", ["C14"]),
            ("使用起点：hsp 的两条假设令归一化残差归零", "PkgNonlinear.lean", ["c15_proved"]),
            ("式（8）的封装：对齐 v 的定义，调用核心定理", "ReportNonlinearUW.lean", ["semiPair_implies_report8"]),
            ("式（7）的封装：第一残差改写，第二残差由守恒律得到", "ReportNonlinearUW.lean", ["semiPair_implies_report7"]),
        ]
        label = "展开式（7）、（8）的关键证明"
    else:
        groups = [
            ("式（21）：两条演化方程的残差", "ReportNonlinearQRM.lean", ["coefficient", "residualQ", "residualR"]),
            ("Q 方程：用双线性起点令残差归零", "ReportNonlinearQRM.lean", ["report_Q_equation"]),
            ("R 方程：用乘积残差分解与式（7）", "ReportNonlinearQRM.lean", ["report_R_equation"]),
            ("式（21）的封装：合并 Q、R 方程与格点约束", "ReportNonlinearQRM.lean", ["semiPair_implies_report21"]),
            ("式（22）的封装：合并场的重构恒等式", "ReportNonlinearQRM.lean", ["report22"]),
        ]
        label = "展开式（21）、（22）的关键证明"
    fragments = []
    for heading, filename, declarations in groups:
        fragments.append(f"-- {heading}（{filename}）\n" + "\n\n".join(proof_excerpt(case, filename, name) for name in declarations))
    code = "\n\n".join(fragments)
    return ('<details class="key-proof"><summary>' + label + '</summary>'
            '<p class="notebook-note">以下摘录来自导入的证明库，按证明关系排列；上方 ▶ 编译终点调用，复用这些已检查的定理。</p>'
            f'<pre class="proof-source" aria-label="{esc(label)}">{lean_markup(code)}</pre></details>')


def proof_guide(case):
    if case["route"] == "uw":
        points = [
            '<strong>输入。</strong> <code>hsp : StartPoint a h F G</code> 是式（1）的假设，展开后与库中的 <code>SemiPair</code> 相同。'
            '<code>hh</code> 要求 h≠0；<code>hF/hG</code> 要求各格点的函数关于 (x,t) 联合实解析，<code>hFp/hGp</code> 要求严格为正。',
            '<strong>结论。</strong> 第一个 <code>example</code> 的冒号后是 <code>reportN1 = 0 ∧ reportN2 = 0</code>，对应式（7）。'
            '第二个的 <code>NonlinearPair</code> 展开为 <code>n1 = 0 ∧ n2 = 0</code>，对应式（8）。',
            '<strong>使用起点。</strong> 核心定理 <code>c15_proved</code> 中的 <code>rw [(hsp j).1]</code> 与 <code>rw [(hsp j).2]</code> '
            '使用两条双线性方程，使归一化残差 <code>normA</code>、<code>normC</code> 为零；'
            '<code>c14_proved</code> 的残差恒等式随后给出 <code>NonlinearPair</code>。',
            '<strong>得到报告终点。</strong> <code>semiPair_implies_report8</code> 用 <code>physical_v</code> 对齐 v 的重构后调用核心定理。'
            '<code>semiPair_implies_report7</code> 使用同一结论：<code>reportN1_eq_n1</code> 给出第一条；'
            '<code>c19_proved</code> 的 W 守恒律经 <code>omega_conservation_bridge</code> 变为 <code>(4/h)·reportN2 = 0</code>，'
            '再由 h≠0 得到第二条。',
        ]
        note = ('<p class="notebook-note">阅读每个 <code>example</code> 时，先看括号中的假设，再看冒号后的结论，最后看 '
                '<code>:=</code> 后提供证明的定理。这里的 <code>example</code> 证明任意满足假设的场；'
                '终点运行会检查这两个调用，<code>#print axioms</code> 输出它们依赖的基础公理。'
                '导数法则、差分恒等式与代数化简封装在导入的证明库中。</p>')
    else:
        points = [
            '<strong>式（21）。</strong> <code>semiPair_implies_report21</code> 接收 <code>StartPoint</code> 及相同的正则性、正性、h≠0 假设，'
            '合并 <code>report_Q_equation</code>、<code>report_R_equation</code> 与 <code>lattice_constraint</code>。',
            '<strong>证明关系。</strong> Q 方程由归一化双线性残差归零得到；R 方程由乘积残差分解、Q 方程和式（7）的第二条得到。',
            '<strong>式（22）。</strong> <code>report22</code> 合并 u、ω、v 的重构恒等式；这部分只依赖场的定义、正则性、正性与 h≠0。',
        ]
        note = '<p class="notebook-note">冒号后给出结论，<code>:=</code> 后调用证明定理；下方可展开关键证明，完整依赖保留在导入库中。</p>'
    return '<div class="proof-reading"><ol class="proof-outline">' + ''.join('<li>'+point+'</li>' for point in points) + '</ol>' + note + '</div>'


def lean_end(case):
    return lean_cell(case,"endpoint","3　验证终点",proof_panel(case),proof_guide(case))


def js_section(cells, group):
    result = []
    for index, cell in enumerate(cells):
        cell_id = cell["id"]
        result.append(
            f'<section class="code-cell" id="{esc(cell_id)}" data-kind="js" data-group="{esc(group)}" data-requires="{esc(json.dumps(cell.get("requires",[])))}">'
            f'<label class="cell-title visually-hidden" for="source-{esc(cell_id)}">{index+1}　{esc(cell["title"])} · JavaScript</label>'
            + f'<p class="cell-lead">{esc(cell["lead"])}</p>'
            + f'<textarea class="source-editor" id="source-{esc(cell_id)}" spellcheck="false" aria-label="{esc(cell["title"])}，可编辑代码">{esc(cell["code"])}</textarea>'
            + f'<pre class="print-source">{esc(cell["code"])}</pre>'
            + '<div class="cell-toolbar">' + play_button() + '<button type="button" data-restore>恢复本段</button><span class="cell-status" role="status">尚未运行</span></div>'
            + '<div class="cell-output" aria-live="polite"></div></section>'
        )
    return "\n".join(result)


def build(base=None):
    PROOF_EXCERPTS.clear()
    base = Path(base) if base else HERE / "before/Report.html"
    page = base.read_text(encoding="utf-8")
    page = page.replace('href="dlw_error_theory.html"', 'href="report/dlw_error_theory.html"')
    if "lean-manifest" in page:
        raise ValueError("Base must be the report before notebook extension.")
    manifest = json.loads((HERE / "lean_material/manifest.json").read_text(encoding="utf-8"))
    cases = {case["route"]:case for case in manifest["cases"]}
    stages=json.loads((HERE / "lean_material/stage_manifest.json").read_text(encoding="utf-8"))
    for case in cases.values():
        case["_stages"]=stages["cases"][case["route"]]
    js_cells = json.loads((HERE / "step_material/cells.json").read_text(encoding="utf-8"))
    hs_path = HERE / "step_material/hs_cells.json"
    hs_cells = json.loads(hs_path.read_text(encoding="utf-8")) if hs_path.exists() else []

    intro = '''<nav class="notebook-nav" aria-label="报告段落">
<a href="#nonlinear-uw">两场非线性化</a><a href="#nonlinear-qrm">比值非线性化</a>
<a href="#hs-numerics">2HS 数值比较</a><a href="#dlw-error-lab">DLW 误差估计</a></nav>
<p class="notebook-intro">从 import 或准备环境开始，点击 ▶ 逐段运行。前段定义保留，输出显示在对应代码下方。</p>
<p class="notebook-note">双击 Report.exe 打开本报告。<span id="runtime-status" class="runtime-status"></span></p>
<div class="notebook-toolbar" role="group" aria-label="代码运行操作">
<button type="button" data-cancel disabled hidden>取消运行</button><button type="button" data-reset>重置运行状态</button>
<button type="button" data-restore-all>恢复示例代码</button><span id="notebook-status" class="cell-status" role="status">尚未运行</span></div>'''
    page = re.sub(r"(</h1>)",r"\1\n"+intro,page,count=1)
    page = page.replace('<h3>1.1　消去辅助势的两场形式</h3>', '<h3 id="nonlinear-uw">1.1　消去辅助势的两场形式</h3>'+lean_import(cases["uw"]))
    equation1 = re.search(r"<p>\$\$B_\{a-h/2\}[\s\S]*?\\tag\{1\}\$\$</p>",page)
    if not equation1: raise ValueError("Equation 1 anchor missing")
    page = page[:equation1.end()] + "\n" + lean_start(cases["uw"]) + page[equation1.end():]
    page = page.replace('<h3>1.2　保留势的比值形式</h3>', lean_end(cases["uw"]) + '\n<h3 id="nonlinear-qrm">1.2　保留势的比值形式</h3>\n<p class="notebook-note">本路线仍从式（1）出发，保留势与中心比值，经过下述公式推导到式（21）、（22）。</p>' + lean_import(cases["qrm"]) + lean_start(cases["qrm"]))
    page = page.replace('<h2>2　2HS 单孤子与二孤子的数值比较</h2>',lean_end(cases["qrm"]) + '\n<h2 id="hs-numerics">2　2HS 单孤子与二孤子的数值比较</h2>')
    if hs_cells:
        hs_intro = (HERE / "step_material/hs_intro.html").read_text(encoding="utf-8")
        page = page.replace('<h3>2.2　二孤子</h3>', '<h3 id="hs-error-lab">2.1.1　单孤子误差的现场计算</h3>\n' + hs_intro + js_section(hs_cells,"hs-error") + '\n<h3>2.2　二孤子</h3>')
    error_intro = (HERE / "step_material/intro.html").read_text(encoding="utf-8")
    error_section = '<h2 id="dlw-error-lab">3　DLW 空间误差估计的现场计算</h2>\n' + error_intro + js_section(js_cells,"dlw-error")
    page = page.replace('</main>',error_section+'\n</main>',1)
    css = (HERE / "notebook.css").read_text(encoding="utf-8")
    js = (HERE / "notebook.js").read_text(encoding="utf-8")
    public_manifest = {"cases": []}
    for case in manifest["cases"]:
        public_manifest["cases"].append({"route":case["route"],"summary":case["title"],"expectedSources":{Path(source["path"]).name:source["sha256"] for source in case["sources"]},"stages":{name:{"sha256":meta["sha256"]} for name,meta in case["_stages"].items()}})
    manifest_text = json.dumps(public_manifest, ensure_ascii=False).replace("<","\\u003c")
    page = page.replace('</head>',f'<style id="notebook-style">{css}</style></head>',1)
    page = page.replace('</body>',f'<script type="application/json" id="lean-manifest">{manifest_text}</script><script id="notebook-runtime">{js}</script></body>',1)
    page = page.replace('<title>Report</title>','<title>DLW 非线性化与 2HS 数值比较 · 可运行报告</title>',1)
    (HERE / "report.src.html").write_text(page,encoding="utf-8")
    (ROOT / "Report.html").write_text(page,encoding="utf-8")
    evidence = {
        "base":str(base), "baseSha256":hashlib.sha256(base.read_bytes()).hexdigest(),
        "outputSha256":hashlib.sha256((ROOT / "Report.html").read_bytes()).hexdigest(), "leanRoutes":list(cases),
        "jsCells":[cell["id"] for cell in hs_cells+js_cells],
        "originalEquationTags":re.findall(r"\\tag\{([^}]+)\}",base.read_text(encoding="utf-8")),
        "outputEquationTags":re.findall(r"\\tag\{([^}]+)\}",re.sub(r"<pre[\s\S]*?</pre>","",page)),
        "originalDisplayMathBlocksPreserved":all(block in page for block in re.findall(r"\$\$[\s\S]*?\$\$",base.read_text(encoding="utf-8"))),
        "proofPresentation":"concise reading guide and one collapsed key-proof panel per route",
        "proofExcerpts":PROOF_EXCERPTS,
    }
    (HERE / "build_manifest.json").write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({"html":str(ROOT/'Report.html'),"bytes":len(page.encode()),"jsCells":evidence["jsCells"]},ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", help="fresh non-notebook Report.html to extend")
    build(parser.parse_args().base)
