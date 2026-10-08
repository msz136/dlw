"""Register the verified runtime session repair without rewriting notebooks.

Only --register updates README and shared records. The regression kernel and
eight runtime cases must have passed, and the parent must authorize execution.
Historical registration and every existing before/ backup are preserved.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
ROOT = PROJECT.parents[1]
BEFORE = HERE / "before"
README = PROJECT / "README.md"
PROGRESS = ROOT / "PROGRESS_LOG.md"
INDEX = ROOT / "FILE_INDEX.md"
NOTEBOOK = ROOT / "notebook" / "DLW刘维尔可积性report.ipynb"
OLD_REGISTRATION = PROJECT / "registration.json"
REGISTRATION = HERE / "registration.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text("utf-8-sig"))


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def link(path: Path, description: str) -> str:
    relative = rel(path)
    return f"- [{relative}]({relative})（{description}）"


def validate_evidence() -> dict:
    kernel = read_json(HERE / "session_regression_execution_validation.json")
    behavior = read_json(HERE / "session_behavior_validation.json")
    runtime = read_json(HERE / "runtime_validation.json")
    assert kernel["success"] and kernel["sources_unchanged"]
    assert kernel["code_cell_count"] == 7 and not kernel["errors"]
    assert behavior["success"]
    assert behavior["old_error_reproduced"] == "Run the Lean library import cell first."
    assert all(behavior[name] for name in (
        "repeated_prepare_preserves_instance", "other_magic_restored",
        "current_conditions_source_compiled_twice",
        "no_hidden_library_cell_or_previous_cell_execution",
    ))
    assert runtime["success"] and runtime["original_library_unchanged"]
    cases = runtime["cases"]
    assert len(cases) == 8
    assert set(cases) == {
        "self_contained_import", "import", "original", "edited",
        "failed_proof", "repaired", "source_changed", "artifact_changed",
    }
    for name in ("self_contained_import", "import", "original", "edited", "repaired"):
        assert cases[name]["failure"] is None
    for name in ("failed_proof", "source_changed", "artifact_changed"):
        assert cases[name]["failure"] is not None
    assert sha(OLD_REGISTRATION) == sha(BEFORE / "registration.json")
    return {"kernel_seconds": kernel["elapsed_seconds"], "cases": len(cases)}


def amend_readme(text: str, evidence: dict) -> str:
    old = "日期：2026-10-07。用户交付为 `C:\\Users\\msz\\aca\\notebook\\DLW刘维尔可积性report.ipynb`，本目录同名文件是逐字相同的项目镜像。"
    new = "日期：2026-10-07。用户交付为 `C:\\Users\\msz\\aca\\notebook\\DLW刘维尔可积性report.ipynb`，本目录同名文件保存生成时的项目镜像。用户重新运行并保存后，交付文件的输出与哈希可能改变。"
    assert old in text or new in text
    text = text.replace(old, new, 1)
    text = text.replace("当前交付 SHA-256：", "此前内容交付 SHA-256（运行保存后可改变）：", 1)
    label = "## 运行器会话修复（2026-10-07）"
    if label not in text:
        addition = (
            f"{label}\n\n"
            "用户在 `%%lean conditions` 遇到 `Run the Lean library import cell first.`。"
            "原实现每次调用 `load_lean()` 都新建运行器，并把 `library_ready` 重置为 false；"
            "重新运行 Python 准备单元后，即使刚才的库导入已成功，也会被人工前置检查拦下。\n\n"
            "现在 `load_lean()` 在同一内核复用现有同类运行器，并重新注册 `%%lean`，"
            "以恢复被其他 notebook 替换的 magic。每个显示 Lean 单元均自带 `import FinalEndpoint`，"
            "在独立临时模块中只编译当前代码；取消 `library_ready` 的人工拦截，不执行任何前段单元。"
            "每次编译前后仍检查完整 105 模块库的源文件、编译产物及 Lean/Mathlib 身份哈希，"
            "失败证明继续报错，源码或产物变更继续拒绝复用。\n\n"
            f"真实内核回归为 {evidence['kernel_seconds']} 秒，重现旧版报错后，"
            "验证了补丁重载、重复准备、跨 notebook magic 恢复及 conditions 两次独立编译；"
            f"运行器 {evidence['cases']} 个用例通过，包括输入编辑、失败恢复和隔离库变更检查。"
            "原库、Notebook 正文及代码未由本次登记修改；当前交付哈希只作用户文件快照，"
            "不要求与此前保存输出时相同。证据与旧版备份见 `session_fix/`；"
            "历史 `registration.json` 保留，本轮登记为 `session_fix/registration.json`。\n\n"
            "**应用修复：** 在当前 notebook 中重启内核，再执行首个 Python 准备单元，"
            "之后按正文顺序运行 Lean 单元。已打开的 Python 内核缓存了旧版导入，"
            "仅修改本地 `.py` 或重跑 `from integrability_runtime import load_lean` 不会自动更新旧实现。\n\n"
        )
        assert "## 生成与登记" in text
        text = text.replace("## 生成与登记", addition + "## 生成与登记", 1)
    return text


def amend_progress(text: str, evidence: dict) -> str:
    label = "> **Notebook 展示（2026-10-07）：** "
    addition = (
        "**运行器会话修复：** 重新准备会新建运行器、重置 library_ready，"
        "导致已导入库后 conditions 单元仍报前置错误；现改为 load_lean 幂等复用并恢复 magic，"
        "每段自带 import，在核验 105 模块源／产物哈希后只编译当前显示代码，"
        "取消无必要的库单元运行状态拦截。"
        f"真实内核回归 {evidence['kernel_seconds']} 秒及 8 个运行器用例通过，"
        "覆盖旧错重现、重复准备、magic 覆盖、真实编译、失败恢复与隔离库变更。"
        "当前已开内核需重启以载入修改后的 Python 模块。"
        "Notebook 内容与证明源未由本轮修复修改，历史登记保留；"
        "证据见 [session_fix](Workspaces/integrability_notebook_20261007/session_fix/registration.json)。 "
        "**此前展示：** "
    )
    assert text.count(label) == 1
    if "**运行器会话修复：**" not in text:
        text = text.replace(label, label + addition, 1)
    return text


def amend_index(text: str) -> str:
    begin = "<!-- INTEGRABILITY_NOTEBOOK_INDEX_BEGIN -->"
    end = "<!-- INTEGRABILITY_NOTEBOOK_INDEX_END -->"
    own_begin = "<!-- INTEGRABILITY_SESSION_FIX_INDEX_BEGIN -->"
    own_end = "<!-- INTEGRABILITY_SESSION_FIX_INDEX_END -->"
    assert text.count(begin) == text.count(end) == 1
    if own_begin in text:
        return text
    rows = [own_begin, "**运行器会话修复与真实内核回归（2026-10-07）：**", ""]
    for path in sorted(HERE.rglob("*"), key=lambda p: rel(p)):
        if not path.is_file() or "before" in path.relative_to(HERE).parts:
            continue
        if path.suffix not in {".py", ".json", ".ipynb"} or path.name == "registration.json":
            continue
        if "execution_inputs" in path.relative_to(HERE).parts:
            description = "真实回归执行前的原始 notebook 输入"
        elif path.suffix == ".py":
            description = "旧错重现、修复回归或保留历史登记的脚本"
        elif path.suffix == ".ipynb":
            description = "旧运行器重置、补丁重载和 magic 恢复的真实内核回归本"
        else:
            description = "本轮真实执行、会话行为或八用例核验结果"
        rows.append(link(path, description))
    rows.append(link(REGISTRATION, "本轮文件快照、记录改动前后与历史登记保留证据"))
    rows.append(
        "- `Workspaces/integrability_notebook_20261007/session_fix/before/`"
        "（运行器、验证器、README、根记录、原核验与历史登记修改前原件，保留不覆盖）"
    )
    rows.extend([own_end, ""])
    return text.replace(end, "\n".join(rows) + "\n" + end, 1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--register", action="store_true")
    args = parser.parse_args()
    if not args.register:
        print("Prepared only; no README or shared record changes. Wait for parent PASS confirmation.")
        return
    evidence = validate_evidence()
    paths = (README, PROGRESS, INDEX)
    before_current = {rel(path): sha(path) for path in paths}
    historical_registration_sha = sha(OLD_REGISTRATION)
    updates = (
        (README, amend_readme(README.read_text("utf-8"), evidence)),
        (PROGRESS, amend_progress(PROGRESS.read_text("utf-8"), evidence)),
        (INDEX, amend_index(INDEX.read_text("utf-8"))),
    )
    for path, text in updates:
        path.write_bytes(text.encode("utf-8"))
    assert sha(OLD_REGISTRATION) == historical_registration_sha
    current = [PROJECT / "integrability_runtime.py", PROJECT / "validate_runtime.py", *paths]
    current.extend(path for path in HERE.rglob("*") if path.is_file()
                   and "before" not in path.relative_to(HERE).parts
                   and path != REGISTRATION and path.suffix in {".py", ".json", ".ipynb"})
    registration = {
        "status": "PASSED", "date": "2026-10-07", "task": "integrability_notebook_session_fix",
        "current_files": [{"path": rel(path), "sha256": sha(path)} for path in sorted(set(current))],
        "records_before_current_sha256": before_current,
        "records_after_sha256": {rel(path): sha(path) for path in paths},
        "initial_backups": [{"path": rel(path), "sha256": sha(path)} for path in sorted(BEFORE.iterdir()) if path.is_file()],
        "historical_registration": {"path": rel(OLD_REGISTRATION), "sha256": historical_registration_sha, "preserved": True},
        "notebook_current_snapshot": {"path": rel(NOTEBOOK), "sha256": sha(NOTEBOOK), "written_by_this_registration": False,
                                      "note": "Current user file; saved outputs may differ from historical delivery."},
        "regression": evidence,
        "scope": "Runtime and validation repair; no proof or notebook edits by this registration.",
    }
    REGISTRATION.write_text(json.dumps(registration, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASSED", "records_updated": len(paths), "registered_files": len(current),
                      "registration": str(REGISTRATION)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
