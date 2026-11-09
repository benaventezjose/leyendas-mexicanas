#!/usr/bin/env node
// Render SVG files to PNG with resvg. Usage:
//   node /home/claude/pipeline/render_svg.js file1.svg [file2.svg ...] [--width 2400] [--out DIR]
// Output: same name with .png (or into --out DIR). Fonts in /home/claude/pipeline/fonts are loaded:
//   Anton, Cinzel, IM FELL English, Rye, Oswald, plus system Lora, Poppins, DejaVu.
const path = require('path');
const fs = require('fs');
const { Resvg } = require(path.join(__dirname, 'node/node_modules/@resvg/resvg-js'));
const FONTDIR = path.join(__dirname, 'fonts');
const fontFiles = fs.readdirSync(FONTDIR).filter(f => f.endsWith('.ttf')).map(f => path.join(FONTDIR, f));
const args = process.argv.slice(2);
let width = null, outDir = null; const files = [];
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--width') width = parseInt(args[++i]);
  else if (args[i] === '--out') outDir = args[++i];
  else files.push(args[i]);
}
let failed = 0;
for (const f of files) {
  try {
    const svg = fs.readFileSync(f, 'utf8');
    const opts = { font: { fontFiles, loadSystemFonts: true, defaultFontFamily: 'Lora' }, background: 'rgba(0,0,0,0)' };
    if (width) opts.fitTo = { mode: 'width', value: width };
    const png = new Resvg(svg, opts).render().asPng();
    const out = outDir ? path.join(outDir, path.basename(f).replace(/\.svg$/i, '.png')) : f.replace(/\.svg$/i, '.png');
    fs.writeFileSync(out + '.tmp', png); fs.renameSync(out + '.tmp', out);
    console.log('ok', out);
  } catch (e) { failed++; console.error('FAIL', f, e.message); }
}
process.exit(failed ? 1 : 0);
