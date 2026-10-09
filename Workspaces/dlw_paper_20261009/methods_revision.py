from pathlib import Path
import json,re
from bs4 import BeautifulSoup

HERE=Path(__file__).resolve().parent

def clean_table(raw,headers):
    soup=BeautifulSoup(raw,'html.parser')
    table=soup.table
    old_values=[td.get_text(strip=True) for td in table.select('tbody td')]
    table['class']='comparison'
    table.thead.clear()
    row=soup.new_tag('tr')
    for label in headers:
        th=soup.new_tag('th',scope='col');th.string=label;row.append(th)
    table.thead.append(row)
    for row in table.select('tbody tr'):
        cells=row.find_all('td',recursive=False)
        minimum=min(float(c.get_text()) for c in cells)
        for cell in cells:
            text=cell.get_text(strip=True)
            if float(text)==minimum:
                cell.clear();b=soup.new_tag('strong');b.string=text;cell.append(b)
        for th in row.find_all('th',recursive=False):
            th.attrs.pop('valign',None)
            th['scope']='rowgroup' if 'rowspan' in th.attrs else 'row'
            th.string=th.get_text().replace('SD2','PF').replace('SD','PE')
    assert old_values==[td.get_text(strip=True) for td in table.select('tbody td')]
    return '<div class="table-wrap">'+str(table)+'</div>'

def revise(source):
    source=source.replace('定理 8.1 给出了局部形式算子意义下的相容性结论；全局谱问题和刘维尔可积性需另行研究。','')
    source=re.sub(r'势变量具有如下时间规范自由度：[\s\S]*?\n\n','',source,count=1)
    source=source.replace('### 8.3　PF 的线性问题与规范','### 8.3　PF 的 Lax 表示')
    source=source.replace('进一步的研究包括高频增长分支对稳定性的影响，以及全离散格式的空间收敛分析。','')
    oldsection=source[source.index('## 9　'):source.index('## 10　')]
    figures='\n\n'.join(re.findall(r'<figure>[\s\S]*?</figure>',oldsection))
    methods=(HERE/'numerical_methods_revised.md').read_text(encoding='utf-8')
    tables=json.loads((HERE/'tables.json').read_text(encoding='utf-8'))
    for label,key,headers in [
        ('SPACE','space_table',['算例','场','PE','PF','FD']),
        ('TIME','time_table',['算例','格式','场','Euler','RK4','C–N']),
        ('MESH','mesh_table',['算例','格式','场','固定网格','动网格'])]:
        methods=methods.replace('TABLE_'+label,clean_table(tables[key],headers))
    methods=methods.replace('FIGURES',figures)
    source=source.replace(oldsection,methods+'\n\n')
    tags=re.findall(r'\\tag\{([^}]+)\}',source)
    mapping={tag:str(i+1) for i,tag in enumerate(tags)}
    assert len(tags)==len(mapping)
    source=re.sub(r'\\tag\{([^}]+)\}',lambda m:r'\tag{'+mapping[m[1]]+'}',source)
    source=re.sub(r'（(R\d+|\d+)）',lambda m:'（'+mapping[m[1]]+'）',source)
    assert '时间自收敛' not in source and '时间规范自由度' not in source
    assert '全局谱问题' not in source and 'TABLE_' not in source
    return source
