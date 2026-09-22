import json, re, os

P = r"C:\Users\msz\.codex\sessions\2026\09\17\rollout-2026-09-17T14-21-01-01a0ae03-d75a-7771-bc00-1b829af1dfc6_01a0ae06-916c-75a2-8eef-ce07c9a9f79e.jsonl"
PAT = re.compile(r'Bäcklund|Backlund|backlund|Baecklund', re.I)

recs = []
with open(P, encoding='utf-8', errors='replace') as f:
    for ln in f:
        try:
            recs.append(json.loads(ln))
        except Exception:
            pass
print("parsed records:", len(recs))


def texts(o, path="", out=None):
    """yield (path, string) for every string field"""
    if out is None:
        out = []
    if isinstance(o, dict):
        for k, v in o.items():
            texts(v, f"{path}.{k}", out)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            texts(v, f"{path}[{i}]", out)
    elif isinstance(o, str):
        out.append((path, o))
    return out


hits = []
for r in recs:
    for pth, s in texts(r):
        if PAT.search(s):
            hits.append((r.get('ordinal'), r.get('type'), r.get('timestamp'), pth, s))

print("text fields containing Backlund:", len(hits))
print()
types = {}
for h in hits:
    types[h[1]] = types.get(h[1], 0) + 1
print("by record type:", types)
print()

# dump distinct hits
seen = set()
n = 0
for ordinal, rtype, ts, pth, s in hits:
    key = (ordinal, pth)
    if key in seen:
        continue
    seen.add(key)
    n += 1
    print("=" * 100)
    print(f"[ord {ordinal}] {rtype}  {ts}   field={pth}")
    print("-" * 100)
    print(s if len(s) < 6000 else s[:6000] + f"\n...[truncated, total {len(s)} chars]")
    print()
    if n >= 25:
        print("... (more hits suppressed)")
        break
