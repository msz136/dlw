"""Validate route-one material in the generated root numerical report."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
import hashlib
import json
import re
import subprocess

from bs4 import BeautifulSoup


ROOT=Path(__file__).resolve().parents[3]
HTML=ROOT/'numerical_analysis.html'
REPORT=ROOT/'Workspaces/dlw_semidiscrete/numerics/REPORT.md'
FIGURE='Workspaces/dlw_semidiscrete/numerics/figures/fig19_route1_mesh.png'
LONG_FIGURE='Workspaces/dlw_semidiscrete/numerics/figures/fig20_route1_transport.png'
INTERVAL_FIGURE='Workspaces/dlw_semidiscrete/numerics/figures/fig21_mesh_refresh_interval.png'
OUT=Path(__file__).with_name('route1_sync_validation.json')


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    soup=BeautifulSoup(HTML.read_text(encoding='utf-8'),'html.parser')
    ids=[element['id'] for element in soup.find_all(id=True)]
    assert len(ids)==len(set(ids)), 'duplicate HTML IDs'
    broken=[]
    for tag in soup.find_all(['a','img']):
        url=tag.get('href' if tag.name=='a' else 'src','')
        if not url:continue
        if url.startswith('#'):
            if url[1:] not in ids:broken.append(url)
        elif not urlsplit(url).scheme:
            if not (ROOT/unquote(urlsplit(url).path)).exists():broken.append(url)
    assert not broken, f'broken local links: {broken}'
    heading=next((h for h in soup.find_all(['h2','h3'])
                  if '路线一：共同 x 网格' in h.get_text(' ',strip=True)),None)
    assert heading is not None,'route-one section absent'
    assert len(soup.find_all('img',src=FIGURE))==1,'route-one figure missing/duplicate'
    assert len(soup.find_all('img',src=LONG_FIGURE))==1,'long-distance figure missing/duplicate'
    assert len(soup.find_all('img',src=INTERVAL_FIGURE))==1,'interval figure missing/duplicate'
    interval_heading=next((h for h in soup.find_all(['h2','h3'])
                           if '路线一延伸：重分布间隔如何影响误差' in h.get_text(' ',strip=True)),None)
    assert interval_heading is not None,'interval section absent'
    assert '较频繁的重分布通常有效' in interval_heading.parent.get_text(' ',strip=True)
    blocks=[]
    for sibling in heading.next_siblings:
        if getattr(sibling,'name',None)=='h3':break
        if getattr(sibling,'get_text',None):blocks.append(sibling.get_text(' ',strip=True))
    text=' '.join(blocks)
    assert '初始重分布有短时收益' in text
    assert '尚未达到几何实验显示稳定收益' in text
    math=[m.group(1) or m.group(2)
          for m in re.finditer(r'\\\((.*?)\\\)|\\\[(.*?)\\\]',text,re.S)]
    math += [m.group(1) for m in re.finditer(
        r'(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)',text,re.S)]
    assert math,'route-one formulas were not preserved in generated HTML'
    katex=ROOT/'Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.min.js'
    js=('const fs=require("fs"), k=require(process.argv[1]);'
        'let xs=JSON.parse(fs.readFileSync(0,"utf8"));'
        'let errors=[];xs.forEach((x,i)=>{try{k.renderToString(x,{throwOnError:true})}'
        'catch(e){errors.push({index:i,error:String(e)})}});'
        'process.stdout.write(JSON.stringify(errors));')
    proc=subprocess.run(['node','-e',js,str(katex)],input=json.dumps(math),
                        text=True,capture_output=True,check=True)
    errors=json.loads(proc.stdout)
    assert not errors,f'KaTeX errors: {errors}'
    result={'numerical_analysis_html_sha256':sha(HTML),
            'report_md_sha256':sha(REPORT),'route1_heading_id':heading['id'],
            'route1_formula_count':len(math),'broken_links':broken,
            'duplicate_ids':len(ids)-len(set(ids)),
            'interval_heading_id':interval_heading['id'],
            'route1_figures':[FIGURE,LONG_FIGURE,INTERVAL_FIGURE],
            'scope':'Generated HTML structure, local links, and route-one KaTeX formulas'}
    OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':main()
