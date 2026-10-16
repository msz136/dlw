import json
from pathlib import Path
from datetime import datetime
from run_suite import run_fd,HERE

folder=HERE/'results'/f'{datetime.now():%Y%m%d_%H%M%S_%f}_extra_controls';folder.mkdir(parents=True)
configs=[dict(case='5.4',left=-20.,right=20.,kappa=0.,T=5.,dt=.000125,offset=0.,alpha=.5,order=2,n=2560,variant='rusanov',id='peak_Rusanov_N2560_halfdt')]
(folder/'planned_configs.json').write_text(json.dumps(configs,indent=2),encoding='utf-8')
rows=[]
for c in configs:
    rows.append(run_fd(c,folder));(folder/'manifest.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
