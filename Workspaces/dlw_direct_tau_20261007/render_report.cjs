const fs = require('node:fs');
const path = require('node:path');
const katex = require('../gsg_project/dlw_report/_assets/package/dist/katex.js');
let html = fs.readFileSync(path.join(__dirname, 'report_source.html'), 'utf8');
let count = 0;
html = html.replace(/\\\[([\s\S]*?)\\\]|\\\(([\s\S]*?)\\\)/g, (_, display, inline) => {
  count++;
  const rendered = katex.renderToString(display ?? inline, {displayMode: display !== undefined, throwOnError: true, strict: 'error'});
  return display !== undefined ? `<div class="math-display">${rendered}</div>` : rendered;
});
const output = path.resolve(__dirname, '../../report/dlw_direct_tau.html');
fs.writeFileSync(output, html, 'utf8');
fs.writeFileSync(path.join(__dirname, 'render_validation.json'), JSON.stringify({success: true, math: count, report: output}, null, 2)+'\n');
console.log(JSON.stringify({success: true, math: count, output}));
