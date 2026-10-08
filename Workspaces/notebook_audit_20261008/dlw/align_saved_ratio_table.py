"""Repair audit alignment only; pandas unstack sorts the model labels."""
import json
import pathlib
import re

root=pathlib.Path(__file__).resolve().parent
path=root/'numerical_checks.json'
checks=json.loads(path.read_text(encoding='utf-8'))
nb=json.loads(pathlib.Path(r'C:\Users\msz\aca\notebook\DLW数值分析report.ipynb').read_text(encoding='utf-8'))
records={(r['case'],r['model'],r['method'],r['mesh']):r for r in checks['main_27_runs']}
html=''.join(nb['cells'][29]['outputs'][1]['data']['text/html'])
stored={(int(row),int(col)):value.strip() for row,col,value in re.findall(r'<td\s+id="[^"]*_row(\d+)_col(\d+)"[^>]*>([^<]+)</td>',html)}
actual={}
for row,(case,model) in enumerate((case,model) for case in ('A','B','C') for model in ('FD','SD','SD2')):
    for col,field in enumerate(('u','v')):
        actual[row,col]=format(records[case,model,'RK4','moving']['max_errors'][field]/records[case,model,'RK4','fixed']['max_errors'][field],'.3f')
checks['saved_tables_against_recomputed'][-1]['mismatches']=[dict(row=row,column=col,saved=value,recomputed=actual[row,col]) for (row,col),value in stored.items() if actual[row,col]!=value]
path.write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
print([(c['cell'],c['numeric_entries'],len(c['mismatches'])) for c in checks['saved_tables_against_recomputed']])
print('all_completed',all(r['completed'] for r in checks['main_27_runs']))
print('max_initial_error',max(r['initial_error'] for r in checks['main_27_runs']))
