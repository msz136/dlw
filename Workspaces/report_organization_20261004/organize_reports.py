"""Rebase links for the report-folder move and verify the final layout."""
from pathlib import Path
from html import unescape
from html.parser import HTMLParser
from urllib.parse import urlsplit, urlunsplit, unquote
import argparse
import hashlib
import json
import os
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
MOVED = (
    "dlw_bilinear_nonlinear_lean.html", "dlw_conserved_mesh.html",
    "dlw_error_theory.html", "dlw_integrability_status.html",
    "dlw_research_ideas.html", "dlw_waveform_fields.html",
    "soliton_reading_guide.html",
)
KEPT = ("theory_results.html", "index.html", "Report.html", "dlw_hamilton.html")
SOURCE_OUTPUTS = {
    "Workspaces/dlw_report_formal_20261002/report.source.html": MOVED[0],
    "Workspaces/dlw_conserved_mesh_20261002/extension/report_source.html": MOVED[1],
    "Workspaces/dlw_factor_model_20260930/_src/dlw_error_theory.src.html": MOVED[2],
    "Workspaces/dlw_research_pipeline_20261001/_src/dlw_research_ideas.html": MOVED[4],
    "Workspaces/soliton_reading_20261002/guide.source.html": MOVED[6],
    "Workspaces/gsg_project/dlw_report/_src/index.src.html": "index.html",
    "Workspaces/report_notebook_20261002/report.src.html": "Report.html",
    "Workspaces/report_notebook_20261002/step_material/intro.html": "Report.html",
    "Workspaces/report_notebook_20261002/error_material/intro.html": "Report.html",
    "Workspaces/dlw_waveform_fields_20261001/waveform_fields.src.html": MOVED[5],
    "Workspaces/dlw_waveform_fields_20261001/revision_euler_crop/euler_errors.src.html": MOVED[5],
}
IMAGE_SOURCES = {
    "Workspaces/dlw_waveform_fields_20261001/waveform_fields.src.html",
    "Workspaces/dlw_waveform_fields_20261001/revision_euler_crop/euler_errors.src.html",
}
ATTR = re.compile(r'(?P<prefix>\b(?:href|src|action)\s*=\s*)(?P<quote>["\'])(?P<url>.*?)(?P=quote)', re.I)
MD_LINK = re.compile(r'(?P<prefix>\]\()(?P<url>[^\s)]+)(?P<suffix>\))')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def relocate_url(url, old_parent, new_parent):
    parts = urlsplit(unescape(url))
    if parts.scheme or parts.netloc or not parts.path or parts.path.startswith("/"):
        return url
    old_target = (old_parent / unquote(parts.path)).resolve()
    if old_target.parent == ROOT and old_target.name in MOVED:
        target = ROOT / "report" / old_target.name
    else:
        target = old_target
    path = os.path.relpath(target, new_parent).replace("\\", "/")
    if path == parts.path:
        return url
    return urlunsplit(("", "", path, parts.query, parts.fragment))


def rewrite_html(text, old_output, new_output, href_only=False):
    def replace(match):
        if href_only and not match["prefix"].lower().startswith("href"):
            return match[0]
        url = relocate_url(match["url"], old_output.parent, new_output.parent)
        return match["prefix"] + match["quote"] + url + match["quote"]
    return ATTR.sub(replace, text)


