"""Register the verified three-notebook delivery without replacing its history."""
from __future__ import annotations

from datetime import datetime
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SUMMARY = HERE / "registration_summary.json"
REPORT_MARKERS = ("<!-- NOTEBOOK_REPORTS_INDEX_BEGIN -->", "<!-- NOTEBOOK_REPORTS_INDEX_END -->")
REPORT_PATHS = (
    "notebook/非线性化report.ipynb",
    "notebook/2HS数值分析report.ipynb",
    "notebook/DLW数值分析report.ipynb",
)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def notebook_counts(path: Path) -> dict:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    cells = notebook["cells"]
    errors = [
        {"cell": i, "ename": out.get("ename"), "evalue": out.get("evalue")}
        for i, cell in enumerate(cells)
        for out in cell.get("outputs", [])
        if out.get("output_type") == "error"
    ]
    assert not errors, (path, errors)
    return {
        "cells": len(cells),
        "markdown_cells": sum(c["cell_type"] == "markdown" for c in cells),
        "code_cells": sum(c["cell_type"] == "code" for c in cells),
        "error_outputs": len(errors),
    }


def merge_entry(text: str, label: str, new_label: str, body: str, separator: str) -> str:
    pattern = re.compile(
        r"^> \*\*2026-10-06（(?:" + label + "|" + re.escape(new_label)
        + r")）：\*\* ([^\r\n]+)", re.MULTILINE,
    )
    matches = list(pattern.finditer(text))
    assert len(matches) == 1, (label, len(matches))
    match = matches[0]
    history = match.group(1)
    if separator in history:
        history = history.split(separator, 1)[1]
    replacement = "> **2026-10-06（" + new_label + "）：** " + body + separator + history
    result = text[:match.start()] + replacement + text[match.end():]
    assert result[:match.start()] == text[:match.start()]
    assert result[match.start() + len(replacement):] == text[match.end():]
    return result


def indexed_files() -> list[Path]:
    files = []
    for path in HERE.rglob("*"):
        if not path.is_file():
            continue
        if any(part in {"__pycache__", ".ipynb_checkpoints", ".local_runtime"}
               for part in path.relative_to(HERE).parts):
            continue
        files.append(path)
    files.extend(ROOT / rel for rel in REPORT_PATHS)
    files.extend((ROOT / "notebook/启动Colab本地运行时.pyw", ROOT / "report/notebook_usage.html"))
    files.extend((ROOT / "report/Report_原HTML_20261006.html",
                  ROOT / "report/DLW数值分析_原HTML_20261006.html"))
    files.append(HERE / "registration.json")
    return sorted(set(files), key=lambda p: p.relative_to(ROOT).as_posix())


