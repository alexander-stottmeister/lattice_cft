/* Run every widget's draw() outside a browser against a stub canvas.
 *
 *     node tools/check_widgets.mjs
 *
 * Catches what a screenshot cannot: an exception in a widget the reader has not clicked to
 * yet, a readout that renders NaN, or a plot with no finite data. Exits non-zero on failure.
 */
import { readFileSync } from 'fs';

/* --- the smallest DOM the plotter needs ------------------------------------------- */
const calls = [];
const ctx2d = new Proxy({}, { get: (_, k) => {
  if (k === 'canvas') return null;
  if (k === 'measureText') return () => ({ width: 10 });
  return (...a) => { calls.push([String(k), a]); };
} });
globalThis.window = { devicePixelRatio: 1 };
globalThis.devicePixelRatio = 1;
globalThis.matchMedia = () => ({ matches: false, addEventListener() {} });
const makeCanvas = () => ({ clientWidth: 900, clientHeight: 340, width: 0, height: 0,
                            getContext: () => ctx2d });

const { WIDGETS } = await import('../docs/assets/widgets.js');
const base = new URL('../docs/data/', import.meta.url);
const ctx = {
  filters: JSON.parse(readFileSync(new URL('filters.json', base))),
  recorded: JSON.parse(readFileSync(new URL('recorded.json', base))),
  results: JSON.parse(readFileSync(new URL('results.json', base))),
};

let bad = 0;
for (const w of WIDGETS) {
  /* sweep each control across its range, not just the default */
  const grid = [{}];
  for (const c of w.controls) {
    const vals = c.type === 'check' ? [0, 1]
      : [c.min, c.value, c.max].filter((v, i, a) => a.indexOf(v) === i);
    const next = [];
    for (const g of grid) for (const v of vals) next.push({ ...g, [c.k]: v });
    grid.length = 0; grid.push(...next);
  }
  let fails = [];
  for (const p of grid) {
    calls.length = 0;
    try {
      const out = w.draw(makeCanvas(), p, ctx);
      if (typeof out !== 'string' || !out.trim()) fails.push([p, 'empty readout']);
      else if (/NaN|Infinity|undefined/.test(out)) fails.push([p, 'readout has ' + out.match(/NaN|Infinity|undefined/)[0]]);
      else if (!calls.some(([k]) => k === 'stroke' || k === 'fill' || k === 'arc'))
        fails.push([p, 'nothing drawn']);
    } catch (e) { fails.push([p, e.message]); }
  }
  const mark = fails.length ? 'FAIL' : ' ok ';
  console.log(`  [${mark}] ${w.id.padEnd(13)} ${String(grid.length).padStart(3)} parameter combinations`);
  for (const [p, why] of fails.slice(0, 3)) {
    bad++; console.log(`         ${JSON.stringify(p)} -> ${why}`);
  }
}
console.log(bad ? `\n  ${bad} failure(s)` : `\n  all ${WIDGETS.length} widgets render for every combination`);
process.exit(bad ? 1 : 0);
