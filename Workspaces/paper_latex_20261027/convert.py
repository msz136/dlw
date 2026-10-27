from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Comment
from urllib.parse import unquote
import re, shutil, json, hashlib

ROOT = Path(__file__).resolve().parents[2]
PREAMBLE = r'''% !TeX program = xelatex
% Standalone paper source; compile from this directory with XeLaTeX twice.
\documentclass[11pt,a4paper]{article}
\usepackage[margin=24mm]{geometry}
\usepackage{fontspec}
\setmainfont{Times New Roman}
\usepackage{amsmath,amssymb,mathtools}
\usepackage{graphicx,adjustbox,booktabs,tabularx,array,multirow}
\usepackage{caption,placeins}
\usepackage[hidelinks,unicode]{hyperref}
\usepackage{enumitem}
\captionsetup{font=small,labelfont=bf,justification=justified,singlelinecheck=false}
\setlength{\parindent}{1.2em}
\setlength{\parskip}{3pt}
\setlength{\emergencystretch}{2em}
\setlength{\textfloatsep}{14pt plus 3pt minus 3pt}
\setlength{\floatsep}{12pt plus 3pt minus 3pt}
\renewcommand{\topfraction}{.92}
\renewcommand{\bottomfraction}{.85}
\renewcommand{\textfraction}{.08}
\renewcommand{\floatpagefraction}{.65}
\setcounter{topnumber}{4}
\setcounter{bottomnumber}{3}
\setcounter{totalnumber}{6}
\newcolumntype{Y}{>{\raggedright\arraybackslash}X}
\newcommand{\paperdisplay}[2]{%
  \begin{equation*}
  \adjustbox{max width=.91\linewidth}{$\displaystyle #1$}#2
  \end{equation*}}
\begin{document}
'''

def escape(t):
    mapping = {'\\':r'\textbackslash{}','&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}',
    'τ':r'\(\tau\)','ρ':r'\(\rho\)','ε':r'\(\varepsilon\)','Δ':r'\(\Delta\)','×':r'\(\times\)','−':'-','≤':r'\(\leq\)','∎':r'\(\square\)','⁻':r'\textsuperscript{-}','⁴':r'\textsuperscript{4}','⁶':r'\textsuperscript{6}'}
    return ''.join(mapping.get(c,c) for c in re.sub(r'\s+', ' ',t))

