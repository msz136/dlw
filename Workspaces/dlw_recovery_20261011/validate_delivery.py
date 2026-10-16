"""Validate saved provenance, links, syntax and preservation, without reruns."""
import ast
import hashlib
import json
import re
import subprocess
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RESEARCH = ROOT / "刘维尔可积性/research"
REPORT = ROOT / "report/dlw_liouville_recovery_20261011.html"
M2_REPORT = ROOT / "report/dlw_m2_conditional_theorem_20261011.html"
M2_REGULAR_REPORT = ROOT / "report/dlw_m2_regular_liouville_20261011.html"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def remove_block(text, start, end):
    assert text.count(start) == text.count(end) == 1
    a, b = text.index(start), text.index(end) + len(end)
    return text[:a] + text[b:], text[a:b]


def resolve_link(path, link):
    if re.match(r"^(?:https?:|mailto:|skill:|app:|#)", link):
        return None
    target = unquote(link.split("#", 1)[0].split("?", 1)[0])
    if not target:
        return None
    if target.startswith("/C:/"):
        return Path(target[1:])
    if target.startswith("C:/"):
        return Path(target)
    return (path.parent / target).resolve()


class ReportParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []
        self.tags = []

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        for key, value in attrs:
            if key == "href":
                self.hrefs.append(value)


