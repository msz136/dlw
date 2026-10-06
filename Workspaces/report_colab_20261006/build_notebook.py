"""Convert the report reading order to ordinary Colab/Jupyter cells.

The report is read, never modified. Numerical cells are the reviewed Python
ports next to this file. bootstrap_source.txt is supplied by the runtime build.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag


HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parent.parent
REPORT = WORKSPACE / "Report.html"
DISPLAY_MATH = re.compile(r"\$\$(.*?)\$\$", re.S)
EQUATION_TAG = re.compile(r"\\tag\{([^}]+)\}")


def sha256(data: str | bytes) -> str:
    return hashlib.sha256(data.encode("utf-8") if isinstance(data, str) else data).hexdigest()


def lines(source: str) -> list[str]:
    return source.splitlines(keepends=True)


def inline(node) -> str:
    """Preserve TeX literally while translating simple semantic HTML."""
    if isinstance(node, NavigableString):
        return str(node)
    inner = "".join(inline(child) for child in node.children)
    if node.name in {"strong", "b"}:
        return f"**{inner}**"
    if node.name in {"em", "i"}:
        return f"*{inner}*"
    if node.name == "code":
        return f"`{inner}`"
    if node.name == "br":
        return "  \n"
    if node.name == "a":
        href = node.get("href", "")
        if href.startswith("report/"):
            href = "../../" + href
        return f"[{inner}]({href})" if href else inner
    if node.name in {"script", "style", "button"}:
        return ""
    return inner


def table_markdown(table: Tag) -> str:
    rows = []
    for row in table.find_all("tr"):
        rows.append([inline(cell).strip().replace("|", "\\|") for cell in row.find_all(["th", "td"], recursive=False)])
    if not rows:
        return ""
    width = len(rows[0])
    assert all(len(row) == width for row in rows), "The report table has a merged cell."
    return "\n".join(
        ["| " + " | ".join(rows[0]) + " |", "| " + " | ".join(["---"] * width) + " |"]
        + ["| " + " | ".join(row) + " |" for row in rows[1:]]
    )


def proof_reading(reading: Tag) -> str:
    blocks = []
    for child in reading.children:
        if not isinstance(child, Tag):
            continue
        if child.name in {"ol", "ul"}:
            for index, item in enumerate(child.find_all("li", recursive=False), start=1):
                blocks.append(f"{index}. {inline(item).strip()}")
        else:
            blocks.append(inline(child).strip())
    return "\n\n".join(blocks)


def compact_proof(route: str) -> str:
    if route == "uw":
        return (
            "关键证明封装在 `PkgNonlinear.lean` 与 `ReportNonlinearUW.lean`："
            "`c15_proved` 使用两条双线性假设，将 `normA`、`normC` 置零；"
            "`c14_proved` 给出物理场残差恒等式，得到 `NonlinearPair`。"
            "`semiPair_implies_report8` 对齐 $v$ 的重构；"
            "`semiPair_implies_report7` 再通过 `reportN1_eq_n1` 与 "
            "`omega_conservation_bridge` 得到式（7）的两条方程。"
            "终点单元调用这些已证明的定理。"
        )
    return (
        "关键证明封装在 `ReportNonlinearQRM.lean`："
        "`report_Q_equation` 由双线性起点得到 $Q$ 方程；"
        "`report_R_equation` 使用乘积残差分解及式（7）的第二条得到 $R$ 方程；"
        "`semiPair_implies_report21` 合并两条演化方程与格点约束。"
        "`report22` 合并 $u$、$\\omega$、$v$ 的重构恒等式。"
    )


def migrate_prose(text: str) -> str:
    """Only replace the old execution transport descriptions."""
    text = text.replace("同一数值会话", "同一笔记本内核").replace("同一会话", "同一笔记本内核")
    text = text.replace("以下可编辑代码均以 JavaScript 在本地计算", "以下代码使用 Python、NumPy 与 Matplotlib 计算")
    return text


def new_markdown(cell_id: str, source: str, provenance: list[dict], attachments: dict | None = None) -> dict:
    cell = {
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": {"id": cell_id, "report_source": provenance},
        "source": lines(source.strip() + "\n"),
    }
    if attachments:
        cell["attachments"] = attachments
    return cell


def new_code(cell_id: str, source: str, provenance: dict, bootstrap: bool = False) -> dict:
    metadata = {"id": cell_id, "report_source": provenance}
    if bootstrap:
        metadata.update({"cellView": "form", "source_hidden": True})
    return {
        "cell_type": "code", "id": cell_id, "metadata": metadata,
        "source": lines(source), "execution_count": None, "outputs": [],
    }


def build(source_path: Path, destination: Path, image_mode: str = "attachments") -> dict:
    html = source_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")
    main = soup.select_one("main")
    assert main is not None, "Report.html has no main reading flow."
    bootstrap_path = HERE / "bootstrap_source.txt"
    if not bootstrap_path.exists():
        raise FileNotFoundError("The runtime build must first provide bootstrap_source.txt.")
    bootstrap = bootstrap_path.read_text(encoding="utf-8")
    assert bootstrap.strip(), "Runtime bootstrap is empty."
    numerical = {}
    for name in ["hs_cells.json", "dlw_cells.json"]:
        for spec in json.loads((HERE / name).read_text(encoding="utf-8")):
            assert spec["id"] not in numerical
            numerical[spec["id"]] = spec

    cells, buffer, provenance, attachments = [], [], [], {}
    included, omitted, adapted, code_checks, image_checks, table_checks = [], [], [], [], [], []
    header_checks = []
    markdown_index = 0

    def origin(index: int, element) -> dict:
        return {
            "main_child_index": index,
            "anchor": element.get("id") if isinstance(element, Tag) else None,
            "tag": element.name if isinstance(element, Tag) else "text",
            "sha256": sha256(str(element)),
        }

    def add_markdown(text: str, source: dict, original: str | None = None):
        migrated = migrate_prose(text)
        buffer.append(migrated)
        provenance.append(source)
        if migrated != text or (original is not None and migrated != original):
            adapted.append({"source": source, "original": original or text, "replacement": migrated})

    def flush():
        nonlocal markdown_index, buffer, provenance, attachments
        if not buffer:
            return
        markdown_index += 1
        cell_id = f"report-text-{markdown_index:02d}"
        cells.append(new_markdown(cell_id, "\n\n".join(buffer), provenance, attachments))
        buffer, provenance, attachments = [], [], {}

    def insert_bootstrap():
        add_markdown(
            "先运行下面的准备单元，载入本笔记本的 Lean 证明库与逐段编译接口。"
            "首次在 Colab 中运行时会准备固定版本的 Lean 与 Mathlib 环境。"
            "随后依次执行各路线的 import、起点和终点；数值部分在同一 Python 内核中逐段计算。"
            "输出保留在运行的单元下方，修改上游代码后重新运行受影响的后段。",
            {"kind": "notebook-runtime-lead"},
        )
        flush()
        cells.append(new_code("runtime-prepare", bootstrap, {"kind": "bootstrap", "sha256": sha256(bootstrap)}, True))

    for index, element in enumerate(main.children):
        if isinstance(element, NavigableString):
            if not str(element).strip():
                continue
            source = origin(index, element)
            included.append(source)
            add_markdown(str(element).strip(), source)
            continue
        if not isinstance(element, Tag):
            continue
        source = origin(index, element)
        classes = set(element.get("class", []))
        if element.name == "nav" or "notebook-toolbar" in classes or "notebook-intro" in classes or element.find(id="runtime-status"):
            omitted.append({**source, "reason": "HTML transport/navigation replaced by native notebook controls"})
            continue
        included.append(source)
        if element.name in {"h1", "h2", "h3"}:
            text = inline(element).strip()
            add_markdown("#" * int(element.name[1]) + " " + text, source)
            header_checks.append({"tag": element.name, "anchor": element.get("id"), "text": element.get_text()})
            if element.name == "h1":
                insert_bootstrap()
        elif "code-cell" in classes:
            cell_id = element["id"]
            route = element.get("data-route")
            if element.get("data-kind") == "lean":
                stage = element["data-stage"]
                lead = inline(element.select_one(".cell-lead")).strip()
                add_markdown(lead, source)
                reading = element.select_one(".proof-reading")
                if reading:
                    add_markdown(proof_reading(reading).replace("下方可展开关键证明，完整依赖保留在导入库中", "关键证明与依赖保留在导入库中"), source)
                flush()
                original_code = element.select_one("pre.lean-source").get_text()
                actual_code = f"%%lean {route} {stage}\n" + original_code
                cells.append(new_code(cell_id, actual_code, source))
                code_checks.append({"id": cell_id, "kind": "lean", "route": route, "stage": stage, "body_sha256": sha256(original_code), "magic": actual_code.splitlines()[0]})
                for note in element.select(".proof-start-note"):
                    add_markdown(inline(note).strip(), source)
                if element.select_one("details.key-proof"):
                    add_markdown(compact_proof(route), source)
            else:
                spec = numerical[cell_id]
                lead = spec["lead"]
                original_code = spec.get("source", spec.get("code"))
                assert original_code, f"No Python body supplied for {cell_id}."
                add_markdown(lead, source)
                flush()
                cells.append(new_code(cell_id, original_code, source))
                code_checks.append({"id": cell_id, "kind": "python", "body_sha256": sha256(original_code), "requires": spec["requires"]})
        elif element.name == "figure":
            image_tag = element.select_one("img")
            caption = element.select_one("figcaption")
            image_src = image_tag["src"]
            match = re.fullmatch(r"data:(image/[a-zA-Z0-9.+-]+);base64,(.+)", image_src, re.S)
            assert match, "Original report figure is not embedded."
            mime, payload = match.groups()
            payload = "".join(payload.split())
            payload_bytes = base64.b64decode(payload, validate=True)
            filename = f"report-figure-{len(image_checks)+1}.png"
            alt = image_tag.get("alt", "").replace("[", "\\[").replace("]", "\\]")
            if image_mode == "attachments":
                attachments[filename] = {mime: payload}
                add_markdown(f"![{alt}](attachment:{filename})\n\n{inline(caption).strip()}", source)
            elif image_mode == "data-uri":
                add_markdown(f"![{alt}](data:{mime};base64,{payload})\n\n{inline(caption).strip()}", source)
            else:
                raise ValueError(image_mode)
            image_checks.append({"filename": filename, "caption": caption.get_text(), "alt": image_tag.get("alt", ""), "mime": mime, "bytes": len(payload_bytes), "sha256": sha256(payload_bytes), "source": source})
        elif element.name == "table":
            converted = table_markdown(element)
            add_markdown(converted, source)
            table_checks.append({"source": source, "rows": [[cell.get_text() for cell in row.find_all(["th", "td"])] for row in element.find_all("tr")], "markdown_sha256": sha256(converted)})
        elif element.name in {"p", "div"}:
            add_markdown(inline(element).strip(), source)
        else:
            raise AssertionError(f"Unrecognized main body element {index}: {element.name}")
    flush()

    notebook = {
        "cells": cells,
        "metadata": {
            "colab": {"name": "Report.ipynb", "provenance": [], "toc_visible": True},
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.12"},
            "report_conversion": {"source_name": source_path.name, "source_sha256": sha256(html), "image_mode": image_mode},
        },
        "nbformat": 4, "nbformat_minor": 5,
    }
    all_markdown = "\n\n".join("".join(cell["source"]) for cell in cells if cell["cell_type"] == "markdown")
    source_math = DISPLAY_MATH.findall(main.get_text())
    notebook_math = DISPLAY_MATH.findall(all_markdown)
    assert source_math == notebook_math, "One or more display formulas changed in conversion."
    source_tags = EQUATION_TAG.findall(main.get_text())
    notebook_tags = EQUATION_TAG.findall(all_markdown)
    assert source_tags == notebook_tags, "Equation tags changed or lost ordering."
    assert len(code_checks) == 20 and sum(check["kind"] == "lean" for check in code_checks) == 6
    assert len(image_checks) == 4 and len(table_checks) == 2
    assert not re.search(r"<(?:script|style|button|textarea|nav|section|details)\b", all_markdown)
    assert "JavaScript" not in all_markdown and "Report.exe" not in all_markdown
    assert len({cell["id"] for cell in cells}) == len(cells)
    destination.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    validation = {
        "source": str(source_path), "source_sha256": sha256(html),
        "notebook": str(destination), "notebook_sha256": sha256(destination.read_bytes()),
        "format": {"nbformat": 4, "nbformat_minor": 5},
        "cell_counts": {"all": len(cells), "markdown": sum(c["cell_type"] == "markdown" for c in cells), "code": sum(c["cell_type"] == "code" for c in cells), "lean": 6, "numerical": 14, "bootstrap": 1},
        "headers": header_checks,
        "source_body_elements_preserved": included,
        "removed_html_transport": omitted,
        "prose_adaptations": adapted,
        "display_formulas": {"source_count": len(source_math), "notebook_count": len(notebook_math), "identical_in_order": True, "body_sha256": [sha256(body) for body in source_math]},
        "equation_tags": {"source": source_tags, "notebook": notebook_tags, "identical_in_order": True},
        "tables": table_checks, "figures": image_checks, "image_mode": image_mode,
        "code": code_checks,
        "proof_guides": {"uw_points": 4, "qrm_points": 3, "full_dependency_listings_embedded": False},
        "outputs": "Unexecuted code cells; outputs are populated by the actual kernel.",
        "no_custom_html_ui": True,
    }
    (HERE / "build_validation.json").write_text(json.dumps(validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"notebook": str(destination), "cells": validation["cell_counts"], "display_formulas": len(source_math), "equation_tags": len(source_tags), "figures": len(image_checks), "sha256": validation["notebook_sha256"]}, ensure_ascii=False))
    return notebook


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=REPORT)
    parser.add_argument("--output", type=Path, default=HERE / "Report.ipynb")
    parser.add_argument("--image-mode", choices=["attachments", "data-uri"], default="attachments")
    args = parser.parse_args()
    build(args.source, args.output, args.image_mode)