def apply():
    receipt = HERE / "migration_manifest.json"
    if receipt.exists():
        raise RuntimeError("Migration already applied; use --verify.")
    changed = []
    def save(path, text):
        before = path.read_bytes()
        after = text.encode("utf-8")
        if before != after:
            try:
                path.write_bytes(after)
            except OSError as error:
                # A preview may memory-map a file and prevent truncation on Windows.
                # Preserve that original in Trash with native PowerShell, then write
                # the revised file at the same path.
                if error.errno != 22 or path.read_bytes() != before:
                    raise
                backup = ROOT / "Trash" / "report_organization_20261004" / path.relative_to(ROOT)
                if backup.exists():
                    raise RuntimeError("Backup already exists: " + str(backup))
                def quote(value):
                    return "'" + str(value).replace("'", "''") + "'"
                command = (
                    "$ErrorActionPreference='Stop'; "
                    "$workspacePath=" + quote(ROOT) + "; "
                    "$sourcePath=[System.IO.Path]::GetFullPath(" + quote(path) + "); "
                    "$backupPath=[System.IO.Path]::GetFullPath(" + quote(backup) + "); "
                    "if (-not $sourcePath.StartsWith($workspacePath+'\\') -or "
                    "-not $backupPath.StartsWith($workspacePath+'\\Trash\\report_organization_20261004\\')) "
                    "{ throw 'Backup path outside intended workspace' }; "
                    "New-Item -ItemType Directory -Path ([System.IO.Path]::GetDirectoryName($backupPath)) -Force | Out-Null; "
                    "Move-Item -LiteralPath $sourcePath -Destination $backupPath"
                )
                subprocess.run(["powershell", "-NoProfile", "-Command", command], check=True, capture_output=True)
                path.write_bytes(after)
            changed.append({"path": path.relative_to(ROOT).as_posix(),
                            "before_sha256": digest(before), "after_sha256": digest(after)})

    for name in KEPT + MOVED:
        old = ROOT / name
        current = ROOT / "report" / name if name in MOVED else old
        if not current.exists():
            raise FileNotFoundError(current)
        text = current.read_bytes().decode("utf-8")
        save(current, rewrite_html(text, old, current))
    for source, output in SOURCE_OUTPUTS.items():
        source_path = ROOT / source
        if source_path.exists():
            old = ROOT / output
            new = ROOT / "report" / output if output in MOVED else old
            save(source_path, rewrite_html(source_path.read_bytes().decode("utf-8"), old, new, source in IMAGE_SOURCES))

    for name in ("AGENTS.md", "FILE_INDEX.md", "PROGRESS_LOG.md"):
        path = ROOT / name
        text = path.read_bytes().decode("utf-8")
        text = MD_LINK.sub(lambda m: m["prefix"] + relocate_url(m["url"], ROOT, ROOT) + m["suffix"], text)
        for report_name in MOVED:
            text = text.replace("`" + report_name + "`", "`report/" + report_name + "`")
        if name == "AGENTS.md":
            text = text.replace("├── index.html              论文式报告（生成物，1.89 MB，自包含）",
                                "├── theory_results.html / index.html / Report.html / dlw_hamilton.html   主入口\r\n├── report\\                 其余用户专题 HTML 报告")
            text = text.replace("并放在主目录下", "并放在 `report\\` 下（主目录保留 theory_results.html、index.html、Report.html、dlw_hamilton.html）")
        elif name == "FILE_INDEX.md":
            text = re.sub(r"已按当前正文核对根目录 11 个 HTML（含新增 Hamilton 报告）。", "当前用户报告共11个：主目录保留4个入口，7个专题页面位于 `report/`。", text)
            text = text.replace("## HTML 阅读地图（2026-10-04复核）", "## HTML 阅读地图（2026-10-04整理）")
            start = text.index("| 根目录页面 | 内容与用途 |")
            end = text.index("子目录中的独立专题报告：", start)
            rows = [line for line in text[start:end].splitlines() if line.startswith("| [")]
            root_rows = [line for line in rows if "](report/" not in line]
            report_rows = [line for line in rows if "](report/" in line]
            tables = "| 主目录页面 | 内容与用途 |\r\n| --- | --- |\r\n" + "\r\n".join(root_rows)
            tables += "\r\n\r\n| report 专题页面 | 内容与用途 |\r\n| --- | --- |\r\n" + "\r\n".join(report_rows) + "\r\n\r\n"
            text = text[:start] + tables + text[end:]
        else:
            match = re.search(r"(?m)^> \*\*2026-10-04（HTML 内容盘点与阅读地图）：.*?(?=\r?\n\r?\n|\Z)", text, re.S)
            if not match:
                raise RuntimeError("Existing HTML progress entry missing")
            entry = "> **2026-10-04（HTML 内容盘点与阅读地图）：** 已核对11个用户HTML。按用户要求，主目录仅保留theory_results.html、index.html、Report.html、dlw_hamilton.html，其余7页移至report/；实际页面、活动正文源、生成/检查脚本、Report服务路由与共享索引同步新路径。waveform仍是index第6节的36图摘录；Report第3章仍为DLW截断残差现场计算。根目录及report/的HTML均纳入Git，子目录模板保留既有排除策略。迁移及本地链接核验记录在Workspaces/report_organization_20261004/；未运行新数学/数值实验。"
            text = text[:match.start()] + text[match.end():]
            text = entry + "\r\n\r\n" + text.lstrip("\r\n")
        save(path, text)

    path = ROOT / ".gitignore"
    text = path.read_bytes().decode("utf-8")
    text = text.replace("# HTML 仅提交根目录用户报告；子目录页面及 HTML 模板留在本地", "# HTML 提交主目录和 report/ 用户报告；其他子目录页面及模板留在本地")
    if "!/report/*.html" not in text:
        text = text.rstrip("\r\n") + "\r\n!/report/*.html\r\n"
    save(path, text)
    receipt.write_text(json.dumps({"kept": list(KEPT), "moved": ["report/" + x for x in MOVED], "changed": changed}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"changed_files": len(changed), "root_html": len(list(ROOT.glob('*.html'))), "report_html": len(list((ROOT / 'report').glob('*.html')))}, ensure_ascii=False))


class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links = []; self.ids = set()
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ("href", "src", "action") and value: self.links.append(value)
            if key == "id" and value: self.ids.add(value)


def verify():
    pages = list(ROOT.glob("*.html")) + list((ROOT / "report").glob("*.html"))
    assert {p.name for p in ROOT.glob("*.html")} == set(KEPT)
    assert {p.name for p in (ROOT / "report").glob("*.html")} == set(MOVED)
    parsed = {}
    for page in pages:
        obj = Links(); obj.feed(page.read_text(encoding="utf-8")); parsed[page.resolve()] = obj
    missing = []; broken_fragments = []; checked = 0
    for page in pages:
        for url in parsed[page.resolve()].links:
            parts = urlsplit(url)
            if parts.scheme or parts.netloc or parts.path.startswith("/"): continue
            target = (page.parent / unquote(parts.path)).resolve() if parts.path else page.resolve()
            checked += 1
            if not target.exists():
                missing.append({"page": page.relative_to(ROOT).as_posix(), "url": url})
            elif parts.fragment and target.suffix.lower() == ".html":
                if target not in parsed:
                    obj = Links(); obj.feed(target.read_text(encoding="utf-8")); parsed[target] = obj
                if unquote(parts.fragment) not in parsed[target].ids:
                    broken_fragments.append({"page": page.relative_to(ROOT).as_posix(), "url": url})
    result = {"root_html": len(list(ROOT.glob("*.html"))), "report_html": len(list((ROOT / "report").glob("*.html"))), "local_links_checked": checked, "missing": missing, "broken_html_fragments": broken_fragments}
    (HERE / "link_validation.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))
    if missing or broken_fragments: raise SystemExit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(); parser.add_argument("--apply", action="store_true"); parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if args.apply: apply()
    if args.verify: verify()
