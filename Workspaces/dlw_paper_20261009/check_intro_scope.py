import pathlib, re, difflib
old = pathlib.Path("narrative_unit1/dlw_paper_draft.html.before").read_text(encoding="utf-8")
new = pathlib.Path(r"C:\Users\msz\aca\report\dlw_paper_draft.html").read_text(encoding="utf-8")
def cut(html):
    a = html.index('<h2 id="en-intro">') if 'id="en-intro"' in html else html.index('id="en-intro"')
    b = html.index('id="en-continuous"')
    c = html.index('id="zh-intro"')
    d = html.index('id="zh-continuous"')
    return html[:a], html[a:b], html[b:c], html[c:d], html[d:]
o, n = cut(old), cut(new)
names = ["EN前言段之前", "EN引言", "EN引言到ZH引言之间", "ZH引言", "ZH引言之后"]
for i in range(5):
    same = o[i] == n[i]
    print(f"{names[i]:<22} identical={same}  len {len(o[i])} -> {len(n[i])}")
