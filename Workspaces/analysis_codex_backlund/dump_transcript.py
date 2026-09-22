import json, re, io

P = r"C:\Users\msz\.codex\sessions\2026\09\17\rollout-2026-09-17T14-21-01-01a0ae03-d75a-7771-bc00-1b829af1dfc6_01a0ae06-916c-75a2-8eef-ce07c9a9f79e.jsonl"
OUT = r"C:\Users\msz\学术内容\Workspaces\analysis_codex_backlund\transcript.txt"

recs = []
with open(P, encoding='utf-8', errors='replace') as f:
    for ln in f:
        try:
            recs.append(json.loads(ln))
        except Exception:
            pass

buf = io.StringIO()
w = buf.write
w(f"parsed records: {len(recs)}\n")
w("=" * 100 + "\n")


def emit(tag, s):
    if not isinstance(s, str) or not s.strip():
        return
    w(f"\n----- {tag} -----\n")
    w(s.rstrip() + "\n")


for r in recs:
    o = r.get('ordinal')
    t = r.get('type')
    ts = r.get('timestamp', '')
    p = r.get('payload') or {}
    w(f"\n############ ord {o}  type={t}  {ts} ############\n")

    if t == 'session_meta':
        w("  session_id=" + str(p.get('session_id')) + " cwd=" + str(p.get('cwd')) + "\n")
        continue

    if t == 'event_msg':
        pt = p.get('type')
        w(f"  [event_msg.type = {pt}]\n")
        if pt == 'user_message':
            emit('USER', p.get('message'))
        elif pt == 'agent_message':
            emit('AGENT', p.get('message'))
        elif pt in ('agent_reasoning', 'reasoning'):
            emit('REASONING', p.get('text') or p.get('message'))
        elif pt == 'exec_command_begin':
            emit('CMD', str(p.get('command')))
        elif pt in ('exec_command_end', 'exec_command_output'):
            emit('OUT', p.get('stdout') or p.get('output'))
        else:
            # generic: dump any long string fields
            for k, v in p.items():
                if isinstance(v, str) and len(v) > 40:
                    emit(f"EVT.{pt}.{k}", v)
                elif isinstance(v, dict):
                    for k2, v2 in v.items():
                        if isinstance(v2, str) and len(v2) > 40:
                            emit(f"EVT.{pt}.{k}.{k2}", v2)
        continue

    if t == 'response_item':
        pt = p.get('type')
        w(f"  [response_item.type = {pt}]\n")
        if pt == 'message':
            c = p.get('content')
            if isinstance(c, list):
                for part in c:
                    if isinstance(part, dict):
                        emit(f"MSG[{p.get('role')}].{part.get('type')}",
                             part.get('text') or part.get('input_text') or part.get('output_text'))
            else:
                emit(f"MSG[{p.get('role')}]", str(c))
        elif pt == 'reasoning':
            c = p.get('summary') or p.get('content')
            emit('REASONING', json.dumps(c, ensure_ascii=False) if not isinstance(c, str) else c)
        elif pt == 'function_call':
            emit(f"CALL {p.get('name')}", str(p.get('arguments'))[:4000])
        elif pt == 'function_call_output':
            o2 = p.get('output')
            emit('CALL_OUT', o2 if isinstance(o2, str) else json.dumps(o2, ensure_ascii=False)[:4000])
        elif pt == 'custom_tool_call':
            emit(f"TOOL {p.get('name')}", str(p.get('input'))[:4000])
        elif pt == 'custom_tool_call_output':
            emit('TOOL_OUT', str(p.get('output'))[:6000])
        else:
            for k, v in p.items():
                if isinstance(v, str) and len(v) > 40:
                    emit(f"RI.{pt}.{k}", v)
        continue

    # world_state / turn_context / token_usage_record: skip

with open(OUT, 'w', encoding='utf-8') as f:
    f.write(buf.getvalue())
print("written:", OUT, len(buf.getvalue()), "chars")