class Converter:
    def __init__(self, source, name):
        self.source=ROOT/source; self.out=ROOT/'pdf'/name
        self.s=BeautifulSoup(self.source.read_text(encoding='utf-8'),'html.parser')
        self.assets=[]; self.math=[]; self.figures=0; self.tables=0
        (self.out/'images').mkdir(exist_ok=True)
        for el in self.s.select('nav,footer,a.export'): el.decompose()
        for el in list(self.s.select('.print-figure-part')): el.decompose()

    def children(self,n): return ''.join(self.convert(c) for c in n.children)
    def asset(self, img, num):
        src=ROOT/unquote(img['src']); candidate=None
        a=img.find_parent('a')
        if a and a.get('href','').endswith('.pdf'): candidate=ROOT/unquote(a['href'])
        if candidate is None:
            candidate=src.with_suffix('.pdf')
        if candidate.exists(): src=candidate
        dest=self.out/'images'/f'figure-{num:02d}{src.suffix}'
        shutil.copy2(src,dest)
        self.assets.append({'source':str(src.relative_to(ROOT)),'file':str(dest.relative_to(self.out)),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()})
        return dest.relative_to(self.out).as_posix()

    def table(self,n):
        self.tables+=1
        rows=n.select('tr'); occupied={}; output=[]; cols=0
        for ri,row in enumerate(rows):
            c=0; cells=[]
            for cell in row.find_all(['td','th'],recursive=False):
                while occupied.get(c,0)>ri: cells.append(''); c+=1
                span=int(cell.get('colspan',1)); rs=int(cell.get('rowspan',1))
                value=self.children(cell).strip()
                # Repeated row labels avoid ambiguous vertical alignment in wrapped cells.
                if rs>1:
                    for j in range(c,c+span): occupied[j]=ri+rs
                if span>1: value=r'\multicolumn{'+str(span)+r'}{>{\raggedright\arraybackslash}p{'+f'{span}'+r'\dimexpr\linewidth/'+str(sum(int(x.get('colspan',1)) for x in rows[0].find_all(['td','th'],recursive=False)))+r'-2\tabcolsep\relax}}{'+value+'}'
                cells.append(value); c+=span
            while occupied.get(c,0)>ri: cells.append(''); c+=1
            cols=max(cols,c)
            output.append(' & '.join(cells)+r' \\'+ ('\n\\midrule' if row.parent.name=='thead' and row==row.parent.find_all('tr',recursive=False)[-1] else ''))
        caption=self.children(n.caption).strip() if n.caption else ''
        if self.source.name=='dlw-paper.html' and self.tables==8:
            return '\n\\begin{table}[!htbp]\n\\centering\n\\caption*{'+caption+'}\n\\small\n\\setlength{\\tabcolsep}{4pt}\n\\renewcommand{\\arraystretch}{1.22}\n\\begin{adjustbox}{max width=\\linewidth}\n\\begin{tabular}{llrrrl}\n\\toprule\n'+'\n'.join(output)+'\n\\bottomrule\n\\end{tabular}\n\\end{adjustbox}\n\\end{table}\n'
        return '\n\\begin{table}[!htbp]\n\\centering\n\\caption*{'+caption+'}\n\\small\n\\setlength{\\tabcolsep}{4pt}\n\\renewcommand{\\arraystretch}{1.22}\n\\begin{tabularx}{\\linewidth}{'+'Y'*cols+'}\n\\toprule\n'+'\n'.join(output)+'\n\\bottomrule\n\\end{tabularx}\n\\end{table}\n'

    def convert(self,n):
        if isinstance(n,Comment): return ''
        if isinstance(n,NavigableString): return escape(str(n))
        cl=n.get('class',[])
        if 'katex-display' in cl:
            raw=re.sub(r'\s+',' ',n.annotation.get_text()).strip(); self.math.append(raw)
            tags=re.findall(r'\\tag\{([^}]+)\}',raw); raw=re.sub(r'\\tag\{[^}]+\}','',raw)
            return '\n\\paperdisplay{'+raw+'}{'+(r'\tag{'+tags[0]+'}' if tags else '')+'}\n'
        if 'katex' in cl:
            raw=re.sub(r'\s+',' ',n.annotation.get_text()).strip(); self.math.append(raw)
            return r'\('+raw+r'\)'
        if n.name=='h1': return '\n{\\centering\\LARGE\\bfseries '+self.children(n)+'\\par}\n\\vspace{1.2em}\n'
        if n.name in ['h2','h3','h4']:
            level={'h2':'section','h3':'subsection','h4':'subsubsection'}[n.name]
            return ('\n\\FloatBarrier\n' if n.name in ['h2','h3'] else '\n')+'\\'+level+'*{'+self.children(n)+'}\n'
        if n.name=='p': return '\n\n'+self.children(n).strip()+'\n\n'
        if n.name=='figure':
            self.figures+=1; img=n.find('img'); asset=self.asset(img,self.figures)
            caption=self.children(n.find('figcaption')).strip()
            return '\n\\begin{figure}[!htbp]\n\\centering\n\\includegraphics[width=\\linewidth,height=.72\\textheight,keepaspectratio]{'+asset+'}\n\\caption*{'+caption+'}\n\\end{figure}\n'
        if n.name=='table': return self.table(n)
        if n.name in ['strong','b','em','i','sup','sub','code']:
            cmd={'strong':'textbf','b':'textbf','em':'emph','i':'textit','sup':'textsuperscript','sub':'textsubscript','code':'texttt'}[n.name]
            return '\\'+cmd+'{'+self.children(n)+'}'
        if n.name=='br': return r'\newline '
        if n.name=='ol': return '\n\\begin{enumerate}[label={[\\arabic*]},leftmargin=*,itemsep=5pt]\n'+self.children(n)+'\n\\end{enumerate}\n'
        if n.name=='ul': return '\n\\begin{itemize}\n'+self.children(n)+'\n\\end{itemize}\n'
        if n.name=='li': return '\n\\item '+self.children(n)+'\n'
        if n.name=='a':
            href=n.get('href','')
            if href.startswith('https://'): return '\\href{'+href.replace('%',r'\%')+'}{'+self.children(n)+'}'
            return self.children(n)
        if n.name in ['script','style']: return ''
        return self.children(n)

    def run(self):
        text=PREAMBLE+self.convert(self.s.body)+'\n\\end{document}\n'
        text=re.sub(r'\n[ \t]*\n(?:[ \t]*\n)+','\n\n',text)
        (self.out/'main.tex').write_text(text,encoding='utf-8')
        return {'source':self.source.name,'figures':self.figures,'tables':self.tables,'math_count':len(self.math),'assets':self.assets,'source_sha256':hashlib.sha256(self.source.read_bytes()).hexdigest()}

if __name__=='__main__':
    result={name:Converter(fn,name).run() for fn,name in [('dlw-paper.html','dlw'),('2HS paper.html','2hs')]}
    (ROOT/'Workspaces/paper_latex_20261027/conversion_manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print({k:{x:v[x] for x in ['figures','tables','math_count']} for k,v in result.items()})

