const fs = require('fs');
const path = require('path');
const {pathToFileURL} = require('url');
const {chromium} = require('C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const katex = require('C:/Users/msz/aca/Workspaces/gsg_project/dlw_report/_assets/package/dist/katex.js');
const root = 'C:/Users/msz/aca';
const out = __dirname;
const css = `
@page{size:A4;margin:23mm 23mm 22mm}
html{background:white;color:#000}body{margin:0;font-family:"Times New Roman",SimSun,serif;font-size:11pt;line-height:1.38}
main{width:164mm;max-width:none;margin:0 auto;padding:0}article,#chinese{margin:0;padding:0;border:0}
.language-nav,nav{display:none}h1{font-size:17pt;line-height:1.25;font-weight:bold;max-width:none;margin:0 0 18pt;text-align:center}
h2{font-size:12pt;line-height:1.25;margin:18pt 0 8pt;break-after:avoid;border:0}
h3{font-size:11pt;line-height:1.3;margin:13pt 0 6pt;break-after:avoid}
h4{font-size:11pt;line-height:1.3;margin:11pt 0 6pt;break-after:avoid}
p{margin:0 0 7pt;text-align:justify;orphans:3;widows:3;hyphens:none}
article[lang="zh-CN"]{font-size:10.5pt;line-height:1.55}article[lang="zh-CN"]>p{text-indent:2em}
.abstract,.keywords{font-size:10pt;line-height:1.4;text-indent:0!important;margin:0 0 9pt;padding:0}
.keywords{margin-bottom:15pt}.theorem{text-indent:0!important}
a{color:#000;text-decoration:none}strong{font-weight:bold}
.eq,.equation{font-size:10.5pt;max-width:100%;overflow:visible;margin:10pt 0;padding:0;break-inside:avoid;text-indent:0}
.eq .katex,.equation .katex{font-size:1em}.katex{font-size:1em}.katex-display{margin:0}
.eq .katex-display>.katex,.equation .katex-display>.katex{min-width:0;padding:0;text-align:center}
.eq .katex-html,.equation .katex-html{width:100%;min-width:0;padding:0 2.3em!important}
.eq .katex-tag,.equation .katex-tag{right:0!important}
.eq-anchor{height:0;margin:0;padding:0;break-after:avoid}
figure{margin:14pt 0 16pt;break-inside:avoid;max-height:none}
figure img{display:block;width:100%;height:auto;max-height:160mm;object-fit:contain;margin:0 auto}
figcaption{font-size:9pt;line-height:1.35;text-align:justify;margin:7pt 0 0;orphans:2;widows:2}
.table-wrap{overflow:visible;break-inside:avoid;margin:12pt 0 14pt}
table{width:100%;table-layout:fixed;font-size:8.2pt;line-height:1.3;white-space:normal;margin:0;border-collapse:collapse;border-top:1pt solid #000;border-bottom:1pt solid #000;font-variant-numeric:tabular-nums}
caption{caption-side:top;text-align:justify;font-size:9pt;line-height:1.35;padding:0 0 7pt;font-weight:normal}
thead{border-bottom:.6pt solid #000;display:table-header-group}tr{break-inside:avoid}th,td{padding:5pt 2pt;border:0;text-align:center;vertical-align:middle}
table.comparison th,table.comparison td{padding:5pt 2pt;background:#fff}table.comparison tbody th{font-weight:normal;text-align:left}
table.comparison strong{font-weight:bold}table.comparison thead th{font-weight:bold}
.sci{white-space:nowrap}.sci sup{font-size:.73em}sub{font-size:.75em}
.ref{font-size:9.3pt;line-height:1.3;padding-left:1.6em;text-indent:-1.6em!important;margin:0 0 5pt;break-inside:avoid;overflow-wrap:anywhere}
.data{text-indent:0!important;font-size:9.5pt}.proof-label{font-style:italic;font-weight:normal}
.references-block{break-inside:avoid}
@media print{main{width:auto;margin:0}body{font-size:11pt}#chinese{break-before:auto}h1{font-size:17pt}.eq,.equation{font-size:10.5pt}table{font-size:8.2pt}figure{max-height:none}}
`;
(async()=>{
fs.mkdirSync(out,{recursive:true});
const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
const results=[];
for(const [id,lang,label] of [['english','en','English'],['chinese','zh-CN','Chinese']]){
 const page=await browser.newPage({viewport:{width:900,height:1100}});
 await page.goto(pathToFileURL(path.join(root,'report/dlw_paper_draft.html')).href);
 const before=await page.evaluate(id=>{
  const a=document.getElementById(id);
  return {math:[...a.querySelectorAll('annotation')].map(e=>e.textContent),numbers:[...a.querySelectorAll('tbody td')].flatMap(e=>e.textContent.match(/\d+\.\d+e-\d+/g)||[]),figures:a.querySelectorAll('figure').length};
 },id);
 await page.evaluate(({id,lang,css})=>{
  const a=document.getElementById(id);document.querySelector('main').replaceChildren(a);
  document.querySelector('.language-nav')?.remove();document.documentElement.lang=lang;
  document.title=a.querySelector('h1').textContent;
  if(lang==='zh-CN'){
   const label=a.querySelector('p strong');if(label?.textContent.startsWith('摘要'))label.textContent='摘要：';
  }
  document.head.appendChild(Object.assign(document.createElement('style'),{textContent:css}));
  const walker=document.createTreeWalker(a,NodeFilter.SHOW_TEXT);const nodes=[];while(walker.nextNode())nodes.push(walker.currentNode);
  for(const n of nodes){
   if(n.parentElement.closest('.katex,figcaption'))continue;
   n.textContent=n.textContent.replace(/Figures?\s+(\d+)(?:[–—-](\d+))?/g,(_,x,y)=>y?`Figures ${+x+4}-${+y+4}`:`Figure ${+x+4}`).replace(/图\s*(\d+)(?:[–—-](\d+))?/g,(_,x,y)=>y?`图 ${+x+4}—${+y+4}`:`图 ${+x+4}`);
   if(lang==='en')n.textContent=n.textContent.replace(/\s+([,;.])/g,'$1').replace(/\u2011/g,'-');
  }
  [...a.querySelectorAll('figure')].forEach((f,i)=>{
   f.id=`${lang}-figure-${i+1}`;
   const c=f.querySelector('figcaption');c.textContent=c.textContent.replace(/^Figure\s+\d+\.\s*|^图\s*\d+\s*/, '');
   if(lang==='zh-CN')c.textContent=c.textContent.replace(/\)的/g,') 的');
   c.prepend(Object.assign(document.createElement('strong'),{textContent:lang==='en'?`Figure ${i+1}. `:`图 ${i+1}　`}));
   const img=f.querySelector('img');img.loading='eager';img.src=new URL(img.getAttribute('src'),document.baseURI).href;
   f.querySelector('a')?.removeAttribute('href');
  });
  for(const [i,t] of [...a.querySelectorAll('table')].entries()){
   const wrap=t.parentElement;const p=wrap.previousElementSibling;
   if(p?.tagName==='P' && /^(Table|表)/.test(p.textContent)){
    const cap=document.createElement('caption');cap.innerHTML=p.innerHTML.replace(/^<strong>([\s\S]*)<\/strong>$/,'$1');t.prepend(cap);p.remove();
   }
   const rows=[...t.tBodies[0].rows];const heads=[...t.tHead.rows[0].cells].map(c=>c.textContent.split(':')[0]);
   t.tHead.innerHTML=`<tr><th rowspan="2">${heads[0]}</th>${heads.slice(1).map(h=>`<th colspan="2">${h}</th>`).join('')}</tr><tr>${heads.slice(1).map(()=>'<th><i>e</i><sub>u</sub></th><th><i>e</i><sub>v</sub></th>').join('')}</tr>`;
   const col=document.createElement('colgroup');col.innerHTML='<col style="width:20%">'+heads.slice(1).map(()=>'<col><col>').join('');t.prepend(col);
   for(const r of rows){for(const c of [...r.cells].slice(1)){
    const parts=c.innerHTML.split(/\s+\/\s+/);if(parts.length!==2)throw Error('Expected two physical fields');for(const part of parts){const td=document.createElement('td');td.innerHTML=part.replace(/(\d+\.\d+)e-(\d+)/g,(_,v,e)=>`<span class="sci" data-value="${v}e-${e}">${v} × 10<sup>−${+e}</sup></span>`);r.insertBefore(td,c)}c.remove();
   }}
   t.id=`${lang}-table-${i+1}`;
  }
  for(const p of a.querySelectorAll(':scope > p')){
   if(p.textContent.startsWith(lang==='en'?'Abstract.':'摘要'))p.classList.add('abstract');
   if(/^(Keywords|关键词)/.test(p.textContent))p.classList.add('keywords');
   if(/^\[\d+\]/.test(p.textContent)){
    p.classList.add('ref');for(const link of p.querySelectorAll('a[href^="https://doi.org/"]'))link.textContent=link.href.replace('https://doi.org/','doi:');
   }
   if(p.querySelector('a[id]')&&!p.textContent.trim())p.classList.add('eq-anchor');
   if(/^(Proposition|Theorem|Lemma|Proof|命题|定理|引理|证明)/.test(p.textContent))p.classList.add('theorem');
   if(/^(Proof\.|证明)/.test(p.textContent))p.querySelector('strong')?.classList.add('proof-label');
  }
  const dh=a.querySelector('h2[id$="-data"]');for(let e=dh?.nextElementSibling;e&&e.tagName!=='H2';e=e.nextElementSibling)e.classList.add('data');
  const rh=a.querySelector('h2[id$="-references"]');if(rh){const block=document.createElement('section');block.className='references-block';rh.before(block);while(block.nextElementSibling)block.appendChild(block.nextElementSibling);}
  // Treat displayed equations as grammatical parts of their surrounding sentence.
  for(const e of a.querySelectorAll('.eq,.equation')){
   let next=e.nextElementSibling;while(next?.classList.contains('eq-anchor'))next=next.nextElementSibling;
   const text=next?.textContent.trim()||'';
   if(next?.tagName==='P'){
    const punct=lang==='en'?( /^(where|and |with |satisfy|implies|so that|which|for |respectively)/.test(text)?',':'.'):(/^(其中|这里|式中|满足|蕴含|则|从而)/.test(text)?',':'.');
    e.dataset.sentencePunctuation=punct;
   }
  }
 },{id,lang,css});
 const punctuation=await page.evaluate(()=>[...document.querySelectorAll('.eq,.equation')].map(e=>({tex:e.querySelector('annotation').textContent,punct:e.dataset.sentencePunctuation})));
 const rendered=punctuation.map(({tex,punct})=>{
   const tag=tex.match(/\\tag\{[^}]+\}/)?.[0]||'';
   const base=tex.replace(/\\tag\{[^}]+\}/,'').trim();
   const final=punct && !/[,.;]$/.test(base)?`${base}${punct}${tag}`:tex;
   return {html:katex.renderToString(final,{displayMode:true,throwOnError:true,strict:'error'}),original:tex};
 });
 await page.evaluate(rendered=>{
  [...document.querySelectorAll('.eq,.equation')].forEach((e,i)=>{e.innerHTML=rendered[i].html;e.dataset.originalTex=rendered[i].original;});
 },rendered);
 await page.evaluate(()=>document.fonts.ready);
 await page.evaluate(async()=>{await Promise.all([...document.images].map(i=>i.decode()));});
 // Fit the rare long display to the text block, leaving space for its number.
 const fitted=await page.evaluate(()=>{
  const res=[];for(const e of document.querySelectorAll('.eq,.equation')){
   const h=e.querySelector('.katex-html');const bases=[...h.children].filter(x=>x.classList.contains('katex-base'));
   const total=bases.reduce((s,b)=>s+b.getBoundingClientRect().width,0);const available=e.clientWidth-68;
   if(total>available){const old=parseFloat(getComputedStyle(e).fontSize);const size=old*available/total;e.style.fontSize=`${size}px`;res.push({eq:e.previousElementSibling?.querySelector('a')?.id,sizePt:size*.75});}
  }return res;
 });
 const after=await page.evaluate(()=>({math:[...document.querySelectorAll('annotation')].map(e=>e.closest('.eq,.equation')?.dataset.originalTex||e.textContent),numbers:[...document.querySelectorAll('.sci')].map(e=>e.dataset.value),figures:document.querySelectorAll('figure').length,broken:[...document.images].filter(i=>!i.naturalWidth).length,overflows:[...document.querySelectorAll('table,figure,.eq')].filter(e=>e.scrollWidth>e.clientWidth+2).map(e=>({tag:e.tagName,width:e.scrollWidth,available:e.clientWidth}))}));
 if(JSON.stringify(before.math)!==JSON.stringify(after.math)||JSON.stringify(before.numbers)!==JSON.stringify(after.numbers)||after.broken||before.figures!==after.figures)throw Error('Content preservation failed');
 const html=path.join(out,`DLW_paper_${label}.html`);fs.writeFileSync(html,'<!doctype html>\n'+await page.content());
 fs.writeFileSync(path.join(root,'report',`dlw_paper_${lang==='en'?'en':'zh'}_print.html`),'<!doctype html>\n'+await page.content());
 const pdf=path.join(out,`DLW_paper_${label}.pdf`);
 await page.pdf({path:pdf,format:'A4',preferCSSPageSize:true,printBackground:true,displayHeaderFooter:true,headerTemplate:'<span></span>',footerTemplate:'<div style="width:100%;text-align:center;font:9px Times New Roman;color:#000"><span class="pageNumber"></span></div>',margin:{top:'23mm',bottom:'22mm',left:'23mm',right:'23mm'},tagged:true});
 results.push({language:lang,pdf,mathItems:before.math.length,figures:after.figures,tableValues:after.numbers.length,fitted,overflows:after.overflows});
 await page.close();
}
await browser.close();fs.writeFileSync(path.join(out,'validation.json'),JSON.stringify(results,null,2));console.log(JSON.stringify(results,null,2));
})();
