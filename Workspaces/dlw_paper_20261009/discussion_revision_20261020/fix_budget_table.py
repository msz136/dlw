from pathlib import Path
import re
p=Path(__file__).resolve().parents[1]/"manuscript.md"
s=p.read_text(encoding="utf-8")
pattern=r"(?m)^\| (?:Test|算例) \| (?:Method|方法) \|[^\n]*\n\|---[^\n]*\n(?:\|[^\n]*\n)+"
def table(m):
    lines=m[0].splitlines()
    def row(line,tag):
        cells=line[2:-2].split(" | ")
        return "<tr>"+"".join(f"<{tag}>{c}</{tag}>" for c in cells)+"</tr>"
    return '<div class="table-wrap"><table class="comparison compact-results"><thead>'+row(lines[0],"th")+"</thead><tbody>"+"".join(row(line,"td") for line in lines[2:])+"</tbody></table></div>\n"
s,n=re.subn(pattern,table,s)
assert n==2,n
p.write_text(s,encoding="utf-8")
