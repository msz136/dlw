"""Check all code excerpts and lecture references against their notebooks."""
from pathlib import Path
import hashlib
import json
import re
from urllib.parse import urlparse

from bs4 import BeautifulSoup
import nbformat
from build_lectures import DEST, HERE, ROOT, SPECS


def verify():
    results = []
    for key, (notebook_name, _, filename) in SPECS.items():
        path = DEST / filename
        notebook_path = ROOT / "notebook" / notebook_name
        notebook = nbformat.read(notebook_path, 4)
        code = {cell.id: cell.source for cell in notebook.cells if cell.cell_type == "code"}
        soup = BeautifulSoup(path.read_text("utf-8"), "html.parser")
        excerpts = []
        for pre in soup.select("pre[data-cell]"):
            cell_id = pre["data-cell"]
            assert cell_id in code
            snippet = pre.get_text().strip("\n")
            assert snippet in code[cell_id], (filename, cell_id, snippet)
            assert len(snippet.splitlines()) <= 12, (filename, cell_id)
            excerpts.append({"cell": cell_id, "lines": len(snippet.splitlines()), "source_contiguous": True})
        visible = soup.get_text()
        covered = [cell_id for cell_id in code if cell_id in visible]
        assert set(covered) == set(code), (filename, set(code)-set(covered))
        local_links = []
        for tag in soup.find_all(["a", "img", "script", "link"]):
            value = tag.get("href") if tag.name in {"a", "link"} else tag.get("src")
            if not value or value.startswith("#") or urlparse(value).scheme:
                continue
            target = path.parent / value.split("#",1)[0]
            assert target.exists(), (filename, value)
            local_links.append(value)
        assert len(soup.find_all("h1")) == 1
        assert soup.find_all("h2")
        assert not any(img.get("src", "").startswith(("http:","https:")) for img in soup.find_all("img"))
        if key == "nonlinear":
            assert set(re.findall(r"\\tag\{(\d+)\}",path.read_text("utf-8"))) == {str(i) for i in range(1,23)}
        results.append({"lecture": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                        "notebook": str(notebook_path), "notebook_sha256": hashlib.sha256(notebook_path.read_bytes()).hexdigest(),
                        "code_cells_covered": covered, "all_code_cells_covered": True,
                        "excerpts": excerpts, "local_links_checked": local_links})
    validation = {"success": True, "reports": results,
                  "all_code_excerpts_are_contiguous_real_source": True}
    (HERE / "content_validation.json").write_text(json.dumps(validation, ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"success": True,"reports":len(results),"covered_code_cells":sum(len(r['code_cells_covered']) for r in results),"code_excerpts":sum(len(r['excerpts']) for r in results)},ensure_ascii=False))
    return validation


if __name__ == "__main__":
    verify()
