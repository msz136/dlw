import re, pathlib
t = pathlib.Path("manuscript.md").read_text(encoding="utf-8")
en = t[:t.index("# （2+1）维")]
used = sorted({int(x) for x in re.findall(r"\[(\d+)(?:[,\u2013-]|\])", en)})
refs = sorted({int(x) for x in re.findall(r"^\[(\d+)\] ", en, re.M)})
print("cited in EN:", used)
print("defined refs:", refs)
print("cited but undefined:", [x for x in used if x not in refs])
print("defined but never cited in EN:", [x for x in refs if x not in used])
