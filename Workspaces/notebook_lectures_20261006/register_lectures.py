"""Register the lecture deliverables; preserve all earlier registration evidence."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil

import nbformat

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DEST = ROOT / "notebook" / "讲稿"
REGISTRATION = HERE / "registration.json"
BACKUP = HERE / "before_records"
RECORD_NAMES = ("PROGRESS_LOG.md", "FILE_INDEX.md")
INDEX_BEGIN = "<!-- NOTEBOOK_LECTURES_INDEX_BEGIN -->"
INDEX_END = "<!-- NOTEBOOK_LECTURES_INDEX_END -->"
INDEX_ANCHOR = "<!-- NOTEBOOK_REPORTS_INDEX_BEGIN -->"
NOTEBOOK_NAMES = ("非线性化report.ipynb", "2HS数值分析report.ipynb", "DLW数值分析report.ipynb")
BODY_NAMES = ("nonlinear_body.html", "hs_body.html", "dlw_body.html")
SCRIPT_NAMES = ("build_lectures.py", "verify_lecture_content.py", "check_lectures.cjs",
                "fix_hs_reference.py", "register_lectures.py")
EVIDENCE_NAMES = ("build_validation.json", "content_validation.json",
                  "browser_validation.json", "hs_reference_correction.json")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def item(path: Path) -> dict:
    assert path.is_file(), f"Missing registered file: {path}"
    return {"path": path.relative_to(ROOT).as_posix(),
            "sha256": sha(path), "bytes": path.stat().st_size}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def code_payload(notebook) -> bytes:
    data = [{"id": c.id, "source": c.source, "execution_count": c.execution_count,
             "outputs": c.outputs} for c in notebook.cells if c.cell_type == "code"]
    return json.dumps(data, ensure_ascii=False, sort_keys=True).encode("utf-8")


def check_evidence() -> dict:
    build, content, browser, correction = (
        read_json(HERE / name) for name in EVIDENCE_NAMES)
    assert all(report["success"] is True for report in (build, content, browser, correction))
    assert len(build["reports"]) == len(content["reports"]) == len(browser["reports"]) == 3
    for report in build["reports"] + content["reports"]:
        assert sha(Path(report["lecture"])) == report["sha256"], report["lecture"]
        assert sha(Path(report["notebook"])) == report["notebook_sha256"], report["notebook"]
    covered = [len(report["code_cells_covered"]) for report in content["reports"]]
    excerpt_counts = [len(report["excerpts"]) for report in content["reports"]]
    assert covered == [14, 13, 15] and excerpt_counts == [21, 16, 20]
    for report in browser["reports"]:
        assert report["passed"] is True and not report["errors"]
        assert not report["remote"] and not report["failed"]
        for view in ("desktop", "mobile", "print"):
            result = report[view]
            assert not result["overflow"] and not result["mathErrors"]
            assert not result["rawMath"] and not result["brokenImages"]
            assert not result["missingAnchors"] and not result["duplicateIds"]
    current_hs = ROOT / "notebook" / NOTEBOOK_NAMES[1]
    old_hs = HERE / "before_reference_fix" / NOTEBOOK_NAMES[1]
    assert sha(current_hs) == correction["after_sha256"]
    assert sha(old_hs) == correction["before_sha256"]
    before, after = nbformat.read(old_hs, 4), nbformat.read(current_hs, 4)
    assert len(before.cells) == len(after.cells)
    changed = []
    for left, right in zip(before.cells, after.cells):
        if left != right:
            changed.append(left.id)
            assert left.id == right.id == correction["markdown_cell"]
            expected = dict(left)
            expected["source"] = left.source.replace(correction["old_reference"],
                                                     correction["correct_reference"])
            assert expected == right
    assert changed == ["hs-time-model"]
    before_code, after_code = code_payload(before), code_payload(after)
    assert before_code == after_code
    assert hashlib.sha256(after_code).hexdigest() == correction["code_and_output_digest"]
    assert correction["code_sources_and_actual_outputs_unchanged"] is True
    return {"build_passed": True, "content_passed": True, "browser_passed": True,
            "code_cells_covered": covered, "code_excerpts": excerpt_counts,
            "hs_only_markdown_reference_changed": True,
            "hs_code_and_actual_outputs_unchanged": True}


def source_paths() -> list[Path]:
    return ([ROOT / "notebook" / name for name in NOTEBOOK_NAMES]
            + [HERE / name for name in BODY_NAMES + SCRIPT_NAMES]
            + [HERE / "README.md"])


def evidence_paths() -> list[Path]:
    return ([HERE / name for name in EVIDENCE_NAMES]
            + sorted(HERE.glob("lecture_*.png"))
            + [HERE / "before_reference_fix" / NOTEBOOK_NAMES[1],
               HERE / "before_reference_fix" / "hs_execution_validation.json",
               ROOT / "Workspaces/notebook_reports_20261006/hs_execution_validation.json"])


def delivery_paths() -> list[Path]:
    paths = sorted(path for path in DEST.rglob("*") if path.is_file())
    expected = {DEST / name for name in
                ("非线性化讲稿.html", "2HS数值分析讲稿.html", "DLW数值分析讲稿.html")}
    assert expected.issubset(paths)
    assert (DEST / "assets" / "KaTeX-LICENSE.txt").is_file()
    return paths


def backup_records() -> None:
    BACKUP.mkdir(exist_ok=True)
    for name in RECORD_NAMES:
        source, target = ROOT / name, BACKUP / name
        if not target.exists():
            shutil.copy2(source, target)
        assert target.is_file()


def update_progress() -> None:
    additions = {
        "> **2026-10-06（非线性化与2HS独立笔记本）：**":
            "**配套讲稿（2026-10-06）：** 新增 [非线性化讲稿](notebook/讲稿/非线性化讲稿.html)"
            " 与 [2HS数值分析讲稿](notebook/讲稿/2HS数值分析讲稿.html)，分别以12节／7节覆盖14／13个实际代码单元，"
            "解释双线性StartPoint至Lean终点、Q/R非零与格点重构，以及2HS坐标链式法则、m/rho推进、RK4与公共物理点误差。"
            "非线性化原式（1）—（22）保持，关键摘录均为真实连续源码且每块≤12行；纵向截断残差与有限时间场误差分别说明。"
            "仅校正2HS的hs-time-model正文公式引用“式（4）或（28）”为“式（4）或（6）”，代码、执行计数与实际输出摘要不变，"
            "修改前笔记本及执行证据保留。三份讲稿共用本地KaTeX与原保存PNG；真实Edge桌面／390px／打印检查全部通过，"
            "无公式错误、页面溢出、坏图、失效锚点或远程请求。构建、核验、截图与记录修改前备份见 "
            "[讲稿项目](Workspaces/notebook_lectures_20261006/README.md)，当前来源及交付哈希见 registration.json。",
        "> **2026-10-06（DLW数值分析笔记本）：**":
            "**配套讲稿（2026-10-06）：** 新增 [DLW数值分析讲稿](notebook/讲稿/DLW数值分析讲稿.html)，"
            "12节覆盖15个实际代码单元、20个真实连续源码摘录；按物理初值与lift、SD/SD2/FD右端、Euler/RK4逐级边界、"
            "ALE节点更新和配对误差评价讲解既有实验，明确T=0.01与所用格距下结果的适用范围。"
            "图取自笔记本已保存输出，本轮未新增PDE轨道；真实Edge桌面／390px／打印及源码对应检查通过。"
            "正文源、生成器、核验脚本、截图及交付哈希见 "
            "[讲稿项目](Workspaces/notebook_lectures_20261006/README.md)。",
    }
    path = ROOT / "PROGRESS_LOG.md"
    text = path.read_bytes().decode("utf-8")
    for prefix, addition in additions.items():
        assert text.count(prefix) == 1, prefix
        line = next(line for line in text.splitlines() if line.startswith(prefix))
        if "**配套讲稿（2026-10-06）：**" not in line:
            text = text.replace(prefix, prefix + " " + addition, 1)
    path.write_bytes(text.encode("utf-8"))


def index_line(path: Path, description: str) -> str:
    relative = path.relative_to(ROOT).as_posix()
    return f"- [{relative}]({relative})（{description}）"


def index_block() -> str:
    lines = [INDEX_BEGIN, "", "**三份笔记本的配套讲稿（2026-10-06）：**", "",
             index_line(HERE / "README.md", "构建、核验与登记入口")]
    labels = {"非线性化讲稿.html": "双线性起点、两路Lean终点与DLW纵向截断残差讲稿",
              "2HS数值分析讲稿.html": "单／二孤子解析场、空间格式、RK4与物理点误差讲稿",
              "DLW数值分析讲稿.html": "初值lift、SD／SD2／FD、时间推进及配对实验讲稿"}
    for path in delivery_paths():
        if path.suffix == ".html":
            description = labels[path.name]
        elif path.parent.name == "fonts":
            description = "KaTeX本地字体"
        elif path.suffix == ".png":
            description = "笔记本已保存的原PNG输出"
        elif path.name == "KaTeX-LICENSE.txt":
            description = "KaTeX许可证"
        elif path.name.startswith("lecture."):
            description = "讲稿共用本地样式／公式初始化"
        else:
            description = "KaTeX本地排版资源"
        lines.append(index_line(path, description))
    for name in BODY_NAMES:
        lines.append(index_line(HERE / name, "对应讲稿的权威正文源"))
    script_labels = {"build_lectures.py": "包装正文、复制本地资源并提取原图的生成器",
                     "verify_lecture_content.py": "全部42代码单元覆盖与57个真实连续摘录、链接核验",
                     "check_lectures.cjs": "真实Edge桌面／窄屏／打印、公式与资源检查",
                     "fix_hs_reference.py": "仅校正2HS正文引用式（4）或（28）为式（4）或（6）",
                     "register_lectures.py": "备份根记录、合并既有专题并登记当前哈希"}
    for name in SCRIPT_NAMES:
        lines.append(index_line(HERE / name, script_labels[name]))
    evidence_labels = {"build_validation.json": "三份构建结果、来源及交付哈希",
                       "content_validation.json": "真实源码摘录、全部代码单元覆盖与链接证据",
                       "browser_validation.json": "桌面／390px／打印通过、公式与资源证据",
                       "hs_reference_correction.json": "2HS仅正文引用校正及代码／实际输出不变摘要"}
    for name in EVIDENCE_NAMES:
        lines.append(index_line(HERE / name, evidence_labels[name]))
    for path in sorted(HERE.glob("lecture_*.png")):
        lines.append(index_line(path, "讲稿真实浏览器截图；1非线性化／2为2HS／3为DLW"))
    lines.extend([
        index_line(HERE / "before_reference_fix" / NOTEBOOK_NAMES[1], "正文公式引用校正前的2HS笔记本"),
        index_line(HERE / "before_reference_fix" / "hs_execution_validation.json", "校正前执行证据"),
        index_line(ROOT / "Workspaces/notebook_reports_20261006/hs_execution_validation.json",
                   "既有实跑证据；保留执行哈希并注明正文引用校正"),
        index_line(BACKUP / "PROGRESS_LOG.md", "本轮讲稿登记前的根进度记录"),
        index_line(BACKUP / "FILE_INDEX.md", "本轮讲稿登记前的逐文件索引"),
        index_line(REGISTRATION, "交付／资源／当前来源及前后记录SHA-256登记"),
        "", INDEX_END])
    return "\n".join(lines)


def update_index() -> None:
    path = ROOT / "FILE_INDEX.md"
    text = path.read_bytes().decode("utf-8")
    block = index_block()
    assert text.count(INDEX_ANCHOR) == 1
    if INDEX_BEGIN not in text:
        assert INDEX_END not in text
        text = text.replace(INDEX_ANCHOR, block + "\n\n" + INDEX_ANCHOR, 1)
    else:
        assert text.count(INDEX_BEGIN) == text.count(INDEX_END) == 1
        begin = text.index(INDEX_BEGIN)
        end = text.index(INDEX_END) + len(INDEX_END)
        assert text[begin:end] == block
        assert end < text.index(INDEX_ANCHOR)
    path.write_bytes(text.encode("utf-8"))


def verify_registration() -> dict:
    manifest = read_json(REGISTRATION)
    count = 0
    for group in ("deliverables", "sources", "evidence"):
        for record in manifest[group]:
            path = ROOT / record["path"]
            assert path.is_file() and sha(path) == record["sha256"], record["path"]
            count += 1
    for record in manifest["records"]:
        assert sha(ROOT / record["path"]) == record["after_sha256"]
        assert sha(ROOT / record["backup"]) == record["before_sha256"]
        count += 2
    index = (ROOT / "FILE_INDEX.md").read_bytes().decode("utf-8")
    assert index.count(INDEX_BEGIN) == index.count(INDEX_END) == 1
    assert index.index(INDEX_END) < index.index(INDEX_ANCHOR)
    for title in ("非线性化与2HS独立笔记本", "DLW数值分析笔记本"):
        assert (ROOT / "PROGRESS_LOG.md").read_text("utf-8").count(
            f"2026-10-06（{title}）") == 1
    return {"success": True, "mode": "verify", "tracked_files_checked": count,
            "registration_sha256": sha(REGISTRATION)}


def register() -> dict:
    if REGISTRATION.exists():
        return verify_registration()
    checks = check_evidence()
    tracked = delivery_paths() + source_paths() + evidence_paths()
    unchanged_before = {str(path): sha(path) for path in tracked}
    backup_records()
    update_progress()
    update_index()
    assert all(sha(Path(path)) == digest for path, digest in unchanged_before.items())
    records = [{"path": name, "backup": (BACKUP / name).relative_to(ROOT).as_posix(),
                "before_sha256": sha(BACKUP / name), "after_sha256": sha(ROOT / name)}
               for name in RECORD_NAMES]
    manifest = {"schema_version": 1, "created_at_utc": datetime.now(timezone.utc).isoformat(),
                "root": str(ROOT), "project": HERE.relative_to(ROOT).as_posix(),
                "deliverables": [item(path) for path in delivery_paths()],
                "sources": [item(path) for path in source_paths()],
                "evidence": [item(path) for path in evidence_paths()],
                "records": records, "checks": checks,
                "lecture_notebook_and_asset_files_unchanged_during_registration": True,
                "historical_registration_files_not_modified": True}
    with REGISTRATION.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(manifest, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    result = verify_registration()
    result["mode"] = "register"
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true", help="Read-only hash verification.")
    options = parser.parse_args()
    result = verify_registration() if options.verify else register()
    print(json.dumps(result, ensure_ascii=False, indent=2))