if __name__ == "__main__":
    results = {}
    manifest = json.loads((HERE / "recovered_manifest.json").read_text(encoding="utf-8"))
    unchanged = []
    for entry in manifest:
        if entry["file"] == "STATE.md":
            before = HERE / "before/刘维尔可积性__research__STATE.md"
            assert sha(before) == entry["sha256"]
            continue
        path = RESEARCH / entry["file"]
        assert sha(path) == entry["sha256"], path
        unchanged.append(entry["file"])
    results["recovered_original_files_unchanged"] = unchanged

    certificates = []
    for directory in (RESEARCH, HERE):
        for path in sorted(directory.glob("*.json")):
            if path.name == "delivery_validation.json":
                continue
            data = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(data, dict) or "script_sha256" not in data:
                continue
            script = path.with_suffix(".py")
            aliases = {
                "scalar_monodromy_linearization_checks": "verify_scalar_monodromy_linearization.py",
                "zero_mean_branch_checks": "verify_zero_mean_branch.py",
                "unfixed_flux_checks": "verify_unfixed_flux.py",
                "mixed_hierarchy_symbol_checks": "verify_mixed_hierarchy_symbols.py",
            }
            if path.stem in aliases:
                script = directory / aliases[path.stem]
            assert script.exists(), script
            assert sha(script) == data["script_sha256"], path
            certificates.append({
                "record": path.relative_to(ROOT).as_posix(),
                "script": script.relative_to(ROOT).as_posix(),
                "sha256": sha(script),
                "status": data.get("status", data.get("purpose", "record read")),
            })
    results["certificate_provenance"] = certificates

    parsed = []
    for path in sorted(HERE.glob("*.py")):
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        parsed.append(path.relative_to(ROOT).as_posix())
    results["python_syntax"] = parsed

    markdown = [ROOT / "刘维尔可积性/README.md", ROOT / "刘维尔可积性/GOAL.md", ROOT / "刘维尔可积性/research_checkpoint.md", RESEARCH / "STATE.md"]
    markdown += sorted(RESEARCH.glob("*20261011.md"))
    markdown += sorted(HERE.glob("*.md"))
    count = 0
    for path in markdown:
        content = path.read_text(encoding="utf-8")
        assert "\ufffd" not in content, path
        for link in re.findall(r"(?<!\\)\[[^\]\n]*\]\(([^\s)]+)\)", content):
            target = resolve_link(path, link)
            if target is not None:
                # Mathematical expressions [F](t) are not document links.
                if not re.search(r"[./\\]", link) and not target.exists():
                    continue
                assert target.exists(), (path, link, target)
                count += 1
        assert content.count("$$") % 2 == 0, path
        assert content.count(r"\[") == content.count(r"\]"), path
    results["markdown_local_links"] = count
    results["markdown_utf8_and_display_delimiters"] = len(markdown)
    results["saved_manuscript_snapshot"] = [
        {"path": path.relative_to(ROOT).as_posix(), "sha256": sha(path)}
        for path in sorted(set(markdown))
    ]

    parser = ReportParser()
    content = REPORT.read_text(encoding="utf-8")
    parser.feed(content)
    assert "\ufffd" not in content and '<meta charset="utf-8">' in content
    assert parser.tags.count("main") == parser.tags.count("h1") == 1
    assert "script" not in parser.tags
    for link in parser.hrefs:
        target = resolve_link(REPORT, link)
        if target:
            assert target.exists(), (REPORT, link)
    results["html"] = {"sha256": sha(REPORT), "local_links": len(parser.hrefs), "sections": parser.tags.count("h2"), "offline": True}

    m2_parser = ReportParser()
    m2_content = M2_REPORT.read_text(encoding="utf-8")
    m2_parser.feed(m2_content)
    assert "\ufffd" not in m2_content and '<meta charset="utf-8">' in m2_content
    assert m2_parser.tags.count("main") == m2_parser.tags.count("h1") == 1
    assert "script" not in m2_parser.tags
    for link in m2_parser.hrefs:
        target = resolve_link(M2_REPORT, link)
        if target:
            assert target.exists(), (M2_REPORT, link)
    results["m2_conditional_theorem_html"] = {"sha256": sha(M2_REPORT), "local_links": len(m2_parser.hrefs), "sections": m2_parser.tags.count("h2"), "offline": True}

    regular_parser = ReportParser()
    regular_content = M2_REGULAR_REPORT.read_text(encoding="utf-8")
    regular_parser.feed(regular_content)
    assert "\ufffd" not in regular_content and '<meta charset="utf-8">' in regular_content
    assert regular_parser.tags.count("main") == regular_parser.tags.count("h1") == 1
    assert "script" not in regular_parser.tags
    for link in regular_parser.hrefs:
        target = resolve_link(M2_REGULAR_REPORT, link)
        if target:
            assert target.exists(), (M2_REGULAR_REPORT, link)
    results["m2_regular_original_liouville_html"] = {"sha256": sha(M2_REGULAR_REPORT), "local_links": len(regular_parser.hrefs), "sections": regular_parser.tags.count("h2"), "offline": True}

    old_progress = (HERE / "before/PROGRESS_LOG.md").read_text(encoding="utf-8")
    new_progress = (ROOT / "PROGRESS_LOG.md").read_text(encoding="utf-8")
    marker_a, marker_b = "<!-- DLW_HAMILTON_BEGIN -->", "<!-- DLW_HAMILTON_END -->"
    old_other, old_topic = remove_block(old_progress, marker_a, marker_b)
    new_other, new_topic = remove_block(new_progress, marker_a, marker_b)
    assert old_other.strip() == new_other.strip(), "Unrelated progress changed"
    old_body = old_topic[len(marker_a):-len(marker_b)].strip()
    assert old_body in new_topic, "Old same-topic progress not preserved"
    old_index = (HERE / "before/FILE_INDEX.md").read_text(encoding="utf-8")
    new_index = (ROOT / "FILE_INDEX.md").read_text(encoding="utf-8")
    index_other, _ = remove_block(new_index, "<!-- DLW_LIOUVILLE_RECOVERY_INDEX_BEGIN -->", "<!-- DLW_LIOUVILLE_RECOVERY_INDEX_END -->")
    assert old_index.strip() == index_other.strip(), "Unrelated index changed"
    results["unrelated_shared_content_preserved"] = {"progress": True, "index": True, "topic_history": True}

    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    assert head == "e2ee3cc6a022c0afc723e3324b3cc57a0fa5b143", head
    diff = subprocess.run(["git", "diff", "--check", "--", "刘维尔可积性/README.md", "PROGRESS_LOG.md", "FILE_INDEX.md"], cwd=ROOT, capture_output=True, text=True)
    assert diff.returncode == 0, diff.stdout + diff.stderr
    results["git"] = {"head": head, "scoped_diff_check": True, "commit_or_push_performed": False}
    results["status"] = "all delivery checks passed"
    results["scope"] = "Saved artifacts and provenance only; not a certification of a complete nonlinear Liouville theorem."
    results["script_sha256"] = sha(Path(__file__))
    (HERE / "delivery_validation.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"PASS: {len(certificates)} certificate hashes, {len(parsed)} Python sources, {count} Markdown links, {len(parser.hrefs) + len(m2_parser.hrefs) + len(regular_parser.hrefs)} HTML links across three reports, preserved shared history.")
