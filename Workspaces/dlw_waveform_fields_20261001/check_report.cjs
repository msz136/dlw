const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL, fileURLToPath} = require('node:url');
const {chromium} = require('C:/Users/msz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root = path.resolve(__dirname, '../..');
const targets = [
  {name: 'waveform', file: path.join(root, 'report', 'dlw_waveform_fields.html')},
  {name: 'index', file: path.join(root, 'index.html')}
];
const screenshots = path.join(__dirname, 'html_preview');
fs.mkdirSync(screenshots, {recursive: true});

async function inspect(page) {
  return page.evaluate(() => {
    const headings = [...document.querySelectorAll('h2')];
    const heading = headings.find(e => /波形|误差场分布|误差分布/.test(e.textContent));
    const contents = [];
    if (heading) {
      if (heading.closest('section')) contents.push(heading.closest('section'));
      else {
        let sibling = heading.nextElementSibling;
        while (sibling && sibling.tagName !== 'H2') {
          contents.push(sibling);
          sibling = sibling.nextElementSibling;
        }
      }
    }
    const plotFigures = contents.flatMap(e => [
      ...(e.matches('figure') ? [e] : []),
      ...e.querySelectorAll('figure')
    ]);
    const figures = [...document.querySelectorAll('figure')];
    return {
      width: innerWidth,
      title: document.title,
      language: document.documentElement.lang,
      overflow: document.documentElement.scrollWidth > innerWidth + 1,
      mathCount: document.querySelectorAll('.katex').length,
      mathErrors: [...document.querySelectorAll('.katex-error')].map(e => e.textContent),
      rawDollarCount: ((document.querySelector('main') || document.body).innerText.match(/\$/g) || []).length,
      sections: headings.map(e => ({id: e.id, title: e.textContent})),
      plotHeading: heading ? {id: heading.id, title: heading.textContent} : null,
      plotText: contents.map(e => e.innerText).join('\n'),
      plotFigures: plotFigures.map(e => ({
        caption: e.querySelector('figcaption')?.innerText || '',
        images: [...e.querySelectorAll('img')].map(i => ({
          alt: i.alt, width: i.naturalWidth, height: i.naturalHeight,
          renderedWidth: i.getBoundingClientRect().width,
          embedded: i.currentSrc.startsWith('data:'),
          decoded: i.complete && i.naturalWidth > 0
        }))
      })),
      figureCount: figures.length,
      details: [...document.querySelectorAll('details')].map(e => ({
        title: e.querySelector('summary')?.innerText || '', open: e.open,
        figures: e.querySelectorAll('figure').length
      })),
      figureCaptions: figures.map(e => e.querySelector('figcaption')?.innerText || ''),
      images: [...document.images].map(e => ({
        alt: e.alt, width: e.naturalWidth, height: e.naturalHeight,
        decoded: e.complete && e.naturalWidth > 0,
        embedded: e.currentSrc.startsWith('data:')
      })),
      links: [...document.querySelectorAll('a[href]')].map(e => e.getAttribute('href')),
      badAnchors: [...document.querySelectorAll('a[href^="#"]')]
        .map(e => e.getAttribute('href'))
        .filter(href => href.length > 1 && !document.getElementById(decodeURIComponent(href.slice(1)))),
      duplicateIds: [...new Set([...document.querySelectorAll('[id]')].map(e => e.id))]
        .filter(id => document.querySelectorAll('[id]').length && [...document.querySelectorAll('[id]')].filter(e => e.id === id).length > 1),
      scrollableTables: [...document.querySelectorAll('table')]
        .filter(e => e.scrollWidth > e.clientWidth + 1).length
    };
  });
}

(async () => {
  const missingTargets = targets.filter(t => !fs.existsSync(t.file)).map(t => t.file);
  if (missingTargets.length) throw new Error('尚未生成目标 HTML：' + missingTargets.join(', '));
  const browser = await chromium.launch({
    executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', headless: true
  });
  const results = [];
  try {
    for (const target of targets) {
      const page = await browser.newPage();
      const errors = [], requests = [], decodeErrors = [];
      page.on('pageerror', e => errors.push(String(e)));
      page.on('request', r => {if (/^https?:/.test(r.url())) requests.push(r.url());});
      const views = [];
      for (const width of [1440, 390]) {
        await page.setViewportSize({width, height: width === 390 ? 844 : 1080});
        await page.goto(pathToFileURL(target.file).href, {waitUntil: 'load'});
        await page.evaluate(() => document.fonts.ready);
        const imageErrors = await page.evaluate(async () => {
          const failures = [];
          await Promise.all([...document.images].map(async image => {
            image.loading = 'eager';
            try {await image.decode();} catch (error) {failures.push({alt: image.alt, error: String(error)});}
          }));
          return failures;
        });
        decodeErrors.push(...imageErrors);
        const view = await inspect(page);
        views.push(view);
        await page.screenshot({path: path.join(screenshots, `${target.name}_${width}_top.png`)});
        if (view.plotHeading?.id) {
          await page.locator(`[id="${view.plotHeading.id}"]`).scrollIntoViewIfNeeded();
          await page.screenshot({path: path.join(screenshots, `${target.name}_${width}_plots.png`)});
        }
      }
      const firstDetails = page.locator('details').first();
      const beforeToggle = await firstDetails.evaluate(e => e.open);
      await firstDetails.locator('summary').click();
      const detailsOperable = await firstDetails.evaluate(e => e.open) !== beforeToggle;
      await page.evaluate(() => document.querySelectorAll('details').forEach(e => {e.open = true;}));
      views.push({...await inspect(page), expanded: true});
      await page.screenshot({path: path.join(screenshots, `${target.name}_390_expanded.png`)});
      await page.setViewportSize({width: 1440, height: 1080});
      const figures = page.locator('figure');
      for (let i = 0; i < await figures.count(); i++) {
        if (target.name === 'waveform' && [0, 1, 2, 12, 13, 14, 24, 25, 26].includes(i)) {
          await figures.nth(i).screenshot({path: path.join(screenshots, `${target.name}_figure_${i + 1}.png`)});
        }
      }
      const missingFiles = views[0].links.filter(h => !h.startsWith('#') && !/^[\w+-]+:/.test(h))
        .map(h => ({href: h, file: fileURLToPath(new URL(h.split('#')[0], pathToFileURL(target.file)))}))
        .filter(item => !fs.existsSync(item.file));
      const issues = [];
      if (errors.length) issues.push('页面脚本错误');
      if (requests.length) issues.push('外部网络资源');
      if (decodeErrors.length) issues.push('图片解码失败');
      if (missingFiles.length) issues.push('本地链接缺失');
      if (!detailsOperable) issues.push('图组折叠控制失效');
      const expectedFigures = target.name === 'waveform' ? 36 : 12;
      if (views[0].figureCount !== expectedFigures) issues.push(`图数 ${views[0].figureCount}，预期 ${expectedFigures}`);
      for (const view of views) {
        if (view.overflow) issues.push(`${view.width}px 页面横向溢出`);
        if (view.mathErrors.length) issues.push(`${view.width}px 数学渲染错误`);
        if (!view.mathCount) issues.push(`${view.width}px 未渲染数学`);
        if (view.rawDollarCount) issues.push(`${view.width}px 残留数学分隔符`);
        if (view.badAnchors.length) issues.push(`${view.width}px 锚点缺失`);
        if (view.duplicateIds.length) issues.push(`${view.width}px 重复 ID`);
        if (view.images.some(i => !i.decoded)) issues.push(`${view.width}px 图片未加载`);
        if (!view.plotHeading) issues.push(`${view.width}px 未找到波形节`);
      }
      results.push({name: target.name, file: target.file, status: issues.length ? 'failed' : 'passed', issues, errors, requests, decodeErrors, missingFiles, detailsOperable, views});
      await page.close();
    }
  } finally {
    await browser.close();
  }
  const result = {status: results.every(r => r.status === 'passed') ? 'passed' : 'failed', results};
  fs.writeFileSync(path.join(__dirname, 'html_validation.json'), JSON.stringify(result, null, 2));
  console.log(JSON.stringify({status: result.status, pages: results.map(r => ({
    name: r.name, status: r.status, issues: r.issues,
    views: r.views.map(v => ({width: v.width, overflow: v.overflow, math: v.mathCount, plotHeading: v.plotHeading, plotFigures: v.plotFigures.length, images: v.images.length, badAnchors: v.badAnchors, duplicateIds: v.duplicateIds})),
    errors: r.errors, missingFiles: r.missingFiles
  }))}, null, 2));
  if (result.status !== 'passed') process.exitCode = 1;
})().catch(error => {console.error(error); process.exitCode = 1;});
