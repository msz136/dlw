const fs = require('node:fs');
const katex = require('../gsg_project/dlw_report/_assets/package/dist/katex.js');
const formulas = JSON.parse(fs.readFileSync(0, 'utf8'));
process.stdout.write(JSON.stringify(formulas.map(({tex, display}) =>
  katex.renderToString(tex, {displayMode:display, throwOnError:true,
    strict:'ignore', trust:false, output:'htmlAndMathml'}))));
