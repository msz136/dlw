from pathlib import Path
import hashlib
import json
import re

root = Path(__file__).resolve().parents[2]
work = Path(__file__).resolve().parent
backup = work / 'registration_before'
backup.mkdir(exist_ok=True)
for name in ('PROGRESS_LOG.md', 'FILE_INDEX.md'):
    target = backup / name
    if not target.exists():
        target.write_bytes((root / name).read_bytes())

progress = '''<!-- MCH_LDG_READING_BEGIN -->
> **2026-10-09（mCH LDG 论文导读）：** 阅读 Chang、Liu、Tao 的 arXiv:2608.28077v2（28页），原文归档为 [2608.28077v2.pdf](Paper/refs/2608_28077/2608.28077v2.pdf)。新增 [中文导读](report/mch_ldg_2608_28077_reading.html)，按一阶重写、通量配对、离散能量、投影与非线性误差闭合、数值证据及2HS/DLW联系组织；明确联合误差k阶、k≥1与光滑/周期/投影初值条件、半离散与RK4全离散的区别、近临界网格观测阶和尖峰波理论范围。核读第5/17/24/25页原图，三部分并行交叉审读；三条关键代数恒等式精确为零，归档与原文件SHA256一致。130处静态数学严格渲染，禁用JavaScript下桌面1280px/窄屏390px无页面溢出、公式错误、破图或失效本地链接；已目视检查布局。源、笔记、页图与核验在 `Workspaces/paper_2608_28077_reading_20261009/`。未运行新的PDE演化或Lean证明。
<!-- MCH_LDG_READING_END -->'''

log = root / 'PROGRESS_LOG.md'
text = log.read_text(encoding='utf-8')
pattern = r'<!-- MCH_LDG_READING_BEGIN -->[\s\S]*?<!-- MCH_LDG_READING_END -->\s*'
text = re.sub(pattern, '', text)
log.write_text(progress + '\n\n' + text, encoding='utf-8')

descriptions = {
    'guide.src.html': '中文导读正文与版式源',
    'build.cjs': '离线HTML及静态数学生成器',
    'verify_layout.cjs': '桌面/窄屏/无JavaScript布局、图片和链接核验',
    'register.py': '本专题进度与逐文件索引合并',
    'pages.json': '原文逐页文本（28页）',
    'paper_layout.txt': '保留页面布局的文本抽取',
    'notes_method.md': '第1–8页方程、通量与能量独立审读',
    'notes_error.md': '第9–17页误差估计独立审读',
    'notes_experiments.md': '数值算例、证据和研究联系独立审读',
    'build_validation.json': '最终HTML公式计数、大小与哈希',
    'math_validation.json': '通量拆分/原函数差商精确核验与原文哈希',
    'layout_validation.json': '最终布局及本地链接核验结果',
}
rows = [
    '- [report/mch_ldg_2608_28077_reading.html](report/mch_ldg_2608_28077_reading.html)：用户中文导读，离线字体与公式、阅读顺序、原文图4。',
    '- [Paper/refs/2608_28077/2608.28077v2.pdf](Paper/refs/2608_28077/2608.28077v2.pdf)：原文归档，与用户指定微信文件字节相同。',
]
for file in sorted(work.iterdir()):
    if not file.is_file():
        continue
    relative = file.relative_to(root).as_posix()
    desc = descriptions.get(file.name)
    if file.name.startswith('page-'):
        desc = f'原文第{int(file.stem.split("-")[1])}页渲染'
    if file.name.startswith('guide_') and file.suffix == '.png':
        desc = '导读页面布局核验截图'
    rows.append(f'- [{relative}]({relative})：{desc or "本专题文件"}。')
rows.extend([
    '- `Workspaces/paper_2608_28077_reading_20261009/registration_before/PROGRESS_LOG.md`：首次登记前进度档备份。',
    '- `Workspaces/paper_2608_28077_reading_20261009/registration_before/FILE_INDEX.md`：首次登记前索引备份。',
    '- `Workspaces/paper_2608_28077_reading_20261009/registration.json`：登记后入口文件与交付文件哈希。',
])
index_block = '<!-- MCH_LDG_READING_INDEX_BEGIN -->\n**mCH LDG 论文导读（2026-10-09）：**\n\n' + '\n'.join(rows) + '\n<!-- MCH_LDG_READING_INDEX_END -->'
index = root / 'FILE_INDEX.md'
text = index.read_text(encoding='utf-8')
text = re.sub(r'<!-- MCH_LDG_READING_INDEX_BEGIN -->[\s\S]*?<!-- MCH_LDG_READING_INDEX_END -->\s*', '', text)
index.write_text(index_block + '\n\n' + text, encoding='utf-8')
tracked = [log, index, root/'report/mch_ldg_2608_28077_reading.html', root/'Paper/refs/2608_28077/2608.28077v2.pdf']
result = {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in tracked}
(work/'registration.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'registered':list(result)},ensure_ascii=False))
