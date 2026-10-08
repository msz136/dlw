const fs=require('node:fs');
const path=require('node:path');
const {pathToFileURL}=require('node:url');
const {chromium}=require('C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
  const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
  const context=await browser.newContext({offline:true,javaScriptEnabled:false});
  const specs=[{name:'dlw_numerical.html',cells:33,key:5,full:17,math:117,appendix:true},{name:'dlw_integrability.html',cells:15,key:1,full:0,math:88,appendix:false,major:5}];
  const results=[];
  for(const spec of specs){
    const page=await context.newPage({viewport:{width:1440,height:1080}});
    await page.setViewportSize({width:1440,height:1080});
    const failed=[],remote=[],errors=[];
    page.on('requestfailed',r=>failed.push({url:r.url(),reason:r.failure()?.errorText}));
    page.on('request',r=>{if(/^https?:/.test(r.url()))remote.push(r.url());});
    page.on('pageerror',e=>errors.push(String(e)));
    const url=pathToFileURL(path.resolve(__dirname,'../..',spec.name)).href;
    await page.goto(url);
    await page.evaluate(()=>document.fonts.ready);
    const inspect=()=>page.evaluate(()=>({
      title:document.querySelector('h1').innerText,
      cells:document.querySelectorAll('main [data-cell]').length,
      majorSections:document.querySelectorAll('main>section.theory-stage').length,
      tocLinks:document.querySelectorAll('nav a').length,
      minorHeadings:document.querySelectorAll('h3,h4').length,
      key:document.querySelectorAll('.key-code').length,
      full:document.querySelectorAll('.code-appendix:not([open]) .full-source').length,
      math:document.querySelectorAll('.katex').length,
      mathErrors:document.querySelectorAll('.katex-error').length,
      rawMath:[...document.querySelectorAll('p,td')].filter(x=>/\$\$|\\[\[\]]/.test(x.innerText)).length,
      pageOverflow:document.documentElement.scrollWidth>innerWidth+1,
      brokenImages:[...document.images].filter(x=>!x.complete||!x.naturalWidth).length,
      missingAnchors:[...document.querySelectorAll('nav a')].filter(x=>!document.getElementById(x.hash.slice(1))).length,
      duplicateIds:[...document.querySelectorAll('[id]')].map(x=>x.id).filter((x,i,a)=>a.indexOf(x)!==i),
      fonts:document.fonts.size,fontErrors:[...document.fonts].filter(x=>x.status==='error').map(x=>x.family),
      bodyFont:getComputedStyle(document.body).fontFamily,mathFont:getComputedStyle(document.querySelector('.katex')).fontFamily,
      controls:document.querySelectorAll('script,button,input,textarea,iframe').length
      ,disclosures:document.querySelectorAll('details,summary').length
      ,outputs:document.querySelectorAll('.compiler-output,.output').length
    }));
    const desktop=await inspect();
    await page.screenshot({path:path.join(__dirname,spec.name.replace('.html','_1440.png'))});
    if(spec.name==='dlw_integrability.html'){
      await page.locator('#conservation-text').scrollIntoViewIfNeeded();
      await page.screenshot({path:path.join(__dirname,'integrability_conservation_1440.png')});
      await page.locator('#lean-endpoint').scrollIntoViewIfNeeded();
      await page.screenshot({path:path.join(__dirname,'integrability_endpoint_1440.png')});
    }
    await page.setViewportSize({width:390,height:844});
    await page.evaluate(()=>scrollTo(0,0));
    const mobile=await inspect();
    await page.screenshot({path:path.join(__dirname,spec.name.replace('.html','_390.png'))});
    await page.setViewportSize({width:794,height:1123});
    await page.emulateMedia({media:'print'});
    const print=await inspect();
    await page.emulateMedia({media:'screen'});
    let appendixOpen=false;
    if(spec.appendix){
      await page.locator('.code-appendix summary').click();
      appendixOpen=await page.locator('.code-appendix').getAttribute('open')!==null;
    }
    const passed=[desktop,mobile,print].every(x=>x.cells===spec.cells&&x.key===spec.key&&x.full===spec.full&&x.math===spec.math&&!x.mathErrors&&!x.rawMath&&!x.pageOverflow&&!x.brokenImages&&!x.missingAnchors&&!x.duplicateIds.length&&x.fonts===20&&!x.fontErrors.length&&x.bodyFont.includes('SimSun')&&x.mathFont.includes('KaTeX_Main')&&!x.controls&&(spec.appendix||(!x.disclosures&&!x.outputs))&&(!spec.major||(x.majorSections===spec.major&&x.tocLinks===spec.major&&!x.minorHeadings)))&&appendixOpen===spec.appendix&&!failed.length&&!remote.length&&!errors.length;
    results.push({file:spec.name,passed,desktop,mobile,print,appendixOpen,failed,remote,errors});
    await page.close();
  }
  // Font diagnostics run separately from page-load checks.
  const fontPage=await context.newPage();
  await fontPage.goto(pathToFileURL(path.resolve(__dirname,'../../dlw_integrability.html')).href);
  await fontPage.evaluate(()=>document.fonts.ready);
  const cdp=await context.newCDPSession(fontPage);
  await cdp.send('DOM.enable');await cdp.send('CSS.enable');
  const {root}=await cdp.send('DOM.getDocument');
  const usedFonts={};
  for(const [name,selector] of Object.entries({body:'#intro>p',math:'.katex .mathnormal'})){
    const {nodeId}=await cdp.send('DOM.querySelector',{nodeId:root.nodeId,selector});
    usedFonts[name]=(await cdp.send('CSS.getPlatformFontsForNode',{nodeId})).fonts;
  }
  const success=results.every(x=>x.passed)&&usedFonts.math.some(x=>x.isCustomFont&&x.familyName.includes('KaTeX'))&&usedFonts.body.some(x=>x.familyName==='SimSun');
  const result={success,offline:true,javaScriptDisabled:true,reports:results,usedFonts};
  fs.writeFileSync(path.join(__dirname,'browser_validation.json'),JSON.stringify(result,null,2)+'\n');
  console.log(JSON.stringify({success,reports:results.map(x=>({file:x.file,passed:x.passed,math:x.desktop.math,code:x.desktop.key})),usedFonts}));
  await browser.close();
  if(!success)process.exitCode=1;
})();
