const fs = require('fs');
const path = require('path');
const {pathToFileURL} = require('url');
const {chromium} = require('C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');

(async () => {
  const root = path.resolve(__dirname, '../..');
  const target = path.join(root, 'report', 'soliton_reading_guide.html');
  const browser = await chromium.launch({headless: true, executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe'});
  const results = [];
  for (const width of [1280, 390]) {
    const page = await browser.newPage({viewport: {width, height: 1050}, deviceScaleFactor: 1});
    await page.goto(pathToFileURL(target).href);
    const result = await page.evaluate(() => ({
      title: document.title,
      language: document.documentElement.lang,
      pageOverflow: document.documentElement.scrollWidth > innerWidth,
      headings: [...document.querySelectorAll('h1,h2')].map(x => x.textContent),
      links: [...document.querySelectorAll('a')].map(x => x.getAttribute('href')),
      tableRows: document.querySelectorAll('tbody tr').length,
      content: document.body.innerText
    }));
    if (result.pageOverflow) throw new Error(`Page overflow at ${width}`);
    for (const link of result.links) {
      const [filename, fragment] = link.split('#');
      if (!fs.existsSync(path.resolve(path.dirname(target), filename))) throw new Error(`Missing link: ${link}`);
      if (fragment?.startsWith('page=')) {
        const p = Number(fragment.slice(5));
        const pageCount = filename.endsWith('ctp8805.pdf') ? 6 : 202;
        if (!(p >= 1 && p <= pageCount)) throw new Error(`Invalid PDF page: ${p}`);
      }
    }
    if (!result.content.includes('156–157') || !result.content.includes('Darboux')) throw new Error('Missing key reading information');
    await page.screenshot({path: path.join(__dirname, `guide_${width}.png`), fullPage: true});
    delete result.content;
    results.push({width, ...result});
    await page.close();
  }
  await browser.close();
  fs.writeFileSync(path.join(__dirname, 'html_validation.json'), JSON.stringify({passed: true, results}, null, 2));
  console.log(JSON.stringify({passed: true, widths: results.map(x => x.width), links: results[0].links.length}));
})().catch(e => { console.error(e); process.exit(1); });
