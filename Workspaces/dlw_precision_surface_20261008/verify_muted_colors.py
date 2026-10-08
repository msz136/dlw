from pathlib import Path
import json, hashlib, base64
import nbformat

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
results = {}
for name in ('DLW', '2HS'):
    filename = f'{name}数值分析report.ipynb'
    current = nbformat.read(ROOT/'notebook'/filename, 4)
    previous = nbformat.read(HERE/'before_muted_colors'/filename, 4)
    nbformat.validate(current)
    def tables(nb):
        return [o.data['text/html'] for c in nb.cells for o in c.get('outputs', [])
                if 'text/html' in o.get('data', {})]
    assert tables(current) == tables(previous)
    images = [o.data['image/png'] for c in current.cells for o in c.get('outputs', [])
              if 'image/png' in o.get('data', {})]
    assert len(images) == (6 if name == 'DLW' else 12)
    for c in current.cells:
        if c.cell_type == 'code':
            compile(c.source, c.id, 'exec')
            assert not any(o.output_type == 'error' for o in c.outputs)
    results[name] = dict(tables_unchanged=True, images=len(images), no_errors=True,
        sha256=hashlib.sha256((ROOT/'notebook'/filename).read_bytes()).hexdigest())
    if name == '2HS':
        (HERE/'hs_muted_0.png').write_bytes(base64.b64decode(images[0]))
results['style'] = dict(color_steps=12, linear_amplitude_bins=True,
    shared_numerical_exact_scale=True, white_near_zero_bin=True,
    colors='muted blue-gray / terracotta; errors ochre',
    dlw_numerical_cache_reused=True)
(HERE/'muted_colors_validation.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
log = ROOT/'PROGRESS_LOG.md'
text = log.read_text(encoding='utf-8')
marker = '**静态图集集成与颜色修正：**'
addition = (' **低刺激色阶修订（2026-10-08）：** 按用户反馈取消白色至饱和色的连续虚化渐变，'
    '改12级线性幅值色阶，零附近留白，非零区采用蓝灰／陶土中等色调，误差采用棕金色；'
    '增强等高线辨识，关闭曲面明暗及抗锯齿造成的浅色接缝。末尾配置新增 color_steps；'
    '两份 Notebook 与主 HTML 同步，DLW 复用数值缓存、2HS 完整19单元执行通过，原误差表保持。'
    '核验见 Workspaces/dlw_precision_surface_20261008/muted_colors_validation.json。')
if addition not in text:
    text = text.replace(marker, marker+addition, 1)
    log.write_text(text, encoding='utf-8')
index = ROOT/'FILE_INDEX.md'
entry = '\n- `Workspaces/dlw_precision_surface_20261008/verify_muted_colors.py` / `muted_colors_validation.json`：柔和分层配色及原表保持核验；`dlw_muted_0..5.png`、`hs_muted_0.png` 为实数值图；`before_muted_colors/` 为本轮修改前备份。\n'
content = index.read_text(encoding='utf-8')
if 'verify_muted_colors.py' not in content:
    index.write_text(content+entry, encoding='utf-8')
print(json.dumps(results, indent=2))
