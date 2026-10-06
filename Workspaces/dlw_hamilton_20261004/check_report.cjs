const fs=require('fs'),path=require('path');
const {chromium}=require('C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
  const root=path.resolve(__dirname,'../..');
  const manifest=JSON.parse(fs.readFileSync(path.join(__dirname,'build_manifest.json'),'utf8'));
  const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
  const page=await browser.newPage();
  const rows=[];
  for(const width of [1440,390]){
    await page.setViewportSize({width,height:1000});
    await page.goto('file:///'+path.join(root,'dlw_hamilton.html').replaceAll('\\','/'));
    rows.push(await page.evaluate(()=>({width:innerWidth,overflow:document.documentElement.scrollWidth>innerWidth,
      math:document.querySelectorAll('math').length,
      unrendered:document.body.textContent.includes('@@M'),
      equationScrolls:[...document.querySelectorAll('.equation')].filter(e=>e.scrollWidth>e.clientWidth+2).length,
      links:[...document.querySelectorAll('a')].map(a=>a.getAttribute('href')),
      anchors:[...document.querySelectorAll('[id]')].map(a=>a.id)})));
    await page.screenshot({path:path.join(__dirname,`report_top_${width}.png`)});
    await page.locator('h2').nth(4).scrollIntoViewIfNeeded();
    await page.screenshot({path:path.join(__dirname,`report_physical_${width}.png`)});
    await page.locator('h2').nth(9).scrollIntoViewIfNeeded();
    await page.screenshot({path:path.join(__dirname,`report_nonperiodic_${width}.png`)});
  }
  for(const row of rows){
    if(row.overflow||row.math!==manifest.math_blocks||row.unrendered)throw Error('Math/layout failed');
    for(const href of row.links){
      if(href.startsWith('#')){
        if(!row.anchors.includes(href.slice(1)))throw Error('Missing anchor '+href);
      }else if(!fs.existsSync(path.join(root,href)))throw Error('Missing reference '+href);
    }
  }
  fs.writeFileSync(path.join(__dirname,'html_validation.json'),JSON.stringify({passed:true,rows},null,2));
  await browser.close();
  console.log(JSON.stringify({passed:true,math_blocks:manifest.math_blocks,rows:rows.map(r=>({width:r.width,overflow:r.overflow,equationScrolls:r.equationScrolls}))}));
})().catch(e=>{console.error(e);process.exitCode=1});
