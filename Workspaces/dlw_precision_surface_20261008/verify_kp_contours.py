from pathlib import Path
import nbformat, base64, hashlib, json
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
results={}
for name in ('DLW','2HS'):
    path=ROOT/f'notebook/{name}数值分析report.ipynb'
    nb=nbformat.read(path,4)
    old=nbformat.read(HERE/'before_kp_contours'/path.name,4)
    def tables(book):
        return [o.data['text/html'] for c in book.cells for o in c.get('outputs',[]) if 'text/html' in o.get('data',{})]
    assert tables(nb)==tables(old)
    nbformat.validate(nb)
    images=[]
    for c in nb.cells:
        if c.cell_type=='code':
            compile(c.source,c.id,'exec')
            assert not any(o.output_type=='error' for o in c.outputs)
        images.extend(o.data['image/png'] for o in c.get('outputs',[]) if 'image/png' in o.get('data',{}))
    assert len(images)==(6 if name=='DLW' else 12)
    for i,data in enumerate(images):
        (HERE/f'{name.lower()}_kp_final_{i}.png').write_bytes(base64.b64decode(data))
    results[name]=dict(tables_unchanged=True,images=len(images),sha256=hashlib.sha256(path.read_bytes()).hexdigest())
results['style']=dict(cmap='jet',map_style='contour',levels=11,shared_numerical_exact_scale=True,reference='case_C_kp.png / user attachment',white_2d_background=True)
(HERE/'kp_contours_validation.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
log=ROOT/'PROGRESS_LOG.md';s=log.read_text(encoding='utf-8')
marker='**静态图集集成与颜色修正：**'
note=(' **最终KP配色与等高线（2026-10-08）：** 按用户附图覆盖前轮柔和填色，'
      '物理场与误差改 jet 配色，二维图为白底彩色等高线，不填充背景；'
      '数值／解析共用11条等高线高度和线性色标，3D曲面采用同色标。'
      'PLOT_CONFIG 提供 map_style、levels、contour_width 与 cmap，A/B/C 独立范围保留。'
      '两份 Notebook 和主HTML同步；原表保持，DLW复用数值缓存。'
      '证据见 Workspaces/dlw_precision_surface_20261008/kp_contours_validation.json。')
if note not in s:log.write_text(s.replace(marker,marker+note,1),encoding='utf-8')
index=ROOT/'FILE_INDEX.md';s=index.read_text(encoding='utf-8')
if 'verify_kp_contours.py' not in s:
    index.write_text(s+'\n- `Workspaces/dlw_precision_surface_20261008/verify_kp_contours.py`、`kp_contours_validation.json`、`dlw_kp_final_0..5.png`、`2hs_kp_final_0..11.png`：用户附图对应KP彩色等高线集成、原表核对；`before_kp_contours/` 修改前备份。\n',encoding='utf-8')
print(json.dumps(results,indent=2))
