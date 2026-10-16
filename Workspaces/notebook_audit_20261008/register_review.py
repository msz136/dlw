from pathlib import Path
import hashlib
import json
import re
import shutil
import uuid

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
summary = json.loads((OUT/'summary.json').read_text(encoding='utf-8'))
backups = OUT / ('registration_before_20261009_' + uuid.uuid4().hex[:8])
backups.mkdir()

def update(path, begin, end, body):
    raw = path.read_bytes()
    shutil.copy2(path, backups/path.name)
    bom = raw.startswith(b'\xef\xbb\xbf')
    text = raw.decode('utf-8-sig')
    newline = '\r\n' if '\r\n' in text else '\n'
    block = (begin+'\n'+body.strip()+'\n'+end+'\n\n').replace('\n',newline)
    if begin in text:
        pattern = re.escape(begin)+r'.*?'+re.escape(end)+r'(?:\r?\n){0,2}'
        text, count = re.subn(pattern,block,text,count=1,flags=re.S)
        assert count==1
    else:
        text = block+text
    encoded = text.encode('utf-8')
    path.write_bytes((b'\xef\xbb\xbf' if bom else b'')+encoded)

update(ROOT/'PROGRESS_LOG.md', '<!-- NOTEBOOK_AUDIT_PROGRESS_BEGIN -->', '<!-- NOTEBOOK_AUDIT_PROGRESS_END -->',
''' > **2026-10-09：Notebook 专项审查（2026-10-08 开始，含并行新增 C–N 的补审）**：仅审查 `notebook/2HS数值分析report.ipynb`、`DLW数值分析report.ipynb`、`DLW理论.ipynb` 共 102 单元／53 代码单元；刘维尔可积性排除。完成 [审查报告](report/notebook_review_20261009.html)。四项 P2：DLW 缓存遗漏配置／谱参数且默认配置对象旧绑定；2HS 局部重运行的单／二孤子状态污染与误标；SD2 Euler 终步未验收 Q 正性（非默认 dt=T=2 反例，当前默认未触发，C–N 残差计算会检查候选 Q）；新增 C–N 的固定残差容差污染时间细化阶。另记录六项 P3：实对数正域、辅助层 LayerOK 文字覆盖、jet 颜色旧叙述、100 段误差旧叙述、T=0 绘图失败、C–N 增加后保存总试验数仍为27。原27组及新增9组 C–N 主试验全部复现，新版四张表共126值匹配；新增720步残差均在设定容差内。C算例 C–N 默认细化观测阶不稳定，仅缩紧容差1000倍后六场恢复1.9986..2.0001；当前细步是一次Picard校正的Heun近似，不是直接Euler，更小步长标量例确会早停接受Euler。宽域三算例独立回算；2HS 两案例两方法默认误差表复现，Integrable 空间细化 N=300..4800 约一阶，时间减半确认尾误差空间主导，默认 [-5,5] Eu 单／二约 .09356／.27944。SD 正增长高频模态属方法局限，不判符号 bug。理论161项精确检查通过，13 Lean 单元起点／终点与已有编译对应，任意 N 精确性／正则性／紧集二阶证明前提链审读完成；未重编译 Lean。审查自身未改 Notebook；2HS/理论原哈希保持，DLW 并行新增C–N的初始与补审哈希均登记，当前与最终审查版本一致。HTML 桌面／390px／打印与本地链接核验通过，独立终审已落实端点界仅为 T=.01 解析尾部的范围澄清。脚本、逐项记录与 JSON 证据在 `Workspaces/notebook_audit_20261008/`。''')

update(ROOT/'FILE_INDEX.md', '<!-- NOTEBOOK_AUDIT_INDEX_BEGIN -->', '<!-- NOTEBOOK_AUDIT_INDEX_END -->',
'''**Notebook 专项审查（2026-10-08—09）：**

- [report/notebook_review_20261009.html](report/notebook_review_20261009.html)：用户阅读报告，四项 P2、六项 P3、数值精度与理论／边界审查，包含并行新增 C–N 的补审。
- [Workspaces/notebook_audit_20261008/summary.json](Workspaces/notebook_audit_20261008/summary.json)：范围、发现定位、计数与原 Notebook 哈希检查汇总。
- [Workspaces/notebook_audit_20261008/inventory.json](Workspaces/notebook_audit_20261008/inventory.json)：三份 Notebook 原始哈希、逐单元与保存输出索引。
- [Workspaces/notebook_audit_20261008/extract_notebooks.py](Workspaces/notebook_audit_20261008/extract_notebooks.py)：抽取本次范围内的正文、代码、表和 18 张保存图；`extracted/` 为单元快照。
- [Workspaces/notebook_audit_20261008/2hs/findings.md](Workspaces/notebook_audit_20261008/2hs/findings.md)：2HS 逐项审查；同目录 `audit_checks.py`、`additional_checks.py`、`evidence.json` 为独立复现脚本及数值证据，`source.txt` 为源码快照。
- [Workspaces/notebook_audit_20261008/dlw/findings.md](Workspaces/notebook_audit_20261008/dlw/findings.md)：DLW 数值逐项审查；`audit_dlw.py`、`numerical_checks.json` 为默认 27 组及边界／算法复核，`final_state_guard_check.py`、`final_state_guard.json` 为终步反例，`align_saved_ratio_table.py` 为保存表标签排序对齐，`notebook_source_numbered.txt` 为定位快照。
- `Workspaces/notebook_audit_20261008/dlw/cn_revision/`：新增 C–N 的 Notebook 快照、`cn_evidence.json`（默认9组及新表54值）、`cn_tolerance_evidence.json`、`cn_tolerance_pure_evidence.json`（纯缩紧容差配对）、可复跑补审脚本和补审发现。`concurrent_revision/` 为主审查检测并行更新时冻结的同版本快照。
- [Workspaces/notebook_audit_20261008/theory/findings.md](Workspaces/notebook_audit_20261008/theory/findings.md)：理论前提与形式化覆盖表；`verify_theory.py`、`evidence.json` 为 161 项精确检查及直接证明链对应。
- [Workspaces/notebook_audit_20261008/audit_plot_and_cache.py](Workspaces/notebook_audit_20261008/audit_plot_and_cache.py)：两本数值本绘图／缓存复现，结果为 `plot_cache_evidence.json`；保存图总览为 `stored_figures_contact_sheet.png`。
- [Workspaces/notebook_audit_20261008/audit_wide_fields.py](Workspaces/notebook_audit_20261008/audit_wide_fields.py)：A/B/C 默认宽域数值场独立回算，结果为 `wide_field_evidence.json`。
- [Workspaces/notebook_audit_20261008/build_review.py](Workspaces/notebook_audit_20261008/build_review.py)：用户 HTML 与汇总证据生成器；`verify_report.cjs`、`report_validation.json`、`report_desktop*.png`、`report_mobile*.png` 为阅读布局核验。
- [Workspaces/notebook_audit_20261008/register_review.py](Workspaces/notebook_audit_20261008/register_review.py)：合并本专题进度和索引；`registration_before_20261009_*/` 保存登记前原件，`registration.json` 保存最终哈希。
''')
record = {'backups':str(backups),'report':str(ROOT/'report'/'notebook_review_20261009.html'),
          'current_matches_final_reviewed_version':summary['current_matches_final_reviewed_version'],
          'reviewed_versions':summary['reviewed_versions'],
          'files':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                   for p in [ROOT/'PROGRESS_LOG.md',ROOT/'FILE_INDEX.md',ROOT/'report'/'notebook_review_20261009.html',OUT/'summary.json']}}
(OUT/'registration.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(record,ensure_ascii=False))
