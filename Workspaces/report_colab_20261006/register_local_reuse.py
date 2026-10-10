"""Merge the verified local-runtime delivery into the existing Report records."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parents[1]
BACKUP = HERE / "before_local_reuse"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    summary = json.loads((HERE / "local_reuse_summary.json").read_text(encoding="utf-8"))
    assert summary["ready_for_registration"] is True
    delivery = Path(summary["local_notebook"])
    assert delivery.is_file()
    assert digest(delivery.read_bytes()) == summary["local_notebook_sha256"]
    assert delivery.read_bytes() == (HERE / "Report.ipynb").read_bytes()
    execution = json.loads((HERE / "execution_validation.json").read_text(encoding="utf-8"))
    assert execution["success"] and not execution["error_outputs"]
    assert execution["notebook_sha256"] == summary["local_notebook_sha256"]
    assert len(execution["code_cells"]) == 21
    for evidence in ("local_runtime_validation.json", "local_lean_validation.json",
                     "lean_seed_chronology_validation.json", "local_import_smoke_validation.json"):
        assert json.loads((HERE / evidence).read_text(encoding="utf-8"))["passed"] is True
    helper_hash = digest((HERE / "lean_notebook.py").read_bytes())
    assert summary["helper_sha256"] == helper_hash
    assert json.loads((HERE / "local_import_smoke_validation.json").read_text(
        encoding="utf-8"))["helper_sha256"] == helper_hash
    paths = [WORKSPACE / "PROGRESS_LOG.md", WORKSPACE / "FILE_INDEX.md"]
    originals = {path: path.read_bytes() for path in paths}
    BACKUP.mkdir(exist_ok=True)
    for path, data in originals.items():
        backup = BACKUP / path.name
        if not backup.exists():
            backup.write_bytes(data)
    progress, index = [originals[path].decode("utf-8") for path in paths]
    newline = "\r\n" if "\r\n" in progress else "\n"

    report_entry = re.search(
        r"^> \*\*2026-10-06（Report (?:原生 Colab|本地 Lean) 笔记本）：\*\* ([^\r\n]+)(?:\r?\n)?",
        progress, re.MULTILINE,
    )
    if report_entry is None:
        raise RuntimeError("Existing Report entry was not found; do not append a duplicate.")
    history_separator = " **此前 HTML 可运行报告与形式证明（2026-10-02）：** "
    assert history_separator in report_entry.group(1)
    history = report_entry.group(1).split(history_separator, 1)[1]
    replacement = (
        "> **2026-10-06（Report 本地 Lean 笔记本）：** " + summary["progress_body"]
        + history_separator + history + newline
    )
    new_progress = progress[:report_entry.start()] + replacement + progress[report_entry.end():]
    assert new_progress[:report_entry.start()] == progress[:report_entry.start()]
    assert new_progress[len(progress[:report_entry.start()] + replacement):] == progress[report_entry.end():]

    begin, end = "<!-- REPORT_COLAB_INDEX_BEGIN -->", "<!-- REPORT_COLAB_INDEX_END -->"
    assert index.count(begin) == index.count(end) == 1
    section_pattern = re.compile(re.escape(begin) + r".*?" + re.escape(end), re.DOTALL)
    section = (
        begin + newline + newline + "**Report 本地 Lean 笔记本（2026-10-06）：**"
        + newline + newline + summary["index_body"].replace("\n", newline)
        + newline + newline + end
    )
    new_index = section_pattern.sub(lambda _match: section, index, count=1)
    for pair in summary["index_replacements"]:
        assert new_index.count(pair["old"]) == 1
        new_index = new_index.replace(pair["old"], pair["new"], 1)
    for relative in summary["indexed_paths"]:
        target = WORKSPACE / relative
        assert target.exists() or target == HERE / "local_reuse_registration.json", relative

    updated = {paths[0]: new_progress.encode("utf-8"), paths[1]: new_index.encode("utf-8")}
    for path, data in updated.items():
        path.write_bytes(data)
    registration = {
        "topic": "Report existing local Lean runtime", "date": "2026-10-06",
        "local_notebook": str(delivery),
        "records": [
            {"path": str(path), "before_sha256": digest(originals[path]),
             "after_sha256": digest(updated[path]), "backup": str(BACKUP / path.name)}
            for path in paths
        ],
        "existing_report_entry_merged": True,
        "unrelated_progress_entries_preserved": True,
        "validation": {
            "unrelated_progress_blocks_unchanged": True,
            "single_merged_report_entry": new_progress.count("（Report 本地 Lean 笔记本）") == 1,
            "current_report_entry_first": new_progress.startswith("> **2026-10-06（Report 本地 Lean 笔记本）"),
            "indexed_paths_checked": len(summary["indexed_paths"]),
            "indexed_paths_all_exist": True,
            "delivery_mirror_bytes_equal": True,
        },
    }
    (HERE / "local_reuse_registration.json").write_text(
        json.dumps(registration, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    assert all((WORKSPACE / relative).exists() for relative in summary["indexed_paths"])
    print("Report local-runtime records merged and indexed paths verified.")


if __name__ == "__main__":
    main()
