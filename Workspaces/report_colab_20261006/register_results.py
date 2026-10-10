"""Merge this project's final evidence into the existing Report records.

Run only after final_summary.json has been checked against local and cloud
validation. The original records are backed up; unrelated topics are preserved.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parent.parent


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def main() -> None:
    summary = json.loads((HERE / "final_summary.json").read_text(encoding="utf-8"))
    assert summary["ready_for_registration"] is True
    progress_path, index_path = WORKSPACE / "PROGRESS_LOG.md", WORKSPACE / "FILE_INDEX.md"
    originals = {path: path.read_bytes() for path in (progress_path, index_path)}
    progress, index = [originals[path].decode("utf-8") for path in (progress_path, index_path)]
    newline = "\r\n" if "\r\n" in progress else "\n"

    match = re.search(
        r"^> \*\*2026-10-02（Report两路非线性化Lean证明与可运行报告）：\*\* ([^\r\n]+)(?:\r?\n)?",
        progress, re.MULTILINE,
    )
    if not match:
        raise RuntimeError("Existing Report progress entry was not found; do not append a duplicate.")
    old_body = match.group(1)
    replacement = (
        "> **2026-10-06（Report 原生 Colab 笔记本）：** " + summary["progress_body"] +
        " **此前 HTML 可运行报告与形式证明（2026-10-02）：** " + old_body + newline + newline
    )
    remaining = progress[:match.start()] + progress[match.end():]
    # Preserve every non-Report entry byte-for-byte, changing only this topic's location.
    progress = replacement + remaining

    marker = "<!-- REPORT_NOTEBOOK_INDEX_BEGIN -->"
    assert index.count(marker) == 1
    assert "<!-- REPORT_COLAB_INDEX_BEGIN -->" not in index
    section = (
        newline + newline + "<!-- REPORT_COLAB_INDEX_BEGIN -->" + newline + newline +
        "**Report 原生 Colab 笔记本（2026-10-06）：**" + newline + newline +
        summary["index_body"].replace("\n", newline) + newline + newline +
        "<!-- REPORT_COLAB_INDEX_END -->"
    )
    index = index.replace(marker, marker + section, 1)
    index = index.replace(
        "**Report 单入口与逐段运行（2026-10-02）：**",
        "**此前 Report HTML 单入口与逐段运行（2026-10-02）：**", 1,
    )
    if summary.get("reading_map_old"):
        old = summary["reading_map_old"]
        assert index.count(old) == 1
        index = index.replace(old, summary["reading_map_new"], 1)
    for pair in summary.get("index_replacements", []):
        assert index.count(pair["old"]) == 1
        index = index.replace(pair["old"], pair["new"], 1)

    backup = HERE / "before_records"
    backup.mkdir(exist_ok=True)
    for path, data in originals.items():
        destination = backup / path.name
        assert not destination.exists(), "Do not overwrite the original records backup."
        destination.write_bytes(data)
    updated = {progress_path: progress.encode("utf-8"), index_path: index.encode("utf-8")}
    for path, data in updated.items():
        path.write_bytes(data)
    registration = {
        "topic": "Report native Colab notebook", "date": "2026-10-06",
        "cloud_url": summary.get("cloud_url"),
        "records": [
            {"path": str(path), "before_sha256": digest(originals[path]),
             "after_sha256": digest(updated[path]), "backup": str(backup / path.name)}
            for path in originals
        ],
        "existing_report_entry_merged": True,
        "unrelated_progress_entries_preserved": True,
    }
    (HERE / "registration.json").write_text(
        json.dumps(registration, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    print(json.dumps(registration, ensure_ascii=False))


if __name__ == "__main__":
    main()
