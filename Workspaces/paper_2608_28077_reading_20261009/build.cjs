const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const dir = __dirname;
const root = path.resolve(dir, '../..');
const assets = path.join(root, 'Workspaces/gsg_project/dlw_report/_assets/package/dist');
const katex = require(path.join(assets, 'katex.js'));
let source = fs.readFileSync(path.join(dir, 'guide.src.html'), 'utf8');
let count = 0;
source = source.replace(/<tex( display)?>([\s\S]*?)<\/tex>/g, (_, display, tex) => {
  count++;
  const rendered = katex.renderToString(tex.replace(/&amp;/g, '&').replace(/&gt;/g, '>').trim(), {
    displayMode: Boolean(display), output: 'htmlAndMathml', throwOnError: true,
  });
  return display ? '<div class="equation">' + rendered + '</div>' : rendered;
});
let css = fs.readFileSync(path.join(assets, 'katex.min.css'), 'utf8');
css = css.replace(/url\(([^)]+)\)/g, (match, relative) => {
  relative = relative.replace(/["']/g, '');
  const data = fs.readFileSync(path.join(assets, relative));
  const ext = path.extname(relative).slice(1);
  return 'url(data:font/' + (ext === 'ttf' ? 'ttf' : ext) + ';base64,' + data.toString('base64') + ')';
});
source = source.replace('__KATEX_CSS__', css);
source = source.replace('__FIGURE4__', 'data:image/png;base64,' + fs.readFileSync(path.join(dir, 'page-24.png')).toString('base64'));
const output = path.join(root, 'report/mch_ldg_2608_28077_reading.html');
fs.writeFileSync(output, source, 'utf8');
const result = {output, mathCount:count, bytes:Buffer.byteLength(source), sha256:crypto.createHash('sha256').update(source).digest('hex')};
fs.writeFileSync(path.join(dir, 'build_validation.json'), JSON.stringify(result, null, 2));
console.log(JSON.stringify(result));
