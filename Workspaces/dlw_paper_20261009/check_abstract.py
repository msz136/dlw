import difflib, pathlib
old = pathlib.Path("narrative_unit1/manuscript.md.before").read_text(encoding="utf-8")
new = pathlib.Path("manuscript.md").read_text(encoding="utf-8")
def grab(t, tag):
    for line in t.splitlines():
        if line.startswith(tag): return line
    return ""
for tag, name in (("**Abstract.**","EN"),("**摘要。**","ZH")):
    a, b = grab(old, tag), grab(new, tag)
    print(f"=== {name}: len {len(a)} -> {len(b)} ===")
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal": continue
        print(f"  [{op}] old:{a[i1:i2]!r}")
        print(f"        new:{b[j1:j2]!r}")
    print()
