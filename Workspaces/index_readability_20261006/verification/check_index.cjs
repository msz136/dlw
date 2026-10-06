/* Read-only verification of index.html, using Edge headless and exact CSV values. */
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const {pathToFileURL} = require('node:url');
const {chromium} = require('C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');

const out = __dirname;
const root = path.resolve(out, '../../..');
const target = path.join(root, 'index.html');
const before = path.join(root, 'Workspaces/index_readability_20261006/before/index.html');
const dataFiles = [
  'Workspaces/dlw_single_aligned_20260929/out/index_t001.csv',
  'Workspaces/dlw_sd2_uv_init_20260929/out/comparison.csv'
];
const csv = file => {
  const lines = fs.readFileSync(path.join(root, file), 'utf8').replace(/^\uFEFF/, '').trim().split(/\r?\n/);
  const keys = lines.shift().split(',');
  return lines.map(line => Object.fromEntries(line.split(',').map((v, i) => [keys[i], v])));
};
const exact = new Map();
for (const file of dataFiles) {
  for (const row of csv(file)) {
    if (Number(row.t) !== .01 || !['fig1a','fig1b','fig3'].includes(row.case)) continue;
    exact.set(`${row.case}|${row.method}|${row.mesh}`, row);
  }
}
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const failures = [], notes = [], screenshots = [];
function requireCheck(ok, label, details) {
  if (!ok) failures.push({label, details});
}

