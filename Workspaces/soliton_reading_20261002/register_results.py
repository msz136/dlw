from pathlib import Path
import hashlib
import json
import msvcrt
import re

workspace = Path(__file__).resolve().parents[2]
folder = Path(__file__).resolve().parent
source = folder / 'guide.source.html'
output = workspace / 'report/soliton_reading_guide.html'
output.parent.mkdir(exist_ok=True)
output.write_bytes(source.read_bytes())

entries = {
    'PROGRESS_LOG.md': (
        '孤子理论教材／Lax与Darboux阅读定位',
        '> **2026-10-02（孤子理论教材／Lax与Darboux阅读定位）：** '
        '已找到广田良吾中文《孤子理论中的直接方法》`Paper/sources/hirota-book-new.pdf`（202PDF页；正文PDF页=书页+9），'
        '封面／目录／相关正文页视觉核对。用户确认口述词为Darboux。'
        '首读§4.0→§4.1，重点书156–157/PDF165–166的Lax与相容性；按需补§1.5/1.6；'
        '后接KP §4.2、Gram §3.2与Toda §4.5.1。区分本书Bäcklund章节与Darboux；'
        '本地ctp8805.pdf §2、PDF1–2（印刷807–808）为直接binary Darboux选读，'
        '已核对Lemma2.1/2.2，不直接等同当前DLW归一化。'
        '[阅读导读](report/soliton_reading_guide.html)含页码与PDF跳页链接；'
        '笔记、页图与HTML源在Workspaces/soliton_reading_20261002/。原PDF未改。'
    ),
    'FILE_INDEX.md': (
        '孤子理论教材／Lax与Darboux阅读定位',
        '**孤子理论教材／Lax与Darboux阅读定位（2026-10-02）：** '
        '[阅读导读](report/soliton_reading_guide.html)；'
        '`Workspaces/soliton_reading_20261002/READING_NOTES.md`（教材、确认术语、书页/PDF页及正文证据）；'
        '`guide.source.html`、`check_guide.cjs`、`html_validation.json`、`guide_1280.png`、`guide_390.png`（导读源与检查）；'
        '`tmp/pdfs/`（原书及ctp8805相关页图）；`register_results.py`、`registration.json`（合并登记）。'
    )
}

for name, (topic, entry) in entries.items():
    target = workspace / name
    with target.open('r+b') as stream:
        msvcrt.locking(stream.fileno(), msvcrt.LK_LOCK, 1)
        try:
            raw = stream.read()
            bom = raw.startswith(b'\xef\xbb\xbf')
            text = raw.decode('utf-8-sig')
            newline = '\r\n' if '\r\n' in text else '\n'
            paragraphs = re.split(r'\r?\n\r?\n', text)
            paragraphs = [p for p in paragraphs if topic not in p]
            body = entry + newline + newline + (newline + newline).join(paragraphs)
            encoded = body.encode('utf-8-sig' if bom else 'utf-8')
            stream.seek(0)
            stream.write(encoded)
            stream.truncate()
        finally:
            stream.seek(0)
            msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)

manifest = {
    'date': '2026-10-02',
    'guide': str(output),
    'guide_sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
    'sources': {
        str(p.relative_to(workspace)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in [workspace / 'Paper/sources/hirota-book-new.pdf', workspace / 'Paper/refs/ctp8805.pdf']
    },
    'term_confirmed_by_user': 'Darboux',
}
(folder / 'registration.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'registered': True, 'output': str(output)}, ensure_ascii=False))
