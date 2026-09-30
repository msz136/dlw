"""Time-step control for the two completed current four-scheme routes."""
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("two_soliton_four", HERE / "run_four_schemes.py")
model = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model)
model.DT = model.DT / 2
out = HERE / "four_half_dt"
out.mkdir(exist_ok=True)
model.HERE = out
results = {}
for scheme in ("S3", "S4"):
    results[scheme] = model.run(scheme)
    print(scheme, results[scheme]["status"], results[scheme]["last_time"], flush=True)
config = {"dt": model.DT, "schemes": ["S3", "S4"],
          "run_four_schemes_sha256": hashlib.sha256((HERE / "run_four_schemes.py").read_bytes()).hexdigest(),
          "driver_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(out / "results.json").write_text(json.dumps({"configuration":config,"results":results},indent=2)+"\n",encoding="utf-8")