def main() -> None:
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert summary["ready_for_registration"] is True
    reports = summary["reports"]
    assert {r["relative_path"] for r in reports} == set(REPORT_PATHS)
    validated = []
    for report in reports:
        path = ROOT / report["relative_path"]
        assert path.is_file(), str(path)
        assert sha(path.read_bytes()) == report["sha256"], str(path)
        counts = notebook_counts(path)
        assert counts["code_cells"] == report["code_cells"], str(path)
        assert all(c.get("execution_count") is not None for c in
                   json.loads(path.read_text(encoding="utf-8"))["cells"]
                   if c["cell_type"] == "code"), str(path)
        evidence_path = ROOT / report["validation_path"]
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
        assert evidence.get("passed", evidence.get("success", False)) is True, str(evidence_path)
        validated.append({**report, **counts})
    for original in summary["original_reports"]:
        path = ROOT / original["relative_path"]
        assert sha(path.read_bytes()) == original["sha256"], str(path)
    backup_notebook = HERE / "before_split/Report.ipynb"
    assert backup_notebook.is_file()
    assert not (ROOT / "notebook/Report.ipynb").exists()

    records = (ROOT / "PROGRESS_LOG.md", ROOT / "FILE_INDEX.md")
    originals = {p: p.read_bytes() for p in records}
    backup_dir = HERE / "before_registration"
    if any((backup_dir / p.name).exists() for p in records):
        backup_dir = HERE / ("before_registration_" + datetime.now().strftime("%Y%m%d_%H%M%S"))
    backup_dir.mkdir(parents=True, exist_ok=False)
    for path, data in originals.items():
        (backup_dir / path.name).write_bytes(data)

    progress = originals[records[0]].decode("utf-8")
    index = originals[records[1]].decode("utf-8")
    newline = "\r\n" if "\r\n" in index else "\n"
    progress = merge_entry(
        progress, "Report (?:原生 Colab|本地 Lean) 笔记本", "非线性化与2HS独立笔记本",
        summary["report_progress_body"], " **此前混合笔记本与本地 Lean 运行（2026-10-06）：** ",
    )
    progress = merge_entry(
        progress, "Index阅读与算法展示", "DLW数值分析笔记本",
        summary["dlw_progress_body"], " **此前Index阅读与算法展示（2026-10-06）：** ",
    )
    # Keep earlier delivery references readable after the former primary is moved.
    progress = progress.replace("[notebook/Report.ipynb](notebook/Report.ipynb)",
        "[原混合笔记本](Workspaces/notebook_reports_20261006/before_split/Report.ipynb)")

    overview_old = "当前本地 Lean 笔记本见 [notebook/Report.ipynb](notebook/Report.ipynb)。"
    overview_new = ("当前可运行笔记本分别为 [非线性化](notebook/非线性化report.ipynb)、"
                    "[2HS数值分析](notebook/2HS数值分析report.ipynb) 与 "
                    "[DLW数值分析](notebook/DLW数值分析report.ipynb)，"
                    "运行步骤见 [使用说明](report/notebook_usage.html)。")
    if overview_old in index:
        index = index.replace(overview_old, overview_new, 1)
    report_row_old = ("当前本地 Lean 笔记本为 [notebook/Report.ipynb](notebook/Report.ipynb)："
        "DLW 两路 Lean、2HS 场误差及 DLW 截断残差；第 3 章残差不等于演化场总误差。")
    report_row_new = ("当前拆为 [非线性化](notebook/非线性化report.ipynb) 与 "
        "[2HS数值分析](notebook/2HS数值分析report.ipynb)；前者保留 DLW 两路 Lean "
        "和空间残差估计，后者独立进行 2HS 数值比较。")
    if report_row_old in index:
        index = index.replace(report_row_old, report_row_new, 1)
    index = index.replace(
        "| [index.html](index.html) | DLW 数值比较主报告：三组孤子、实际误差与最优值、递推伪代码、12张彩色误差曲线。 |",
        "| [index.html](index.html) | DLW 数值比较主报告；可运行版为 [DLW数值分析report.ipynb](notebook/DLW数值分析report.ipynb)：三组孤子、三种空间方案与时间推进、实际误差和曲线。 |", 1,
    )
    index = index.replace("**Report 本地 Lean 笔记本（2026-10-06）：**",
                          "**此前混合版迁移与共用本地运行时（2026-10-06）：**", 1)
    index = index.replace(
        "- [Report.html](Report.html)（迁移正文来源与此前 HTML 运行版；当前本地 Lean notebook 见下方 Report 笔记本索引）",
        "- [Report.html](Report.html)（迁移正文来源与此前 HTML 运行版；当前三份可运行报告见下方独立笔记本索引）", 1,
    )
    index = index.replace(
        "- [notebook/Report.ipynb](notebook/Report.ipynb)（当前交付；六行本地 import，42标准单元，21代码单元实际执行约110.91秒、零错误，输出已保存）",
        "- [before_split/Report.ipynb](Workspaces/notebook_reports_20261006/before_split/Report.ipynb)（拆分前混合版保留；42标准单元、21代码单元实际执行约110.91秒、零错误）", 1,
    )
    index = index.replace(
        "- `Workspaces/report_colab_20261006/Report.ipynb`（当前项目内镜像；根目录notebook为主交付）",
        "- `Workspaces/report_colab_20261006/Report.ipynb`（此前混合版项目镜像；共用运行时仍在该项目，当前三份交付见上方新索引）", 1,
    )
    index = index.replace("[notebook/Report.ipynb](notebook/Report.ipynb)",
                          "[原混合笔记本](Workspaces/notebook_reports_20261006/before_split/Report.ipynb)")

    paths = indexed_files()
    for path in paths:
        assert path.is_file() or path == HERE / "registration.json", str(path)
    begin, end = REPORT_MARKERS
    description = {
        REPORT_PATHS[0]: "当前主交付；DLW 两路非线性化、Lean 起点至终点与空间残差估计",
        REPORT_PATHS[1]: "当前主交付；2HS 数值推进、误差表和图",
        REPORT_PATHS[2]: "当前主交付；DLW 三组孤子与空间、时间方案数值比较",
        "notebook/启动Colab本地运行时.pyw": "三份共用的本地运行时启动器",
        "report/notebook_usage.html": "VS Code、Colab 与逐段执行的用户使用说明",
        "report/Report_原HTML_20261006.html": "原综合 HTML 留档；保持原相对链接",
        "report/DLW数值分析_原HTML_20261006.html": "原 DLW 数值 HTML 留档；保持原相对链接",
        "Workspaces/notebook_reports_20261006/README.md": "新项目的结构、运行与证据入口",
        "Workspaces/notebook_reports_20261006/before_split/Report.ipynb": "拆分前混合版原本保留",
        "Workspaces/notebook_reports_20261006/before_split/Report.original_delivery.ipynb": "从根 notebook 目录移入的原交付文件，与固定混合版源字节一致",
        "Workspaces/notebook_reports_20261006/before_split/report_colab_README.md": "共用运行时项目说明在更新当前入口前的原稿",
        "Workspaces/notebook_reports_20261006/registration_summary.json": "最终执行结果与交付哈希汇总",
        "Workspaces/notebook_reports_20261006/register_notebook_split.py": "同专题合并登记与逐文件路径核对",
        "Workspaces/notebook_reports_20261006/registration.json": "本次登记与共享记录哈希",
    }
    lines = [begin, "", "**非线性化、2HS 与 DLW 独立笔记本（2026-10-06）：**", ""]
    for path in paths:
        relative = path.relative_to(ROOT).as_posix()
        suffix = "（" + description[relative] + "）" if relative in description else ""
        lines.append("- [" + relative + "](" + relative + ")" + suffix)
    lines.extend(("", end))
    section = newline.join(lines)
    if begin in index:
        assert index.count(begin) == index.count(end) == 1
        index = re.sub(re.escape(begin) + r".*?" + re.escape(end),
                       lambda _: section, index, count=1, flags=re.DOTALL)
    else:
        anchor = "<!-- REPORT_COLAB_INDEX_BEGIN -->"
        assert index.count(anchor) == 1
        index = index.replace(anchor, section + newline + newline + anchor, 1)

    updates = {records[0]: progress.encode("utf-8"), records[1]: index.encode("utf-8")}
    for path, data in updates.items():
        path.write_bytes(data)
    registration = {
        "date": "2026-10-06", "reports": validated,
        "existing_report_and_index_topics_merged": True,
        "indexed_paths": [p.relative_to(ROOT).as_posix() for p in paths],
        "records": [{"path": str(path), "before_sha256": sha(originals[path]),
                     "after_sha256": sha(updates[path]), "backup": str(backup_dir / path.name)}
                    for path in records],
    }
    (HERE / "registration.json").write_text(
        json.dumps(registration, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    assert all(path.is_file() for path in paths)
    print("Three notebook reports registered; existing topic history and all indexed paths preserved.")


if __name__ == "__main__":
    main()
