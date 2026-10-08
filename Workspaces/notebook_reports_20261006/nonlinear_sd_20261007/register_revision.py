"""Register the validated nonlinear SD revision within the existing DLW topic.

Reads final native-kernel and static-report evidence before touching shared
records. Root records are copied first; historical numerical manifests remain
unchanged. Repeated registration replaces this revision's marked snippets.
"""
from pathlib import Path
import hashlib
import json
import re
import shutil

import nbformat


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
ROOT = PROJECT.parents[1]
STATIC = ROOT / "Workspaces/dlw_notebook_static_20261007"
BEFORE = PROJECT / "before_nonlinear_sd_20261007"
NOTEBOOK = ROOT / "notebook/DLW数值分析report.ipynb"
HTML = ROOT / "dlw_numerical.html"
TAU_ARCHIVE = ROOT / "report/DLW数值分析_双线性SD留档_20261007.html"
PROGRESS_BEGIN = "<!-- DLW_NONLINEAR_SD_PROGRESS_BEGIN -->"
PROGRESS_END = "<!-- DLW_NONLINEAR_SD_PROGRESS_END -->"
INDEX_BEGIN = "<!-- DLW_NONLINEAR_SD_INDEX_BEGIN -->"
INDEX_END = "<!-- DLW_NONLINEAR_SD_INDEX_END -->"


