const fs=require('fs'),path=require('path');
const {chromium}=require('C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const {pathToFileURL}=require('url');
const root='C:/Users/msz/aca';
const old=fs.readFileSync(path.join(root,'Workspaces/dlw_paper_20261009/pdf_edition_20261015/build_pdf.cjs'),'utf8');
const css=old.match(/const css = `([\s\S]*?)`;/)[1]+`\n.profile-pair img{max-height:none!important;object-fit:fill} .profile-pair>div{break-inside:avoid} .eq{overflow:visible!important} main{padding:0!important} article{background:white!important;box-shadow:none!important} table{overflow-wrap:anywhere} table.comparison th,table.comparison td{padding:3pt 2pt!important} p.table-heading{break-after:avoid!important} figure{margin:4pt 0 6pt!important} figcaption{margin-top:4pt!important} figure.spatial-error img{width:88%!important;max-height:none!important} `;
(async()=>{
const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});let results=[];
for(const [id,label,lang] of [['english','English','en']]){
 const page=await browser.newPage();await page.goto(pathToFileURL(root+'/report/dlw_paper_draft.html').href);
 const before=await page.locator('#'+id).innerText();
 await page.evaluate(()=>{for(const f of document.querySelectorAll('figure'))if(/(?:A|B|C|D)_errors3d\.png/.test(f.querySelector('img')?.src||''))f.classList.add('spatial-error');});
 await page.evaluate(({id,css,lang})=>{
 const a=document.getElementById(id);for(const p of a.querySelectorAll(':scope > p'))if(/^(Table|表)\s*\d/.test(p.textContent))p.classList.add('table-heading');document.querySelector('main').replaceChildren(a);document.querySelector('.language-nav')?.remove();document.documentElement.lang=lang;
 document.head.appendChild(Object.assign(document.createElement('style'),{textContent:css}));
 for(const i of document.images){i.loading='eager';i.src=new URL(i.getAttribute('src'),document.baseURI).href;}
 let abstract=false;for(const p of a.children){if(p.tagName!=='P')continue;if(/^(Abstract|摘要)/.test(p.textContent))abstract=true;if(/^(Keywords|关键词)/.test(p.textContent)){abstract=false;p.classList.add('keywords');}if(abstract)p.classList.add('abstract');if(/^\[\d+\]/.test(p.textContent))p.classList.add('ref');}
 },{id,css,lang});
 await page.emulateMedia({media:'print'});await page.evaluate(async()=>{await document.fonts.ready;await Promise.all([...document.images].map(i=>i.decode()));});
 const fitted=await page.evaluate(()=>{let r=[];for(const e of document.querySelectorAll('.eq')){const h=e.querySelector('.katex-html');if(!h)continue;const bs=[...h.children].filter(x=>x.classList.contains('katex-base'));const w=bs.reduce((s,b)=>s+b.getBoundingClientRect().width,0),max=e.clientWidth-65;if(w>max){const size=parseFloat(getComputedStyle(e).fontSize)*max/w;e.style.fontSize=size+'px';r.push(size);}}return r;});
 if(before!==await page.locator('#'+id).innerText())throw Error('Text changed');
 fs.writeFileSync(path.join(__dirname,`DLW_paper_${label}.html`),await page.content());
 await page.pdf({path:path.join(__dirname,`DLW_paper_${label}_layout_trial.pdf`),format:'A4',preferCSSPageSize:true,printBackground:true,displayHeaderFooter:true,headerTemplate:'<span></span>',footerTemplate:'<div style="width:100%;text-align:center;font:9px Times New Roman"><span class="pageNumber"></span></div>',tagged:true});
 results.push({label,fitted,figures:await page.locator('figure').count(),equations:await page.locator('.eq').count(),textPreserved:true});await page.close();
}await browser.close();fs.writeFileSync(path.join(__dirname,'validation.json'),JSON.stringify(results,null,2));console.log(results);
})();
