"""Keep source HTML byte snapshots and usable report-folder archive copies."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urlparse

from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SOURCES = {
    "Report.html": "Report_原HTML_20261006.html",
    "index.html": "DLW数值分析_原HTML_20261006.html",
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def archive() -> dict:
    records = []
    backup_dir = HERE / "before_split"
    backup_dir.mkdir(exist_ok=True)
    for name, archive_name in SOURCES.items():
        source = ROOT / name
        before = source.read_bytes()
        backup = backup_dir / name
        if backup.exists():
            assert backup.read_bytes() == before, "Original source differs from the preserved snapshot."
        else:
            backup.write_bytes(before)
        text = before.decode("utf-8")
        assert not re.search(r"<base\b", text, re.I)
        archived = re.sub(r"(<head\b[^>]*>)", r'\1\n<base href="../">', text, count=1, flags=re.I)
        # Fragment links must stay on this archive even with a root-relative base.
        archived = re.sub(
            r'\bhref=(\"|\')#([^\"\']+)\1',
            lambda match: 'href=' + match[1] + "report/" + archive_name + "#" + match[2] + match[1],
            archived,
        )
        destination = ROOT / "report" / archive_name
        destination.write_bytes(archived.encode("utf-8"))
        old_soup = BeautifulSoup(text, "html.parser")
        new_soup = BeautifulSoup(archived, "html.parser")
        assert old_soup.get_text() == new_soup.get_text().replace("\n\n", "\n", 1) or (
            old_soup.get_text().split() == new_soup.get_text().split()
        )
        assert [tag.get("src") for tag in old_soup.find_all("img")] == [
            tag.get("src") for tag in new_soup.find_all("img")
        ]
        local_links = []
        for tag in new_soup.find_all(["a", "link", "script", "img"]):
            value = tag.get("href") if tag.name in {"a", "link"} else tag.get("src")
            if not value or value.startswith(("data:", "#", "/")) or urlparse(value).scheme:
                continue
            path = ROOT / value.split("#", 1)[0].split("?", 1)[0]
            local_links.append({"reference": value, "exists": path.exists()})
        # Missing historical references are reported without silently changing them.
        assert source.read_bytes() == before
        records.append({
            "source": str(source), "source_sha256": sha(before), "backup": str(backup),
            "backup_bytes_identical": True, "archive": str(destination),
            "archive_sha256": sha(destination.read_bytes()),
            "source_unchanged": True, "text_and_image_payloads_preserved": True,
            "base_href": "../", "fragment_links_stay_on_archive": True,
            "local_references": local_links,
        })
    validation = {"success": True, "archives": records}
    (HERE / "html_archive_validation.json").write_text(
        json.dumps(validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return validation


if __name__ == "__main__":
    print(json.dumps(archive(), ensure_ascii=False, indent=2))
