import json, sys, re

P = r"C:\Users\msz\.codex\sessions\2026\09\17\rollout-2026-09-17T14-21-01-01a0ae03-d75a-7771-bc00-1b829af1dfc6_01a0ae06-916c-75a2-8eef-ce07c9a9f79e.jsonl"

with open(P, encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
print("total lines:", len(lines))

from collections import Counter
types = Counter()
for ln in lines[:400]:
    try:
        o = json.loads(ln)
    except Exception:
        types['<unparsed>'] += 1
        continue
    types[o.get('type', o.get('record_type', '?'))] += 1
print("first-400 record types:", dict(types))

print()
print("=== structure of first 3 parseable records ===")
shown = 0
for ln in lines:
    try:
        o = json.loads(ln)
    except Exception:
        continue
    print("--- keys:", sorted(o.keys()))
    print(json.dumps(o, ensure_ascii=False)[:900])
    print()
    shown += 1
    if shown >= 3:
        break
