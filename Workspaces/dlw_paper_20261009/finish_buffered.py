"""Publish and validate the fully completed buffered experiment."""
from pathlib import Path
import subprocess,sys,json,re
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OUT=HERE/'buffered_run'
manifest=json.loads((OUT/'manifest.json').read_text(encoding='utf8'))
assert manifest['runs']==48 and manifest['all_completed']
for script in ['publish_buffered.py','finalize_buffered_notebook.py','validate_buffered.py','build.py']:
    subprocess.run([sys.executable,str(HERE/script)],check=True)
subprocess.run(['node',str(HERE/'check_buffered_layout.cjs')],check=True)
v=json.loads((OUT/'validation.json').read_text(encoding='utf8'));a=json.loads((OUT/'analysis.json').read_text(encoding='utf8'))
settings=json.loads((HERE/'next_numerical_settings.json').read_text(encoding='utf8'));settings['status']='completed_48_runs_and_published'
(HERE/'next_numerical_settings.json').write_text(json.dumps(settings,indent=2))
p=ROOT/'PROGRESS_LOG.md';s=p.read_text(encoding='utf8')
note=f"> **2026-10-10（扩域计算与正文更新完成）：** 48/48组均到达T=.01；四算例计算半宽10/20/40/40，展示与共同误差评价半宽5/10/30/30，dx=h=.1、dt=.0001。补入Physica D图4二孤子(1,2;4,-3)。完整域演化后裁切内部y层，x样条仅内插；最小节点覆盖余量{v['minimum_x_support_margin']:.6g}，最小J={v['min_J']:.6g}。1200个CN步满足原残差容差，最多{v['cn_max_iterations']}次迭代。Notebook三表和八幅PF输出更新；论文中英文3.4/3.5、三表、四幅精确解和八幅三方法比较图、摘要/结论同步。动网格改善{a['moving_improved']}/24个场误差；CN/RK4终止误差最大相对差{a['cn_rk4_max_relative_percent']:.6g}%。48份原生状态、12份场缓存与288个正文表值核对通过，全部陈列公式未改；桌面/窄屏无溢出、破图和公式错误。数据、备份和核验在buffered_run/；旧域结果仅保留为历史，不再作为当前论文结论。"
s=re.sub(r'> \*\*2026-10-10（扩域计算、内部截取，正在重算）：\*\*[^\n]*',lambda m:note,s,count=1)
p.write_text(s,encoding='utf8')
print('PUBLICATION COMPLETE')
