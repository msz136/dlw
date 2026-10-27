const {chromium}=require('C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs');
(async()=>{
 const browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
 const page=await browser.newPage({viewport:{width:1200,height:900}});
 await page.goto('file:///C:/Users/msz/aca/dlw-paper.html');
 await page.evaluate(async()=>{await document.fonts.ready;document.querySelectorAll('img').forEach(i=>i.loading='eager');await Promise.all([...document.images].map(i=>i.decode().catch(()=>{})))});
 const base='C:/Users/msz/aca/Workspaces/dlw_paper_20261009/fe_comparison_20261027/';
 for(const [id,file] of [['#fe-formulation','algorithm.png'],['#table-final','table.png']])await page.locator(id).screenshot({path:base+file});
 const state=await page.evaluate(()=>({brokenImages:[...document.images].filter(i=>!i.complete||!i.naturalWidth).map(i=>i.src),mathErrors:document.querySelectorAll('.katex-error').length,tableWidth:document.querySelector('#table-final').getBoundingClientRect().width,bodyWidth:document.body.getBoundingClientRect().width,formulaWidths:[...document.querySelectorAll('#fe-formulation .katex-display')].map(e=>({width:e.clientWidth,scrollWidth:e.scrollWidth}))}));
 fs.writeFileSync(base+'layout_validation.json',JSON.stringify(state,null,2));console.log(state);await browser.close();
})();
