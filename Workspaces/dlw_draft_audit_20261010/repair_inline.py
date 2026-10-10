from pathlib import Path
import re
p=Path(__file__).resolve().parent/'audit.md'
s=p.read_bytes().decode('utf-8')
if re.search(r'(?<!\$)\$(?!\$)[^\n$]+\$',s):
    print('Inline math is already normalized.')
    raise SystemExit(0)
commands=('psi','tau','zeta','varepsilon','rho','lambda','alpha','beta','omega','delta','sum','eta','ell','operatorname','theta','kappa','sigma','chi','dot','bar')
def fix_prose(z):
    for old,new in [('\t'+'au',r'\tau'),('\t'+'heta',r'\theta'),('\v'+'arepsilon',r'\varepsilon'),('\r'+'ho',r'\rho'),('\b'+'eta',r'\beta'),('\b'+'ar',r'\bar')]:
        z=z.replace(old,new)
    out=[];i=0
    while i<len(z):
        if z[i]!='(' or (i and z[i-1]==']'):
            out.append(z[i]);i+=1;continue
        depth=1;j=i+1
        while j<len(z) and depth:
            if z[j]=='(':depth+=1
            elif z[j]==')':depth-=1
            j+=1
        assert depth==0,z[i:]
        tex=z[i+1:j-1]
        tex=re.sub(r'(?<![a-zA-Z\\])('+'|'.join(commands)+r')(?![a-zA-Z])',lambda m:'\\'+m[0],tex)
        out.append('$'+tex+'$');i=j
    return ''.join(out)
parts=re.split(r'(\$\$[\s\S]*?\$\$)',s)
s=''.join(z if i%2 else fix_prose(z) for i,z in enumerate(parts))
assert not any(ord(c)<32 and c not in '\n\r' for c in s)
p.write_text(s,encoding='utf-8')
