const fs = require('fs');
const path = require('path');
const root = __dirname;
const katex = require(path.join(root, '..', 'gsg_project', 'dlw_report', '_assets', 'package', 'dist', 'katex.min.js'));
const html = fs.readFileSync(path.join(root, 'GSG_STYLE_REPORT.html'), 'utf8');
const decode = s => s.replace(/&quot;/g, '"').replace(/&#x27;|&#39;/g, "'")
  .replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
const maths = [...html.matchAll(/<(div|span) class="math-(display|inline)" data-tex="([^"]*)"/g)]
  .map(m => ({tex: decode(m[3]), display: m[2] === 'display'}));
const errors = [];
for (let i = 0; i < maths.length; i++) {
  try { katex.renderToString(maths[i].tex, {displayMode: maths[i].display,
    throwOnError: true, strict: 'ignore'}); }
  catch (e) { errors.push({index: i, tex: maths[i].tex, error: String(e)}); }
}
const body = html.split('<main>')[1].split('</main>')[0];
const images = [...body.matchAll(/<img\b/g)].length;
const output = {math_count: maths.length, image_count: images,
  leftover_tokens: (html.match(/MATHTOKEN\d+END/g) || []).length,
  katex_errors: errors};
fs.writeFileSync(path.join(root, 'out', 'extended_report_validation.json'), JSON.stringify(output,null,2));
console.log(JSON.stringify({math_count: output.math_count, image_count: images,
  leftover_tokens: output.leftover_tokens, error_count: errors.length}));
if (errors.length || output.leftover_tokens || images !== 13) process.exitCode = 1;
