import json, io

P = r"C:\Users\msz\.codex\sessions\2026\09\17\rollout-2026-09-17T14-21-01-01a0ae03-d75a-7771-bc00-1b829af1dfc6_01a0ae06-916c-75a2-8eef-ce07c9a9f79e.jsonl"
OUT = r"C:\Users\msz\学术内容\Workspaces\analysis_codex_backlund\conversation.txt"

recs = []
with open(P, encoding='utf-8', errors='replace') as f:
    for ln in f:
        try:
            recs.append(json.loads(ln))
        except Exception:
            pass

buf = io.StringIO()
n_u = n_a = 0
for r in recs:
    o = r.get('ordinal')
    t = r.get('type')
    p = r.get('payload') or {}
    if t == 'event_msg':
        pt = p.get('type')
        if pt == 'user_message':
            n_u += 1
            buf.write(f"\n\n########## [{o}] USER #{n_u} ##########\n")
            buf.write((p.get('message') or '').rstrip() + "\n")
        elif pt == 'agent_message':
            n_a += 1
            buf.write(f"\n\n---------- [{o}] CODEX #{n_a} ----------\n")
            buf.write((p.get('message') or '').rstrip() + "\n")
    elif t == 'response_item':
        pt = p.get('type')
        if pt == 'message' and p.get('role') in ('assistant', 'user'):
            role = p.get('role').upper()
            c = p.get('content')
            parts = []
            if isinstance(c, list):
                for part in c:
                    if isinstance(part, dict):
                        tx = part.get('text') or part.get('input_text') or part.get('output_text')
                        if tx:
                            parts.append(tx)
            if parts:
                buf.write(f"\n\n---------- [{o}] {role} (response_item) ----------\n")
                buf.write("\n".join(parts).rstrip() + "\n")

with open(OUT, 'w', encoding='utf-8') as f:
    f.write(buf.getvalue())
print("written:", OUT, len(buf.getvalue()), "chars; user msgs:", n_u, "codex msgs:", n_a)