def read_json(path):
    return json.loads(path.read_text("utf-8"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path):
    return path.relative_to(ROOT).as_posix()


def save_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def marked_replace(text, begin, end, replacement):
    assert text.count(begin) == text.count(end) == 1
    return re.sub(re.escape(begin) + r".*?" + re.escape(end),
                  lambda _: replacement, text, count=1, flags=re.S)


def validated_inputs():
    results = read_json(PROJECT / "dlw_numeric_results.json")
    execution = read_json(PROJECT / "dlw_execution_validation.json")
    build = read_json(PROJECT / "dlw_build_validation.json")
    kernel = read_json(HERE / "kernel_validation.json")
    spatial = read_json(HERE / "spatial_validation.json")
    delivery = read_json(HERE / "delivery_validation.json")
    static_build = read_json(STATIC / "build_validation.json")
    content = read_json(STATIC / "content_validation.json")
    browser = read_json(STATIC / "browser_validation.json")
    assert execution["success"] and delivery["success"] and spatial["success"]
    assert kernel["all_passed"] and static_build["success"] and content["success"]
    assert browser["success"] and browser["offline"] and browser["javaScriptDisabled"]
    assert execution["notebook_sha256"] == delivery["notebook_sha256"] == sha(NOTEBOOK)
    assert execution["exported_results_sha256"] == delivery["exported_results_sha256"] == sha(PROJECT / "dlw_numeric_results.json")
    assert execution["exported_curves_sha256"] == delivery["exported_curves_sha256"] == sha(PROJECT / "dlw_numeric_curves.npz")
    assert static_build["source_sha256"] == content["notebook_sha256"] == sha(NOTEBOOK)
    assert static_build["delivery_sha256"] == content["html_sha256"] == sha(HTML)
    assert content["no_code_elements_or_implementation_prose"]
    assert static_build["visible_code_excerpts"] == static_build["visible_code_lines"] == 0
    assert not static_build["full_sources_included"] and not static_build["table_of_contents"]
    assert execution["independent_native_kernel"] and execution["outputs_saved"]
    assert execution["sources_unchanged"] and execution["executed_cells"] == execution["code_cells"]
    assert len(results["rows"]) == build["primary_runs"] == delivery["primary_runs"] == 36
    assert len(results["refinement_rows"]) == build["time_order_additional_runs"] == delivery["temporal_refinement_runs"] == 12
    assert all(row["completed"] and abs(row["reached"] - build["configuration"]["T"]) < 1e-13
               for row in results["rows"] + results["refinement_rows"])
    for layout in ("desktop", "mobile", "print"):
        record = browser[layout]
        assert record["sections"] == 7 and record["tables"] == 5
        assert record["codeElements"] == record["code"] == 0
        assert len(record["images"]) == 3 and all(item["loaded"] for item in record["images"])
        for table in record["tableRules"]:
            assert table["top"] and table["headerBottom"] and table["bottom"]
            assert table["sideBorders"] == table["headerOtherBorders"] == table["interiorBorders"] == 0

    notebook = nbformat.read(NOTEBOOK, as_version=4)
    sources = {cell.id: hashlib.sha256(cell.source.encode()).hexdigest() for cell in notebook.cells}
    assert sources == results["source_hashes"] == execution["source_hashes"]
    for name, value in delivery["source_modules_sha256"].items():
        assert sha(PROJECT / name) == value, name + " changed after delivery verification"
    assert sha(PROJECT / "sd_nonlinear_cell.py") == kernel["source_sha256"]
    previous = nbformat.read(BEFORE / "notebook/DLW数值分析report.ipynb", as_version=4)
    current_exact = next(cell.source for cell in notebook.cells if cell.id == "dlw-exact-text")
    previous_exact = next(cell.source for cell in previous.cells if cell.id == "dlw-exact-text")
    assert current_exact == previous_exact
    return dict(results=results, execution=execution, build=build, kernel=kernel,
                spatial=spatial, delivery=delivery, static_build=static_build,
                content=content, browser=browser, exact_prose_preserved=True)


def progress_note(data):
    execution, delivery = data["execution"], data["delivery"]
    orders = delivery["euler_order_ranges"]
    independent_error = max(row["omega_form_relative_error"]
                            for row in data["kernel"]["comparisons"])
    return ("**非线性 SD 重算（2026-10-07）：** SD 改为第一种非线性半离散方程，"
        "以 P=δ₋u、W=4ω/h=v−δ₀u 推进，并由下边界恢复 u、v；保留三点二阶 D₁ 与直接 D₂。"
        "SD、SD2、FD 共同比较 Euler/RK4 及固定/动网格，空间与网格表统一 RK4，局部误差曲线统一 Euler。"
        f"{execution['code_cells']} 个代码单元在新本地内核完整执行 {execution['seconds']:.3f} 秒，"
        f"{delivery['primary_runs']} 组主试验与 {delivery['temporal_refinement_runs']} 组时间细化均到达 T=0.01；"
        f"SD / SD2 的 Euler 时间观测阶分别为 {orders['SD'][0]:.3f}–{orders['SD'][1]:.3f} / "
        f"{orders['SD2'][0]:.3f}–{orders['SD2'][1]:.3f}。"
        f"独立 ω 形式与演化右端相对差最大 {independent_error:.2e}，"
        f"初始物理场节点差最大 {delivery['initial_maximum_evaluation_node_error']:.2e}；"
        "制造解的固定/动网格空间阶约 2，SD2/FD 保留组合的表值及曲线逐值一致。"
        "用户精确解表述保持，Notebook 保存全部新输出；HTML 仅保留数学叙述、五张三线表与三张新图，"
        "七节、无目录、代码、参考资料或完整实现附录，离线桌面/390px/打印及字体检查通过。"
        "源码、运行记录、源/输出哈希和交付核验见 "
        "[非线性重算登记](Workspaces/notebook_reports_20261006/nonlinear_sd_20261007/revision_manifest.json)，"
        "重算前 τ 版及用户编辑留存 before_nonlinear_sd_20261007。本轮未提交、未推送。")


def index_block():
    paths = {
        NOTEBOOK: "可逐段运行的自包含数值 Notebook，保存非线性 SD 新输出",
        HTML: "无代码数学报告：非线性递推、五张三线表、三张误差图",
        TAU_ARCHIVE: "改回非线性 SD 前的双线性 τ 数值报告留档",
        PROJECT / "sd_nonlinear_cell.py": "当前 SD 核心：P/W 初值、物理场恢复与非线性右端",
        PROJECT / "dlw_numeric_cells.py": "当前全部可执行单元与共享 Euler/RK4 实验流程",
        PROJECT / "build_dlw_numerics_notebook.py": "Notebook 权威生成器与实验配置登记",
        PROJECT / "revise_dlw_structure.py": "空间方案的数学正文与单元编排",
        PROJECT / "execute_dlw_notebook.py": "新内核执行、真实输出与 JSON/NPZ 导出",
        PROJECT / "dlw_build_validation.json": "当前生成配置与 36+12 组实验计数",
        PROJECT / "dlw_execution_validation.json": "本轮原生执行时长、源哈希与导出哈希",
        PROJECT / "dlw_numeric_results.json": "36 主试验及 12 时间细化的实际误差",
        PROJECT / "dlw_numeric_curves.npz": "全部主试验的公共点误差曲线",
        HERE / "verify_nonlinear_sd_kernel.py": "独立 ω/P/W 方程、边界恢复与 ALE 核验",
        HERE / "kernel_validation.json": "非线性核心独立核验证据",
        HERE / "verify_nonlinear_delivery.py": "三点空间阶与完整 Notebook/JSON/NPZ 交付核验",
        HERE / "spatial_validation.json": "固定/动网格制造解及直接 D₂ 证据",
        HERE / "delivery_validation.json": "36+12 组结果、源哈希、原始表图及保留方法对照",
        HERE / "register_revision.py": "合并当前 DLW 专题进度与索引",
        HERE / "revision_manifest.json": "本轮最终交付、数学检查与全部文件哈希",
        HERE / "record_snippets.json": "本轮登记的专题正文与索引片段",
        HERE / "before_registration": "共享进度与索引修改前的最新原件",
        BEFORE: "改回非线性格式前 τ 方案、Notebook/HTML、数据及用户精确解原件",
        STATIC / "build_static.py": "无代码 HTML 权威生成器",
        STATIC / "build_validation.json": "当前 HTML/Notebook 对应与哈希",
        STATIC / "content_validation.json": "当前数学正文及保存表图逐项比对",
        STATIC / "browser_validation.json": "当前离线桌面、390px、打印、三线表及字体证据",
    }
    body = [INDEX_BEGIN, "**当前非线性 SD 重算（2026-10-07）：**", ""]
    body.extend(f"- [{relative(path)}]({relative(path)})（{description}）"
                for path, description in paths.items())
    body.append(INDEX_END)
    return "\n".join(body)


def revise_index(text, block):
    if INDEX_BEGIN in text:
        text = marked_replace(text, INDEX_BEGIN, INDEX_END, block)
    else:
        marker = "<!-- DLW_GSG_SECOND_ORDER_INDEX_BEGIN -->"
        title = "**DLW 三点二阶空间差分（2026-10-07）：**"
        assert marker in text and title in text
        replacement = ("**DLW 三点二阶空间差分与数值更新：**\n\n" + block +
                       "\n\n**GSG 三点二阶对齐的历史记录（τ 方案，2026-10-07）：**")
        text = text.replace(title, replacement, 1)
    # Update active entry-point descriptions, retaining all historic paths.
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("| [dlw_numerical.html](dlw_numerical.html) |"):
            lines[i] = ("| [dlw_numerical.html](dlw_numerical.html) | 当前 DLW Notebook 的无代码静态报告："
                "宋体论文正文、数学公式、第一种非线性 SD 递推及新保存表图；第1—7节、五张三线表、三张误差图，"
                "无目录与附录。双击离线打开或直接发送此文件。可运行原件为 "
                "[DLW数值分析report.ipynb](notebook/DLW数值分析report.ipynb)。 |")
        elif line.startswith("- [dlw_numerical.html](dlw_numerical.html)（") and (
                "直接双线性SD" in line or "关键代码6段" in line or "当前 DLW notebook" in line):
            lines[i] = ("- [dlw_numerical.html](dlw_numerical.html)（当前 DLW Notebook 的无代码数学报告；"
                "第一种非线性 SD 的 P/W 递推、共享 Euler/RK4、五张三线表及三张新误差图；"
                "第1—7节，无目录、参考资料和代码附录，原 HTML 留档保持）")
        elif line.startswith("- [notebook/DLW数值分析report.ipynb](notebook/DLW数值分析report.ipynb)") and "本轮字节保持" in line:
            lines[i] = ("- [notebook/DLW数值分析report.ipynb](notebook/DLW数值分析report.ipynb)"
                "（报告来源；非线性 SD、SD2 与 FD 的逐段可运行代码及本轮真实输出）")
        elif line.startswith("- [Workspaces/dlw_notebook_static_20261007/verify_static.py]"):
            lines[i] = ("- [Workspaces/dlw_notebook_static_20261007/verify_static.py]"
                "(Workspaces/dlw_notebook_static_20261007/verify_static.py)（无代码数学正文、公式与保存表图核验）")
        elif line == "**DLW 主报告直接双线性 τ 更新（2026-10-07）：**":
            lines[i] = "**DLW 主报告直接双线性 τ 更新的历史记录（2026-10-07）：**"
    return "\n".join(lines) + "\n"


def main():
    data = validated_inputs()
    progress_path, index_path = ROOT / "PROGRESS_LOG.md", ROOT / "FILE_INDEX.md"
    original_progress = progress_path.read_text("utf-8")
    original_index = index_path.read_text("utf-8")
    note = progress_note(data)
    marked_note = PROGRESS_BEGIN + note + PROGRESS_END
    if PROGRESS_BEGIN in original_progress:
        progress = marked_replace(original_progress, PROGRESS_BEGIN, PROGRESS_END, marked_note)
    else:
        marker = "> **2026-10-06（DLW数值分析笔记本）：** "
        assert original_progress.count(marker) == 1
        progress = original_progress.replace(marker, marker + marked_note + " **此前记录：** ", 1)
    block = index_block()
    index = revise_index(original_index, block)

    before = HERE / "before_registration"
    before.mkdir(exist_ok=True)
    for path in (progress_path, index_path):
        target = before / path.name
        if not target.exists():
            shutil.copy2(path, target)

    artifacts = [NOTEBOOK, HTML, TAU_ARCHIVE, *(PROJECT / name for name in data["delivery"]["source_modules_sha256"]),
        PROJECT / "dlw_build_validation.json", PROJECT / "dlw_numeric_results.json",
        PROJECT / "dlw_numeric_curves.npz", PROJECT / "dlw_execution_validation.json",
        HERE / "verify_nonlinear_sd_kernel.py", HERE / "verify_nonlinear_delivery.py",
        HERE / "kernel_validation.json", HERE / "spatial_validation.json", HERE / "delivery_validation.json",
        HERE / "register_revision.py", STATIC / "build_static.py", STATIC / "verify_static.py",
        STATIC / "check_static.cjs", STATIC / "build_validation.json",
        STATIC / "content_validation.json", STATIC / "browser_validation.json"]
    artifacts += list(HERE.glob("dlw_notebook_figure_*.png")) + list(STATIC.glob("report_*.png"))
    record = dict(date="2026-10-07", success=True, sd_formulation="Report (7), nonlinear u/omega; P=delta_-u, W=4omega/h",
        configuration=data["build"]["configuration"], spatial_order=2,
        time_methods={model: ["Euler", "RK4"] for model in ("SD", "SD2", "FD")},
        spatial_and_mesh_tables="RK4", local_error_curves="Euler",
        primary_runs=data["delivery"]["primary_runs"],
        temporal_refinement_runs=data["delivery"]["temporal_refinement_runs"],
        code_cells=data["execution"]["code_cells"], executed_cells=data["execution"]["executed_cells"],
        execution_seconds=data["execution"]["seconds"], image_outputs=data["execution"]["image_outputs"],
        euler_order_ranges=data["delivery"]["euler_order_ranges"],
        initial_maximum_evaluation_node_error=data["delivery"]["initial_maximum_evaluation_node_error"],
        unchanged_SD2_FD_runs=len(data["delivery"]["unchanged_SD2_FD_runs"]),
        exact_prose_preserved=data["exact_prose_preserved"],
        presentation=dict(sections=7, tables=5, figures=3, code=False, table_of_contents=False,
            math_expressions=data["static_build"]["math_expressions"],
            font_style=data["static_build"]["font_style"], offline=True),
        no_commit=True, no_push=True, backup=relative(BEFORE),
        source_modules_sha256=data["delivery"]["source_modules_sha256"],
        file_hashes={relative(path): sha(path) for path in dict.fromkeys(artifacts)},
        previous_record_hashes={relative(path): sha(before / path.name) for path in (progress_path, index_path)})
    save_json(HERE / "revision_manifest.json", record)
    progress_path.write_text(progress, encoding="utf-8")
    index_path.write_text(index, encoding="utf-8")
    save_json(HERE / "record_snippets.json", dict(progress_note=note, index_block=block,
        final_record_hashes={relative(path): sha(path) for path in (progress_path, index_path)}))
    print(json.dumps(dict(success=True, primary_runs=record["primary_runs"],
        temporal_refinement_runs=record["temporal_refinement_runs"],
        execution_seconds=record["execution_seconds"], exact_prose_preserved=True,
        notebook_sha256=sha(NOTEBOOK), html_sha256=sha(HTML)), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
