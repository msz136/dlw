"""Time control for T=1 candidates; no changes to spatial equations."""
import json
import long_moving as study

def main():
    path=study.OUT/'time_half.json'
    saved=json.loads(path.read_text()) if path.exists() else dict(runs=[])
    for case in study.previous.CASES:
        for model in ('structure','fd'):
            for mesh in ('fixed','moving'):
                spec=dict(case=case,model=model,mesh=mesh,nx=32,dt=.00025)
                if any(r['spec']==spec for r in saved['runs']):continue
                row=study.one(spec);saved['runs'].append(row);study.previous.dump(path,saved)
                print(spec,row['status'],row['reached'],flush=True)

if __name__=='__main__':main()