(async () => {
  fs.mkdirSync(out, {recursive:true});
  requireCheck(exact.size === 12, 'CSV has the 12 comparison combinations', {rows:exact.size});
  if (!fs.existsSync(before)) throw new Error(`Missing original backup: ${before}`);
  const source = fs.readFileSync(target, 'utf8');
  const original = fs.readFileSync(before, 'utf8');
  const browser = await chromium.launch({
    executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
    headless:true
  });
  const page = await browser.newPage({viewport:{width:1280,height:1050}});
  const errors = [], failedRequests = [];
  page.on('pageerror', err => errors.push(String(err)));
  page.on('requestfailed', request => failedRequests.push({url:request.url().slice(0,180),error:request.failure()?.errorText}));
  await page.goto(pathToFileURL(target).href);
  await page.waitForFunction(() => document.querySelectorAll('.katex').length > 0);
  await page.evaluate(() => document.fonts.ready);

  const sourceChecks = await page.evaluate(({source,original}) => {
    const parse = html => new DOMParser().parseFromString(html, 'text/html');
    const formulae = dom => [...dom.querySelectorAll('.equation')].map(el => el.textContent.replace(/\s+/g,''));
    const currentDom = parse(source), beforeDom = parse(original);
    const current = formulae(currentDom), prior = formulae(beforeDom);
    const nums = current.map(tex => Number(tex.match(/\\tag\{(\d+)\}/)?.[1]));
    const changed = current.map((value,i) => value === prior[i] ? null : i+1).filter(Boolean);
    const collectTable = table => {
      const grid = [];
      [...table.querySelectorAll('tbody tr')].forEach((tr,r) => {
        grid[r] ??= [];
        let c=0;
        for (const cell of tr.cells) {
          while(grid[r][c]) c++;
          const info = {
            text:cell.textContent.replace(/\s+/g,' ').trim(),
            error:cell.hasAttribute('data-error') ? Number(cell.dataset.error) : null,
            strong:!!cell.querySelector('strong,b'),
            raw:cell.getAttribute('data-error'),
            rowSpan:cell.rowSpan,
            colSpan:cell.colSpan
          };
          for(let rr=r;rr<r+cell.rowSpan;rr++) {
            grid[rr] ??= [];
            for(let cc=c;cc<c+cell.colSpan;cc++) grid[rr][cc]=info;
          }
          c+=cell.colSpan;
        }
      });
      return {
        id:table.id,
        headers:[...table.querySelectorAll('thead th')].map(th=>th.textContent.replace(/\s+/g,' ').trim()),
        rows:grid
      };
    };
    return {
      equations:{currentCount:current.length,beforeCount:prior.length,numbers:nums,changed},
      tables:[...currentDom.querySelectorAll('table')].map(collectTable),
      dataErrorCells:currentDom.querySelectorAll('td[data-error]').length,
      strongErrorCells:currentDom.querySelectorAll('td[data-error] strong,td[data-error] b').length,
      sourceFigures:currentDom.querySelectorAll('figure').length,
      mainSourceText:currentDom.querySelector('main').textContent
    };
  }, {source,original});
  requireCheck(sourceChecks.equations.currentCount===16, '16 display formulas', sourceChecks.equations);
  requireCheck(sourceChecks.equations.beforeCount===16, 'Backup has 16 display formulas', sourceChecks.equations);
  requireCheck(sourceChecks.equations.changed.length===0, 'Display formulas unchanged', sourceChecks.equations.changed);
  requireCheck(sourceChecks.equations.numbers.every((n,i)=>n===i+1), 'Formula numbers are 1 through 16', sourceChecks.equations.numbers);
  requireCheck(sourceChecks.tables.length===5, 'Five tables', sourceChecks.tables.length);
  requireCheck(sourceChecks.dataErrorCells===90, '90 comparison numeric cells', sourceChecks.dataErrorCells);
  requireCheck(sourceChecks.strongErrorCells===42, '42 best comparison results are bold', sourceChecks.strongErrorCells);

  const mappedCases = {'A':'fig1a','B':'fig1b','C':'fig3'};
  const checkedCells = [], checkedRows = [];
  function identify(row, withModel) {
    const labels = row.filter(cell=>cell.error===null).map(cell=>cell.text.replace(/\$/g,''));
    const text = labels.join(' ');
    const caseMatch = text.match(/(?:算例|孤子)?\s*([ABC])\b/);
    const modelMatch = text.match(/\b(SD2|SD|FD)\b/);
    const fieldMatch = labels.find(text=>/^\s*[uv]\s*$/.test(text));
    return {case:caseMatch&&mappedCases[caseMatch[1]], model:withModel&&modelMatch?.[1], field:fieldMatch?.trim()};
  }
  const expectedRows = {3:6,4:18,5:18};
  for (let n=3;n<=5;n++) {
    const table = sourceChecks.tables.find(table=>table.id===`table-${n}`) ?? sourceChecks.tables[n-1];
    requireCheck(table.rows.length===expectedRows[n], `Table ${n} logical rows`, table.rows.length);
    const uniqueness = new Set();
    for (let r=0;r<table.rows.length;r++) {
      const row=table.rows[r], id=identify(row,n!==3), numeric=row.filter(cell=>cell.error!==null);
      requireCheck(numeric.length === (n===3?3:2), `Table ${n} row ${r+1} numeric columns`, numeric.length);
      requireCheck(id.case&&id.field&&(n===3||id.model), `Table ${n} row ${r+1} labels`, id);
      if (!id.case||!id.field||(n!==3&&!id.model)) continue;
      const key=`${id.case}|${id.model||'all'}|${id.field}`;
      requireCheck(!uniqueness.has(key), `Table ${n} unique row`, key);
      uniqueness.add(key);
      const expected = n===3
        ? ['SD','SD2','FD'].map(model=>Number(exact.get(`${id.case}|RK4|fixed`)[`${model}_${id.field}`]))
        : n===4
          ? ['Euler','RK4'].map(method=>Number(exact.get(`${id.case}|${method}|fixed`)[`${id.model}_${id.field}`]))
          : ['fixed','moving'].map(mesh=>Number(exact.get(`${id.case}|RK4|${mesh}`)[`${id.model}_${id.field}`]));
      for (let c=0;c<numeric.length;c++) {
        const cell=numeric[c];
        const equal=cell.error===expected[c];
        requireCheck(equal, `Table ${n} row ${r+1} column ${c+1} equals original CSV`, {id,actual:cell.error,expected:expected[c]});
        const label=cell.error.toExponential(3).replace('e-0','e-').replace('e+0','e+');
        const displayed=cell.text.replace(/[−–]/g,'-').replace(/†/g,'').trim();
        // The display format is checked independently of the full-precision value.
        const parsedDisplay=Number(displayed);
        requireCheck(Number.isFinite(parsedDisplay), `Table ${n} numeric display parses`, cell.text);
        requireCheck(parsedDisplay===Number(cell.error.toExponential(3)), `Table ${n} display is correctly rounded`, {displayed,expected:label});
        checkedCells.push({table:n,row:r+1,column:c+1,...id,value:cell.error,display:cell.text,equalsCSV:equal,bold:cell.strong});
      }
      const minimum = Math.min(...expected);
      requireCheck(numeric.every((cell,i)=>cell.strong===(expected[i]===minimum)), `Table ${n} row ${r+1} bold marks exact minimum`, {id,expected,bold:numeric.map(cell=>cell.strong)});
      checkedRows.push({table:n,row:r+1,...id,bestColumn:expected.indexOf(minimum)+1});
    }
    requireCheck(uniqueness.size===expectedRows[n], `Table ${n} complete comparison rows`, uniqueness.size);
  }

  async function inspectSurface() {
    return page.evaluate(() => {
      const main=document.querySelector('main');
      return {
        width:innerWidth,
        scrollWidth:document.documentElement.scrollWidth,
        overflow:document.documentElement.scrollWidth>innerWidth,
        tables:document.querySelectorAll('table').length,
        math:document.querySelectorAll('.katex').length,
        displayMath:document.querySelectorAll('.katex-display').length,
        mathErrors:[...document.querySelectorAll('.katex-error')].map(el=>el.textContent),
        rawDollars:(main.innerText.match(/\$/g)||[]).length,
        headings:[...main.querySelectorAll('h1,h2,h3')].map(el=>el.textContent),
        links:[...main.querySelectorAll('a')].map(el=>({href:el.getAttribute('href'),text:el.textContent})),
        images:[...main.querySelectorAll('img')].map(el=>{
          const full=el.getAttribute('src')||'',comma=full.indexOf(','),embedded=full.startsWith('data:');
          const payload=embedded?full.slice(comma+1):'';
          return {src:embedded?full.slice(0,comma):full,byteLength:embedded?Math.floor(payload.length*3/4)-(payload.match(/=+$/)?.[0].length||0):null,alt:el.getAttribute('alt'),width:el.naturalWidth,height:el.naturalHeight,complete:el.complete};
        }),
        bestResultWeights:[...main.querySelectorAll('td[data-error] strong,td[data-error] b')].map(el=>Number(getComputedStyle(el).fontWeight)),
        overflowElements:[...main.querySelectorAll('*')].filter(el=>{
          const rect=el.getBoundingClientRect();
          return rect.right>innerWidth+1 && !el.closest('.katex-display,.table-wrap,pre');
        }).slice(0,8).map(el=>({tag:el.tagName,class:el.className,right:el.getBoundingClientRect().right})),
        defensivePhrases:['不能据此认为','不能由','不构成','不将','未通过','仅描述主配置'].filter(term=>main.innerText.includes(term))
      };
    });
  }
  for (const image of await page.locator('main img').all()) {
    await image.scrollIntoViewIfNeeded();
    const decoded = await image.evaluate(async el=>{
      const full=el.getAttribute('src')||'',comma=full.indexOf(','),embedded=full.startsWith('data:');
      const payload=embedded?full.slice(comma+1):'';
      const metadata={src:embedded?full.slice(0,comma):full,byteLength:embedded?Math.floor(payload.length*3/4)-(payload.match(/=+$/)?.[0].length||0):null};
      try {await el.decode();return {ok:true,...metadata,alt:el.alt,width:el.naturalWidth,height:el.naturalHeight};}
      catch(err){return {ok:false,...metadata,error:String(err)};}
    });
    requireCheck(decoded.ok&&decoded.width>0&&decoded.height>0, 'Image decodes', decoded);
    notes.push({decodedImage:decoded});
  }
  await page.evaluate(()=>scrollTo(0,0));
  const desktop=await inspectSurface();
  const screenshot=async(name,locator) => {
    const file=path.join(out,name+'.png');
    if(locator) await locator.screenshot({path:file}); else await page.screenshot({path:file});
    screenshots.push(path.relative(root,file).replace(/\\/g,'/'));
  };
  await screenshot('desktop_top');
  await page.locator('#table-3').evaluate(el=>el.closest('.table-wrap').previousElementSibling.scrollIntoView());
  await screenshot('desktop_results');
  await screenshot('table_3',page.locator('#table-3').locator('..'));
  await screenshot('table_4',page.locator('#table-4').locator('..'));
  await screenshot('table_5',page.locator('#table-5').locator('..'));
  const pairs = page.locator('.error-curve-pair');
  const pairCount=await pairs.count();
  if(pairCount) {
    for(let i=0;i<pairCount;i++) await screenshot(`desktop_curves_${i+1}`,pairs.nth(i));
  } else {
    const figs=page.locator('figure');
    for(let i=0;i<await figs.count();i++) await screenshot(`desktop_curve_${i+1}`,figs.nth(i));
  }
  await page.setViewportSize({width:390,height:844});
  await page.evaluate(()=>scrollTo(0,0));
  const mobile=await inspectSurface();
  await screenshot('mobile_top');
  await page.locator('#table-3').scrollIntoViewIfNeeded();
  await screenshot('mobile_results');
  await page.locator('figure').first().scrollIntoViewIfNeeded();
  await screenshot('mobile_curves');

  const linkChecks=[];
  for(const link of desktop.links) {
    const href=link.href;
    if(!href || /^(https?:|mailto:|data:|javascript:)/i.test(href)) continue;
    const url=new URL(href,pathToFileURL(target).href);
    if(url.protocol!=='file:') continue;
    const filename=decodeURIComponent(url.pathname).replace(/^\/([A-Za-z]:)/,'$1');
    const exists=fs.existsSync(filename);
    let anchorExists=true;
    if(url.hash && filename.replace(/\\/g,'/')===target.replace(/\\/g,'/')) {
      anchorExists=await page.evaluate(id=>!!document.getElementById(id),decodeURIComponent(url.hash.slice(1)));
    }
    linkChecks.push({href,exists,anchorExists});
    requireCheck(exists&&anchorExists, 'Local link exists', {href,exists,anchorExists});
  }
  for (const surface of [desktop,mobile]) {
    requireCheck(!surface.overflow, `${surface.width}px page has no horizontal overflow`, surface.overflowElements);
    requireCheck(!surface.mathErrors.length, `${surface.width}px no KaTeX errors`, surface.mathErrors);
    requireCheck(!surface.rawDollars, `${surface.width}px no visible unrendered math delimiters`, surface.rawDollars);
    requireCheck(surface.displayMath===16, `${surface.width}px 16 formulas rendered`, surface.displayMath);
    requireCheck(surface.images.length===12, `${surface.width}px 12 curve images`, surface.images.length);
    requireCheck(surface.images.every(image=>image.alt?.trim()), `${surface.width}px all images have alt text`, surface.images);
    requireCheck(surface.bestResultWeights.length===42&&surface.bestResultWeights.every(weight=>weight===700), `${surface.width}px 42 best results render at font weight 700`, surface.bestResultWeights);
    requireCheck(surface.defensivePhrases.length===0, `${surface.width}px no removed defensive phrases`, surface.defensivePhrases);
  }
  requireCheck(!errors.length, 'No page JavaScript errors', errors);
  requireCheck(!failedRequests.length, 'No failed browser requests', failedRequests);
  const result={
    checkedAt:new Date().toISOString(),
    source:{html:target,sha256:sha(target),backup:before,backupSha256:sha(before),csv:dataFiles.map(file=>({file,sha256:sha(path.join(root,file))}))},
    passed:failures.length===0,
    summary:{tables:sourceChecks.tables.length,formulas:sourceChecks.equations.currentCount,formulaChanges:sourceChecks.equations.changed.length,exactNumericCells:checkedCells.length,bestResults:sourceChecks.strongErrorCells,images:desktop.images.length,desktopOverflow:desktop.overflow,mobileOverflow:mobile.overflow},
    sourceChecks:{equations:sourceChecks.equations,dataErrorCells:sourceChecks.dataErrorCells,strongErrorCells:sourceChecks.strongErrorCells},
    desktop,mobile,checkedRows,checkedCells,linkChecks,errors,failedRequests,notes,screenshots,failures
  };
  fs.writeFileSync(path.join(out,'validation.json'),JSON.stringify(result,null,2));
  console.log(JSON.stringify({passed:result.passed,summary:result.summary,failures,screenshots},null,2));
  await browser.close();
  if(failures.length)process.exitCode=1;
})().catch(err=>{console.error(err);process.exitCode=1;});
