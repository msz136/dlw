const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {chromium} = require('C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const manifest=JSON.parse(fs.readFileSync(path.join(__dirname,'build_validation.json'),'utf8'));
(async()=>{
  const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
  const context=await browser.newContext({offline:true,javaScriptEnabled:false});
  const page=await context.newPage();
  const requests=[],errors=[],failed=[];
  page.on('request',r=>{if(/^https?:/.test(r.url()))requests.push(r.url());});
  page.on('requestfailed',r=>failed.push({url:r.url(),reason:r.failure()?.errorText}));
  page.on('pageerror',e=>errors.push(String(e)));
  await page.setViewportSize({width:1440,height:1080});
  await page.goto(pathToFileURL(path.resolve(__dirname,'../../dlw_numerical.html')).href);
  await page.evaluate(()=>document.fonts.ready);
  const inspect=()=>page.evaluate(()=>({
    h1:document.querySelector('h1').innerText,
    cells:document.querySelectorAll('main > section[data-cell]').length,
    code:document.querySelectorAll('.key-code').length,
    codeElements:document.querySelectorAll('main code,main pre,.code-caption').length,
    codeLines:[...document.querySelectorAll('.key-code code')].reduce((n,x)=>n+x.textContent.split('\n').length,0),
    fullCode:document.querySelectorAll('.full-source').length,
    appendices:document.querySelectorAll('.code-appendix,details,summary').length,
    sections:document.querySelectorAll('h2').length,
    tocLinks:document.querySelectorAll('nav a').length,
    lastCell:document.querySelector('main > section:last-child').dataset.cell,
    math:document.querySelectorAll('.katex').length,
    mathErrors:document.querySelectorAll('.katex-error').length,
    images:[...document.images].map(x=>({width:x.naturalWidth,height:x.naturalHeight,loaded:x.complete&&x.naturalWidth>0})),
    tables:document.querySelectorAll('table').length,
    tableRules:[...document.querySelectorAll('table')].map(table=>{
      const edge=(node,side)=>parseFloat(getComputedStyle(node)['border'+side+'Width']);
      return {
        id:table.id,
        headerRows:table.tHead.rows.length,
        top:edge(table,'Top'),
        headerBottom:edge(table.tHead,'Bottom'),
        bottom:edge(table,'Bottom'),
        sideBorders:edge(table,'Left')+edge(table,'Right'),
        headerOtherBorders:edge(table.tHead,'Top')+edge(table.tHead,'Left')+edge(table.tHead,'Right'),
        interiorBorders:[...table.querySelectorAll('tr,th,td,tbody,tfoot')].filter(node=>
          ['Top','Bottom','Left','Right'].some(side=>edge(node,side)>0)).length
      };
    }),
    overflow:document.documentElement.scrollWidth>innerWidth+1,
    controls:document.querySelectorAll('button,textarea,input,script').length,
    badAnchors:[...document.querySelectorAll('nav a')].filter(x=>!document.getElementById(x.hash.slice(1))).length,
    fonts:[...document.fonts].filter(x=>x.status==='error').map(x=>x.family),
    registeredFonts:document.fonts.size,
    bodyFont:getComputedStyle(document.body).fontFamily,
    mathFont:getComputedStyle(document.querySelector('.katex')).fontFamily
  }));
  const desktop=await inspect();
  await page.screenshot({path:path.join(__dirname,'report_1440.png')});
  await page.locator('#dlw-sd-text').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(__dirname,'report_sd_1440.png')});
  await page.locator('#dlw-exact-text').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(__dirname,'report_exact_1440.png')});
  await page.locator('#dlw-space-text').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(__dirname,'report_table_1440.png')});
  await page.locator('#dlw-field-plots .output').first().scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(__dirname,'report_figure_1440.png')});
  await page.setViewportSize({width:390,height:844});
  await page.evaluate(()=>scrollTo(0,0));
  const mobile=await inspect();
  await page.screenshot({path:path.join(__dirname,'report_390.png')});
  await page.locator('#dlw-sd-text').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(__dirname,'report_sd_390.png')});
  await page.locator('#dlw-space-text').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(__dirname,'report_table_390.png')});
  await page.setViewportSize({width:794,height:1123});
  await page.emulateMedia({media:'print'});
  const print=await inspect();
  await page.locator('#dlw-sd-text').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(__dirname,'report_sd_print.png')});
  await page.locator('#dlw-time-text').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(__dirname,'report_time_print.png')});
  await page.locator('#dlw-space-text').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(__dirname,'report_table_print.png')});
  await page.emulateMedia({media:'screen'});
  await page.setViewportSize({width:1440,height:1080});
  // Inspect font glyphs on a separate page: CSS.enable itself can request a
  // file-origin stylesheet source. Keep that diagnostic request out of the
  // report's ordinary resource-load check.
  const fontPage=await context.newPage();
  await fontPage.goto(pathToFileURL(path.resolve(__dirname,'../../dlw_numerical.html')).href);
  await fontPage.evaluate(()=>document.fonts.ready);
  const cdp=await context.newCDPSession(fontPage);
  await cdp.send('DOM.enable');
  await cdp.send('CSS.enable');
  const {root}=await cdp.send('DOM.getDocument');
  const usedFonts={};
  for(const [label,selector] of Object.entries({body:'#dlw-title > p',math:'.katex .mathnormal'})){
    const {nodeId}=await cdp.send('DOM.querySelector',{nodeId:root.nodeId,selector});
    usedFonts[label]=(await cdp.send('CSS.getPlatformFontsForNode',{nodeId})).fonts;
  }
  await fontPage.close();
  const success=[desktop,mobile,print].every(x=>!x.overflow&&!x.mathErrors&&!x.controls&&!x.codeElements&&!x.badAnchors&&!x.fonts.length&&x.registeredFonts>=20&&x.mathFont.includes('KaTeX_Main')&&x.bodyFont.includes('SimSun')&&x.math===manifest.math_expressions&&x.cells===manifest.cells&&x.code===manifest.visible_code_excerpts&&x.codeLines===manifest.visible_code_lines&&!x.fullCode&&!x.appendices&&x.sections===7&&!x.tocLinks&&x.lastCell==='dlw-field-plots'&&x.images.length===manifest.image_outputs&&x.images.every(y=>y.loaded)&&x.tables===5&&x.tableRules.every(t=>t.top>0&&t.headerBottom>0&&t.bottom>0&&!t.sideBorders&&!t.headerOtherBorders&&!t.interiorBorders))
    &&usedFonts.math.some(x=>x.isCustomFont&&x.familyName.includes('KaTeX'))
    &&usedFonts.body.some(x=>/SimSun|宋体/.test(x.familyName))
    &&!requests.length&&!errors.length&&!failed.length;
  const result={success,offline:true,javaScriptDisabled:true,desktop,mobile,print,usedFonts,requests,errors,failed};
  fs.writeFileSync(path.join(__dirname,'browser_validation.json'),JSON.stringify(result,null,2)+'\n');
  console.log(JSON.stringify(result));
  await browser.close();
  if(!success)process.exitCode=1;
})();
