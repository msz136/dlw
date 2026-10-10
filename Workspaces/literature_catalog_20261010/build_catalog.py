"""Index local literature without modifying or publishing its originals."""
from pathlib import Path
import json
import re
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / 'Paper'


def build():
    records = {}
    downloads = json.loads((PAPER / 'sources/literature_download_20261010.json').read_text(encoding='utf-8'))
    for item in downloads:
        stem = item['stem']
        path = PAPER / 'sources' / (item.get('filename') or stem + '.url')
        records[path] = (item['title'], item.get('page', ''), item.get('download_url', ''))
    benchmarks = json.loads((ROOT / 'Workspaces/dlw_structure_benchmarks/manifest.json').read_text(encoding='utf-8'))
    for item in benchmarks:
        records[ROOT / item['file']] = (item['title'], item['source'], '')
    known = {
        'PhysD-published.pdf': ('Solitons, breathers and rational solutions for a (2+1)-dimensional dispersive long wave system', 'https://doi.org/10.1016/j.physd.2021.133140'),
        'Numerical_Algorithms_gsg (1).pdf': ('Integrable semi-discretizations and self-adaptive moving mesh method for a generalized sine-Gordon equation', 'https://doi.org/10.1007/s11075-023-01504-1'),
        'hirota-book-new.pdf': ('广田良吾：孤子理论中的直接方法', ''),
    }
    for path in sorted(PAPER.rglob('*.pdf')):
        if path in records:
            continue
        title, source = known.get(path.name, (path.name, ''))
        match = re.search(r'(\d{4}\.\d{4,5})(?:v\d+)?', path.stem)
        if match:
            source = 'https://arxiv.org/abs/' + match[1]
        elif re.fullmatch(r'(math|nlin)\d{7}', path.stem):
            match = re.fullmatch(r'(math|nlin)(\d{7})', path.stem)
            source = f'https://arxiv.org/abs/{match[1]}/{match[2]}'
        records[path] = (title, source, '')
    lines = [
        '# 本地文献清单', '',
        '更新：2026-10-10。列出 `Paper/` 中的 PDF 和仅保存链接的文献。题名与来源取自已有下载记录；没有题名记录的条目按文件名列出。', '',
        '文献原件保存在本地。来源链接用于在线查阅；本地路径用于定位当前工作区文件。', '',
        '| 文献 | 来源 | 本地文件 | 状态 |',
        '| --- | --- | --- | --- |',
    ]
    for path, (title, source, download) in sorted(records.items(), key=lambda pair: str(pair[0]).lower()):
        assert path.is_file(), path
        local = path.relative_to(PAPER).as_posix()
        links = ([f'[来源]({source})'] if source else [])
        if download and download != source:
            links.append(f'[全文入口]({download})')
        title = title.replace('|', '\\|').replace('\n', ' ')
        status = 'PDF' if path.suffix.lower() == '.pdf' else '仅链接，尚无 PDF'
        lines.append(f'| {title} | {" · ".join(links) or "待补来源"} | [{local}]({quote(local)}) | {status} |')
    lines += ['', f'共 {len(records)} 条；其中 {sum(p.suffix.lower() == ".pdf" for p in records)} 份 PDF。', '']
    (PAPER / 'LITERATURE.md').write_text('\n'.join(lines), encoding='utf-8')
    print(f'Catalogue: {len(records)} records')


if __name__ == '__main__':
    build()
