from pathlib import Path

p = Path(r'C:\Users\msz\aca\Workspaces\dlw_paper_20261009\appendix_fill_20261026\publish_appendices.py')
s = p.read_text(encoding='utf-8')
pairs = s.count('\\\\')
s = s.replace('\\\\', '\\')

bad_start = s.index("<p><strong>Coefficient form of the compatibility condition.</strong>")
bad_end = s.index("<p><strong>Midpoint expansions.</strong>")
new = ("<p><strong>Coefficient form of the compatibility condition.</strong> Expanding "
       "{m('L_t+LM-" + r"\widetilde ML" + "')} with the rules {m('Dq=qD+q_x')} and {m('Yq_k=q_{k-1}Y')} produces "
       "terms proportional to {m('DY')}, {m('Y')}, {m('D')} and {m('D^0')}. The coefficient of {m('DY')} "
       "is {m('(S_k-S_{k-1})-2(C_k-A_k)_x')}, which vanishes by (47); once it is removed, the coefficient of "
       "{m('Y')} reduces to (48), the coefficient of {m('D^0')} to (49), and the coefficient of {m('D')} "
       "vanishes identically. Since {m('L')} and {m('M')} are at most second order in {m('D')}, the "
       "compatibility condition (42) is therefore equivalent to those three scalar relations.</p>\n")
s = s[:bad_start] + new + s[bad_end:]
p.write_text(s, encoding='utf-8')
print('pairs replaced:', pairs)
print('remaining pairs:', s.count('\\\\'))
print('single backslashes before widetilde:', s.count(r'\widetilde'))
