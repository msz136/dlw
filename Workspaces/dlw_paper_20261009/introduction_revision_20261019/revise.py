from pathlib import Path
import re, json, shutil

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
ROOT = PROJECT.parents[1]
source = PROJECT / 'manuscript.md'
before = source.read_text(encoding='utf-8')
if (HERE / 'before_manuscript.md').exists():
    assert before == (HERE / 'before_manuscript.md').read_text(encoding='utf-8'), 'Source has changed since backup.'
else:
    shutil.copy2(source, HERE / 'before_manuscript.md')
    shutil.copy2(ROOT / 'report/dlw_paper_draft.html', HERE / 'before_draft.html')

refs = '''[11] D. S. Maltseva, R. O. Popovych. Point-symmetry pseudogroup, Lie reductions and exact solutions of Boiti–Leon–Pempinelli system. *Physica D* **460** (2024), 134081. [DOI](https://doi.org/10.1016/j.physd.2024.134081). [Preprint](https://arxiv.org/abs/2103.08734).

[12] S.-F. Tian, T.-T. Zhang, P.-L. Ma, X.-Y. Zhang. Lie symmetries and nonlocally related systems of the continuous and discrete dispersive long waves system by geometric approach. *Journal of Nonlinear Mathematical Physics* **22** (2015), 180–193. [DOI](https://doi.org/10.1080/14029251.2015.1023562).

[13] B.-F. Feng, K. Maruno, Y. Ohta. A self-adaptive moving mesh method for the Camassa–Holm equation. *Journal of Computational and Applied Mathematics* **235** (2010), 229–243. [DOI](https://doi.org/10.1016/j.cam.2010.05.044). [Preprint](https://arxiv.org/abs/0905.2693).

[14] B.-F. Feng, K. Maruno, Y. Ohta. Self-adaptive moving mesh schemes for short pulse type equations and their Lax pairs. *Pacific Journal of Mathematics for Industry* **6** (2014), 8. [DOI](https://doi.org/10.1186/s40736-014-0008-7). [Preprint](https://arxiv.org/abs/1403.6191).

[15] W. Huang, R. D. Russell. *Adaptive Moving Mesh Methods*. Applied Mathematical Sciences, vol. 174, Springer, 2011. [DOI](https://doi.org/10.1007/978-1-4419-7916-2).

[16] R. Hirota. *The Direct Method in Soliton Theory*. Cambridge Tracts in Mathematics, vol. 155, Cambridge University Press, 2004. [DOI](https://doi.org/10.1017/CBO9780511543043).'''

after = before
for lang, title in [('en', 'Introduction'), ('zh', '引言')]:
    start = after.index(f'## 1. {title} {{#{lang}-intro}}')
    end = after.index('## 2.', start)
    after = after[:start] + (HERE / f'introduction_{lang}.md').read_text(encoding='utf-8').strip() + '\n\n' + after[end:]
after = after.replace('# （2+1）维色散长波系统的可积半离散化 {#zh-title}', refs + '\n\n# （2+1）维色散长波系统的可积半离散化 {#zh-title}')
after = after.rstrip() + '\n\n' + refs + '\n'

def unchanged_body(text, lang):
    start = text.index('## 2.', text.index(f'{{#{lang}-intro}}'))
    end = text.index('## References' if lang == 'en' else '## 参考文献', start)
    return text[start:end]

stats = {}
for lang in ('en', 'zh'):
    assert unchanged_body(before, lang) == unchanged_body(after, lang)
    assert re.search(r'\*\*(?:Abstract\.|摘要。)\*\*[^\n]+', before[before.index(f'{{#{lang}-title}}'):])[0] == re.search(r'\*\*(?:Abstract\.|摘要。)\*\*[^\n]+', after[after.index(f'{{#{lang}-title}}'):])[0]
    for label, text in [('before', before), ('after', after)]:
        start = text.index(f'{{#{lang}-intro}}')
        intro = text[start:text.index('## 2.', start)]
        stats[f'{lang}_{label}_words_or_characters'] = len(re.findall(r"\b[\w]+(?:[’'-][\w]+)*\b", intro)) if lang == 'en' else len(intro)
    article = after[after.index(f'{{#{lang}-title}}'):]
    if lang == 'en':
        article = article[:article.index('# （2+1）维')]
    body, bibliography = re.split(r'## (?:References|参考文献).*?\n', article, maxsplit=1)
    defined = set(map(int, re.findall(r'^\[(\d+)\]', bibliography, re.M)))
    used = set()
    prose = re.sub(r'\$\$[\s\S]*?\$\$|\$[^\n$]*\$', '', body)
    for citation in re.findall(r'\[(\d[\d,– -]*)\](?!\()', prose):
        for part in citation.split(','):
            nums = list(map(int, re.findall(r'\d+', part)))
            used.update(range(nums[0], nums[-1]+1))
    assert defined == set(range(1,17)), defined
    assert used == defined, (lang, used, defined)
stats.update(abstracts_unchanged=True, sections_2_to_appendices_unchanged=True, references_per_language=16, all_references_cited=True)
source.write_text(after, encoding='utf-8')
(HERE / 'scope_validation.json').write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(stats, ensure_ascii=False, indent=2))
