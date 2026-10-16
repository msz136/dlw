"""Independent, validated interpolation of exact-reference source histories.

Only the optional three-way decomposition uses interpolation. The primary
one-step defects and their four propagators remain evaluated at every step.
"""
from pathlib import Path
import json
import numpy as np
import common as C


class SourceCache:
    def __init__(self, out, module, models, T, count=5):
        self.module, self.models = module, models
        self.nodes = np.linspace(0., T, count)
        self.path = Path(out) / 'independent_source_cache'
        self.path.mkdir(exist_ok=True)
        self.arrays = {}
        self.checks = {}
        for kind, model in models.items():
            self.arrays[kind] = []
            for j, t in enumerate(self.nodes):
                path = self.path / f'{kind}_{j}.npy'
                receipt = self.path / f'{kind}_{j}.json'
                if not path.exists() or not receipt.exists():
                    src = module.source_parts(model, float(t))
                    np.save(path, np.stack([src[n] for n in ('y_model', 'x_stencil', 'x_wrap')]))
                    receipt.write_text(json.dumps({'t': float(t), 'checks': src['checks']}), encoding='utf-8')
                    del src
                data = json.loads(receipt.read_text(encoding='utf-8'))
                self.checks[kind] = max(self.checks.get(kind, 0.), max(data['checks'].values()))
                self.arrays[kind].append(np.load(path, mmap_mode='r'))
                print('SOURCE_CACHE', kind, j, float(t), flush=True)
        receipt = self.path / 'holdout_validation.json'
        if receipt.exists():
            self.validation = json.loads(receipt.read_text(encoding='utf-8'))
        else:
            records = []
            for kind, model in models.items():
                # Four unseen midpoints test every interpolation interval.
                for t in (self.nodes[:-1] + self.nodes[1:])/2:
                    exact = module.source_parts(model, float(t))
                    predicted = self.interpolate(kind, float(t))
                    for j, name in enumerate(('y_model', 'x_stencil', 'x_wrap')):
                        ref, err = exact[name], predicted[j]-exact[name]
                        scale = max(np.linalg.norm(ref), 1e-100)
                        records.append(dict(kind=kind,t=float(t),source=name,
                            full_relative_l2=float(np.linalg.norm(err)/scale),
                            full_linf=float(np.max(abs(err)))))
                    self.checks[kind] = max(self.checks[kind], max(exact['checks'].values()))
                    print('SOURCE_HOLDOUT', kind, float(t), records[-3:], flush=True)
            maximum = max(r['full_relative_l2'] for r in records)
            self.validation = dict(nodes=self.nodes.tolist(),records=records,
                maximum_relative_l2=maximum,initial_uniform_1e_5_threshold_passed=maximum<1e-5)
            receipt.write_text(json.dumps(self.validation,indent=2),encoding='utf-8')
        records=self.validation['records']
        self.validation['main_sources_maximum_relative_l2']=max(r['full_relative_l2'] for r in records if r['source']!='x_wrap')
        self.validation['wrap_maximum_relative_l2']=max(r['full_relative_l2'] for r in records if r['source']=='x_wrap')
        self.validation['acceptance']='y_model and x_stencil <1e-5; x_wrap <1e-3 (small cancellation residual)'
        self.validation['passed']=(self.validation['main_sources_maximum_relative_l2']<1e-5 and self.validation['wrap_maximum_relative_l2']<1e-3)
        receipt.write_text(json.dumps(self.validation,indent=2),encoding='utf-8')
        assert self.validation['passed'], self.validation

    def interpolate(self, kind, t):
        ans = np.zeros_like(self.arrays[kind][0])
        for j, node in enumerate(self.nodes):
            weight = 1.
            for l, other in enumerate(self.nodes):
                if l != j:
                    weight *= (t-other)/(node-other)
            if weight:
                ans += weight*self.arrays[kind][j]
        return ans

    def source_parts(self, model, t):
        val = self.interpolate(model.kind, t)
        ref = C.reference(model, t)
        ans = {n: val[j] for j,n in enumerate(('y_model','x_stencil','x_wrap'))}
        ans.update(total=val.sum(axis=0), native_ref=C.to_native(model,ref,t),
                   checks={'maximum_exact_source_check':self.checks[model.kind]})
        return ans
