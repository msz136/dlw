"""Sequential wall-clock comparison including setup; fixed modes skip monitor."""
from pathlib import Path
import sys, json, hashlib, time, statistics

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'lib'),str(ROOT/'experiments')]
from moving_mesh_study import ALL
from moving_mesh_route1_coupled import run


def main():
    modes=('uniform','static_adaptive','moving','intermittent',
           'gradient_static','gradient_intermittent')
    output={'scope':{'cases':['P1','P7'],'models':['structure','fd'],
                     'T':.04,'dt':.000125,'nx':128,'repeats':3,
                     'clock':'sequential perf_counter around full setup+run',
                     'fixed_kernel':'no density/flux work between remaps'},
            'rows':[]}
    for index in (0,6):
        for model in ('structure','fd'):
            samples={mode:[] for mode in modes}
            for repeat in range(3):
                ordered=modes[repeat:]+modes[:repeat]
                for mode in ordered:
                    start=time.perf_counter()
                    row=run(ALL[index],model,mode,.04,.000125)
                    elapsed=time.perf_counter()-start
                    if row['status']!='complete':
                        raise RuntimeError((index,model,mode,row['status']))
                    samples[mode].append(elapsed)
            for mode in modes:
                output['rows'].append({'parameter_id':f'P{index+1}',
                    'model':model,'mode':mode,'seconds':samples[mode],
                    'median_seconds':statistics.median(samples[mode])})
            print(f'P{index+1} {model} done',flush=True)
    output['source_sha256']={str(Path(__file__).relative_to(ROOT)):
                            hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (ROOT/'out'/'moving_mesh'/'route1_cost.json').write_text(
        json.dumps(output,indent=2,allow_nan=False),encoding='utf-8')


if __name__=='__main__':main()
