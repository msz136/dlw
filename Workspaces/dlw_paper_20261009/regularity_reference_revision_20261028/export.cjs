const {chromium}=require('C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
 const p=await b.newPage();
 await p.goto('file:///C:/Users/msz/aca/dlw-paper.html',{waitUntil:'networkidle'});
 await p.evaluate(async()=>{document.querySelectorAll('img').forEach(i=>i.loading='eager');await document.fonts.ready;await Promise.all([...document.images].map(i=>i.decode().catch(()=>{})))});
 await p.pdf({path:'C:/Users/msz/aca/Workspaces/dlw_paper_20261009/regularity_reference_revision_20261028/print-review.pdf',format:'A4',preferCSSPageSize:true,printBackground:true,displayHeaderFooter:false,margin:{top:'10mm',bottom:'10mm',left:'10mm',right:'10mm'}});
 await b.close();
})();
